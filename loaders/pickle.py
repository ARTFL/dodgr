"""pickle.py
Loader class to populate a dico from a series of Python dict cPickles that
already have defined values for things like headword, pos, pron, etc.
"""
import os
import re
import cPickle
from base import Base


class Pickle(Base):
    """Load a dictionary from specially set up Python dict pickles. Pass
    either pickle_dir, a directory full of entry pickles, or pickle_file, a
    single pickle which has an iterable full of entries."""

    def __init__(self, pickle_dir=None, pickle_file=None,
                 extension=".pickle"):
        self.entry_id = 0

        if pickle_dir:
            if not os.path.isdir(pickle_dir):
                raise Exception('supplied pickle_dir %s does not exist as a'
                                ' directory.' % pickle_dir)
            self.pickle_dir = pickle_dir
            self._extension_pattern = None
            if extension:
                self._extension_pattern = re.compile(extension + '$')
            self.load = self.load_dir
        elif pickle_file:
            if not os.path.isfile(pickle_file):
                raise Exception('supplied pickle_file %s does not exist as a'
                                ' file.' % pickle_file)

            self.pickle_file = pickle_file
            self.load = self.load_file
        else:
            raise Exception('initialize with a pickle_dir or pickle_file')

    def load_dir(self):
        """Load a dictionary from the pickled dicts in pickle_dir."""
        for pickle_file in os.listdir(self.pickle_dir):
            if self._extension_pattern:
                if not self._extension_pattern.search(pickle_file):
                    continue

            pickle_handle = open(self.pickle_dir + '/' + pickle_file, 'r')
            entry = cPickle.load(pickle_handle)
            if entry['error']:
                continue
            else:
                yield entry

    def load_file(self):
        """Load a dictionary from the dicts found in pickle_file, which should
        contain the pickle of an iterable containg entry dicts"""
        pickle_handle = open(self.pickle_file, 'r')
        entries = cPickle.load(pickle_handle)
        for entry in entries:
            if 'error' in entry and entry['error']:
                continue
            else:
                yield entry
