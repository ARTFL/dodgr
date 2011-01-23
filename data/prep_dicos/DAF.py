# /usr/bin/env python2.6
# -*- coding: utf-8 -*-
"""DAF.py
Creating entry pickles for DAF dictionaries.
"""

import sys
import os
import re
import cPickle
import mmap
import chardet
import ents

import simplog
log = simplog.Simplog.logger('DAF')

import MySQLdb
conn = MySQLdb.connect(host = "localhost", user="root", db="dico1look")
cursor = conn.cursor(MySQLdb.cursors.DictCursor)

output_dir = '/w/artfl/corpora/DAF/dico_dicts'

dico_root = '/w/artfl/corpora/DAF'
dico_dirs = {}
dico_dirs['NICOT1606'] = '/nicot/canonical_0904'
dico_dirs['ACAD1694'] = '/acad1694/canonical_0904'
dico_dirs['ACAD1762'] = '/acad1762/canonical_0904'
dico_dirs['ACAD1798'] = '/acad1798/canonical_0904'
dico_dirs['ACAD1835'] = '/acad1835/canonical_0904'
dico_dirs['ACAD1932'] = '/acad1932/canonical_0904'
dico_dirs['FERAUD1787'] = '/feraud/canonical_0904'
dico_dirs['LITTRE1872'] = '/littre/canonical_0904'

file_name = False
file_path = False
file_handle = False
file_encoding = False


def try_decoding(bytes, tried_encoding=False):
    """Try a bunch of different ways to decode a recalcitrant string"""

    encodings = ['utf-8', 'iso-8859-1']

    for encoding in encodings:
        if encoding != tried_encoding:
            try:
                decoded = bytes.decode(encoding)
                return decoded
            except UnicodeDecodeError:
                pass

    decoded = bytes.decode('utf-8', 'replace')
    log.warning('try_encoding had to replace, got: %s', decoded)

    return decoded

for dico_id, dico_dir in dico_dirs.iteritems():
    entries = []
    cursor.execute("""SELECT * FROM dico1look WHERE dicoid = %s""", (dico_id))
    rows = cursor.fetchall()
    for row in rows:

        if row['filename'] != file_name:
            file_name = row['filename']
            if file_handle:
                file_handle.close()
            file_path = dico_root + dico_dir + '/' + file_name
            file_handle = open(file_path, 'r')
            file_size = os.path.getsize(file_path)
            file_map = mmap.mmap(file_handle.fileno(), file_size,
                                 access=mmap.ACCESS_READ)
            file_encoding = chardet.detect(file_map[10000:50000])['encoding']

            log.debug('file_path: %s file_size: %d file_encoding: %s',
                       file_path, file_size, file_encoding)

        entry = {}
        headword = row['headword']

        try:
            headword = headword.decode(file_encoding)
        except UnicodeDecodeError, e:
            log.warning('Bad encoding in headword, dico %s, file_path %s,'
                        'error text: %s', dico_id, file_path, str(e))
            headword = try_decoding(headword, tried_encoding=file_encoding)
        headword = ents.convert(headword)
        if type(headword) != unicode:
            raise Exception('somehow headword isn''t unicode: %s', headword)
        entry['headwords'] = [(headword, None)]

        start_byte = int(row['startbyte'])
        end_byte = start_byte + int(row['byteoff'])
        content = file_map[start_byte:end_byte]
        try:
            content = content.decode(file_encoding)
        except UnicodeDecodeError, e:
            log.warning('Bad encoding in content, dico %s, file_path %s,'
                        'error text: %s', dico_id, file_path, str(e))
            content = try_decoding(content, tried_encoding=file_encoding)

        content = ents.convert(content)
        if type(content) != unicode:
            raise Exception('somehow content isn''t unicode: %s', content)
        entry['content'] = content
        entries.append(entry)

    pickle_handle = open(output_dir + '/' + dico_id + '.pickle', 'w')
    cPickle.dump(entries, pickle_handle)
    pickle_handle.close()
