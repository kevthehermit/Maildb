#!/usr/bin/env python
'''
Copyright (C) 2012-2013 Kevin Breen.
This file is part of the Maildb web application
See the 'LICENSE' File for copying permission.
'''

import core.postfile
import simplejson
import urllib
import urllib2
from config.config import vtapikey


def vtsubmit():
	host = "www.virustotal.com"
	selector = "https://www.virustotal.com/vtapi/v2/file/scan"
	fields = [("apikey", vtapikey)]
	file_to_send = open("test.txt", "rb").read()
	files = [("file", "test.txt", file_to_send)]
	json = postfile.post_multipart(host, selector, fields, files)
	print json

def vtreport(sha256):

	url = "https://www.virustotal.com/vtapi/v2/file/report"
	parameters = {"resource": '"' + sha256+ '"', "apikey": vtapikey}
	data = urllib.urlencode(parameters)
	req = urllib2.Request(url, data)
	response = urllib2.urlopen(req)
	json = response.read()
	print json


