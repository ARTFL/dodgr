#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb
from dodgr.lib.helpers import highlight

#blatantly copied from Russ' dictionnary classes :-)


class MySQLBased(object):
    
    def __init__(self, name, citation, db, limit):
        self.db = db
        self.name = name
        self.table = citation
        self.limit = limit


class Stack(object):
    """Container for a collection of example databases"""

    def __init__(self, exdbs=[]):
        """Create the stack"""
        self.exdbs = []
        for exdb in exdbs:
            self.add_exdb(exdb)

    def __len__(self):
        """Length of the stack is the number of dicos it contains"""
        return len(self._dicos)

    def __iter__(self):
        """Yielded dicos upon iteration"""
        for i in range(len(self)):
            yield self.dicos[i]

    def add_exdb(self, exdb):
        """Load an example db into the stack"""
        self.exdbs.append(exdb)

    def define(self, word, pattern):
        """Return a list of all entries for a word"""
        sentences_db = []
        for exdb in self.exdbs:
            if exdb == 'corpasentences_utf8':
                corpasentences = self.db.list("""SELECT content FROM corpasentences_utf8
                                            WHERE headword = %s""", word)
                corpasentences = corpasentences[:self_limit]
                corpasentences = [highlight(corpasentences[i], pattern) for i in range(len(corpasentences))]
                num_sentences += len(corpasentences)
                if (len(corpasentences) > 0):
                    num_corpora += 1
            if exdb == 'littresentences_utf8':
                littresentences = self.db.query("""SELECT content, source
                                            FROM littresentences_utf8
                                            WHERE headword = %s""", word)
                littresentences = littresentences[:self_limit]
                for i in range(len(c.littresentences)):
                    littresentences[i]['content'] = highlight(littresentences[i]['content'], pattern)
                num_sentences += len(littresentences)
                
                if (len(littresentences) > 0):
                    c.num_corpora += 1
            if exdb == 'websentences_utf8':
                websentences = self.db.query("""SELECT content, source, link
                                        FROM websentences_utf8
                                        WHERE headword = %s""", word)
                websentences = websentences[:self.limit]
                link_pattern = re.compile('(\w+\.)+\w+\/')
                
                for i in range(len(websentences)):
                    link = websentences[i]['link']
                    if not link_pattern.match(link):
                        websentences[i]['link'] = None
                    websentences[i]['content'] = highlight(websentences[i]['content'], pattern)
                num_sentences += len(websentences)
                if (len(websentences) > 0):
                    num_corpora += 1
            
            if entries:
                dico_entries.append((dico.name, dico.citation, sentences))
        if dico_entries:
            return dico_entries
        else:
            return None