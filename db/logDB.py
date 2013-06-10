#!/usr/bin/env python
'''
Copyright (C) 2012-2013 Kevin Breen.
This file is part of the Maildb web application
See the 'LICENSE' File for copying permission.
'''
# The Database interaction Module


import os
import sys
from config.config import MaildbRoot
import MySQLdb
import urllib
from datetime import datetime


class logDatabase:
	def __init__(self, root="."):
		
		self.conn = MySQLdb.connect("localhost", "tvtLog", "tvtLog", "logDB")
		self.cursor = self.conn.cursor()
		self.commit = self.conn.commit()
  	

	def searchUser(self,column, term, start, end):
		search = str(term)
		conn = MySQLdb.connect("localhost", "tvtLog", "tvtLog", "logDB")
		cursor = conn.cursor()
		cursor.execute('SELECT timestamp, cIP, scStatus, csMethod, csURI, userCredential FROM http WHERE '+ column +'=%s AND timestamp >= %s AND timestamp <= %s ORDER BY timestamp DESC;', (search, start, end))
		user = cursor.fetchall()
		return user
	def insertHTTP(self, logLine):
		self.cursor.execute('INSERT INTO http VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);', tuple(logLine))
		#self.conn.commit()
	def commitData(self):
		self.conn.commit()
	def countAll(self):
		count = self.cursor.execute('SELECT COUNT(*) FROM http;')
		print count
		
		
		
	def searchEmail(self, column, term, start, end):
		search = str(urllib.unquote(term))
		conn = MySQLdb.connect("localhost", "tvtLog", "tvtLog", "logDB")
		cursor = conn.cursor()
		start = datetime.strptime(start, '%Y-%m-%d')
		end = datetime.strptime(end, '%Y-%m-%d')
		sql = column, search
		cursor.execute("SELECT sender, recipient, time_t, relay, msgid, subject, size, action, reason FROM email WHERE "+ column +"=%s AND str_to_date(time_t, '%%Y-%%m-%%d %%T') >= %s AND str_to_date(time_t, '%%Y-%%m-%%d %%T') <= %s ORDER BY time_t DESC;", (search, start, end))
		#cursor.execute(sql)
		#print sql
		emails = cursor.fetchall()
		return emails


	def compareEmails(self, column, term):
		list_of_lists = []
		search = str(urllib.unquote(term))
		conn = MySQLdb.connect("localhost", "tvtLog", "tvtLog", "logDB")
		cursor = conn.cursor()
		sql = column, search
		cursor.execute('SELECT sender, recipient, time_t, relay, msgid, subject, size, action, reason FROM email WHERE '+ column +'=%s;', search)
		emails = cursor.fetchall()
		for j in range(len(emails)):
			list_of_lists.append([])
		counter = 0
		
		for recipient in emails:
			cursor.execute('SELECT sender, recipient, time_t, relay, msgid, subject, size, action, reason FROM email WHERE recipient=%s;', recipient[1])
			collects = cursor.fetchall()
			for each in collects:
				list_of_lists[counter].append(each[5])
			counter += 1
		match = list(set.intersection(*map(set, list_of_lists)))
		return match
			
			
					 
