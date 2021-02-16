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
import syllab_stress.tree_builder as tree_builder
import syllab_stress.syllabification as syllabification

from entry import PronDictEntry


def init_ref_dict(dict_file, separator):
    """Init the reference dictionary, 'ref_str' is the reference version of either a syllabified or
    a syllabified and stress labeled transcription"""

    pron_dict = []
    for line in dict_file:
        word, transcr, ref_str = line.split(separator)
        entry = PronDictEntry(word, transcr, reference=ref_str)
        pron_dict.append(entry)
    return pron_dict


def create_tree_list(pron_dict):

    tree_list = []
    for entry in pron_dict:
        t = tree_builder.build_compound_tree(entry)
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

    for entry in syllabified:
        print(entry.syllable_format())

    print(str(len(ref_dict)) + " type: " + test_type)


if __name__ == '__main__':
    main()