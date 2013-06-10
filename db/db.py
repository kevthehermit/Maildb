#!/usr/bin/env python
'''
Copyright (C) 2012-2013 Kevin Breen.
This file is part of the Maildb web application
See the 'LICENSE' File for copying permission.
'''
# The Database interaction Module


import os
import sys
from config.config import MaildbRoot, DBFile
from core.common import Dictionary
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
		cursor.execute("INSERT INTO sqlite_sequence VALUES ('main', 0);")
		conn.commit()
		cursor.close()

    	
	def tasks(self, limit, offset):
		conn = sqlite3.connect(self.db_file, timeout=60)
		conn.row_factory = dict_factory
		cursor = conn.cursor()
		taskList = cursor.execute("SELECT * FROM main ORDER BY msg_id DESC LIMIT ? OFFSET ?", (limit, offset)).fetchall()
		cursor.close()
		return taskList 

	def lastLine(self):
		conn = sqlite3.connect(self.db_file, timeout=60)
		conn.row_factory = dict_factory
		cursor = conn.cursor()
		key = cursor.execute("SELECT * from sqlite_sequence WHERE name='main'").fetchone()
		cursor.close()
		if key.seq == 0:
			return 1
		else:
			print key.seq + 1
			return key.seq + 1
		
			
	def msgHeaders(self, msg_id):
		conn = sqlite3.connect(self.db_file, timeout=60)
		conn.row_factory = dict_factory
		cursor = conn.cursor()
		msgHead = cursor.execute('SELECT * FROM header WHERE msg_id=?', (msg_id,)).fetchall()
		cursor.close()
		return msgHead

	def msgInfo(self, msg_id):
		conn = sqlite3.connect(self.db_file, timeout=60)
		conn.row_factory = dict_factory
		cursor = conn.cursor()
		info = cursor.execute('SELECT date_added, type, Revmatch, Comment, attCount FROM main WHERE msg_id=?', (msg_id,)).fetchone()
		cursor.close()
		return info

	def msgAttach(self, msg_id):
		attatch = self.cursor.execute('SELECT * FROM attatch WHERE msg_id=?', (msg_id,)).fetchall()
		self.cursor.close()
		return attatch

	def sigPage(self, msg_id):
		conn = sqlite3.connect(self.db_file, timeout=60)
		conn.row_factory = dict_factory
		cursor = conn.cursor()
		msgHead = cursor.execute('SELECT * FROM header WHERE msg_id=?', (msg_id,)).fetchall()
		attatch = cursor.execute('SELECT * FROM attatch WHERE msg_id=?', (msg_id,)).fetchall()
		emailLinks = cursor.execute('SELECT * FROM links WHERE msg_id=?', (msg_id,)).fetchall()
		emailHops =  cursor.execute('SELECT * FROM hops WHERE msg_id=?', (msg_id,)).fetchall()
		yaraMail = cursor.execute('SELECT * FROM yara WHERE msg_id=?', (msg_id,)).fetchall()
		cursor.close()
		return msgHead, attatch, emailLinks, emailHops, yaraMail

	def fileInfo(self, msg_id, md5):
		conn = sqlite3.connect(self.db_file, timeout=60)
		conn.row_factory = dict_factory
		cursor = conn.cursor()
		data = cursor.execute('SELECT * FROM attatch WHERE msg_id=? AND md5=?', (msg_id, md5,)).fetchall()
		cursor.close()
		return data


	def yaraScan(self, msg_id):
		conn = sqlite3.connect(self.db_file, timeout=60)
		conn.row_factory = dict_factory
		cursor = conn.cursor()
		result = cursor.execute('SELECT * FROM yara WHERE msg_id=?', (msg_id,)).fetchall()
		cursor.close()
		return result

	def yaraFile(self, md5, msg_id):
		conn = sqlite3.connect(self.db_file, timeout=60)
		conn.row_factory = dict_factory
		cursor = conn.cursor()
		result = cursor.execute('SELECT * FROM yara WHERE md5=? AND msg_id=?', (md5, msg_id,)).fetchall()
		cursor.close()
		return result		
		
	def countAll(self):
		conn = sqlite3.connect(self.db_file, timeout=60)
		conn.row_factory = dict_factory
		cursor = conn.cursor()
		result = cursor.execute('SELECT * FROM main').fetchall()
		cursor.close()
		return len(result)
		
## Admin Functions Here
	

	def delRecord(self, msg_id): #pass the id here and then delete
		conn = sqlite3.connect(self.db_file, timeout=60)
		cursor = conn.cursor()
		msg_id = int(msg_id)
		cursor.execute('DELETE FROM attatch WHERE msg_id=%s' % msg_id)
		cursor.execute('DELETE FROM comments WHERE msg_id=%s' % msg_id)
		cursor.execute('DELETE FROM flows WHERE msg_id=%s' % msg_id)
		cursor.execute('DELETE FROM header WHERE msg_id=%s' % msg_id)
		cursor.execute('DELETE FROM hops WHERE msg_id=%s' % msg_id)
		cursor.execute('DELETE FROM links WHERE msg_id=%s' % msg_id)
		cursor.execute('DELETE FROM main WHERE msg_id=%s' % msg_id)
		cursor.execute('DELETE FROM streams WHERE msg_id=%s' % msg_id)
		cursor.execute('DELETE FROM words WHERE msg_id=%s' % msg_id)
		cursor.execute('DELETE FROM yara WHERE msg_id=%s' % msg_id)
		conn.commit()
		cursor.close()
	def modRecord(self, msg_id): # SQL UPDATE ...
		return True
	def expRecord(self, msg_id): # Write record to file for IMPEX
		return True
	def retRecord(self, msg_id): # Return a Record
		pass
	
### Stats Functions here


	def stats(self):
		conn = sqlite3.connect(self.db_file, timeout=60)
		conn.row_factory = dict_factory
		cursor = conn.cursor()
		countAll = (cursor.execute("SELECT COUNT(*) as counted FROM main").fetchone()).counted
		countNonTasks = (cursor.execute("SELECT COUNT(*) as counted FROM main WHERE Comment NOT LIKE 'Tasking%'").fetchone()).counted
		countTasks = (cursor.execute("SELECT COUNT(*) as counted FROM main WHERE Comment LIKE 'Tasking%'").fetchone()).counted
		countEvents = (cursor.execute("SELECT COUNT(*) as counted FROM main WHERE Revmatch='1'").fetchone()).counted
		countRev = (cursor.execute("SELECT COUNT(*) as counted FROM main WHERE Revmatch='2'").fetchone()).counted
		countOut = (cursor.execute("SELECT COUNT(*) as counted FROM main WHERE (Revmatch='0' OR Revmatch='3')").fetchone()).counted
		counts = [countAll, countNonTasks, countTasks, countEvents, countOut, countRev]
		cursor.close()
		return counts
		
		

### Review Functions Here

	def review(self, reviewflag, msg_id):
		conn = sqlite3.connect(self.db_file, timeout=60)
		conn.row_factory = dict_factory
		cursor = conn.cursor()		
		if reviewflag == 'event':
			
			cursor.execute("UPDATE main SET 'Revmatch'='1' WHERE msg_id=?", (msg_id,))
		
						
		elif reviewflag == 'review':
			cursor.execute("UPDATE main SET 'Revmatch'='2' WHERE msg_id=?", (msg_id,))
		
			
		elif reviewflag == 'yara':
			cursor.execute("UPDATE main SET 'Revmatch'='3' WHERE msg_id=?", (msg_id,))
		
			
			
		elif reviewflag == 'clear':
			cursor.execute("UPDATE main SET 'Revmatch'='0' WHERE msg_id=?", (msg_id,))
		conn.commit()
		cursor.close()
			


### Word Counters here

	
	def insert(self, word, count, msg_id):
		self.conn.text_factory = str
		self.cursor.execute("INSERT into 'words' ('word', 'count', 'msg_id') VALUES (?,?,?)", (word, count, msg_id))
		self.cursor.close()
		
		
		
### Comments go here

# view comments
	def viewComment(self, msg_id):
		conn = sqlite3.connect(self.db_file, timeout=60)
		conn.row_factory = dict_factory
		cursor = conn.cursor()
		result = cursor.execute('SELECT rowid,* FROM comments WHERE msg_id=?', (msg_id,)).fetchall()
		cursor.close()
		return result
		
# enter comments
	def enterComments(self, msg_id, title, comments):
		conn = sqlite3.connect(self.db_file, timeout=60)
		conn.row_factory = dict_factory
		cursor = conn.cursor()
		comments_clean = comments.decode('ascii', 'ignore')
		cursor.execute('INSERT INTO comments VALUES (?,?,?)', (msg_id, title, comments_clean))
		conn.commit()
		cursor.close()
# update comments		
	def updateComment(self, comm_id, title, comments):
		conn = sqlite3.connect(self.db_file, timeout=60)
		conn.row_factory = dict_factory
		cursor = conn.cursor()
		comments_clean = comments.decode('ascii', 'ignore')
		cursor.execute('UPDATE comments SET title=?, freetext=? WHERE rowid=?', (title, comments_clean, comm_id))
		conn.commit()
		cursor.close()


# Http Stuff

	def httpFlows(self, msg_id):
		conn = sqlite3.connect(self.db_file, timeout=60)
		conn.row_factory = dict_factory
		cursor = conn.cursor()
		flows = cursor.execute('SELECT SIP, DIP, Count(*) as counted from flows where msg_id=? GROUP BY DIP', (msg_id,)).fetchall()
		cursor.close()
		return flows
		
	def httpSessions(self, msg_id):
		conn = sqlite3.connect(self.db_file, timeout=60)
		conn.row_factory = dict_factory
		cursor = conn.cursor()
		sessions = cursor.execute('SELECT host, Count(*) as counted from streams where msg_id=? GROUP BY host', (msg_id,)).fetchall()
		cursor.close()
		return sessions
			
	def hostInfo(self, msg_id, host):
		conn = sqlite3.connect(self.db_file, timeout=60)
		conn.row_factory = dict_factory
		cursor = conn.cursor()
		hostFiles = cursor.execute('SELECT * FROM streams WHERE msg_id=? AND Host=?', (msg_id, host)).fetchall()
		cursor.close()
		return hostFiles

# Email Link Stuff

	def emailLink(self, msg_id):
		conn = sqlite3.connect(self.db_file, timeout=60)
		conn.row_factory = dict_factory
		cursor = conn.cursor()
		emailLinks = cursor.execute('SELECT * FROM links WHERE msg_id=?', (msg_id,)).fetchall()
		cursor.close()
		return emailLinks


# Insert Statments

	def parseMain(self, sql):
		conn = sqlite3.connect(self.db_file, timeout=60)
		cursor = conn.cursor()
		cursor.execute("INSERT INTO main (date_added,eml_md5,Revmatch,Comment,type) VALUES (?,?,?,?,?)", sql)
		conn.commit()
		conn.close()
	
	def parseHops(self, sql):
		conn = sqlite3.connect(self.db_file, timeout=60)
		cursor = conn.cursor()
		cursor.execute('INSERT INTO hops VALUES(?,?)', sql)
		conn.commit()
		conn.close()
	
	def parseHeader(self, sql):
		conn = sqlite3.connect(self.db_file, timeout=60)
		cursor = conn.cursor()
		cursor.execute('INSERT INTO header VALUES (?,?,?,?,?,?,?,?,?,?,?)', sql)
		conn.commit()
		conn.close()
	
	def parseLinks(self, sql):
		conn = sqlite3.connect(self.db_file, timeout=60)
		cursor = conn.cursor()
		cursor.execute('INSERT INTO links VALUES(?,?,?)', sql)
		conn.commit()
		conn.close()
	
	def parseAttatch(self, sql):
		conn = sqlite3.connect(self.db_file, timeout=60)
		cursor = conn.cursor()
		cursor.execute('INSERT INTO attatch VALUES (?,?,?,?,?,?,?,?)', sql)
		conn.commit()
		conn.close()
	
	def parseYara(self, sql):
		conn = sqlite3.connect(self.db_file, timeout=60)
		cursor = conn.cursor()
		cursor.execute("UPDATE main SET 'attCount'=?, 'Revmatch'=? WHERE msg_id=?", sql)
		conn.commit()
		conn.close()
	
	def parseHttpMain(self, sql):
		conn = sqlite3.connect(self.db_file, timeout=60)
		cursor = conn.cursor()
		cursor.execute("INSERT INTO main (date_added,eml_md5,Revmatch,Comment,type) VALUES (?,?,?,?,?)", sql)
		
		conn.commit()
		conn.close()
	
	def parseHttpInfo(self, flowSql, streamSql):
		conn = sqlite3.connect(self.db_file, timeout=60)
		cursor = conn.cursor()
		cursor.execute("INSERT INTO flows (msg_id, SIP, Sport, DIP, Dport) VALUES (?,?,?,?,?)", flowSql)
		cursor.execute("INSERT INTO streams VALUES (?,?,?,?,?,?,?,?,?,?)", streamSql)
		conn.commit()
		conn.close()	
	
	
# Search Functions

	def searchTables(self, tableName, column, Search):
		searchTerm = str(Search)
		conn = sqlite3.connect(self.db_file, timeout=60)
		conn.row_factory = dict_factory
		cursor = conn.cursor()		
		row = cursor.execute("SELECT main.msg_id, date_added, eml_md5, main.Revmatch, attCount, Comment, type FROM main INNER JOIN "+ tableName +" ON "+ tableName +".msg_id=main.msg_id WHERE "+ column +" LIKE ?", ('%'+Search+'%',)).fetchall()
		conn.close()
		return row
		
	def searchMain(self, column, Search):
		searchTerm = str(Search)
		conn = sqlite3.connect(self.db_file, timeout=60)
		conn.row_factory = dict_factory
		cursor = conn.cursor()
		row = cursor.execute("SELECT * FROM main WHERE "+ column +" LIKE ?", ('%'+Search+'%',)).fetchall()
		conn.close()
		return row
		
# Yara Functions
	def storeYara(self, sql):
		conn = sqlite3.connect(self.db_file, timeout=60)
		cursor = conn.cursor()
		cursor.execute("INSERT INTO yara (msg_id,md5,rule,description) VALUES (?,?,?,?)", sql)
		conn.commit()
		conn.close()
	
