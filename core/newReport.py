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
import sqlite3

class Reporting():
		
	def mainRep(self, startDate, endDate):
		conn = sqlite3.connect(DBFile)
		cursor = conn.cursor()
		genDate = datetime.now().strftime("%Y-%m-%d")
		csv = os.path.join(MaildbRoot, "web", "static", "graph", "allSubmits.csv")
		nonTasks = cursor.execute("SELECT Comment, Revmatch, COUNT(*) as comm FROM main WHERE Comment NOT LIKE 'Tasking%' AND date_added BETWEEN ? AND ? GROUP BY Comment", (startDate, endDate)).fetchall()
		tasks = cursor.execute("SELECT Comment, Revmatch, COUNT(*) as comm FROM main WHERE Comment LIKE 'Tasking%' AND date_added BETWEEN ? AND ? GROUP BY Comment", (startDate, endDate)).fetchall()
		dateline = "<h1>Report for "+startDate+" to "+endDate+"</h1> <h3>Created on " + str(genDate) + "</h3>"
		countAll = (cursor.execute("SELECT COUNT(*) as counted FROM main WHERE date_added BETWEEN ? AND ?", (startDate, endDate)).fetchone())[0]
		countNonTasks = (cursor.execute("SELECT COUNT(*) as counted FROM main WHERE Comment NOT LIKE 'Tasking%' AND date_added BETWEEN ? AND ? ", (startDate, endDate)).fetchone())[0]
		countTasks = (cursor.execute("SELECT COUNT(*) as counted FROM main WHERE Comment LIKE 'Tasking%' AND date_added BETWEEN ? AND ? ", (startDate, endDate)).fetchone())[0]
		countEvents = (cursor.execute("SELECT COUNT(*) as counted FROM main WHERE Revmatch='1' AND date_added BETWEEN ? AND ? ", (startDate, endDate)).fetchone())[0]
		countOut = (cursor.execute("SELECT COUNT(*) as counted FROM main WHERE (Revmatch='0' OR Revmatch='3') AND date_added BETWEEN ? AND ? ", (startDate, endDate)).fetchone())[0]
		counts = [countAll, countNonTasks, countTasks, countEvents, countOut]
		
		ntaskNames = ["categories,"]
		ntaskRev = ["Reviewed,"]
		ntaskEv = ["Event,"]
		ntaskOut = ["Outstanding,"]		
		for row in nonTasks:
			revCount = (cursor.execute("SELECT COUNT(*) as counted FROM main WHERE Comment='"+ row[0] +"'AND Revmatch='2' AND date_added BETWEEN ? AND ? ", (startDate, endDate)).fetchone())[0]			
			evCount = (cursor.execute("SELECT COUNT(*) as counted FROM main WHERE Comment='"+ row[0] +"'AND Revmatch='1' AND date_added BETWEEN ? AND ? ", (startDate, endDate)).fetchone())[0]
			outCount = (cursor.execute("SELECT COUNT(*) as counted FROM main WHERE Comment='"+ row[0] +"'AND (Revmatch='0' OR Revmatch='3') AND date_added BETWEEN ? AND ? ", (startDate, endDate)).fetchone())[0]
			ntaskRev.append(str(revCount) + ",")
			ntaskEv.append(str(evCount) + ",")
			ntaskOut.append(str(outCount) + ",")
			ntaskNames.append(str(row[0]) + ",")
			
		taskNames = []
		taskRev = []
		taskEv = []
		taskOut = []
		for row in tasks:
			revCount = (cursor.execute("SELECT COUNT(*) as counted FROM main WHERE Comment='"+ row[0] +"'AND Revmatch='2' AND date_added BETWEEN ? AND ? ", (startDate, endDate)).fetchone())[0]
			evCount = (cursor.execute("SELECT COUNT(*) as counted FROM main WHERE Comment='"+ row[0] +"'AND Revmatch='1' AND date_added BETWEEN ? AND ? ", (startDate, endDate)).fetchone())[0]
			outCount = (cursor.execute("SELECT COUNT(*) as counted FROM main WHERE Comment='"+ row[0] +"'AND (Revmatch='0' OR Revmatch='3') AND date_added BETWEEN ? AND ? ", (startDate, endDate)) .fetchone())[0]
			taskRev.append(str(revCount) + ",")
			taskEv.append(str(evCount) + ",")
			taskOut.append(str(outCount) + ",")
			taskNames.append(str(row[0]) + ",")
		f = open(csv, "wb")
		for name in ntaskNames:
			f.write(name)
		for name in taskNames:
			f.write(name)
		f.write("\n")
		for name in ntaskRev:
			f.write(name)
		for name in taskRev:
			f.write(name)
		f.write("\n")
		for name in ntaskEv:
			f.write(name)
		for name in taskEv:
			f.write(name)
		f.write("\n")
		for name in ntaskOut:
			f.write(name)
		for name in taskOut:
			f.write(name)
		f.close()
		cursor.close()	
		return (ntaskNames, ntaskRev, ntaskEv, ntaskOut, taskNames, taskRev, taskEv, taskOut, counts, dateline)
		
		
	def attatchRep(self, startDate, endDate):
		conn = sqlite3.connect(DBFile)
		cursor = conn.cursor()
		genDate = datetime.now().strftime("%Y-%m-%d")
		attatch = cursor.execute("SELECT fileExt, count(fileExt) as counted from attatch LEFT OUTER JOIN main ON main.msg_id = attatch.msg_id WHERE main.date_added BETWEEN ? AND ? GROUP BY fileExt", (startDate, endDate)).fetchall()
		csv = os.path.join(MaildbRoot, "web", "static", "graph", "attReport.csv")
		attExt = ["Categories,"]
		countNonEv = ["Non-Event,"]
		countEv = ["Event,"]
		totalAtt = "12"
		f = open(csv, "wb")
		for row in attatch:
			attExt.append(row[0] + ",")
			ev = cursor.execute("SELECT fileExt, count(fileExt) as counted from attatch LEFT OUTER JOIN main ON main.msg_id = attatch.msg_id WHERE main.date_added BETWEEN ? AND ? AND NOT main.Revmatch='1' AND fileExt='"+str(row[0])+"'", (startDate, endDate)).fetchone()
			nonEv = cursor.execute("SELECT fileExt, count(fileExt) as counted from attatch LEFT OUTER JOIN main ON main.msg_id = attatch.msg_id WHERE main.date_added BETWEEN ? AND ? AND NOT main.Revmatch!='1' AND fileExt='"+str(row[0])+"'", (startDate, endDate)).fetchone()
			countNonEv.append(str(ev[1]) + ",")
			countEv.append(str(nonEv[1]) + ",")
		for value in attExt:
			f.write(value)
		f.write("\n")
		for value in countNonEv:
			f.write(value)
		f.write("\n")
		for value in countEv:
			f.write(value)
		f.close()
		return (attExt, countNonEv, countEv, totalAtt)

	def monthLine(self, startDate, endDate):
		conn = sqlite3.connect(DBFile)
		cursor = conn.cursor()
		genDate = datetime.now().strftime("%Y-%m-%d")
		csv = os.path.join(MaildbRoot, "web", "static", "graph", "monthLine.csv")
		f = open(csv, "wb")
		f.write("Categories,")
		for date in range(1,31):
			f.write(str(date))
			f.write(",")
		task = cursor.execute("select strftime('%d', `date_added`) as d, count(date_added) as c from main where date_added BETWEEN ? AND ? and Comment like 'Tasking%' group by d", (startDate, endDate)).fetchall()
		nonTask = cursor.execute("select strftime('%d', `date_added`) as d, count(date_added) as c from main where date_added BETWEEN ? AND ? and Comment not like 'Tasking%' group by d", (startDate, endDate)).fetchall()
		count = {'01':'0', '02':'0','03':'0','04':'0','05':'0','06':'0','07':'0','08':'0','09':'0','10':'0','11':'0','12':'0','13':'0','14':'0','15':'0','16':'0','17':'0','18':'0','19':'0','21':'0','21':'0','22':'0','23':'0','24':'0','25':'0','26':'0','27':'0','28':'0','29':'0','30':'0','31':'0'};
		nCount = {'01':'0', '02':'0','03':'0','04':'0','05':'0','06':'0','07':'0','08':'0','09':'0','10':'0','11':'0','12':'0','13':'0','14':'0','15':'0','16':'0','17':'0','18':'0','19':'0','21':'0','21':'0','22':'0','23':'0','24':'0','25':'0','26':'0','27':'0','28':'0','29':'0','30':'0','31':'0'};
		for row in task:
			count[row[0]] = row[1];
		for row in nonTask:
			nCount[row[0]] = row[1];
		f.write("\nSignatures,")
		for value in sorted(count):
			f.write(str(count[value]))
			f.write(",")
		f.write("\nTasks,")
		for value in sorted(nCount):
			f.write(str(nCount[value]))
			f.write(",")
		f.close()
		return (count, nCount)
		

