# /usr/bin/python
# -*- coding: utf-8 -*-
"""idol.py

Class for IDOL dictionary entries. Contains a Parser that uses BeautifulSoup
to extract the relevant entry parts, and a simple Entry class to hold them.
"""

import sys
import os
import re
import cPickle
from BeautifulSoup import BeautifulSoup

import simplog
log = simplog.Simplog.logger('idol_soup')


def main():
    """Process the IDOL webpages into Entry objects."""

    in_dir = '/w/artfl/corpora/idol/webpages'
    out_dir = '/w/artfl/corpora/idol/entry_pickles'

    start_yet = False
    for page_string in os.listdir(in_dir):
        if page_string == 'soumission':
            start_yet = True
        if start_yet:
            page = page_string.decode('utf-8')
            page_file = in_dir + '/' + page
            log.debug(u'opening page_file %s', page_file)
            page_handle = open(page_file, 'r')
            html = page_handle.read().decode('utf-8')
            log.debug(u'opened page_file %s', page_file)

            parser = Parser(html)
            # Create entry and dump it to a pickle
            entry = parser.build_entry()

            out_file = out_dir + '/' + page
            pickle_handle = open(out_file, 'w')
            cPickle.dump(entry, pickle_handle)
            pickle_handle.close()
            log.info(u"dumped pickle to out_file: %s\n", out_file)
        else:
            print 'skipping', page_string


class Entry(object):
    """A dictionary entry from the IDOL"""

    def __init__(self, headwords=None, content=None, examples=None, pos=None,
                                                    prons=None, error=None):
        self.headwords = headwords
        self.content = content
        self.examples = examples
        self.prons = prons
        self.error = error


class Parser(object):
    """BeautifulSoup-based parser for IDOL dictionary entries"""
    # _el stands for 'element'. headword_el is the HTML element that
    # contains the headword, e.g.

    # Strategy here is to get each element of interest as a unicode string --
    # NOT as a byte string of any sort. We'll encode as we print out.
    # Therefore, the renderContents() and prettify() methods shouldn't be
    # used, as these encode to byte str types, I believe. But, since we can't
    # get the contents of a tag as a unicode string, sometimes we need to
    # encode and then decode I guess, by calling unicode(renderContents()).

    # So we use most unicode(), which renders all the contents of a set of
    # tags (including the tags themselves) as a unicode string. This is kind
    # of confusing, because normally the unicode() function decodes from byte
    # strings into unicode strings. Hopefully BS knows how to return its
    # internal unicode strings rather than encoding and then decoding them. At
    # any rate it seems to work out OK.
    def __init__(self, html):

        self.soup = BeautifulSoup(html)
        log.debug(u'created soup')
        self.headwords = None
        self.content = None
        self.examples = None
        self.prons = None

        self.find_error()
        if not self.error:
            self.get_headword()
        if not self.error:
            self.get_content()
            self.get_examples()
            self.get_prons()

    def find_error(self):
        """Look for errors in the HTML of the page that indicate a problem
        with the definition. These pages may need to be recrawled."""
        self.error = False
        error_el = self.soup.findAll('div', attrs={"id": "contentbox"},
                    text=re.compile('Cette forme est introuvable'))
        if error_el:
            log.info(u'Error in entry: Cette forme est introuvable')
            self.error = 'Cette forme est introuvable'

        error_el = self.soup.findAll('div', attrs={"id": "contentbox"},
                    text=re.compile('Terme introuvable'))
        if error_el:
            log.info(u'Error in entry: Terme introuvable')
            self.error = 'Terme introuvable'

    def get_headword(self):
        """There should only be one headword, I think. It should be inside
        <div class="tlf_cvedette"><span class="tlf_cmot">"""
        headword_els = []
        headword_parent_els = self.soup.findAll('div',
                    attrs={"class": "tlf_cvedette"})
        if not headword_parent_els:
            log.warning(u'no headword_parent_els found')
            self.error = 'no headword_parent_els found'
            return None
        for headword_parent_el in headword_parent_els:
            headword_els.extend(headword_parent_el.findAll('span',
                                attrs={"class": "tlf_cmot"}))
        # If we've found more than one, that's odd.
        if not headword_els:
            log.warning(u'no headword elements in parent els %s',
                                            headword_parent_els)
            self.error = 'no headword elements in parent els'
            return None

        # There can be more than one headword, see e.g. 'abadie'
        self.headwords = []
        for headword_el in headword_els:
            self.headword_el = headword_el
            # This is pretty dumb -- we're rendering contents, which encodes
            # to utf-8 and then re-decoding it into a unicode string. Why?
            # Because BS has no method which will simply give you the contents
            # of an element as a unicode string. We don't want the enclosing
            # tag, so I think this is how we have to do it.
            headword_contents = headword_el.renderContents(encoding='utf-8')
            headword = headword_contents.decode('utf-8').strip()
            log.info(u'extracted headword: %s', headword)
            pos = self.get_pos(headword_el)
            self.headwords.append((headword, pos))
        log.info(u'extracted headwords: %s', self.headwords)

    def get_content(self):
        """Capture the entire entry content, including headword."""
        content_el = self.headword_el.parent.parent
        self.content = unicode(content_el).strip()

    def get_examples(self):
        """Find example sentences"""
        example_els = self.soup.findAll(attrs={"class": "tlf_tabulation"})
        self.examples = [unicode(example).strip() for example in example_els]
        log.info(u'found %d example sentences', len(self.examples))

    def get_pos(self, headword_el):
        """Find the part of speech, which should be next to the headword"""
        pos_el = headword_el.nextSibling
        print 'pos_el', len(pos_el), 'xxx'
        if not pos_el:
            log.debug('could not find pos_el')

        # Check to see if the next sibling is a tag. If it has attrs, it is...
        # if not, it might be a string, in which case we'll try skipping it
        # and seeing if the next element over might be a POS span.
        try:
            el_class = pos_el.attrs[0][1]
        except AttributeError:
            log.debug('nextSibling to headword doesn''t have attrs, scooting'
            'over one more to see if we get anywhere...')
            pos_el = pos_el.nextSibling
            try:
                el_class = pos_el.attrs[0][1]
            except AttributeError:
                log.debug('nextSibling stil doesn''t have attrs, giving up')
                return None
        if el_class != 'tlf_ccode':
            log.debug('nextSibling to headword is not of class ccode')
            if el_class == 'tlf_cmot':
                # If the next sibling is itself a headword, we might
                # want to infer that the POS for this headword is the
                # same one as the next one. That seems to be how they
                # are structured, e.g. 'acetabule'.
                # So, send along the current pos_el as the headword_el,
                # and see if we can get a POS from its next sibling.
                # Note: this will chain through an arbitrary # of
                # consecutive headwords!
                log.debug('nextSibling to headword is headword, trying to'
                                            'find POS in its nextSibling')
                return self.get_pos(pos_el)
            else:
                return None
        posel_contents = pos_el.renderContents(encoding='utf-8')
        pos = posel_contents.decode('utf-8').strip()
        log.info(u'extracted POS: %s', pos)
        return pos

    def get_prons(self):
        """Find all pronunciations, and feminine pronunciations"""
        pron_els = self.soup.findAll('div', text=re.compile("Prononc"),
                                attrs={"class": "tlf_parothers"})
        pron_contexts = set()
        for pron_el in pron_els:
            pron_contexts.add(unicode(pron_el.parent.nextSibling).strip())
        self.prons = []
        self.fem_prons = []
        for pron_context in pron_contexts:
            match = re.match('\[([^\]]+)\]', pron_context)
            if match:
                self.prons.append(match.group(1))
            match = re.search('fém\.\s*\[([^\]]+)\]', pron_context)
            if match:
                self.fem_prons.append(match.group(1))
        if self.prons:
            log.info(u'extracted prons: %s', ', '.join(self.prons))
        else:
            log.info(u'no prons extracted')
        if self.fem_prons:
            log.info(u'extracted fem_prons: %s', ', '.join(self.fem_prons))
        else:
            log.info(u'no fem_prons extracted')

    def build_entry(self):
        """Create an Entry object from the values stored in the parser"""
        return Entry(headwords=self.headwords, content = self.content,
             examples=self.examples, prons=self.prons,
                                    error=self.error)


if __name__ == "__main__":
    sys.exit(main())
