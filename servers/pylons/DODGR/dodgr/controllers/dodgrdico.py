import logging
import json

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from dodgr.lib.base import BaseController, render
from pylons import app_globals

log = logging.getLogger(__name__)


class DodgrdicoController(BaseController):

    def index(self):
        # Return a rendered template
        #return render('/dodgrdico.mako')
        # or, return a response
        return 'Hello World'

    def define(self, word):
        """Load up the test dictionary and serve the definition, if any, for
        the word defined in the route"""
        c.dico_entries = app_globals.stack.define(word)
        c.prons = []
        c.num_entries = 0
        if c.dico_entries:
            c.num_dicos = len(c.dico_entries)
            for citation, entries in c.dico_entries.iteritems():
                for entry in entries:
                    c.num_entries += 1
                    if entry.prons:
                        c.prons += entry.prons
        else:
            c.num_dicos = 0


        cursor = app_globals.db.cursor()
        c.num_sentences = 0
        c.num_corpora = 0

        cursor.execute("""SELECT content FROM corpasentences_utf8
                          WHERE headword = %s""", word)
        corpasentence_rows = cursor.fetchall()

        c.corpasentences = [row[0] for row in
                            corpasentence_rows]
        c.num_sentences += len(c.corpasentences)
        if (len(c.corpasentences) > 0):
            c.num_corpora += 1


        cursor.execute("""SELECT content, source FROM littresentences_utf8
                          WHERE headword = %s""", word)
        littresentence_rows = cursor.fetchall()
        c.littresentences = [{'content': row[0], 'source': row[1]} for row in
                             littresentence_rows]
        c.num_sentences += len(c.littresentences)
        if (len(c.littresentences) > 0):
            c.num_corpora += 1

        cursor.execute("""SELECT content, source, link FROM websentences_utf8
                          WHERE headword = %s""", word)
        websentence_rows = cursor.fetchall()

        c.websentences = [{'content': row[0], 'source': row[1],
                           'link': row[2]} for row in websentence_rows]
        c.num_sentences += len(c.websentences)
        if (len(c.websentences) > 0):
            c.num_corpora += 1

        # Syonoyms and antonyms
        cursor.execute("""SELECT synonyms, antonyms FROM nyms
                          WHERE word = %s""", word)
        nym_row = cursor.fetchone()
        c.synonyms = []
        c.antonyms = []

        if nym_row:
            c.synonyms = json.loads(nym_row[0])
            c.antonyms = json.loads(nym_row[1])


        return render('/entry.html')
