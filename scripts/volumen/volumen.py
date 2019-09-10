#!/usr/bin/python2
# -*- coding: utf-8 -*-

import os
import sys
import time
import argparse
import subprocess
import re
import gi
gi.require_version('Notify', '0.7')
from gi.repository import Notify
import os.path

# Console text formatting characters
class Colouring:
	C_RESET = '\033[0m'
	C_BOLD = '\033[1m'
	C_DIM = '\033[2m'
	C_ITALIC = '\033[3m'
	C_UNDERLINE = '\033[4m'

	C_BLACK = 0
	C_RED = 1
	C_GREEN = 2
	C_YELLOW = 3
	C_BLUE = 4
	C_MAGENTA = 5
	C_CYAN = 6
	C_WHITE = 7

	def textColor(colorNumber):
		return '\033[%dm' % (30 + colorNumber)

	def backgroundColor(colorNumber):
		return '\033[%dm' % (40 + colorNumber)

	C_INFO = textColor(C_BLUE) + C_BOLD
	C_WARN = textColor(C_YELLOW) + C_BOLD
	C_ERROR = textColor(C_RED) + C_BOLD

T_INFO = Colouring.C_INFO + '[info]' + Colouring.C_RESET
T_WARN = Colouring.C_WARN + '[warn]' + Colouring.C_RESET
T_ERROR = Colouring.C_ERROR + '[ERROR]' + Colouring.C_RESET

def info(message):
	print(T_INFO + " " + message)

def warn(message):
	print(T_WARN + " " + message)

def error(message):
	print(T_ERROR + " " + message)

def fatal(message):
	error(message)
	sys.exit()


def shellExec(cmd):
	errCode = subprocess.call(cmd, shell=True)
	if errCode != 0:
		fatal('failed executing: %s' % cmd)

def shellExecErrorCode(cmd):
	return subprocess.call(cmd, shell=True)

def shellGetOutput(cmd):
	return subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)


def popArg(args):
	if len(args) == 0:
		return (None, args)
	nextArg = args[0]
	args = args[1:]
	return (nextArg, args)

def nextArg(args):
	if len(args) == 0:
		return None
	return args[0]



def updateVolume(volumeDirection, volumeStep):
	if (volumeDirection == 1):
		shellExec('amixer -q sset Master %d%%+' % volumeStep)
	elif (volumeDirection == -1):
		shellExec('amixer -q sset Master %d%%-' % volumeStep)

def showCurrentVolume():
	masterVolume = readMasterVolume()
	iconName = getNotificationIcon(masterVolume)
	summary = 'Volume'
	body = '%d%%' % masterVolume
	showNotification(iconName, summary, body)

def readMasterVolume():
	masterVolumeRegex = r'^(.*)Front (Right|Left): Playback (\d*) \[(\d+)%\] \[on\]$'
	for line in shellGetOutput('amixer get Master').split('\n'):
		match = re.match(masterVolumeRegex, line)
		if match:
			return int(match.group(4))
	warn('Master volume could not have been read')
	return None

def getNotificationIcon(volume):
	if volume is None:
		return 'audio-card'
	if volume == 0:
		return "notification-audio-volume-off"
	elif volume < 30:
		return "notification-audio-volume-low"
	elif volume < 60:
		return "notification-audio-volume-medium"
	else:
		return "notification-audio-volume-high"

def saveCurrentBody(currentFile, body):
	f = open(currentFile, 'w')
	f.write(body)
	f.close()

def currentMillis():
	return int(round(time.time() * 1000))

def showNotification(iconName, summary, body):

	CURRENT_VOLUME_FILE = '/tmp/volumen-current'
	
	if os.path.isfile(CURRENT_VOLUME_FILE):
		saveCurrentBody(CURRENT_VOLUME_FILE, body)
		# skip - another process is displaying notification
		return
	saveCurrentBody(CURRENT_VOLUME_FILE, body)

	Notify.init("volumen")
	notification = Notify.Notification.new(
		summary,
		body,
		iconName
	)
	notification.show()

	# monitor for changes
	start = currentMillis()
	while(currentMillis() < start + 1000):
		if os.path.isfile(CURRENT_VOLUME_FILE):
			f = open(CURRENT_VOLUME_FILE, 'r')
			newBody = f.read()
			if body != newBody: # body changed
				body = newBody
				notification.update(summary, body, iconName)
				notification.show()
				# reset timer
				start = currentMillis()
		time.sleep(0.05)

	notification.close()
	
	os.remove(CURRENT_VOLUME_FILE)

class Main:

	def __init__(self):
		self.volumeChange = 0  # change direction: +1 - up, -1 - down
		self.VOLUME_STEP = 1

	def start(self):
		self.parseArguments()
		updateVolume(self.volumeChange, self.VOLUME_STEP)
		showCurrentVolume()

	def parseArguments(self):
		args = sys.argv[1:]
		while args:
			args = self.parseArgument(*popArg(args))

	def parseArgument(self, arg, args):
		if arg == 'up':
			self.volumeChange = +1
		elif arg == 'down':
			self.volumeChange = -1
		else:
			fatal('invalid argument: %s' % arg)
		return args

Main().start()
