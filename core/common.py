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
from config.config import MaildbRoot, reportRoot
from HTMLParser import HTMLParser, HTMLParseError
import zipfile


def fileUpload(data, uploadDir):
	print uploadDir
	raw = data.file.read()
	filename = data.filename
	print filename
	if not os.path.exists(uploadDir):
		os.mkdir(uploadDir)
	f = open(os.path.join(uploadDir, filename), "wb")
	f.write(raw)
	f.close()
	print filename
	return filename	

def exportFile(msg_id, inFile):
	expFile = os.path.join(MaildbRoot, "web", "static", "downloads", "Export.zip")
	filePath = os.path.join(reportRoot, msg_id, "Case_Files", inFile)
	with zipfile.ZipFile(expFile, 'w') as myzip:
		myzip.write(filePath, inFile, zipfile.ZIP_DEFLATED)
	
def exportDir(msg_id, webID):
	
	if webID:
		msgDir = os.path.join(MaildbRoot, "store", msg_id, "sites", webID)
	else:
		msgDir = os.path.join(MaildbRoot, "store", msg_id)
	exp_file = os.path.join(MaildbRoot, "web", "static", "downloads", "Export.zip")
	zip = zipfile.ZipFile(exp_file, 'w', compression=zipfile.ZIP_DEFLATED)
	root_len = len(os.path.abspath(msgDir))
	for root, dirs, files in os.walk(msgDir):
		archive_root = os.path.abspath(root)[root_len:]
		for f in files:
			fullpath = os.path.join(root, f)
			archive_name = os.path.join(archive_root, f)
			zip.write(fullpath, archive_name, zipfile.ZIP_DEFLATED)
	zip.close()
	return exp_file


def listCaseFiles(msg_id):
	casefileDir = os.path.join(reportRoot, msg_id, "Case_Files")
	if os.path.exists(casefileDir):
		caseFiles = [ f for f in os.listdir(casefileDir) ]
		return caseFiles
	else:
		return None

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
		
  
