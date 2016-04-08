#coding:utf-8
__author__ = 'scott'

"""
提供udp侦听服务，接收外部用户发起的查询和控制请求
commnad:
	获取当前播放信息（时间进度，影片名称)
	获取播放列表
	停止播放
	播放上一项、播放下一项
	播放指定影片
	切换声音通道
"""

import socket
import threading,time,os,traceback,json
import web
PATH = os.path.dirname(os.path.abspath(__file__))

URLS = (
	'/', 'Index',
	'/playIndex','PlayIndex', #播放指定文件  ?index=2
	'/playInfo','PlayInfo',
	'/playList','PlayList',
	'/playSkip','PlaySkip', # ?pos=10  forward 10 second
	'/setTrack','SetTrack', # ?track=1
)

class Index:
	def GET(self):
		render = web.template.render(PATH+'/template')
		# hello = web.template.frender('templates/hello.html')
		return render.pandatv('hello')
		# return "Hello, world!"

class PlayInfo:
	def GET(self):
		player = PlayController.instance().getPlayer()
		info = player.getPlayInfo()
		web.header('Content-Type', 'application/json')
		return json.dumps(info)


class PlayList:
	def GET(self):
		player = PlayController.instance().getPlayer()
		info = player.getPlayList()
		web.header('Content-Type', 'application/json')
		return json.dumps(info)

class PlaySkip:
	"""
	播放跳跃
	"""
	def GET(self):
		i = web.input()
		index = i.get('index')

class PlayIndex:
	"""
	播放指定索引视频文件
	"""
	def GET(self):
		i = web.input()
		index = i.get('index')
		index = int(index)
		player = PlayController.instance().getPlayer()
		# player.playIndex(index)
		player.singal_playIndex.emit(index)


class SetTrack:
	def GET(self):
		i = web.input()
		track = i.get('track')
		track = int(track)

		player = PlayController.instance().getPlayer()
		player.playSetAudioTrack(track)

class PlayController:
	Name='chomp'
	def __init__(self,player,conf):
		self.player = player
		self.conf = conf
		self.sock = None
		PlayController._instance = self

	def getPlayer(self):
		return self.player


	def run(self):
		thread = threading.Thread(target=self.http_serv)
		thread.start()
		return True


	def http_serv(self):
		print 'web service starting..'
		self.app = web.application(URLS, globals())
		self.app.run()

	def stop(self):
		self.app.stop()


	_instance = None
	@staticmethod
	def instance():
		return PlayController._instance



