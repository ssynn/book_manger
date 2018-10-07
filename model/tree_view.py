import os
from PyQt5.QtWidgets import (QTreeWidget, QTreeWidgetItem)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from model import public_function as pf

ILLIGAL = ['未看', '夏欢', '未分类', '分类', '所有']


class MyTreeView(QTreeWidget):
    def __init__(self, master):
        super().__init__()
        self.master = master
        self.classify_all = pf.getAllClassifyName()
        self.authorAll = os.listdir('./books')
        self.authorAll = list(filter(isDir, self.authorAll))
        temp = []
        for i in self.authorAll:
            authorDir = os.path.join('./books', i)
            if len(os.listdir(authorDir)) == 0:
                os.rmdir(authorDir)
            else:
                temp.append(i)
        self.authorAll = temp

        self.setColumnCount(1)
        self.setHeaderLabels(['选项'])
        self.setMinimumWidth(150)
        # self.resize(150, 150)
        self.setMaximumWidth(250)
        self.setStyleSheet('''
            QTreeWidget{
                border: 0px;
                background-color: rgba(255, 233, 240, 1);
            }
        ''')

        # 未看
        unread = QTreeWidgetItem(self)
        unread.setText(0, '未看')
        unread.setIcon(0, QIcon('./icon/unread.png'))
        unread.setSelected(True)

        # 喜欢
        like = QTreeWidgetItem(self)
        like.setIcon(0, QIcon('./icon/favourite.png'))
        like.setText(0, '喜欢')

        # 所有书
        allBook = QTreeWidgetItem(self)
        allBook.setIcon(0, QIcon('./icon/all.png'))
        allBook.setText(0, '所有')

        # 未分类
        unclassified = QTreeWidgetItem(self)
        unclassified.setIcon(0, QIcon('./icon/unclassified.png'))
        unclassified.setText(0, '未分类')

        # 作者
        self.author = QTreeWidgetItem(self)
        self.author.setIcon(0, QIcon('./icon/tag.png'))
        self.author.setText(0, '作者')
        self.insertAuthor()
        self.author.setExpanded(False)

        # 分类
        self.classify = QTreeWidgetItem(self)
        self.classify.setIcon(0, QIcon('./icon/classified.png'))
        self.classify.setText(0, '分类')
        self.addNewClassify(self.classify_all)
        self.classify.setExpanded(True)

        # 添加左键
        self.clicked.connect(self.treeItemHandle)

    # 树状视图左键方法
    def treeItemHandle(self, val: object):
        if val.data() == '分类' or val.data() == '作者':
            return
        if val.data() in self.authorAll:
            self.master.refresh(pf.getBookListByAuthor(val.data()))
            return
        self.master.selectedClassifiy = val.data()
        self.master.refresh()

    # 把子分类加入分类
    def addNewClassify(self, text: list):
        for i in text:
            child = QTreeWidgetItem(self.classify)
            child.setIcon(0, QIcon('./icon/tag.png'))
            child.setText(0, i)

    # 删除节点
    def deleteClassify(self, text):
        if text not in self.classify_all:
            return False
        item = self.findItems(text, Qt.MatchRecursive)
        if len(item) != 0:
            self.classify.removeChild(item[0])
            return True
        else:
            return False

    def insertAuthor(self, author=None):
        if author is not None:
            child = QTreeWidgetItem(self.author)
            child.setIcon(0, QIcon('./icon/tag.png'))
            child.setText(0, author)
            return
        for i in self.authorAll:
            child = QTreeWidgetItem(self.author)
            child.setIcon(0, QIcon('./icon/tag.png'))
            child.setText(0, i)


def isDir(name: str):
    ext = os.path.splitext(name)[1]
    return ext == ''

    # # 右键菜单
    # def contextMenuEvent(self, e):
    #     contextMenu = QMenu(self)
    #     contextMenu.addAction(self.deleteItem())
    #     contextMenu.exec_(e.globalPos())

    # # 删除当前分类
    # def deleteItem(self):
    #     item = QAction('&删除', self)
    #     item.triggered.connect(self.deleteItemFunction)
    #     # item.setEnabled(False)
    #     return item
