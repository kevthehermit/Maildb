#!/usr/bin/env python
'''
Copyright (C) 2012-2013 Kevin Breen.
This file is part of the Maildb web application
See the 'LICENSE' File for copying permission.
'''

import os, subprocess
from config.config import MaildbRoot, ProxyPort, SSLPort
from core.hashing import MailHash
from datetime import datetime
from db.db import Maildatabase
from base64 import b64decode
import urlparse
import shutil
db=Maildatabase()
from BaseHTTPServer import BaseHTTPRequestHandler
from StringIO import StringIO
from core.common import HTTPRequest
import core.yarascan
import logging

## http://stackoverflow.com/questions/4685217/parse-raw-http-headers

class httpParse:

    def http(self, msg_id, comment):        		
		evType = "web"
		match = '0'
		dateadded = datetime.now()
		streamDir = os.path.join(MaildbRoot, "store", msg_id)
		emlmd5 = MailHash().fileMD5(os.path.join(MaildbRoot, "store", msg_id, "http.pcap"))
		mainSql = (dateadded, emlmd5, match, comment, evType)
		db.parseHttpMain(mainSql)
		trunCounter = 0
		Counter = 0
		for httpReq in os.listdir(streamDir):
			try:
				if httpReq.endswith(ProxyPort) or httpReq.endswith(SSLPort):					
					sIP = httpReq[0:15]
					sPort = httpReq[16:21]
					dIP = httpReq[22:37]
					dPort = httpReq[38:43]
					httpResp = dIP + "." + dPort + "-" + sIP + "." + sPort + "-HTTP"				
					httpFile = httpResp + "BODY"
					if os.path.exists(os.path.join(streamDir, httpFile+"-GZIP")):
						httpFile = httpResp + "BODY-GZIP"				
					header = open(os.path.join(streamDir, httpReq), 'r')
					reqHeader = header.read()
					header.close				
					request = HTTPRequest(reqHeader)
					flowSql = (msg_id, sIP, sPort, dIP, dPort)
					if os.path.exists(os.path.join(streamDir, httpResp)):					
						respHeaders = open(os.path.join(streamDir, httpResp), 'r')
						response = respHeaders.readline()
						dbResponse = response[:-2]
						dbRequest = request.command
						dbPath = request.path
						dbHost = request.headers['host']
						try:
							dbAgent = request.headers['user-agent']
						except:
							dbAgent = "N/A"
						try:
							dbRefer = request.headers['Referer']
						except:
							dbRefer = "N/A"
						try:
							codedProx = request.headers['Proxy-Authorization'][6:]
							dbProxy = b64decode(codedProx)
						except:
							dbProxy = "N/A"
						
						# Main httpDB
						streamSql = (msg_id, dbRequest, dbHost, dbPath, dbRefer, dbProxy, dbResponse, httpReq, httpResp, httpFile)
						db.parseHttpInfo(flowSql, streamSql)
						urlpath = urlparse.urlsplit(dbPath).path
						structure = urlpath.split('/')
						fullpath = structure[1:-1]				
						storeSite = os.path.join(MaildbRoot, "store", msg_id, "sites")
						storeHost = os.path.join(storeSite, dbHost)
						if not os.path.exists(storeSite):
							os.mkdir(storeSite)
				
						if not os.path.exists(storeHost):
							os.mkdir(storeHost)
						fileDir = ""
						for level in fullpath:
							fileDir += level + os.sep
						filePath = os.path.join(storeHost, fileDir[:-1])
						if not os.path.exists(filePath):
							os.makedirs(filePath)													
						if os.path.exists(os.path.join(streamDir, httpFile)):
							fileName = os.path.basename(urlpath)
							query = urlparse.urlsplit(dbPath).query
							if query:
								fullName = fileName+"?"+query # ? is an Illegal Filename Char on Windows OK on linux
							elif not fileName:
								fullName = "index.html"
							else:
								fullName = fileName
							try: # 255 character limit can be broken easily and often in this
								shutil.copyfile(os.path.join(streamDir, httpFile), os.path.join(filePath, fullName))
								scanFile = os.path.join(filePath, fullName)
								Counter += 1							
							except IOError as e:
								if e.errno == 36: # this is the error No for a long filename									
									trunCounter += 1
									newName = "Truncated" + str(trunCounter)
									shutil.copyfile(os.path.join(streamDir, httpFile), os.path.join(filePath, newName))
									scanFile = os.path.join(filePath, newName)
									Counter += 1
									logging.info('Truncated FileName From %s To %s', fullName, newName)
								else:
									logging.info('Failed to copy %s With error %s:%s', fileName, e.errno, e.strerror)
									
							# yara here							
							

							if os.path.exists(scanFile):
								md5Hash = MailHash().fileMD5(scanFile)
								result = core.yarascan.fileScan(scanFile, md5Hash, msg_id)
								if result:
									match = '3'
							else:
								md5Hash = "None"
					else:
						logging.info('File Doesnt Exist %s', httpResp)
						
			except:
				logging.info('Failed to Parse File %s', httpResp)
		sqlYara = (Counter, match, msg_id)
		db.parseYara(sqlYara)									
		for filename in os.listdir(streamDir):
			if not (filename == "http.pcap" or filename == "report.xml" or filename == "sites"):
				os.remove(os.path.join(streamDir, filename))						
					

				
				
				

						
					
				
				
		


