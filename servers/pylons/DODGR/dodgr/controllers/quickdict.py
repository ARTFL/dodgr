import logging
import itertools
from database import SQL

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to, url_for

from dodgr.lib.base import BaseController, render
from dodgr.lib.helpers import stealth_headword_link, headword_link
from sentences import get_sentences
from pylons import app_globals
from frequencies import get_freqs
from helpers import compile_patterns

log = logging.getLogger(__name__)


class QuickdictController(BaseController):

    def index(self):
        # Return a rendered template
        #return render('/dodgrdico.mako')
        # or, return a response
        return 'Hello World'

    def home(self):
        """Test"""

        return render('/home.html')

    def apropos(self):

        return render('/apropos.html')

    def lookup(self):
        """This action handles incoming search requests."""

        word = request.params['word']
        return redirect_to(url_for(controller='dodgrdico', action='define',
                            word=word))
                            
    def lem_search(self, word):
        lem = app_globals.word2lem[word]
        c.lem = stealth_headword_link(app_globals.word2lem[word])
        return lem
        
    def find_closer_dico(self, date, dicos_with_match):
        """function taken from http://stackoverflow.com/questions/445782/finding-closest-match-in-collection-of-numbers"""
        
        dico_date = [(dico, dates) for dico, dates in app_globals.dico_date if dico in dicos_with_match]
        if date > dico_date[-1][1]:
            return dico_date[-1][0]
        elif date < dico_date[0][1]:
            print 'hi'
            return dico_date[0][0]
        else:
            dico = ''
            lowest = False
            highest = False
            for dico, lower in dico_date:
                if lower <= date:
                    lowest = (dico, lower)
            for dico, higher in dico_date:
                if higher >= date:
                    highest = (dico, higher)
                    break
            
            if highest[1] - date < date - lowest[1]: # compares the differences
                return highest[0]
            else:
                return lowest[0]
        
    def define(self):
        """Load up the test dictionary and serve the definition, if any, for
        the word defined in the route"""
        word = request.params['word']
        word = word.rstrip().lstrip().lower()
        c.word = word
        c.dico_entries = app_globals.quickdict_stack.define(word)
        c.prons = []
        c.num_entries = 0
        c.lem = None
        if not c.dico_entries:
            try:
                lem = self.lem_search(word)
                c.dico_entries = app_globals.quickdict_stack.define(lem)
                if c.dico_entries:
                    word = lem
            except KeyError:
                pass
        if not c.dico_entries:
            norm_word = app_globals.virt_norm.normalize(word)
            c.dico_entries = app_globals.quickdict_stack.define(norm_word)
            if c.dico_entries:
                word = norm_word
            else:
                try:
                    lem = self.lem_search(norm_word)
                    c.dico_entries = app_globals.quickdict_stack.define(lem)
                    if c.dico_entries:
                        word = lem
                except KeyError:
                    pass
        if c.dico_entries:
            c.num_dicos = len(c.dico_entries)
            c.dico_entries.reverse()
            if c.num_dicos < 3:
                try:
                    c.lem = stealth_headword_link(app_globals.word2lem[word])
                    if app_globals.word2lem[word] == word:
                        c.lem = None
                except KeyError:
                    pass
                c.matches = app_globals.stack.fuzzy_matching(word)
                c.matches = [headword_link(term) for term in c.matches if term != word.lower()][:3]
            for dico_name, citation, entries in c.dico_entries:
                if dico_name == 'tlfi':
                    if len(entries['prons']) > 0:
                        c.prons += entries['prons']
                c.num_entries += len(entries['content'])
                
        else:
            c.num_dicos = 0
            c.matches = app_globals.quickdict_stack.fuzzy_matching(word)
            c.matches = [headword_link(term) for term in c.matches if term != word][:3]
                        
        
        db = app_globals.db

        # User-submitted definitions
        c.userdefs = db.query("content", "submit", word, obj='array')
        
        try:
            date = int(request.params['date'])
        except ValueError:
            date = 2011
        try:
            dicos_with_match = set([dico_name for dico_name, citation, entries in c.dico_entries])
            c.closer_dico = self.find_closer_dico(date, dicos_with_match)
        except IndexError:
            pass
        
        return render('/profile_lookup.html')
