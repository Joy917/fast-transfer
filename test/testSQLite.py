# coding=utf-8

import sqlite3

with sqlite3.connect(":memory:") as conn:
    conn.text_factory = str  # 此处是关键,sqlite默认文本存取是Unicode
    try:
        init_sql = " create table test (id integer primary key ,name text(200) not null ,time text not null);" \
                   " insert into test (name,time) values ('小居居','2017/1/1 16:08:09');" \
                   " insert into test (name,time) values ('大居居','2018/1/1 19:09:18');"
        conn.executescript(init_sql)
    except Exception as e:
        conn.rollback()
        raise e
    else:
        conn.commit()
        try:
            for row in conn.execute(" select * from test where time between ? and ? limit 0,2", ("2017/1/1 0:00:00","2018/1/1 0:00:00")):
                print row[0],row[1],row[2], type(row[2])
        except Exception as e:
            raise e


# with sqlite3.connect("../src/logManager.db") as conn:
#     try:
#         for row in conn.execute(" select content from log where time between ? and ? limit 1,2",("2017/1/1", "2018/5/1")):
#             print row[0]
#     except Exception as e:
#         raise e
