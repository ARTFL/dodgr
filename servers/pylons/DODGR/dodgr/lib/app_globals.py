# /usr/bin/env python2.6
# -*- coding: utf-8 -*-
"""The application's Globals object"""
import cPickle
import MySQLdb
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
        db = MySQLdb.connect(user='dvlf', passwd='dvlf', db='dvlf',
                             use_unicode=True)
        cursor = db.cursor()
        db.set_character_set('utf8')
        cursor.execute('SET NAMES utf8;')
        cursor.execute('SET CHARACTER SET utf8;')
        cursor.execute('SET character_set_connection=utf8;')

        dicos = [(u'NICOT1606',
                 u'Jean Nicot\'s Thresor de la langue française '
                 u'(1606)'),
                 (u'ACAD1694',
                 u'Dictionnaire de L\'Académie française 1st edition '
                 u'(1694)'),
                 (u'ACAD1762',
                 u'Dictionnaire de L\'Académie française 4th edition '
                 u'(1762)'),
                 (u'FERAUD1787',
                 u'Jean-François Féraud\'s Dictionaire critique de '
                 u'la langue française (1787-1788)'),
                 (u'ACAD1798',
                 u'Dictionnaire de L\'Académie française 5th edition '
                 u'(1798)'),
                 (u'ACAD1835',
                 u'Dictionnaire de L\'Académie française 6th edition '
                 u'(1835)'),
                 (u'LITTRE1872',
                 u'Émile Littré\'s Dictionnaire de la langue '
                 u'française (1872-1877)'),
                 (u'ACAD1932',
                 u'Dictionnaire de L\'Académie française 8th edition '
                 u'(1932-1935)'),
                 (u'TLFI',
                 u'Le Trésor de la Langue Française Informatisé')]

        stack_dicos = []
        for name, citation in dicos:
            mapper = dico.mappers.IdolMapper()
            daf_dico = dico.MySQLBased(name, citation, mapper, cursor)
            stack_dicos.append(daf_dico)

        self.stack = dico.Stack(dicos=stack_dicos)
        self.db = db
