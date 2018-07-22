# -*- coding:utf-8 -*-
import Parent
from bs4 import BeautifulSoup
from BaseTools.MyDownload import request
from BaseTools.MyUtil import FileTool

class jjwxk_free_simple():
    def __init__(self):
        self.basePath = "/jjwxk_free_simple/"
        FileTool.mkdir(self.basePath)
        self.baseListFilePath = self.basePath + "book-list.txt"
        self.totalFinishFilePath = self.basePath + "total.txt"

    # 抓取入口:默认 http://www.jjwxc.net/bookbase_slave.php?booktype=free
    def free_list(self, url="http://www.jjwxc.net/bookbase_slave.php?booktype=free"):
        html = self.request(url)  ##调用request函数把套图地址传进去会返回给我们一个response
        list_table = BeautifulSoup(html.text, 'lxml').find("table", class_="cytable")
        if(list_table == None):
            return
        # TODO：后续
        
    def request(self, url):  ##这个函数获取网页的response 然后返回
        content = request.get(url, headers={}, timeout=3)
        return content

jjwxk = jjwxk_free_simple()