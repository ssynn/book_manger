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
        self.setColumnCount(1)
        self.setHeaderLabels(['选项'])
        self.clicked.connect(self.treeItemHandle)
        self.setMinimumWidth(150)
        self.setMaximumWidth(150)
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

        # 分类
        self.classify = QTreeWidgetItem(self)
        self.classify.setIcon(0, QIcon('./icon/classified.png'))
        self.classify.setText(0, '分类')
        self.addNewClassify(self.classify_all)
        self.classify.setExpanded(True)

    # 树状视图左键方法
    def treeItemHandle(self, val: object):
        if val.data() == '分类':
            return
        self.master.selectedClassifiy = val.data()
        self.master.refresh()

    # 添加分类
    def addNewClassify(self, text: list):
        for i in text:
            child = QTreeWidgetItem(self.classify)
            child.setIcon(0, QIcon('./icon/tag.png'))
            child.setText(0, i)

    # 删除节点
    def deleteClassify(self, text):
        item = self.findItems(text, Qt.MatchRecursive)
        if len(item) != 0:
            self.classify.removeChild(item[0])
            return True
        else:
            return False

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
