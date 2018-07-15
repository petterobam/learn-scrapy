# -*- coding:utf-8 -*-
from pymongo import MongoClient

class MyMongoClient(object):
    def __init__(self, dbname=None, setname=None):
        self.dbname = dbname
        self.setname = setname
        self.client = MongoClient() ##与MongDB建立连接（这是默认连接本地MongDB数据库）
        self.db = self.client[dbname] ## 选择一个数据库
        self.collection = self.db[setname] ##在这个数据库中，选择一个集合        
        
    def save(self, data):
        res = self.collection.save(data)
        if SHOW_RESULT:
            print(res)
        return res
    
    def getOne(self, query):
        res = self.collection.find_one(query)
        if SHOW_RESULT:
            print(res)
        return res
    
    def isExit(self, query):
        if self.getOne(query):
            return True
        else:
            return False
        
    def get(self, query):
        res = self.collection.find(query)
        if SHOW_RESULT:
            print(res)
        return res      

SHOW_RESULT = True
        