# -*- coding: utf-8 -*-


def get_lemma(db):
    
    word2lem = {}
    for row in db.query("""SELECT word, lemma FROM word2lemma"""):
        word2lem[row['word'].decode('utf-8')] = row['lemma'].decode('utf-8').rstrip('\n')
    
    return word2lem
    
    
def get_forms(db):
    
    lem2words = {}
    for row in db.query("""SELECT lemma, words FROM lemma2words"""):
        lem2words[row['lemma'].decode('utf-8')] = row['words'].decode('utf-8').rstrip('\n').split(',')
        
    return lem2words
    
