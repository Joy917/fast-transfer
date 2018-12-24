# coding=utf-8
import sqlite3

"""
简化SQLite操作框架
        ——— by Joy
"""


class DB:
    def __init__(self, dbname):
        if type(dbname) is str and dbname.endswith(".db"):
            self.__db = sqlite3.connect(dbname)
            self.__cursor = self.__db.cursor()
        else:
            self.__db = None
            self.__cursor = None

    # 支持 with as 语法
    def __enter__(self):
        print " start"
        if self.__cursor is None:
            print "数据库名不合法!"
            return None
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.__cursor:
            self.__cursor.close()
            self.__db.close()

        print "end"

    """基础工具方法"""

    def __is_empty(self, s):  # 返回有效字符串
        if type(s) == str:
            return s and s.strip()
        else:
            return False

    """对外接口,处理输入的sql语句，并分发给对应私有处理方法"""

    def sql(self, sql):
        sql_strip = sql.lstrip()
        if type(sql) is not str:
            return False
        elif sql_strip.startswith("create"):
            self.__create(sql)
        elif sql_strip.startswith("insert"):
            self.__insert(sql)
        elif sql_strip.startswith("select"):
            self.__select(sql)
        elif sql_strip.startswith("update"):
            self.__update(sql)
        elif sql_strip.startswith("delete"):
            self.__delete(sql)
        elif sql_strip.startswith("drop"):
            self.__drop(sql)

    """分发SQL处理方法"""

    def __create(self, sql):
        try:
            self.__cursor.execute(sql)
        except Exception as e:
            print "sql语句执行错误,请检查...", e
        else:
            self.__db.commit()

    def __insert(self, sql):
        try:
            self.__cursor.execute(sql)
        except Exception as e:
            print "sql语句执行错误,请检查...", e
        else:
            self.__db.commit()

    def __select(self, sql):
        try:
            self.__cursor.execute(sql)
        except Exception as e:
            print "sql语句执行错误,请检查...", e
        else:
            # SQL语句清洗,取出查询字段
            columnList = sql2.rpartition("from")[0].split(" ")
            colstr = list(filter(self.__is_empty, columnList))[-1]  # 获取的查询字段
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

    def __update(self, sql):
        try:
            self.__cursor.execute(sql)
        except Exception as e:
            print "sql语句执行错误,请检查...", e
        else:
            self.__db.commit()

    def __delete(self, sql):
        pass

    def __drop(self, sql):
        pass


"""测试SQL语句"""
sql1 = "create table user (id int(20) primary key,name varchar(200) not null)"

sql2 = "insert into user (id,name) values (1,\"傻居居\");" \
       "insert into user (id,name) values (2,\"小毕气\");" \
       "insert into user (id,name) values (3,\"小胖几\");"

sql3 = "drop table user"

with DB("dbtest.db") as db:
    db.sql(sql1)
