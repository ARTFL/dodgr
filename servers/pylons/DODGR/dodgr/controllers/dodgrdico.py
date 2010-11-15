import logging
import re
import json
import MySQLdb

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to, url_for

from dodgr.lib.base import BaseController, render
from dodgr.lib.helpers import highlight, highlight_patterns
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

        db = app_globals.db()

        # User-submitted definitions
        c.userdefs = db.list("""SELECT content FROM submit
                             WHERE headword = %s""", word)

        # SENTENCES
        # TODO get all this sentence stuff out of here

        # TODO shouldn't we be limiting the # of sentences in the query, not
        # post-hoc?
        sentence_limit = 20

        c.num_sentences = 0
        c.num_corpora = 0
        
        pattern = highlight_patterns(word)
            
        c.corpasentences = db.list("""SELECT content FROM corpasentences_utf8
                                    WHERE headword = %s""", word)
        c.corpasentences = c.corpasentences[:sentence_limit]
        c.corpasentences = [highlight(c.corpasentences[i], pattern) for i in range(len(c.corpasentences))]
        c.num_sentences += len(c.corpasentences)
        if (len(c.corpasentences) > 0):
            c.num_corpora += 1

        # Littre sentences
        c.littresentences = db.query("""SELECT content, source
                                       FROM littresentences_utf8
                                       WHERE headword = %s""", word)
        c.littresentences = c.littresentences[:sentence_limit]
        for i in range(len(c.littresentences)):
            c.littresentences[i]['content'] = highlight(c.littresentences[i]['content'], pattern)
        c.num_sentences += len(c.littresentences)
        
        if (len(c.littresentences) > 0):
            c.num_corpora += 1

        # Web sentences
        c.websentences = db.query("""SELECT content, source, link
                                  FROM websentences_utf8
                                  WHERE headword = %s""", word)
        c.websentences = c.websentences[:sentence_limit]
        link_pattern = re.compile('(\w+\.)+\w+\/')
        
        for i in range(len(c.websentences)):
            link = c.websentences[i]['link']
            if not link_pattern.match(link):
                c.websentences[i]['link'] = None
            c.websentences[i]['content'] = highlight(c.websentences[i]['content'], pattern)
        c.num_sentences += len(c.websentences)
        if (len(c.websentences) > 0):
            c.num_corpora += 1

        # Synonyms and antonyms
        nym_rows = db.query("""SELECT synonyms, antonyms, ranksyns FROM newnyms
                            WHERE word = %s""", word)
        
        if nym_rows:
            synonyms = nym_rows[0]['synonyms'].decode('utf-8').split(',')[:39]
            ranksyns = nym_rows[0]['ranksyns'].decode('utf-8').split(',')
            c.synonyms = (ranksyns + [syn for syn in synonyms if syn not in ranksyns])[:39]
            if not re.match('empty', nym_rows[0]['antonyms']):
                c.antonyms = nym_rows[0]['antonyms'].decode('utf-8').split(',')
        else:
            c.synonyms = []
            c.antonyms = []

        c.neighbors = app_globals.wordwheel.index_neighbors(word)

        db.close()

        return render('/profile.html')
