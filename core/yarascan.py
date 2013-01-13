#!/usr/bin/env python
'''
Copyright (C) 2012-2013 Kevin Breen.
This file is part of the Maildb web application
See the 'LICENSE' File for copying permission.
'''




import os
import sys
import yara
from config.config import emailSig, fileSig
emailRules = yara.compile(emailSig)
fileRules = yara.compile(fileSig)
from db.db import Maildatabase
db = Maildatabase()

class Scan():
		
	
	def emailScan(self, scanemail, reportDir):
		matches = []
		try: #reset or emtpy DB willbreak without this
			msg_id = str(db.lastLine() + 1)
		except:
			msg_id ='1'
		
		for match in emailRules.match(scanemail):
			matches.append({"name" : match.rule, "meta" : match.meta})
		for m in matches:
			yaraRule = m["name"]
			yaraDesc = m["meta"]["description"]
			db.cursor.execute("INSERT INTO yara (msg_id,rule,description) VALUES (?,?,?)", (msg_id, yaraRule, yaraDesc))
			db.conn.commit()						
		return matches
	    
	def fileScan(self, scanfile, md5Hash):
		try:
			msg_id = int(db.lastLine())
		except:
			msg_id = '1'
		matches = []


		if os.path.getsize(scanfile) > 0:
			for match in fileRules.match(scanfile):
				matches.append({"name" : match.rule, "meta" : match.meta})
		for m in matches:
			yaraRule = m["name"]
			yaraDesc = m["meta"]["description"]
			db.cursor.execute("INSERT INTO yara (msg_id,md5,rule,description) VALUES (?,?,?,?)", (msg_id, md5Hash, yaraRule, yaraDesc))
			db.conn.commit()
		return matches




















	
