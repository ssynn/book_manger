import os
import time
from PyQt5.QtWidgets import (QWidget, QDesktopWidget, QMainWindow, QAction,
                             qApp, QInputDialog, QFileDialog, QSplitter,
                             QTextBrowser, QLabel, QVBoxLayout)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt
from model import public_function as pf
from model import flowlayout as fl
from model import set_book_dialog as st
from model import book_model as bm
from model import tree_view as tv
from model import set_books_dialog as sts

class MainWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.selectedClassifiy = '未看'
        self.list_view = False
        self.books = pf.getBookList('未看')
        self.initUI()

    def initUI(self):
        # 底部状态栏
        self.statusBar().showMessage("Ready")

        # 设置菜单
        self.setMenu()

        # 设置右边内容
        self.setCenter()

        # 设置样式
        self.setMyStyle()

        # 页面初始化
        self.setMainWindow()

    # 把主页面居中的方法
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        # self.move(qr.topLeft())

    # 菜单选项
    # 退出方法菜单
    def exitFunction(self):
        exitAction = QAction('&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)
        return exitAction

    # 切换视图菜单
    def swiftItemView(self):
        swiftItem = QAction('改变视图', self)
        swiftItem.setShortcut('Ctrl+S')
        swiftItem.triggered.connect(self.toggleView)
        return swiftItem

    # 单个插入新书菜单
    def addOneNewBook(self):
        addBookItem = QAction("添加单个", self)
        addBookItem.setShortcut('Ctrl+A')
        addBookItem.triggered.connect(self.addOneNewBookDialog)
        return addBookItem

    def addNewBooks(self):
        item = QAction("批量添加", self)
        item.triggered.connect(self.addNewBooksDialog)
        return item

    # 添加分类菜单项
    def addClassify(self):
        addClassifyItem = QAction('添加分类', self)
        addClassifyItem.setShortcut('Ctrl+L')
        addClassifyItem.triggered.connect(self.addNewClassifyFunction)
        return addClassifyItem

    # 删除菜单选项
    def deleteClassify(self):
        item = QAction('删除分类', self)
        item.setShortcut('Ctrl+D')
        item.triggered.connect(self.deleteClassifyFunction)
        return item

    # 总菜单设置
    def setMenu(self):
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&文件')
        fileMenu.addAction(self.exitFunction())
        fileMenu.addAction(self.addOneNewBook())
        fileMenu.addAction(self.addNewBooks())
        editMenu = menubar.addMenu('&编辑')
        # editMenu.addAction(self.swiftItemView())
        editMenu.addAction(self.addClassify())
        editMenu.addAction(self.deleteClassify())

    # 插入新书对话框
    def addOneNewBookDialog(self):
        dirName = QFileDialog.getExistingDirectory(self, '选择文件夹', './')
        if dirName:
            # print(dirName)
            self.addWindow = st.SetBookMessage(dirName)
            self.addWindow.before_close_signal.connect(
                self.addOneNewBookFunction)
            self.addWindow.show()
        else:
            print('error!')

    # 批量添加窗口
    def addNewBooksDialog(self):
        dirName = QFileDialog.getExistingDirectory(self, '选择文件夹', './')
        filelist = os.listdir(dirName)
        filelist = list(filter(isDir, filelist))
        print(dirName, filelist)
        self.addBooksWindow = sts.SetMultiMessage(filelist, dirName)
        self.addBooksWindow.before_close_signal.connect(self.addNewBooksFunction)
        self.addBooksWindow.show()

    # 插入新分类方法
    def addNewClassifyFunction(self):
        text, ok = QInputDialog.getText(self, '新的分类:', '可输入多个分类(空格间隔)')
        if ok and len(text) != 0:
            text = text.split()
            if pf.addNewClassify(text):
                self.leftTree.addNewClassify(text)
            else:
                self.textOut.append(time.strftime("%Y-%m-%d %H:%M") + "添加失败!")

    # 数据处理函数
    def addOneNewBookFunction(self, value):
        pf.addNewBook(value, self.textOut)

    # 批量添加
    def addNewBooksFunction(self, bookList: list):
        cnt = 0
        for i in bookList:
            cnt += int(pf.addNewBook(i, self.textOut))
        self.textOut.append(time.strftime("%Y-%m-%d %H:%M") + "成功插入:" + str(cnt) + "个，失败:" + str(len(bookList)-cnt) + "个。")

    # 删除分类方法
    def deleteClassifyFunction(self):
        text, ok = QInputDialog.getText(self, '删除分类:', '仅可输入一个要删除的分类')
        if ok and len(text) != 0 and pf.deleteClassify(text) and self.leftTree.deleteClassify(text):
            pass
        else:
            self.textOut.append(time.strftime("%Y-%m-%d %H:%M") + "删除失败!")

    # 主页面初始化
    def setMainWindow(self):
        # 设置位置和大小
        # self.setGeometry(300, 600, 300, 300)
        self.setWindowIcon(QIcon('pic/tx.jpg'))
        self.resize(1280, 720)
        self.center()
        self.setWindowTitle('Manger')
        self.textOut.append(time.strftime("%Y-%m-%d %H:%M") + "页面加载完成!")
        self.textOut.append('''
            <input>sad</input>
        ''')
        self.show()

    # 设置主页面内容
    def setCenter(self):
        # 设置主控件
        self.center_widget = QSplitter(self)

        # 左右分割
        self.leftTree = tv.MyTreeView(self)
        self.center_widget.addWidget(self.leftTree)

        # 上下分割
        self.textOut = QTextBrowser()
        self.makeRightContent()
        self.setCentralWidget(self.center_widget)

    # 右侧内容设置
    def makeRightContent(self):
        # 上下分割
        self.rightContent = QSplitter()

        # 设置为图片浏览
        if self.list_view:
            flowLayout = fl.FlowLayout()
            for i in self.books:
                flowLayout.addWidget(pf.makeBookView(i))
            booksView = QWidget()
            booksView.setLayout(flowLayout)
        # 文字详情浏览
        else:
            booksView = QSplitter()
            book_model = bm.BookModel(self.books, self)
            book_model.setStyleSheet('''
                BookModel{
                    border: 0px;
                }
            ''')
            booksView.addWidget(book_model)
            self.picLayout = QLabel()
            pic = QPixmap('./pic/face.jpg')

            self.picLayout.setPixmap(pic.scaled(400, 800, aspectRatioMode=Qt.KeepAspectRatio))
            self.picLayout.setMaximumWidth(400)
            self.picLayout.setMinimumWidth(400)
            self.picLayout.setStyleSheet('''
                *{
                    background-color: white;
                }
            ''')
            booksView.addWidget(self.picLayout)

        self.rightContent.addWidget(booksView)
        self.rightContent.addWidget(self.textOut)
        self.rightContent.setOrientation(Qt.Vertical)
        self.rightContent.setStretchFactor(0, 7)
        self.rightContent.setStretchFactor(1, 3)
        self.center_widget.addWidget(self.rightContent)

    # 切换视图 暂时放弃
    def toggleView(self):
        self.rightContent.deleteLater()
        self.list_view = not self.list_view
        self.makeRightContent()

    # 刷新右上角详细书单
    def refresh(self):
        # print(book_list)
        self.books = pf.getBookList(self.selectedClassifiy, self.textOut)
        self.rightContent.deleteLater()
        self.makeRightContent()

    # 设置样式
    def setMyStyle(self):
        self.center_widget.setStyleSheet('''
            QSplitter::handle{
                width: 0px;
                border: 0px solid gray;
            }
        ''')
        self.textOut.setStyleSheet(''' 
            QTextBrowser{
                border-top: 1px solid #f7f7f7;
            }
        ''')


def makeBookView(book: dict):
    view = QWidget()
    imgeLabel = QLabel()
    pixMap = QPixmap(os.path.join(book['address'], book['face']))
    imgeLabel.setPixmap(pixMap.scaled(120, 170))

    text = QLabel()
    name = book['book_name']
    if len(name) > 5:
        name = name[:5] + '...'
    text.setText(name)
    text.setAlignment(Qt.AlignCenter)
    vLayout = QVBoxLayout()
    vLayout.addWidget(imgeLabel)
    vLayout.addWidget(text)
    view.setLayout(vLayout)
    view.resize(150, 150)
    return view


def isDir(name: str):
    ext = os.path.splitext(name)[1]
    return ext == ''
