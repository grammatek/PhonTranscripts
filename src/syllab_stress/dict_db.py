

import sys
import sqlite3

from data import DBPath

class DictDB:
    # Pron dict tables
    SQL_CREATE_FROB_TABLE = 'CREATE TABLE IF NOT EXISTS frob(id INTEGER PRIMARY KEY, word TEXT, ' \
                     'transcript TEXT) '
    SQL_INSERT_2_FROB = 'INSERT OR IGNORE INTO frob(word, transcript) VALUES(?, ?)'
    SQL_SELECT_TRANSCR_FROM_FROB = 'SELECT * FROM frob'

    # Compound tables
    SQL_SELECT_FROM_COMP = 'SELECT * FROM compound_transcr'
    SQL_SELECT_COMPOUND = 'SELECT * FROM compound_transcr WHERE word = ?'
    SQL_SELECT_MODIFIERS = 'SELECT * FROM compound_transcr WHERE modifier = ?'
    SQL_SELECT_HEADS = 'SELECT * FROM compound_transcr WHERE head = ?'

    def __init__(self):
        self.db_path = DBPath().db_path

    def create_connection(self):
        try:
            conn = sqlite3.connect(self.db_path)
            return conn
        except sqlite3.Error as e:
            print(e)
        return None

    def open_connection(self):
        return self.create_connection()

    def populate_frob_database(self, dict_list):
        db = self.create_connection(self.db_path)
        db.execute(self.SQL_CREATE_FROB_TABLE)
        for entry in dict_list:
            db.execute(self.SQL_INSERT_2_FROB, (entry[0], entry[1]))

        db.commit()

    def get_transcriptions_map(self):
        conn = self.create_connection()
        result = conn.execute(self.SQL_SELECT_TRANSCR_FROM_FROB)
        transcriptions = result.fetchall()
        transcr_dict = {}
        for transcr in transcriptions:
            transcr_dict[transcr[1]] = transcr[2]

        return transcr_dict

    def get_compound(self, wordform, conn):
        result = conn.execute(self.SQL_SELECT_COMPOUND, (wordform,))
        compound = result.fetchone()
        if compound:
            return compound[1], compound[2], compound[3]

    def create_map(self, comp_list, key_index, val_index):
        comp_map = {}
        for comp in comp_list:
            if comp[key_index] in comp_map:
                comp_map[comp[key_index]].append(comp[val_index])
            else:
                comp_map[comp[key_index]] = [val_index]

        return comp_map

    def get_modifier_map(self):
        conn = self.open_connection()
        result = conn.execute(self.SQL_SELECT_FROM_COMP)
        compounds = result.fetchall()
        conn.close()
        return self.create_map(compounds, 2, 3)

    def get_head_map(self):
        conn = self.open_connection()
        result = conn.execute(self.SQL_SELECT_FROM_COMP)
        compounds = result.fetchall()
        conn.close()
        return self.create_map(compounds, 3, 2)


def main():

    frob = sys.argv[1]

    frob_list = []
    for line in open(frob).readlines():
        word, transcr = line.split('\t')
        frob_list.append([word, transcr.strip()])

    db_manager = DictDB
    db_manager.populate_frob_database(frob_list)


if __name__ == '__main__':
    main()
