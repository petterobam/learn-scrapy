# -*- coding:utf-8 -*-
import Parent
from bs4 import BeautifulSoup
import os
import re
from BaseTools.MyUtil import FileManager
from BaseTools.MyDownload import request
import csv
## http://vacations.ctrip.com/visa/lsg
## div.c_con a
## table.sin_lis td
# lqmc: h4
# lsgmc: p[0]
# lsgdz: p[1]
# lsggzsj: p[3]
class VisaLqxxCrawler():
    def __init__(self):
        self.headers = {'User-Agent': "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"}
        self.gqtpPath = "./gqtp/"
        self.mkdir(self.gqtpPath)
        self.mkdir("./lsgxx/")
        self.lsgxxFilePath = "./lsgxx/lsgxx.txt"
        self.lsgxxCsvPath = "./lsgxx/lsgxx.csv"
        self.lsgxxList = []
    def all_url(self, url="http://vacations.ctrip.com/visa/lsg"):
        html = self.request(url)##调用request函数把套图地址传进去会返回给我们一个response
        all_div = BeautifulSoup(html.text, 'lxml').find_all('div', class_='c_con')
        print("一共有 %d 个州" % len(all_div))
        for div in all_div:
            all_a = div.find_all('a')
            print("该洲一共有 %d 个国家" % len(all_a))
            for a in all_a:
                img = a.find("img")
                self.headers['referer'] = url
                self.save(img["src"])
                href = "http://vacations.ctrip.com" + a['href']
                title = a["title"]
                self.currGjmc = title
                print(title, href)
                self.headers['referer'] = href
                self.html(href)
        self.exportCsv(self.lsgxxCsvPath)
    def html(self, href):   ##这个函数是处理套图地址获得图片的页面地址
        try:
            html = self.request(href)
            #max_span = BeautifulSoup(html.text, 'lxml').find('div', class_='pagenavi').find_all('span')[-2].get_text()
            tds = BeautifulSoup(html.text, 'lxml').find('table', class_="sin_lis").find_all('td')
            for td in tds:
                lsgInfo = {}
                lsgInfo["gjmc"] = self.currGjmc
                h4 = td.find("h4").get_text()
                lsgInfo["lqmc"] = self.trim(h4)
                ps = td.find_all('p')
                lsgInfo["lqgmc"] = self.trim(ps[0].get_text())
                lsgInfo["lqgdz"] = self.trim(ps[1].get_text())
                lsgInfo["lsggzsj"] = self.trim(ps[2].get_text())
                print(lsgInfo)
                self.lsgxxList.append(lsgInfo)
                # FileManager.write(self.lsgxxFilePath,lsgInfo.encode("utf-8"))
        except Exception as e:
            print('发生了异常：', e)

    def exportCsv(self,csvfile, list=None, cloumnList=None):
        if list == None:
            list = self.lsgxxList
        if cloumnList == None and len(list) > 0:
            cloumnList = list[0].keys()
        # fobj = open(csvfile, 'w+')
        # fobj = open(csvfile, 'ab+')
        with open(csvfile, 'w', newline='') as fobj:
            writer = csv.DictWriter(fobj, fieldnames=cloumnList)
            writer.writeheader()
            for item in list:
                writer.writerow(item)

    def trim(self, myStr):
        myStr = re.sub('\n', '', myStr)
        myStr = re.sub(' ', '', myStr)
        myStr = re.sub('\ufffd', ' ', myStr)
        return myStr

    def save(self, img_url): ##这个函数保存图片
        try:
            index = img_url.rindex("/")
            name = img_url[index:]
            img = self.request(img_url)
            f = open(self.gqtpPath + name, 'ab')
            f.write(img.content)
            f.close()
        except Exception as e:
            print('发生了        异常：', e)

    def mkdir(self, path=""): ##这个函数创建文件夹
        path = path.strip()
        isExists = os.path.exists(path)
        if not isExists:
            print('建了一个名字叫做', path, '的文件夹！')
            os.makedirs(path)
            #os.chdir(os.path.join(self.gqtpPath, path)) ##切换到目录
            return True
        else:
            print('名字叫做', path, '的文件夹已经存在了！')
            return False

    def request(self, url): ##这个函数获取网页的response 然后返回
        content = request.get(url, headers=self.headers, timeout=3)
        return content

visaLqxxCrawler = VisaLqxxCrawler()
visaLqxxCrawler.all_url()