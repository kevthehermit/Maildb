#!/usr/bin/env python
'''
Copyright (C) 2012-2013 Kevin Breen.
This file is part of the Maildb web application
See the 'LICENSE' File for copying permission.
'''

import os
import time
from BaseHTTPServer import BaseHTTPRequestHandler
from StringIO import StringIO
from config.config import MaildbRoot
from HTMLParser import HTMLParser, HTMLParseError




class Dictionary(dict):
	def __getattr__(self, key):
		return self.get(key, None)
		
	__setattr__ = dict.__setitem__
	__delattr__ = dict.__delitem__


class cleanup():
	def cleartmp(self, tmpPath):
		for file in os.listdir(tmpPath):
			os.remove(os.path.join(tmpPath, file))
					
class HTTPRequest(BaseHTTPRequestHandler):
    def __init__(self, request_text):
        self.rfile = StringIO(request_text)
        self.raw_requestline = self.rfile.readline()
        self.error_code = self.error_message = None
        self.parse_request()

    def send_error(self, code, message):
        self.error_code = code
        self.error_message = message

class Counters():
	def imapCounter(self, count):
		mustend = time.time() + 30
		while time.time() < mustend:
			if os.path.getsize(os.path.join(transferDir, "IMAP"+str(count)+".txt")) > 0: return True
			time.sleep(0.25)
		return False
		
  
