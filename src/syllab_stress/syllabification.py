
"""

Perform syllabification on words transcribed with X-SAMPA, or whatever alphabet defined in transcription.conf.
Syllable rules for Icelandic as described in:
    - Anton Karl Ingason (2006): Íslensk atkvæði - vélræn nálgun. (http://www.linguist.is/skjol/atkvadi.pdf)
    - Kristján Árnason (2005): Hljóð. Ritröðin Íslensk tunga.

The basic assumption is that Icelandic syllable structure follows the onset-rhyme model. From this follows that,
whenever possible, a syllable has a 'need' for an onset consonant. This contradicts in some cases with rules for
'between-the-lines' word division rules saying that a word should be divided between lines
such that the next line starts with a vowel: 'hes.tur' vs. 'hest.ur'.

The following consonant combinations always build an onset together:

    s, p, t, k + v, j, r    (sv, sj, sr, pv, pj, pr, etc.)
    fr

# input: transcribed and aligned word, example: a v p r I G D I (afbrigði)
# output: syllabified word: af.prIG.DI (af.brig.ði)

# algorithm:
# 1) symbols upto the second vowel build the first syllable: 'afpr'
# 2) the remaining string is divided into syllables each starting with a vowel: 'afpr.IGD.I'
# 3) identify cons cluster: 'af(pr).IGD.I'
# 4) move consonants to onset (cons clusters and single consonants): 'af.prIG.DI'

This algorithm normally gives correct results for simple words, but can produce errors when applied to compounds.
Thus it is important to perform compound analysis before applying the core syllabification algorithm.

"""

from . import syllable
from entry import PhonDict


def syllabify_on_nucleus(transcription_arr):
    """
    First round of syllabification. Divide the word such that each syllable
    starts with a vowel (except the first one, if the word starts with a consonant/consonants).
    """
    syllables = []
    current_syllable = syllable.Syllable()
    for phone in transcription_arr:
        if current_syllable.has_nucleus and phone in PhonDict.get_alphabet().vowels:
            syllables.append(current_syllable)
            current_syllable = syllable.Syllable()

        if phone in PhonDict.get_alphabet().vowels:
            current_syllable.has_nucleus = True

        current_syllable.append(phone)
    # append last syllable
    syllables.append(current_syllable)
    return syllables


def identify_clusters(entry):
    for syll in entry.syllables:
        for clust in PhonDict.get_alphabet().cons_clusters:
            if syll.content.strip().endswith(clust):
                syll.cons_cluster = clust


def syllabify_final(entry):
    """
    Iterate once more over the syllable structure and move consonants from rhyme to onset
    where appropriate, i.e. where one syllable ends with a consonant and the
    next one starts with a vowel. If a syllable ends with a consonant cluster, the whole
    cluster is moved to the next syllable, otherwise only the last consonant.
    However, if a syllable has a fixed boundary (as a result of decompounding), end or start,
    the boundary can not be changed.
    """

    for ind, syll in enumerate(entry.syllables):
        if ind == 0:
            continue
        prev_syll = entry.syllables[ind - 1]
        # syllable after the first syllable starts with a vowel - look for consonant onset in previous syllable
        # and move the consonant / consonant cluster from the previous to the current syllable
        if ind > 0 and syll.content[0] in PhonDict.get_alphabet().vowels:
            if prev_syll.cons_cluster:
                # copy cons_cluster to next syllable
                syll.append_before(prev_syll.cons_cluster)
                prev_syll.remove_cluster()
                entry.update_syllables(ind, prev_syll, syll)
            elif prev_syll.last_phones() not in PhonDict.get_alphabet().vowels:
                # handle 'jE' (=é) as one vowel
                if prev_syll.endswith('j') and syll.startswith('E'):
                    phone = prev_syll.last_phones(1)
                    syll.append_before(phone)
                    prev_syll.content = prev_syll.content[:-(len(phone)+1)]
                else:
                    phone = prev_syll.last_phones()
                    syll.append_before(phone)
                    prev_syll.content = prev_syll.content[:-(len(phone)+1)]
                entry.update_syllables(ind, prev_syll, syll)


def syllabify_entry(entry):

    entry.syllables = syllabify_on_nucleus(entry.transcription_arr)
    identify_clusters(entry)
    syllabify_final(entry)


def syllabify_tree(entry_tree, syllables):
    """
    Recursively call syllabification on each element of entry_tree.
    Add up the syllables of the leaf nodes to build the syllable structure of the root element.
    :param entry_tree: a binary tree of a compound structure, the tree might not have any leaves,
    i.e. is not necessarily a compound
    :param syllables: an array to add up the leaf syllables of the tree
    :return:
    """
    if not entry_tree.left:
        syllabify_entry(entry_tree.elem)
        syllables += entry_tree.elem.syllables
    if entry_tree.left:
        syllabify_tree(entry_tree.left, syllables)
    if entry_tree.right:
        syllabify_tree(entry_tree.right, syllables)


def syllabify_tree_dict(tree_dict):
    """
    Syllabifies each entry in tree_dict
    :param tree_dict: a list of compoundTrees to syllabify
    :return: a list of syllabified PronDictEntries. Note that the returned list does NOT contain tree elements any more,
    but simple PronDictEntries.
    """
    syllabified = []
    for t in tree_dict:
        syllables = []
        syllabify_tree(t, syllables)
        t.elem.syllables = syllables
        syllabified.append(t.elem)

    return syllabified



