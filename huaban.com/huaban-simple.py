from selenium import webdriver
import time
import os
import requests


class Huaban():
    def __init__(self, username, password):
        self.username = username
        self.password = password

    # 获取图片url并存到列表urls_list
    def get_picture_url(self, content):
        global path
        path = "./" + content
        # 保存图片到磁盘文件夹 file_path中，默认为当前脚本运行目录下的文件夹
        if not os.path.exists(path):
            os.makedirs(path)
        url = "http://huaban.com"
        # 使用Chrome浏览器模拟打开网页，但是要把下载的chromedriver.exe放在python的文件路径下,
        # 调试好之后换成PhantomJs,速度应该会快一点
        # driver = webdriver.PhantomJs() 
        # 下拉滑动浏览器屏幕，具体下拉多少根据自己实际情况决定
        driver = webdriver.PhantomJS()
        #driver = webdriver.Chrome()
        # 设置全屏
        driver.maximize_window()
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
        #搜索图片
        driver.find_elements_by_xpath('//input[@placeholder="搜索你喜欢的"]')[0].send_keys(content)
        driver.find_elements_by_xpath('//form[@id="search_form"]/a')[0].click()
        time.sleep(5)
        i = 0
        page = 1
        global name
        global store_path
        global urls_list
        urls_list = []
        #获取图片的总数
        pictures_count = driver.find_elements_by_xpath('//a[@class="selected"]/i')[0].text
        print(pictures_count)
        pages = int(int(pictures_count) / 20)
        print(pages)
        #匹配到图片url所在的元素
        url_elements = driver.find_elements_by_xpath('//span[@class="stop"]/../img')
        #遍历图片元素的列表获取图片的url
        for url_element in url_elements:
            picture_url = url_element.get_attribute("src")[:-3] + "658"
            #防止获取重复的图片url
            if picture_url not in urls_list:
                urls_list.append(picture_url)
        while page <= pages:
            while len(urls_list) < 20*page:
                driver.execute_script("window.scrollBy(0,1000)")
                time.sleep(3)
                url_elements = driver.find_elements_by_xpath('//span[@class="stop"]/../img')
                for url_element in url_elements:
                    picture_url = url_element.get_attribute("src")[:-3] + "658"
                    if picture_url not in urls_list:
                        urls_list.append(picture_url)
            print("第%s页" % page)

            for download_url in urls_list[20*(page-1):20*page]:
                i += 1
                name = content + "_" + str(i)
                store_path = name + '.jpg'
                self.store(download_url)
            page += 1
        #最后一页
        print("第%s页" % int(page))

        while len(urls_list) < int(pictures_count):
            driver.execute_script("window.scrollBy(0,1000)")
            time.sleep(3)
            url_elements = driver.find_elements_by_xpath('//span[@class="stop"]/../img')
            for url_element in url_elements:
                picture_url = url_element.get_attribute("src")[:-3] + "658"
                if picture_url not in urls_list:
                    urls_list.append(picture_url)
        for download_url in urls_list[20*(page-1): ]:
            i += 1
            name = content + "_" + str(i)
            store_path = name + '.jpg'
            self.store(download_url)

    #存储图片到本地
    def store(self, picture_url):
        picture = requests.get(picture_url)
        f = open(path + '\\'+ store_path, 'wb')
        f.write(picture.content)
        print('正在保存图片：' + picture_url)
        print('文件：' + name)

if __name__ == "__main__":
    content = '迪丽热巴'
    username = '1460300366@qq.com' # '花瓣账号'
    password = '111237' # '账号密码'
    huaban = Huaban(username, password)
    huaban.get_picture_url(content)
