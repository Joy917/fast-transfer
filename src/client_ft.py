# coding=utf-8

import json
import logging
import math
import os
import re
import struct
import time
from socket import *

from PySide import QtGui, QtCore

import _client_qt4


class Client(QtGui.QWidget, _client_qt4.Ui_Form):
    def __init__(self):
        super(Client, self).__init__()
        self.setupUi(self)

        self.__modifyUi()
        self.__listenEvent()

        # 软件运行日志
        self.__logger_app = self.__getLogger("App")

        self.perUp = 0
        self.perDown = 0

    # 获取日志实例方法
    def __getLogger(self, name):
        logger = logging.getLogger(name)
        fmt = logging.Formatter("%(asctime)s [%(levelname)s] [%(name)s]: %(message)s\n", datefmt="%Y-%m-%d %H:%M:%S")
        file_handler = logging.FileHandler("{}.log".format(name))
        file_handler.setFormatter(fmt)
        logger.addHandler(file_handler)
        logger.setLevel(logging.INFO)
        return logger

    # 调整UI方法
    def __modifyUi(self):
        # 设置标题及图表
        self.setWindowTitle(u"文件传输")
        self.path = os.getcwd()
        self.setWindowIcon(QtGui.QIcon(self.path + "/imgs/icon.png"))
        # 隐藏提示框及进度条
        self.progressBar_download.hide()
        self.progressBar_upload.hide()
        # 文件路径只读
        self.lineEdit_filePathUp.setReadOnly(True)
        self.lineEdit_dirPath.setReadOnly(True)
        self.label_tooltipDown.setText(u"请提供源文件路径及保存文件夹...")
        self.label_tooltipUp.setText(u"请选择上传文件及服务端保存路径...")

    # 时间监听方法
    def __listenEvent(self):
        # 上传界面事件
        self.pushButton_chooseFile.clicked.connect(self.__chooseFile)
        self.pushButton_cancleUp.clicked.connect(self.__cancleUp)
        self.pushButton_startUp.clicked.connect(self.__startUp)
        # 下载界面事件
        self.pushButton_chooseDir.clicked.connect(self.__chooseDir)
        self.pushButton_cancleDown.clicked.connect(self.__cancleDown)
        self.pushButton_startDown.clicked.connect(self.__startDown)

    '''
        上传文件系列方法
    '''

    def __chooseFile(self):
        self.progressBar_upload.setHidden(True)
        fileTuple = QtGui.QFileDialog.getOpenFileName(self, u"选择上传文件", "C:\\Users")
        self.lineEdit_filePathUp.setText(fileTuple[0])
        self.fileSize = os.path.getsize(fileTuple[0])
        self.label_tooltipUp.setText(u"文件大小 %s M" % (self.fileSize / 1024 / 1024))

    def __startUp(self):
        filePathUp = self.lineEdit_filePathUp.text()
        if "" == filePathUp.strip() or filePathUp is None:
            self.__logger_app.info(u"上传时文件路径为空...")
            self.label_tooltipUp.setText(u"文件路径不能为空!")
            return False
        upDirPath = self.lineEdit_upDirPath.text()
        # 正则匹配磁盘名
        p = re.match(r"[a-zA-Z]:[/\\]", str(upDirPath))
        if not p:
            self.__logger_app.info(u"上传时文件夹路径不合法...")
            self.label_tooltipUp.setText(u"上传时文件夹路径不合法...")
            return False
        self.upThread = Upload(filePathUp, upDirPath, self.__logger_app)
        # 启动信号连接
        self.upThread.upingSignal.connect(self.__uping)
        self.upThread.upedSignal.connect(self.__uped)
        self.upThread.upTooltipSignal.connect(self.__tooltipUp)
        self.upThread.upProgressSignal.connect(self.__progressUp)
        self.upThread.start()

    def __cancleUp(self):
        self.lineEdit_filePathUp.clear()
        self.lineEdit_upDirPath.clear()
        self.label_tooltipUp.setText(u"请选择上传文件及服务端保存路径...")
        self.progressBar_upload.setHidden(True)

    def __uping(self):
        self.pushButton_chooseFile.setDisabled(True)
        self.pushButton_startUp.setDisabled(True)
        self.pushButton_cancleUp.setDisabled(True)
        self.progressBar_upload.setHidden(False)

    def __uped(self):
        self.pushButton_chooseFile.setDisabled(False)
        self.pushButton_startUp.setDisabled(False)
        self.pushButton_cancleUp.setDisabled(False)

    def __tooltipUp(self, content):
        self.label_tooltipUp.setText(content)

    def __progressUp(self, value):
        self.progressBar_upload.setValue(value)

    '''
        下载文件系列方法
    '''

    def __chooseDir(self):
        dirPath = QtGui.QFileDialog.getExistingDirectory(self, u"选择文件夹", "C:\\Users")
        self.lineEdit_dirPath.setText(dirPath)

    def __startDown(self):
        filePath_down = self.lineEdit_filePathDown.text()
        # 正则匹配磁盘名
        p = re.match(r"[a-zA-Z]:[/\\]", str(filePath_down))
        if not p:
            self.__logger_app.info(u"下载时源文件路径不合法")
            self.label_tooltipDown.setText(u"下载时源文件路径不合法")
            return False
        dirPath = self.lineEdit_dirPath.text()
        if "" == dirPath.strip() or dirPath is None:
            self.__logger_app.info(u"下载时保存文件夹路径为空...")
            self.label_tooltipDown.setText(u"文件夹路径不能为空!")
            return False
        # 转储至本地文件夹
        fileName = os.path.basename(filePath_down)
        savePath = dirPath + "\\" + fileName
        if os.path.isfile(savePath):
            self.__logger_app.info(u"下载时存在同名文件...请更换保存文件夹")
            self.label_tooltipDown.setText(u"下载时存在同名文件...请更换保存文件夹!")
            return False
        else:
            self.downThread = Download(savePath, filePath_down, self.__logger_app)
            self.downThread.downingSignal.connect(self.__downing)
            self.downThread.downedSignal.connect(self.__downed)
            self.downThread.downTooltipSignal.connect(self.__tooltipDown)
            self.downThread.downProgressSignal.connect(self.__progressDown)
            self.downThread.start()

    def __cancleDown(self):
        self.lineEdit_dirPath.clear()
        self.lineEdit_filePathDown.clear()
        self.label_tooltipDown.setText(u"请提供源文件路径及保存文件夹...")
        self.progressBar_download.setHidden(True)

    def __downing(self):
        # 下载等按钮失效
        self.lineEdit_filePathDown.setReadOnly(True)
        self.pushButton_startDown.setDisabled(True)
        self.pushButton_chooseDir.setDisabled(True)
        self.pushButton_cancleDown.setDisabled(True)
        self.progressBar_download.setHidden(False)

    def __downed(self):
        self.lineEdit_filePathDown.setReadOnly(False)
        self.pushButton_startDown.setDisabled(False)
        self.pushButton_chooseDir.setDisabled(False)
        self.pushButton_cancleDown.setDisabled(False)

    def __tooltipDown(self, content):
        self.label_tooltipDown.setText(content)

    def __progressDown(self, value):
        self.progressBar_download.setValue(value)


# 创建上传及下载的线程
class Upload(QtCore.QThread):
    # 定义触发信号
    upingSignal = QtCore.Signal()
    upedSignal = QtCore.Signal()
    upProgressSignal = QtCore.Signal(float)
    upTooltipSignal = QtCore.Signal(str)

    def __init__(self, filePathUp, upDirPath, logger_app):
        super(Upload, self).__init__()
        self.filePathUp = filePathUp
        self.upDirPath = upDirPath
        self.__logger_app = logger_app

    def run(self):
        # 传输数据大小
        global DATA_SIZE
        # 计时
        startTime = time.time()
        # 初始化上传百分比
        perUp = 0
        # 初始化socket
        self.tcpSocket = socket(AF_INET, SOCK_STREAM)
        # 读取服务端信息
        root_path = os.getcwd()
        with open(root_path + "/config/severInfo.json", "r") as f:
            severInfo_str = f.read()
            severInfo_dic = json.loads(severInfo_str)
            self.severAddr = (severInfo_dic["ip"], severInfo_dic["port"])
        if os.path.isfile(self.filePathUp):
            # 判断是否可读
            if os.access(self.filePathUp, os.R_OK):
                with open(self.filePathUp, "rb") as fr:
                    fileSize = os.path.getsize(self.filePathUp)
                    self.upTooltipSignal.emit(u"文件上传中...大小 %s M" % (fileSize / 1024 / 1024))
                    try:
                        # 连接服务端
                        self.tcpSocket.connect(self.severAddr)
                    except Exception as e:
                        self.upTooltipSignal.emit(u"连接服务器失败,请稍后重试...")
                        self.__logger_app.error(u"上传时连接服务器失败...{}".format(e))
                    else:
                        try:
                            # 通知服务端上传任务
                            task = struct.pack("4s", "up")
                            self.tcpSocket.send(task)
                            # 定义文件头信息，包含文件名,上传至文件夹及文件大小
                            fileHead = struct.pack("128s128sq", str(self.filePathUp), str(self.upDirPath),
                                                   fileSize)  # struct打包
                            self.tcpSocket.send(fileHead)
                            # 文件传输开始触发信号
                            self.upingSignal.emit()
                            # 已发送数据
                            sendedSize = 0
                            while fileSize <> sendedSize:
                                if fileSize - sendedSize > DATA_SIZE:
                                    data = fr.read(DATA_SIZE)
                                    perUp += DATA_SIZE * 1.0 / fileSize * 100
                                else:
                                    data = fr.read(fileSize - sendedSize)
                                    perUp = 100
                                self.tcpSocket.sendall(data)
                                sendedSize += len(data)
                                self.upProgressSignal.emit(perUp)

                            endSize = struct.calcsize("2s")
                            # 等待结束反馈
                            end = self.tcpSocket.recv(endSize)
                            if end:
                                endFlag = struct.unpack("2s", end)[0].strip("\0")  # 解包,任务名,去除末尾补齐的字符位
                                if not "ok" == endFlag:
                                    self.__logger_app.error(u"上传时文件尾部接受错误")
                        except Exception as e:
                            self.upTooltipSignal.emit(u"传输数据出错...请联系管理员")
                            self.__logger_app.error(u"上传时传输数据出错...{}".format(e))
                        else:
                            # 下载完成，统计用时
                            endTime = time.time()
                            usedTime = math.floor(endTime - startTime)
                            self.upTooltipSignal.emit(u"文件上传成功!共耗时{}s".format(usedTime))
                    finally:
                        # 文件传输结束触发信号
                        self.upedSignal.emit()
            else:
                self.upTooltipSignal.emit(u"没有权限读取文件...")
                self.__logger_app.info(u"上传时没有权限读取文件...")
        else:
            self.upTooltipSignal.emit(u"文件不存在...")
            self.__logger_app.info(u"上传时文件不存在...")

        self.tcpSocket.close()


class Download(QtCore.QThread):
    # 定义触发信号
    downingSignal = QtCore.Signal()
    downedSignal = QtCore.Signal()
    downProgressSignal = QtCore.Signal(float)
    downTooltipSignal = QtCore.Signal(str)

    def __init__(self, savePath, filePathDown, logger_app):
        super(Download, self).__init__()

        self.filePathDown = str(filePathDown)
        self.savePath = savePath
        self.__logger_app = logger_app

    def run(self):
        global DATA_SIZE
        # 计时
        startTime = time.time()
        # 初始化下载百分比
        perDown = 0
        # 初始化socket
        self.tcpSocket = socket(AF_INET, SOCK_STREAM)
        # 读取服务端信息
        root_path = os.getcwd()
        with open(root_path + "/config/severInfo.json", "r") as f:
            severInfo_str = f.read()
            severInfo_dic = json.loads(severInfo_str)
            self.severAddr = (severInfo_dic["ip"], severInfo_dic["port"])
        try:
            self.tcpSocket.connect(self.severAddr)
        except Exception as e:
            self.__logger_app.error(u"下载时连接服务端出错...{}".format(e))
            self.downTooltipSignal.emit("连接服务端出错,请联系管理员...")
        else:
            try:
                # 通知服务端下载任务
                self.tcpSocket.send(struct.pack("4s", "down"))
                self.tcpSocket.send(struct.pack("128s", self.filePathDown))  # 打包文件地址
                fheadSize = struct.calcsize("q")
                fhead = self.tcpSocket.recv(fheadSize)
            except Exception as e:
                self.__logger_app.error(u"下载时头文件发送失败...{}".format(e))
            else:
                if fhead:
                    fileSize = struct.unpack("q", fhead)[0]  # 解包头文件，下载文件大小
                    if fileSize <> 0:
                        self.downingSignal.emit()
                        try:
                            with open(self.savePath, "wb") as fw:
                                self.downTooltipSignal.emit(u"文件下载中...大小 %s M" % (fileSize / 1024 / 1024))
                                receivedSize = 0  # 接收文件大小
                                while fileSize <> receivedSize:
                                    data = self.tcpSocket.recv(DATA_SIZE)
                                    receivedSize += len(data)
                                    perDown += DATA_SIZE * 1.0 / fileSize * 100
                                    if perDown >= 100:
                                        perDown = 100
                                    # 转储至本地文件夹
                                    fw.write(data)
                                    self.downProgressSignal.emit(perDown)
                                fw.flush()  # 写入缓存区文件
                                os.fsync(fw)

                                # 接受完成发送反馈
                                endMessage = struct.pack("2s", "ok")
                                self.tcpSocket.send(endMessage)
                        except Exception as e:
                            self.__logger_app.error(u"文件下载失败...{}".format(e))
                            self.downTooltipSignal.emit(u"文件下载失败,请联系管理员...")
                            # 清除接受的残余文件
                            os.remove(self.savePath)
                        else:
                            # 下载完成，统计用时
                            endTime = time.time()
                            usedTime = math.floor(endTime - startTime)
                            self.downTooltipSignal.emit(u"文件下载成功!共耗时{}s".format(usedTime))
                    else:
                        self.__logger_app.error(u"文件下载时源文件不存在...")
                        self.downTooltipSignal.emit(u"源文件不存在，请检查下载文件路径是否正确...")
            finally:
                # 结束信号
                self.downedSignal.emit()
        self.tcpSocket.close()


if __name__ == "__main__":
    import sys

    """全局变量位置"""
    # 每次传输数据大小
    DATA_SIZE = 1024 * 100

    app = QtGui.QApplication(sys.argv)
    client = Client()
    client.show()
    sys.exit(app.exec_())
