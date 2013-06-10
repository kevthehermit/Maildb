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
db=Maildatabase()
global newPath
import logging
	
def submit(tmpDir, comment):# THis is for txt files
	for emlfile in os.listdir(tmpDir): #Run for each email file
		from core.parse import emlParse
		lastPath = db.lastLine()
		newPath = str(lastPath)
		logging.info('Record %s Submitted', newPath)
		reportDir = os.path.join(reportRoot, newPath)
		if not os.path.exists(reportDir):
			os.makedirs(reportDir) #Create the Dir Structure
			os.makedirs(os.path.join(reportDir, "attatchments"))
		# SMTP Headers break the parser so remove them
		edit = open(os.path.join(tmpDir, emlfile))
		lines = edit.readlines()
		edit.close()			
		flag = 1
		edited = 0
		new = open(os.path.join(tmpDir, "newFile.eml"), "w")
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
			emailFile = os.path.join(tmpDir, "newFile.eml")
		else:
			emailFile = os.path.join(tmpDir, emlfile)
		shutil.copyfile(emailFile, os.path.join(reportDir, "message.eml"))
		
        emlName = os.path.join(reportDir, "message.eml") # Name of the eml to pass over to the parse script
        parseRun = emlParse(emlName, reportDir, comment) # Call the parse script
        parseRun.run()
        
        
	return newPath
	
def submitpcap(tmpDir, pcapfile, comment): # for pcaps
    
    shutil.copyfile(os.path.join(tmpDir, pcapfile), os.path.join(tmpDir, "raw.pcap"))
    retcode = subprocess.call("(cd %s && tcpflow -r %s)"%(os.path.join(tmpDir), "raw.pcap"), shell=True)
    
    suffix = "00025"
    filecount = 0
    for i in os.listdir(tmpDir):
        if i.endswith(suffix): # i only want emails here
            ###SMTP Headers break the parser so remove them
            filecount +=1
            edit = open(os.path.join(tmpDir, i))
            lines = edit.readlines()
            edit.close()
            new = open(os.path.join(tmpDir, "newFile.eml"), "w")
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
            newPath = str(lastPath)
            logging.info('Record %s Submitted', newPath)
            emlName = os.path.basename(i) # Name of the eml to pass oveflogr to the parse script
            reportDir = os.path.join(reportRoot, newPath)
            logging.info('Pcap Submitted')
            if not os.path.exists(reportDir):
                os.makedirs(reportDir) #Create the Dir Structure
                os.makedirs(os.path.join(reportDir, "attatchments"))
            
            if os.path.getsize(os.path.join(tmpDir, newFile)) > 200: # if file is this small it has no data
            	shutil.copyfile(os.path.join(tmpDir, newFile), os.path.join(reportDir, "message.eml")) #copy the message in as is
            	parseRun = emlParse(i, reportDir, comment) # Call the parse script
            	parseRun.run()
	            	
	            		        

	    
def submithttp(tmpDir, pcapfile, comment):
				
	lastPath = db.lastLine()
	newPath = str(lastPath)
	logging.info('Record %s Submitted', newPath)
	reportDir = os.path.join(reportRoot, newPath) # Set the path
	if not os.path.exists(reportDir):
		os.makedirs(reportDir) #Create the Dir Structure					
	shutil.copyfile(os.path.join(tmpDir, pcapfile), os.path.join(reportDir, "http.pcap")) # Copy The Pcap File in 
	retcode = subprocess.call("(cd %s && tcpflow -r %s -AH)"%(os.path.join(MaildbRoot, "store", newPath), "http.pcap"), shell=True)# Extract all the stream in HTTP Format.
	from core.httpParse import httpParse
	httpParse().http(newPath, comment)
	return newPath

def submitTask(taskFile, comment):
	lastPath = db.lastLine()
	newPath = str(lastPath)
	logging.info('Record %s Submitted', newPath)
	reportDir = os.path.join(reportRoot, newPath) # Set the path
	uploadDir = os.path.join(reportDir, "Case_Files")
	if not os.path.exists(reportDir):
		os.makedirs(reportDir) #Create the Dir Structure
		os.makedirs(uploadDir)
	shutil.copyfile(os.path.join(MaildbRoot, "tmp", taskFile), os.path.join(reportDir, "Case_Files", taskFile))
	dateadded = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	emlmd5 = MailHash().fileMD5(os.path.join(reportDir, "Case_Files", taskFile))
	evType = "Task"
	db.cursor.execute("INSERT INTO main (date_added,eml_md5,Comment,type) VALUES (?,?,?,?)", (dateadded, emlmd5, comment, evType))
	db.conn.commit()
	return newPath

