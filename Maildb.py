#!/usr/bin/env python
'''
Copyright (C) 2012-2013 Kevin Breen.
This file is part of the Maildb web application
See the 'LICENSE' File for copying permission.
'''

import os
import sys
from beaker.middleware import SessionMiddleware
from cork import Cork
from config.config import DBFile, reportRoot, MaildbRoot, transferDir, webPort
from db.db import Maildatabase
from mako.template import Template
from mako.lookup import TemplateLookup
import bottle
import core.common
from bottle import route, run, static_file, redirect, request, HTTPError, error, get, app
import time
import tempfile
import shutil
import logging


def main():
	logging.basicConfig(filename='maildb.log', format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %I:%M:%S %p', level=logging.DEBUG)
	logging.info('Application Started')
	print "Welcome to the Maildb Version # 0.3.0"
	run(app=app, server='cherrypy', host="0.0.0.0", port=webPort, reloader=True)
	logging.info('Application Closed')


# Auth and Sessions

# Use users.json and roles.json in the local example_conf directory
auth = Cork('users', email_sender=None)

import datetime
app = app()
session_opts = {
    'session.type': 'cookie',
    'session.validate_key': True,
    'session.cookie_expires': True,
    'session.timeout': 3600, # 1 hour
    'session.encrypt_key': 'heres a random secret to use',
}
app = SessionMiddleware(app, session_opts)

def postd():
    return request.forms
    
def postf():
	return request.files

def post_get(name, default=''):
    return request.POST.get(name, default).strip()

# Debugging
from bottle import debug
debug(True)
# Debugging
lookup = TemplateLookup(directories=['web'], output_encoding='utf-8', encoding_errors='replace')
db = Maildatabase()
	


# Main Page
@route("/")
def index():
	auth.require(fail_redirect='/login')
	context = {}
	template = lookup.get_template("home.html")
	return template.render(**context)

	
### default view all the taskings
@route("/browse")	
def browse():
	auth.require(fail_redirect='/sorry_page')	
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

### Submit a new task
@route("/submit", method='POST')
def do_upload():
	auth.require(role='submit', fail_redirect='/sorry_page')
	tmpDir = tempfile.mkdtemp()
	taskType = request.forms.type
	data = request.files.data
	taskFile = request.forms.taskFile
	print taskType
	comment = request.forms.comment
	import core.submit

	if taskType == "email":
		print "Here i am"
		upload = core.common.fileUpload(data, tmpDir)
		fileName, fileExt = os.path.splitext(upload)
		if fileExt == ".pcap":
			core.submit.submitpcap(tmpDir, upload, comment.lower())
		elif fileExt == ".txt":
			print "txt"
			core.submit.submit(tmpDir, comment.lower())
	if taskType == "http":		
		upload = core.common.fileUpload(data, tmpDir)
		fileName, fileExt = os.path.splitext(upload)
		if fileExt == ".pcap":
			core.submit.submithttp(tmpDir, upload, comment.lower())
		else:
			return " You Must submit a pcap for web traffic"
	if taskType == "task":
		upload = core.common.fileUpload(data, tmpDir)
		core.submit.submitTask(upload, comment.lower())	
	redirect("/browse")


### The Tools Page
	
@route("/decode")
def help():
	auth.require(fail_redirect='/sorry_page')
	context = {}
	template = lookup.get_template("decode.html")
	return template.render(**context)


### The Main Report Pages
	
@route("/sig/<msg_id>")
def sig(msg_id):
	auth.require(fail_redirect='/sorry_page')
	info = db.msgInfo(msg_id)
	if info == None:
		return "ID %s not found in database" % msg_id
	comments = db.viewComment(msg_id)
	caseFiles = core.common.listCaseFiles(msg_id)
	if info.type == "mail":
		headers, attatch, links, hops, yara = db.sigPage(msg_id)			
		text = os.path.join(MaildbRoot, "store", msg_id, "attatchments", "body.txt")
		html = os.path.join(MaildbRoot, "store", msg_id, "attatchments", "htmlbody.txt")
		import codecs
		if os.path.isfile(text):
			textBody = codecs.open(text, encoding='utf-8', errors='ignore')
		else:
			textBody = None
		if os.path.isfile(html):
			htmlBody = codecs.open(html, encoding='utf-8', errors='ignore')
		else:
			htmlBody = None
		template = lookup.get_template("sig.html")	
		return template.render(msg_id=msg_id, attatch=attatch, info=info, headers=headers, text=text, textBody=textBody, htmlBody=htmlBody, yara=yara, comments=comments, hops=hops, links=links, caseFiles=caseFiles)
	if info.type == "web":
		flows = db.httpFlows(msg_id)
		sessions = db.httpSessions(msg_id)
		yara = db.yaraScan(msg_id)
		template = lookup.get_template("http.html")
		return template.render(msg_id=msg_id, flows=flows, info=info, sessions=sessions, comments=comments, yara=yara, caseFiles=caseFiles)
	if info.type == "Task":
		template = lookup.get_template("task.html")
		return template.render(msg_id=msg_id, info=info, comments=comments, caseFiles=caseFiles)
   
@route("/file")
def filePage():
	auth.require(fail_redirect='/sorry_page')
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

### Review And Comments from Here
		
@route("/review")

def review():
	auth.require(role='submit', fail_redirect='/sorry_page')
	flag = request.query.flag
	msg_id = request.query.ID
	template = lookup.get_template("review.html")
	return template.render(flag=flag, msg_id=msg_id)
	
@route("/review", method="POST")
def postReview():
	auth.require(role='submit', fail_redirect='/sorry_page')
	reviewflag = request.forms.flag
	msg_id = request.forms.msg_id
	commTitle = request.forms.title
	commText = request.forms.freetext	
	if reviewflag:
		db.review(reviewflag, msg_id)
	db.enterComments(msg_id, commTitle, commText)
	logging.info('Record %s Reviewed by %s', msg_id, auth.current_user.username)
	return '''<script type="text/javascript">window.close(); window.opener.location.reload(true);</script>'''

@route("/edit")
def taskEdit():
	auth.require(role='submit', fail_redirect='/sorry_page')
	if request.query.section == "comment":
		commID = request.query.commID
		template = lookup.get_template("commEdit.html")
		return template.render(commID=commID)
	
@route("/edit", method="POST")
def postReview():
	auth.require(role='submit', fail_redirect='/sorry_page')
	commID = request.forms.commID
	commTitle = request.forms.title
	commText = request.forms.freetext	
	db.updateComment(commID, commTitle, commText)
	return '''<script type="text/javascript">window.close(); window.opener.location.reload(true);</script>'''
					
#Stats and Reports

@route("/report", method='POST')
def create_report():
	auth.require(fail_redirect='/sorry_page')
	startDate = request.forms.startDate
	endDate = request.forms.endDate
	from core.newReport import Reporting
	display = []	
	w = Reporting().monthLine(startDate, endDate)
	x = Reporting().mainRep(startDate, endDate)
	y = Reporting().attatchRep(startDate, endDate)
	template = lookup.get_template("report.html")
	return template.render(w=w, x=x, y=y)
	
@route("/stats")
def stats():
	auth.require(fail_redirect='/sorry_page')
	context	= {}
	stats = db.stats()
	template = lookup.get_template("stats.html")
	return template.render(stats=stats, **context)

# Search Page
@route("/search")
def search():
	auth.require(fail_redirect='/sorry_page')
	context = {}
	template = lookup.get_template("search.html")
	return template.render(**context)

@route("/results")
def do_search():
	auth.require(fail_redirect='/sorry_page')
	from core.search import MailSearch
	context = {}
	search = str(request.query.Term)
	table = str(request.query.optone)
	column = str(request.query.opttwo)
	if table == 'main':
		rows = db.searchMain(column, search)
	else:
		rows = db.searchTables(table, column, search)

	template = lookup.get_template("results2.html")
	return template.render(rows=rows, **context)

# Creates your Export.zip file
	           
@route("/export")
def export():
	
	context = {}
	if request.query_string:
		msg_id = request.query.msg_id
		if request.query.type == "file":
			if request.query.fileID.endswith('pcap') or request.query.fileID.endswith('txt') or request.query.fileID.endswith('doc') or request.query.fileID.endswith('xls') or request.query.fileID.endswith('pdf'):
				auth.require(role='submit', fail_redirect='/sorry_page')
			else:
				auth.require(role='malware', fail_redirect='/sorry_page')
			core.common.exportFile(msg_id, request.query.fileID)			
		if request.query.type == "web":
			auth.require(role='malware', fail_redirect='/sorry_page')
			webID = request.query.webID
			core.common.exportDir(msg_id, webID)
		if request.query.type == "all":
			auth.require(role='malware', fail_redirect='/sorry_page')
			webID = request.query.webID
			core.common.exportDir(msg_id, webID)
	logging.info('Export For %s Created by %s', msg_id, auth.current_user.username)
	return static_file('Export.zip', root=os.path.join(MaildbRoot, "web", "static", "downloads"), download='Export.zip')

	
@route("/upload", method="POST")
def fileUpload():
	auth.require(role='submit', fail_redirect='/sorry_page')
	msg_id = request.forms.msg_id
	data = request.files.data
	uploadDir = os.path.join(MaildbRoot, "store", msg_id, "Case_Files")
	upload = core.common.fileUpload(data, uploadDir)
	logging.info('%s Added to Record %s by %s', data.filename, msg_id, auth.current_user.username)
				
#static files

@get('/static/:path#.+#')
def server_static(path):
	return static_file(path, root=os.path.join(MaildbRoot, "web", "static"))

@error(404)
def error404(error):
	return "These are not the pages your looking for"

@error(500)
def error404(error):
	logging.error('Error 500 Produced')
	template = lookup.get_template("result.html")
	page = '''<h1>Dont Panic! </h1><p>Report the Error<p><a href="#" onclick="history.back();">Then Click Here to Go back</a></p>'''
	return template.render(page=page)
 	
@get('/favicon.ico')# Just because the 404 was annoying me
def get_favicon():
    return server_static('favicon.ico')

# Auth Failure
@route('/sorry_page')
def sorry_page():
	template = lookup.get_template("fail.html")
	return template.render()

#Admin Pages Here
	
@route("/admin")
def admin():
	auth.require(role='submit', fail_redirect='/sorry_page')
	context	= {}
	username = auth.current_user.username
	if request.query.function == "install" and auth.current_user.role == "admin":
		import core.install
	if request.query.function == "backup":
		from core.admin_function import adFunction
		adFunction().archive()	
	if request.query.function == "reset" and auth.current_user.role == "admin":
		from core.admin_function import adFunction
		adFunction().reset()
	if request.query.function == "Delete":
		start = int(request.query.start)
		if request.query.end == "":
			from core.admin_function import recordTools
			recordTools().removeRecord(start)
			logging.info('Record %s Deleted by %s', start, username)
			return "Record %s was succesfully removed" % (start)
		else:
			end = int(request.query.end) + 1
			from core.admin_function import recordTools
			for delete in range(start, end):
				recordTools().removeRecord(delete)
				logging.info('Record %s Deleted by %s', delete, username)
			return "Record %s to %s was succesfully removed" % (start, end)
	if os.path.exists(os.path.join(MaildbRoot, "maildb.log")):
		logFile = open(os.path.join(MaildbRoot, "maildb.log"))			
	else:
		logFile = "*" # Lazy fix for an empty Log File
	template = lookup.get_template("admin.html")
	return template.render(logFile=logFile, **context)

# Account Controls

@route('/useradmin')

def admin():
    """Only admin users can see this"""
    auth.require(role='admin', fail_redirect='/sorry_page')
    template = lookup.get_template("admin/useradmin.html")
    current_user = auth.current_user
    users = auth.list_users()
    roles = auth.list_roles()
    return template.render(current_user=current_user, users=users, roles=roles)

@route('/create_user', method="POST")
def create_user():
    try:
        auth.create_user(postd().username, postd().role, postd().password)
        logging.info('User %s Created', postd().username)
        return dict(ok=True, msg='User Created')
        
    except Exception, e:
        return dict(ok=False, msg=e.message)

@route('/delete_user', method="POST")
def delete_user():
    try:
        auth.delete_user(post_get('username'))
        logging.info('User %s Deleted', post_get('username'))
        return dict(ok=True, msg='User Deleted')

    except Exception, e:
        print repr(e)
        return dict(ok=False, msg=e.message)

@route('/passwd', method="POST")
def passReset():
	passwd = post_get('password')
	auth.current_user.update(pwd=passwd)
	auth.logout(success_redirect='/login')
@route('/passwd')
def resetForm():
	template = lookup.get_template("reset.html")
	return template.render()

# Login Page
@route('/login', method="POST")
def login():
    """Authenticate users"""
    username = post_get('username')
    password = post_get('password')
    auth.login(username, password, success_redirect='/', fail_redirect='/login')
@route('/login')
def login_form():
	template = lookup.get_template("login.html")
	"""Serve login form"""
	return template.render()
	
# Logout 	
	
@route('/logout')
def logout():
	
    auth.logout(success_redirect='/login')

@route("/imap", method="POST")
def imapFetch():
	auth.require(role='admin', fail_redirect='/sorry_page')
	context = {}
	usr = request.forms.user
	pwd = request.forms.password
	server = request.forms.server
	inbox = request.forms.inbox
	protocol = request.forms.protocol
	from core.webMail import imapMail
	mailFetch = imapMail()
	if protocol == 'imap':
		mailFetch.getIMAP(usr, pwd, server, inbox)
	elif protocol == 'pop':
		mailFetch.getPOP(usr, pwd, server)
	redirect("/browse")



		
if __name__ == "__main__":
	main()

	
		
	

	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
