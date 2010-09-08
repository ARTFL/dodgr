"""Dictionary models"""
import json
import MySQLdb
import entries


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
    """A dictionary stored in MySQL tables"""

    def __init__(self, name, citation, mapper, cursor, loader=None):
        self.name = name
        self.citation = citation
        self.mapper = mapper
        self.cursor = cursor
        if loader:
            self._build(loader)

    def __len__(self):
        pass

    def __iter__(self):
        pass

    def _build(self, loader):
        """Build the dictionary data tables from the loader data"""

        # Setup the initial tables
        entry_table = self.name + '_entries'
        index_table = self.name + '_index'
        self.cursor.execute('DROP TABLE IF EXISTS `' + entry_table + '`')
        self.cursor.execute('DROP TABLE IF EXISTS `' + index_table + '`')
        self.cursor.execute("""CREATE TABLE `""" + entry_table + """` (
                            `id` int(11) NOT NULL AUTO_INCREMENT,
                            `entry` mediumtext CHARACTER SET utf8,
                            PRIMARY KEY (`id`))
                            ENGINE=MyISAM
                            DEFAULT CHARSET=utf8;""")
        self.cursor.execute("""CREATE TABLE `""" + index_table + """` (
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

            self.cursor.execute("""INSERT INTO `""" + entry_table + """`
                           (entry) VALUES (%s)""", json.dumps(entry_input))
            for headword in entry_input['headwords']:
                citation_form = self.mapper.citation_form(headword[0])
                self.cursor.execute("""INSERT INTO `""" + index_table + """`
                               (headword, entry_id) VALUES (%s, %s)""",
                               (citation_form, entry_id))
            entry_id += 1

    def define(self, word):
        """Return a list of all entries for a word"""

        entry_table = self.name + '_entries'
        index_table = self.name + '_index'
        self.cursor.execute("""SELECT `""" + entry_table + """`.entry
                            FROM `""" + entry_table + """`
                            LEFT JOIN `""" + index_table + """`
                            ON `""" + index_table + """`.entry_id
                            = `""" + entry_table + """`.id
                            WHERE `""" + index_table + """`.headword = %s""",
                            word)
        entry_rows = self.cursor.fetchall()
        entry_list = []
        for entry_row in entry_rows:
            entry_dict = json.loads(entry_row[0])
            entry_list.append(entries.Entry(prop_dict=entry_dict))

        return entry_list

    def get_entry(self, entry_id):
        """Return a specific entry by id"""
        try:
            return self._entries[entry_id]
        except IndexError:
            return None

class Stack(object):
    """Container for a collection of dictionaries"""

    def __init__(self, dicos=[]):
        """Create the stack"""
        self.dicos = []
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
        self.index.sort()

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
