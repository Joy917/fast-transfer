# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\SVNzhangy\fast-transfer\src\_sever.ui'
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
        Form.resize(798, 732)
        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.groupBox_2 = QtGui.QGroupBox(Form)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.checkBox_time = QtGui.QCheckBox(self.groupBox_2)
        self.checkBox_time.setObjectName(_fromUtf8("checkBox_time"))
        self.horizontalLayout.addWidget(self.checkBox_time)
        self.dateTimeEdit_start = QtGui.QDateTimeEdit(self.groupBox_2)
        self.dateTimeEdit_start.setDateTime(QtCore.QDateTime(QtCore.QDate(2017, 1, 1), QtCore.QTime(0, 0, 0)))
        self.dateTimeEdit_start.setCalendarPopup(True)
        self.dateTimeEdit_start.setObjectName(_fromUtf8("dateTimeEdit_start"))
        self.horizontalLayout.addWidget(self.dateTimeEdit_start)
        self.label_2 = QtGui.QLabel(self.groupBox_2)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout.addWidget(self.label_2)
        self.dateTimeEdit_end = QtGui.QDateTimeEdit(self.groupBox_2)
        self.dateTimeEdit_end.setDateTime(QtCore.QDateTime(QtCore.QDate(2018, 1, 1), QtCore.QTime(0, 0, 0)))
        self.dateTimeEdit_end.setCalendarPopup(True)
        self.dateTimeEdit_end.setObjectName(_fromUtf8("dateTimeEdit_end"))
        self.horizontalLayout.addWidget(self.dateTimeEdit_end)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        spacerItem2 = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.checkBox_ip = QtGui.QCheckBox(self.groupBox_2)
        self.checkBox_ip.setObjectName(_fromUtf8("checkBox_ip"))
        self.horizontalLayout_3.addWidget(self.checkBox_ip)
        self.lineEdit_ip = QtGui.QLineEdit(self.groupBox_2)
        self.lineEdit_ip.setObjectName(_fromUtf8("lineEdit_ip"))
        self.horizontalLayout_3.addWidget(self.lineEdit_ip)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem3)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        spacerItem4 = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem4)
        self.checkBox_fuzzy = QtGui.QCheckBox(self.groupBox_2)
        self.checkBox_fuzzy.setObjectName(_fromUtf8("checkBox_fuzzy"))
        self.horizontalLayout_4.addWidget(self.checkBox_fuzzy)
        self.lineEdit_fuzzysearch = QtGui.QLineEdit(self.groupBox_2)
        self.lineEdit_fuzzysearch.setObjectName(_fromUtf8("lineEdit_fuzzysearch"))
        self.horizontalLayout_4.addWidget(self.lineEdit_fuzzysearch)
        spacerItem5 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem5)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.gridLayout.addWidget(self.groupBox_2, 1, 0, 1, 2)
        self.groupBox = QtGui.QGroupBox(Form)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.textBrowser_log = QtGui.QTextBrowser(self.groupBox)
        self.textBrowser_log.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.textBrowser_log.setMouseTracking(True)
        self.textBrowser_log.setObjectName(_fromUtf8("textBrowser_log"))
        self.verticalLayout.addWidget(self.textBrowser_log)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.lineEdit_pagenumStart = QtGui.QLineEdit(self.groupBox)
        self.lineEdit_pagenumStart.setMaximumSize(QtCore.QSize(50, 16777215))
        self.lineEdit_pagenumStart.setObjectName(_fromUtf8("lineEdit_pagenumStart"))
        self.horizontalLayout_2.addWidget(self.lineEdit_pagenumStart)
        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setMaximumSize(QtCore.QSize(20, 16777215))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_2.addWidget(self.label_3)
        self.lineEdit_pagenumEnd = QtGui.QLineEdit(self.groupBox)
        self.lineEdit_pagenumEnd.setMaximumSize(QtCore.QSize(50, 16777215))
        self.lineEdit_pagenumEnd.setObjectName(_fromUtf8("lineEdit_pagenumEnd"))
        self.horizontalLayout_2.addWidget(self.lineEdit_pagenumEnd)
        spacerItem6 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem6)
        self.pushButton_pageup = QtGui.QPushButton(self.groupBox)
        self.pushButton_pageup.setObjectName(_fromUtf8("pushButton_pageup"))
        self.horizontalLayout_2.addWidget(self.pushButton_pageup)
        self.pushButton_pagedown = QtGui.QPushButton(self.groupBox)
        self.pushButton_pagedown.setObjectName(_fromUtf8("pushButton_pagedown"))
        self.horizontalLayout_2.addWidget(self.pushButton_pagedown)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 2)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.label_notice = QtGui.QLabel(Form)
        self.label_notice.setMinimumSize(QtCore.QSize(600, 0))
        self.label_notice.setObjectName(_fromUtf8("label_notice"))
        self.horizontalLayout_5.addWidget(self.label_notice)
        spacerItem7 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem7)
        self.pushButton_check = QtGui.QPushButton(Form)
        self.pushButton_check.setObjectName(_fromUtf8("pushButton_check"))
        self.horizontalLayout_5.addWidget(self.pushButton_check)
        self.gridLayout.addLayout(self.horizontalLayout_5, 2, 0, 1, 2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "LogManager", None))
        self.groupBox_2.setTitle(_translate("Form", "Search Setting", None))
        self.checkBox_time.setText(_translate("Form", "time：", None))
        self.label_2.setText(_translate("Form", "-----", None))
        self.checkBox_ip.setText(_translate("Form", "IP：   ", None))
        self.checkBox_fuzzy.setText(_translate("Form", "fuzzy：", None))
        self.groupBox.setTitle(_translate("Form", "Log Display", None))
        self.label_3.setText(_translate("Form", "---", None))
        self.pushButton_pageup.setText(_translate("Form", "page up ", None))
        self.pushButton_pagedown.setText(_translate("Form", "page down", None))
        self.label_notice.setText(_translate("Form", "Notice:", None))
        self.pushButton_check.setText(_translate("Form", "Check", None))

