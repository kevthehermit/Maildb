#!/usr/bin/env python
'''
Copyright (C) 2012-2013 Kevin Breen.
This file is part of the Maildb web application
See the 'LICENSE' File for copying permission.
'''

import os
from config.config import logEnable, MaildbRoot
from datetime import datetime

class MaildbLog:

	def logEntry(self, entry):
	
		if logEnable == '1':
			logDate = datetime.now()
			logEntry = str(entry)
			logLine = "\n"+ str(logDate) + " - " + logEntry 
			f = open(os.path.join(MaildbRoot, "log.txt"), "a")
			f.write(logLine)
			f.close

