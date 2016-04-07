#coding:utf-8
#! /usr/bin/python


import sys
import os.path,os
import vlc
from PyQt4 import QtGui, QtCore

class Player(QtGui.QMainWindow):
	"""A simple Media Player using VLC and Qt
	"""
	def __init__(self, master=None,ctrl=None):
		QtGui.QMainWindow.__init__(self, master)
		self.setWindowTitle("Media Player")

		# creating a basic vlc instance
		self.instance = vlc.Instance()
		# creating an empty vlc media player
		self.mediaplayer = self.instance.media_player_new()

		self.createUI()
		self.isPaused = False

		self.ctrl = ctrl

	def createUI(self):
		"""Set up the user interface, signals & slots
		"""
		self.widget = QtGui.QWidget(self)
		self.setCentralWidget(self.widget)

		# In this widget, the video will be drawn
		if sys.platform == "darwin": # for MacOS
			self.videoframe = QtGui.QMacCocoaViewContainer(0)
		else:
			self.videoframe = QtGui.QFrame()
		self.palette = self.videoframe.palette()
		self.palette.setColor (QtGui.QPalette.Window,
							   QtGui.QColor(0,0,0))
		self.videoframe.setPalette(self.palette)
		self.videoframe.setAutoFillBackground(True)

		self.playfilename = QtGui.QLabel(self.widget)
		self.playfilename.setGeometry(QtCore.QRect(30, 30, 200, 140))
		self.playfilename.setText(u'PandaTV')

		self.vboxlayout = QtGui.QVBoxLayout()
		self.vboxlayout.addWidget(self.videoframe)
		self.vboxlayout.setStretchFactor(self.videoframe,1)
		self.vboxlayout.setSpacing(0)
		self.vboxlayout.setContentsMargins(0,0,0,0)
		#
		self.widget.setLayout(self.vboxlayout)

		self.timer = QtCore.QTimer(self)
		self.timer.setInterval(200)
		self.connect(self.timer, QtCore.SIGNAL("timeout()"),
					 self.updateUI)


	def PlayPause(self):
		"""Toggle play/pause status
		"""
		if self.ctrl:
			self.ctrl.PlayPause()
			return

		if self.mediaplayer.is_playing():
			self.mediaplayer.pause()
			self.playbutton.setText("Play")
			self.isPaused = True
		else:
			if self.mediaplayer.play() == -1:
				self.OpenFile()
				return
			self.mediaplayer.play()
			self.playbutton.setText("Pause")
			self.timer.start()
			self.isPaused = False

	def Stop(self):
		"""Stop player
		"""
		if self.ctrl:
			self.ctrl.Stop()
			return
		self.mediaplayer.stop()
		self.playbutton.setText("Play")

	def OpenFile(self, filename=None):
		"""Open a media file in a MediaPlayer
		"""

		if filename is None:
			filename = QtGui.QFileDialog.getOpenFileName(self, "Open File", os.path.expanduser('~'))
		if not filename:
			return

		# create the media
		if sys.version < '3':
			filename = unicode(filename)

		self.filename = filename

		self.media = self.instance.media_new(filename)
		# put the media in the media player
		self.mediaplayer.set_media(self.media)

		# parse the metadata of the file
		self.media.parse()
		# set the title of the track as window title
		self.setWindowTitle(self.media.get_meta(0))

		# the media player has to be 'connected' to the QFrame
		# (otherwise a video would be displayed in it's own window)
		# this is platform specific!
		# you have to give the id of the QFrame (or similar object) to
		# vlc, different platforms have different functions for this
		if sys.platform.startswith('linux'): # for Linux using the X Server
			self.mediaplayer.set_xwindow(self.videoframe.winId())
		elif sys.platform == "win32": # for Windows
			self.mediaplayer.set_hwnd(self.videoframe.winId())
		elif sys.platform == "darwin": # for MacOS
			self.mediaplayer.set_nsobject(self.videoframe.winId())
		self.PlayPause()

	def setVolume(self, Volume):
		"""Set the volume
		"""
		self.mediaplayer.audio_set_volume(Volume)

	def setPosition(self, position):
		"""Set the position
		"""
		self.mediaplayer.set_position(position / 1000.0)

	def updateUI(self):
		"""updates the user interface"""
		# setting the slider to the desired position
		progress = self.mediaplayer.get_position() * 1000
		c,a = self.mediaplayer.get_time()/1000,self.mediaplayer.get_length()/1000
		self.ctrl.onPlayProgress(a,c,progress)
		if not self.mediaplayer.is_playing():
			self.timer.stop()
			if not self.isPaused:
				self.Stop()

if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	player = Player()
	player.show()
	player.resize(901, 619)
	if sys.argv[1:]:
		player.OpenFile(sys.argv[1])
	sys.exit(app.exec_())
