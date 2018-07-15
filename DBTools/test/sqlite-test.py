# -*- coding:utf-8 -*-s
import Parent
from MySqlite import MySqlite
import os


###############################################################
####            测试操作     START
###############################################################
def drop_table_test():
    '''删除数据库表测试'''
    print('删除数据库表测试...')
    sqlite.dropTable(TABLE_NAME)


def create_table_test():
    '''创建数据库表测试'''
    print('创建数据库表测试...')
    create_table_sql = '''CREATE TABLE `student` (
                          `id` int(11) NOT NULL,
                          `name` varchar(20) NOT NULL,
                          `gender` varchar(4) DEFAULT NULL,
                          `age` int(11) DEFAULT NULL,
                          `address` varchar(200) DEFAULT NULL,
                          `phone` varchar(20) DEFAULT NULL,
                           PRIMARY KEY (`id`)
                        )'''
    sqlite.createTable(create_table_sql)


def save_test():
    '''保存数据测试...'''
    print('保存数据测试...')
    save_sql = '''INSERT INTO student values (?, ?, ?, ?, ?, ?)'''
    data = [(1, 'Hongten', '男', 20, '广东省广州市',
             '13423****62'), (2, 'Tom', '男', 22, '美国旧金山', '15423****63'),
            (3, 'Jake', '女', 18, '广东省广州市',
             '18823****87'), (4, 'Cate', '女', 21, '广东省广州市', '14323****32')]
    sqlite.insert(save_sql, data)


def fetchall_test():
    '''查询所有数据...'''
    print('查询所有数据...')
    fetchall_sql = '''SELECT * FROM student'''
    sqlite.selectAll(fetchall_sql)


def fetchone_test():
    '''查询一条数据...'''
    print('查询一条数据...')
    fetchone_sql = 'SELECT * FROM student WHERE ID = ? '
    data = 1
    sqlite.selectOne(fetchone_sql, data)

def update_test():
    '''更新数据...'''
    print('更新数据...')
    update_sql = 'UPDATE student SET name = ? WHERE ID = ? '
    data = [('HongtenAA', 1), ('HongtenBB', 2), ('HongtenCC', 3), ('HongtenDD',
                                                                   4)]
    sqlite.update(update_sql, data)


def delete_test():
    '''删除数据...'''
    print('删除数据...')
    delete_sql = 'DELETE FROM student WHERE NAME = ? AND ID = ? '
    data = [('HongtenAA', 1), ('HongtenCC', 3)]
    sqlite.delete(delete_sql, data)


###############################################################
####            测试操作     END
###############################################################


def init():
    '''初始化方法'''
    #数据库文件绝句路径
    global DB_FILE_PATH
    DB_FILE_PATH = os.getcwd() + '/sqlite-test/test.db'
    #数据库表名称
    global TABLE_NAME
    TABLE_NAME = 'student'

    global sqlite
    sqlite = MySqlite(DB_FILE_PATH, TABLE_NAME, True)
    #如果存在数据库表，则删除表
    drop_table_test()
    #创建数据库表student
    create_table_test()
    #向数据库表中插入数据
    save_test()


def main():
    init()
    fetchall_test()
    print('#' * 50)
    fetchone_test()
    print('#' * 50)
    update_test()
    fetchall_test()
    print('#' * 50)
    delete_test()
    fetchall_test()


if __name__ == '__main__':
    main()