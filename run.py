# Author = SkyDrive
# Initial date = 03-11-2016

# Import libraries.
import socket
import sys
from time import sleep
import functions
import update

# Bot information.
version = '1.0'
changes = "Initial version."
help = "!help, !repos"

# IRC Server information
server = "irc.lichtsnel.nl"
port = "6667"
botnick = "SkyBot"
nickserv = "aPPeLTaaRT"

# Define things here.
def sendmsg(chan , msg):
	irc.send("PRIVMSG "+ chan +" :"+ msg +"\n")

def joinchan(channel):
	irc.send("JOIN "+ channel +"\n")
	
# Update on start
if update.check(functions.getVersion()) == True:
	reload(functions)
	print "SkyBot has been updated to "+ functions.getVersion() +"\n"
else:
	print "SkyBot has not been updated\n"

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
	
	if ircmsg.find(":.update") != -1 and functions.isAdmin(ircmsg):
		if update.check(functions.getVersion()) == True:
			reload(functions)
			print "SkyBot has been updated to "+ functions.getVersion() +"\n"
		else:
			print "SkyBot has not been updated\n"
	
	send = functions.check(ircmsg)
	if isinstance(send, list):
		for x in send:
			irc.send(x)
	elif send != None:
		irc.send(send)
