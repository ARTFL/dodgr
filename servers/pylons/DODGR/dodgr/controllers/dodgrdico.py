import logging
import itertools
from database import SQL

from pylons import request, response, session, url, tmpl_context as c
from pylons.controllers.util import abort, redirect

from dodgr.lib.base import BaseController, render
from dodgr.lib.helpers import stealth_headword_link, headword_link
from sentences import get_sentences
from pylons import app_globals
from frequencies import get_freqs
from helpers import compile_patterns

log = logging.getLogger(__name__)


class DodgrdicoController(BaseController):

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
        return redirect(url(controller='dodgrdico', action='define',
                            word=word))
                            
    def lem_search(self, word):
        lem = app_globals.pull_lem(app_globals.db, word)
        c.lem = stealth_headword_link(lem)
        print c.lem.encode('utf-8')
        return lem

    def define(self, word):
        """Load up the test dictionary and serve the definition, if any, for
        the word defined in the route"""
        c.word = word
        word = word.rstrip().lower()
        c.dico_entries = app_globals.stack.define(word)
        c.prons = []
        c.num_entries = 0
        c.lem = None
        if not c.dico_entries:
            try:
                lem = self.lem_search(word)
                c.dico_entries = app_globals.stack.define(lem)
                if c.dico_entries:
                    word = lem
            except KeyError:
                pass
        if not c.dico_entries:
            norm_word = app_globals.virt_norm.normalize(word)
            c.dico_entries = app_globals.stack.define(norm_word)
            if c.dico_entries:
                word = norm_word
            else:
                try:
                    lem = self.lem_search(norm_word)
                    c.dico_entries = app_globals.stack.define(lem)
                    if c.dico_entries:
                        word = lem
                except KeyError:
                    pass
        if c.dico_entries:
            c.num_dicos = len(c.dico_entries)
            if c.num_dicos < 3:
                try:
                    lem = self.lem_search(word)
                    if lem == word:
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
            c.matches = app_globals.stack.fuzzy_matching(word)
            c.matches = [headword_link(term) for term in c.matches if term != word][:3]
                        
        
        db = app_globals.db

        # User-submitted definitions
        c.userdefs = db.query("content", "submit", word, obj='array')

        # SENTENCES
        
        c.corpasentences = get_sentences('corpasentences', word, db)
        c.websentences = get_sentences('websentences', word, db)
        c.littresentences = get_sentences('littresentences_utf8', word, db)
        c.word_to_highlight = word
        
        c.num_sentences = 0
        c.num_corpora = 0
        for sentence_db in [c.corpasentences, c.websentences, c.littresentences]:
            if len(sentence_db) > 0:
                c.num_corpora += 1
                c.num_sentences += len(sentence_db)
                
        if c.num_corpora > 0:
            if c.lem == None:
                c.patterns = compile_patterns(c.word)
            else:
                c.patterns = compile_patterns(lem)


        # Synonyms and antonyms                            
        nym_rows = db.query('synonyms, antonyms, ranksyns', 'nyms', word)
                
        if nym_rows:
            synonyms = nym_rows[0]['synonyms'].decode('utf-8').rstrip('\n').split(',')
            ranksyns = nym_rows[0]['ranksyns'].decode('utf-8').rstrip('\n').split(',')
            c.synonyms = (ranksyns + [syn for syn in synonyms if syn not in ranksyns])
            if not nym_rows[0]['antonyms'].startswith('empty'):
                c.antonyms = nym_rows[0]['antonyms'].decode('utf-8').rstrip('\n').split(',')
            else:
                c.antonyms = []
        else:
            c.synonyms = []
            c.antonyms = []

        c.neighbors = app_globals.stack.index_neighbors(word)
        
        
        try:
            c.wordfreqs = get_freqs(word, db)
        except:
            c.wordfreqs = []

        return render('/profile.html')
