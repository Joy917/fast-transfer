# coding=utf-8

import os
import zipfile
import time


filePath = "D:\\test1.zip"

# if zipfile.is_zipfile(filePath):
#     source = zipfile.ZipFile(filePath)
#     for fileName in source.namelist():
#         print fileName

# 判断是否是文件
if os.path.isfile(filePath):
    # 判断是否可读
    if os.access(filePath,os.R_OK):
        with open(filePath,"rb") as fr:
            copyPath = "D:\\666\\"+filePath.split("\\")[-1]
            with open(copyPath,"wb") as fw:
                fileSize = os.path.getsize(filePath)
                print fileSize
                for data in fr: # 解释器自行读取文件，效率最高
                    fw.write(data)
                # fw.flush()
            copySize = os.path.getsize(copyPath)
            print copySize
            if fileSize == copySize:
                print "上传成功..."
            else:
                print "丢失文件..."
    else:
        print "没有权限读取文件..."
else:
    print "不是文件无法上传"
