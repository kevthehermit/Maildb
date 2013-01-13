#!/usr/bin/env python
'''
Copyright (C) 2012-2013 Kevin Breen.
This file is part of the Maildb web application
See the 'LICENSE' File for copying permission.
'''
# All The Hashing Functions will be in here somewhere

import os
import sys
import hashlib
from core.common import Dictionary


class MailHash():
		  
		
	def HashMD5(self, part_data): #Generate the md5
	
		md5_hash = hashlib.md5()
		md5_hash.update(part_data)

		return md5_hash.hexdigest()
		
	def HashSha1(self, part_data): # Generate the SHA1
		
		sha1_hash = hashlib.sha1()
		sha1_hash.update(part_data)

		return sha1_hash.hexdigest()
		
	def HashSha256(self, part_data): # Generate the SHA 256
		sha256_hash = hashlib.sha256()
		sha256_hash.update(part_data)
		return sha256_hash.hexdigest()
		
	def HashSha512(self, part_data): # Generate the Sha512
		sha512_hash = hashlib.sha512()
		sha512_hash.update(part_data)
		return sha512_hash.hexdigest()
		
	def Hashssdeep(self, part_data):
		import ssdeep
		deep = ssdeep.hash(part_data)
		return deep

	def fileMD5(self, filePath):
		fh = open(filePath, 'rb')
		m = hashlib.md5()
		while True:
			data = fh.read(8192)
			if not data:
				break
			m.update(data)
		return m.hexdigest()






















	
