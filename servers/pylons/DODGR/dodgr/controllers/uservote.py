import logging
#import MySQLdb
import psycopg2

import re

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to, url_for
from dodgr.lib.base import BaseController, render
from pylons import app_globals
from sentences import get_sentences
from database import SQL

log = logging.getLogger(__name__)


class UservoteController(BaseController):
    
      
    def index(self):
        table = request.params['table']
        id = int(request.params['id'])
        action = request.params['action']
        score = int(request.params['score'])
        if action == 'add':
            score = score + 1
        else:
            score = score - 1
        self.updatedb(table, id, score)
        return str(score)
        
    def updatedb(self,table, id, score):
        db = SQL(backend=app_globals.backend)
        db.updatedb(table, score, id)
        
                        