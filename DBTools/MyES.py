# -*- coding:utf-8 -*-
import os
import time
import csv
from os import walk
from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

class MyESClient(object):
    def __init__(self, index_name, index_type, ip ="127.0.0.1", print=False):
        '''
        :param index_name: 索引名称
        :param index_type: 索引类型
        '''
        self.index_name =index_name
        self.index_type = index_type
        # 无用户名密码状态
        self.es = Elasticsearch([ip], port=9200)
        #用户名密码状态
        self.es = Elasticsearch([ip], http_auth=('elastic', 'password'), port=9200)
        self.show_es_result = print

    def createIndex(self, index_mappings):
        '''
        创建索引,创建索引名称为ott，类型为ott_type的索引
        :param ex: Elasticsearch对象
        :return:
        '''
        #创建映射
        if self.es.indices.exists(index=self.index_name) is not True:
            res = self.es.indices.create(index=self.index_name, body=index_mappings)
            if self.show_es_result:
                print(res)

    def indexDataFromCvsDir(self, cloumnDict):
        csvdir = './ElasticSearch/exportExcels'
        filenamelist = []
        for (dirpath, dirnames, filenames) in walk(csvdir):
            filenamelist.extend(filenames)
            break
        for file in filenamelist:
            csvfile = csvdir + '/' + file
            self.indexDataFromCSV(csvfile, cloumnDict)
            time.sleep(10)

    def indexDataFromCSV(self, csvfile, cloumnList=None):
        '''
        从CSV文件中读取数据，并存储到es中
        :param csvfile: csv文件，包括完整路径
        :return:
        '''
        with open(csvfile) as f:
            reader = csv.reader(f)
            # 读取一行，下面的reader中已经没有该行了
            index = 0
            if cloumnList == None:
                cloumnList = next(reader)
                index = 1
            doc = {}
            cloumnLength = len(cloumnList)
            for item in reader:
                if index > 0:#第一行是标题
                    if cloumnLength <= len(item):
                        for i in range(cloumnLength):
                            doc[cloumnList[i]] = item[i]
                        self.es.index(index=self.index_name, doc_type=self.index_type, body=doc)
                index += 1

    def getDataExportCSV(self, csvfile, query={'query': {'match_all': {}}}, cloumnList=None):
        '''
        从数据库导出csv表格
        :param csvfile:
        :param query:
        :param cloumnList:
        :return:
        '''
        res = self.getDataByBody(query)
        if res is not None and len(res['hits']['hits']) > 0:
            # fobj = open(csvfile, 'w+')
            with open(csvfile, 'w', newline='') as fobj:
                if cloumnList == None:
                    cloumnList = res['hits']['hits'][0]["_source"].keys()
                writer = csv.DictWriter(fobj, fieldnames=cloumnList)
                writer.writeheader()
                for hit in res['hits']['hits']:
                    writer.writerow(hit["_source"])

    def indexDataList(self, list=[]):
        '''
        数据存储到es
        :return:
        '''
        for item in list:
            res = self.es.index(index=self.index_name, doc_type=self.index_type, body=item)
            if self.show_es_result:
                print(res)

    def indexData(self, data, id=None):
        '''
        单条数据添加
        :param data:
        :return:
        '''
        res = self.es.index(index=self.index_name, doc_type=self.index_type, body=data, id=id)
        if self.show_es_result:
            print(res)
        return res

    def bulkIndexData(self, list=[]):
        '''
        用bulk将批量数据存储到es
        :return:
        '''
        ACTIONS = []
        for line in list:
            action = {
                "_index": self.index_name,
                "_type": self.index_type,
                "_source": line
            }
            ACTIONS.append(action)
            # 批量处理
        success, _ = bulk(self.es, ACTIONS, index=self.index_name, raise_on_error=True)
        if self.show_es_result:
            print('Performed %d actions' % success)
        return success

    def deleteDataById(self,id):
        '''
        删除索引中的一条
        :param id:
        :return:
        '''
        res = self.es.delete(index=self.index_name, doc_type=self.index_type, id=id)
        if self.show_es_result:
            print(res)
        return res

    def getDataId(self,id):
        res = self.es.get(index=self.index_name, doc_type=self.index_type, id=id)
        # 输出查询到的结果
        if self.show_es_result:
            print(res)
        return res

    def getDataSourceById(self,id):
        res = self.es.get(index=self.index_name, doc_type=self.index_type, id=id)
        # 输出查询到的结果
        if self.show_es_result:
            print(res)
        if res is not None and len(res['hits']['hits']) > 0:
            return res['hits']['hits'][0]["_source"]
        else:
            return None

    def exit(self, queryBody):
        if queryBody == None:
            return False
        res = self.getDataByBody(queryBody)
        if res is not None and len(res['hits']['hits']) > 0:
            return True
        else:
            return False

    def getOneByBody(self, query):
        params = {"size":1}
        res = self.getDataByBody(query, params)
        if res is not None and len(res['hits']['hits']) > 0:
            return res['hits']['hits'][0]["_source"]
        else:
            return None

    def getDataByBody(self, queryBody={'query': {'match_all': {}}}, params=None):
        # queryBody = {'query': {'match_all': {}}}
        _searched = None
        if params == None:
            _searched = self.es.search(index=self.index_name, doc_type=self.index_type, body=queryBody)
        else:
            _searched = self.es.search(index=self.index_name, doc_type=self.index_type, body=queryBody, params=params)

        if self.show_es_result:
            print(_searched)
        return _searched