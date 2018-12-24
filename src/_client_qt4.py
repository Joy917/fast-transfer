# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\SVNzhangy\fast-transfer\src\_client.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

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
        Form.resize(470, 250)
        Form.setMinimumSize(QtCore.QSize(470, 250))
        Form.setMaximumSize(QtCore.QSize(470, 250))
        Form.setSizeIncrement(QtCore.QSize(470, 250))
        self.tabWidget = QtGui.QTabWidget(Form)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 470, 250))
        self.tabWidget.setMinimumSize(QtCore.QSize(470, 250))
        self.tabWidget.setMaximumSize(QtCore.QSize(470, 250))
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab_download = QtGui.QWidget()
        self.tab_download.setObjectName(_fromUtf8("tab_download"))
        self.progressBar_download = QtGui.QProgressBar(self.tab_download)
        self.progressBar_download.setGeometry(QtCore.QRect(10, 160, 431, 23))
        self.progressBar_download.setProperty("value", 24)
        self.progressBar_download.setObjectName(_fromUtf8("progressBar_download"))
        self.label_tooltipDown = QtGui.QLabel(self.tab_download)
        self.label_tooltipDown.setGeometry(QtCore.QRect(10, 190, 431, 21))
        self.label_tooltipDown.setObjectName(_fromUtf8("label_tooltipDown"))
        self.pushButton_startDown = QtGui.QPushButton(self.tab_download)
        self.pushButton_startDown.setGeometry(QtCore.QRect(230, 100, 93, 28))
        self.pushButton_startDown.setObjectName(_fromUtf8("pushButton_startDown"))
        self.pushButton_cancleDown = QtGui.QPushButton(self.tab_download)
        self.pushButton_cancleDown.setGeometry(QtCore.QRect(340, 100, 71, 28))
        self.pushButton_cancleDown.setObjectName(_fromUtf8("pushButton_cancleDown"))
        self.lineEdit_filePathDown = QtGui.QLineEdit(self.tab_download)
        self.lineEdit_filePathDown.setGeometry(QtCore.QRect(70, 14, 359, 21))
        self.lineEdit_filePathDown.setObjectName(_fromUtf8("lineEdit_filePathDown"))
        self.label_filePathDown = QtGui.QLabel(self.tab_download)
        self.label_filePathDown.setGeometry(QtCore.QRect(10, 10, 53, 29))
        self.label_filePathDown.setObjectName(_fromUtf8("label_filePathDown"))
        self.lineEdit_dirPath = QtGui.QLineEdit(self.tab_download)
        self.lineEdit_dirPath.setGeometry(QtCore.QRect(110, 54, 319, 21))
        self.lineEdit_dirPath.setReadOnly(True)
        self.lineEdit_dirPath.setObjectName(_fromUtf8("lineEdit_dirPath"))
        self.pushButton_chooseDir = QtGui.QPushButton(self.tab_download)
        self.pushButton_chooseDir.setGeometry(QtCore.QRect(10, 50, 93, 28))
        self.pushButton_chooseDir.setObjectName(_fromUtf8("pushButton_chooseDir"))
        self.tabWidget.addTab(self.tab_download, _fromUtf8(""))
        self.tab_upload = QtGui.QWidget()
        self.tab_upload.setObjectName(_fromUtf8("tab_upload"))
        self.pushButton_cancleUp = QtGui.QPushButton(self.tab_upload)
        self.pushButton_cancleUp.setGeometry(QtCore.QRect(350, 100, 71, 28))
        self.pushButton_cancleUp.setObjectName(_fromUtf8("pushButton_cancleUp"))
        self.pushButton_startUp = QtGui.QPushButton(self.tab_upload)
        self.pushButton_startUp.setGeometry(QtCore.QRect(240, 100, 93, 28))
        self.pushButton_startUp.setObjectName(_fromUtf8("pushButton_startUp"))
        self.progressBar_upload = QtGui.QProgressBar(self.tab_upload)
        self.progressBar_upload.setGeometry(QtCore.QRect(10, 160, 431, 23))
        self.progressBar_upload.setProperty("value", 24)
        self.progressBar_upload.setObjectName(_fromUtf8("progressBar_upload"))
        self.label_tooltipUp = QtGui.QLabel(self.tab_upload)
        self.label_tooltipUp.setGeometry(QtCore.QRect(10, 190, 431, 21))
        self.label_tooltipUp.setObjectName(_fromUtf8("label_tooltipUp"))
        self.pushButton_chooseFile = QtGui.QPushButton(self.tab_upload)
        self.pushButton_chooseFile.setGeometry(QtCore.QRect(10, 10, 101, 28))
        self.pushButton_chooseFile.setObjectName(_fromUtf8("pushButton_chooseFile"))
        self.lineEdit_filePathUp = QtGui.QLineEdit(self.tab_upload)
        self.lineEdit_filePathUp.setGeometry(QtCore.QRect(120, 14, 319, 21))
        self.lineEdit_filePathUp.setInputMask(_fromUtf8(""))
        self.lineEdit_filePathUp.setText(_fromUtf8(""))
        self.lineEdit_filePathUp.setReadOnly(True)
        self.lineEdit_filePathUp.setObjectName(_fromUtf8("lineEdit_filePathUp"))
        self.label_upDirPath_2 = QtGui.QLabel(self.tab_upload)
        self.label_upDirPath_2.setGeometry(QtCore.QRect(22, 56, 61, 29))
        self.label_upDirPath_2.setObjectName(_fromUtf8("label_upDirPath_2"))
        self.lineEdit_upDirPath = QtGui.QLineEdit(self.tab_upload)
        self.lineEdit_upDirPath.setGeometry(QtCore.QRect(90, 60, 351, 21))
        self.lineEdit_upDirPath.setObjectName(_fromUtf8("lineEdit_upDirPath"))
        self.tabWidget.addTab(self.tab_upload, _fromUtf8(""))

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.label_tooltipDown.setText(_translate("Form", "提示消息！", None))
        self.pushButton_startDown.setText(_translate("Form", "开始下载", None))
        self.pushButton_cancleDown.setText(_translate("Form", "取消", None))
        self.label_filePathDown.setText(_translate("Form", "源路径:", None))
        self.pushButton_chooseDir.setText(_translate("Form", "选择文件夹", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_download), _translate("Form", "Tab 1", None))
        self.pushButton_cancleUp.setText(_translate("Form", "取消", None))
        self.pushButton_startUp.setText(_translate("Form", "开始上传", None))
        self.label_tooltipUp.setText(_translate("Form", "提示消息！", None))
        self.pushButton_chooseFile.setText(_translate("Form", "选择上传文件", None))
        self.lineEdit_filePathUp.setToolTip(_translate("Form", "粘贴本地文件路径", None))
        self.label_upDirPath_2.setText(_translate("Form", "上传至:", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_upload), _translate("Form", "Tab 2", None))

