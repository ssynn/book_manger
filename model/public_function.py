import re
import time
import os
import shutil
import sqlite3
import copy
from PIL import Image
from model import chinesization as ch
from PyQt5.QtCore import QThread, pyqtSignal

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


# 加入新书时会开一个子线程，作者改变时会发送作者名称，书移动完成后会发送状态信息，最发送操作结果
class AddNewBook(QThread):
    stateChange = pyqtSignal(str)
    authorChange = pyqtSignal(str)
    end = pyqtSignal()

    def __init__(self, book_):
        super().__init__()
        self.book_ = book_

    def run(self):
        try:
            conn = sqlite3.connect('./data/data.db')
            cursor = conn.cursor()
            if len(cursor.execute('''select original_name from books where original_name=?''', [self.book_['original_name']]).fetchall()) != 0:
                raise Exception
            # 把书收入库
            author_all = os.listdir('./books')
            # 没有对应的作者目录则需要建立对应的作者目录
            if author_all.count(self.book_['author']) == 0:
                os.makedirs('./books/'+self.book_['author'])
                self.authorChange.emit(self.book_['author'])
            # 把书移动到books文件夹内
            self.stateChange.emit(time.strftime("%Y-%m-%d %H:%M") + '开始添加：' + self.book_['new_name'] + ',请不要进行其他操作!')
            # 移动之前先产生缩略图
            makeFace(os.path.join(self.book_['original_path'], self.book_['face']))
            shutil.move(self.book_['original_path'], self.book_['address'])
            # 把dict内的值提取作为数组
            book_info = []
            for i in DICTHEAD:
                book_info.append(self.book_[i])
            cursor.execute('''insert into books values (?,?,?,?,?,?,?,?,?,?,?,?)''', book_info)
            # 记录执行结果
            res = True
        except Exception as e:
            print(e)
            res = False
            self.stateChange.emit(time.strftime("%Y-%m-%d %H:%M") + '添加失败！' + self.book_['new_name'])
        finally:
            if res:
                conn.commit()
                self.stateChange.emit(time.strftime("%Y-%m-%d %H:%M") + '已添加:' + self.book_['new_name'] + "。")
            cursor.close()
            conn.close()
            self.end.emit()


# 同时加入多本新书
class AddNewBookS(QThread):
    stateChange = pyqtSignal(str)
    authorChange = pyqtSignal(str)
    end = pyqtSignal()

    def __init__(self, books: list):
        super().__init__()
        self.books = books

    def run(self):
        self.conn = sqlite3.connect('./data/data.db')
        self.cursor = self.conn.cursor()
        self.author_all = os.listdir('./books')
        cnt = 0
        self.no = 1
        self.stateChange.emit(time.strftime("%Y-%m-%d %H:%M") + '正在批量添加,请不要进行其他操作!')
        for i in self.books:
            cnt += int(self.process(i))
            self.no += 1
        self.stateChange.emit(
            time.strftime("%Y-%m-%d %H:%M") +
            "成功添加:" +
            str(cnt) +
            "个，失败:" +
            str(len(self.books)-cnt) + "个。"
        )
        self.cursor.close()
        self.conn.close()
        self.end.emit()

    def process(self, book_):
        res = False
        try:
            if len(self.cursor.execute('''select original_name from books where original_name=?''', [book_['original_name']]).fetchall()) != 0:
                raise Exception
            # 没有对应的作者目录则需要建立对应的作者目录
            if self.author_all.count(book_['author']) == 0:
                os.makedirs('./books/'+book_['author'])
                self.author_all.append(book_['author'])
                self.authorChange.emit(book_['author'])
            # 把书移动到books文件夹内
            self.stateChange.emit(time.strftime("%Y-%m-%d %H:%M") + '开始添加：('+str(self.no) + '/' + str(len(self.books)) + ')' + book_['new_name'])
            # 移动之前先产生缩略图
            makeFace(os.path.join(book_['original_path'], book_['face']))
            shutil.move(book_['original_path'], book_['address'])
            # 把dict内的值提取作为数组
            book_info = []
            for i in DICTHEAD:
                book_info.append(book_[i])
            self.cursor.execute('''insert into books values (?,?,?,?,?,?,?,?,?,?,?,?)''', book_info)
            res = True
        except Exception as e:
            print(e)
            self.stateChange.emit(time.strftime("%Y-%m-%d %H:%M") + '添加失败！' + book_['new_name'])
        finally:
            if res:
                self.conn.commit()
                self.stateChange.emit(time.strftime("%Y-%m-%d %H:%M") + '已添加:' + book_['new_name'] + "。")

            return res


# 修改书的信息，子线程，作者改变时会发送作者名称，书移动完成后会发送状态信息，最发送操作结果
class ModifyBookInfo(QThread):
    stateChange = pyqtSignal(str)
    authorChange = pyqtSignal(str)
    end = pyqtSignal()

    def __init__(self, book_):
        super().__init__()
        self.book_ = book_

    def run(self):
        try:
            conn = sqlite3.connect('./data/data.db')
            cursor = conn.cursor()
            # 把书收入库
            author_all = os.listdir('./books')
            # 没有对应的作者目录则需要建立对应的作者目录
            if author_all.count(self.book_['author']) == 0:
                os.makedirs('./books/'+self.book_['author'])
                self.authorChange.emit(self.book_['author'])
            # 把书移动到books文件夹内
            # 移动之前先产生缩略图
            makeFace(os.path.join(self.book_['original_path'], self.book_['face']))
            if self.book_['original_path'] != self.book_['address']:
                shutil.move(self.book_['original_path'], self.book_['address'])
            # 把dict内的值提取作为数组
            book_info = []
            for i in DICTHEAD:
                book_info.append(self.book_[i])
            cursor.execute('''delete from books where address=?''', [self.book_['original_path']])
            cursor.execute('''insert into books values (?,?,?,?,?,?,?,?,?,?,?,?)''', book_info)
            res = True
        except Exception:
            print('modifyError!')
            res = False
            self.stateChange.emit(time.strftime("%Y-%m-%d %H:%M") + '修改失败！')
        finally:
            if res:
                conn.commit()
                self.stateChange.emit(time.strftime("%Y-%m-%d %H:%M") + '修改成功。')
                self.end.emit()
            cursor.close()
            conn.close()


# 修改书的信息，子线程，作者改变时会发送作者名称，书移动完成后会发送状态信息，最发送操作结果
class ModifyMultiBookInfo(QThread):
    stateChange = pyqtSignal(str)
    authorChange = pyqtSignal(str)
    end = pyqtSignal()

    def __init__(self, bookList: list):
        super().__init__()
        self.bookList = bookList

    def run(self):
        self.conn = sqlite3.connect('./data/data.db')
        self.cursor = self.conn.cursor()
        cnt = 0
        self.no = 1
        self.stateChange.emit(time.strftime("%Y-%m-%d %H:%M") + '正在批量添加,请不要进行其他操作!')
        for i in self.bookList:
            self.book_ = i
            cnt += int(self.process())
            self.no += 1
        self.stateChange.emit(
            time.strftime("%Y-%m-%d %H:%M") +
            "成功修改:" +
            str(cnt) +
            "个，失败:" +
            str(len(self.bookList)-cnt) + "个。"
        )
        self.cursor.close()
        self.conn.close()
        self.end.emit()

    def process(self):
        try:
            # 把书收入库
            author_all = os.listdir('./books')
            # 没有对应的作者目录则需要建立对应的作者目录
            if author_all.count(self.book_['author']) == 0:
                os.makedirs('./books/'+self.book_['author'])
                self.authorChange.emit(self.book_['author'])
            # 把书移动到books文件夹内
            # 移动之前先产生缩略图
            makeFace(os.path.join(self.book_['original_path'], self.book_['face']))
            if self.book_['original_path'] != self.book_['address']:
                shutil.move(self.book_['original_path'], self.book_['address'])
            # 把dict内的值提取作为数组
            book_info = []
            for i in DICTHEAD:
                book_info.append(self.book_[i])
            self.cursor.execute('''delete from books where address=?''', [self.book_['original_path']])
            self.cursor.execute('''insert into books values (?,?,?,?,?,?,?,?,?,?,?,?)''', book_info)
            res = True
        except Exception:
            print('modifyError!')
            res = False
            self.stateChange.emit(time.strftime("%Y-%m-%d %H:%M") + self.book_['new_name'] + '修改失败！')
        finally:
            if res:
                self.conn.commit()
                self.stateChange.emit(time.strftime("%Y-%m-%d %H:%M") + '(' + str(self.no) + '/' + str(len(self.bookList)) + ')' + self.book_['new_name'] + '修改成功。')

            return res


# 只是提出参考
def book_name_cut(name: str):
    book_name = []
    newBook = {
        "face": "",                             # 不预设
        "classify": "",                         # 不预设
        "book_name": "",                        # 预设
        "Cxx": "C00",                           # 预设
        "chinesization": "未知汉化",                # 预设
        "author": "未知作者",                       # 预设
        "favourite": 0,                         # 预设
        "date": time.strftime("%Y-%m-%d"),      # 预设
        "address": "",                          # 不预设
        "unread": 0,                            # 预设
        "original_name": name,                  # 预设
        "new_name": ""                          # 不预设
    }

    # 找出COMIC_MARKET号
    comic_market = re.search(r"C\d{2,3}", name, re.I)
    name = re.sub(r"\(C\d{2,3}\)", '', name)
    if comic_market:
        comic_market = comic_market.group()
        newBook['Cxx'] = comic_market

    # 规范括号
    name = name.replace('【', '[')
    name = name.replace('】', ']')

    # 4k[s版]扫图组 需要单独判断
    if name.find('[4K[S版]掃圖組]') != -1:
        book_name = ['[4K[S版]掃圖組]']
        name = name.replace('[4K[S版]掃圖組]', '')

    # 用于判断是否为汉化组
    chss = ch.all_name
    part = ch.part
    chss = set(chss)
    book_name += re.findall(r'\[[^\[\]]*\]', name)
    name = re.sub(r'\[[^\[\]]*\]', '', name)

    is_find = False

    # 汉化组的匹配规则
    # 首先在完整的汉化组名字集合里找如果没有，就找可能是汉化组的字段
    for i in book_name:
        temp = i[1:-1]
        if temp in chss:
            is_find = True
            newBook['chinesization'] = temp
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

    # 默认book_name的第一个为作者名
    if book_name:
        newBook['author'] = book_name[0][1:-1]
        book_name = book_name[1:]

    # 将余下的方括号加入书本名
    for item in book_name:
        name += item

    newBook['book_name'] = name.replace(' ', '')
    return newBook


# 传入要插入的分类名, 返回插入状态 bool
def addNewClassify(classify_name: list):
    try:
        conn = sqlite3.connect('./data/data.db')
        cursor = conn.cursor()
        for i in classify_name:
            cursor.execute("insert into classify (name) values (?)", [i])
        res = True
    except Exception as e:
        print(e)
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


# 通过查找分类返回包含完整书本信息的dict列表，使用glob查找
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
    except Exception:
        print('获取目录失败！')
        if out_box:
            out_box.append(time.strftime("%Y-%m-%d %H:%M") + '获取目录失败！')
    finally:
        cursor.close()
        conn.close()
        return toDictList(data)


# 通过查找分类返回包含完整书本信息的dict列表，使用glob查找
def getBookListByAuthor(author_name: str, out_box=None):
    try:
        conn = sqlite3.connect('./data/data.db')
        cursor = conn.cursor()
        data = cursor.execute("select * from books where author=? ", [author_name]).fetchall()
    except Exception:
        print('获取目录失败！')
        if out_box:
            out_box.append(time.strftime("%Y-%m-%d %H:%M") + '获取目录失败！')
    finally:
        cursor.close()
        conn.close()
        return toDictList(data)


# 书名切割
def bookNameCut(book_name: str):
    return book_name_cut(book_name)


# 从当前分类删除
def deleteBookClassify(book_address: str, out_box, classify_name=None):
    try:
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
            classify_list = cursor.execute("select classify from books where address=?", [book_address]).fetchall()[0][0]
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
        if res:
            conn.commit()
        cursor.close()
        conn.close()
        out_box.append(time.strftime("%Y-%m-%d %H:%M") + '移除完毕。')


# 为书本添加分类
def addBookClassify(book_address: str, out_box, classify_name=None):
    if classify_name is None:
        return
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
            # 在书的分类列表中添加分类
            classify_list = cursor.execute("select classify from books where address=?", [book_address]).fetchall()[0][0]
            classify_list = classify_list.split()
            classify_name = classify_name.split()
            for i in classify_name:
                if classify_list.count(i) == 0:
                    classify_list.append(i)
            classify_list = str(classify_list)
            classify_list = classify_list[1: -1].replace('\'', '')
            cursor.execute("update books set classify=? where address=?", [classify_list.replace(',', ''), book_address])
        res = True
    except Exception:
        res = False
        out_box.append(time.strftime("%Y-%m-%d %H:%M") + '添加失败。')
        print('添加时出现错误!')
    finally:
        if res:
            conn.commit()
            out_box.append(time.strftime("%Y-%m-%d %H:%M") + '成功为添加分类:' + str(classify_name))
        cursor.close()
        conn.close()


# 彻底删除此书
def deleteBook(book_address: str, out_box):
    # 删除目录
    try:
        conn = sqlite3.connect('./data/data.db')
        cursor = conn.cursor()
        # 删除目录
        if os.path.exists(book_address):
            shutil.rmtree(book_address)
        cursor.execute("delete from books where address=?", [book_address])
        res = True
    except Exception:
        res = False
        out_box.append(time.strftime("%Y-%m-%d %H:%M") + '删除失败。')
        print('删除时出现错误!')
    finally:
        if res:
            conn.commit()
            out_box.append(time.strftime("%Y-%m-%d %H:%M") + '删除成功。')
        cursor.close()
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
    # 存放结果
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


# 通过查找书名和分类并返回包含完整书本信息的dict列表，使用glob查找
def search(val: str):
    val = val.split()
    data = []
    try:
        conn = sqlite3.connect('./data/data.db')
        cursor = conn.cursor()
        for i in val:
            temp = cursor.execute("select * from books where new_name glob ?", ['*' + i + '*']).fetchall()
            data += temp
            temp = cursor.execute("select * from books where classify glob ?", ['*' + i + '*']).fetchall()
            data += temp
        data = list(set(data))
    except Exception:
        print('Error!')
    finally:
        cursor.close()
        conn.close()
        return toDictList(data)


# 产生缩略图并保存副本传入图片的路径
def makeFace(path: str):
    img = Image.open(path)
    width, height = img.size
    if width <= 400:
        return
    headPath, imgNameAll = os.path.split(path)
    img.save(os.path.join(headPath, '备份' + imgNameAll))
    ratio = float(width) / float(height)
    width = 400.0
    height = width / ratio
    width = int(width)
    height = int(height)
    img = img.resize((width, height), Image.BICUBIC)
    # img.show()
    # os.remove(path)
    img.save(path)
