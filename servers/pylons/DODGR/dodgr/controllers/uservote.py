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
    
    def corpa(self, example):
        table = 'corpasentences_utf8'
        self.getdata(table, example)
    
    def littre(self, example):
        table = 'littresentences_utf8'
        self.getdata(table, example)
        
    def web(self, example):
        table = 'websentences_utf8'
        self.getdata(table, example)
        
    def getdata(self, table, example):
        db = app_globals.db()
        m = re.search('(\D+)(\d+)(\D+)', example)
        word = m.group(1)
        num = int(m.group(2))
        action = m.group(3)
        corpasentences = get_sentences(table, word, db)
        sentence = corpasentences[num]['content']
        word = corpasentences[num]['word']
        if action == '+':
            self.increment(table, sentence, word)
        else:
            self.decrement(table, sentence, word)
            
        return redirect_to(url_for(controller='dodgrdico', action='define',
                            word=word))
        
    def increment(self,table, sentence, word):
        db = MySQLdb.connect(user='dvlf2', passwd='d00v33d',
                             db='dvlf', use_unicode=True)
        cursor = db.cursor()
        db.set_character_set('utf8')
        cursor.execute('SET NAMES utf8;')
        cursor.execute('SET CHARACTER SET utf8;')
        cursor.execute('SET character_set_connection=utf8;')
        
        cursor.execute('''UPDATE %s SET score = score + 1 WHERE headword = "%s" AND content = "%s"''' % (table, word, sentence))
                        
    def decrement(self,table, sentence, word):
        db = MySQLdb.connect(user='dvlf2', passwd='d00v33d',
                             db='dvlf', use_unicode=True)
        cursor = db.cursor()
        db.set_character_set('utf8')
        cursor.execute('SET NAMES utf8;')
        cursor.execute('SET CHARACTER SET utf8;')
        cursor.execute('SET character_set_connection=utf8;')
        
        cursor.execute('''UPDATE %s SET score = score - 1 WHERE headword = "%s" AND content = "%s"''' % (table, word, sentence))
                        