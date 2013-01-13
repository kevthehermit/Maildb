#!/usr/bin/env python
'''
Copyright (C) 2012-2013 Kevin Breen.
This file is part of the Maildb web application
See the 'LICENSE' File for copying permission.
'''

import os
from core.logging import MaildbLog
from config.config import MaildbRoot, enableMAS, enableCuckoo

import shutil
import subprocess

# stackoverflow.com/questions/3090724/


class sandboxSubmit():
	def submitMAS(self, profile, filename, msg_id):
		if enableMAS == '1':
			from config.config import MASRoot
			fileName = os.path.join(MaildbRoot, "store", msg_id,"attatchments", filename)
			profilePath = os.path.join(MASRoot, profile, "src", filename)
			shutil.copyfile(fileName, profilePath)
			log = "##INFO##, File: " + filename + " Submitted To MAS"
			MaildbLog().logEntry(log)
	def submitCuckoo(self, user, pwd, server):
		pass

