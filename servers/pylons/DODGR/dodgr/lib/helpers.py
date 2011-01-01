# -*- coding: utf-8 -*-
"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to templates as 'h'.
"""
# Import helpers as desired, or define your own, ie:
#from webhelpers.html.tags import checkbox, password

import tidylib
import re
from pylons.controllers.util import url_for
from pylons import app_globals


def sanitize_html(html):
    document, errors = tidylib.tidy_fragment(html,
                                options={'numeric-entities': 1})
    return document


def pluralize(word, count, plurals=None):
    """Take a word and a count, and pluralize the word if the count is not
    equal to 1.

    Optionally take a plural form to use if the plural is not
    formed by appending s.

    If word is a list, add the suffix to each word in the list. This is handy
    for French adjectives.

    TODO -- this function needs to be set up for localization.
    """
    if type(word) == list:
        words = word
    else:
        words = [word]

    if count == 1:
        return '1 ' + ' '.join(words)
    else:
        if not plurals:
            plurals = [word + 's' for word in words]
        return str(count) + ' ' + ' '.join(plurals)


def stealth_headword_link(word):
    """Return a "stealth" link for the word"""

    word_url = url_for(controller='dodgrdico', action='define', word=word)
    return '<a class="stealth_headword" href="%s">%s</a>' % (word_url, word)

def headword_link(word):
    word_url = url_for(controller='dodgrdico', action='define', word=word)
    return '<a class="visible_headword" href="%s">%s</a>' % (word_url, word)

def compile_patterns(word):
    patterns = set([])
    try:
        lem2words = set(app_globals.lem2words[word])
        for term in lem2words:
            patterns.add(re.compile('(?iu)(\W+|\A)(%s)(\W+|\Z)' % term))
    except:
        patterns.add(re.compile('(?iu)(\W+|\A)(%s)(\W+|\Z)' % word))
    return patterns

def highlight(text, word, patterns):
    for pattern in patterns:
        text = pattern.sub('\\1<span class="word_highlight">\\2</span>\\3', text)
    return text


## idea taken from http://code.activestate.com/recipes/576507-sort-strings-containing-german-umlauts-in-correct-/
## workaround for OSX
def custom_sorting(word):
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
