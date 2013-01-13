#!/usr/bin/env python
'''
Copyright (C) 2012-2013 Kevin Breen.
This file is part of the Maildb web application
See the 'LICENSE' File for copying permission.
'''
# The Database interaction Module


import os
import sys
from core.logging import MaildbLog
from config.config import MaildbRoot, DBFile
from core.common import Dictionary
writeLog = MaildbLog()
import sqlite3
conn = sqlite3.connect(DBFile)
conn.text_factory = sqlite3.OptimizedUnicode
cursor = conn.cursor()

def dict_factory(cursor, row):
	d = Dictionary()
	for idx, col in enumerate(cursor.description):
		setattr(d, col[0], row[idx])
	return d

class Maildatabase:
	def __init__(self, root="."):
		
		self.db_file = DBFile
		self.conn = sqlite3.connect(self.db_file, timeout=60)
		self.conn.row_factory = dict_factory
		self.cursor = self.conn.cursor()
		self.commit = self.conn.commit()
		self.conn.text_factory = str

### install function ###    

	def generate(self):
		conn = sqlite3.connect(DBFile)
		cursor = conn.cursor()
		cursor.execute("CREATE TABLE if not exists main (msg_id INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL, date_added DATETIME, eml_md5 VARCHAR, Revmatch INTEGER, attCount INTEGER, Comment VARCHAR, type);")
		cursor.execute("CREATE TABLE if not exists header (msg_id INTEGER NOT NULL  UNIQUE, date, from_add, domain, subject, x_mailer, x_priority, message_id, count_to, count_cc, to_add);")
		cursor.execute("CREATE TABLE if not exists attatch (msg_id INTEGER, filename, fileExt, filesize, md5, sha256,ssdeep, Revmatch INTEGER);")
		cursor.execute("CREATE TABLE if not exists hops (msg_id INTEGER, hop);")		
		cursor.execute("CREATE TABLE if not exists words (msg_id INTEGER, word VARCHAR, count NUMERIC);")
		cursor.execute("CREATE TABLE if not exists yara (msg_id INTEGER, md5, rule, description);")
		cursor.execute("CREATE TABLE if not exists comments (msg_id INTEGER NOT NULL, title VARCHAR, freetext VARCHAR);")
		cursor.execute("CREATE TABLE if not exists streams (msg_id INTEGER NOT NULL, Request, Host, Path, Referer, Proxy, Response, ReqFile, RespFile , httpFile);")
		cursor.execute("CREATE TABLE if not exists flows (msg_id INTEGER NOT NULL, SIP, Sport, DIP,Dport);")
		cursor.execute("CREATE TABLE if not exists links (msg_id INTEGER NOT NULL, link_type, address);")		
		conn.commit()
		cursor.close()
		log = "##INFO## Database Tables Created "
		writeLog.logEntry(log)
    	

	def tasks(self, limit, offset):
		taskList = self.cursor.execute("SELECT * FROM main ORDER BY msg_id DESC LIMIT ? OFFSET ?", (limit, offset)).fetchall()
		return taskList 

	def lastLine(self):
		try:
			key = self.cursor.execute("SELECT * from sqlite_sequence WHERE rowid=1").fetchone()
			return key.seq
		except:
			pass
			
	def msgHeaders(self, msg_id):
		msgHead = self.cursor.execute('SELECT * FROM header WHERE msg_id=?', (msg_id,)).fetchall()
		cursor.close()
		return msgHead

	def msgInfo(self, msg_id):
		info = self.cursor.execute('SELECT date_added, type, Comment FROM main WHERE msg_id=?', (msg_id,)).fetchone()
		cursor.close()
		return info

	def msgAttach(self, msg_id):
		attatch = self.cursor.execute('SELECT * FROM attatch WHERE msg_id=?', (msg_id,)).fetchall()
		cursor.close()
		return attatch

	def sigPage(self, msg_id):
		msgHead = self.cursor.execute('SELECT * FROM header WHERE msg_id=?', (msg_id,)).fetchall()
		attatch = self.cursor.execute('SELECT * FROM attatch WHERE msg_id=?', (msg_id,)).fetchall()
		emailLinks = self.cursor.execute('SELECT * FROM links WHERE msg_id=?', (msg_id,)).fetchall()
		emailHops =  self.cursor.execute('SELECT * FROM hops WHERE msg_id=?', (msg_id,)).fetchall()
		yaraMail = self.cursor.execute('SELECT * FROM yara WHERE msg_id=?', (msg_id,)).fetchall()
		return msgHead, attatch, emailLinks, emailHops, yaraMail

	def fileInfo(self, msg_id, md5):
		data = self.cursor.execute('SELECT * FROM attatch WHERE msg_id=? AND md5=?', (msg_id, md5,)).fetchall()
		return data


	def yaraMail(self, msg_id):
		result = self.cursor.execute('SELECT * FROM yara WHERE msg_id=?', (msg_id,)).fetchall()
		return result

	def yaraFile(self, md5, msg_id):
		result = self.cursor.execute('SELECT * FROM yara WHERE md5=? AND msg_id=?', (md5, msg_id,)).fetchall()
		return result
		
		
	def countAll(self):
		result = self.cursor.execute('SELECT * FROM main').fetchall()
		return len(result)
		
## Admin Functions Here
	

	def delRecord(self, msg_id): #pass the id here and then delete
		msg_id = int(msg_id)
		self.cursor.execute('DELETE FROM attatch WHERE msg_id=%s' % msg_id)
		self.cursor.execute('DELETE FROM comments WHERE msg_id=%s' % msg_id)
		self.cursor.execute('DELETE FROM flows WHERE msg_id=%s' % msg_id)
		self.cursor.execute('DELETE FROM header WHERE msg_id=%s' % msg_id)
		self.cursor.execute('DELETE FROM hops WHERE msg_id=%s' % msg_id)
		self.cursor.execute('DELETE FROM links WHERE msg_id=%s' % msg_id)
		self.cursor.execute('DELETE FROM main WHERE msg_id=%s' % msg_id)
		self.cursor.execute('DELETE FROM streams WHERE msg_id=%s' % msg_id)
		self.cursor.execute('DELETE FROM words WHERE msg_id=%s' % msg_id)
		self.cursor.execute('DELETE FROM yara WHERE msg_id=%s' % msg_id)
		self.conn.commit()
		log = "##ALERT## Record %s Deleted" % msg_id
		writeLog.logEntry(log)
	def modRecord(self, msg_id): # SQL UPDATE ...
		return True
	def expRecord(self, msg_id): # Write record to file for IMPEX
		return True
	def retRecord(self, msg_id): # Return a Record
		pass
	
### Stats Functions here


	def stats(self):
		countall = self.cursor.execute('SELECT COUNT(*) FROM main as count').fetchall()

		countattatch = self.cursor.execute('SELECT COUNT(*) FROM attatch').fetchall()
		topattatch = self.cursor.execute('SELECT fileExt, count(fileExt) as counted	from attatch group by fileExt order by 2 desc limit 10').fetchall()
		topdomain = self.cursor.execute('SELECT domain, count(domain) as counted from header group by domain order by 2 desc limit 10').fetchall()
		topxmail = self.cursor.execute('SELECT x_mailer, count(x_mailer) as counted from header group by x_mailer order by 2 desc limit 10').fetchall()
		combined = [countall, countattatch, topattatch, topdomain, topxmail]
		
		return (countall, countattatch, topattatch, topdomain, topxmail)
		
		

### Review Functions Here

	def review(self, reviewflag, msg_id):
		
		if reviewflag == 'event':
			
			self.cursor.execute("UPDATE main SET 'Revmatch'='1' WHERE msg_id=?", (msg_id,))
						
		elif reviewflag == 'review':
			self.cursor.execute("UPDATE main SET 'Revmatch'='2' WHERE msg_id=?", (msg_id,))
			
		elif reviewflag == 'yara':
			self.cursor.execute("UPDATE main SET 'Revmatch'='3' WHERE msg_id=?", (msg_id,))
			
			
		elif reviewflag == 'clear':
			self.cursor.execute("UPDATE main SET 'Revmatch'='0' WHERE msg_id=?", (msg_id,))
		self.conn.commit()
			


### Word Counters here

	
	def insert(self, word, count, msg_id):
		self.conn.text_factory = str
		self.cursor.execute("INSERT into 'words' ('word', 'count', 'msg_id') VALUES (?,?,?)", (word, count, msg_id))
		
		
		
### Comments go here

# view comments
	def viewComment(self, msg_id):
		result = self.cursor.execute('SELECT * FROM comments WHERE msg_id=?', (msg_id,)).fetchall()
		return result
		
# enter comments
	def enterComments(self, msg_id, title, comments):
		comments_clean = comments.decode('ascii', 'ignore')
		self.cursor.execute('INSERT INTO comments VALUES (?,?,?)', (msg_id, title, comments_clean))
		self.conn.commit()
# update comments		



# Http Stuff

	def httpFlows(self, msg_id):
		flows = self.cursor.execute('SELECT SIP, DIP, Count(*) as counted from flows where msg_id=? GROUP BY DIP', (msg_id,)).fetchall()
		return flows
		
	def httpSessions(self, msg_id):
		sessions = self.cursor.execute('SELECT host, Count(*) as counted from streams where msg_id=? GROUP BY host', (msg_id,)).fetchall()
		return sessions
			
	def hostInfo(self, msg_id, host):
		hostFiles = self.cursor.execute('SELECT * FROM streams WHERE msg_id=? AND Host=?', (msg_id, host)).fetchall()
		return hostFiles

# Email Link Stuff

	def emailLink(self, msg_id):
		emailLinks = self.cursor.execute('SELECT * FROM links WHERE msg_id=?', (msg_id,)).fetchall()
		return emailLinks

