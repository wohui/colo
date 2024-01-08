# -*- encoding: utf-8 -*-
'''

'''

import psycopg2
from psycopg2 import sql
class PgsqlHandle(object):
    ''' 定义一个 Postgres SQL 操作类'''

    def __init__(self, host, username, password, database=None, port=5432):
        '''初始化数据库信息并创建数据库连接'''
        # 下面的赋值其实可以省略，connect 时 直接使用形参即可
        self.host = host
        self.username = username
        self.password = password
        self.database = database
        self.port = port

    def create_database(self,database_name):
        conn = psycopg2.connect(host=self.host,user=self.username, password=self.password)
        cursor = conn.cursor()
        conn.autocommit = True  # !
        #  transaction.set_autocommit(True) #?
        # dbname = sql.Identifier(f'tenant_{tenant_id}')
        try:
            create_cmd = sql.SQL(f'CREATE DATABASE {database_name}')
            # grant_cmd = sql.SQL(f'GRANT ALL PRIVILEGES ON DATABASE {database_name} TO {self.username}')
            cursor.execute(create_cmd)
            # cursor.execute(grant_cmd)
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()
    def execute_sql(self,sql):

        conn = psycopg2.connect(host=self.host, user=self.username, password=self.password, database=self.database,
                                  port=self.port)
        cursor = conn.cursor()
        try:
            # 执行sql
            cursor.execute(sql)
            conn.commit()
        except:
            # 发生错误时回滚
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

    def execute_sql_from_file(self,database, sql_file):
        self.database = database
        conn = psycopg2.connect(host=self.host, user=self.username, password=self.password, database=self.database,
                                port=self.port)
        # 创建一个游标对象
        cur = conn.cursor()
        cur.execute("ROLLBACK")
        with open(sql_file, "r") as f:
            sql_file = f.read()
        # 要保证sql文件里没有多余的;每个sql都要以;结尾
        sql_commands = sql_file.strip().split(';')
        print(sql_commands)
        try:
            for command in sql_commands:
                print(command)
                if command != '':
                    cur.execute(command)
            conn.commit()
        except Exception as e:
            print(f'execute_sql_from_file-{command}-报错信息{e}')
        finally:
            cur.close()
            conn.close()

    def fetch_all(self, sql):
        """查询数据并返回所有结果"""
        conn = psycopg2.connect(host=self.host, user=self.username, password=self.password, database=self.database,
                                port=self.port)
        cur = conn.cursor()
        cur.execute(sql)
        result = cur.fetchall()
        cur.close()
        return result

    def fetch_one(self, sql):
        """查询数据并返回一条结果"""
        conn = psycopg2.connect(host=self.host, user=self.username, password=self.password, database=self.database,
                                port=self.port)
        cur = conn.cursor()
        cur.execute(sql)
        result = cur.fetchone()
        cur.close()
        return result

if __name__ == '__main__':
    DbHandle = PgsqlHandle('192.168.0.101', 'postgres', 'hui666666', 'postgres', 5432)
    DbHandle.create_database('colo_test')
    print('库创建完成，开始建表')
    DbHandle.execute_sql_from_file('colo_test','../assets/timescale_schema.sql')
