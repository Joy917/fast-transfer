# coding=utf-8

from socket import *
import struct, os, logging
import threading
import sqlite3
from PySide import QtGui, QtCore
import _sever_qt4
import time


class Sever(QtGui.QWidget, _sever_qt4.Ui_Form):
    def __init__(self):
        super(Sever, self).__init__()
        self.setupUi(self)
        self.__modifyUI()

        # 用户操作日志
        self.logger_user = self.__getLogger("User")
        # 软件运行日志
        self.logger_app = self.__getLogger("App")

        self.__setUp()

    # 微调界面UI格式以及输入规则
    def __modifyUI(self):
        # IP正则
        validatorIP = QtGui.QRegExpValidator(QtCore.QRegExp(
            "^(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|[1-9])\."
            + "(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\."
            + "(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\."
            + "(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)$"))
        self.lineEdit_ip.setValidator(validatorIP)

        # IP以及模糊查询格式
        self.lineEdit_ip.setAlignment(QtCore.Qt.AlignHCenter)
        self.lineEdit_fuzzysearch.setAlignment(QtCore.Qt.AlignHCenter)

        # 页码输入正则
        self.lineEdit_pagenumStart.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("^[0-9]+$")))
        self.lineEdit_pagenumEnd.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("^[0-9]+$")))

        # 提示信息格式
        self.label_notice.setStyleSheet("color:rgba(255,0,0,150)")

        self.dateTimeEdit_start.setDisplayFormat("yyyy/MM/dd HH:mm:ss")
        self.dateTimeEdit_end.setDisplayFormat("yyyy/MM/dd HH:mm:ss")

    # 根据输入日志名返回日志实例
    def __getLogger(self, name):
        # 操作频繁可以根据日期命名日志，避免单个日志文件过大
        date = time.strftime("%Y-%m-%d", time.localtime())
        # 获取日志实例
        logger = logging.getLogger(name)
        # 日志打印内容格式
        fmt = logging.Formatter("%(asctime)s [%(levelname)s] [%(name)s]: %(message)s\n", datefmt="%Y-%m-%d %H:%M:%S")
        # 输出格式及日志文件位置
        file_handler = logging.FileHandler("{0}_{1}.log".format(date, name))
        file_handler.setFormatter(fmt)
        # 配置日志实例
        logger.addHandler(file_handler)
        logger.setLevel(logging.INFO)
        return logger

    # 主方法
    def __setUp(self):
        self.__listenUI()
        self.__createDB()

        # 开启线程监听客户端连接
        threading._start_new_thread(self.__listenClient, ())

        # 连接数据库获取展示数据
        self.page = 0
        content = ""
        with sqlite3.connect(DB_NAME) as conn:
            conn.text_factory = str
            try:
                for row in conn.execute(" select content from log limit ?,?; ", self.__pageRange(self.page)):
                    content += row[0] + "\n\n"
            except Exception as e:
                raise e
            else:
                self.textBrowser_log.setText(content.decode("utf-8"))

    # 初始化数据库
    def __createDB(self):
        # 当前路径不存在数据库文件则创建
        if not os.path.isfile(DB_NAME):
            with sqlite3.connect(DB_NAME) as conn:
                try:
                    # 创建日志表
                    conn.execute(
                        " create table log( "
                        " id INTEGER primary key, "
                        " time TEXT(100) not null, "
                        " IP TEXT(15) not null, "
                        " content TEXT(200) not null"
                        ");"
                    )
                except Exception as e:
                    conn.rollback()
                    raise e
                else:
                    conn.commit()
                    self.logger_app.critical("日志数据库: logManager.db 初始化成功!")

    # 监听界面触发事件
    def __listenUI(self):

        self.pushButton_pageup.clicked.connect(lambda: self.__changePage(-1))
        self.pushButton_pagedown.clicked.connect(lambda: self.__changePage(1))
        self.pushButton_check.clicked.connect(self.__checkLog)

    # 查询日志
    def __checkLog(self):
        # 根据勾选初始化对应判断标识
        time_flag = 0
        ip_flag = 0
        fuzzy_flag = 0

        # 初始化变量,避免查询SQL语法错误
        start_time = ""
        end_time = ""
        ip = ""
        fuzzy = ""

        # 判断是否被勾选
        if self.checkBox_time.isChecked():  # 时间条件
            start_time = str(self.dateTimeEdit_start.text())
            end_time = str(self.dateTimeEdit_end.text())
            time_flag = 1
        if self.checkBox_ip.isChecked() and self.lineEdit_ip.text().strip() != "":  # IP条件
            ip = str(self.lineEdit_ip.text())
            ip_flag = 1
        if self.checkBox_fuzzy.isChecked() and self.lineEdit_fuzzysearch.text().strip() != "":  # 模糊查询
            fuzzy = str(self.lineEdit_fuzzysearch.text())
            fuzzy_flag = 1

        # 8种勾选情况对应SQL
        # 条件改变,重新获取日志内容
        content = ""
        if time_flag == 0 and ip_flag == 0 and fuzzy_flag == 0:  # 没有勾选额外查询条件
            with sqlite3.connect(DB_NAME) as conn:
                conn.text_factory = str
                try:
                    for row in conn.execute(" select content from log limit ?,? ;", self.__pageRange(self.page)):
                        content += row[0] + "\n\n"
                except Exception as e:
                    raise e
        if time_flag == 1 and ip_flag == 0 and fuzzy_flag == 0:  # 仅勾选时间
            with sqlite3.connect(DB_NAME) as conn:
                conn.text_factory = str
                try:
                    for row in conn.execute(" select content from log where time between ? and ? limit ?,? ;",
                                            (start_time, end_time, self.__pageRange(self.page)[0],
                                             self.__pageRange(self.page)[1])):
                        content += row[0] + "\n\n"
                except Exception as e:
                    raise e
        if time_flag == 0 and ip_flag == 1 and fuzzy_flag == 0:  # 仅勾选IP
            with sqlite3.connect(DB_NAME) as conn:
                conn.text_factory = str
                try:
                    for row in conn.execute(" select content from log where ip = ? limit ?,? ;",
                                            (ip, self.__pageRange(self.page)[0], self.__pageRange(self.page)[1])):
                        content += row[0] + "\n\n"
                except Exception as e:
                    raise e
        if time_flag == 0 and ip_flag == 0 and fuzzy_flag == 1:  # 仅勾选模糊查询
            with sqlite3.connect(DB_NAME) as conn:
                conn.text_factory = str
                try:
                    for row in conn.execute(" select content from log where content like ? limit ?,? ;",
                                            ("%" + fuzzy + "%", self.__pageRange(self.page)[0],
                                             self.__pageRange(self.page)[1])):
                        content += row[0] + "\n\n"
                except Exception as e:
                    raise e
        if time_flag == 1 and ip_flag == 1 and fuzzy_flag == 0:  # 勾选时间、IP
            with sqlite3.connect(DB_NAME) as conn:
                conn.text_factory = str
                try:
                    for row in conn.execute(
                            " select content from log where ip = ? and time between ? and ? limit ?,? ;",
                            (ip, start_time, end_time, self.__pageRange(self.page)[0], self.__pageRange(self.page)[1])):
                        content += row[0] + "\n\n"
                except Exception as e:
                    raise e
        if time_flag == 0 and ip_flag == 1 and fuzzy_flag == 1:  # 勾选IP、模糊查询
            with sqlite3.connect(DB_NAME) as conn:
                conn.text_factory = str
                try:
                    for row in conn.execute(" select content from log where ip = ? and content like ? limit ?,? ;",
                                            (ip, "%" + fuzzy + "%", self.__pageRange(self.page)[0],
                                             self.__pageRange(self.page)[1])):
                        content += row[0] + "\n\n"
                except Exception as e:
                    raise e
        if time_flag == 1 and ip_flag == 0 and fuzzy_flag == 1:  # 勾选时间、模糊查询
            with sqlite3.connect(DB_NAME) as conn:
                conn.text_factory = str
                try:
                    for row in conn.execute(
                            " select content from log where time between ? and ? and content like ? limit ?,? ;",
                            (start_time, end_time, "%" + fuzzy + "%", self.__pageRange(self.page)[0],
                             self.__pageRange(self.page)[1])):
                        content += row[0] + "\n\n"
                except Exception as e:
                    raise e
        if time_flag == 1 and ip_flag == 1 and fuzzy_flag == 1:  # 勾选时间、IP、模糊查询
            print start_time,end_time,ip,fuzzy,self.__pageRange(self.page)[0]
            print type(start_time),end_time,type(ip),type(fuzzy),type(self.__pageRange(self.page)[0])

            with sqlite3.connect(DB_NAME) as conn:
                conn.text_factory = str
                try:
                    for row in conn.execute(
                            " select content from log where ip = ? and time between ? and ? and content like ? limit ?,? ;",
                            (ip, start_time, end_time, "%" + fuzzy + "%", self.__pageRange(self.page)[0],
                             self.__pageRange(self.page)[1])):
                        content += row[0] + "\n\n"
                except Exception as e:
                    raise e

        self.textBrowser_log.setText(content.decode("utf-8"))

    # 设置页码
    def __changePage(self, count):
        if count == 1:
            self.page += 1
        if count == -1:
            self.page -= 1
        if self.page < 0:
            self.page = 0

        # 根据勾选初始化对应标识
        time_flag = 0
        ip_flag = 0
        fuzzy_flag = 0

        # 初始化变量,避免查询SQL错误
        start_time = ""
        end_time = ""
        ip = ""
        fuzzy = ""

        # 判断是否被勾选
        if self.checkBox_time.isChecked():  # 时间条件
            start_time = str(self.dateTimeEdit_start.text())
            end_time = str(self.dateTimeEdit_end.text())
            time_flag = 1
        if self.checkBox_ip.isChecked() and self.lineEdit_ip.text().strip() != "":  # IP条件
            ip = str(self.lineEdit_ip.text())
            ip_flag = 1
        if self.checkBox_fuzzy.isChecked() and self.lineEdit_fuzzysearch.text().strip() != "":  # 模糊查询
            fuzzy = str(self.lineEdit_fuzzysearch.text())
            fuzzy_flag = 1

        # 8种勾选情况对应SQL
        # 条件改变,重新获取日志内容
        content = ""
        if time_flag == 0 and ip_flag == 0 and fuzzy_flag == 0:  # 没有勾选额外查询条件
            with sqlite3.connect(DB_NAME) as conn:
                conn.text_factory = str
                try:
                    for row in conn.execute(" select content from log limit ?,? ;", self.__pageRange(self.page)):
                        content += row[0] + "\n\n"
                except Exception as e:
                    raise e
        if time_flag == 1 and ip_flag == 0 and fuzzy_flag == 0:  # 仅勾选时间
            with sqlite3.connect(DB_NAME) as conn:
                conn.text_factory = str
                try:
                    for row in conn.execute(" select content from log where time between ? and ? limit ?,? ;",
                                            (start_time, end_time, self.__pageRange(self.page)[0],
                                             self.__pageRange(self.page)[1])):
                        content += row[0] + "\n\n"
                except Exception as e:
                    raise e
        if time_flag == 0 and ip_flag == 1 and fuzzy_flag == 0:  # 仅勾选IP
            with sqlite3.connect(DB_NAME) as conn:
                conn.text_factory = str
                try:
                    for row in conn.execute(" select content from log where ip = ? limit ?,? ;",
                                            (ip, self.__pageRange(self.page)[0], self.__pageRange(self.page)[1])):
                        content += row[0] + "\n\n"
                except Exception as e:
                    raise e
        if time_flag == 0 and ip_flag == 0 and fuzzy_flag == 1:  # 仅勾选模糊查询
            with sqlite3.connect(DB_NAME) as conn:
                conn.text_factory = str
                try:
                    for row in conn.execute(" select content from log where content like ? limit ?,? ;",
                                            ("%" + fuzzy + "%", self.__pageRange(self.page)[0],
                                             self.__pageRange(self.page)[1])):
                        content += row[0] + "\n\n"
                except Exception as e:
                    raise e
        if time_flag == 1 and ip_flag == 1 and fuzzy_flag == 0:  # 勾选时间、IP
            with sqlite3.connect(DB_NAME) as conn:
                conn.text_factory = str
                try:
                    for row in conn.execute(
                            " select content from log where ip = ? and time between ? and ? limit ?,? ;",
                            (ip, start_time, end_time, self.__pageRange(self.page)[0], self.__pageRange(self.page)[1])):
                        content += row[0] + "\n\n"
                except Exception as e:
                    raise e
        if time_flag == 0 and ip_flag == 1 and fuzzy_flag == 1:  # 勾选IP、模糊查询
            with sqlite3.connect(DB_NAME) as conn:
                conn.text_factory = str
                try:
                    for row in conn.execute(" select content from log where ip = ? and content like ? limit ?,? ;",
                                            (ip, "%" + fuzzy + "%", self.__pageRange(self.page)[0],
                                             self.__pageRange(self.page)[1])):
                        content += row[0] + "\n\n"
                except Exception as e:
                    raise e
        if time_flag == 1 and ip_flag == 0 and fuzzy_flag == 1:  # 勾选时间、模糊查询
            with sqlite3.connect(DB_NAME) as conn:
                conn.text_factory = str
                try:
                    for row in conn.execute(
                            " select content from log where time between ? and ? and content like ? limit ?,? ;",
                            (start_time, end_time, "%" + fuzzy + "%", self.__pageRange(self.page)[0],
                             self.__pageRange(self.page)[1])):
                        content += row[0] + "\n\n"
                except Exception as e:
                    raise e
        if time_flag == 1 and ip_flag == 1 and fuzzy_flag == 1:  # 勾选时间、IP、模糊查询
            print start_time, end_time, ip, fuzzy, self.__pageRange(self.page)[0]
            print type(start_time), end_time, type(ip), type(fuzzy), type(self.__pageRange(self.page)[0])

            with sqlite3.connect(DB_NAME) as conn:
                conn.text_factory = str
                try:
                    for row in conn.execute(
                            " select content from log where ip = ? and time between ? and ? and content like ? limit ?,? ;",
                            (ip, start_time, end_time, "%" + fuzzy + "%", self.__pageRange(self.page)[0],
                             self.__pageRange(self.page)[1])):
                        content += row[0] + "\n\n"
                except Exception as e:
                    raise e

        self.textBrowser_log.setText(content.decode("utf-8"))

    # 根据页数返回页码范围列表
    def __pageRange(self, page):
        numStart = self.lineEdit_pagenumStart.text()
        numEnd = self.lineEdit_pagenumEnd.text()
        numRange = 0
        if numStart and numEnd:
            numRange = int(numEnd) - int(numStart) + 1
        if numRange < 0:
            self.label_notice.setText(u"输入页码不合法,请检查!")
            numRange = 0

        # 更新页码
        self.lineEdit_pagenumStart.setText(u"{}".format(1 + numRange * page))
        self.lineEdit_pagenumEnd.setText(u"{}".format(20 + numRange * page))
        # 返回字符串类型的页码列表
        pageRange = [(0 + numRange * page), (20 + numRange * page)]
        return pageRange

    # 监听客户端
    def __listenClient(self):
        # 服务端初始化
        tcpSocket = socket(AF_INET, SOCK_STREAM)
        tcpSocket.bind(("", 12306))
        tcpSocket.listen(50)
        while 1:
            newSocket, clientAddr = tcpSocket.accept()
            taskSize = struct.calcsize("4s")  # 任务长度
            task = struct.unpack("4s", newSocket.recv(taskSize))[0].strip("\0")  # 解包,任务名,去除末尾补齐的字符位
            if "up" == task:  # 上传任务
                self.upLoad = UpLoad(newSocket, clientAddr, self.logger_app, self.logger_user)
                self.upLoad.start()
            if "down" == task:  # 下载任务
                self.downLoad = DownLoad(newSocket, clientAddr, self.logger_app, self.logger_user)
                self.downLoad.start()


# 负责上传模块
class UpLoad(threading.Thread):
    def __init__(self, newSocket, clientAddr, logger_app, logger_user):
        super(UpLoad, self).__init__()
        self.newSocket = newSocket
        self.clientAddr = clientAddr
        self.logger_app = logger_app
        self.logger_user = logger_user

    def run(self):
        # 初始化每次数据传输大小
        global DATA_SIZE

        fheadSize = struct.calcsize("128s128sq")
        try:
            self.newSocket.settimeout(300)
        except Exception as e:
            self.logger_app.error(u"上传时客户端连接超时...{}".format(e))
        else:
            try:
                fhead = self.newSocket.recv(fheadSize)
                if fhead:
                    filePath, dirPath, fileSize = struct.unpack("128s128sq", fhead)  # 解包头文件
                    filePath = filePath.strip("\0")
                    dirPath = dirPath.strip("\0")
                    # 路径格式纠错
                    if dirPath.endswith("\\"):
                        dirPath = dirPath.strip("\\")
                    elif dirPath.endswith("/"):
                        dirPath = dirPath.strip("/")
                    else:
                        pass
                    fileName = os.path.basename(filePath)
                    savePath = u"{}".format(dirPath + "/" + fileName)
                    if os.path.isfile(savePath):  # 如果存在该文件，删除原文件
                        self.logger_app.info(u"上传时删除已存在的旧文件...")
                        os.remove(savePath)
                        dirName = dirPath + "/"
                    else:  # 不存在文件创建给定的文件夹
                        dirName = os.path.dirname(savePath)
                        if not os.path.isdir(dirName):  # 不存在该文件夹则创建
                            os.makedirs(dirName)
                    try:
                        with open(savePath, "wb") as fw:
                            receivedSize = 0  # 接收文件大小
                            while fileSize <> receivedSize:
                                data = self.newSocket.recv(DATA_SIZE)
                                receivedSize += len(data)
                                fw.write(data)
                            fw.flush()
                            os.fsync(fw)

                        # 接受完成发送反馈
                        endMessage = struct.pack("2s", "ok")
                        self.newSocket.send(endMessage)

                        # 用户操作数据插入数据库
                        ip, port = self.clientAddr
                        currentTime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
                        content = "{} 来自:{} 上传文件:{}, 文件夹路径:{}".format(currentTime, self.clientAddr, fileName, dirName)
                        with sqlite3.connect("logManager.db") as conn:
                            conn.text_factory = str
                            try:
                                conn.execute(" insert into log(time, IP, content) values(?,?,?)", (currentTime, ip, content))
                            except Exception as e:
                                conn.rollback()
                                raise e
                            else:
                                conn.commit()
                                self.logger_app.info(u"上传信息插入数据库成功!")
                                self.logger_user.info(u"{} 上传文件: {} ,文件夹路径: {}".format(self.clientAddr, fileName, dirName))
                    except Exception as e:
                        if os.path.isfile(savePath):
                            self.logger_app.error(u"上传时删除失败残留文件...{}".format(e))
                            os.remove(savePath)
                        else:
                            self.logger_app.error(u"上传时删除失败残留文件...{}".format(e))
            except Exception as e:
                self.logger_app.error(u"文件上传失败...{}".format(e))


# 负责下载模块
class DownLoad(threading.Thread):
    def __init__(self, newSocket, clientAddr, logger_app, logger_user):
        super(DownLoad, self).__init__()

        self.newSocket = newSocket
        self.clientAddr = clientAddr
        self.logger_app = logger_app
        self.logger_user = logger_user

    def run(self):
        # 初始化每次数据传输大小
        global DATA_SIZE

        fheadSize = struct.calcsize("128s")
        try:
            self.newSocket.settimeout(300)
        except Exception as e:
            self.logger_app.error(u"下载时客户端连接超时...{}".format(e))
        else:
            # 获取文件头
            fhead = self.newSocket.recv(fheadSize)
            if fhead:
                filePathDown = struct.unpack("128s", fhead)[0].strip("\0")  # 解包头文件
                filePathDown = u"{}".format(filePathDown)
                fileName = os.path.basename(filePathDown)
                dirName = os.path.dirname(filePathDown)
                if os.path.isfile(filePathDown):
                    # 判断是否可读
                    if os.access(filePathDown, os.R_OK):
                        with open(filePathDown, "rb") as fr:
                            fileSize = os.path.getsize(filePathDown)
                            try:
                                # 定义文件头信息:文件大小
                                fileHead = struct.pack("q", fileSize)
                                self.newSocket.send(fileHead)
                                sendedSize = 0
                                while sendedSize <> fileSize:
                                    if fileSize - sendedSize > DATA_SIZE:
                                        data = fr.read(DATA_SIZE)
                                    else:
                                        data = fr.read(fileSize - sendedSize)
                                    sendedSize += len(data)
                                    self.newSocket.send(data)

                                # 等待结束反馈
                                endSize = struct.calcsize("2s")
                                end = self.newSocket.recv(endSize)
                                if end:
                                    endFlag = struct.unpack("2s", end)[0].strip("\0")  # 解包,任务名,去除末尾补齐的字符位
                                    if not "ok" == endFlag:
                                        self.logger_app.error(u"下载时文件尾部接受错误")
                            except Exception as e:
                                self.logger_app.error(u"下载时发送数据至客户端出错...{}".format(e))

                        # 用户操作数据插入数据库
                        ip, port = self.clientAddr
                        currentTime = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
                        content = "{} 来自:{} 上传文件:{}, 文件夹路径:{}".format(currentTime, self.clientAddr, fileName, dirName)
                        with sqlite3.connect("logManager.db") as conn:
                            conn.text_factory = str
                            try:
                                conn.execute(" insert into log( time, IP, content) values(?,?,?)", (currentTime, ip, content))
                            except Exception as e:
                                conn.rollback()
                                raise e
                            else:
                                conn.commit()
                                self.logger_app.info(u"插入数据库成功!")
                                self.logger_user.info(u"{} 下载文件: {} ,服务端文件路径: {}".format(self.clientAddr, fileName, dirName))
                    else:
                        self.logger_app.error(u"下载时服务端没有权限读取文件...")
                else:
                    self.logger_app.error(u"下载时服务端找不到对应文件...")
                    fileHead = struct.pack("q", 0)
                    self.newSocket.send(fileHead)


if __name__ == "__main__":
    import sys

    DATA_SIZE = 1024 * 100
    DB_NAME = "logManager.db"

    app = QtGui.QApplication(sys.argv)
    sever = Sever()
    sever.show()
    sys.exit(app.exec_())
