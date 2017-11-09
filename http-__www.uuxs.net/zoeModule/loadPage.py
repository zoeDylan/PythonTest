# 获取页面

from zoeModule.dbFile import DbFile as DB
import requests
import time
import random
import chardet
import hashlib
import os

filePath = './zoeModule/loadPage/'
db = DB('loadPage')
if not(os.path.exists(filePath)):
    os.mkdir(filePath)
"""
    db：数据格式
    db.data = {
        url:{
            name: 爬取后存储文件名称 str
            url: 爬取页面地址 str
            __update: 更新时间 float
        }
    }
"""


class LoadPage(object):

    def __init__(self, url,  encode='utf-8'):
        md5 = hashlib.md5()
        md5.update(url.encode('utf-8'))
        self.__url = url
        self.__fileName = md5.hexdigest()
        self.__path = filePath + self.__fileName + '.db.txt'
        self.__encode = encode

        # 有数据记录读取历史文件 没有则抓取
        if url in db.data:
            nowData = db.data[url]
            nowFile = open(self.__path, 'r', -1, 'utf-8')
            self.__data = nowFile.read()
            nowFile.close()
            self.isCache = True
        else:
            req = self.__getReq()
            self.__data = req.text
            data = {}
            data[self.__url] = {}
            data[self.__url]['path'] = self.__fileName
            data[self.__url]['url'] = self.__url
            data[self.__url]['__update'] = time.time()
            nowFile = open(self.__path, 'w+', -1, 'utf-8')
            nowFile.write(self.__data)
            db.save(data)
            self.isCache = False
            nowFile.close()

    # 更新内容
    def update(self):
        req = self.__getReq()
        self.__data = req.text
        data = db.data[self.__url]
        data['__update'] = time.time()
        nowFile = open(self.__path, 'w+', -1, 'utf-8')
        nowFile = open(self.__path, 'w+')
        nowFile.write(self.__data)
        db.save(data)
        nowFile.close()

    def __get_data(self):
        return self.__data

    def __getReq(self):
        sleepTime = random.randint(1, 3)
        print('安全策略-休眠：%s秒' % (sleepTime))
        req = requests.get(self.__url)
        req.encoding = self.__encode
        return req

    data = property(__get_data)
