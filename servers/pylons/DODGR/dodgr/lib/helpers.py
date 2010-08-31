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
