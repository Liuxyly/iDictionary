# -*- coding: utf-8 -*-

import sqlite3
import os
import sys

DB_FILE_PATH = './db/vocabulary.db'
SHOW_SQL = True

class DBControl:

    '''
        调试时，使用的信息
    '''
    def showSql(self, sql):
        print('running sql:[{}]'.format(sql))
    
    '''获取到数据库的连接对象，参数为数据库文件的绝对路径
    如果传递的参数是存在，并且是文件，那么就返回硬盘上面改
    路径下的数据库文件的连接对象；否则，返回内存中的数据接
    连接对象'''
    def getConnect(self, path):
        Connect = sqlite3.connect(path)
        Connect.text_factory=lambda x: unicode(x, "utf-8", "ignore")
        if os.path.exists(path) and os.path.isfile(path):
            print('Vocabulary DB is Ready')
            return Connect
        else:
            print('Vocabulary DB is Filed')
            return None
        
    '''该方法是获取数据库的游标对象，参数为数据库的连接对象
    如果数据库的连接对象不为None，则返回数据库连接对象所创
    建的游标对象；否则返回一个游标对象，该对象是内存中数据
    库连接对象所创建的游标对象'''
    def getCursor(self, conn):
        if conn is not None:
            return conn.cursor()
        else:
            print('Vocabulary DB is Filed')
            return None

    '''创建数据库表'''
    def createTable(self, conn, sql):
        if sql is not None and sql != '':
            Cursor  = self.getCursor(conn)
            if SHOW_SQL:
                self.showSql(sql)
            Cursor.execute(sql)
            conn.commit()
            print('create successfully!')
            self.closeAll(conn, Cursor)
        else:
            print('the [{}] is empty or equal None!'.format(sql))

    '''关闭数据库游标对象和数据库连接对象'''
    def closeAll(self, conn, cur):
        try:
            if cur is not None:
                cur.close()
        finally:
            if cur is not None:
                cur.close()

    '''插入数据'''
    def insertData(self, conn, sql, data):
        if sql is not None and sql != '':
            if data is not None:
                Cursor = self.getCursor(conn)
                for d in data:
                    if SHOW_SQL:
                        self.showSql(sql)
                    Cursor.execute(sql, d)
                    conn.commit()
                self.closeAll(conn, Cursor)
    
    '''查询所有数据'''
    def selectAllData(self, conn, sql):
        if sql is not None and sql != '':
            Cursor = self.getCursor(conn)
            if SHOW_SQL:
                self.showSql(sql)
            Cursor.execute(sql)
            return Cursor.fetchall()
        else:
            print('the [{}] is empty or equal None!'.format(sql))

    '''如果表存在,则删除表，如果表中存在数据的时候，使用该
    方法的时候要慎用！'''
    def dropTable(self, conn, table):
        if table is not None and table != '':
            sql = 'DROP TABLE IF EXISTS ' + table
            if SHOW_SQL:
                self.showSql(sql)
            Cursor = self.getCursor(conn)
            Cursor.execute(sql)
            conn.commit()
            print('Delete [{}] Successfully!'.format(table))
            self.closeAll(conn, Cursor)
        else:
            print('the [{}] is empty or equal None!'.format(sql))

    '''更新数据'''
    def updateTable(self, conn, sql, data):
        if sql is not None and sql != '':
            if data is not None:
                Cursor = self.getCursor(conn)
                for d in data:
                    if SHOW_SQL:
                        self.showSql(sql)
                    Cursor.execute(sql, d)
                    conn.commit()
                self.closeAll(conn, Cursor)
        else:
            print('the [{}] is empty or equal None!'.format(sql))

def displaySelectedData(data):
    if len(data) > 0:
        for e in range(len(data)):
            for a in range(len(data[e])):
                print data[e][a]
        
if __name__ == '__main__':
    db = DBControl()
    Connect = db.getConnect(DB_FILE_PATH)
    Cursor  = db.getCursor(Connect)
    db.dropTable(Connect, 'vocabulary')
    create_table_sql = '''CREATE TABLE `vocabulary` (
                          `id` int(16) NOT NULL,
                          `vocabulary` varchar(64) NOT NULL,
                          `feq` int(8) DEFAULT NULL,
                          `meaning` varchar(64) DEFAULT NULL,
                          `property` varchar(64) DEFAULT NULL,
                          `comment` varchar(512) DEFAULT NULL,
                           PRIMARY KEY (`id`)
                        )'''
    db.createTable(Connect, create_table_sql)
    save_sql = '''INSERT INTO vocabulary values (?, ?, ?, ?, ?, ?)'''
    data = [(1, 'comment', 0, u'评论; 注释; 意见; 说明; ', u'n', u''),
            (2, 'comment', 0, u'评论，谈论;', u'vt.& vi.', u''),
            (3, 'comment', 0, u'表达意见; 解释，注释; ', u'vt.', u''),
            (4, 'comment', 0, u'作注释; 作注解; 作解释; 作评语; ', u'vi.', u'')]
    db.insertData(Connect, save_sql, data)

    update_sql = 'UPDATE vocabulary SET feq = ? WHERE ID = ? '
    
    data1 = [(1, 1),
             (1, 2),
             (1, 3),
             (1, 4)]
    
    db.updateTable(Connect, update_sql, data1)
    
    fetchall_sql = '''SELECT * FROM vocabulary'''
    
    data = db.selectAllData(Connect, fetchall_sql)
    
    displaySelectedData(data)
