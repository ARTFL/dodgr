"""pickle.py
Loader class to populate a dico from a series of Python dict cPickles that
already have defined values for things like headword, pos, pron, etc.
"""
import os
import re
import cPickle
from base import Base

class Pickle(Base):
    """Load a dictionary from specially set up Python dict pickles."""

    def __init__(self, pickle_dir, extension=".pickle"):
        self.entry_id = 0
        
        if not os.path.isdir(pickle_dir):
            raise Exception('supplied pickle_dir %s does not exist as a'
                                            'directory.' % pickle_dir)
        self.pickle_dir = pickle_dir
        self._extension_pattern = None
        if extension:
            self._extension_pattern = re.compile(extension + '$')
        
    def load(self):
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
