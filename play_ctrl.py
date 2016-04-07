# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'play_ctrl.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(639, 512)
        self.positionslider = QtGui.QSlider(Form)
        self.positionslider.setGeometry(QtCore.QRect(30, 440, 581, 22))
        self.positionslider.setOrientation(QtCore.Qt.Horizontal)
        self.positionslider.setObjectName(_fromUtf8("positionslider"))
        self.playbutton = QtGui.QPushButton(Form)
        self.playbutton.setGeometry(QtCore.QRect(250, 410, 110, 32))
        self.playbutton.setObjectName(_fromUtf8("playbutton"))
        self.stopbutton = QtGui.QPushButton(Form)
        self.stopbutton.setGeometry(QtCore.QRect(360, 410, 110, 32))
        self.stopbutton.setObjectName(_fromUtf8("stopbutton"))
        self.volumeslider = QtGui.QSlider(Form)
        self.volumeslider.setGeometry(QtCore.QRect(500, 410, 111, 22))
        self.volumeslider.setOrientation(QtCore.Qt.Horizontal)
        self.volumeslider.setObjectName(_fromUtf8("volumeslider"))
        self.mutebutton = QtGui.QCheckBox(Form)
        self.mutebutton.setGeometry(QtCore.QRect(560, 390, 61, 18))
        self.mutebutton.setObjectName(_fromUtf8("mutebutton"))
        self.addbutton = QtGui.QPushButton(Form)
        self.addbutton.setGeometry(QtCore.QRect(520, 20, 110, 32))
        self.addbutton.setObjectName(_fromUtf8("addbutton"))
        self.deletebutton = QtGui.QPushButton(Form)
        self.deletebutton.setGeometry(QtCore.QRect(520, 50, 110, 32))
        self.deletebutton.setObjectName(_fromUtf8("deletebutton"))
        self.playfilename = QtGui.QLabel(Form)
        self.playfilename.setGeometry(QtCore.QRect(30, 380, 471, 16))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Helvetica"))
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.playfilename.setFont(font)
        self.playfilename.setObjectName(_fromUtf8("playfilename"))
        self.playtime = QtGui.QLabel(Form)
        self.playtime.setGeometry(QtCore.QRect(30, 410, 241, 20))
        self.playtime.setObjectName(_fromUtf8("playtime"))
        self.ckRewind = QtGui.QCheckBox(Form)
        self.ckRewind.setGeometry(QtCore.QRect(550, 340, 85, 18))
        self.ckRewind.setObjectName(_fromUtf8("ckRewind"))
        self.savebutton = QtGui.QPushButton(Form)
        self.savebutton.setGeometry(QtCore.QRect(520, 110, 110, 32))
        self.savebutton.setObjectName(_fromUtf8("savebutton"))
        self.tvFiles = QtGui.QTreeWidget(Form)
        self.tvFiles.setGeometry(QtCore.QRect(10, 10, 511, 361))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Helvetica"))
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.tvFiles.setFont(font)
        self.tvFiles.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.tvFiles.setColumnCount(2)
        self.tvFiles.setObjectName(_fromUtf8("tvFiles"))
        self.tvFiles.headerItem().setText(0, _fromUtf8("1"))
        self.tvFiles.headerItem().setText(1, _fromUtf8("2"))
        self.tvFiles.header().setVisible(False)
        self.btnClearAll = QtGui.QPushButton(Form)
        self.btnClearAll.setGeometry(QtCore.QRect(520, 80, 110, 32))
        self.btnClearAll.setObjectName(_fromUtf8("btnClearAll"))
        self.btnMoveDown = QtGui.QPushButton(Form)
        self.btnMoveDown.setGeometry(QtCore.QRect(520, 210, 110, 32))
        self.btnMoveDown.setObjectName(_fromUtf8("btnMoveDown"))
        self.btnMoveUp = QtGui.QPushButton(Form)
        self.btnMoveUp.setGeometry(QtCore.QRect(520, 180, 110, 32))
        self.btnMoveUp.setObjectName(_fromUtf8("btnMoveUp"))
        self.cbxAudioTrack = QtGui.QComboBox(Form)
        self.cbxAudioTrack.setGeometry(QtCore.QRect(20, 470, 104, 26))
        self.cbxAudioTrack.setMinimumContentsLength(0)
        self.cbxAudioTrack.setObjectName(_fromUtf8("cbxAudioTrack"))
        self.btnSetAudioTrack = QtGui.QPushButton(Form)
        self.btnSetAudioTrack.setGeometry(QtCore.QRect(120, 470, 110, 32))
        self.btnSetAudioTrack.setObjectName(_fromUtf8("btnSetAudioTrack"))

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.playbutton.setText(_translate("Form", "Play", None))
        self.stopbutton.setText(_translate("Form", "Stop", None))
        self.mutebutton.setText(_translate("Form", "Mute", None))
        self.addbutton.setText(_translate("Form", "Add", None))
        self.deletebutton.setText(_translate("Form", "Delete", None))
        self.playfilename.setText(_translate("Form", "Playing Film", None))
        self.playtime.setText(_translate("Form", "PlayTime Elasped", None))
        self.ckRewind.setText(_translate("Form", "Rewind", None))
        self.savebutton.setText(_translate("Form", "SaveList", None))
        self.btnClearAll.setText(_translate("Form", "ClearAll", None))
        self.btnMoveDown.setText(_translate("Form", "MoveDown", None))
        self.btnMoveUp.setText(_translate("Form", "MoveUp", None))
        self.btnSetAudioTrack.setText(_translate("Form", "audio set", None))

