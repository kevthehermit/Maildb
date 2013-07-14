#!/usr/bin/env python
'''
Copyright (C) 2012-2013 Kevin Breen.
This file is part of the Maildb web application
See the 'LICENSE' File for copying permission.
'''

import email, imaplib, os, poplib
import tempfile
from datetime import datetime
from config.config import reportRoot, transferDir, MaildbRoot
from db.db import Maildatabase
import shutil

db=Maildatabase()

class imapMail():
	def getIMAP(self, user, pwd, server, inbox):
		tmpDir = tempfile.mkdtemp()
		print tmpDir
		m = imaplib.IMAP4_SSL(server)
		m.login(user,pwd)
		m.select(inbox)
		resp, items = m.search(None, "ALL") # IMAP Filter Rules here
		items = items[0].split()
		date = datetime.now().strftime("%Y-%m-%d")
		comment = "Tasking-"+date+"-"+server
		count = len(items)
		counter = 0
		for emailid in items:
			emailFile = os.path.join(tmpDir, inbox+emailid + ".txt")
			print emailFile
			counter +=1
			resp, data = m.fetch(emailid, "(RFC822)")
			email_body = data[0][1]
			with open(emailFile, "w+") as msgFile:
				msgFile.write(email_body)
			newPath = db.lastLine()
			reportDir = os.path.join(reportRoot, str(newPath))
			if not os.path.exists(reportDir):
				os.makedirs(reportDir) #Create the Dir Structure
				os.makedirs(os.path.join(reportDir, "attatchments"))
				shutil.copyfile(emailFile, os.path.join(reportDir, "message.eml"))
			from core.parse import emlParse
			emlName = os.path.join(reportDir, "message.eml") # Name of the eml to pass over to the parse script
			parseRun = emlParse(emlName, reportDir, comment) # Call the parse script
			parseRun.run()
		shutil.rmtree(tmpDir)

	def getPOP(self, user, pwd, server):
		tmpDir = tempfile.mkdtemp()
		m = poplib.POP3_SSL(server)
		m.user(user)
		m.pass_(pwd)
		emailCount, total_bytes = m.stat()
		date = datetime.now().strftime("%Y-%m-%d")
		comment = "Tasking-"+date+"-"+server
		counter = 0
		for email in range(emailCount):
			counter +=1
			emailFile = os.path.join(tmpDir, server+str(counter) + ".txt")
			msgFile = open(emailFile, "w")
			for msg in m.retr(email+1)[1]:				
				msgFile.write(msg)
				msgFile.write("\n")
			msgFile.close()
			newPath = db.lastLine()
			reportDir = os.path.join(reportRoot, str(newPath))
			if not os.path.exists(reportDir):
				os.makedirs(reportDir) #Create the Dir Structure
				os.makedirs(os.path.join(reportDir, "attatchments"))
				shutil.copyfile(emailFile, os.path.join(reportDir, "message.eml"))
			from core.parse import emlParse
			emlName = os.path.join(reportDir, "message.eml") # Name of the eml to pass over to the parse script
			parseRun = emlParse(emlName, reportDir, comment) # Call the parse script
			parseRun.run()
		shutil.rmtree(tmpDir)
