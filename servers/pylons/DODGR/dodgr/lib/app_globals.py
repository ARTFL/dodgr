# /usr/bin/env python2.6
# -*- coding: utf-8 -*-
"""The application's Globals object"""

from pylons import config
import tornado.database
import dico
from database import SQL
from lemmas import get_lemma, get_forms
import sqlite3

class Globals(object):

    """Globals acts as a container for objects available throughout the
    life of the application

    """

    def __init__(self):
        """One instance of Globals is created during application
        initialization and is available during requests via the
        'app_globals' variable

        """

        dicos = [('tlfi',
                u'Le Trésor de la Langue Française ' +
                u'Informatisé'),
                (u'acad1932',
                 u'Dictionnaire de L\'Académie française 8e édition '
                 u'(1932-1935)'),
                 (u'littre',
                 u'Émile Littré: Dictionnaire de la langue '
                 u'française (1872-1877)'),
                 (u'acad1835',
                 u'Dictionnaire de L\'Académie française 6e édition '
                 u'(1835)'),
                 (u'acad1798',
                 u'Dictionnaire de L\'Académie française 5e édition '
                 u'(1798)'),
                 (u'feraud',
                 u'Féraud: Dictionaire critique de '
                 u'la langue française (1787-1788)'),
                 (u'acad1762',
                 u'Dictionnaire de L\'Académie française 4e édition '
                 u'(1762)'),
                 (u'acad1694',
                 u'Dictionnaire de L\'Académie française 1re édition '
                 u'(1694)'),
                 (u'nicot',
                 u'Jean Nicot: Thresor de la langue française '
                 u'(1606)')]

        stack_dicos = []
        tlfi_url = 'http://www.cnrtl.fr/definition/'
        
        dbname = config['psql.database']
        user = config['psql.user']
        
        self.db = SQL(dbname, user)

        self.stack = dico.Stack(self.db, dicos=dicos, full_entry_url=tlfi_url)
        
        self.lem2words = get_forms(self.db)
        self.word2lem = get_lemma(self.db)   