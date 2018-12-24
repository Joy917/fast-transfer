# coding:utf-8
import sqlite3
import queue, os


def singleton(cls):
    instances = {}

    def _singleton(*args, **kw):
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
            return instances[cls]

    return _singleton


@singleton
class SQLiteUtil(object):
    __queue_conn = queue.Queue(maxsize=1)
    __path = None

    def __init__(self, path):
        self.__path = path
        print('path:', self.__path)
        self.__create_conn()

    def __create_conn(self):
        conn = sqlite3.connect(self.__path, check_same_thread=False)
        self.__queue_conn.put(conn)

    def __close(self, cursor, conn):
        if cursor is not None:
            cursor.close()
        if conn is not None:
            cursor.close()
        self.__create_conn()




# example:

one = SQLiteUtil('xxx.sqlite') 

rst = one.execute_query('select * from website', None) 
for line in rst: 
    print(line.get('id'), line.get('url'), line.get('content'))


print(one.execute_update('update website set content = \'2222222\' where id = ?', ('1',))) 
print(one.execute_update('update website set content = \'2222222\' where id = \'1\'', None)) 


print('update many') 
count = one.execute_update_many( 
[
'update website set content = \'一\' where id = \'1\'', 
'update website set content = \'二\' where id = \'2\'', 
'update website set content = 1 where id = \'3\'' 
], 
[None, None, None] 
) 
print('count:', count) 
