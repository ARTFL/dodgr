import logging
import itertools
from tornado.database import Row
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
        return redirect_to(url_for(controller='dodgrdico', action='define',
                            word=word))

    def define(self, word):
        """Load up the test dictionary and serve the definition, if any, for
        the word defined in the route"""
        word = word.rstrip().lower()
        c.dico_entries = app_globals.stack.define(word)
        c.prons = []
        c.num_entries = 0
        c.lem = u''
        if not c.dico_entries:
            try:
                lem = app_globals.word2lem[word]
                c.lem = stealth_headword_link(app_globals.word2lem[word])
                c.dico_entries = app_globals.stack.define(lem)
                if c.dico_entries:
                    word = lem
            except KeyError:
                pass
        if c.dico_entries:
            c.num_dicos = len(c.dico_entries)
            if c.num_dicos < 3:
                try:
                    c.lem = stealth_headword_link(app_globals.word2lem[word])
                    if app_globals.word2lem[word] == word:
                        c.lem = u''
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
                        
        
        db = app_globals.db()
        #newdb = app_globals.newdb
        newdb = SQL(backend=app_globals.backend)
        c.backend = app_globals.backend

        # User-submitted definitions
        c.userdefs = newdb.list("""SELECT content FROM submit
                             WHERE headword = '%s'""" % word)

        # SENTENCES
        
        c.corpasentences = get_sentences('corpasentences_utf8', word, newdb)
        c.websentences = get_sentences('websentences_utf8', word, newdb)
        c.littresentences = get_sentences('littresentences_utf8', word, newdb)
        c.word_to_highlight = word
        
        c.num_sentences = 0
        c.num_corpora = 0
        for sentence_db in [c.corpasentences, c.websentences, c.littresentences]:
            if len(sentence_db) > 0:
                c.num_corpora += 1
                c.num_sentences += len(sentence_db)
                
        if c.num_corpora > 0:
            c.patterns = compile_patterns(c.word)


        # Synonyms and antonyms                            
        nym_rows = newdb.query("""select synonyms, antonyms, ranksyns from nyms
                            where word = '%s'""" % word)
                
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
            c.wordfreqs = get_freqs(word, newdb, Row)
        except:
            c.wordfreqs = []

        db.close()

        return render('/profile.html')
