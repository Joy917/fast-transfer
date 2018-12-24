# coding=utf-8

from distutils.core import setup
import py2exe
from glob import glob
import os

options = {"py2exe": {  "compressed": 1,
                        "optimize": 0,
                        "ascii": 0,
                        "bundle_files": 2,# 参数1不支持64位
                        'dist_dir': "D:/666",
                        "includes":["sip"],
                    }
                }

path = os.getcwd()
datafiles = [
        ("imgs", glob(path + r'/imgs/*.*')),
        ("conf", glob(path + r'/conf/*.*')),
]

datafiles.append(('imageformats', [
                r'C:\Python27\Lib\site-packages\PySide\plugins\imageformats\qjpeg4.dll'
                ]))

setup(options = options,
      data_files = datafiles,
      zipfile=None,
      console = [{"script":r'D:\SVN\Python\ftp\src\client_ft.py'}]
    )

# C:\Python27\python.exe D:\SVN\Python\ftp\src\setup.py py2exe