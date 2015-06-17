#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author : Jash Lee
# June 16, 2015

"""
Requirements:
 - Python 2.6 +
 - boto v2.38.0

# Not anymore, this is a simple S3 upload script
# Usage : python uploadGitHubBackupToS3.py
"""

import boto
import boto.s3
from boto.s3.key import Key
import os.path
import os
import time
import datetime
import shutil

# S3 Credentials
AWS_ACCESS_KEY = 'XXXXXXX'
AWS_ACCESS_KEY_SECRET = 'XXXXXX'
# Bucket name
BUCKET_NAME = 'XXXXXX'
# Source directory
SOURCEDIR = 'XXXXXX'
# destination directory name (on s3)
DESTDIR = 'XXXXXXX'
TODAY = datetime.datetime.today().date() # 2015-06-16

s3Bucket = boto.connect_s3(AWS_ACCESS_KEY,AWS_ACCESS_KEY_SECRET)
s3Uploader = s3Bucket.get_bucket(BUCKET_NAME)
s3Key = Key(s3Uploader)

# Remove Yesterday's backup
for root, dirs, files in os.walk(SOURCEDIR, followlinks=False):
    for file in files:
        if root.strip(SOURCEDIR).count(os.sep) <= 1:
            try:
                findOldFolders = root
                ctime = time.ctime(os.path.getctime(findOldFolders))
                parsed = datetime.datetime.strptime(ctime, "%a %b %d %H:%M:%S %Y").date() # Tue Jun 16 14:57:32 2015
                if (str(parsed) != str(TODAY)):
                    print "Removed %s created: %s" % (findOldFolders, str(parsed))
                    shutil.rmtree(findOldFolders) # Remove folders recursively
            except:
                pass

# Upload today's backup to S3
for root, dirs, files in os.walk(SOURCEDIR, followlinks=False):
    for file in files:
        try:
            root = root.strip(SOURCEDIR)
            realFiles = os.path.join(SOURCEDIR, root,file)
            keyName = os.path.join(DESTDIR,root,file)
            if not s3Uploader.get_key(keyName):
                s3Key.key = keyName
                print 'Key...', keyName
                s3Key.set_contents_from_filename(realFiles)
                print 'Uploading...', realFiles
                #os.remove(relpath)
        except:
            pass
