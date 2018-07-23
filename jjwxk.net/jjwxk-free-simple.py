# -*- coding:utf-8 -*-
import Parent
from bs4 import BeautifulSoup
from BaseTools.MyDownload import request
from BaseTools.MyUtil import FileTool

class jjwxk_free_simple():
    def __init__(self):
        self.basePath = "jjwxk_free_simple/"
        FileTool.mkdir(self.basePath)
        self.baseListFilePath = self.basePath + "book-list.txt"
        self.baseUrlFilePath = self.basePath + "book-url.txt"
        self.basePageFilePath = self.basePath + "book-page.txt"
        self.totalFinishFilePath = self.basePath + "total.txt"
        self.globalPageCount = 0
        self.pageCount = 0
        self.lineCount = 0
        self.readFinishCountInfo()

    # 抓取入口:默认 http://www.jjwxc.net/bookbase_slave.php?booktype=free
    def free_list(self, url="http://www.jjwxc.net/bookbase_slave.php?booktype=free"):
        html_content = self.request_content(url)  ##调用request函数把套图地址传进去会返回给我们一个response
        FileTool.write_behind(self.basePageFilePath, url)
        html_ele = BeautifulSoup(html_content, 'lxml')
        self.globalPageCount = self.globalPageCount + 1

        if self.globalPageCount >= self.pageCount:
            # 如果当前页码比记录的页码大，行数从第一行开始记录，否则就当前页码记录
            if(self.globalPageCount > self.pageCount):
                self.lineCount = 0
                self.pageCount = self.globalPageCount
            
            # 获取图书表格元素
            book_table = html_ele.find("table", class_="cytable")
            if book_table == None:
                return
            list_tr = book_table.find_all("tr")
            count = -1
            for tr in list_tr:
                count = count + 1
                if count == 0 or self.lineCount >= count:
                    continue
                list_td = tr.find_all("td")
                book_list_url = None
                book_info_arr = []
                count_td = 0
                for td in list_td:
                    book_info_arr.append(td.get_text().replace('\n', '').replace(' ', ''))
                    if count_td == 1:
                        book_list_url = "http://www.jjwxc.net/" + td.find("a")['href']
                    count_td = count_td + 1
                FileTool.write_behind(self.baseUrlFilePath, book_list_url)
                book_list_info = "  |  ".join(book_info_arr)
                FileTool.write_behind(self.baseListFilePath, book_list_info)
                self.lineCount = count
                # 完成一行，记录一下count信息，便于后面断点爬取
                self.saveFinishCountInfo()

        page_next = "http://www.jjwxc.net/" + html_ele.find_all("div", class_="controlbar")[1].find_all("a")[2]["href"]
        if page_next == None or "" == page_next:
            return
        self.free_list(page_next)

    # 保存已完成的条数信息
    def saveFinishCountInfo(self):
        FileTool.overwrite(self.totalFinishFilePath, str(self.pageCount) + "-" + str(self.lineCount))

    # 读取已完成的条数信息
    def readFinishCountInfo(self):
        isExists = FileTool.isExit(self.totalFinishFilePath)
        if isExists:
            countTxt = FileTool.read_utf8(self.totalFinishFilePath)
            countStrArr = countTxt.split("-")
            self.pageCount = int(countStrArr[0])
            self.lineCount = int(countStrArr[1])
        else:
            self.pageCount = 0
            self.lineCount = 0

    # 获取网页html文本内容
    def request_content(self, url):
        return request.get_utf8_content(url)

jjwxk = jjwxk_free_simple()
jjwxk.free_list()