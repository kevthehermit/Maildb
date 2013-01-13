#!/usr/bin/env python
'''
Copyright (C) 2012-2013 Kevin Breen.
This file is part of the Maildb web application
See the 'LICENSE' File for copying permission.
'''

# All The reporting Functions Will Be Here


import os
import sys
from datetime import datetime
from db.db import Maildatabase
from config.config import *
db=Maildatabase()

class Reporting():
		
	def mainRep(self, date):
		genDate = datetime.now()
		repDate = date+"%"
		countAll = db.cursor.execute("SELECT COUNT(*) FROM main WHERE date_added LIKE ?", (repDate,)).fetchone()
		countNonTasks = db.cursor.execute("SELECT COUNT(*) FROM main WHERE Comment NOT LIKE 'Tasking%' AND date_added LIKE ?", (repDate,)).fetchone()
		countTasks = db.cursor.execute("SELECT COUNT(*) FROM main WHERE Comment LIKE 'Tasking%' AND date_added LIKE ?", (repDate,)).fetchone()
		nonTasks = db.cursor.execute("SELECT Comment, Revmatch, COUNT(*) as comm FROM main WHERE Comment NOT LIKE 'Tasking%' AND date_added LIKE ? GROUP BY Comment", (repDate,)).fetchall()
		tasks = db.cursor.execute("SELECT Comment, Revmatch, COUNT(*) as comm FROM main WHERE Comment LIKE 'Tasking%' AND date_added LIKE ? GROUP BY Comment", (repDate,)).fetchall()
		dateline = "<h1>Report for "+date+"</h1> <h3>Created on " + str(genDate) + "</h3>"
		allTasks = str(countAll["COUNT(*)"])
		
		ntaskNames = []
		ntaskRev = []
		ntaskEv = []
		ntaskOut = []		
		for row in nonTasks:
			revCount = db.cursor.execute("SELECT COUNT(*) FROM main WHERE Comment='"+ row.Comment +"'AND Revmatch='2' AND date_added LIKE ?", (repDate,)).fetchone()			
			evCount = db.cursor.execute("SELECT COUNT(*) FROM main WHERE Comment='"+ row.Comment +"'AND Revmatch='1' AND date_added LIKE ?", (repDate,)).fetchone()
			outCount = db.cursor.execute("SELECT COUNT(*) FROM main WHERE Comment='"+ row.Comment +"'AND Revmatch='0' AND date_added LIKE ?", (repDate,)).fetchone()
			#ntaskTotal.append(str(row.comm))
			ntaskRev.append(str(revCount["COUNT(*)"]))
			ntaskEv.append(str(evCount["COUNT(*)"]))
			ntaskOut.append(str(outCount["COUNT(*)"]))
			ntaskNames.append(row.Comment)
			
		taskNames = []
		taskRev = []
		taskEv = []
		taskOut = []
		for row in tasks:
			revCount = db.cursor.execute("SELECT COUNT(*) FROM main WHERE Comment='"+ row.Comment +"'AND Revmatch='2' AND date_added LIKE ?", (repDate,)).fetchone()
			evCount = db.cursor.execute("SELECT COUNT(*) FROM main WHERE Comment='"+ row.Comment +"'AND Revmatch='1' AND date_added LIKE ?", (repDate,)).fetchone()
			outCount = db.cursor.execute("SELECT COUNT(*) FROM main WHERE Comment='"+ row.Comment +"'AND Revmatch='0' AND date_added LIKE ?", (repDate,)) .fetchone()
			#taskTotal.append(str(row.comm))
			taskRev.append(str(revCount["COUNT(*)"]))
			taskEv.append(str(evCount["COUNT(*)"]))
			taskOut.append(str(outCount["COUNT(*)"]))
			taskNames.append(row.Comment)
		
		return (ntaskNames, ntaskRev, ntaskEv, ntaskOut, taskNames, taskRev, taskEv, taskOut)

