from base import Base

class Separated(Base):
    """Load a dictionary from a tab-separated file. Expects to find one
    entry per line, with a headword, the separator, and then a definition."""

    def __init__(self, file_path, separator="\t"):
        self.separator = separator
        self.entry_id = 0
        self._file = open(file_path)

    def load(self, separator="\t"):
        """Load a separated dictionary file"""

        for line in self._file:
            entry = line.rstrip()
            try:
                yield tuple(entry.split(self.separator))
            except Exception:
                raise Exception('Could not split line: %s by separator: %s,'
                'encountered exception: %s', (line, self.separator,
                                                        Exception))
