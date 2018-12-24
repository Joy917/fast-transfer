# coding=utf-8

# t = "((18,))"
# t1 = str(tuple(eval(t))[0])
# print t1
# print type(t1)



sql1 = "select * from table "
sql2 = " select distinct t1,t2,t3 from table where t1==2"

try:
    self.__cursor.execute(sql2)
except Exception as e:
    print "sql语句执行错误,请检查...",e
else:
    # SQL语句清洗,取出查询字段
    def is_empty(s):
        if type(s) == str:
            return s and s.strip()
        else:
            return False
    columnList = sql2.rpartition("from")[0].split(" ")
    colstr = list(filter(is_empty, columnList))[-1] # 获取的查询字段
    print colstr

    try:
        if "*" == columnList:
            pass
        else:
            col_list = []
            for column in columnList.split(","):
                col_list.append(column)

            list_len = col_list.__len__()
            for col in self.__cursor.fetchall():
                print col[col_list.index()]
    except Exception as e:
        print e, "返回查询结果出错..."
