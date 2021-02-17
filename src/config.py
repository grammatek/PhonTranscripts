"""
Creates the configuration file needed by the module

Change the phonetic alphabet if you are not using SAMPA as defined for the Icelandic Pronunciation Dicaitonry.
Adjust the path for the database if needed.

"""

import configparser

config = configparser.ConfigParser()
config['ALPHABET'] = {}
config['ALPHABET']['VOWELS'] = 'sampa_vowels.txt'
config['ALPHABET']['CONS_CLUSTERS'] = 'sampa_consclusters.txt'
config['DB'] = {}
config['DB']['DB_PATH'] = '../data/dictionary.db'

with open('transcription.conf', 'w') as configfile:
    config.write(configfile)