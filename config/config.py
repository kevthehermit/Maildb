#!/usr/bin/env python
'''
Copyright (C) 2012-2013 Kevin Breen.
This file is part of the Maildb web application
See the 'LICENSE' File for copying permission.
'''

import os

##### Version #####

version = '0.4.5'
development = True

##### Settings ######

webPort = '7171'
logEnable='1' # Log Errors

##### Locations ######
MaildbRoot = os.path.normpath(os.path.join(os.path.abspath(os.path.dirname(__file__)), "..",))
transferDir = os.path.join(MaildbRoot, "tmp")		# Location of temporary Pcap files
reportRoot = os.path.join(MaildbRoot, "store")		# Save Location for reports
DBFile = os.path.join(MaildbRoot, "db", "database.db")	# Database File
ProxyPort = '80'
SSLPort = '443'
##### Enable SSDEEP #######

ssdeepcheck='1'

##### Clam AV ######

clamscan='0'
dblocation = os.path.join(MaildbRoot, "clam", "clam.db")

##### Yara #####

enableYara = '1'
yaraRuleFile = os.path.join(MaildbRoot, "yara", "index.yar")

##### Virus Total#####
# Not Implemented Yet

vtsubmit='0'
vtapikey=''


## Cuckoo
enableCuckoo = '1'
cuckooUrl = "192.168.0.21"
cuckooPort = "8090"
cuckooMachine = "SandBox_Win7"








