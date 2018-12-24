# coding=utf-8
import re

# # 路径格式纠错
# dirPath = "D:\\test\\"
#
# if dirPath.endswith("\\") :
#     dirPath = dirPath.strip("\\")
# elif dirPath.endswith("/"):
#     dirPath = dirPath.strip("/")
# else:
#     pass
#
# print dirPath

# 正则匹配
p =  re.match(r"[a-zA-Z]:[/\\]","e:|daw\\sadf")
if p:
    print True
else:
    print False
