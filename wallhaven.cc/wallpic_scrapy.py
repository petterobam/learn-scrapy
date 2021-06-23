# -*- coding:utf-8 -*-
import Parent
from bs4 import BeautifulSoup
import os
from BaseTools.MyDownload import request

class wallpic():
    def __init__(self):
        self.headers = {'User-Agent': "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"}
        self.basePath = "./wallpic/"
        self.currPath = self.basePath
        self.mkdir(self.basePath)
        self.totalFinishPath = "./wallpic/totalPage.txt"
        self.totalFinish = self.getTotalFinish()

    def all_get(self, totalPage):
        count = 0
        while count < totalPage:
            count = count + 1
            if count > self.totalFinish:
                self.overwriteTotalFinish(count)
            else:
                print("第", count, "页已经抓取过，跳过！")
                continue
            title = '第' + str(count) + '页/'
            href = 'https://wallhaven.cc/toplist?page=' + str(count)
            print(title, href)  ##加点提示不然太枯燥了
            ##调用mkdir函数创建文件夹！这儿path代表的是标题title哦！！！！！不要糊涂了哦！
            path = title
            self.mkdir(path)
            self.html(href) ##调用html函数把href参数传递过去！href是啥还记的吧？ 就是套图的地址哦！！不要迷糊了哦！
            self.totalFinish = count

    def html(self, href):   ##这个函数是处理套图地址获得图片的页面地址
        try:
            html = self.request(href)
            self.headers['referer'] = href
            figures = BeautifulSoup(html.text, 'lxml').find('section', class_='thumb-listing-page').find_all('figure')
            for figure in figures:
                page_url = figure.find_all('a')[0]['href']
                self.img(page_url) ##调用img函数
        except Exception as e:
            print('发生了异常：', e)

    def img(self, page_url): ##这个函数处理图片页面地址获得图片的实际地址
        img_html = self.request(page_url)
        img_url = BeautifulSoup(img_html.text, 'lxml').find('div', class_='scrollbox').find_all('img')[0]['src']
        print(img_url)
        self.saveImg(img_url)

    def saveImg(self, img_url): ##这个函数保存图片
        name = img_url[-9:-4]
        imgPath = self.currPath + name + '.jpg'
        isExists = os.path.exists(imgPath)
        if not isExists:
            img = self.request(img_url)
            f = open(imgPath, 'ab')
            f.write(img.content)
            f.close()
            print('该图片下载完毕')
        else:
            print('该图片已经存在')

    def mkdir(self, path): ##这个函数创建文件夹
        if USE_ONE_DIR:
            path = ""
        elif USE_DEF_DIR:
            index = path.rindex("/")
            path = path[index + 1:]
        else:
            path = path.strip()
        self.currPath = os.path.join(self.basePath, path)
        isExists = os.path.exists(self.currPath)
        if not isExists:
            print('建了一个名字叫做', path, '的文件夹！')
            os.makedirs(self.currPath)
            #os.chdir(os.path.join("./mzitu", path)) ##切换到目录
            return True
        else:
            print('名字叫做', self.currPath, '的文件夹已经存在了！')
            return False


    def request(self, url): ##这个函数获取网页的response 然后返回
        content = request.get(url, headers=self.headers, timeout=3)
        return content

    def getTotalFinish(self):
        isExists = os.path.exists(self.totalFinishPath)
        if isExists:
            with open(self.totalFinishPath, 'r', encoding='UTF-8') as f:
                return int(f.read())
        else:
            return 0

    def overwriteTotalFinish(self, count):
        with open(self.totalFinishPath, 'w', encoding='UTF-8') as f:
            f.write(str(count))

USE_ONE_DIR = False
USE_DEF_DIR = False
WallPic = wallpic() ##实例化

if __name__ == "__main__":
    ## 传入你要爬取的页数，你可以当作启动爬虫（就是入口）
    WallPic.all_get(11) 
