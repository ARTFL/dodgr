import logging
import MySQLdb
import re

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to, url_for
from dodgr.lib.base import BaseController, render
from pylons import app_globals
from sentences import get_sentences

log = logging.getLogger(__name__)


class UservoteController(BaseController):
    
      
    def index(self):
        table = request.params['table']
        id = int(request.params['id'])
        action = request.params['action']
        score = int(request.params['score'])
        if action == 'add':
            score = score + 1
            self.increment(table, id, score)
        else:
            score = score - 1
            self.decrement(table, id, score)
        return str(score)
        
    def increment(self,table, id, score):
        db = MySQLdb.connect(user='dvlf2', passwd='d00v33d',
                             db='dvlf', use_unicode=True)
        cursor = db.cursor()
        db.set_character_set('utf8')
        cursor.execute('SET NAMES utf8;')
        cursor.execute('SET CHARACTER SET utf8;')
        cursor.execute('SET character_set_connection=utf8;')
        
        cursor.execute('''UPDATE %s SET score = %d WHERE id = %d''' % (table, score, id))
                        
    def decrement(self,table, id, score):
        db = MySQLdb.connect(user='dvlf2', passwd='d00v33d',
                             db='dvlf', use_unicode=True)
        cursor = db.cursor()
        db.set_character_set('utf8')
        cursor.execute('SET NAMES utf8;')
        cursor.execute('SET CHARACTER SET utf8;')
        cursor.execute('SET character_set_connection=utf8;')
        
        cursor.execute('''UPDATE %s SET score = %d WHERE id = %d''' % (table, score, id))
                        