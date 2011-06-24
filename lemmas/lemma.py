# -*- coding: utf-8 -*-

import itertools

def get_lemma(db):
    word2lem = {}
    query = db.query('word, lemma', 'word2lemma')
    for row in query:
        word2lem[row['word'].decode('utf-8')] = row['lemma'].decode('utf-8').rstrip('\n')
    return word2lem
    
    
def get_forms(db):
    lem2words = {}
    query = db.query('lemma, words', 'lemma2words')
    for row in query:
        lem2words[row['lemma'].decode('utf-8')] = row['words'].decode('utf-8').rstrip('\n').split(',')
    return lem2words
    
