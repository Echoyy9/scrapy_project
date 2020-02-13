# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
from twisted.enterprise import adbapi
#专门做数据库处理
from pymysql import cursors



#同步
class JianshuPipeline(object):
    def __init__(self):
        dpparams = {
            'host':'127.0.0.1',
            'port':3306,
            'database': 'jianshu',
            'user': 'root',
            'password': '123321',
            'charset': 'utf8'
        }
        self.conn = pymysql.connect(**dpparams)
        self.cursor = self.conn.cursor()
        self._sql = None

    def process_item(self, item, spider):
        self.cursor.execute(self.sql,(item['title'],item['content'], item['author'], item['img'], item['pub_time'], item['origin_url'], item['article_id'] ))
        self.conn.commit()

        return item

    @property
    def sql(self):
        if not self._sql:
            self._sql = """
            insert into article(id,title,content,author,img,pub_time,origin_url,article_id) value(null,%s,%s,%s,%s,%s,%s,%s)
            """
            return self._sql
        return self._sql


#异步
class JianShuTwistedPipeline(object):
    def __init__(self):
        self.dbpool = adbapi.ConnectionPool('pymysql')
        dpparams = {
            'host': '127.0.0.1',
            'port': 3306,
            'database': 'jianshu',
            'user': 'root',
            'password': '123321',
            'charset': 'utf8',
            'cursorclass': cursors.DictCursor
        }

        self.dbpool = adbapi.ConnectionPool('pymysql', **dpparams)
        self._sql = None


    @property
    def sql(self):
        if not self._sql:
            self._sql = """
            insert into article(id,title,content,author,img,pub_time,origin_url,article_id) value(null,%s,%s,%s,%s,%s,%s,%s)
            """
            return self._sql
        return self._sql

    def process_item(self,item, spider):
        defer = self.dbpool.runInteraction(self.insert_item,item  )
        #通过runInteraction实现异步
        defer.addErrback(self.handle_error, item, spider)

    def insert_item(self, cursor, item ):
        cursor.execute(self.sql,(item['title'],item['content'], item['author'], item['img'], item['pub_time'], item['origin_url'], item['article_id'] ))

    def handle_error(self, error, item, spider):
        print('=' * 10 + 'error' + '=' * 10)
        print(error)
        print('=' * 10 + 'error' + '=' * 10)



