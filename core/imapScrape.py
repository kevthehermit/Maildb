#!/usr/bin/env python
'''
Copyright (C) 2012-2013 Kevin Breen.
This file is part of the Maildb web application
See the 'LICENSE' File for copying permission.
'''

import email, imaplib, os
import time 
from core.logging import MaildbLog
from config.config import reportRoot, transferDir, deleml, MaildbRoot
MaildbLog = MaildbLog()
from db.db import Maildatabase
import shutil

db=Maildatabase()

class imapMail():
	def getInbox(self, user, pwd, server, inbox):

		m = imaplib.IMAP4_SSL(server)
		m.login(user,pwd)
		m.select(inbox)

		resp, items = m.search(None, "ALL") # IMAP Filter Rules here
		items = items[0].split()
		comment = "Tasking-IMAP"
		count = len(items)
		counter = 0
		for emailid in items:
			emailFile = os.path.join(transferDir, server+emailid + ".txt")
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
			parseRun = emlParse(emlName, reportDir, comment) # Call the parse script
			parseRun.run()
