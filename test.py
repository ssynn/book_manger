import json
import os
import shutil
import time
import difflib
import sqlite3
from model import public_function as pf
# 打开JSON读取数据，修改，保存
# with open("./config/books.json", "r") as books:
#     book = books.read()
#     book = json.loads(book)

# add = book[".\\books\呵呵呵\[chin] サクセックスストーリーズ"]["address"]
# add = ".\\books\呵呵呵\[chin] サクセックスストーリーズ"
# print(os.listdir(add))

# with open("./config/books.json", "w") as books:
#     book = json.dumps(book)
#     books.write(book)

# # 文件移动
# src = "サクセックスストーリーズ"
# dst = ".\\books\呵呵呵2"
# shutil.move(src, dst)

# # 获取时间
# a = time.time()
# print(time.strftime("%Y-%m-%d"))

# a = []
# for i in book:
#     a.append(book[i])
# print(a[0]['time'])

# 比较差异性
# str1 = '1234567'
# str2 = '123456'
# print(difflib.SequenceMatcher(None, str1, str2).quick_ratio())

# a = os.listdir('./')
# print(a)

# 拼接路径
# print(os.path.join('.\\books', 'a', 'b'))

# print(time.strftime("%Y-%m-%d %H:%M"))

# !/usr/bin/python

# print(os.path.abspath('./books\H-SQUAD (ぐりえるも)\[H-SQUAD (ぐりえるも)]わたしたちの行為特別実習-戯編-(オリジナル)C94'))

# a = ['1', '3333', '324234']
# a = json.dumps(a)
# print(type(a))

# a = {}
# a['1']=1
# a['2']=2
# a['3']=3
# for i in a:
#     print(i)

# 测试在except中return
# def hehe(ss):
#     try:
#         a = 5 / ss
#     except ZeroDivisionError as e:
#         print(e)

#     finally:
#         return True


# print(hehe(0))


# a = [1, 2, 3, 4]
# b = str(a)
# b = b[1: -1]
# print(b)
# b = b.replace(', ', ' ')
# print(b)
# print(b.split())

# a = [1, 2, 3, 4]
# b = [2, 3, 5]
# a.append(b)
# a.extend(b)
# print(a)

name = '[秋月伊槻] イビツナ彼女は年中「発情期!!」[4K[S版]掃圖組]'
print(pf.book_name_cut(name))