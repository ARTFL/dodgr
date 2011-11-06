# -*- coding: utf-8 -*-

import re

def get_sentences(sentence_db, word, db, limit=10):
    """Return a list of all sentences in each database"""
    #TODO set the number of sentences before query?
    args = 'ORDER BY score DESC, defsim DESC LIMIT %d' % limit
    if sentence_db == 'corpasentences':
        corpasentences = db.query("id, content, score", sentence_db, word, args=args)
        return corpasentences
        
    elif sentence_db == 'littresentences_utf8':
        #littresentences = db.query('''SELECT id, content, source, score
                                    #FROM littresentences_utf8
                                    #WHERE headword = "%s" collate utf8_bin ORDER BY score DESC LIMIT %d''' % (word, limit))
        #return littresentences
        return []
        
    elif sentence_db == 'websentences':
        websentences = db.query('id, content, source, link, score', sentence_db, word, args=args)
        link_pattern = re.compile('(\w+\.)+\w+\/')
        for i in xrange(len(websentences)):
            link = websentences[i]['link']
            if not link_pattern.match(link):
                websentences[i]['link'] = None
        return websentences
        
    
        
        
       
