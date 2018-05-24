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
__version__ = "403"
admin = ["SkyDrive", "I.am.in.the.fucking.cloud"]
changes = "SkyBot is now completely rewritten to support new programming standards. Enjoy!"
help = ".changes, .help, .nodes (use arg -l to see the nodelist)"#, .check [ip]:[port]"

""" Get Version """	
def getVersion():
	return __version__

""" Init method """
def check(ircmsg):
	if ircmsg.find("PING") != -1:
		split = ircmsg.split()
		thing = split[1].strip(':')
		return "PONG :"+ thing +"\r\n"
	
	ircmsg = ircmsg.lower()
	
	if ircmsg.find(".shutdown") != -1 and isAdmin(ircmsg):
		shutdown()

	if ircmsg.find(":.version") != -1:
		return version(ircmsg)
		
	if ircmsg.find(":.help") != -1:
		return help(ircmsg)
		
	if ircmsg.find(":.changes") != -1:
		return changes()
		
	if ircmsg.find(":.nodes") != -1:
		try:
			if ircmsg.split(".nodes ")[1].split()[0] == "-l" :
				return nodes(ircmsg, l=True)
			else:
				return nodes(ircmsg)
		except:
			return nodes(ircmsg)
	
	#if ircmsg.find("") != -1:
	
	#if ircmsg.find("") != -1:
	
	return None

""" Ident methods """
def findNick(ircmsg):
	ni = ircmsg.split('!')
	nick = ni[0].strip(':')
	return nick

def findHost(ircmsg):
	host = ircmsg.split('@')[1].split()[0]
	return host

def findChan(ircmsg):
	return ircmsg.split()[2]

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
	
def help(ircmsg):
	return "NOTICE "+ findNick(ircmsg) +" :My commands are "+ help +".\r\n"
	
def changes(ircmsg):
	return "NOTICE "+ findNick(ircmsg) +" :Version "+ __version__ +", changes: "+ changes +".\r\n"
	
def nodes(ircmsg, l=False):
	get = BeautifulSoup(urllib2.urlopen("https://factorialcoin.nl:5151/?nodelist"), "html.parser").get_text()
	data = get.split(" ")
	
	if l == True:
		rdata = []
		pdata = [[]]
		rdata.append("PRIVMSG "+ findChan(ircmsg) +" : 07* There are "+ str(len(data)) +" nodes initialised and active\r\n")
		i = 0
		l = 2
		
		if(len(data) > 4 and len(data) <= 9):
			l = 3
		elif(len(data) > 9 and len(data) <= 16):
			l = 4
		elif(len(data) > 16 and len(data) <= 25):
			l = 5
		elif(len(data) > 25 and len(data) <= 36):
			l = 6
		elif(len(data) > 36 and len(data) <= 49):
			l = 7
		elif(len(data) > 49 and len(data) <= 64):
			l = 8
		
		for x in sorted(data):
			if(len(pdata[i]) < l):
				pdata[i].append(x)
			else:
				pdata.append([x])
				i += 1
		
		for list in pdata:
			st = ""
			for x in list:
				st = st + "* " + str(x)
				i = len(str(x))
				while(i <= 20):
					st = st + " "
					i += 1
			rdata.append("NOTICE "+ findNick(ircmsg) +" : 03"+ st +"\r\n")
		return rdata
	else:
		return "PRIVMSG "+ findChan(ircmsg) +" : 07* There are "+ str(len(data)) +" nodes initialised and active\r\n"