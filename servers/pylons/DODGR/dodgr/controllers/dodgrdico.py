import logging
import re
import json
import MySQLdb

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to, url_for

from dodgr.lib.base import BaseController, render
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
        
        #TODO make highlighting its own function and move out of here
        highlight = re.compile('(?iu)(%s)' % word)
        trimmed_word = re.sub('(\w)$', '', word)
        highlight_trim = re.compile('(?iu)(%s\w*)' % trimmed_word)
        
        c.corpasentences = db.list("""SELECT content FROM corpasentences_utf8
                                    WHERE headword = %s""", word)
        c.corpasentences = c.corpasentences[:sentence_limit]
        for i in range(len(c.corpasentences)):
            c.corpasentences[i] = highlight.sub('<span style="background-color: #EBE4E1"><strong>\\1</strong></span>', c.corpasentences[i])
            c.corpasentences[i] = highlight_trim.sub('<span style="background-color: #EBE4E1"><strong>\\1</strong></span>', c.corpasentences[i])
        c.num_sentences += len(c.corpasentences)
        if (len(c.corpasentences) > 0):
            c.num_corpora += 1

        # Littre sentences
        c.littresentences = db.query("""SELECT content, source
                                       FROM littresentences_utf8
                                       WHERE headword = %s""", word)
        c.littresentences = c.littresentences[:sentence_limit]
        #for i in range(len(c.littresentences)):
            #c.littresentences[i]['content'] = highlight.sub('<span style="background-color: #EBE4E1"><strong>\\1%s</strong></span>' % last_letter, c.littresentences[i]['content'])
            #c.littresentences[i]['content'] = highlight_trim.sub('<span style="background-color: #EBE4E1"><strong>\\1</strong></span>', c.littresentences[i]['content'])
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
            c.websentences[i]['content'] = highlight.sub('<span style="background-color: #EBE4E1"><strong>\\1</strong></span>', c.websentences[i]['content'])
            c.websentences[i]['content'] = highlight_trim.sub('<span style="background-color: #EBE4E1"><strong>\\1</strong></span>', c.websentences[i]['content'])
        c.num_sentences += len(c.websentences)
        if (len(c.websentences) > 0):
            c.num_corpora += 1

        # Syonoyms and antonyms
        nym_rows = db.query("""SELECT synonyms, antonyms, ranksyns FROM newnyms
                            WHERE word = %s""", word)
        
        c.synonyms = []
        c.antonyms = []
        
        if nym_rows:
            antonyms = nym_rows[0]['antonyms']
            if re.search('empty', antonyms):
                c.antonyms = []
            else:
                c.antonyms = nym_rows[0]['antonyms'].decode('utf-8').split(',')
            synonyms = nym_rows[0]['synonyms'].decode('utf-8').split(',')
            ranksyns = nym_rows[0]['ranksyns'].decode('utf-8').split(',')
            try:
                # maybe add a global variable to indicate that there is ranking
                # involved and display it in the results page
                c.synonyms = [syns for syns in ranksyns]
                for syn in synonyms:
                    if len(c.synonyms) > 39:
                        break
                    if syn not in c.synonyms:
                        c.synonyms.append(syn)
            except:
                c.synonyms = synonyms[:40]

        c.neighbors = app_globals.stack.index_neighbors(word)

        db.close()

        return render('/profile.html')
