#!/usr/bin/env python
'''
Copyright (C) 2013 Kevin Breen.
Log Parse
Version 0.1
'''

import os
import sys
import gzip
import shlex
import time
import MySQLdb
import logging
from optparse import OptionParser
from datetime import datetime
from config.config import logTemp
import db.logDB
from db.logDB import logDatabase
db = logDatabase()
def webParse():
	httpCounter = 0
	httpsCounter = 0
	fileCounter = 0
	timeCounter = 0
	startTime = time.time()
	conn = MySQLdb.connect("localhost", "tvtLog", "tvtLog", "logDB")
	cursor = conn.cursor()	
	for gzFile in os.listdir(logTemp):
		if gzFile.endswith(".gz"): 
			if gzFile.startswith("http"):
				method = 1
				fileCounter += 1
				try:
					gz = gzip.open((os.path.join(logTemp, gzFile)), 'r')
					for line in gz:
						if method == 1:
							httpCounter += 1
							logEntry = shlex.split(line,posix=False)
							if not line.startswith("#"):
								try:
									cursor.execute('INSERT INTO http VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);', tuple(logEntry))
								except:
									print gzFile
						elif method == 2:
							logEntry = line.split()
							print logEntry
							#db.dbLog.logLine(logEntry)
					conn.commit()
					gz.close()
							
				except IOError as e:
					print e.strerror
				timeCounter = time.time() - startTime
				os.remove((os.path.join(logTemp, gzFile)))
				print "Files %s Processed in %s Seconds" % (fileCounter, timeCounter)
	return httpCounter, fileCounter, timeCounter

def emailParse():
	httpCounter = 0
	httpsCounter = 0
	fileCounter = 0
	timeCounter = 0
	startTime = time.time()
	conn = MySQLdb.connect("localhost", "tvtLog", "tvtLog", "logDB")
	cursor = conn.cursor()	
	for gzFile in os.listdir(logTemp):
		if gzFile.endswith(".gz"): 
			if gzFile.startswith("email"):
				method = 1
				fileCounter += 1
				try:
					gz = gzip.open((os.path.join(logTemp, gzFile)), 'r')
					for line in gz:
						if method == 1:
							httpCounter += 1
							logEntry = line.split('\t')
							if not line.startswith("SENDER"):
								try:
									cursor.execute('INSERT INTO email VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);', tuple(logEntry))
								except:
									print line
									log = "##ERROR## Line Not Inserted " + str(line)
									
						elif method == 2:
							print "here instead"
							logEntry = line.split()
							print logEntry
							#db.dbLog.logLine(logEntry)
					conn.commit()
					gz.close()
							
				except IOError as e:
					print e.strerror
				timeCounter = time.time() - startTime
				os.remove((os.path.join(logTemp, gzFile)))
				print "Files Number:%s Name: %s Processed in %s Seconds" % (fileCounter, gzFile, timeCounter)
	return httpCounter, fileCounter, timeCounter
	
	
def logValidate():
	import hashlib
	okCounter = 0
	failCounter = 0
	startTime = time.time()
	for gzFile in os.listdir(logTemp):
		if gzFile.endswith(".gz"):
			md5Name = gzFile[:-2] + "md5"
			with open(os.path.join(logTemp, md5Name), 'r') as f:
				md5Sum = f.readline()
			gzFileSum = hashlib.md5()
			data = open(os.path.join(logTemp, gzFile), 'rb').read()
			gzFileSum = hashlib.md5(data).hexdigest()
			if gzFileSum == md5Sum:
				okCounter += 1
			elif gzFileSum != md5Sum:
				failCounter += 1
				logging.warning('Validation failed for %s', gzFile)
			print gzFile
			print md5Name
			print gzFileSum
			print md5Sum
	if failCounter == 0:
		return "All Files Verified"
	else:
		return "Validation Failed Check Log For Details"
		
