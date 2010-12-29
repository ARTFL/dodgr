# -*- coding: utf-8 -*-

def get_freqs(word, db):
    freqs = db.query("""SELECT year, score FROM word_frequencies WHERE word = %s""", word)
    freq_by_year = {}
    for i in range(len(freqs)):
        freq_by_year[freqs[i]['year']] = freqs[i]['score']
    return freq_by_year
    