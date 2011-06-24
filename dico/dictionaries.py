# -*- coding: utf-8 -*-
"""Dictionary models"""
import cPickle
import copy
from Levenshtein import distance

        

class Stack(object):
    """Container for a collection of dictionaries"""

    def __init__(self, db, dicos=[], full_entry_url=None):
        """Create the stack"""
        self.index_dico = {}
        self.db = db
        self.add_dico(dicos)
        self.index = sorted([word for word in self.index_dico], key=self.custom_sorting)
        self.full_entry_url = full_entry_url

    def add_dico(self, dicos):
        """Load a dico into the stack"""
        for dico, citation in dicos:
            results = self.db.query('headword', dico, obj='array')
            results = [result.decode('utf-8') for result in results]
            for word in results:
                if word in self.index_dico:
                    self.index_dico[word].append((dico, citation))
                else:
                    self.index_dico[word] = []
                    self.index_dico[word].append((dico, citation))
                    
    def custom_sorting(self, word):
        """idea taken from http://code.activestate.com/recipes/576507-sort-strings-containing-german-umlauts-in-correct-/
        It's a workaround for OSX"""
        word = word.replace(u'é', u'e')
        word = word.replace(u'è', u'e')
        word = word.replace(u'ê', u'e')
        word = word.replace(u'ë', u'e')
        word = word.replace(u'à', u'a')
        word = word.replace(u'â', u'a')
        word = word.replace(u'ù', u'u')
        word = word.replace(u'û', u'u')
        word = word.replace(u'î', u'i')
        word = word.replace(u'ï', u'i')
        word = word.replace(u'ô', u'o')
        word = word.replace(u'ç', u'c')
        return word

    def define(self, word):
        """Return a list of all entries for a word"""
        dico_entries = []
        try:
            for dico, citation in self.index_dico[word]:
                results = self.db.query("entry", dico, word, obj='array')
                if len(results) != 0:
                    entries = cPickle.loads(str(results[0]))
                    if dico == 'tlfi':
                        entries['url'] = self.full_entry_url + word
                    dico_entries.append((dico, citation, entries))
        except KeyError:
            pass

        return dico_entries       

    def index_neighbors(self, word, distance=20):
        """Fetch all the neighboring headwords from the index table"""
        if word.lower() in self.index:
            word_id = self.index.index(word.lower())
            start = word_id - distance
            if start < 0:
                start = 0
            stop = word_id + distance + 1
            return self.index[start:stop]
        else:
            index = copy.copy(self.index)
            index.append(word.lower())
            index = sorted(index, key=self.custom_sorting)
            word_id = index.index(word.lower())
            start = word_id - distance
            if start < 0:
                start = 0
            stop = word_id + distance
            return index[start:stop]
        
    def fuzzy_matching(self, word):
        """Return a list of up to four words based on similarity"""
        results = dict((term, distance(word, term)) for term in set(self.index))
        return [result for result in sorted(results, key=results.get)][:4]    