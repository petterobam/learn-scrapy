# -*- coding:utf-8 -*-
import Parent
from bs4 import BeautifulSoup
import os
from BaseTools.MyDownload import request

class mzitu():
    def __init__(self):
        self.headers = {'User-Agent': "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"}
        self.currPath = "./mzitu-no-es/"
    def all_url(self, url):
        html = self.request(url)##调用request函数把套图地址传进去会返回给我们一个response
        all_a = BeautifulSoup(html.text, 'lxml').find('div', class_='all').find('ul', class_="archives").find_all('a')
        for a in all_a:
            title = a.get_text()
            href = a['href']
            print(title, href)  ##加点提示不然太枯燥了
            #path = str(title).replace("?", '_') ##我注意到有个标题带有 ？  这个符号Windows系统是不能创建文件夹的所以要替换掉
            self.mkdir(title) ##调用mkdir函数创建文件夹！这儿path代表的是标题title哦！！！！！不要糊涂了哦！
            self.html(href) ##调用html函数把href参数传递过去！href是啥还记的吧？ 就是套图的地址哦！！不要迷糊了哦！

    def html(self, href):   ##这个函数是处理套图地址获得图片的页面地址
        try:
            html = self.request(href)
            self.headers['referer'] = href
            #max_span = BeautifulSoup(html.text, 'lxml').find('div', class_='pagenavi').find_all('span')[-2].get_text()
            max_span = BeautifulSoup(html.text, 'lxml').find_all('span')[10].get_text()
            for page in range(1, int(max_span) + 1):
                page_url = href + '/' + str(page)
                self.img(page_url) ##调用img函数
        except Exception as e:
            print('发生了异常：', e)

    def img(self, page_url): ##这个函数处理图片页面地址获得图片的实际地址
        img_html = self.request(page_url)
        img_url = BeautifulSoup(img_html.text, 'lxml').find('div', class_='main-image').find('img')['src']
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
        isExists = os.path.exists(os.path.join("./mzitu-no-es", path))
        if not isExists:
            print('建了一个名字叫做', path, '的文件夹！')
            os.makedirs(os.path.join("./mzitu-no-es/", path))
            self.currPath =  "./mzitu-no-es/" + path + "/"
            #os.chdir(os.path.join("./mzitu", path)) ##切换到目录
            return True
        else:
            print('名字叫做', self.currPath, '的文件夹已经存在了！')
            return False


    def request(self, url): ##这个函数获取网页的response 然后返回
        content = request.get(url, headers=self.headers, timeout=3)
        return content

USE_ONE_DIR = True
USE_DEF_DIR = False
Mzitu = mzitu() ##实例化
Mzitu.all_url('http://www.mzitu.com/all') ##给函数all_url传入参数  你可以当作启动爬虫（就是入口）
