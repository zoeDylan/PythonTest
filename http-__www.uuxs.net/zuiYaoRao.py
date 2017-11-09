from zoeModule.loadPage import LoadPage
from zoeModule.dbFile import DbFile as DB
from pyquery import PyQuery as PQ
import threadpool
import random
import os


# 从这里开始配置
# 示例：'http://www.uuxs.net/book/0/57/'
hostURL = 'http://www.uuxs.la/book/40/40873/'
name = '最妖娆'
db = DB('zuiYaoRao_list')
# 配置结束


db.save()
state = {
    'success': 0,
    'all': 0,
    'forCache': 0,
    'forNet': 0,
    'error': 0,
    'errList': []
}


def threadLoadCont(data=None, i=None):
    nowData = db.data[data]
    maxLength = len(db.data)
    if not(nowData['isLoad']):
        # 加载内容页面 存储内容数据
        try:
            loadContPage = LoadPage(nowData['url'], 'gbk')
            contPQ = PQ(loadContPage.data)
            nowData['isLoad'] = True
            db.save(nowData['url'], nowData)
            state['success'] += 1
        except:
            state['error'] += 1
            state['errList'].append(nowData['url'])

            # 如果从缓存中读取则不进行休眠
        if loadContPage.isCache:
            state['forCache'] += 1
            print('已缓存，解析文件中：%s %s/%s ' %
                  (nowData['url'], str(i + 1), maxLength))
        else:
            state['forNet'] += 1
            print('正在抓取：%s,进度：%s/%s' %
                  (nowData['url'], str(i + 1), maxLength))
# 加载内页


def loadCont():
    pool = threadpool.ThreadPool(10)
    argList = []
    [argList.append((None, {'data': data, 'i': i}))
     for i, data in enumerate(db.data)]
    state['all'] = len(db.data)
    # threadLoadCont(data, i)
    mReq = threadpool.makeRequests(threadLoadCont, argList)
    [pool.putRequest(req) for req in mReq]
    pool.wait()

    # 加载主界面
loadPage = LoadPage(hostURL, 'gbk')

# a标签
aList = PQ(loadPage.data)('dl.chapterlist a')

# 提取全部a标签存入数据
for i in aList:
    aElem = PQ(i)
    title = aElem.html()
    url = hostURL + aElem.attr('href')
    if not(url in db.data):
        db.setData(url, {
            'title': title,
            'url': url,
            'isLoad': False
        })
# 保存
db.save()
loadCont()
print('\n\n抓取:【%s】\n总章节：%s\n成功：%s\n失败:%s\n缓存读取:%s\n网络抓取:%s\n错误地址：' %
      (hostURL, state['all'], state['success'], state['error'], state['forCache'], state['forNet']), state['errList'])
