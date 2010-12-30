# -*- coding: utf-8 -*-
"""Dictionary models"""
import json
import bisect
import MySQLdb
import entries
import locale
import copy
from dodgr.lib.helpers import custom_sorting
from difflib import get_close_matches


class Simple(object):
    """A very simple dictionary, with only headwords and defintions"""

    def __init__(self, loader):
        self.loader = loader.load()
        self._index = {}
        self._headwords = []
        self._definitions = []
        self._build()

    def __len__(self):
        return len(self._headwords)

    def __iter__(self):
        for i in range(len(self)):
            yield (self._headwords[i], self._definitions[i])

    def _build(self):
        """Build the dictionary object from the loader data"""
        entry_id = 0
        for headword, definition in self.loader:
            try:
                self._index[headword].append(entry_id)
            except KeyError:
                self._index[headword] = [entry_id]
            self._headwords.append(headword)
            self._definitions.append(definition)
            entry_id += 1

    def define(self, word):
        """Return a list of all entries for a word"""
        try:
            entry_ids = self._index[word]
        except KeyError:
            return
        return [(self._headwords[id], self._definitions[id])
                                for id in entry_ids]


class EntryBased(object):
    """A dictionary organized as a collection of Entry objects"""

    def __init__(self, name, citation, loader, mapper):
        self.name = name
        self.citation = citation
        self.mapper = mapper
        self._index = {}
        self._headwords = []
        self._entries = []
        self._build(loader)

    def __len__(self):
        return len(self._entries)

    def __iter__(self):
        for i in range(len(self)):
            yield self._entries[i]

    def _build(self, loader):
        """Build the dictionary object from the loader data"""
        entry_id = 0
        for entry_input in loader.load():
            # Don't build entries if there are errors
            if 'error' in entry_input and entry_input['error']:
                continue

            entry = entries.Entry(prop_dict=entry_input)
            self._entries.append(entry)
            for headword, pos in entry.headwords:
                # Only the citation form of the headword goes into the
                # _headwords lists, so you can iterate the list and get
                # a list of good citation forms. Other forms do get indexed
                # though.
                citation_form = self.mapper.citation_form(headword)
                self._headwords.append(citation_form)
                forms = self.mapper.index_forms(citation_form)
                for form in forms:
                    try:
                        self._index[form].append(entry_id)
                    except KeyError:
                        self._index[form] = [entry_id]

            entry_id += 1

    def define(self, word):
        """Return a list of all entries for a word"""
        try:
            entry_ids = self._index[word]
        except KeyError:
            return None
        return [self._entries[id] for id in entry_ids]

    def get_entry(self, entry_id):
        """Return a specific entry by id"""
        try:
            return self._entries[entry_id]
        except IndexError:
            return None


class MySQLBased(object):
    """A dictionary stored in MySQL tables. Uses the tornado database MySQLdb
    wrapper."""

    def __init__(self, name, citation, mapper, db, loader=None,
                 truncate=False, full_entry_url=None):
        self.name = name
        self.citation = citation
        self.mapper = mapper
        self.db = db
        self.entry_table = self.name + '_entries'
        self.index_table = self.name + '_index'
        self.truncate = truncate
        self.full_entry_url = full_entry_url

        if loader:
            self._build(loader)

    def __len__(self):
        pass

    # TODO -- MySQLBased and EntryBased should yield the same kind
    # of thing on iteration; right now, EntryBased gives out Entries;
    # MySQLBased gives out headwords.
    def __iter__(self):
        """Fetch all the headwords from the index table"""
        index_table = self.name + '_index'
        for row in self.db.query("""SELECT headword FROM `%s`""" % \
                                 self.index_table):
            yield row['headword']

    def _build(self, loader):
        """Build the dictionary data tables from the loader data"""

        # Setup the initial tables
        entry_table = self.name + '_entries'
        index_table = self.name + '_index'
        self.db.execute('DROP TABLE IF EXISTS `' + entry_table + '`')
        self.db.execute('DROP TABLE IF EXISTS `' + index_table + '`')
        self.db.execute("""CREATE TABLE `""" + entry_table + """` (
                            `id` int(11) NOT NULL AUTO_INCREMENT,
                            `entry` mediumtext CHARACTER SET utf8,
                            PRIMARY KEY (`id`))
                            ENGINE=MyISAM
                            DEFAULT CHARSET=utf8;""")
        self.db.execute("""CREATE TABLE `""" + index_table + """` (
                            `id` int(11) NOT NULL AUTO_INCREMENT,
                            `headword` varchar(255) CHARACTER SET utf8,
                            `entry_id` int,
                            PRIMARY KEY (`id`))
                            ENGINE=MyISAM
                            DEFAULT CHARSET=utf8;""")

        entry_id = 1
        for entry_input in loader.load():
            # Don't build entries if there are errors
            if 'error' in entry_input and entry_input['error']:
                continue

            self.db.execute("""INSERT INTO `""" + entry_table + """`
                            (entry) VALUES (%s)""", json.dumps(entry_input))
            for headword in entry_input['headwords']:
                citation_form = self.mapper.citation_form(headword[0])
                self.db.execute("""INSERT INTO `""" + index_table + """`
                                (headword, entry_id) VALUES (%s, %s)""",
                                (citation_form, entry_id))
            entry_id += 1

    def define(self, word):
        """Return a list of all entries for a word"""

        entry_table = self.name + '_entries'
        index_table = self.name + '_index'
        entry_rows = self.db.query("""SELECT `""" + entry_table + """`.entry
                                   AS entry
                                   FROM `""" + entry_table + """`
                                   LEFT JOIN `""" + index_table + """`
                                   ON `""" + index_table + """`.entry_id
                                   = `""" + entry_table + """`.id
                                   WHERE `""" + index_table + \
                                   """`.headword = %s""",
                                   word)
        entry_list = []
        truncated_entries = 1
        for row in entry_rows:
            entry_dict = json.loads(row['entry'])
            entry_dict['searched_headword'] = word
            if self.truncate:
                if truncated_entries:
                    truncated_entries = 0
                    entry_list.append(entries.TruncatedEntry(
                                        prop_dict=entry_dict,
                                        length=self.truncate,
                                        full_entry_url=self.full_entry_url))
            else:
                entry_list.append(entries.Entry(prop_dict=entry_dict))
        return entry_list

    def get_entry(self, entry_id):
        """Return a specific entry by id"""
        # TODO implement this
        pass

class Stack(object):
    """Container for a collection of dictionaries"""

    def __init__(self, dicos=[]):
        """Create the stack"""
        self.dicos = []
        self.index = []
        for dico in dicos:
            self.add_dico(dico)

    def __len__(self):
        """Length of the stack is the number of dicos it contains"""
        return len(self._dicos)

    def __iter__(self):
        """Yielded dicos upon iteration"""
        for i in range(len(self)):
            yield self.dicos[i]

    def add_dico(self, dico):
        """Load a dico into the stack"""
        self.dicos.append(dico)
        for headword in dico:
            self.index.append(headword)
        self.index = list(set(self.index))
        self.index = sorted(self.index, key=custom_sorting)
        ## this function doesn't work on Macs
        #locale.setlocale(locale.LC_ALL, "en_US.UTF-8")
        #self.index.sort(cmp=locale.strcoll)

    def define(self, word):
        """Return a list of all entries for a word"""
        dico_entries = []
        for dico in self.dicos:
            entries = dico.define(word)
            if entries:
                dico_entries.append((dico.name, dico.citation, entries))
        if dico_entries:
            return dico_entries
        else:
            return None

    # TODO this shouldn't be a MySQL-only thing, it should work off an API
    # that EntryBased dicos also expose
    def index_neighbors(self, word, distance=20):
        """Fetch all the neighboring headwords from the index table"""
        if word in self.index:
            word_id = self.index.index(word)
            start = word_id - distance
            if start < 0:
                start = 0
            stop = word_id + distance + 1
            return self.index[start:stop]
        else:
            index = copy.copy(self.index)
            index.append(word)
            index = sorted(index, key=custom_sorting)
            word_id = index.index(word)
            start = word_id - distance
            if start < 0:
                start = 0
            stop = word_id + distance
            return index[start:stop]
                   
                   
    def fuzzy_matching(self, word):
        matches = get_close_matches(word, self.index, 4)
        return matches
      
    
        
        
        
