import logging
import re
import json
import MySQLdb

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to, url_for

from dodgr.lib.base import BaseController, render
from dodgr.lib.helpers import highlight_patterns, stealth_headword_link
from sentences import get_sentences
from pylons import app_globals

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
        word = word.rstrip()
        c.dico_entries = app_globals.stack.define(word)
        c.prons = []
        c.num_entries = 0
        if c.dico_entries:
            c.num_dicos = len(c.dico_entries)
            for dico_name, citation, entries in c.dico_entries:
                for entry in entries:
                    c.num_entries += 1
                    if entry.prons:
                        c.prons += entry.prons
        else:
            c.num_dicos = 0
            c.matches = app_globals.stack.fuzzy_matching(word)
            c.matches = ' OR '.join([stealth_headword_link(word) for word in c.matches])

        db = app_globals.db()

        # User-submitted definitions
        c.userdefs = db.list("""SELECT content FROM submit
                             WHERE headword = %s""", word)

        # SENTENCES
        # TODO shouldn't we be limiting the # of sentences in the query, not
        # post-hoc?
        
        sentence_limit = 20
        pattern = highlight_patterns(word)
        
        c.corpasentences = get_sentences('corpa', word, pattern, db, sentence_limit)
        c.websentences = get_sentences('web', word, pattern, db, sentence_limit)
        c.littresentences = get_sentences('littre', word, pattern, db, sentence_limit)
        
        c.num_sentences = 0
        c.num_corpora = 0
        for sentence_db in [c.corpasentences, c.websentences, c.littresentences]:
            if len(sentence_db) > 0:
                c.num_corpora += 1
                c.num_sentences += len(sentence_db)


        # Synonyms and antonyms
        nym_rows = db.query("""SELECT synonyms, antonyms, ranksyns FROM nyms
                            WHERE word = %s""", word)
        
        if nym_rows:
            synonyms = nym_rows[0]['synonyms'].decode('utf-8').split(',')[:40]
            ranksyns = nym_rows[0]['ranksyns'].decode('utf-8').split(',')
            c.synonyms = (ranksyns + [syn for syn in synonyms if syn not in ranksyns])[:40]
            if not re.match('empty', nym_rows[0]['antonyms']):
                c.antonyms = nym_rows[0]['antonyms'].decode('utf-8').split(',')
            else:
                c.antonyms = []
        else:
            c.synonyms = []
            c.antonyms = []

        c.neighbors = app_globals.wordwheel.index_neighbors(word)

        db.close()

        return render('/profile.html')
