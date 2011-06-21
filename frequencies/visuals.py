# -*- coding: utf-8 -*-

import itertools

def get_freqs(word, db, Row):
    freqs = db.query("""select year, score from word_frequencies where word = ?""", (word,))
    freq_by_year = {}
    for i in xrange(len(freqs)):
        freq_by_year[freqs[i]['year']] = freqs[i]['score']
    return freq_by_year
    