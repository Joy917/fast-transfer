# coding=utf-8

from socket import *
import struct,os,json
from PySide import QtGui,QtCore
from multiprocessing import Process
import _client_qt4


class Client(QtGui.QWidget,_client_qt4.Ui_Form):
    def __init__(self):
        super(Client,self).__init__()
        self.setupUi(self)

        self.modifyUi()
        self.setup()


    def modifyUi(self):

        # 隐藏提示框及进度条
        self.progressBar_download.hide()
        self.progressBar_upload.hide()
        # 文件路径只读
        self.lineEdit_filePathUp.setReadOnly(True)
        self.lineEdit_dirPath.setReadOnly(True)
        self.label_tooltipDown.setText(u"请提供源文件路径及保存文件夹...")
        self.label_tooltipUp.setText(u"请选择上传文件...")

    def listenEvent(self):
        # 上传界面事件
        self.pushButton_chooseFile.clicked.connect(self.chooseFile)
        self.pushButton_cancleUp.clicked.connect(self.cancleUp)
        self.pushButton_startUp.clicked.connect(self.startUp)
        # 下载界面事件
        self.pushButton_chooseDir.clicked.connect(self.chooseDir)
        self.pushButton_cancleDown.clicked.connect(self.cancleDown)
        self.pushButton_startDown.clicked.connect(self.startDown)

    def setup(self):
        self.listenEvent()

    '''
        上传文件系列方法
    '''
    def chooseFile(self):
        self.progressBar_upload.setHidden(True)
        fileTuple = QtGui.QFileDialog.getOpenFileName(self, u"选择上传文件", "C:\\Users")
        self.lineEdit_filePathUp.setText(fileTuple[0])
        self.fileSize = os.path.getsize(fileTuple[0])
        self.label_tooltipUp.setText(u"文件大小 %s M" % (self.fileSize / 1024 / 1024))
    def startUp(self):
        filePathUp = self.lineEdit_filePathUp.text()
        self.upThread = Upload(filePathUp)
        # 启动信号连接
        self.upThread.upingSignal.connect(self.uping)
        self.upThread.upedSignal.connect(self.uped)
        self.upThread.tooltipSignal.connect(self.tooltipUp)
        self.upThread.progressSignal.connect(self.progressUp)
        self.upThread.start()
    def cancleUp(self):
        self.lineEdit_filePathUp.clear()
        self.label_tooltipUp.setText(u"请选择上传文件...")
        self.progressBar_upload.setHidden(True)
    def uping(self):
        self.pushButton_chooseFile.setDisabled(True)
        self.pushButton_startUp.setDisabled(True)
        self.pushButton_cancleUp.setDisabled(True)
        self.progressBar_upload.setHidden(False)
    def uped(self):
        self.pushButton_chooseFile.setDisabled(False)
        self.pushButton_startUp.setDisabled(False)
        self.pushButton_cancleUp.setDisabled(False)
    def tooltipUp(self,content):
        self.label_tooltipUp.setText(content)
    def progressUp(self,value):
        self.progressBar_upload.setValue(value)

    '''
        下载文件系列方法
    '''
    def chooseDir(self):
        dirPath = QtGui.QFileDialog.getExistingDirectory(self, u"选择文件夹", "C:\\Users")
        self.lineEdit_dirPath.setText(dirPath)
    def startDown(self):
        filePath_down = self.lineEdit_filePathDown.text()
        dirPath = self.lineEdit_dirPath.text()
        # 转储至本地文件夹
        fileName = os.path.basename(filePath_down)
        savePath = dirPath + "\\" + fileName
        if os.path.isfile(savePath):
            print "存在同名文件...请更换保存文件夹"
            return
        else:
            self.downThread = Download(savePath,filePath_down)
            self.downThread.downingSignal.connect(self.downing)
            self.downThread.downedSignal.connect(self.downed)
            self.downThread.tooltipSignal.connect(self.tooltipDown)
            self.downThread.progressSignal.connect(self.progressDown)
            self.downThread.start()
    def cancleDown(self):
        self.lineEdit_dirPath.clear()
        self.lineEdit_filePathDown.clear()

    def downing(self):
        # 下载等按钮失效
        self.lineEdit_filePathDown.setReadOnly(True)
        self.pushButton_startDown.setDisabled(True)
        self.pushButton_chooseDir.setDisabled(True)
        self.pushButton_cancleDown.setDisabled(True)
        self.progressBar_download.setHidden(False)
    def downed(self):
        self.lineEdit_filePathDown.setReadOnly(False)
        self.pushButton_startDown.setDisabled(False)
        self.pushButton_chooseDir.setDisabled(False)
        self.pushButton_cancleDown.setDisabled(False)
    def tooltipDown(self,content):
        self.label_tooltipDown.setText(content)
    def progressDown(self,value):
        self.progressBar_download.setValue(value)

    # 上传及下载的专属进程方法
    def upLoad(self,filePathUp):
        pass

    def downLoad(self):
        pass

# 创建上传及下载的线程
class Upload(Process,QtCore.QObject):
    # 定义触发信号
    upingSignal = QtCore.Signal()
    upedSignal = QtCore.Signal()
    upProgressSignal = QtCore.Signal(float)
    upTooltipSignal = QtCore.Signal(str)
    def __init__(self,filePathUp):
        super(Upload, self).__init__()
        self.filePathUp = filePathUp

    def run(self):
        # 初始化上传百分比
        perUp = 0
        # 初始化socket
        self.tcpSocket = socket(AF_INET, SOCK_STREAM)
        # 读取服务端信息
        f = open("..\properties\severInfo.json", "r")
        severInfo_str = f.read()
        f.close()
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
                        raise e
                    else:
                        try:
                            # 通知服务端上传任务
                            task = struct.pack("4s","up")
                            self.tcpSocket.send(task)
                            # 定义文件头信息，包含文件名及文件大小
                            fileHead = struct.pack("64sq",str(self.filePathUp), fileSize) # struct打包
                            self.tcpSocket.send(fileHead)
                            # 文件传输开始触发信号
                            self.upingSignal.emit()
                            while 1:
                                data = fr.read(1024)
                                if not data:
                                    break
                                self.tcpSocket.send(data)
                                if perUp >= 100:
                                    perUp = 100
                                else:
                                    perUp += 1024 * 1.0 / fileSize * 100
                                self.upProgressSignal.emit(perUp)
                        except Exception as e:
                            print "发送数据出错...请稍后重试",e
                            self.upTooltipSignal.emit(u"传输数据出错...请稍后重试")
                        else:
                            self.upTooltipSignal.emit(u"上传成功...")
                    finally:
                        # 文件传输结束触发信号
                        self.upedSignal.emit()
            else:
                self.upTooltipSignal.emit(u"没有权限读取文件...")
        else:
            self.upTooltipSignal.emit(u"文件不存在...")

        self.tcpSocket.close()


class Download(Process,QtCore.QObject):
    # 定义触发信号
    downingSignal = QtCore.Signal()
    downedSignal = QtCore.Signal()
    downProgressSignal = QtCore.Signal(float)
    downTooltipSignal = QtCore.Signal(str)
    def __init__(self,savePath,filePathDown):
        super(Download,self).__init__()

        self.filePathDown = str(filePathDown)
        self.savePath = savePath

    def run(self):
        # 初始化下载百分比
        perDown = 0
        # 初始化socket
        self.tcpSocket = socket(AF_INET, SOCK_STREAM)
        # 读取服务端信息
        f = open("..\properties\severInfo.json", "r")
        severInfo_str = f.read()
        f.close()
        severInfo_dic = json.loads(severInfo_str)
        self.severAddr = (severInfo_dic["ip"], severInfo_dic["port"])

        try:
            self.tcpSocket.connect(self.severAddr)
        except Exception as e :
            print "连接服务端出错...",e
            self.downTooltipSignal.emit("连接服务端出错,请联系管理员...")
        else:
            try:
                # 通知服务端下载任务
                self.tcpSocket.send(struct.pack("4s","down"))
                self.tcpSocket.send(struct.pack("32s",self.filePathDown)) # 打包文件地址
                fheadSize = struct.calcsize("q")
                fhead = self.tcpSocket.recv(fheadSize)
            except Exception as e:
                print "头文件发送失败...", e
            else:
                if fhead:
                    fileSize = struct.unpack("q",fhead)[0]  # 解包头文件，下载文件大小
                    if fileSize <> 0 :
                        receivedSize = 0  # 接收文件大小
                        self.downingSignal.emit()
                        try:
                            with open(self.savePath, "wb") as fw:
                                self.downTooltipSignal.emit(u"文件下载中...大小 %s M" % (fileSize / 1024 / 1024))
                                while fileSize <> receivedSize:
                                    if fileSize - receivedSize > 1024:
                                        data = self.tcpSocket.recv(1024)
                                        receivedSize += len(data)
                                    else:
                                        data = self.tcpSocket.recv(fileSize - receivedSize)
                                        receivedSize = fileSize
                                        fw.flush()
                                    # 转储至本地文件夹
                                    fw.write(data)
                                    if perDown >= 100:
                                        perDown = 100
                                    else:
                                        perDown += 1024 * 1.0 / fileSize * 100
                                    self.downProgressSignal.emit(perDown)
                        except Exception as e :
                            self.downTooltipSignal.emit(u"文件下载失败,请联系管理员...")
                            # 清除接受的残余文件
                            os.remove(self.savePath)
                        else:
                            self.downTooltipSignal.emit(u"文件下载成功")
                    else:
                        self.downTooltipSignal.emit(u"源文件不存在，请检查下载文件路径是否正确...")

            finally:
                self.downedSignal.emit()

        self.tcpSocket.close()


if __name__ =="__main__":
    import sys

    app = QtGui.QApplication(sys.argv)
    client = Client()
    client.show()
    sys.exit(app.exec_())
