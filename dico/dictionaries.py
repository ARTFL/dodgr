"""Dictionary models"""
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

    def __init__(self, loader, mapper):
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
