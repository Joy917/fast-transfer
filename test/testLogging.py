# coding=utf-8

import logging,time,os


# 获取日志实例方法
def getLogger(name):
    # 操作频繁可以根据日期命名日志，避免单个日志文件过大
    date = time.strftime("%Y-%m-%d", time.localtime())
    # 获取日志实例
    logger = logging.getLogger(name)
    # 日志打印内容格式
    fmt = logging.Formatter("%(asctime)s [%(levelname)s] [%(name)s]: %(message)s\n", datefmt="%Y-%m-%d %H:%M:%S")
    # 输出格式及日志文件位置
    path = os.getcwd()
    file_handler = logging.FileHandler(r"{}/log/{}_{}.log".format(path,date,name))
    file_handler.setFormatter(fmt)
    # 配置日志实例
    logger.addHandler(file_handler)
    logger.setLevel(logging.INFO)
    return logger


logger = getLogger("Test")
logger.info("这是一条测试信息")