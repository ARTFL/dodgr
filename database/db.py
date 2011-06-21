#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import MySQLdb
import psycopg2
import itertools

       
class SQL(object):
    
    def __init__(self, backend='MySQL', db_path='/home/clovis/DVLF/'):
        self.db_path = db_path
        self.backend = backend
        
    def MySQL(self):
        self.conn = MySQLdb.connect(user='dvlf_readonly', passwd='d00r33d',                                                                                                                                                                                                                   
                             db='dvlf', use_unicode=True)                                                                                                                                                                                                                      
        self.cursor = self.conn.cursor()                                                                                                                                                                                                                                                           
        self.conn.set_character_set('utf8')                                                                                                                                                                                                                                                   
        self.cursor.execute('SET NAMES utf8;')                                                                                                                                                                                                                                              
        self.cursor.execute('SET CHARACTER SET utf8;')                                                                                                                                                                                                                                      
        self.cursor.execute('SET character_set_connection=utf8;')
        
    def SQLite(self):
        self.conn = sqlite3.connect(self.db_path + 'dvlf.sqlite', check_same_thread = False)
        self.conn.text_factory = str
        self.cursor = self.conn.cursor()
        
    def PostgreSQL(self):
        self.conn = psycopg2.connect("dbname=dvlf user=clovis")
        self.cursor = self.conn.cursor()
        
    def list(self, query):
        getattr(self, self.backend)()
        self.cursor.execute(query)
        result = [row[0] for row in self.cursor]
        self.close()
        return result
        
    def query(self, query):
        getattr(self, self.backend)()
        self.cursor.execute(query)
        column_names = [d[0] for d in self.cursor.description]
        result = [Row(itertools.izip(column_names, row)) for row in self.cursor]
        self.close()
        return result
        
    def updatedb(self, table, score, id):
        getattr(self, self.backend)()
        query = "UPDATE %s SET score = %d WHERE id = %d" % (table, score, id)
        self.cursor.execute(query)
        self.conn.commit()
        self.close()
        
    def insert(self, headword, content, source):
        getattr(self, self.backend)()
        if self.backend != 'SQLite':
            self.cursor.execute("""INSERT INTO submit (headword, content, source) VALUES (%s, %s, %s)""", (headword, content, source))
        else:
            self.cursor.execute("""INSERT INTO submit (headword, content, source) VALUES (?, ?, ?)""", (headword, content, source))
        self.conn.commit()
        self.close()
    
    def close(self):
        self.cursor.close()
        self.conn.close()
    
    
class Row(dict):
    """A dict that allows for object-like property access syntax."""
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)
    
        