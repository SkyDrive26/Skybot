# File: 	nodes.py
# Author: 	SkyDrive
# Init:		24-05-2018

""" Module vars """
nodelist = []
nodetime = {}

""" Module Methods """
def getNodelist():
	return nodelist
def setNodelist(data):
	nodelist = data

def getNodetime(index):
	return nodetime[index]
def setNodetime(index, data):
	nodetime[index] = data