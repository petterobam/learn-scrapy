# -*- coding:utf-8 -*-
import Parent
import datetime
from bs4 import BeautifulSoup
import os
# import lxml
from BaseTools.MyDownload import request ##导入模块变了一下

class MzituThread(object):
    def __init__(self, mzitu_es):
        self.headers = {'User-Agent': "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"}
        self.currPath = "./mzitu/"
        self.currdata = {}
        self.currdata["imgUrlList"] = []
        self.es = mzitu_es

    def all_url(self, url='http://www.mzitu.com/all'):
        html = self.request(url)##调用request函数把套图地址传进去会返回给我们一个response
        all_a = BeautifulSoup(html.text, 'lxml').find('div', class_='all').find('ul', class_="archives").find_all('a')
        for a in all_a:
            try:
                title = a.get_text()
                href = a['href']
                print(title, href)  ##加点提示不然太枯燥了
                if self.es.exit_es(href):
                    continue
                self.currdata["imgThemeTitle"] = title
                self.currdata["imgThemeUrl"] = href
                self.es.save_es(self.currdata)
            except Exception as e:
                print(e)
                continue
    
    def scrapy_one(self, url=None):
        try:
            data = None
            if url == None:
                data = self.es.get_one_need_scrapy_es()
            else:
                data = self.es.get_by_themeId_es(url)
                
            if data == None:
                return False
            else:
                data["scrapyStatus"]=1
                self.es.save_es(data) ## 更新状态为爬取中
                href = data["imgThemeUrl"]
                self.mkdir(href) ##调用mkdir函数创建文件夹！
                self.html(href, data) ##调用html函数把href参数传递过去！
                data["scrapyStatus"]=2
                self.es.save_es(data) ## 保存数据，并更新状态为已完成
                return True
        except Exception as e:
            print(e)
            return False
            

    def html(self, href, data=None):   ##这个函数是处理套图地址获得图片的页面地址
        try:
            html = self.request(href)
            self.headers['referer'] = href
            ## max_span = BeautifulSoup(html.text, 'lxml').find('div', class_='pagenavi').find_all('span')[-2].get_text()
            max_span = BeautifulSoup(html.text, 'lxml').find_all('span')[10].get_text()
            for page in range(1, int(max_span) + 1):
                page_url = href + '/' + str(page)
                self.img(page_url, data) ##调用img函数
        except Exception as e:
            print('发生了异常：', e)

    def img(self, page_url, data=None): ##这个函数处理图片页面地址获得图片的实际地址
        img_html = self.request(page_url)
        img_url = BeautifulSoup(img_html.text, 'lxml').find('div', class_='main-image').find('img')['src']
        print(img_url)
        self.saveImg(img_url, data)

    def saveImg(self, img_url, data=None): ##这个函数保存图片
        name = img_url[-9:-4]
        currUrl = self.currPath + name + '.jpg'
        isExists = os.path.exists(currUrl)
        if not isExists:
            img = self.request(img_url)
            f = open(currUrl, 'ab')
            f.write(img.content)
            f.close()
            print('该图片下载完毕')
            if data == None:
                self.currdata["imgUrlList"].append({"originUrl":img_url, "currentUrl": currUrl})
            else:
                data["imgUrlList"].append({"originUrl":img_url, "currentUrl": currUrl})
        else:
            print('该图片已经存在')

    def mkdir(self, path): ##这个函数创建文件夹
        if USE_ONE_DIR:
            path = ""
        elif USE_DEF_DIR:
            if path == None:
                path = self.currdata["imgThemeUrl"]
            index = path.rindex("/")
            path = path[index + 1:]
        else:
            path = path.strip()
        isExists = os.path.exists(os.path.join("./mzitu", path))
        if not isExists:
            print('建了一个名字叫做', path, '的文件夹！')
            os.makedirs(os.path.join("./mzitu", path))
            self.currPath =  "./mzitu/" + path + "/"
            ## os.chdir(os.path.join("./mzitu", path)) ##切换到目录
            return True
        else:
            print('名字叫做', self.currPath, '的文件夹已经存在了！')
            return False

    def request(self, url): ##这个函数获取网页的response 然后返回
        content = request.get(url, headers=self.headers, timeout=3)
        return content

    

USE_ONE_DIR = False
USE_DEF_DIR = True

#mzituThread = MzituThread() ##实例化
#mzituThread.all_url()
#mzituThread.scrapy_one()