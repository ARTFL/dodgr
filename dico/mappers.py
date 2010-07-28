# /usr/bin/python
# -*- coding: utf-8 -*-
"""mapper.py
Class for mapping between various forms of words. For example, a French word
like éclat might have many acceptable forms:

    ECLAT
    ÉCLAT
    Eclat
    éclat
    ...
    
There also may be technically unacceptable forms, but forms which we wish to
support for searching purposes:

    eclat
    e/clat
    EcLaT
    ...
    
An entry should be indexed under all these headword forms.

All functions expect Unicode strings, not byte strings.

TODO: issue scores for how closely an input form corresponds to a citation
form.

TODO: mappings for query input strings into strings to match against the 
index
"""
import unicodedata

class Base(object):
    """Base form mapper"""

    @classmethod
    def citation_form(cls, dirty_form):
        """Return the citation form of the word, based on some kind of 'dirty'
         input form. The purpose of this method is to provide a place to map
         from whatever representation is found in the data source being loaded
         to the a clean, citation form of the word. 
        
        For example, perhaps your data source lists all headwords in upper
        case, with commans after them, inside brackets. The clean citation
        form would be lower case, without the punctuation and brackets.
        
        This method, if needed, should be overridden in a descendent class,
        most likely not in this file, but in the script that does the actual
        loading of the data into the dictionary structure. Whatever conversion
        needs to take place in this method will be highly dependent on the
        specific data source being loaded. That said, it may be useful to
        overried this method in some of the descendant language-specific
        mappers, if there are general rules that should be applied for a given
        language (e.g. English citation forms shouldn't have trailing
        punctuation, trivial things like that.)
        """
        citation_form = dirty_form.strip()
        return citation_form
    
    @classmethod
    def lower(cls, word):
        """Lower-case form of the word"""
        return word.lower()

    @classmethod
    def upper(cls, word):
        """Upper-case form of the word (retaining diacritics)"""
        return word.upper()

    @classmethod
    def lose_accents(cls, word):
        """Discard all accents, but keep base character. We do this by
        converting the string to Unicode normalized form, with diacritics
        represented as separate characters, and then discarding all those
        diacritics.
        
        Note that this method might not be safe for some languages where
        the normalized form does more than simply break out diacritics
        into their own characters.
        """

        # 'NFD' is 'normal form decomposed', with diacritics separated
        # http://docs.python.org/library/unicodedata.html
        normalized = unicodedata.normalize('NFD', word)
        # Diacritics are category 'Mark' + 'non-spacing' = 'Mn'
        # http://www.fileformat.info/info/unicode/category/index.htm
        non_diacritics = [char for char in normalized if
                    unicodedata.category(char) != 'Mn']
        return u''.join(non_diacritics)

    @classmethod
    def upper_lose_accents(cls, word):
        """Upper case form, accents stripped"""
        return cls.lose_accents(cls.upper(word))

class French(Base):
    """Form mapper for French dictionaries"""
    
    @classmethod
    def index_forms(cls, citation_form):
        """Return a list of all citable forms that should be indexed, given
        the canonical citation form"""
        
        # TODO: score each value for how well it matches, provide an ordered
        # list of forms.
        
        forms = set()
        forms.add(citation_form)
        forms.add(cls.upper(citation_form))
        forms.add(cls.upper_lose_accents(citation_form))
        
        return forms

