# -*- coding: utf-8 -*-
# 导入scrapy包
import os
import scrapy
from bs4 import BeautifulSoup
# 一个单独的 request 的模块，需要跟进 URL 的时候，需要用它
from scrapy.http import Request
# 这是我定义的需要保存的字段，（导入项目中，items文件中的 BaseScrapyItem 类）
from base_scrapy.items import BaseScrapyItem

# 在 Scrapy 框架根目录，控制台输入： scrapy crawl base_spider -o data/base_spider/item.json
class BaseSpider(scrapy.Spider):
    # 爬虫名字，定义后在项目根目录: scrapy crawl {name} ，运行该爬虫
    name = 'base_spider'
    # 定义一些常量
    data_dir = 'data'
    allowed_domains = ['baidu.com']
    bash_url = 'https://www.baidu.com/s?wd='

    def start_requests(self):
        for i in range(1, 10):
            url = self.bash_url + str(i)
            # 爬取到的页面 提交 给 parse 方法处理
            yield Request(url, self.parse)

    def parse(self, response):
        '''
        start_requests 已经爬取到页面，那如何提取我们想要的内容，可以在这个方法里面定义。
        也就是用xpath、正则、或是css进行相应提取，这个例子就是让你看看scrapy运行的流程：
        1、定义链接；
        2、通过链接爬取（下载）页面；
        3、定义规则，然后提取数据；（当前步骤）
        '''
        # # 根据上面的链接提取个数，文件名：baidu.com-{n}.txt
        # file_name = self.allowed_domains[0] + '-' + response.url.split("=")[-1] + '.txt'
        # # 文件路径
        # file_path = os.path.join(self.data_dir, self.name)
        # # 创建文件夹
        # if not os.path.exists(file_path):
        #     os.makedirs(file_path)
        # # 拼接文件名
        # file_full_name = os.path.join(file_path, file_name)
        # with open(file_full_name, 'wb') as f:        
        #     # python文件操作，不多说了；
        #     f.write(response.body)
        # # 打个日志
        # self.log('保存文件: %s' % file_full_name)
        item = BaseScrapyItem()
        item['url'] = response.url
        item['status'] = response.status
        # item['headers'] = str(response.headers, encoding='utf8')
        item['body'] = str(response.body, encoding='utf8')
        yield item