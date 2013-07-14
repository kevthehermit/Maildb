#!/usr/bin/env python
'''
Copyright (C) 2012-2013 Kevin Breen.
This file is part of the Maildb web application
See the 'LICENSE' File for copying permission.
'''

import base64
import codecs
import hashlib
import sys
import os.path, os
import subprocess
import shutil
import email, mimetypes, errno
import zipfile
import email.utils
from bs4 import BeautifulSoup
from email.utils import getaddresses
from datetime import datetime
from db.db import Maildatabase
from config.config import *
from core.hashing import MailHash
import re
db=Maildatabase()


class emlParse(object):
	def __init__(self, emlName, reportDir, comment):

		self.reportDir = reportDir
		self.msgFile = os.path.join(reportDir, "message.eml")

		evType="mail"				
		dateadded = datetime.now()
		emlmd5 = MailHash().fileMD5(self.msgFile)
		sqlMain = (dateadded, emlmd5, '0', comment, evType)
		db.parseMain(sqlMain)
				
	def run(self):
		x = open(os.path.join(self.reportDir, self.msgFile))
		msg = email.message_from_file(x) # open the eml file so we can parse ie
		x.close()
		
		################# Header Information ###################
		# Get me all the sections then write them as one big sql line
		
		dateLine = msg.get('Date')
		
		msg_id = int(os.path.basename(self.reportDir)) # Unique id for this email used to cross ref other tables
		try:
			fromAdd = msg['from'] # might need to tidy this up a little bit using the address parse option
		except:
			fromAdd = msg['from']
		stringIt = str(fromAdd)
		dbFrom = stringIt[stringIt.find("<")+1:stringIt.find(">")]
		# very messy need to fix this.
		addDomain = dbFrom[dbFrom.find("@")+1:] 
		try:
			subjectLine = unicode(msg['subject'], errors = 'replace')
		except:
			subjectLine = msg['subject']
		x_mailer = msg['X-Mailer']
		x_priority = msg['X-Priority']
		try:
			message_id = re.sub('[<>]', '', msg['Message-ID'])
		except:
			message_id = msg['Message-ID']
		hops = msg.get_all('Received')
		if hops:
			for hop in hops:
				hop = re.sub('[<>]', '', hop)
				sqlHop = (msg_id, hop)
				db.parseHops(sqlHop)
		try:
			sender = re.sub('[<>]', '', msg.get('From')) # remove <> so it renders correctly in the HTML
		except:
			sender = dbFrom
		try:
			to_add = re.sub('[<>]', '', msg.get('To')) #
		except:
			to_add = msg.get('To')
		try:
			cc_add = re.sub('[<>]', '', msg.get('cc'))
		except:
			cc_add = msg.get('cc')
		try:
			bcc_add = re.sub('[<>]', '', msg.get('Bcc'))
		except:
			bcc_add = msg.get('bcc')
		sqlHeader = ( msg_id, dateLine, sender, addDomain, subjectLine, x_mailer, x_priority, message_id, cc_add, bcc_add, to_add)
		db.parseHeader(sqlHeader)
		
		counter = 0
		for part in msg.walk():
			if part.get_content_maintype() == 'multipart':				
				continue
			
			if part.get_content_type() == 'text/plain': # Plain Text Body				
				contents = part.get_payload(decode=True)
				links = re.findall(r'(https?://\S+)', contents)
				link_type = "url"
				for urls in links:
					sqlUrl = (msg_id, link_type, urls)
					db.parseLinks(sqlUrl)
								
				from core.cleanHtml import cleanHTML
				htmlStrip = cleanHTML().safe_html(contents)
				if htmlStrip is not None:
					fp = open(os.path.join(self.reportDir, "attatchments", "body.txt"), 'wb')
					fp.write(htmlStrip.encode('ascii', 'ignore'))
					fp.close()
				
			if part.get_content_type() == 'text/html': # HTML Body
				contents = part.get_payload(decode=True)
				soup = BeautifulSoup(contents)
				for link in soup.find_all('a'):
					link_type = "url"
					urls = link.get('href')
					sqlUrl = (msg_id, link_type, urls)
					db.parseLinks(sqlUrl)
				for images in soup.find_all('img'):
					link_type = "img"
					image = images.get('src')
					sqlImg = (msg_id, link_type, image)
					db.parseLinks(sqlImg)
				for iframes in soup.find_all('iframe'):
					link_type = "iframe"
					frames = "Fix Me"
					sqlFrames = (msg_id, link_type, frames)
					db.parseLinks(sqlFrames)
								
				from core.cleanHtml import cleanHTML
				htmlStrip = cleanHTML().safe_html(contents)
				if htmlStrip is not None:
					fp = open(os.path.join(self.reportDir, "attatchments", "htmlbody.txt"), 'wb')
					fp.write(htmlStrip.encode('ascii', 'ignore'))
					fp.close()
 			
			if part.get('Content-Disposition') is None: # Actual File attatchments here
				continue
												
			from bs4 import UnicodeDammit
			filenameraw = str(part.get_filename())			
			dammit = UnicodeDammit(filenameraw)
			enctype = dammit.original_encoding
			if enctype == "ascii":
				filename = dammit.unicode_markup
			else:
				ext = mimetypes.guess_extension(part.get_content_type())
				filename = '%s-encoded-File-%s.%s' % (enctype, counter, ext)
								
			if filename == 'None': # if theres no name then guess the extension and make something up
				ext = mimetypes.guess_extension(part.get_content_type())
				if not ext:
					ext = ".bin"
				filename = 'part-%03d%s' % (counter, ext)
			counter +=1
			fp = open(os.path.join(self.reportDir, "attatchments", filename), 'wb') # write the attatchment out to a folder
			# Deal With Zero Size Files
			if part.get_payload(decode=True) is None:
				part_data = "This is a Zero Byte File"
				fp.write(part_data)
				fp.close()			
			else:
				fp.write(part.get_payload(decode=True))
				fp.close()
				part_data = part.get_payload(decode=True)
			fileSize = os.path.getsize(os.path.join(self.reportDir, "attatchments", filename))
			fileExt = os.path.splitext(os.path.join(self.reportDir, "attatchments", filename))		
			md5Hash = MailHash().HashMD5(part_data)
			sha256Hash = MailHash().HashSha256(part_data)
				
			if ssdeepcheck == '1': # check to see if users has enabled ssdeep
				try: 	#gracefull fail if the python wrapper is not installed.
				
					ssdHash = MailHash().Hashssdeep(part_data)
				except:
					ssdHash = "0"
			else:
				ssdHash = "0"
			
			import core.yarascan
			filetoScan = os.path.join(self.reportDir, "attatchments", filename)
			result = core.yarascan.fileScan(filetoScan, md5Hash, msg_id)
			match = '0'
			if result:
				yaraMatch = '3'
				match = '3'
			else:
				yaraMatch = '0'
					
			# database stuff here
		
			sqlAttatchments = (msg_id, str(filename), fileExt[1][1:], fileSize, md5Hash, sha256Hash, ssdHash, yaraMatch)			
			db.parseAttatch(sqlAttatchments)
			sqlYara = (counter, match, msg_id)
			db.parseYara(sqlYara)

			
			

			

		

		
		
