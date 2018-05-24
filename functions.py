# File: 	functions.py
# Author: 	SkyDrive
# Init:		24-05-2018

""" Import stuff here """
import socket
import sys
import urllib2
import time
import urllib2
from time import sleep
from datetime import datetime
from bs4 import BeautifulSoup

""" Module vars """
__version__ = "421"
admin = ["SkyDrive", "I.am.in.the.fucking.cloud"]
changes = "SkyBot is now completely rewritten to support new programming standards. Enjoy!"
hcmd = ["05.changes	02 See what changed since the last version.","05.nodes	02 See how many nodes are online.","05.nodes -l	02 See which nodes are online.","05.check [ip]:[port]	02 Check if the specified node is online, also shows node uptime."]
lnodes = []
tnodes = {}
frun = True

""" Get Version """	
def getVersion():
	return __version__

""" Init method """
def check(ircmsg):
	if ircmsg.find("PING") != -1:
		rdata = []
		split = ircmsg.split()
		thing = split[1].strip(':')
		rdata.append("PONG :"+ thing +"\r\n")
		try:
			for x in checknodes():
				rdata.append(x)
			return rdata
		except TypeError:
			return rdata
	
	ircmsg = ircmsg.lower()
	
	if ircmsg.find(".shutdown") != -1 and isAdmin(ircmsg):
		shutdown()

	if ircmsg.find(":.version") != -1:
		return version(ircmsg)
		
	if ircmsg.find(":.help") != -1:
		return help(ircmsg, hcmd)
		
	if ircmsg.find(":.changes") != -1:
		return change(ircmsg)
		
	if ircmsg.find(":.nodes") != -1:
		try:
			if ircmsg.split(".nodes ")[1].split()[0] == "-l" :
				return nodes(ircmsg, l=True)
			else:
				return nodes(ircmsg)
		except:
			return nodes(ircmsg)
	
	if ircmsg.find(":.check") != -1:
		try:
			check = ircmsg.split(".check ")[1].split()[0]
			try:
				ipcheck = socket.gethostbyname(check.split(":")[0])
				check = str(ipcheck) +":"+ check.split(":")[1]
				return checknode(ircmsg, check)
			except socket.gaierror:
				return "NOTICE "+ findNick(ircmsg) +" :Can not resolve "+ check +". Check domain DNS.\r\n"
		except IndexError:
			return "NOTICE "+ findNick(ircmsg) +" :No [ip]:[port] specified.\r\n"
	
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
	
def help(ircmsg, hcmd):
	rdata = ["NOTICE "+ findNick(ircmsg) +" :My commands are:\r\n"]
	for x in hcmd:
		rdata.append("NOTICE "+ findNick(ircmsg) +" :"+ x +"\r\n")
	return rdata
	
def change(ircmsg):
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
	
def checknode(ircmsg, check):
	rdata = []
	global lnodes
	if check in lnodes:
		ti = datetime.now().replace(microsecond=0)
		dti = str(ti - tnodes[check]).split(':')
		rti = dti[0] +"h "+ dti[1] +"m "+ dti[2] +"s"
		
		rdata.append("NOTICE "+ findNick(ircmsg) +" : 03* "+ check +" is initialised and active! *\r\n")
		rdata.append("NOTICE "+ findNick(ircmsg) +" : 03* Node uptime: "+ rti +" *\r\n")
		return rdata
	else:
		rdata.append("NOTICE "+ findNick(ircmsg) +" : 04* "+ check +" appears to be offline! *\r\n")
		return rdata

def checknodes():
	channel = "#Crypto"
	get = BeautifulSoup(urllib2.urlopen("https://factorialcoin.nl:5151/?nodelist"), "html.parser").get_text()
	data = get.split(" ")
	rdata = []
	global lnodes, frun
	if frun != True:
		if len(data) > len(lnodes):
			replace = False
			for x in data:
				if x not in lnodes:
					rdata.append("PRIVMSG "+ channel +" : 03* "+ x +" is a newly connected node!\r\n")
					tnodes[x] = datetime.now().replace(microsecond=0)
					replace = True
			if replace:
				lnodes = data
		else:
			replace = False
			for x in lnodes:
				if x not in data:
					rdata.append("PRIVMSG "+ channel +" : 04* "+ x +" appears to be offline!\r\n")
					tnodes[x] = None
					replace = True
		
			if replace:
				lnodes = data
	else:
		lnodes = data
		for x in data:
			tnodes[x] = datetime.now().replace(microsecond=0)
		frun = False
		return None
	return rdata