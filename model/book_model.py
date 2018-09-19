import os
import time
from model import public_function as pf
from model import set_book_dialog as st
from PyQt5.QtWidgets import (QAbstractItemView, QAction, QMessageBox, QMenu,
                             QApplication, QTreeView, QInputDialog)
from PyQt5.QtGui import QStandardItemModel, QPixmap
from PyQt5.QtCore import Qt

NAME, AUTHOR, DATE, CLASSIFY, ADDRESS = range(5)


class BookModel(QTreeView):
    def __init__(self, book_list, master):
        super().__init__()
        self.master = master
        self.book_ = book_list
        self.setRootIsDecorated(False)
        self.setAlternatingRowColors(True)
        self.setSortingEnabled(True)
        self.setModel(self.createBookModel())
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.doubleClicked.connect(self.doubleClickedFunction)
        self.clicked.connect(self.clickedFunction)

    # 建立模型
    def createBookModel(self):
        model = QStandardItemModel(0, 5, self)
        model.setHeaderData(NAME, Qt.Horizontal, '书名')
        model.setHeaderData(AUTHOR, Qt.Horizontal, '作者')
        model.setHeaderData(DATE, Qt.Horizontal, '创建时间')
        model.setHeaderData(CLASSIFY, Qt.Horizontal, '分类')
        model.setHeaderData(ADDRESS, Qt.Horizontal, '文件地址')

        for i in self.book_:
            self.addBook(model, i['book_name'], i['author'], i['date'],
                         i['classify'], i['address'])
        return model

    # 加入新条目方法
    def addBook(self, model, name, author, date, classify, address):
        model.insertRow(0)
        model.setData(model.index(0, NAME), name)
        model.setData(model.index(0, AUTHOR), author)
        model.setData(model.index(0, DATE), date)
        model.setData(model.index(0, CLASSIFY), self.listToStr(classify))
        model.setData(model.index(0, ADDRESS), address)

    # 打开书本所在文件夹
    def openFileItem(self):
        openFile = QAction("&打开文件夹", self)
        openFile.triggered.connect(self.openFileInExplorer)
        return openFile

    # 修改选中书本的内容
    def modifyItem(self):
        modify = QAction("&修改", self)
        modify.triggered.connect(self.modifyFunction)
        return modify

    # 彻底删除当前书本
    def deleteItem(self):
        delete = QAction("&删除", self)
        delete.triggered.connect(self.deleteItemFunction)
        return delete

    # 从当前分类删除这本书
    def deleteClassifyItem(self):
        deleteClassify = QAction('&从当前分类删除', self)
        deleteClassify.triggered.connect(self.deleteClassifyItemFunction)
        return deleteClassify

    # 复制信息菜单
    def copyItem(self):
        copy = QAction('&复制', self)
        copy.triggered.connect(self.copyFunction)
        return copy

    # 为书本添加分类
    def addClassifyForBook(self):
        item = QAction('&添加分类', self)
        item.triggered.connect(self.addClassifyForBookFunction)
        return item

    # 右键菜单
    def contextMenuEvent(self, e):
        contextMenu = QMenu(self)
        contextMenu.addAction(self.openFileItem())
        contextMenu.addAction(self.modifyItem())
        contextMenu.addAction(self.deleteItem())
        contextMenu.addAction(self.copyItem())
        contextMenu.addAction(self.deleteClassifyItem())
        contextMenu.addAction(self.addClassifyForBook())
        contextMenu.exec_(e.globalPos())

    # 左键双击
    def doubleClickedFunction(self, e):
        os.system('explorer.exe %s' % os.path.abspath(
            self.selectedIndexes()[4].data()))
        print('左键双击!', self.selectedIndexes()[4].data())

    # 左键单击
    def clickedFunction(self, e):
        for i in self.book_:
            if i['address'] == self.selectedIndexes()[4].data():
                self.master.picLayout.setPixmap(QPixmap(os.path.join(i['address'], i['face'])).scaled(400, 800, aspectRatioMode=Qt.KeepAspectRatio))
                break

    # 删除书本方法
    def deleteItemFunction(self):
        msgBox = QMessageBox(QMessageBox.Warning, "警告!", '您将会永久删除这本书!',
                             QMessageBox.NoButton, self)
        msgBox.addButton("确认", QMessageBox.AcceptRole)
        msgBox.addButton("取消", QMessageBox.RejectRole)
        if msgBox.exec_() == QMessageBox.AcceptRole:
            pf.deleteBook(self.selectedIndexes()[4].data(), self.master.textOut)
            self.master.refresh()

    # 复制单行数据方法
    def copyFunction(self):
        text = ''
        datas = self.selectedIndexes()
        for i in datas:
            text += i.data()
            text += ' '
        clipboard = QApplication.clipboard()
        clipboard.setText(text)
        print(text)
        self.master.textOut.append(time.strftime("%Y-%m-%d %H:%M") + "已复制:" + text)

    # 从当前分类删除
    def deleteClassifyItemFunction(self):
        if self.master.selectedClassifiy == '未分类' or self.master.selectedClassifiy == '所有':
            self.master.textOut.append(time.strftime("%Y-%m-%d %H:%M") + "不能从此分类删除!")
            print('不能从此分类删除!')
            return
        msgBox = QMessageBox(QMessageBox.Warning, "警告!", '您将会从此分类删除这本书!',
                             QMessageBox.NoButton, self)
        msgBox.addButton("确认", QMessageBox.AcceptRole)
        msgBox.addButton("取消", QMessageBox.RejectRole)
        if msgBox.exec_() == QMessageBox.AcceptRole:
            pf.deleteBookClassify(self.selectedIndexes()[4].data(), self.master.textOut, self.master.selectedClassifiy)
            print('从当前分类删除')
            self.master.refresh()

    # 为当前书籍添加分类
    def addClassifyForBookFunction(self):
        temp = QInputDialog(self)
        text, ok = temp.getText(self, '新的分类:', '可输入多个分类(空格间隔)')
        if ok and len(text) != 0:
            pf.addBookClassify(self.selectedIndexes()[4].data(), self.master.textOut, text)
            print('添加成功！')
            self.master.refresh()

    # 修改书本信息
    def modifyFunction(self):
        for i in self.book_:
            if i['address'] == self.selectedIndexes()[4].data():
                self.addWindow = st.SetBookMessage(i)
                self.addWindow.before_close_signal.connect(self.modifyFunctionBase)
                self.addWindow.show()

    def modifyFunctionBase(self, value):
        print(value)
        pf.modifyBookInfo(value, self.master.textOut)

    # list转str
    def listToStr(self, classify_names: list):
        temp = ""
        for i in classify_names:
            temp += i
            temp += ' '
        return temp

    # 在资源管理器中打开文件夹
    def openFileInExplorer(self):
        os.system('explorer.exe %s' % os.path.abspath(
            self.selectedIndexes()[4].data()))
