# -*- coding:utf-8 -*-
import Parent
from MyUtil import FileTool
from MyUtil import DateTool
def main():
    # 指定写入文件的名称
    filename = 'test.txt'
    # 执行写入功能函数
    FileTool.write_behind(filename, 'hello')
    FileTool.write_behind(filename, 'world')
    print("1.追加单行写\n", FileTool.read_utf8(filename))

    FileTool.write_behind(filename, '你好！')
    print("1.1.追加写中文\n", FileTool.read_utf8(filename))

    FileTool.write_behind_muti(filename, ['hello', 'world', 'zhangzhang'])
    print("2.追加多行写\n", FileTool.read_utf8(filename))

    FileTool.overwrite(filename, "hello_world!")
    print("1.覆写\n", FileTool.read_utf8(filename))
    
    FileTool.write_behind(filename, '你好，世界！')
    print("1.1.覆写写中文\n", FileTool.read_utf8(filename))



    # 开始进行日期转换
    # 转换之后 返回一个结果对象
    date = DateTool.get_date('2020 2 22')
    #date有三个属性 分别为year，month，day
    print("日期转换")
    print(date.year)
    print(date.month)
    print(date.day)


if __name__ == '__main__':
    main()