#!/usr/bin/env python
'''
Copyright (C) 2012-2013 Kevin Breen.
This file is part of the Maildb web application
See the 'LICENSE' File for copying permission.
'''

import email, imaplib, os, poplib
import time 
from core.logging import MaildbLog
from config.config import reportRoot, transferDir, MaildbRoot
MaildbLog = MaildbLog()
from db.db import Maildatabase
import shutil

db=Maildatabase()

class imapMail():
	def getIMAP(self, user, pwd, server, inbox):

		m = imaplib.IMAP4_SSL(server)
		m.login(user,pwd)
		m.select(inbox)

		resp, items = m.search(None, "ALL") # IMAP Filter Rules here
		items = items[0].split()
		comment = "Tasking-"+inbox
		count = len(items)
		counter = 0
		log = "##INFO##, IMAP Connection to: " + server
		MaildbLog.logEntry(log)
		for emailid in items:
			emailFile = os.path.join(transferDir, inbox+emailid + ".txt")
			counter +=1
			resp, data = m.fetch(emailid, "(RFC822)")
			email_body = data[0][1]
			msgFile = open(emailFile, "w")
			msgFile.write(email_body)
			msgFile.close()
			lastPath = db.lastLine()
			try: # this try means an empty db file wont break it
				newPath = str(lastPath + 1) # will be used to set the database and match it to a physical location
			except:
				newPath = '1'

			reportDir = os.path.join(reportRoot, newPath)
			if not os.path.exists(reportDir):
				os.makedirs(reportDir) #Create the Dir Structure
				os.makedirs(os.path.join(reportDir, "attatchments"))
				shutil.copyfile(emailFile, os.path.join(reportDir, "message.eml"))
			from core.parse import emlParse
			emlName = os.path.join(reportDir, "message.eml") # Name of the eml to pass over to the parse script
			log = "##INFO## Email Submitted With ID " + newPath
			MaildbLog.logEntry(log)
			parseRun = emlParse(emlName, reportDir, comment) # Call the parse script
			parseRun.run()

	def getPOP(self, user, pwd, server):
		m = poplib.POP3_SSL(server)
		m.user(user)
		m.pass_(pwd)
		emailCount, total_bytes = m.stat()
		comment = "Tasking-"+server
		counter = 0
		log = "##INFO##, POP Connection to: %s Retrieving %s Emails in %s bytes" % (server, emailCount, total_bytes)
		MaildbLog.logEntry(log)
		for email in range(emailCount):
			counter +=1
			emailFile = os.path.join(transferDir, server+str(counter) + ".txt")
			msgFile = open(emailFile, "w")
			for msg in m.retr(email+1)[1]:				
				msgFile.write(msg)
				msgFile.write("\n")
			msgFile.close()
			lastPath = db.lastLine()
			try: # this try means an empty db file wont break it
				newPath = str(lastPath + 1) # will be used to set the database and match it to a physical location
			except:
				newPath = '1'

			reportDir = os.path.join(reportRoot, newPath)
			if not os.path.exists(reportDir):
				os.makedirs(reportDir) #Create the Dir Structure
				os.makedirs(os.path.join(reportDir, "attatchments"))
				shutil.copyfile(emailFile, os.path.join(reportDir, "message.eml"))
			from core.parse import emlParse
			emlName = os.path.join(reportDir, "message.eml") # Name of the eml to pass over to the parse script
			log = "##INFO## Email Submitted With ID " + newPath
			MaildbLog.logEntry(log)
			parseRun = emlParse(emlName, reportDir, comment) # Call the parse script
			parseRun.run()