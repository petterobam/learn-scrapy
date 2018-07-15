# -*- coding:utf-8 -*-
import Parent
from MyES import MyESClient

list = [
    {"date": "2017-09-13",
     "source": "慧聪网",
     "link": "http://info.broadcast.hc360.com/2017/09/130859749974.shtml",
     "keyword": "电视",
     "title": "付费 电视 行业面临的转型和挑战"
     },
    {"date": "2017-09-13",
     "source": "中国文明网",
     "link": "http://www.wenming.cn/xj_pd/yw/201709/t20170913_4421323.shtml",
     "keyword": "电视",
     "title": "电视 专题片《巡视利剑》广获好评：铁腕反腐凝聚党心民心"
     },
    {"date": "2017-09-13",
     "source": "人民电视",
     "link": "http://tv.people.com.cn/BIG5/n1/2017/0913/c67816-29533981.html",
     "keyword": "电视",
     "title": "中国第21批赴刚果（金）维和部隊启程--人民 电视 --人民网"
     },
    {"date": "2017-09-13",
     "source": "站长之家",
     "link": "http://www.chinaz.com/news/2017/0913/804263.shtml",
     "keyword": "电视",
     "title": "电视 盒子 哪个牌子好？ 吐血奉献三大选购秘笈"
     }
]

# 提前给elasticsearch安装对应版本的中文分词器 https://github.com/medcl/elasticsearch-analysis-ik
index_mappings = {
    "mappings": {
        "ott_type": {
            "properties": {
                "title": {
                    "type": "text",
                    "index": True,
                    "analyzer": "ik_max_word",
                    "search_analyzer": "ik_max_word"
                },
                "date": {
                    "type": "text",
                    "index": True
                },
                "keyword": {
                    "type": "text",
                    "index": False
                },
                "source": {
                    "type": "text",
                    "index": False
                },
                "link": {
                    "type": "text",
                    "index": False
                }
            }
        }
    }
}

es = MyESClient("ott", "ott_type", print=True)

es.createIndex(index_mappings)

es.indexDataList(list)

queryBody = {
    "query": {
        "match": {
            "title": "电视"
        }
    }
}

es.getDataByBody(queryBody)

es.getDataExportCSV('es-test/ott.csv')

es.indexDataFromCSV("es-test/ott.csv")
