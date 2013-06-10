#!/usr/bin/env python
'''
Copyright (C) 2013 Kevin Breen.
Log Parse
Version 0.1
'''

import os
import sys
from gzip import GzipFile
import shlex
import time
import MySQLdb
import logging
from datetime import datetime
logTemp = "/mnt/DATA/dev/logtmp"
import subprocess
import cStringIO
io_method = cStringIO.StringIO

from multiprocessing import Pool

def webParse(gzFile):
	conn = MySQLdb.connect("localhost", "tvtLog", "tvtLog", "logDB")
	cursor = conn.cursor()	
	if gzFile.endswith(".gz"):
		p = subprocess.Popen(["zcat", gzFile], stdout = subprocess.PIPE)
		fh = io_method(p.communicate()[0])
		print "Processing ", gzFile
		assert p.returncode == 0
	for line in fh:
		if not line.startswith("#"):
			logEntry = shlex.split(line,posix=False)
			cursor.execute('INSERT INTO http VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);', tuple(logEntry))
	conn.commit()
	os.remove((os.path.join(logTemp, gzFile)))
	
def webThread(arg, dirname, names):
	pool = Pool()
	results = pool.map(webParse, [os.path.join(dirname, name) for name in names])


if __name__ == '__main__':
	start = time.time()
	os.path.walk(logTemp, webThread, None)
	print "Process Time", time.time()-start



		
