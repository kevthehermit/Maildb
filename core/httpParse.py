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
from core.logging import MaildbLog
from core.yarascan import Scan

## http://stackoverflow.com/questions/4685217/parse-raw-http-headers

class httpParse:

    def http(self, msg_id, comment):
        		
		evType = "web"
		mailMatch = "0"
		dateadded = datetime.now()
		streamDir = os.path.join(MaildbRoot, "store", msg_id)
		emlmd5 = MailHash().fileMD5(os.path.join(MaildbRoot, "store", msg_id, "http.pcap"))

		
		
		for httpReq in os.listdir(streamDir):
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
				
				if os.path.exists(os.path.join(streamDir, httpResp)):
					
					respHeaders = open(os.path.join(streamDir, httpResp), 'r')
					response = respHeaders.readline()
					dbResponse = response[:-2]
					dbRequest = request.command
					dbPath = request.path
					try:
						dbHost = request.headers['host']
					except:
						dbHost = "N/A"
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
					db.cursor.execute("INSERT INTO flows (msg_id, SIP, Sport, DIP, Dport) VALUES (?,?,?,?,?)", (msg_id, sIP, sPort, dIP, dPort))
				
					# httpHeadersDB
					db.cursor.execute("INSERT INTO streams VALUES (?,?,?,?,?,?,?,?,?,?)", (msg_id, dbRequest, dbHost, dbPath, dbRefer, dbProxy, dbResponse, httpReq, httpResp, httpFile))
					db.conn.commit()

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
							
						except IOError as e:
							if e.errno == 36: # this is the error No for a long filename
								shutil.copyfile(os.path.join(streamDir, httpFile), os.path.join(filePath, "Truncated"))
								fullName = "Truncated"
							else:
								log = "##Error##, Failed to Copy " + fullName + str(e.errno) + " " + str(e.strerror)
								MaildbLog().logEntry(log)
						# yara here
						scanFile = os.path.join(filePath, fullName)
						md5Hash = MailHash().fileMD5(scanFile)
						result = Scan().httpScan(scanFile, md5Hash)
						if result:
							mailMatch = '3'

				else:
					log = "##Error##, File Doesnt Exist " + httpResp
					MaildbLog().logEntry(log)						
		for filename in os.listdir(streamDir):
			if not (filename == "http.pcap" or filename == "report.xml" or filename == "sites"):
				os.remove(os.path.join(streamDir, filename))						
		db.cursor.execute("INSERT INTO main (date_added,eml_md5,Revmatch,Comment,type) VALUES (?,?,?,?,?)", (dateadded, emlmd5, mailMatch, comment, evType))
		db.conn.commit()					

				
				
				

						
					
				
				
		


