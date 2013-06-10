#!/usr/bin/env python
'''
Copyright (C) 2012-2013 Kevin Breen.
This file is part of the Maildb web application
See the 'LICENSE' File for copying permission.
'''

import os
from config.config import MaildbRoot, enableMAS, enableCuckoo
import shutil
import subprocess
import logging

class sandboxSubmit():
	def submitMAS(self, profile, filename, msg_id):
		if enableMAS == '1':
			from config.config import MASRoot
			fileName = os.path.join(MaildbRoot, "store", msg_id,"attatchments", filename)
			profilePath = os.path.join(MASRoot, profile, "src", filename)
			shutil.copyfile(fileName, profilePath)
			logging.info('File %s Submitted to MAS', fileName)
	def submitCuckoo(self, user, pwd, server):
		pass

class cuckooAPI():


	def submitFile(self, fileName):
		if enableCuckoo == '1':
			import requests
			from config.config import cuckooUrl, cuckooPort, cuckooMachine
			url = "http://"+cuckooUrl+":"+cuckooPort+"/tasks/create/file"
			options = {'file': fileName, 'machine':cuckooMachine} 
			capi = requests.post(url, data=options)
			return True
		
	def submitURL(self, malUrl):
		if enableCuckoo == '1':
			import requests
			from config.config import cuckooUrl, cuckooPort, cuckooMachine
		url = "http://"+cuckooUrl+":"+cuckooPort+"/tasks/create/url"
		options = {'url': malUrl, 'machine': cuckooMachine}
		capi = requests.post(url, data=options)
		return capi.text
		
	def queryFiles():
		pass
	
	def viewReport():
		pass
		
		
	
