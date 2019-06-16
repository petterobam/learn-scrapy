# -*- coding:utf-8 -*-
from selenium import webdriver
import time
import os
import requests
import PreviewHtmlTool


class Huaban():
    def __init__(self, username, password):
        self.username = username
        self.password = password

    # 获取图片和图片文字信息，并存储成文件
    def get_picture_info_by_border_url(self, border_url):
        
        # 使用Chrome浏览器模拟打开网页，但是要把下载的chromedriver.exe放在python的文件路径下,
        # 调试好之后换成PhantomJs,速度应该会快一点
        # driver = webdriver.PhantomJs()
        # driver = webdriver.PhantomJS('../plugin/phantomjs-2.1.1-macosx/bin/phantomjs')
        driver = webdriver.Chrome('../plugin/chromedriver')
        # 设置全屏
        driver.maximize_window()

        if username != None and len(username) > 0:
            url = "http://huaban.com"
            driver.get(url)
            time.sleep(8)

            # 点击登录、呼起登录窗口
            driver.find_elements_by_xpath('//a[@class="login bounce btn wbtn"]')[0].click()
            # 输入用户名
            try:
                driver.find_elements_by_xpath('//input[@name="email"]')[0].send_keys(self.username)
                print('用户名输入OK!')
            except:
                print('用户名输入异常!')
            time.sleep(3)
            # 输入密码
            try:
                driver.find_elements_by_xpath('//input[@name="password"]')[0].send_keys(self.password)
                print('密码输入OK!')
            except:
                print('密码输入异常!')
            time.sleep(3)
            # 点击登陆按钮
            try:
                driver.find_elements_by_xpath('//a[@class="btn btn18 rbtn"]')[0].click()
                print('点击登陆OK!')
            except:
                print('点击登陆异常')
            time.sleep(3)

        #访问画板，例如 http://huaban.com/boards/13448395/
        driver.get(border_url)
        time.sleep(5)
        i = 0
        page = 1
        global name
        global store_path
        global path
        # 获取画板标题 //div[@id="board_card"]/div[@class="inner"]/div[@class="head-line"]/h1
        content = driver.find_elements_by_xpath('//div[@id="board_card"]/div[@class="inner"]/div[@class="head-line"]/h1')[0].text
        path = "./" + content
        # hash_content = str(hash(content))
        # hash_content = border_url[-9:-1]
        url_split_list = border_url.split("/")
        hash_content = url_split_list[-2] + url_split_list[-1]

        # 保存图片到磁盘文件夹 file_path中，默认为当前脚本运行目录下的文件夹
        if not os.path.exists(path):
            os.makedirs(path)
        #获取图片的总数  //div[@id="board_card"]/div[@class="bar"]/div[@class="tabs"]/a
        pictures_count = driver.find_elements_by_xpath('//div[@id="board_card"]/div[@class="bar"]/div[@class="tabs"]/a')[0].text.replace('采集', '')
        print(pictures_count)

        # 生成预览用的HTML页面
        PreviewHtmlTool.saveIndexHtmlFile(path + "/index.html", content, hash_content, pictures_count)

        pages = int(int(pictures_count) / 20)
        print(pages)
        #匹配到图片url所在的元素
        url_elements = driver.find_elements_by_xpath('//span[@class="stop"]/../img')
        #匹配图片对应的文字描述
        pic_info_elements = driver.find_elements_by_xpath('//div[@id="waterfall"]//p[@class="description"]')

        while page <= pages:
            while len(url_elements) < 20 * page:
                driver.execute_script("window.scrollBy(0,1000)")
                time.sleep(3)
                url_elements = driver.find_elements_by_xpath('//span[@class="stop"]/../img')
                pic_info_elements = driver.find_elements_by_xpath('//div[@id="waterfall"]//p[@class="description"]')

            print("第%s页" % page)

            for url_element in url_elements[20 * (page - 1):20 * page]:
                download_url = url_element.get_attribute("src")[:-3] + "658"
                pic_info = pic_info_elements[i].get_attribute("data-raw")
                i += 1
                store_path = hash_content + "_" + str(i)
                self.store(download_url, pic_info)

            page += 1

        #最后一页
        print("第%s页" % int(page))

        while len(url_elements) < int(pictures_count):
            driver.execute_script("window.scrollBy(0,1000)")
            time.sleep(3)
            url_elements = driver.find_elements_by_xpath('//span[@class="stop"]/../img')
            pic_info_elements = driver.find_elements_by_xpath('//div[@id="waterfall"]//p[@class="description"]')

        for url_element in url_elements[20 * (page - 1):]:
            download_url = url_element.get_attribute("src")[:-3] + "658"
            pic_info = pic_info_elements[i].get_attribute("data-raw")
            i += 1
            store_path = hash_content + "_" + str(i)
            self.store(download_url, pic_info)

    #存储图片到本地
    def store(self, picture_url, picture_info):
        pic_path = path + '/'+ store_path

        with open(pic_path + '.jpg', 'wb') as f:
            picture = requests.get(picture_url)
            f.write(picture.content)
        print('正在保存图片：' + picture_url)
        print(f'文件：{pic_path}.jpg')

        with open(pic_path + '.txt', 'w', encoding='UTF-8') as f:
            f.write(picture_info)
        print('正在保存图片文字信息：' + picture_url)
        print(f'文件：{pic_path}.txt')

if __name__ == "__main__":
    username = input('请输入花瓣账号名：') # '花瓣账号'
    password = input('请输入账号对应密码：') # '账号密码'
    huaban = Huaban(username, password)
    #获取画板图片信息[淡然小笺赋箴言] http://huaban.com/boards/13448395/
    border_url = 'http://huaban.com/boards/13448395/'
    huaban.get_picture_info_by_border_url(border_url)
