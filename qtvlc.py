#coding:utf-8
#! /usr/bin/python

#
# Qt example for VLC Python bindings
# Copyright (C) 2009-2010 the VideoLAN team
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston MA 02110-1301, USA.
#

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
        #
        # self.vboxlayout.addWidget(self.label_file)
        #
        self.vboxlayout.addWidget(self.videoframe)
        # self.vboxlayout.addWidget(self.positionslider)
        # self.vboxlayout.addLayout(self.hbuttonbox)
        #
        self.vboxlayout.setStretchFactor(self.videoframe,1)
        self.vboxlayout.setSpacing(0)
        self.vboxlayout.setContentsMargins(0,0,0,0)
		#
        self.widget.setLayout(self.vboxlayout)
		#
        # open = QtGui.QAction("&Open", self)
        # self.connect(open, QtCore.SIGNAL("triggered()"), self.OpenFile)
        # exit = QtGui.QAction("&Exit", self)
        # self.connect(exit, QtCore.SIGNAL("triggered()"), sys.exit)
        # menubar = self.menuBar()
        # filemenu = menubar.addMenu("&File")
        # filemenu.addAction(open)
        # filemenu.addSeparator()
        # filemenu.addAction(exit)

        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(200)
        self.connect(self.timer, QtCore.SIGNAL("timeout()"),
                     self.updateUI)
        
       
		
    def reload_films(self):
        print 'start..'
        file = open('playlist.txt')
        data = file.readlines()
        dirs=[]
        for line in data:
            line = line.strip()
            if not line:
                continue 
            dirs.append(line.decode('utf-8')) 
        self.playfiles = self.load_files(dirs)
        
        
    def load_files(self,dirs):
        #dirs=[u'邵氏760',u'sb_300',u'sb_400',u'sb_500',u'sb_600',u'sb_700' ]
        allfiles=[]
        for _ in dirs:
            files  = os.listdir(_)
            for f in files:
                allfiles.append(f)
        allfiles = sorted(allfiles)
        for f in allfiles:
            print f.encode('gbk')
        return allfiles
        
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
        # print 'play setPosition:',position
        # setting the position to where the slider was dragged
        self.mediaplayer.set_position(position / 1000.0)
        # the vlc MediaPlayer needs a float value between 0 and 1, Qt
        # uses integer variables, so you need a factor; the higher the
        # factor, the more precise are the results
        # (1000 should be enough)

    def human_time(self,value):
        s = value%60
        h = value/3600
        m = (value-h*3600)/60
        
        return '%02d:%02d:%02d'%(h,m,s)
    
    def play_percent(self,current,length):
        return "%02d"%(current/length*100+1)


    def updateUI(self):
        """updates the user interface"""
        # setting the slider to the desired position
        # print 'updateUI..'
        progress = self.mediaplayer.get_position() * 1000
        # self.positionslider.setValue(self.mediaplayer.get_position() * 1000)
        #
        c,a = self.mediaplayer.get_time()/1000,self.mediaplayer.get_length()/1000
        # current = self.human_time( c)
        # all = self.human_time( a )
        # playtime = current+'/'+all +'('+self.play_percent(c,a)+'%)'
        # self.label_file.setText(playtime + ' ' + os.path.basename(self.filename) )
        self.ctrl.onPlayProgress(a,c,progress)

        if not self.mediaplayer.is_playing():
            # no need to call this function if nothing is played
            self.timer.stop()
            if not self.isPaused:
                # after the video finished, the play button stills shows
                # "Pause", not the desired behavior of a media player
                # this will fix it
                self.Stop()

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    player = Player()
    player.show()
    player.resize(901, 619)
    if sys.argv[1:]:
        player.OpenFile(sys.argv[1])
    sys.exit(app.exec_())
