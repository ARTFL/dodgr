#!/usr/bin/env python
# -*- coding: utf-8 -*-

import psycopg2
import itertools

       
class SQL(object):
    
    def __init__(self, dbname, user):
        self.cred = 'dbname=%s user=%s' % (dbname, user)
    
    def __db_init__(self):
        self.conn = psycopg2.connect(self.cred)
        self.cursor = self.conn.cursor()
        
    def listall(self, dico):
        self.__db_init__()
        query = 'select headword from %s' % dico
        self.cursor.execute(query)
        result = [row[0] for row in self.cursor]
        self.close()
        return result
        
    def list(self, fields, table, word):
        self.__db_init__()
        query = "select %s from %s where headword=" % (fields, table)
        query += '%s'
        self.cursor.execute(query, (word,))
        result = [row[0] for row in self.cursor]
        self.close()
        return result
        
    def query(self, fields, table, word=None, args=''):
        self.__db_init__()
        if word:
            query = "select %s from %s where headword=" % (fields, table)
            query += '%s '
            query += args
            self.cursor.execute(query, (word,))
        else:
            query = "select %s from %s" % (fields, table)
            self.cursor.execute(query)
        column_names = [d[0] for d in self.cursor.description]
        result = [Row(itertools.izip(column_names, row)) for row in self.cursor]
        self.close()
        return result
        
    def updatedb(self, table, score, id):
        self.__db_init__()
        query = "UPDATE %s SET score = %d WHERE id = %d" % (table, score, id)
        self.cursor.execute(query)
        self.conn.commit()
        self.close()
        
    def insert(self, headword, content, source):
        self.__db_init__()
        self.cursor.execute("""INSERT INTO submit (headword, content, source) VALUES (%s, %s, %s)""", (headword, content, source))
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
    
        