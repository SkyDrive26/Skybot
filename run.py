# Author = SkyDrive
# Initial date = 03-11-2016

# Import libraries.
import socket
import sys
from time import sleep

# Bot information.
version = '1.0'
changes = "Initial version."
help = "!help, !repos"

# IRC Server information
server = "irc.rizon.net"
port = "6667"
botnick = "SkyRC"
nickserv = ""

# Define things here.
def sendmsg(chan , msg):
	irc.send("PRIVMSG "+ chan +" :"+ msg +"\n")

def joinchan(channel):
	irc.send("JOIN "+ channel +"\n")
	
def findNick():
	ni = ircmsg.split('!')
	nick = ni[0].strip(':')
	return nick

def findHost():
	host = ircmsg.split('@')[1].split()[0]
	return host

def isAdmin():
	if findNick() == admin[0] and findHost() == admin[1]:
		return True
	else:
		return False

# Variables
admin = ["SkyDrive", "I.am.in.the.fucking.Cloud"]

# Connect to the IRC server here.
irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
irc.connect((server, 6667))
irc.send("USER "+ botnick +" "+ botnick +" "+ botnick +" :Building cake since 2016\n")
irc.send("NICK "+ botnick +"\n")
sleep(1)
irc.send("NICKSERV IDENTIFY "+ nickserv +"\n")

# Here we join the channels.
sleep(1)
joinchan("#SkyDev")

while 1:
	ircmsg = irc.recv(2048)
	print(ircmsg)
	
	if ircmsg.find("PING") != -1:
		split = ircmsg.split()
		thing = split[1].strip(':')
		irc.send("PONG :"+ thing +"\r\n")
	
	if ircmsg.find(":!changes") != -1:
		findNick()
		irc.send("NOTICE "+ nick +" :Version "+ version +" , Changes: "+ changes +".\r\n")
	
	if ircmsg.lower().find(":!help") != -1:
		nick = findNick()
		host = findHost()
		if isAdmin():
			irc.send("NOTICE "+ nick +" :My current commands are: "+ help +", !java.\r\n")
		else:
			irc.send("NOTICE "+ nick +" :My current commands are: "+ help +".\r\n")
			
	if (ircmsg.lower().find(":!shutdown") != -1) and isAdmin():
		sys.exit()
			
	if ircmsg.lower().find(":!java") != -1:
		nick = findNick()
		if isAdmin():
			irc.send("NOTICE "+ nick +" :https://github.com/SkyDrive26/JAVA\r\n")
			
	if ircmsg.lower().find(":!repos") != -1:
		nick = findNick()
		irc.send("NOTICE "+ nick +" :https://github.com/SkyDrive26?tab=repositories\r\n")
		