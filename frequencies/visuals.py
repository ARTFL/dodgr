# -*- coding: utf-8 -*-

import itertools

def get_freqs(word, db, Row):
    freqs = db.query('year, score', 'word_frequencies', word)
    freq_by_year = {}
    for i in xrange(len(freqs)):
        freq_by_year[freqs[i]['year']] = freqs[i]['score']
    return freq_by_year
    