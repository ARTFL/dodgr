# -*- coding: utf-8 -*-
    
def pull_lemma(db, word):
    query = db.query('lemma', 'word2lemma', word=word)
    try:
        return query[0]['lemma'].decode('utf-8').rstrip('\n')
    except IndexError:
        raise KeyError
        
def pull_forms(db, lemma):
    query = db.query('words', 'lemma2words', word=lemma)
    try:
        return query[0]['words'].decode('utf-8').rstrip('\n').split(',')
    except IndexError:
        raise KeyError
    
