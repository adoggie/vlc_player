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


		self.init_signal()

		self.init_data()
		self.init_ui()
		self.load_default()
		self.load_extensions()

	singal_playIndex = pyqtSignal(object)

	def init_signal(self):
		self.singal_playIndex.connect(self.playIndex)



	def init_data(self):
		self.playlist =[]
		self.tvitems ={}
		self.current_ti = None

		self.last_elapsed_time = 0

		self.current_playfilm = ''
		self.current_playtime =''

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
		self.connect(self.btnClearAll,SIGNAL('clicked()'),self.onClearAll)
		self.connect(self.btnMoveUp,SIGNAL('clicked()'),self.onMoveUp)
		self.connect(self.btnMoveDown,SIGNAL('clicked()'),self.onMoveDown)
		self.connect(self.btnSetAudioTrack,SIGNAL('clicked()'),self.onSetAudioTrack)

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

		self.connect(self.cbxAudioTrack,SIGNAL('currentIndexChanged(int)'),self.onAudioTrackChanged)


		self.cbxAudioTrack.addItem('Track-0')
		self.cbxAudioTrack.addItem('Track-1')
		self.cbxAudioTrack.addItem('Track-2')
		self.cbxAudioTrack.addItem('Track-3')


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

		for idx in range(self.tvFiles.topLevelItemCount()):
			ti = self.tvFiles.topLevelItem(idx)
			content.append( self.tvitems[ti] )
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

		# self.tvFiles.topLevelItem(0).setSelected(True)
		# self.tvFiles.topLevelItem(1).setSelected(True)

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
		print 'playFile:'
		print ti
		playitem = self.tvitems[ti]
		basename = playitem['basename']
		filename = playitem['fullname']
		self.playfilename.setText(basename)
		self.playtime.setText('')
		self.playwnd.OpenFile(filename)

		#write film filename to file
		fp = open(PATH+'/filmname.txt','w')
		fp.write(basename.encode('utf-8'))
		fp.close()

		self.current_playfilm = basename.encode('utf-8')


	def onTreeItemDoubleClick(self,ti,col):
		self.playFile()

	def PlayPause(self):
		"""Toggle play/pause status
		"""

		if self.playwnd.mediaplayer.is_playing():
			self.playwnd.mediaplayer.pause()
			self.playbutton.setText("Play")
			self.playwnd.isPaused = True
		else:
			ti = None
			if self.playwnd.mediaplayer.play() == -1:
				self.playFile()
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
		# print current,length
		if not length:
			return '00'
		return "%02d"%(current/(length*1.0)*100+1)

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

			self.current_playtime = playtime.encode('utf-8')

	def onSliderPressed(self):
		self.playwnd.setPosition( self.positionslider.sliderPosition())

	def onMoveDown(self):
		items = self.tvFiles.selectedItems()
		if not items:
			return
		# qt bug , orders will be wrong after treeitem moving.
		# must sort treeitem as new array
		items = sorted(items,lambda x,y:cmp(self.tvFiles.indexOfTopLevelItem(x),self.tvFiles.indexOfTopLevelItem(y)))

		first = items[0]
		end = items[-1]
		idx = self.tvFiles.indexOfTopLevelItem(end)
		if idx == self.tvFiles.topLevelItemCount()-1:
			return
		items.reverse()
		for ti in items:
			idx = self.tvFiles.indexOfTopLevelItem(ti)
			below = self.tvFiles.topLevelItem(idx+1)
			self.tvFiles.takeTopLevelItem(idx+1)
			self.tvFiles.insertTopLevelItem(idx,below)
		for ti in items:
			ti.setSelected(True)
		self.adjustTreeList()

	def onMoveUp(self):
		items = self.tvFiles.selectedItems()
		if not items:
			return
		# qt bug , orders will be wrong after treeitem moving.
		# must sort treeitem as new array
		items = sorted(items,lambda x,y:cmp(self.tvFiles.indexOfTopLevelItem(x),self.tvFiles.indexOfTopLevelItem(y)))

		first = items[0]
		# end = items[-1]
		idx = self.tvFiles.indexOfTopLevelItem( first)
		if idx == 0:
			return # reached header
		# items.reverse()
		for ti in items:
			idx = self.tvFiles.indexOfTopLevelItem(ti)
			up = self.tvFiles.topLevelItem(idx-1)
			self.tvFiles.takeTopLevelItem(idx-1)
			self.tvFiles.insertTopLevelItem(idx,up)
		for ti in items:
			ti.setSelected(True)
		self.adjustTreeList()

		pass

	def onClearAll(self):
		track_count = self.playwnd.mediaplayer.audio_get_track_count()
		track_current = self.playwnd.mediaplayer.audio_get_track()
		print track_count,track_current

		self.tvitems = {}
		self.current_ti = None
		self.tvFiles.clear()

	def onSetAudioTrack(self):
		idx = self.cbxAudioTrack.currentIndex()
		self.playwnd.mediaplayer.audio_set_track(idx)

	def onAudioTrackChanged(self,index):
		self.playwnd.mediaplayer.audio_set_track(index)

	def load_extensions(self):
		if not hasattr(self,'extensions'):
			self.extensions =[]

		import extension
		for mcls in extension.all:
			print mcls.Name

			conf = self.getConfig()['extension'].get(mcls.Name)
			if not conf['enable']:
				continue
			print 'create module: ',mcls.Name
			inst = mcls(self,conf)
			print 'instance: ',inst
			inst.run()
			self.extensions.append(inst)

	def unload_extensions(self):
		if not hasattr(self,'extensions'):
			return
		for ext in self.extensions:
			ext.stop()


	def getPlayInfo(self,max_list_num = 999):
		"""
		获取当前播放信息
			- 当前影片, 播放时间信息, 已播放影片, 待播放影片
			- 当前音轨编号
		"""
		start = 0
		if self.current_ti:
			start = self.tvFiles.indexOfTopLevelItem(self.current_ti)
		result = []
		for idx in range(start+1, self.tvFiles.topLevelItemCount()):
			if len(result) > max_list_num:
				break
			ti = self.tvFiles.topLevelItem(idx)
			name = self.tvitems[ti]['basename']
			result.append( {'index':idx,'name':name} )


		info = {
			'film':self.current_playfilm,
			'time':self.current_playtime,
			'film_played':[],
			'film_next': result,
			'film_audio_track_count':self.playwnd.mediaplayer.audio_get_track_count(),
			'file_audio_track_current':self.playwnd.mediaplayer.audio_get_track()
		}
		return info

	def getPlayList(self,max_list_num= 999):
		"""
		获取播放影片列表
		"""
		result = []
		for idx in range(self.tvFiles.topLevelItemCount()):
			if len(result) > max_list_num:
				break
			ti = self.tvFiles.topLevelItem(idx)
			name = self.tvitems[ti]['basename']
			result.append( {'index':idx,'name':name} )
			# print 'tree-item index:'
			treeidx = self.tvFiles.indexOfTopLevelItem(ti)
			print idx,' ',treeidx,'  ',name
		return result

	def playIndex(self,index):
		"""
		播放指定索引的影片
		"""
		print 'ready to play index:',index
		ti = self.tvFiles.topLevelItem(index)
		if not ti:
			return
		if self.current_ti == ti:
			return
		print self.tvitems[ti]['basename']


		self.tvFiles.setCurrentItem(ti)
		# ti.setSelected(True)
		print 'treeItem:',ti
		self.playFile()


	def playSkip(self,span):
		"""
		播放时间跳跃 , + - 控制向前还是向后
		:param span:
		:return:
		"""
		pass

	def playSetAudioTrack(self,track):
		"""
		设置音轨
		:param track:
		:return:
		"""
		self.playwnd.mediaplayer.audio_set_track(track)



	def playPrev(self):
		pass

	def playNext(self):
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

	def closeEvent(self,event):
		self.unload_extensions()
		event.accept()

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
	sys.exit(app.exec_())