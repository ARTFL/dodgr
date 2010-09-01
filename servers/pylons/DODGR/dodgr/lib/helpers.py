"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to templates as 'h'.
"""
# Import helpers as desired, or define your own, ie:
#from webhelpers.html.tags import checkbox, password

import tidylib


def sanitize_html(html):
    document, errors = tidylib.tidy_document(html,
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
