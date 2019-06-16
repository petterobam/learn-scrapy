# -*- coding:utf-8 -*-
import Parent
from bs4 import BeautifulSoup
from BaseTools.MyDownload import request
from BaseTools.MyUtil import FileTool
import time

class jjwxk_free_simple():
    def __init__(self):
        self.headers = {
            # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            # 'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Host': 'www.jjwxc.net',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent':"Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
        }
        self.basePath = "jjwxk_free_simple/"
        FileTool.mkdir(self.basePath)
        self.baseListFilePath = self.basePath + "book-list.txt"
        self.baseUrlFilePath = self.basePath + "book-url.txt"
        self.basePageFilePath = self.basePath + "book-page.txt"
        self.totalFinishFilePath = self.basePath + "total.txt"
        self.finishBookLineCountFilePath = self.basePath + "book-total.txt"
        self.globalPageCount = 0
        self.pageCount = 0
        self.lineCount = 0
        self.readFinishCountInfo()

    # 抓取入口:默认 http://www.jjwxc.net/bookbase_slave.php?booktype=free
    def free_list(self, limitPage=1, url="http://www.jjwxc.net/bookbase_slave.php?booktype=free"):
        html_content = self.request_content(url)  ##调用request_content返回html文本给我们
        FileTool.write_behind(self.basePageFilePath, url)
        html_ele = BeautifulSoup(html_content, 'lxml')
        self.globalPageCount = self.globalPageCount + 1
        if self.globalPageCount > limitPage:
            return

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
        else:
            self.globalPageCount = self.pageCount - 1

        # page_next = "http://www.jjwxc.net/" + html_ele.find_all("div", class_="controlbar")[1].find_all("a")[2]["href"]
        page_next = "http://www.jjwxc.net/bookbase_slave.php?booktype=free&opt=&endstr=&orderstr=4&page=" + str(self.globalPageCount + 1)
        if page_next == None or "" == page_next:
            return
        print("书籍清单第", self.globalPageCount, "页信息：[", url, "]抓取完毕")
        # 暂停一秒，防止爬虫被发现
        # time.sleep(1)
        self.headers['Referer'] = url
        # 继续拉取下一页
        self.free_list(limitPage, page_next)

    # 从保存的书籍链接记录里面抓取每一本书的内容
    def book_list(self):
        book_count = 0
        book_finish_count = self.readSimpleFinishCountInfo(self.finishBookLineCountFilePath)
        for line in open(self.baseUrlFilePath):
            # 逐行读取此前爬取的书籍链接，去掉最后的换行符号
            url = line.replace("\n", "")
            book_count = book_count + 1
            if book_count <= book_finish_count:
                print("[", url, "]，该本书已经抓取过！")
                continue
            self.book_one(url)
            # 记录抓取书的数量，实现简单断点续爬
            FileTool.overwrite(self.finishBookLineCountFilePath, str(book_count))
        print("[", url, "]，该本书所有章节已经抓取完毕！")

    # 保存一本书的内容
    def book_one(self, url="http://www.jjwxc.net/onebook.php?novelid=3468871"):
        html_content = self.request_content(url)  ##调用request_content返回html文本给我们
        html_ele = BeautifulSoup(html_content, 'lxml')
        # 获取图书表格元素
        book_table = html_ele.find("table", id="oneboolt")
        list_tr = book_table.find_all("tr")
        self.headers['Referer'] = url
        if len(list_tr) > 0:
            book_title = list_tr[0].find("h1").get_text()
            # 去掉文件夹中特殊字符，防止小说名中特殊字符
            book_floder = self.basePath + FileTool.replace_invalid_filename(book_title) + "/"
            FileTool.mkdir(book_floder)
            book_chapter_file = book_floder + "0.chapter_list.txt"
            book_chapter_url_file = book_floder + "0.chapter_url_list.txt"
            book_chapter_finish_count_file = book_floder + "0.current_count.txt"
            chapter_count = 0
            chapter_finish_count = self.readSimpleFinishCountInfo(book_chapter_finish_count_file)
            for tr in list_tr:
                if "itemprop" in tr.attrs:
                    chapter_count = chapter_count + 1
                    if chapter_count <= chapter_finish_count:
                        print("第", chapter_count, "章，该章节已经抓取过！")
                        continue
                    list_td = tr.find_all("td")
                    count_td = 0
                    chapter_info_arr = []
                    chapter_url = None
                    chapter_title = None
                    for td in list_td:
                        chapter_info_arr.append(td.get_text().replace('\n', '').replace(' ', ''))
                        if count_td == 1:
                            chapter_a = td.find("a")
                            if chapter_a != None:
                                chapter_url = chapter_a['href']
                                chapter_title = chapter_a.get_text()
                        count_td = count_td + 1
                    if chapter_url == None:
                        print("第", chapter_count, "章，该章节已丢失！")
                        chapter_url = "第" + str(chapter_count) + "章，该章节已丢失！"
                    else:
                        # 去掉文件名中的特殊字符
                        curr_filename = FileTool.replace_invalid_filename(str(chapter_count) + "." + chapter_title + ".txt")
                        curr_chapter_file_path = book_floder + curr_filename
                        self.save_chapter(curr_chapter_file_path, chapter_url)
                    FileTool.write_behind(book_chapter_url_file, chapter_url)
                    chapter_info = "  |  ".join(chapter_info_arr)
                    FileTool.write_behind(book_chapter_file, chapter_info)
                    # 记录完成的章节数，简单实现断点续爬
                    FileTool.overwrite(book_chapter_finish_count_file, str(chapter_count))
                    print("第", chapter_count, "章，该章节已经抓取完毕！")

    # 保存一个章节的内容
    def save_chapter(self, path, chapter_url):
        html_content = self.request_content(chapter_url)  ##调用request_content返回html文本给我们
        html_ele = BeautifulSoup(html_content, 'lxml')
        novelDiv = html_ele.find("div", class_="noveltext")
        if novelDiv == None:
            return
        novelHtmls = novelDiv.contents
        novelTextArr = []
        # 处理小说文本数据，保证简单换行，保证基本格式
        for novelHtml in novelHtmls:
            if novelHtml.name == "div" or novelHtml.name == "br":
                continue
            else:
                text = novelHtml.string
                if text == None:
                    continue
                text = text.replace('\n', '').replace("\r", "").replace(" ", "")
                if len(text) > 0:
                    novelTextArr.append(text)
        novelText = "\n\n".join(novelTextArr)
        FileTool.overwrite(path, novelText)


    # 读取简单的数字信息
    def readSimpleFinishCountInfo(self, path):
        isExists = FileTool.isExit(path)
        if isExists:
            countTxt = FileTool.read_utf8(path)
            return int(countTxt)
        else:
            return 0

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
        try:
            return request.get_utf8_content(url, headers=self.headers)
        except:
            return ""


jjwxk = jjwxk_free_simple()
jjwxk.free_list()
# while jjwxk.globalPageCount < 10000:
#     try:
#         jjwxk.free_list()
#     except Exception as e:
#         print('except:', e)
#     finally:
#         print('finally...')
jjwxk.book_list()