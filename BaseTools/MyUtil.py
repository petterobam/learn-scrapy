# -*- coding:utf-8 -*-
import random,string
from hashlib import md5
import os
import codecs
import tomd

class MyStr():
    @classmethod
    def getRandomPsw(cls, length=6):
        src = string.ascii_letters + string.digits
        if length < 6:
            length = 6
        list_passwd_all = random.sample(src, length - 3) #从字母和数字中随机取3位
        list_passwd_all.extend(random.sample(string.digits, 1))  #让密码中一定包含数字
        list_passwd_all.extend(random.sample(string.ascii_lowercase, 1)) #让密码中一定包含小写字母
        list_passwd_all.extend(random.sample(string.ascii_uppercase, 1)) #让密码中一定包含大写字母
        random.shuffle(list_passwd_all) #打乱列表顺序

    @classmethod
    def getFileMd5(cls, name):
        m = md5()
        a_file = open(name, 'rb')    #需要使用二进制格式读取文件内容
        m.update(a_file.read())
        a_file.close()
        return m.hexdigest()

    @classmethod
    def getMd5(cls, instr, length=32):
        m = md5()
        m.update(instr)
        res = m.hexdigest()
        if length < 32:
            res = random.sample(res, length) #从字母和数字中随机取3位
        return res
    
    @classmethod
    def html2markdown(cls, html):
        mdTxt = tomd.Tomd(html).markdown
        return mdTxt

class FileTool(object):
    #追加写入：写一个写入数据的接口
    @classmethod
    def write_behind(cls, filename, content, split='\n'):
        ''''' 
        :param content: 要写入的数据 
        :param split: 每条数据之间的分隔符 
        :return: 
        '''
        if content == None:
            return
        # 判断传入的参数是否字符串类型，如果是，写入 . 如果不是,抛出异常
        if isinstance(content, str):
            #1.打开文件
            f = codecs.open(filename, 'a', 'utf-8')
            #2.写入数据
            f.write(content)
            f.write(split)
            #3.关闭文件
            f.close()
        else:
            raise TypeError('content must be a str!')

    #追加写入：写入多行数据
    @classmethod
    def write_behind_muti(cls, filename, str_list, split='\n'):
        #判断某个对象是否是某个类型，若是，返回True;否则，返回False
        rs = isinstance(str_list, list)
        #如果为True
        if rs:
            #for循环遍历列表，取出每一数据，判断数据类型是否为字符串
            for content in str_list:
                #如果不是字符串类型
                if isinstance(content,str) == False:
                    #抛出异常
                    raise TypeError('str_list must be a list of "str",ex:["str1","str2"...]')
            #如果没有异常，就可以写入数据了
            #1.打开文件
            f = open(filename,'a')
            #2.写入数据 str1\nstr2\nstr3...
            string = split.join(str_list)
            f.write(string)
            #3.关闭文件
            f.close()
        else:
            #如果传入的不是列表，抛出异常
            raise TypeError('str_list must be a list of "str",ex:["str1","str2"...]')
    #创建文件夹
    @classmethod
    def mkdir(cls, path):  ##这个函数创建文件夹
        isExists = os.path.exists(path)
        if not isExists:
            print('建了一个名字叫做', path, '的文件夹！')
            os.makedirs(path)
            return True
        else:
            print('名字叫做', path, '的文件夹已经存在了！')
            return False
    #读取文件内容
    @classmethod
    def read_utf8(cls, path):
        isExists = os.path.exists(path)
        if isExists:
            with open(path, 'r', encoding='UTF-8') as f:
                return str(f.read())
        else:
            return ''
    # 覆盖写入
    @classmethod
    def overwrite(cls, path, text):
        with open(path, 'w', encoding='UTF-8') as f:
            f.write(text)

    # 判断文件是否存在
    @classmethod
    def isExit(cls, path):
        return os.path.exists(path)

    # 检查文件名是否合理，替换特殊字符
    @classmethod
    def replace_invalid_filename(cls, filename, replaced_char='_'):
        '''
        替换有特殊字符的文件名中的特殊字符，默认将特殊字符替换为'_'.
        例如 C/C++ -> C_C++
        '''
        valid_filename = filename
        invalid_characaters = '\\/:*?"<>|'
        for c in invalid_characaters:
            #print 'c:', c
            valid_filename = valid_filename.replace(c, replaced_char)
        return valid_filename 


class DateTool(object):
    #日期格式化工具类，用类执行一个函数，返回一个对象，对象分别有year\month\day
    '''
    2018-2-1 2018.2.1 2018/2/1 
    date.year = 2018 
    date.month = 2 
    date.day = 1 
    '''
    #初始化函数
    def __init__(self,year=1970,month=1,day=1):
        self.year = year
        self.month = month
        self.day = day
    #类函数，传递进来一个日期，返回一个该类的对象
    @classmethod
    def get_date(cls,date):
        #判断date是否为str类型
        if not isinstance(date,str):
            #不是str类型，直接触发异常
            raise TypeError('date must be a str!')
        #转换
        #判断是-还是.还是空格
        if '-' in date:
            #分别将2018赋值year 2赋值给month 1赋值给day
            # year, month, day = [2018,2,1]
            year,month,day = list(map(int,date.split('-')))
        elif '.' in date:
            year,month,day = list(map(int,date.split('.')))
        elif ' ' in date:
            year,month,day = list(map(int,date.split(' ')))
        elif '/' in date:
            year,month,day = list(map(int,date.split('/')))
        #创建对象
        # obj = DateTool(year,month,day)
        obj = cls(year,month,day)
        #返回对象
        return obj