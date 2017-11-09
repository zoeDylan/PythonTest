# 抓取内容生成TXT
from zoeModule.loadPage import LoadPage
from zoeModule.dbFile import DbFile as DB
from pyquery import PyQuery as PQ
import os
import time

print('输入小说缩小名:')
name = input()
db = DB(name)
maxLength = len(db.data)
nowTime = time.time()
print('\n准备合并文件:', maxLength)
for i, data in enumerate(db.data):
    print('正在合并：%s/%s' % (i + 1, maxLength))
    lp = LoadPage(data)
    contPQ = PQ(lp.data)
    title = PQ(contPQ('#BookTitle')).html()
    cont = PQ(contPQ('#BookText')).html().replace('<br/>', '\n')
    path = name + '.txt'
    if os.path.exists(path):
        file = open(path, 'a', -1, 'utf-8')
        file.write('\n\n' + title + '\n' + cont)
        file.close()
    else:
        file = open(path, 'w', -1, 'utf-8')
        file.write('\n\n' + title + '\n' + cont)
        file.close()

print('\n\n合并完成：\n文件名称：%s\n耗时：%s秒' %
      (name + '.txt', round(time.time() - nowTime, 2)))
