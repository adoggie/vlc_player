#coding:utf-8

__author__ = 'zhangbin'


import sys
import os.path,os,time
import vlc
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import QtGui, QtCore
import play_ctrl
import qtvlc
import json


PATH = os.path.dirname(os.path.abspath(__file__))

class YamlConfigReader:
	def __init__(self,conf):
		self.props ={}
		self.conf = conf
		self.read_file(conf)

	def read_file(self,conf):
		import yaml
		f = open(conf)
		self.props = yaml.load(f.read())
		f.close()



class PlayCtrlWnd(QtGui.QFrame,play_ctrl.Ui_Form):
	def __init__(self):
		QtGui.QWidget.__init__(self)
		self.playwnd = qtvlc.Player(self,self)
		self.playwnd.show()


		self.setupUi(self)

		x,y = map(int,self.getConfig()['player']['play_win_size'].split(','))
		self.playwnd.resize(x,y)

		self.init_data()
		self.init_ui()
		self.load_default()

	def init_data(self):
		self.playlist =[]
		self.tvitems ={}
		self.current_ti = None

		self.last_elapsed_time = 0

	def getConfig(self):
		confile = PATH+'/play.yaml'
		conf = YamlConfigReader(confile).props
		return conf

	def init_ui(self):
		self.tvFiles.setHeaderLabels([
			u'序号',
			u'名称',
			u'',
		])
		self.tvFiles.resizeColumnToContents(0)
		self.tvFiles.setAlternatingRowColors(True)

		self.connect(self.addbutton,SIGNAL('clicked()'),self.onAddFile)
		self.connect(self.deletebutton,SIGNAL('clicked()'),self.onDeleteFile)
		self.connect(self.savebutton,SIGNAL('clicked()'),self.onSaveFileList)
		# self.connect(self.btnExport_1,SIGNAL('clicked()'),self.onBtnExport1Click)

		self.positionslider.setToolTip("Position")
		self.positionslider.setMaximum(1000)

		self.connect(self.positionslider,QtCore.SIGNAL("sliderMoved(int)"), self.playwnd.setPosition)
		# self.connect(self.positionslider,QtCore.SIGNAL("sliderPressed(int)"), self.onSliderPressed)
		# self.connect(self.positionslider,QtCore.SIGNAL("sliderPressed(int)"), self.setPosition)
		self.connect(self.playbutton, QtCore.SIGNAL("clicked()"),self.PlayPause)

		self.connect(self.stopbutton, QtCore.SIGNAL("clicked()"),self.Stop)
		self.volumeslider.setMaximum(100)
		self.volumeslider.setValue(self.playwnd.mediaplayer.audio_get_volume())
		self.volumeslider.setToolTip("Volume")
		self.connect(self.volumeslider,QtCore.SIGNAL("valueChanged(int)"),self.playwnd.setVolume)

		self.connect(self.tvFiles,SIGNAL('itemDoubleClicked(QTreeWidgetItem*,int)'),self.onTreeItemDoubleClick)


	def onDeleteFile(self):
		items = self.tvFiles.selectedItems()
		for ti in items:
			del self.tvitems[ti]
			idx = self.tvFiles.indexOfTopLevelItem(ti)
			self.tvFiles.takeTopLevelItem(idx)
			if self.current_ti == ti:
				self.current_ti = None

	def onSaveFileList(self):
		conf = self.getConfig()
		filename = conf['player']['play_list_file']
		content=[]
		for item in self.tvitems.values():
			content.append(item)
		data = json.dumps(content)
		fp = open(PATH+'/'+filename,'w')
		fp.write(data)
		fp.close()
		QMessageBox.about(self,u'提示',u'save okay!')

	def	onAddFile(self):
		files = QFileDialog.getOpenFileNames(self)
		for no,file in enumerate(files):
			no+=1
			file = file.toUtf8().data().decode('utf-8')
			basename = os.path.basename(file)
			print no, file

			playitem ={'basename':basename,'fullname':file}
			row = (str(no),playitem['basename'])
			print row
			ti = QTreeWidgetItem(row )
			self.tvFiles.addTopLevelItem(ti)
			self.tvitems[ti] = playitem


		self.adjustTreeList()

	def load_default(self):
		conf = self.getConfig()
		filename = conf['player']['play_list_file']
		content=[]
		if not os.path.exists(PATH+'/'+filename):
			return

		self.tvitems.clear()
		fp = open(PATH+'/'+filename)
		content = fp.read()
		filelist = json.loads(content)
		for no,item in enumerate(filelist):
			row = (str(no),item['basename'])
			ti = QTreeWidgetItem(row )
			self.tvFiles.addTopLevelItem(ti)
			self.tvitems[ti] = item


		self.adjustTreeList()

	def adjustTreeList(self):
		count = 1
		for idx in range(self.tvFiles.topLevelItemCount()):
			ti = self.tvFiles.topLevelItem(idx)
			ti.setText(0,str(count))
			count+=1
		self.tvFiles.resizeColumnToContents(0)
		self.tvFiles.resizeColumnToContents(1)

	def playFile(self):
		if self.tvFiles.topLevelItemCount() == 0:
			return
		ti = None
		items = self.tvFiles.selectedItems()
		if items:
			ti = items[0]
		if not ti:
			ti = self.tvFiles.topLevelItem(0)
		self.current_ti = ti
		self.tvFiles.setCurrentItem(ti)

		playitem = self.tvitems[ti]
		basename = playitem['basename']
		filename = playitem['fullname']
		self.playfilename.setText(basename)
		self.playtime.setText('')
		self.playwnd.OpenFile(filename)

		#write film filename to file
		fp = open(PATH+'/filmname.txt','w')
		fp.write(basename.encode('utf-8'))
		# fp.write(basename.decode('gbk').encode('utf-8'))
		fp.close()


	def onTreeItemDoubleClick(self,ti,col):
		self.playFile()

	def PlayPause(self):
		"""Toggle play/pause status
		"""
		# if self.tvFiles.topLevelItemCount() == 0:
		# 	return

		if self.playwnd.mediaplayer.is_playing():
			self.playwnd.mediaplayer.pause()
			self.playbutton.setText("Play")
			self.playwnd.isPaused = True
		else:
			ti = None
			if self.playwnd.mediaplayer.play() == -1:
			# if True:
				# items = self.tvFiles.selectedItems()
				# if items:
				# 	ti = items[0]
				# else:
				# 	ti = self.tvFiles.topLevelItem(0) #默认播放第一条
				#
				# if ti:
				#
				# 	self.playFile(ti)
				self.playFile()
				# self.playwnd.OpenFile()
				return
			self.playwnd.mediaplayer.play()
			self.playbutton.setText("Pause")
			self.playwnd.timer.start()
			self.playwnd.isPaused = False

	def Stop(self):
		"""Stop player
		"""
		self.playwnd.mediaplayer.stop()
		self.playbutton.setText("Play")

		self.PlayNext()
		# if rewind is set ,then replay


	def PlayNext(self):
		if not self.tvFiles.topLevelItemCount():
			self.current_ti = None
			return

		if self.current_ti == None :
			self.current_ti = self.tvFiles.topLevelItem(0)
		else:
			idx = self.tvFiles.indexOfTopLevelItem(self.current_ti)
			idx+=1
			if idx == self.tvFiles.topLevelItemCount():
				self.current_ti = self.tvFiles.topLevelItem(0) # rewind to first
			else:
				self.current_ti = self.tvFiles.topLevelItem(idx)
		self.tvFiles.setCurrentItem( self.current_ti)
		self.playFile()

	def human_time(self,value):
		s = value%60
		h = value/3600
		m = (value-h*3600)/60

		return '%02d:%02d:%02d'%(h,m,s)

	def play_percent(self,current,length):
		return "%02d"%(current/length*100+1)

	def onPlayProgress(self,duration,elapsed,progress):
		current = self.human_time( elapsed)
		all = self.human_time( duration )
		playtime = current+'/'+all +'('+self.play_percent(elapsed,duration)+'%)'
		self.playtime.setText( playtime )
		self.positionslider.setValue(progress)

		#write play time to file
		if time.time() - self.last_elapsed_time > 5:
			fp = open(PATH+'/playtime.txt','w')
			fp.write(playtime.encode('utf-8'))
			fp.close()
			self.last_elapsed_time = time.time()

	def onSliderPressed(self):
		self.playwnd.setPosition( self.positionslider.sliderPosition())

	# def onPlayEnd(self):
	# 	print 'play is ending..'
	# 	pass

def test():
	fp = open('playlist.json')
	d = fp.read()
	list = json.loads(d)
	fp = open('test.txt','w')
	fp.write( list[0]['basename'].encode('utf-8'))
	fp.close()

if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	wnd = PlayCtrlWnd()
	wnd.show()
	# wnd.resize(901, 619)
	# print app ,wnd

	# test()

	sys.exit(app.exec_())