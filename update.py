# File: 	update.py
# Author: 	SkyDrive
# Init:		24-05-2018

import urllib2, base64

def check(curversion):
	response = urllib2.Request('https://skybot.daanvb.nl/update/versionb.txt')
	base64string = base64.b64encode('%s:%s' % ("username", "password"))
	response.add_header("Authorization", "Basic %s" % base64string)
	VERSION = int(urllib2.urlopen(response).read())
	curversion = int(curversion)
	
	print "Our version is: "+ str(curversion) +"\r"
	print "Update version is: "+ str(VERSION) +"\r"
	
	if(VERSION > curversion):
		return update()

def update():
	response = urllib2.Request("https://skybot.daanvb.nl/update/functions.py")
	base64string = base64.b64encode('%s:%s' % ("username", "password"))
	response.add_header("Authorization", "Basic %s" % base64string)
	data = urllib2.urlopen(response).read()
 
	# Write data to file
	filename = "functions.py"
	file_ = open(filename, 'w')
	file_.write(data)
	file_.close()
	return True
