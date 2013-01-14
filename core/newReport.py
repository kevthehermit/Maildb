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
		genDate = datetime.now().strftime("%Y-%m-%d")
		repDate = date+"%"

		nonTasks = db.cursor.execute("SELECT Comment, Revmatch, COUNT(*) as comm FROM main WHERE Comment NOT LIKE 'Tasking%' AND date_added LIKE ? GROUP BY Comment", (repDate,)).fetchall()
		tasks = db.cursor.execute("SELECT Comment, Revmatch, COUNT(*) as comm FROM main WHERE Comment LIKE 'Tasking%' AND date_added LIKE ? GROUP BY Comment", (repDate,)).fetchall()
		dateline = "<h1>Report for "+date+"</h1> <h3>Created on " + str(genDate) + "</h3>"
		countAll = (db.cursor.execute("SELECT COUNT(*) as counted FROM main WHERE date_added LIKE ?", (repDate,)).fetchone()).counted
		countNonTasks = (db.cursor.execute("SELECT COUNT(*) as counted FROM main WHERE Comment NOT LIKE 'Tasking%' AND date_added LIKE ?", (repDate,)).fetchone()).counted
		countTasks = (db.cursor.execute("SELECT COUNT(*) as counted FROM main WHERE Comment LIKE 'Tasking%' AND date_added LIKE ?", (repDate,)).fetchone()).counted
		countEvents = (db.cursor.execute("SELECT COUNT(*) as counted FROM main WHERE Revmatch='1' AND date_added LIKE ?", (repDate,)).fetchone()).counted
		countOut = (db.cursor.execute("SELECT COUNT(*) as counted FROM main WHERE (Revmatch='0' OR Revmatch='3') AND date_added LIKE ?", (repDate,)).fetchone()).counted
		counts = [countAll, countNonTasks, countTasks, countEvents, countOut]
		
		ntaskNames = []
		ntaskRev = []
		ntaskEv = []
		ntaskOut = []		
		for row in nonTasks:
			revCount = (db.cursor.execute("SELECT COUNT(*) as counted FROM main WHERE Comment='"+ row.Comment +"'AND Revmatch='2' AND date_added LIKE ?", (repDate,)).fetchone()).counted			
			evCount = (db.cursor.execute("SELECT COUNT(*) as counted FROM main WHERE Comment='"+ row.Comment +"'AND Revmatch='1' AND date_added LIKE ?", (repDate,)).fetchone()).counted
			outCount = (db.cursor.execute("SELECT COUNT(*) as counted FROM main WHERE Comment='"+ row.Comment +"'AND (Revmatch='0' OR Revmatch='3') AND date_added LIKE ?", (repDate,)).fetchone()).counted
			ntaskRev.append(revCount)
			ntaskEv.append(evCount)
			ntaskOut.append(outCount)
			ntaskNames.append(row.Comment)
			
		taskNames = []
		taskRev = []
		taskEv = []
		taskOut = []
		for row in tasks:
			revCount = (db.cursor.execute("SELECT COUNT(*) as counted FROM main WHERE Comment='"+ row.Comment +"'AND Revmatch='2' AND date_added LIKE ?", (repDate,)).fetchone()).counted
			evCount = (db.cursor.execute("SELECT COUNT(*) as counted FROM main WHERE Comment='"+ row.Comment +"'AND Revmatch='1' AND date_added LIKE ?", (repDate,)).fetchone()).counted
			outCount = (db.cursor.execute("SELECT COUNT(*) as counted FROM main WHERE Comment='"+ row.Comment +"'AND (Revmatch='0' OR Revmatch='3') AND date_added LIKE ?", (repDate,)) .fetchone()).counted
			taskRev.append(revCount)
			taskEv.append(evCount)
			taskOut.append(outCount)
			taskNames.append(row.Comment)
		
		return (ntaskNames, ntaskRev, ntaskEv, ntaskOut, taskNames, taskRev, taskEv, taskOut, counts)
		
		
	def attatchRep(self, date):
		genDate = datetime.now()
		repDate = date+"%"
		attatch = db.cursor.execute("SELECT fileExt, count(fileExt) as counted from attatch LEFT OUTER JOIN main ON main.msg_id = attatch.msg_id WHERE main.date_added LIKE ? GROUP BY fileExt", (repDate,)).fetchall()
		attExt = []
		countNonEv = []
		countEv = []
		totalAtt = "12"
		for row in attatch:
			attExt.append(row.fileExt)
			ev = db.cursor.execute("SELECT fileExt, count(fileExt) as counted from attatch LEFT OUTER JOIN main ON main.msg_id = attatch.msg_id WHERE main.date_added LIKE ? AND NOT main.Revmatch='1' AND fileExt='"+str(row.fileExt)+"'", (repDate,)).fetchone()
			nonEv = db.cursor.execute("SELECT fileExt, count(fileExt) as counted from attatch LEFT OUTER JOIN main ON main.msg_id = attatch.msg_id WHERE main.date_added LIKE ? AND NOT main.Revmatch!='1' AND fileExt='"+str(row.fileExt)+"'", (repDate,)).fetchone()
			countNonEv.append(ev.counted)
			countEv.append(nonEv.counted)
		return (attExt, countNonEv, countEv, totalAtt)


		

