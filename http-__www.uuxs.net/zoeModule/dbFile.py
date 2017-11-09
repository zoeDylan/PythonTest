# 模拟一个简单的数据存储

import os
import time


class DbFile(object):

    # 初始化
    # name: 存储名称，*注意冲突
    # dbType: 存储类型
    def __init__(self, name, dbType='dict'):

        # 文件路径、名称、类型、文件对象、是否可以保存、错误信息、数据
        self.__path = './zoeModule/dbFileData/' + name + '.db.txt'
        self.__name = name
        self.__type = dbType
        self.__fileExists = os.path.exists(self.__path)

        # 有文件，只读模式打开，没有文件，写入模式打开
        self.__file = open(
            self.__path, 'r' if self.__fileExists else 'w+', -1, 'utf-8')

        self.__canSave = True
        self.__error = ''

        readCont = self.__file.read()

        # 有文件获取文件，没有文件初始化一个文件
        self.__db = eval(readCont) if len(readCont) > 0 else {
            'name': self.__name,
            'type': dbType,
            'data': {} if dbType == 'dict' else '',
            '__insert': time.time(),
            '__update': time.time()
        }

        # 判断是否有写入权限
        if self.__db['type'] != dbType:
            self.__canSave = False
            self.__error = 'dbType error: dbType != save=>DbType'
        self.__file.close()

        # 没有文件，将数据写入
        if not(self.__fileExists):
            self.save()

    # 获取数据
    # 返回数据
    def __get_data(self):
        return self.__db['data']
    data = property(__get_data)

    # 保存数据
    # 根据类型保存数据
    # 有写入权限进行保存，没有权限返回报错信息
    def save(self, op=False, val=''):
        if self.__canSave:
            # 进行数据操作
            if op:
                self.setData(op, val)

            # 存储
            self.__file = open(self.__path, 'w', -1, 'utf-8')
            self.__file.write(str(self.__db))
            self.__file.close()
            return True
        else:
            return self.__error

    # 设置数据
    def setData(self, op, val=''):
        if op:
            self.__db['__update'] = time.time()
            if self.__type == 'dict':
                # 字典操作
                if type(op) == type({}):
                    data = self.__db['data']
                    data.update(op)
                    self.__db['data'] = data
                elif type(op) == type(''):
                    self.__db['data'][op] = val
            elif self.__type == 'str':
                self.__db['data'] = op
