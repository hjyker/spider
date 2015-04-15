#!/usr/bin/env python
# -*- coding:gbk -*-

import sqlite3

class StoreWebpage():
    def __init__(self, dbfile):
        self.restoreDB = sqlite3.connect(dbfile, check_same_thread=False)
        self.restoreDB.text_factory = str

        self.cu = self.restoreDB.cursor()
        self.createTable(self.cu)

    def createTable(self, cu):
        #if not table webpages, create it.
        createDB = r'''
        create table if not exists webpages (
            id integer primary key ,
            content text
        )'''
        cu.execute(createDB)

    def insertWebpage(self, cu, webpage):
        cu.execute("insert into webpages(content) values(?)", (webpage,))

    def store(self, webpage):
        self.insertWebpage(self.cu, webpage)
        self.restoreDB.commit() # 必须提交才能使插入生效

def testdoc():
    '''
        >>> s = StoreWebpage('test.db')
        >>> s.store('我是测试')
    '''

if __name__ == '__main__': pass
