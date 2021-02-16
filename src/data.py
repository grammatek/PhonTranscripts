import os
import configparser


class PhoneticData:

    def __init__(self, configfile='transcription.conf', working_dir=None):
        if working_dir:
            current_dir = working_dir
        else:
            current_dir = os.getcwd() + '/'

        config = configparser.ConfigParser()
        config.read(current_dir + configfile)

        alphabet = config['ALPHABET']
        vowels_file = current_dir + alphabet.get('vowels')
        clusters_file = current_dir + alphabet.get('cons_clusters')
        self.vowels = self.init_list_from_file(vowels_file)
        self.cons_clusters = self.init_list_from_file(clusters_file)

    @staticmethod
    def init_list_from_file(filename: str):
        with open(filename) as f:
            return f.read().splitlines()
