#!/usr/bin/env python
'''
Copyright (C) 2012-2013 Kevin Breen.
This file is part of the Maildb web application
See the 'LICENSE' File for copying permission.
'''


import codecs
import sys
import os.path, os
import subprocess
import shutil
import time
from core.hashing import MailHash
from datetime import datetime
from db.db import Maildatabase
from config.config import reportRoot, transferDir,  MaildbRoot
from core.logging import MaildbLog	
writeLog = MaildbLog()
db=Maildatabase()
global newPath
class emlSubmit():

	
	def submit(self, comment):
		for emlfile in os.listdir(transferDir): #Run for each email file
			from core.parse import emlParse
			lastPath = db.lastLine()
			print emlfile
			try: # this try means an empty db file wont break it
				newPath = str(lastPath + 1) # will be used to set the database and match it to a physical location
			except:
				newPath = '1'
			log = "##INFO## Email Submitted With ID " + newPath
			writeLog.logEntry(log)
			reportDir = os.path.join(reportRoot, newPath)
			if not os.path.exists(reportDir):
				os.makedirs(reportDir) #Create the Dir Structure
				os.makedirs(os.path.join(reportDir, "attatchments"))
			# SMTP Headers break the parser so remove them
			edit = open(os.path.join(MaildbRoot, "tmp", emlfile))
			lines = edit.readlines()
			edit.close()			
			flag = 1
			edited = 0
			new = open(os.path.join(MaildbRoot, "tmp", "newFile.eml"), "w")
			for line in lines:
				if line.startswith("EHLO") or line.startswith("220 "):
					flag = 0
					edited = 1
				if line.startswith("DATA") or line.startswith("354 Start") or line.startswith("354 Enter mail"):
					flag = 1
				if flag and not (line.startswith("DATA") or line.startswith("354 Start") or line.startswith("354 Enter mail") or line.startswith("250 ")):					
					new.write(line)
			new.close() 
			
			if edited:
				emailFile = os.path.join(transferDir, "newFile.eml")
				print "Copy Edited"
			else:
				emailFile = os.path.join(transferDir, emlfile)
				print "copy Non Edited"
			shutil.copyfile(emailFile, os.path.join(reportDir, "message.eml"))
			
	        emlName = os.path.join(reportDir, "message.eml") # Name of the eml to pass over to the parse script
	        parseRun = emlParse(emlName, reportDir, comment) # Call the parse script
	        parseRun.run()
	        
	        
		return newPath
	
	def submitpcap(self, pcapfile, comment):

	    if not os.path.exists(os.path.join(MaildbRoot, "tmp")):
	        os.mkdir(os.path.join(MaildbRoot, "tmp"))	    
	    shutil.copyfile(os.path.join(MaildbRoot, "tmp", pcapfile), os.path.join(transferDir, "raw.pcap"))
	    retcode = subprocess.call("(cd %s && tcpflow -r %s)"%(os.path.join(MaildbRoot, "tmp"), "raw.pcap"), shell=True)
	    
	    suffix = "00025"
	    filecount = 0
	    for i in os.listdir(transferDir):
	        if i.endswith(suffix): # i only want emails here
	            ###SMTP Headers break the parser so remove them
	            filecount +=1
	            edit = open(os.path.join(transferDir, i))
	            lines = edit.readlines()
	            edit.close()
	            new = open(os.path.join(transferDir, "newFile.eml"), "w")
	            edited = 0	            
	            flag = 1
	            for line in lines:
	                if line.startswith("EHLO") or line.startswith("220 "):
	                    flag = 0
	                if line.startswith("DATA") or line.startswith("354 Start") or line.startswith("354 Enter mail"):
	                    flag = 1
	                if flag and not (line.startswith("DATA") or line.startswith("354 Start") or line.startswith("354 Enter mail") or line.startswith("250 ")):
	                    new.write(line)
	            new.close()
	            newFile = "newFile.eml"
	            from core.parse import emlParse
	            lastPath = db.lastLine()
	            try: # this try means an empty db file wont break it
	                newPath = str(lastPath + 1) # will be used to set the database and match it to a physical location

	            except:
	                newPath = '1'
	            emlName = os.path.basename(i) # Name of the eml to pass over to the parse script
	            reportDir = os.path.join(reportRoot, newPath)
	            log = "##INFO##, PCAP Submitted With ID " + newPath
	            writeLog.logEntry(log)
	            if not os.path.exists(reportDir):
	                os.makedirs(reportDir) #Create the Dir Structure
	                os.makedirs(os.path.join(reportDir, "attatchments"))
	            
	            if os.path.getsize(os.path.join(transferDir, newFile)) > 200: # if file is this small it has no data
	            	shutil.copyfile(os.path.join(transferDir, newFile), os.path.join(reportDir, "message.eml")) #copy the message in as is
	            	parseRun = emlParse(i, reportDir, comment) # Call the parse script
	            	parseRun.run()
	            	
	            		        

	    
	def submithttp(self, pcapfile, comment):

		lastPath = db.lastLine()			
		try: # this try means an empty db file wont break it
			newPath = str(lastPath + 1) # will be used to set the database and match it to a physical location
		except:
			newPath = '1'
		reportDir = os.path.join(reportRoot, newPath) # Set the path
		log = "##INFO##, HTTP Submitted With ID " + newPath
		writeLog.logEntry(log)
		if not os.path.exists(reportDir):
			os.makedirs(reportDir) #Create the Dir Structure					
		shutil.copyfile(os.path.join(MaildbRoot, "tmp", pcapfile), os.path.join(reportDir, "http.pcap")) # Copy The Pcap File in 
		retcode = subprocess.call("(cd %s && tcpflow -r %s -AH)"%(os.path.join(MaildbRoot, "store", newPath), "http.pcap"), shell=True)# Extract all the stream in HTTP Format.
		from core.httpParse import httpParse
		httpParse().http(newPath, comment)
		return newPath

	def submitTask(self, taskFile, comment):
		lastPath = db.lastLine()			
		try: # this try means an empty db file wont break it
			newPath = str(lastPath + 1) # will be used to set the database and match it to a physical location
		except:
			newPath = '1'
		reportDir = os.path.join(reportRoot, newPath) # Set the path
		log = "##INFO##, Task Submitted With ID " + newPath
		writeLog.logEntry(log)
		if not os.path.exists(reportDir):
			os.makedirs(reportDir) #Create the Dir Structure
		
		shutil.copyfile(os.path.join(MaildbRoot, "tmp", taskFile), os.path.join(reportDir, taskFile)) # Copy The Pcap File in
		dateadded = datetime.now()
		emlmd5 = MailHash().fileMD5(os.path.join(reportDir, taskFile))
		evType = "Task"
		db.cursor.execute("INSERT INTO main (date_added,eml_md5,Comment,type) VALUES (?,?,?,?)", (dateadded, emlmd5, comment, evType))
		db.conn.commit()
		return newPath

