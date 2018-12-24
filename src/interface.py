# coding=utf-8

from socket import *
import struct,os,json
import logging,re
import threading
import time


# 全局传输数据大小
DATA_SIZE = 1024 * 100
class Interface():
    def __init__(self):

        # 软件运行日志
        self.__logger_interface = self.__getLogger("Interface")

        # 传输进度百分比初始化
        self.perUp = 0
        self.perDown = 0

    # 根据输入日志名返回日志实例
    def __getLogger(self, name):
        # 操作频繁可以根据日期命名日志，避免单个日志文件过大
        date = time.strftime("%Y-%m-%d", time.localtime())
        # 获取日志实例
        logger = logging.getLogger(name)
        # 日志打印内容格式
        fmt = logging.Formatter("%(asctime)s [%(levelname)s] [%(name)s]: %(message)s\n",
                                datefmt="%Y-%m-%d %H:%M:%S")
        # 输出格式及日志文件位置
        file_handler = logging.FileHandler("{0}_{1}.log".format(date, name))
        file_handler.setFormatter(fmt)
        # 配置日志实例
        logger.addHandler(file_handler)
        logger.setLevel(logging.INFO)
        return logger

    # 文件上传接口
    # 输入参数：文件上传路径、保存文件夹名，没有则在服务端创建
    def upLoad(self, filePathUp, dirPath):
        # 校验给定的文件路径
        if "" == filePathUp.strip() or filePathUp is None:
            self.__logger_interface.info(u"上传时文件路径为空...")
            return False
        # 正则匹配磁盘名
        p = re.match(r"[a-zA-Z]:[/\\]", str(dirPath))
        if not p:
            return False
        filePathUp = u"{}".format(str(filePathUp))
        dirPath = u"{}".format(str(dirPath))
        if os.path.isfile(filePathUp):  # 没有异常，开启线程处理任务
            threading._start_new_thread(self.__upThread,(filePathUp,dirPath))
            return True
        else:
            self.__logger_interface.info(u"不存在该文件...")
        return False

    # 文件下载接口
    # 输入参数：服务端文件所在路径，本地文件夹路径
    def downLoad(self, filePath_down, dirPath):
        # 正则匹配磁盘名
        p = re.match(r"[a-zA-Z]:[/\\]", str(dirPath))
        if not p:
            self.__logger_interface.info(u"下载时文件夹路径不合法...")
            return False
        filePath_down = u"{}".format(str(filePath_down))
        # 路径格式纠错
        if dirPath.endswith("\\"):
            dirPath = dirPath.strip("\\")
        elif dirPath.endswith("/"):
            dirPath = dirPath.strip("/")
        # 转储至本地文件夹
        fileName = os.path.basename(filePath_down)
        savePath = u"{}".format(str(dirPath) + "\\" + fileName)
        if not os.path.isdir(dirPath):
            self.__logger_interface.info(u"下载时本地文件夹不存在...")
            return False
        if os.path.isfile(savePath):
            self.__logger_interface.info(u"下载时存在同名文件...请更换保存文件夹")
            return False
        else:  # 没有异常，开启线程处理任务
            threading._start_new_thread(self.__downThread,(filePath_down, savePath))
            return True

        return False

    def __upThread(self, filePathUp, dirPath):
        global DATA_SIZE
        self.perUp = 0
        # 初始化socket
        tcpSocket = socket(AF_INET, SOCK_STREAM)
        # 读取服务端信息
        root_path = os.getcwd()
        # 读取文件，获取服务端地址
        with open(root_path + "/config/severInfo.json", "r") as f:
            severInfo_str = f.read()
            severInfo_dic = json.loads(severInfo_str)
            severAddr = (severInfo_dic["ip"], severInfo_dic["port"])
        if os.path.isfile(filePathUp):
            # 判断是否可读
            if os.access(filePathUp, os.R_OK):
                with open(filePathUp, "rb") as fr:
                    fileSize = os.path.getsize(filePathUp)
                    self.__logger_interface.info(u"文件上传中...大小 {} M,路径{}".format((fileSize / 1024 / 1024), filePathUp))
                    try:
                        # 连接服务端
                        tcpSocket.connect(severAddr)
                    except Exception as e:
                        self.__logger_interface.error(u"上传时连接服务器失败,请稍后重试...{}".format(e))
                    else:
                        try:
                            # 通知服务端上传任务
                            task = struct.pack("4s", "up")
                            tcpSocket.send(task)
                            # 定义文件头信息，包含文件名及文件大小
                            fileHead = struct.pack("128s128sq", str(filePathUp),str(dirPath), fileSize)  # struct打包
                            tcpSocket.send(fileHead)
                            # 已发送数据
                            sendedSize = 0
                            while fileSize <> sendedSize:
                                if fileSize - sendedSize > DATA_SIZE:
                                    data = fr.read(DATA_SIZE)
                                    self.perUp += DATA_SIZE * 1.0 / fileSize * 100
                                else:
                                    data = fr.read(fileSize - sendedSize)
                                    self.perUp = 100
                                sendedSize += len(data)
                                tcpSocket.sendall(data)

                            endSize = struct.calcsize("2s")
                            # 等待结束反馈
                            end = tcpSocket.recv(endSize)
                            if end:
                                endFlag = struct.unpack("2s", end)[0].strip("\0")  # 解包,任务名,去除末尾补齐的字符位
                                if not "ok" == endFlag:
                                    raise Exception(u"文件尾部接受错误")
                        except Exception as e:
                            self.__logger_interface.error(u"上传时发送数据出错...请稍后重试{}".format(e))
                        else:
                            self.__logger_interface.info(u"上传成功...")
            else:
                self.__logger_interface.info(u"上传时没有权限读取文件...")
        else:
            self.__logger_interface.info(u"上传时找不到文件...")

        tcpSocket.close()

    def __downThread(self,filePath_down , savePath):
        global DATA_SIZE
        self.perDown = 0
        # 初始化socket
        tcpSocket = socket(AF_INET, SOCK_STREAM)
        # 读取服务端信息
        root_path = os.getcwd()
        with open(root_path + "/config/severInfo.json", "r") as f:
            severInfo_str = f.read()
            severInfo_dic = json.loads(severInfo_str)
            severAddr = (severInfo_dic["ip"], severInfo_dic["port"])
        try:
            tcpSocket.connect(severAddr)
        except Exception as e:
            self.__logger_interface.exception(u"下载时连接服务端出错...{}".format(e))
        else:
            try:
                # 通知服务端下载任务
                tcpSocket.send(struct.pack("4s", "down"))
                tcpSocket.send(struct.pack("128s", str(filePath_down)))  # 打包文件地址
                fheadSize = struct.calcsize("q")
                fhead = tcpSocket.recv(fheadSize)
            except Exception as e:
                self.__logger_interface.exception(u"下载时头文件发送失败...{}".format(e))
            else:
                if fhead:
                    fileSize = struct.unpack("q", fhead)[0]  # 解包头文件，下载文件大小
                    if fileSize <> 0:
                        try:
                            with open(savePath, "wb") as fw:
                                self.__logger_interface.info(u"文件下载中...大小 {} M".format(fileSize / 1024 / 1024))
                                receivedSize = 0  # 接收文件大小
                                while fileSize <> receivedSize:
                                    data = tcpSocket.recv(DATA_SIZE)
                                    receivedSize += len(data)
                                    self.perDown += DATA_SIZE * 1.0 / fileSize * 100
                                    if self.perDown >= 100:
                                        self.perDown = 100
                                    # 转储至本地文件夹
                                    fw.write(data)
                                fw.flush()
                                os.fsync(fw)

                                # 接受完成发送反馈
                                endMessage = struct.pack("2s", "ok")
                                tcpSocket.send(endMessage)
                        except Exception as e:
                            self.__logger_interface.exception(u"文件下载失败...{}".format(e))
                            # 清除接受的残余文件
                            os.remove(savePath)
                        else:
                            self.__logger_interface.info(u"文件下载成功")
                    else:
                        self.__logger_interface.error(u"源文件不存在，请检查下载文件路径是否正确...")

        tcpSocket.close()


if __name__ =="__main__":

    interface = Interface()
