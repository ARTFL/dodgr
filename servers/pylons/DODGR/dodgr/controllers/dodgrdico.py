import logging

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

        cursor = app_globals.db.cursor()
        cursor.execute('SET NAMES utf8;')
        cursor.execute('SET CHARACTER SET utf8;')
        cursor.execute('SET character_set_connection=utf8;')

        cursor.execute("""SELECT content FROM corpasentences WHERE headword =
                       %s""", word)
        corpasentence_rows = cursor.fetchall()
        c.corpasentences = [row[0] for row in corpasentence_rows]

        cursor.execute("""SELECT content, source FROM littresentences WHERE
                       headword = %s""", word)
        littresentence_rows = cursor.fetchall()
        c.littresentences = [{'content': row[0], 'source': row[1]} for row in
                             littresentence_rows]

        cursor.execute("""SELECT content, source, link FROM websentences WHERE
                      headword = %s""", word)
        websentence_rows = cursor.fetchall()
        c.websentences = [{'content': row[0], 'source': row[1],
                           'link': row[2]} for row in websentence_rows]

        return render('/entry.html')
