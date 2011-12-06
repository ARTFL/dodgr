# /usr/bin/python
# -*- coding: utf-8 -*-
"""I never should have stored the idol entries in object pickles, where
simple dicts will do nicely, Change 'em."""

import sys
import os
import re
import cPickle

class Entry(object):
    """A dictionary entry from the IDOL"""

    def __init__(self, headwords=None, content=None, examples=None, pos=None,
                                                    prons=None, error=None):
        self.headwords = headwords
        self.content = content
        self.examples = examples
        self.prons = prons
        self.error = error


in_dir = '/w/artfl/corpora/idol/entry_pickles'
out_dir = '/tmp'

pattern = re.compile('CROIRE')

for page_string in os.listdir(in_dir):
    # print page_string
    pickin_file = in_dir + '/' + page_string
    pickin_handle = open(pickin_file, 'r')
    entry_obj = cPickle.load(pickin_handle)
    pickin_handle.close()

    try:
        if pattern.search(entry_obj.headwords[0][0]):
            print pickin_file
    except:
        pass

    # entry_dict = {}
    # entry_dict['headwords'] = entry_obj.headwords
    # entry_dict['content'] = entry_obj.content
    # entry_dict['examples'] = entry_obj.examples
    # entry_dict['prons'] = entry_obj.prons
    # entry_dict['error'] = entry_obj.error
    #
    # out_file = out_dir + '/' + page_string + '.pickle'
    # pickout_handle = open(out_file, 'w')
    # cPickle.dump(entry_dict, pickout_handle)
    # pickout_handle.close()
