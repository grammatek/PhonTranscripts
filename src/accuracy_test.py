"""
Performs accuracy tests for syllabification and stress algorithms.

Reference files should be in csv format:

word,phonetic_transcr,syllabified_phonetic_transcr

and:

word,phonetic_transcr,syllabified_phonetic_transcr_with_stress_labels

We are testing syllabification and stress labeling on transcribed words, i.e. we take as input the correct phonetic
transcription.
"""

import argparse
from datetime import datetime
import syllab_stress.tree_builder as tree_builder
import syllab_stress.syllabification as syllabification
import syllab_stress.stress as stress

from entry import PronDictEntry


def init_ref_dict(dict_file, separator):
    """Init the reference dictionary, 'ref_str' is the reference version of either a syllabified or
    a syllabified and stress labeled transcription"""

    pron_dict = []
    for line in dict_file:
        word, transcr, ref_str = line.split(separator)
        entry = PronDictEntry(word, transcr, reference=ref_str.strip())
        pron_dict.append(entry)
    return pron_dict


def create_tree_list(pron_dict):
    tb = tree_builder.TreeBuilder()
    tree_list = []
    for entry in pron_dict:
        t = tb.build_compound_tree(entry)
        tree_list.append(t)
    return tree_list


def parse_args():
    parser = argparse.ArgumentParser(description='Accuracy tests for syllabification and stress labeling')
    parser.add_argument('i', type=argparse.FileType('r'), help='Reference file')
    parser.add_argument('-t', '--type', type=str, default='syllab', choices=['syllab', 'stress'],
                        help="Type of test to run: 'syllab' or 'stress'")
    parser.add_argument('-s', '--sep', type=str, default=',', help=("Separator used in the reference file"))

    return parser.parse_args()


def main():

    args = parse_args()
    ref_file = args.i
    test_type = args.type
    separator = args.sep

    ref_dict = init_ref_dict(ref_file, separator)
    tree_dict = create_tree_list(ref_dict)
    syllabified = syllabification.syllabify_tree_dict(tree_dict)

    if test_type == 'stress':
        syllabified = stress.set_stress(syllabified)

    mismatches = []
    with open(str(datetime.now().time()) + '_' + test_type + '_mismatches.csv', 'w') as f:
        for entry in syllabified:
            if test_type == 'syllab':
                hypothesis = entry.dot_format_syllables()
            else:
                hypothesis = entry.stress_format()
            if entry.reference_transcr != hypothesis:
                mismatches.append(entry.word + '\t' + entry.reference_transcr + '\t' + hypothesis)
                f.write(entry.word + '\t' + entry.reference_transcr + '\t' + hypothesis + '\n')

    print(str(len(mismatches)))
    print(str(len(mismatches)/len(ref_dict) * 100) + '%')


if __name__ == '__main__':
    main()