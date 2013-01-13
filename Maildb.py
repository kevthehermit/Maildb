#!/usr/bin/env python
'''
Copyright (C) 2012-2013 Kevin Breen.
This file is part of the Maildb web application
See the 'LICENSE' File for copying permission.
'''

import os
import sys
from config.config import DBFile, reportRoot, MaildbRoot, transferDir
from db.db import Maildatabase
from mako.template import Template
from mako.lookup import TemplateLookup
import bottle
from bottle import route, run, static_file, redirect, request, HTTPError, error, get

# Debugging
from bottle import debug
debug(True)
# Debugging

lookup = TemplateLookup(directories=['web'], output_encoding='utf-8', encoding_errors='replace')
db = Maildatabase()
	
#static files

@get('/static/:path#.+#')
def server_static(path):
	return static_file(path, root=os.path.join(MaildbRoot, "web", "static"))

# Main Page
@route("/")
def index():

	context = {}
	template = lookup.get_template("home.html")
	return template.render(**context)

# Search Page
@route("/search")
def search():
	context = {}
	template = lookup.get_template("search.html")
	return template.render(**context)
		
	
### default view all the taskings
@route("/browse")	
def browse():	
	context = {}
	if request.query_string:
		limit = request.query.limit
		offset = request.query.offset
	else:
		limit = 30
		offset = 0

	rows = db.tasks(limit, offset)
	template = lookup.get_template("browse.html")
	return template.render(rows=rows, offset=offset, limit=limit, **context)

	
#Admin Pages Here
	
@route("/admin")
def admin():
	context	= {}
	if request.query.function == "install":
		import core.install
	if request.query.function == "backup":
		from core.admin_function import adFunction
		adFunction().archive()	
	if request.query.function == "reset":
		from core.admin_function import adFunction
		adFunction().reset()
	if request.query.function == "delete":
		pass
	logFile = open(os.path.join(MaildbRoot, "log.txt"))
	template = lookup.get_template("admin.html")
	return template.render(logFile=logFile, **context)

@route("/admin", method="POST")
def adminPost():
	msg_id = request.forms.msg_id
	from core.admin_function import recordTools
	recordTools().removeRecord(msg_id)
	return "Task no %s was succesfully removed" % (msg_id)
	

### Stats Pages Here
	
@route("/stats")
def stats():
	context	= {}
	stats = db.stats()
	countall = stats[0]

	template = lookup.get_template("stats.html")
	return template.render(stats=stats, **context)
		
### Help Pages Here

@route("/help")
def help():
	context = {}
	template = lookup.get_template("help.html")
	return template.render(**context)

### The Tools Page
	
@route("/decode")
def help():
	context = {}
	template = lookup.get_template("decode.html")
	return template.render(**context)


### The Main Report Page
	
@route("/sig/<msg_id>")
def sig(msg_id):

	comments = db.viewComment(msg_id)	
	info = db.msgInfo(msg_id)
	print info.Comment
	if info.type == "mail":
		headers, attatch, links, hops, yara = db.sigPage(msg_id)
		#yara = db.yaraMail(msg_id)			
		text = os.path.join(MaildbRoot, "store", msg_id, "attatchments", "body.txt")
		html = os.path.join(MaildbRoot, "store", msg_id, "attatchments", "htmlbody.txt")
		import codecs
		if os.path.isfile(text):
			f = codecs.open(text, encoding='utf-8', errors='ignore')
		elif os.path.isfile(html):
			f = codecs.open(html, encoding='utf-8', errors='ignore')
		else:
			f = "Content Not Found"
		template = lookup.get_template("sig.html")	
		return template.render(msg_id=msg_id, attatch=attatch, info=info, headers=headers, text=text, f=f, yara=yara, comments=comments, hops=hops, links=links)
	if info.type == "web":
		flows = db.httpFlows(msg_id)
		sessions = db.httpSessions(msg_id)
		template = lookup.get_template("http.html")
		return template.render(msg_id=msg_id, flows=flows, info=info, sessions=sessions, comments=comments)
	if info.type == "Task":
		template = lookup.get_template("task.html")
		return template.render(msg_id=msg_id, info=info, comments=comments)
		
## this is the return for a search
 
@route("/results", method='POST')
def do_search():
	from core.search import MailSearch
	context = {}
	search = str(request.forms.Term)
	table = str(request.forms.optone)
	column = str(request.forms.opttwo)
	if table == 'main':
		rows = MailSearch().searchMain(column, search)
	else:
		rows = MailSearch().searchTables(table, column, search)

	template = lookup.get_template("results2.html")
	return template.render(rows=rows, **context)

### Review And Comments from Here
		
@route("/review")

def review():
	flag = request.query.flag
	msg_id = request.query.ID
	template = lookup.get_template("review.html")
	return template.render(flag=flag, msg_id=msg_id)
	
@route("/review", method="POST")
def postReview():
	reviewflag = request.forms.flag
	msg_id = request.forms.msg_id
	commTitle = request.forms.title
	commText = request.forms.freetext	
	if commTitle and commText:
		db.review(reviewflag, msg_id)
		db.enterComments(msg_id, commTitle, commText)
		'''Updated'''
	else:
		return '''You Missed a bit '''		
		
### Submit a new task
@route("/submit", method='POST')
def do_upload():
	from core.common import cleanup
	cleanup().cleartmp(transferDir)
	data = request.files.data
	taskFile = request.forms.taskFile
	comment = request.forms.comment
	if data and comment:
		raw = data.file.read()
		filename = data.filename
		f = open(os.path.join(transferDir, filename), "wb")
		f.write(raw)
		f.close()
		from core.submit import emlSubmit
		context = {}
		# Is pcap or Not
        fileName, fileExtension = os.path.splitext(filename)
        if filename.startswith('http'):
        	newPath = emlSubmit().submithttp(filename, comment)
        if filename.startswith('Tasking'):
        	newPath = emlSubmit().submitTask(filename, comment)
        else:	
        	pcapExt = ".pcap"
        	txtExt = ".txt"
        	if str(fileExtension) == txtExt:
				newPath = emlSubmit().submit(comment)
				redir = "/browse"
        	elif str(fileExtension) == pcapExt:
				print "pcap Being Processed"
				emlSubmit().submitpcap(filename, comment)
	redirect("/browse")
			
### this creates the reporting method

@route("/report", method='POST')
def create_report():
	repDate = request.forms.reportDate

	from core.newReport import Reporting
	x = Reporting().mainRep(repDate)
	template = lookup.get_template("report.html")
	return template.render(x=x)

### This will be for the file pages	
    
@route("/file")
def filePage():
	context = {}	
	msg_id = request.query.ID
	if request.query.md5:
		md5 = request.query.md5
		fileInfo = db.fileInfo(msg_id, md5)
		yara = db.yaraFile(md5, msg_id)
		template = lookup.get_template("file.html")
		return template.render(fileInfo=fileInfo, yara=yara, **context)
	if request.query.host:
		host = request.query.host
		hostInfo = db.hostInfo(msg_id, str(host))
		template = lookup.get_template("host.html")
		return template.render(hostInfo=hostInfo, **context)

### Creates your Export.zip file
	           
@route("/export")
def export():
	context = {}
	if request.query_string:
		msg_id = request.query.msg_id
		fileID = request.query.fileID
	from core.admin_function import recordTools
	recordTools().exportDir(msg_id, fileID)
	return static_file('Export.zip', root=os.path.join(MaildbRoot, "web", "static"), download='Export.zip')

### IMAP And POP Fetch

@route("/imap", method="POST")
def imapFetch():
	from core.common import cleanup
	cleanup().cleartmp()
	context = {}
	usr = request.forms.user
	pwd = request.forms.password
	server = request.forms.server
	inbox = request.forms.inbox
	protocol = request.forms.protocol
	from core.webMail import imapMail
	if protocol == 'imap':
		imapMail().getIMAP(usr, pwd, server, inbox)
	elif protocol == 'pop':
		imapMail().getPOP(usr, pwd, server)
	redirect("/browse")


### Sandbox

@route("/analyse")
def sandbox():
	msg_id = request.query.ID
	if request.query.sandbox == "MAS":
		profile = request.query.profile
		filename = request.query.filename
		from core.sandbox import sandboxSubmit
		sandboxSubmit().submitMAS(profile, filename, msg_id)
		return "File Submitted to MAS"
	if request.query.sandbox == "Cuckoo":
		pass
	

	
### Error Pages

@error(404)
def error404(error):
	return "These are not the pages your looking for"

@error(500)
def error404(error):
	return '''<h1>Oh my god you broke it! Quickly turn off the screen and walk away!</h1><p><a href="#" onclick="history.back();">Click Here to Go back</a></p>'''

# Just because the 404 was annoying me 	
@get('/favicon.ico')
def get_favicon():
    return server_static('favicon.ico')

# set the interface and the port to run the application	
if __name__ == "__main__":
	run(host="0.0.0.0", port=7070, reloader=True)
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
