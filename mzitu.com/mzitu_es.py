# -*- coding:utf-8 -*-
import Parent
from DBTools.MyES import MyESClient
from datetime import datetime

class MzituEs():
    def __init__(self):
        self.init_es()
        
    def init_es(self):
        self.esindex = "mzitu"
        self.estype = "mzitu_imgs"
        index_mappings = {
            "mappings": {
                self.estype: {
                    "properties": {
                        "imgThemeTitle": {
                            "type": "text",
                            "index": True,
                            "analyzer": "ik_max_word",
                            "search_analyzer": "ik_max_word"
                        },
                        "imgThemeUrl": {
                            "type": "keyword",
                            "index": True
                        },
                        "createTime": {
                            "type": "date",
                            "index": True
                        },
                        "scrapyStatus":{
                            "type": "integer",
                            "index": True,
                            # 0,1,2 待爬取，爬取中，已完成
                            "null_value": 0
                        }
                    }
                }
            }
        }
        self.es = MyESClient(self.esindex, self.estype)
        self.es.createIndex(index_mappings)
        self.currdata = {}
        self.currdata["imgUrlList"] = []

    def save_es(self, data=None):
        '''
        存储当前数据到ES，并清空
        :return:
        '''
        if data == None:
            data = self.currdata
            data["createTime"] = datetime.now()
            data["scrapyStatus"] = 0
            self.currdata = {}
            self.currdata["imgUrlList"] = []
        self.es.indexData(data, data["imgThemeUrl"])
        
    def get_one_need_scrapy_es(self):
        '''
        从ES库中找一个待爬取的数据
        '''
        queryBody = {
          "query": {
            "bool": {
              "must": [
                {
                  "term": {
                    "scrapyStatus": {
                      "value": 0
                    }
                  }
                }
              ]
            }
          }
        }        
        res = self.es.getOneByBody(queryBody)
        return res
    
    def get_by_themeId_es(self, themeId):
        res = self.es.getDataSourceById(themeId)
        return res

    def exit_es(self, themeurl):
        queryBody = {
          "query": {
            "bool": {
              "must": [
                {
                  "term": {
                    "imgThemeUrl": {
                      "value": themeurl
                    }
                  }
                }
              ]
            }
          }
        }
        if self.es.exit(queryBody):
            print("ES数据库里面已经存在！！")
            return True
        else:
            return False
        
mzitu_es = MzituEs()