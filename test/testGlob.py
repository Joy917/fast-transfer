from glob import glob


dirPath = r"D:\SVN\Python\ftp\src"
for g in glob(dirPath+r"\*.py"):
    print g

#  只能匹配当前路径
