import os
import time
from PyQt5.QtWidgets import (QWidget, QDesktopWidget, QMainWindow, QAction,
                             QGridLayout, qApp, QInputDialog, QFileDialog,
                             QSplitter, QLineEdit, QTextBrowser, QLabel,
                             QVBoxLayout, QToolButton)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt
from model import public_function as pf
from model import set_book_dialog as st
from model import book_model as bm
from model import tree_view as tv
from model import set_books_dialog as sts


class MainWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.selectedClassifiy = '未看'
        self.list_view = False
        self.setAcceptDrops(True)
        self.books = pf.getBookList('未看')
        self.initUI()

    def initUI(self):
        # 底部状态栏
        self.statusBar().showMessage("Ready")

        # 设置菜单
        self.setMenu()

        # 设置主要内容
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

    # 批量添加菜单
    def addNewBooks(self):
        item = QAction("批量添加", self)
        item.setShortcut('Ctrl+M')
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

    # 批量修改
    def modifyMultiBooks(self):
        item = QAction('修改当前页的所有书籍信息', self)
        item.setShortcut('Ctrl+M')
        item.triggered.connect(self.modifyMultiBooksDialog)
        return item

    # 总菜单设置
    def setMenu(self):
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&文件')
        fileMenu.addAction(self.addOneNewBook())
        fileMenu.addAction(self.addNewBooks())
        fileMenu.addAction(self.exitFunction())
        editMenu = menubar.addMenu('&编辑')
        # editMenu.addAction(self.swiftItemView())
        editMenu.addAction(self.addClassify())
        editMenu.addAction(self.deleteClassify())
        editMenu.addAction(self.modifyMultiBooks())

    # 插入新书对话框
    def addOneNewBookDialog(self, address=None):
        # 读取上次打开的目录作为起始目录
        with open('./data/path.txt', 'r', encoding="UTF-8") as p:
            path = p.read()
        print(address)
        if address is False:
            dirName = QFileDialog.getExistingDirectory(self, '选择文件夹', path)
        else:
            dirName = address
        if dirName:
            # 保持当前所在的目录
            path = os.path.split(dirName)[0]
            with open('./data/path.txt', 'w', encoding="UTF-8") as p:
                p.write(path)

            self.addWindow = st.SetBookMessage(dirName, self)
            self.addWindow.after_close_signal.connect(self.addOneNewBookFunction)
        else:
            print('error!')

    # 批量添加窗口
    def addNewBooksDialog(self, addressList=None):
        # 打开文件夹
        if not addressList:
            # 读取上次打开的目录作为起始目录
            with open('./data/path.txt', 'r', encoding="UTF-8") as p:
                path = p.read()
            dirName = QFileDialog.getExistingDirectory(self, '选择文件夹', path)
            if dirName == '':
                return
            path = os.path.split(dirName)[0]
            # 保存当前所在的目录
            with open('./data/path.txt', 'w', encoding="UTF-8") as p:
                p.write(path)
            filelist = os.listdir(dirName)
            filelist = list(filter(isDir, filelist))
            filelist = [os.path.join(dirName, x) for x in filelist]
        else:
            filelist = addressList
        # print(filelist)
        # 传入父文件夹地址和文件夹内的子文件夹名
        self.addBooksWindow = sts.SetMultiMessage(filelist, self, address=True)
        self.addBooksWindow.stateChange.connect(self.textOut.append)
        self.addBooksWindow.after_close_signal.connect(self.addNewBooksFunction)

    # 插入新分类方法
    def addNewClassifyFunction(self):
        text, ok = QInputDialog.getText(self, '新的分类:', '可输入多个分类(空格间隔)')
        if ok and len(text) != 0:
            text = text.split()
            if pf.addNewClassify(text):
                self.leftTree.classify_all += text
                self.leftTree.addNewClassify(text)
            else:
                self.textOut.append(time.strftime("%Y-%m-%d %H:%M") + "添加失败!")

    # 数据处理函数线程
    def addOneNewBookFunction(self, value):
        self.addBook = pf.AddNewBook(value)
        self.addBook.start()
        self.addBook.stateChange.connect(self.textOut.append)
        self.addBook.authorChange.connect(self.authorChange)
        self.addBook.end.connect(self.refresh)

    # 批量添加线程
    def addNewBooksFunction(self, bookList: list):
        self.addBooks = pf.AddNewBookS(bookList)
        self.addBooks.start()
        self.addBooks.stateChange.connect(self.textOut.append)
        self.addBooks.authorChange.connect(self.authorChange)
        self.addBooks.end.connect(self.refresh)

    # 删除分类方法
    def deleteClassifyFunction(self):
        text, ok = QInputDialog.getText(self, '删除分类:', '仅可输入一个要删除的分类')
        if ok and len(text) != 0 and pf.deleteClassify(text) and self.leftTree.deleteClassify(text):
            pass
        else:
            self.textOut.append(time.strftime("%Y-%m-%d %H:%M") + "删除失败!")

    # 批量修改信息方法
    def modifyMultiBooksDialog(self):
        self.modifyBooks = sts.SetMultiMessage(self.books, self)
        self.modifyBooks.after_close_signal.connect(self.modifyMultiBooksFunction)

    # 批量修改信息方法线程
    def modifyMultiBooksFunction(self, bookList):
        self.modifyBooks = pf.ModifyMultiBookInfo(bookList)
        self.modifyBooks.start()
        self.modifyBooks.stateChange.connect(self.textOut.append)
        self.modifyBooks.authorChange.connect(self.authorChange)
        self.modifyBooks.end.connect(self.refresh)

    # 搜索方法
    def searchFunction(self):
        if len(self.searchInput.text()) != 0:
            self.refresh(pf.search(self.searchInput.text()))
            self.textOut.append(time.strftime(
                "%Y-%m-%d %H:%M") + "找到" + str(len(self.books)) + "条结果。")

    # 主页面初始化
    def setMainWindow(self):
        # 设置位置和大小
        self.setWindowIcon(QIcon('pic/tx.jpg'))
        self.resize(1280, 800)
        self.center()
        self.setWindowTitle('Manger')
        self.textOut.append(time.strftime("%Y-%m-%d %H:%M") + "页面加载完成!")
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

        # 上方组件
        # 设置为图片浏览, 不知道什么时候会做这个功能
        if False:
            pass
            # flowLayout = fl.FlowLayout()
            # for i in self.books:
            #     flowLayout.addWidget(makeBookView(i))
            # booksView = QWidget()
            # booksView.setLayout(flowLayout)
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
            self.picLayout.setPixmap(
                QPixmap('./pic/face.jpg').scaled(400, 800, aspectRatioMode=Qt.KeepAspectRatio))
            self.picLayout.setMaximumWidth(400)
            self.picLayout.setMinimumWidth(400)
            self.picLayout.setStyleSheet('''
                *{
                    background-color: white;
                }
            ''')
            booksView.addWidget(self.picLayout)

        # 下方组建, 一个搜索条一个输出信息框
        textView = QSplitter()
        self.searchButton = QToolButton()
        self.searchButton.setIcon(QIcon('icon/search.png'))
        self.searchButton.clicked.connect(self.searchFunction)
        self.searchButton.setStyleSheet('''
            QToolButton{
                border: 0px;
            }
        ''')
        self.searchInput = QLineEdit()
        self.searchInput.setMaximumWidth(200)
        self.searchInput.setMinimumHeight(30)
        self.searchInput.editingFinished.connect(self.searchFunction)
        self.searchInput.setStyleSheet('''
            *{
                border: 1px solid #c3c3c3;
                border-radius: 8px;
                color: #aaaaaa;
                margin: 0px
            }
        ''')
        space = QLabel()
        self.searchLayout = QGridLayout()
        self.searchLayout.addWidget(space, 0, 0, 1, 5)
        self.searchLayout.addWidget(self.searchInput, 0, 6)
        self.searchLayout.addWidget(self.searchButton, 0, 7, 1, 1)
        self.searchBar = QWidget()
        self.searchBar.setLayout(self.searchLayout)
        self.searchBar.setStyleSheet('''
            *{
                background-color: white;
            }
        ''')
        textView.addWidget(self.searchBar)
        textView.addWidget(self.textOut)
        textView.setOrientation(Qt.Vertical)
        textView.setStretchFactor(0, 2)
        textView.setStretchFactor(1, 5)
        textView.setStyleSheet('''
            QSplitter{
                background-color = white;
                border: 0px;
                border-top: 1px solid #c3c3c3;
            }
        ''')

        self.rightContent.addWidget(booksView)
        self.rightContent.addWidget(textView)
        self.rightContent.setOrientation(Qt.Vertical)
        self.rightContent.setStretchFactor(0, 6)
        self.rightContent.setStretchFactor(1, 4)
        self.center_widget.addWidget(self.rightContent)

    # 切换视图 暂时放弃
    def toggleView(self):
        self.rightContent.deleteLater()
        self.list_view = not self.list_view
        self.makeRightContent()

    # 刷新右上角详细书单
    def refresh(self, val=None):
        if val is None:
            self.books = pf.getBookList(self.selectedClassifiy, self.textOut)
        else:
            self.books = val
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
            border: 0px;
        ''')
        self.textOut.verticalScrollBar().setStyleSheet('''
            QScrollBar{background:transparent; width: 10px;}
            QScrollBar::handle{background:lightgray; border:2px solid transparent; border-radius:5px;}
            QScrollBar::handle:hover{background:gray;}
            QScrollBar::sub-line{background:transparent;}
            QScrollBar::add-line{background:transparent;}
        ''')

    # 添加作者
    def authorChange(self, author):
        self.leftTree.authorAll.append(author)
        self.leftTree.insertAuthor(author)

    # 拖拽添加
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            if len(event.mimeData().urls()) == 1:
                self.addOneNewBookDialog(event.mimeData().urls()[0].toLocalFile())
            else:
                url = [str(x.toLocalFile()) for x in event.mimeData().urls()]
                self.addNewBooksDialog(url)
            event.acceptProposedAction()


def makeBookView(book: dict):
    view = QWidget()
    imageLabel = QLabel()
    pixMap = QPixmap(os.path.join(book['address'], book['face']))
    imageLabel.setPixmap(pixMap.scaled(120, 170))

    text = QLabel()
    name = book['book_name']
    if len(name) > 5:
        name = name[:5] + '...'
    text.setText(name)
    text.setAlignment(Qt.AlignCenter)
    vLayout = QVBoxLayout()
    vLayout.addWidget(imageLabel)
    vLayout.addWidget(text)
    view.setLayout(vLayout)
    view.resize(150, 150)
    return view


def isDir(name: str):
    ext = os.path.splitext(name)[1]
    return ext == ''
