# -*- coding: utf-8 -*-

import re
from pylons import app_globals
from dodgr.lib.helpers import highlight
from operator import itemgetter

def get_sentences(sentence_db, word, db, limit=20):
    """Return a list of all sentences in each database"""
    
    #TODO set the number of sentences before query?
    
    if sentence_db == 'corpasentences_utf8':
        corpasentences = db.query("""SELECT content, score FROM corpasentences_utf8
                                    WHERE headword = %s""", word)
        sentences = {}
        count = 0
        for sentence in sorted(corpasentences, key=itemgetter('score'), reverse=True):
            sentences[count] = {}
            sentences[count]['content'] = sentence['content']
            sentences[count]['word'] = word
            count += 1
            if count == limit:
                break
        return sentences
        
    elif sentence_db == 'littresentences_utf8':
        littresentences = db.query("""SELECT content, source, score
                                    FROM littresentences_utf8
                                    WHERE headword = %s""", word)
        sentences = {}
        count = 0
        for sentence in sorted(littresentences, key=itemgetter('score'), reverse=True):
            sentences[count] = {}
            sentences[count]['content'] = sentence['content']
            sentences[count]['source'] = sentence['source']
            sentences[count]['word'] = word
            count += 1
            if count == limit:
                break
        return sentences
        
    elif sentence_db == 'websentences_utf8':
        websentences = db.query("""SELECT content, source, link, score
                                FROM websentences_utf8
                                WHERE headword = %s""", word)
        sentences = {}
        count = 0
        link_pattern = re.compile('(\w+\.)+\w+\/')
        for sentence in sorted(websentences, key=itemgetter('score'), reverse=True):
            sentences[count] = {}
            sentences[count]['content'] = sentence['content']
            sentences[count]['source'] = sentence['source']
            if link_pattern.match(sentence['link']):
                sentences[count]['link'] = sentence['link']
            else:
                sentences[count]['link'] = None
            sentences[count]['word'] = word
            count += 1
            if count == limit:
                break
        return sentences
        
        
       