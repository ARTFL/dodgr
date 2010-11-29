# -*- coding: utf-8 -*-

import re
from pylons import app_globals
from dodgr.lib.helpers import highlight

def get_sentences(sentence_db, word, db, limit=20):
    """Return a list of all sentences in each database"""
    
    #TODO set the number of sentences before query?
    
    if sentence_db == 'corpa':
        corpasentences = db.list("""SELECT content FROM corpasentences_utf8
                                    WHERE headword = %s""", word)
        corpasentences = corpasentences[:limit]
        corpasentences = [highlight(corpasentences[i], word) for i in range(len(corpasentences))]
        return corpasentences
        
    elif sentence_db == 'littre':
        littresentences = db.query("""SELECT content, source
                                    FROM littresentences_utf8
                                    WHERE headword = %s""", word)
        littresentences = littresentences[:limit]
        for i in range(len(littresentences)):
            littresentences[i]['content'] = highlight(littresentences[i]['content'], word)
        return littresentences
        
    elif sentence_db == 'web':
        websentences = db.query("""SELECT content, source, link
                                FROM websentences_utf8
                                WHERE headword = %s""", word)
        websentences = websentences[:limit]
        link_pattern = re.compile('(\w+\.)+\w+\/')
        for i in range(len(websentences)):
            link = websentences[i]['link']
            if not link_pattern.match(link):
                websentences[i]['link'] = None
            websentences[i]['content'] = highlight(websentences[i]['content'], word)
        return websentences
        
       