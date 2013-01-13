#!/usr/bin/env python
'''
Copyright (C) 2012-2013 Kevin Breen.
This file is part of the Maildb web application
See the 'LICENSE' File for copying permission.
'''

# All The Search Functions Will Be Here


import os
import sys
import sqlite3
from config.config import DBFile
from core.common import Dictionary
conn = sqlite3.connect(DBFile)
cursor = conn.cursor()

def dict_factory(cursor, row):
	d = Dictionary()
	for idx, col in enumerate(cursor.description):
		setattr(d, col[0], row[idx])
	return d

class MailSearch():
		

	def __init__(self, root="."):
		
		self.db_file = DBFile
		self.conn = sqlite3.connect(self.db_file, timeout=60)
		self.conn.row_factory = dict_factory
		self.cursor = self.conn.cursor()
		self.commit = self.conn.commit()
    



	def searchTables(self, tableName, column, Search):
		searchTerm = str(Search)
		row = cursor.execute("SELECT main.msg_id, date_added, eml_md5, main.Revmatch, attCount, Comment, type FROM main INNER JOIN "+ tableName +" ON "+ tableName +".msg_id=main.msg_id WHERE "+ column +" LIKE ?", ('%'+Search+'%',)).fetchall()
		return row
		
	def searchMain(self, column, Search):
		searchTerm = str(Search)
		row = cursor.execute("SELECT * FROM main WHERE "+ column +" LIKE ?", ('%'+Search+'%',)).fetchall()
		return row

		

		
	
