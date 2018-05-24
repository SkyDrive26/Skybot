# File: 	functions.py
# Author: 	SkyDrive
# Init:		24-05-2018

""" Import stuff here """
import sys
import urllib2
import time
import urllib2
from time import sleep
from datetime import datetime
from bs4 import BeautifulSoup

""" Module vars """
__version__ = "401"
admin = ["SkyDrive", "I.am.in.the.fucking.cloud"]

""" Get Version """	
def getVersion():
	return __version__

""" Init method """
def check(ircmsg):
	if ircmsg.find("PING") != -1:
		split = ircmsg.split()
		thing = split[1].strip(':')
		return "PONG :"+ thing +"\r\n"

	if ircmsg.find(".shutdown") != -1 and isAdmin(ircmsg):
		shutdown()

	if ircmsg.find(".version") != -1:
		return version(ircmsg)

	return None

""" Ident methods """
def findNick(ircmsg):
	ni = ircmsg.split('!')
	nick = ni[0].strip(':')
	return nick

def findHost(ircmsg):
	host = ircmsg.split('@')[1].split()[0]
	return host

def isAdmin(ircmsg):
	if findNick(ircmsg) == admin[0] and findHost(ircmsg) == admin[1]:
		return True
	else:
		return False

""" Methods """
def version(ircmsg):
	return "NOTICE "+ findNick(ircmsg) +" :Version of SkyBot: "+ __version__ +"\r\n"

def shutdown():
	sys.exit()