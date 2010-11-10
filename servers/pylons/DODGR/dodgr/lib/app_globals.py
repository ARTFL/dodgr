# /usr/bin/env python2.6
# -*- coding: utf-8 -*-
"""The application's Globals object"""
import cPickle
from pylons import config
import tornado.database
import dico
import dico.mappers


class Globals(object):

    """Globals acts as a container for objects available throughout the
    life of the application

    """

    def __init__(self):
        """One instance of Globals is created during application
        initialization and is available during requests via the
        'app_globals' variable

        """

        dicos = [(u'ACAD1932',
                 u'Dictionnaire de L\'Académie française 8e édition '
                 u'(1932-1935)'),
                 (u'LITTRE1872',
                 u'Émile Littré: Dictionnaire de la langue '
                 u'française (1872-1877)'),
                 (u'ACAD1835',
                 u'Dictionnaire de L\'Académie française 6e édition '
                 u'(1835)'),
                 (u'ACAD1798',
                 u'Dictionnaire de L\'Académie française 5e édition '
                 u'(1798)'),
                 (u'FERAUD1787',
                 u'Féraud: Dictionaire critique de '
                 u'la langue française (1787-1788)'),
                 (u'ACAD1762',
                 u'Dictionnaire de L\'Académie française 4e édition '
                 u'(1762)'),
                 (u'ACAD1694',
                 u'Dictionnaire de L\'Académie française 1re édition '
                 u'(1694)'),
                 (u'NICOT1606',
                 u'Jean Nicot: Thresor de la langue française '
                 u'(1606)')]

        stack_dicos = []
        wordwheel_dicos = []
        db = self.db()
        mapper = dico.mappers.IdolMapper()
        tlfi_url = 'http://www.cnrtl.fr/definition/'
        tlfi_dico = dico.MySQLBased('TLFI',
                                    u'Le Trésor de la Langue Française ' +
                                    u'Informatisé', mapper, self.db(),
                                    truncate=1000, full_entry_url=tlfi_url)
        stack_dicos.append(tlfi_dico)
        wordwheel_dicos.append(tlfi_dico)

        for name, citation in dicos:
            daf_dico = dico.MySQLBased(name, citation, mapper, self.db())
            stack_dicos.append(daf_dico)
            if name == u'ACAD1932':
                wordwheel_dicos.append(daf_dico)

        self.stack = dico.Stack(dicos=stack_dicos)
        self.wordwheel = dico.Stack(dicos=wordwheel_dicos)

    def db(self):
        """Return a database connection"""
        return tornado.database.Connection("localhost",
                                           config['mysql.database'],
                                           user=config['mysql.user'],
                                           password=config['mysql.password'])
