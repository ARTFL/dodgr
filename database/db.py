#!/usr/bin/env python
# -*- coding: utf-8 -*-

#import psycopg2
import MySQLdb
import itertools

       
class SQL(object):
    
    def __init__(self, dbname, user_r, pwd_r, user_w, pwd_w):
        self.cred_r = {'user': user_r, 'password': pwd_r, 'db': dbname}
        self.cred_w = {'user': user_w, 'password': pwd_w, 'db': dbname}
        
    def __db_init_read__(self):
        self.conn = MySQLdb.connect(user=self.cred_r['user'], passwd=self.cred_r['password'], db=self.cred_r['db'], use_unicode=True)
        self.cursor = self.conn.cursor()
        self.conn.set_character_set('utf8')                                                                                                                                                                                                                                                   
        self.cursor.execute('SET NAMES utf8;')                                                                                                                                                                                                                                              
        self.cursor.execute('SET CHARACTER SET utf8;')                                                                                                                                                                                                                                      
        self.cursor.execute('SET character_set_connection=utf8;')
        
    def __db_init_write__(self):
        self.conn = MySQLdb.connect(user=self.cred_w['user'], passwd=self.cred_w['password'], db=self.cred_w['db'], use_unicode=True)
        self.cursor = self.conn.cursor()
        self.conn.set_character_set('utf8')                                                                                                                                                                                                                                                   
        self.cursor.execute('SET NAMES utf8;')                                                                                                                                                                                                                                              
        self.cursor.execute('SET CHARACTER SET utf8;')                                                                                                                                                                                                                                      
        self.cursor.execute('SET character_set_connection=utf8;')
        
    def query(self, fields, table, word=None, obj='list_tuples', args=''):
        self.__db_init_read__()
        if word:
            query = "select %s from %s where headword=" % (fields, table)
            query += '%s '
            query += ' collate utf8_bin '
            query += args
            
            try:
                self.cursor.execute(query, (word,))
            except UnicodeEncodeError:
                self.cursor.execute(query, (word.encode('utf-8'),)) 
        else:
            query = "select %s from %s" % (fields, table)
            self.cursor.execute(query)
        return getattr(self, obj)()
        
    def array(self):
        result = [row[0] for row in self.cursor]
        self.close()
        return result
        
    def list_tuples(self):
        column_names = [d[0] for d in self.cursor.description]
        result = [Row(itertools.izip(column_names, row)) for row in self.cursor]
        self.close()
        return result
        
    def updatedb(self, table, score, id):
        self.__db_init_write__()
        query = "UPDATE %s SET score = %d WHERE id = %d" % (table, score, id)
        self.cursor.execute(query)
        self.close(commit=True)
        
    def insert(self, headword, content, source):
        self.__db_init_write__()
        self.cursor.execute("""INSERT INTO submit (headword, content, source) VALUES (%s, %s, %s)""", (headword, content, source))
        self.close(commit=True)
    
    def close(self, commit=False):
        if commit:
            self.conn.commit()
        self.cursor.close()
        self.conn.close()
    
    
class Row(dict):
    """A dict that allows for object-like property access syntax."""
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)
    
        
