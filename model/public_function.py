import re
import time
import os
import shutil
import sqlite3
import copy
from model import chinesization as ch

DICTHEAD = ["address",
            "face",
            "classify",
            "book_name",
            "Cxx",
            "chinesization",
            "favourite",
            "date",
            "unread",
            "original_name",
            "new_name",
            "author"]


# 只是提出参考
def book_name_cut(name: str):
    newBook = {
        "face": "",                             # 不预设
        "classify": "",                         # 不预设
        "book_name": "",                        # 预设
        "Cxx": "C00",                           # 预设
        "chinesization": "未知",                # 预设
        "author": "未知",                       # 预设
        "favourite": 0,                         # 不预设
        "date": time.strftime("%Y-%m-%d"),      # 预设
        "address": "",                          # 不预设
        "unread": 0,                            # 不预设
        "original_name": name,                  # 预设
        "new_name": ""                          # 不预设
    }
    comic_market = re.search(r"C\d{2,3}", name, re.I)
    name = re.sub(r"\(C\d{2,3}\)", '', name)
    if comic_market:
        comic_market = comic_market.group()
        newBook['Cxx'] = comic_market
    # 匹配作者和汉化组
    name = name.replace('【', '[')
    name = name.replace('】', ']')
    # 用于判断是否为汉化组
    chss = ch.all_name
    part = ch.part
    chss = set(chss)
    book_name = re.findall(r'\[[^\[\]]*\]', name)
    name = re.sub(r'\[[^\[\]]*\]', '', name)
    is_find = False
    # 汉化组的匹配规则
    # 首先在完整的汉化组名字集合里找如果没有，就找可能是汉化组的字段
    for i in book_name:
        if i in chss:
            is_find = True
            newBook['chinesization'] = i[1:-1]
            book_name.remove(i)
            break
    if not is_find:
        for i in part:
            for j in book_name:
                res = re.search(i, j)
                if res:
                    is_find = True
                    newBook['chinesization'] = j[1:-1]
                    book_name.remove(j)
                    break
    if book_name:
        newBook['author'] = book_name[0][1:-1]
    newBook['book_name'] = name.replace(' ', '')
    return newBook


def addNewBook(book_: dict, out_box):
    # print(book_['original_path'], book_['address'])
    try:
        res = True
        conn = sqlite3.connect('./data/data.db')
        cursor = conn.cursor()
        # 把书收入库
        author_all = os.listdir('./books')
        if author_all.count(book_['author']) == 0:
            os.makedirs('./books/'+book_['author'])
        os.renames(book_['original_path'], book_['address'])
        book_info = []
        # 把值单独作为数组
        for i in DICTHEAD:
            book_info.append(book_[i])
        cursor.execute('''insert into books values (?,?,?,?,?,?,?,?,?,?,?,?)''', book_info)
    except Exception:
        print('insertError!')
        res = False
        out_box.append(time.strftime("%Y-%m-%d %H:%M") + '插入失败！' + book_['new_name'])
    finally:
        cursor.close()
        if res:
            conn.commit()
        conn.close()
        out_box.append(time.strftime("%Y-%m-%d %H:%M") + '已插入:' + book_['new_name'] + "。")
        return res


# 修改书本信息, 此操作会删除原书然后插入修改后的书
def modifyBookInfo(book_: dict, out_box):
    try:
        res = True
        conn = sqlite3.connect('./data/data.db')
        cursor = conn.cursor()
        # 把书收入库
        author_all = os.listdir('./books')
        if author_all.count(book_['author']) == 0:
            os.makedirs('./books/'+book_['author'])
        if book_['original_path'] != book_['address']:
            os.renames(book_['original_path'], book_['address'])
        book_info = []
        # 把值单独作为数组
        for i in DICTHEAD:
            book_info.append(book_[i])
        cursor.execute('''delete from books where address=?''', [book_['original_path']])
        cursor.execute('''insert into books values (?,?,?,?,?,?,?,?,?,?,?,?)''', book_info)
    except Exception:
        print('modifyError!')
        res = False
        out_box.append(time.strftime("%Y-%m-%d %H:%M") + '修改失败！')
    finally:
        cursor.close()
        if res:
            conn.commit()
        conn.close()
        out_box.append(time.strftime("%Y-%m-%d %H:%M") + '修改成功。')


# 传入要插入的分类名, 返回插入状态 bool
def addNewClassify(classify_name: list):
    try:
        conn = sqlite3.connect('./data/data.db')
        cursor = conn.cursor()
        for i in classify_name:
            cursor.execute("insert into classify values (?,'')", [i])
        res = True
    except Exception:
        print("添加分类失败！")
        res = False
    finally:
        cursor.close()
        if res:
            conn.commit()
        conn.close()
        return res


# 传入要删除的分类名, 返回插入状态 bool
def deleteClassify(classify_name: str):
    try:
        conn = sqlite3.connect('./data/data.db')
        cursor = conn.cursor()
        cursor.execute("delete from classify where name=?", [classify_name])
        res = True
    except Exception:
        print("删除分类失败！")
        res = False
    finally:
        cursor.close()
        if res:
            conn.commit()
        conn.close()
        return res


# 返回包含完整书本信息的dict列表，使用glob查找
def getBookList(classify_name: str, out_box=None):
    try:
        conn = sqlite3.connect('./data/data.db')
        cursor = conn.cursor()
        if classify_name == '喜欢':
            data = cursor.execute("select * from books where favourite=1").fetchall()
        elif classify_name == '未看':
            data = cursor.execute("select * from books where unread=1").fetchall()
        elif classify_name == '所有':
            data = cursor.execute("select * from books").fetchall()
        elif classify_name == '未分类':
            data = cursor.execute("select * from books where classify='' ").fetchall()
        else:
            data = cursor.execute("select * from books where classify glob ? ", ['*'+classify_name+'*']).fetchall()
        return toDictList(data)
    except Exception:
        print('获取目录失败！')
        if out_box:
            out_box.append(time.strftime("%Y-%m-%d %H:%M") + '获取目录失败！')
    finally:
        cursor.close()
        conn.close()
        # if out_box:
        #     out_box.append(time.strftime("%Y-%m-%d %H:%M") + '获取列表完毕。')


# 书名切割
def bookNameCut(book_name: str):
    return book_name_cut(book_name)


# 从当前分类删除
def deleteBookClassify(book_address: str, out_box, classify_name=None):
    try:
        # print(book_address, classify_name)
        conn = sqlite3.connect('./data/data.db')
        cursor = conn.cursor()
        # 删除未读
        if classify_name == '未看':
            cursor.execute('update books set unread=0 where address=?', [book_address])
        # 删除喜欢的书
        elif classify_name == '喜欢':
            cursor.execute('update books set favourite=0 where address=?', [book_address])
        # 从特定分类中删除
        else:
            # # 获取分类下所有书
            # cursor.execute("select book_list from classify where name=?", [classify_name])
            # book_list = cursor.fetchall()
            # book_list = json.loads(book_list)
            # book_list.remove(book_address)
            # cursor.execute("update classify set book_list=? where name=?", [json.dumps(book_list), classify_name])
            # 在书的分类列表中移除分类
            classify_list = cursor.execute("select classify from books where address=?", [book_address]).fetchall()[0][0]
            print(classify_list)
            classify_list = classify_list.split()
            classify_list.remove(classify_name)
            classify_list = str(classify_list)
            classify_list = classify_list[1: -1].replace('\'', '')
            cursor.execute("update books set classify=? where address=?", [classify_list.replace(',', ''), book_address])
        res = True
    except Exception as e:
        res = False
        out_box.append(time.strftime("%Y-%m-%d %H:%M") + '移除失败。')
        print('删除时出现错误!')
        print(e)
    finally:
        cursor.close()
        if res:
            conn.commit()
        conn.close()
        out_box.append(time.strftime("%Y-%m-%d %H:%M") + '移除完毕。')


# 为书本添加分类
def addBookClassify(book_address: str, out_box, classify_name=None):
    try:
        conn = sqlite3.connect('./data/data.db')
        cursor = conn.cursor()
        # 添加未读
        if classify_name == '未看':
            cursor.execute('update books set unread=1 where address=?', [book_address])
        # 添加喜欢的书
        elif classify_name == '喜欢':
            cursor.execute('update books set favourite=1 where address=?', [book_address])
        # 添加到特定分类中
        else:
            # 在书的分类列表中移除分类
            classify_list = cursor.execute("select classify from books where address=?", [book_address]).fetchall()[0][0]
            print(classify_list)
            classify_list = classify_list.split()
            classify_name = classify_name.split()
            for i in classify_name:
                if classify_list.count(i) == 0:
                    classify_list.append(i)
            classify_list = str(classify_list)
            classify_list = classify_list[1: -1].replace('\'', '')
            cursor.execute("update books set classify=? where address=?", [classify_list.replace(',', ''), book_address])
        res = True
    except Exception as e:
        res = False
        out_box.append(time.strftime("%Y-%m-%d %H:%M") + '添加失败。')
        print('删除时出现错误!')
        print(e)
    finally:
        cursor.close()
        if res:
            conn.commit()
        conn.close()


# 彻底删除此书
def deleteBook(book_address: str, out_box):
    # 删除目录
    try:
        conn = sqlite3.connect('./data/data.db')
        cursor = conn.cursor()
        if os.path.exists(book_address):
            shutil.rmtree(book_address)
        # # 获得这本书所有的分类
        # cursor.execute('select classify from books where address=?', [book_address])
        # classify_list = cursor.fetchall()[0][0]
        # classify_list = classify_list.split()
        # 删除这本书
        cursor.execute("delete from books where address=?", [book_address])
        # # 删除对应分类下的书本
        # for i in classify_list:
        #     cursor.execute("select book_list from classify where name=?", i)
        #     book_list = cursor.fetchall()
        #     book_list = json.loads(book_list)
        #     book_list.remove(i)
        #     cursor.execute("update classify set book_list=? where name=?", [json.dumps(book_list), i])
        res = True
    except Exception as e:
        res = False
        out_box.append(time.strftime("%Y-%m-%d %H:%M") + '移除失败。')
        print('删除时出现错误!')
    finally:
        cursor.close()
        if res:
            conn.commit()
        conn.close()


# sqlite 返回值转为dict列表
def toDictList(book_list: list):
    model = {
            "address": None,
            "face": None,
            "classify": "",
            "book_name": None,
            "Cxx": "C00",
            "chinesization": "未知",
            "favourite": 0,
            "date": time.strftime("%Y-%m-%d"),
            "unread": 0,
            "original_name": "",
            "new_name": "",
            "author": "未知",
        }
    temp = []
    for i in book_list:
        newBook = copy.deepcopy(model)
        # 给newBook每一个元素赋值
        for j in range(12):
            newBook[DICTHEAD[j]] = i[j]
        temp.append(newBook)
    return temp


# 获得所有分类名返回分类名列表
def getAllClassifyName():
    try:
        conn = sqlite3.connect('./data/data.db')
        cursor = conn.cursor()
        classify_list = cursor.execute('select name from classify').fetchall()
        for i in range(len(classify_list)):
            classify_list[i] = classify_list[i][0]
    except Exception:
        print('查找失败')
    finally:
        cursor.close()
        conn.close()
        return classify_list
