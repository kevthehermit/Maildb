#!/usr/bin/env python
'''
Copyright (C) 2012-2013 Kevin Breen.
This file is part of the Maildb web application
See the 'LICENSE' File for copying permission.
'''

import os
import sys
import yara
from config.config import yaraRuleFile
from db.db import Maildatabase
  
def fileScan(scanfile, md5Hash, msg_id):
	yaraRules = yara.compile(yaraRuleFile)
	matches = []
	if os.path.getsize(scanfile) > 0:
		for match in yaraRules.match(scanfile):
			matches.append({"name" : match.rule, "meta" : match.meta})
	db = Maildatabase()
	for m in matches:
		yaraRule = m["name"]
		try:
			yaraDesc = m["meta"]["maltype"]
		except:
			yaraDesc = None
		sqlYara = (msg_id, md5Hash, yaraRule, yaraDesc)
		db.storeYara(sqlYara)
	return matches


















	
