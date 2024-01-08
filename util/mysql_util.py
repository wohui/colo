# -*- encoding: utf-8 -*-

import pymysql


class PyMysqlHandle(object):
    ''' 定义一个 MySQL 操作类'''

    def __init__(self, host, username, password, database, port):
        '''初始化数据库信息并创建数据库连接'''
        # 下面的赋值其实可以省略，connect 时 直接使用形参即可
        self.host = host
        self.username = username
        self.password = password
        self.database = database
        self.port = port

        self.db = pymysql.connect(host=self.host, user=self.username, password=self.password, database=self.database,
                                  port=self.port, charset='utf8')
    def insertDB(self, sql):
        ''' 插入数据库操作 '''
        self.cursor = self.db.cursor()

        try:
            # 执行sql
            self.cursor.execute(sql)
            # tt = self.cursor.execute(sql)  # 返回 插入数据 条数 可以根据 返回值 判定处理结果
            # print(tt)
            self.db.commit()
        except:
            # 发生错误时回滚
            self.db.rollback()
        finally:
            self.cursor.close()

    def deleteDB(self, sql):
        ''' 操作数据库数据删除 '''
        self.cursor = self.db.cursor()

        try:
            # 执行sql
            self.cursor.execute(sql)
            # tt = self.cursor.execute(sql) # 返回 删除数据 条数 可以根据 返回值 判定处理结果
            # print(tt)
            self.db.commit()
        except:
            # 发生错误时回滚
            self.db.rollback()
        finally:
            self.cursor.close()

    def updateDb(self, sql):
        ''' 更新数据库操作 '''

        self.cursor = self.db.cursor()

        try:
            # 执行sql
            self.cursor.execute(sql)
            # tt = self.cursor.execute(sql) # 返回 更新数据 条数 可以根据 返回值 判定处理结果
            # print(tt)
            self.db.commit()
        except:
            # 发生错误时回滚
            self.db.rollback()
        finally:
            self.cursor.close()

    def selectDb(self, sql):
        ''' 数据库查询 '''
        data = None
        self.cursor = self.db.cursor()
        try:
            self.cursor.execute(sql)  # 返回 查询数据 条数 可以根据 返回值 判定处理结果
            data = self.cursor.fetchall()  # 返回所有记录列表
        except:
            print('Error: unable to fecth data')
        finally:
            self.cursor.close()
        return data

    def closeDb(self):
        ''' 数据库连接关闭 '''
        self.db.close()


if __name__ == '__main__':
    DbHandle = PyMysqlHandle('192.168.20.251', 'root', '1234567890///', 'tes', 3306)
    bar_code = '83010013'
    res = DbHandle.selectDb(f"select frame_id from frame where barcode = '{bar_code}'")
    print(res[0][0])
    DbHandle.closeDb()
