# -*- coding:utf-8 -*-
import time
import threading
import multiprocessing
from mzitu_for_thread import MzituThread
from mzitu_es import mzitu_es

SLEEP_TIME = 1
def mzitu_crawler(max_threads=5):
    def pageurl_crawler():
        mzituThread = MzituThread(mzitu_es)
        while True:
            if mzituThread.scrapy_one() is not True:
                time.sleep(SLEEP_TIME)
            
    threads = []
    while True:
        """
        这儿crawl_queue用上了，就是我们__bool__函数的作用，为真则代表我们MongoDB队列里面还有数据
        threads 或者 crawl_queue为真都代表我们还没下载完成，程序就会继续执行
        """
        for thread in threads:
            if not thread.is_alive(): ##is_alive是判断是否为空,不是空则在队列中删掉
                threads.remove(thread)
        while len(threads) < max_threads: ##线程池中的线程少于max_threads 或者 crawl_qeue时
            thread = threading.Thread(target=pageurl_crawler) ##创建线程
            thread.setDaemon(True) ##设置守护线程
            thread.start() ##启动线程
            threads.append(thread) ##添加进线程队列
        time.sleep(SLEEP_TIME)
     
def process_crawler():
    process = []
    num_cpus = multiprocessing.cpu_count()
    print('将会启动进程数为：', num_cpus)
    for i in range(num_cpus):
        p = multiprocessing.Process(target=mzitu_crawler) ##创建进程
        p.start() ##启动进程
        process.append(p) ##添加进进程队列
    for p in process:
        p.join() ##等待进程队列里面的进程结束
 
if __name__ == "__main__":
    #mzituThread = MzituThread(mzitu_es)
    #mzituThread.all_url()  # 抓取所有需要带处理的链接
    process_crawler()