# -*- coding: utf-8 -*-

import re
import itertools
import MySQLdb
from tornado.database import Row
from operator import itemgetter
from pylons import config


def get_sentences(sentence_db, word, db, limit=20):
    """Return a list of all sentences in each database"""
    
    #TODO set the number of sentences before query?
    
    if sentence_db == 'corpasentences_utf8':
        corpasentences = db.query("""SELECT id, content, score FROM corpasentences_utf8 WHERE headword = %s ORDER BY score DESC""", word)[:limit]
        return corpasentences
        
    elif sentence_db == 'littresentences_utf8':
        littresentences = db.query("""SELECT id, content, source, score
                                    FROM littresentences_utf8
                                    WHERE headword = %s ORDER BY score DESC""", word)[:limit]
        return littresentences
        
    elif sentence_db == 'websentences_utf8':

        websentences = db.query("""SELECT id, content, source, link, score
                                FROM websentences_utf8
                                WHERE headword = %s ORDER BY score DESC""", word)[:limit]
        link_pattern = re.compile('(\w+\.)+\w+\/')
        for sentence in websentences:
            if not link_pattern.match(sentence['link']):
                sentence['link'] = None
        return websentences
        
    
        
        
       