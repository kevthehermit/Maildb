#!/usr/bin/env python
'''
Copyright (C) 2012-2013 Kevin Breen.
This file is part of the Maildb web application
See the 'LICENSE' File for copying permission.
'''

import os
import sys


from config.config import MaildbRoot, DBFile
from core.common import Dictionary

## Setup The Folder Structure ###
if not os.path.exists(os.path.join(MaildbRoot, "store")):
    os.mkdir(os.path.join(MaildbRoot, "store"))
    
if not os.path.exists(os.path.join(MaildbRoot, "tmp")):
    os.mkdir(os.path.join(MaildbRoot, "tmp"))

## Setup The Tables ###
from db.db import Maildatabase
Maildatabase().generate()


## Restart the APP ###

# Manual for now
