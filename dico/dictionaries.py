"""Dictionary models"""


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
