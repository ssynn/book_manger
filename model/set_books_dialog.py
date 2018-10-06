import os
from PyQt5.QtWidgets import (QWidget, QGridLayout, QTreeView,
                             QLabel, QLineEdit, QTextEdit, QPushButton,
                             QCheckBox, QHBoxLayout, QGroupBox, QToolButton)
from PyQt5.QtGui import QStandardItemModel, QIcon, QImage
from PyQt5.QtCore import Qt, QSize, pyqtSignal
from model import public_function as pf


# self.newBook为当前显示的书本
class SetMultiMessage(QWidget):
    after_close_signal = pyqtSignal(list)

    def __init__(self, filelist: list, address: str, master=None):
        super().__init__()
        self.path = address
        # 书名分割
        self.bookList = []
        for i in filelist:
            temp = pf.bookNameCut(i)
            temp['face_list'] = os.listdir(os.path.join(address, i))
            temp['face_list'] = list(filter(isPic, temp['face_list']))[:3]
            if len(temp['face_list']) == 0:
                print(temp['original_name'])
                continue
            temp['face'] = temp['face_list'][0]
            temp['original_path'] = os.path.join(self.path, temp['original_name'])
            self.faceSelected = temp['face']
            self.bookList.append(temp)
        self.newBook = self.bookList[0]
        self.initUI()

    def initUI(self):
        self.setGeometry(600, 200, 1000, 500)
        self.body = QGridLayout(self)
        self.setWindowTitle("批量添加")
        self.setWindowIcon(QIcon('pic/tx.jpg'))
        # 列表视图
        self.left = QTreeView()
        self.left.setModel(self.createBookModel())
        self.left.clicked.connect(self.clickFunction)
        self.body.addWidget(self.left, 0, 0, 5, 5)

        # 详情视图
        self.right = self.createMessageBox()
        self.body.addLayout(self.right, 0, 6, 8, 5)

        # 公有属性
        publicAuthorLabel = QLabel("公有作者")
        self.publicAuthorInput = QLineEdit(self)
        publicCliassify = QLabel("公有分类")
        self.publicClassifyInput = QLineEdit(self)
        self.body.addWidget(publicAuthorLabel, 5, 0)
        self.body.addWidget(self.publicAuthorInput, 5, 1, 1, 4)
        self.body.addWidget(publicCliassify, 6, 0)
        self.body.addWidget(self.publicClassifyInput, 6, 1, 1, 4)
        self.publicFavourite = QCheckBox("全部喜欢")
        self.publicUnread = QCheckBox('全部未看')
        self.body.addWidget(self.publicFavourite, 7, 1)
        self.body.addWidget(self.publicUnread, 7, 2)

        # 信息视图
        done = QPushButton('确认')
        done.clicked.connect(self.finish)
        cancel = QPushButton('取消')
        cancel.clicked.connect(self.close)
        self.body.addWidget(done, 10, 9)
        self.body.addWidget(cancel, 10, 10)
        self.setInformation()
        self.show()

    def createBookModel(self):
        model = QStandardItemModel(0, 1, self)
        model.setHeaderData(0, Qt.Horizontal, '书名')
        for i in self.bookList:
            self.addBook(model, i['original_name'])
        return model

    def addBook(self, model, name):
        model.insertRow(0)
        model.setData(model.index(0, 0), name)

    # 右侧设置详细信息部分
    def createMessageBox(self):
        gLayOut = QGridLayout()
        bookNameLabel = QLabel('书名')
        # bookNameLabel.setAlignment(Qt.AlignBottom)
        self.bookNameInput = QLineEdit(self)

        authorLabel = QLabel("作者")
        # authorLabel.setAlignment(Qt.AlignBottom)
        self.authorInput = QLineEdit(self)

        chinesizationLabel = QLabel('汉化')
        # chinesizationLabel.setAlignment(Qt.AlignBottom)
        self.chinesizationInput = QLineEdit(self)

        comicMarketLabel = QLabel("Comic Market")
        # comicMarketLabel.setAlignment(Qt.AlignBottom)
        self.comicMarketInput = QLineEdit(self)

        classifyLabel = QLabel('分类')
        # classifyLabel.setAlignment(Qt.AlignBottom)
        self.classifyInput = QLineEdit(self)

        originalLabel = QLabel("源文件名")
        # originalLabel.setAlignment(Qt.AlignCenter)
        self.originalInput = QTextEdit(self)

        gLayOut.addWidget(bookNameLabel, 0, 0)
        gLayOut.addWidget(self.bookNameInput, 0, 1, 1, 3)
        gLayOut.addWidget(authorLabel, 1, 0)
        gLayOut.addWidget(self.authorInput, 1, 1, 1, 3)
        gLayOut.addWidget(chinesizationLabel, 2, 0)
        gLayOut.addWidget(self.chinesizationInput, 2, 1, 1, 3)
        gLayOut.addWidget(comicMarketLabel, 3, 0)
        gLayOut.addWidget(self.comicMarketInput, 3, 1, 1, 3)
        gLayOut.addWidget(originalLabel, 4, 0)
        gLayOut.addWidget(self.originalInput, 4, 1, 1, 3)
        gLayOut.addWidget(classifyLabel, 5, 0)
        gLayOut.addWidget(self.classifyInput, 5, 1, 1, 3)

        self.favourite = QCheckBox("喜欢")
        self.unread = QCheckBox('未看')
        gLayOut.addWidget(self.favourite, 6, 1)
        gLayOut.addWidget(self.unread, 6, 2)

        self.pics = QGroupBox()
        # pics.setObjectName()
        self.pics.setTitle('选择封面')
        self.pic_layout = QHBoxLayout(self.pics)

        self.face0 = QToolButton()
        self.face0.setIconSize(QSize(100, 100))
        self.face0.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.face0.clicked.connect(self.selectFace0Function)
        self.pic_layout.addWidget(self.face0)

        self.face1 = QToolButton()
        self.face1.setIconSize(QSize(100, 100))
        self.face1.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.face1.clicked.connect(self.selectFace1Function)
        self.pic_layout.addWidget(self.face1)

        self.face2 = QToolButton()
        self.face2.setIconSize(QSize(100, 100))
        self.face2.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.face2.clicked.connect(self.selectFace2Function)
        self.pic_layout.addWidget(self.face2)

        gLayOut.addWidget(self.pics, 7, 0, 5, 4)
        return gLayOut

    # 把右侧更改后的信息保存到newBook
    def confirm(self):
        # 以下参数允许手动修改
        self.newBook['author'] = self.authorInput.text()
        self.newBook['book_name'] = self.bookNameInput.text()
        self.newBook['Cxx'] = self.comicMarketInput.text()
        self.newBook['chinesization'] = self.chinesizationInput.text()
        self.newBook['classify'] = self.classifyInput.text()
        self.newBook['favourite'] = int(self.favourite.isChecked())
        self.newBook['unread'] = int(self.unread.isChecked())
        self.newBook['face'] = self.faceSelected
        image = QImage()
        image.load(os.path.join(self.path, self.newBook['face']))
        image.save(os.path.join(self.path, self.newBook['face']))

    def setInformation(self):
        self.bookNameInput.setText(self.newBook['book_name'])
        self.authorInput.setText(self.newBook['author'])
        self.chinesizationInput.setText(self.newBook['chinesization'])
        self.comicMarketInput.setText(self.newBook['Cxx'])
        self.originalInput.setText(self.newBook['original_name'])
        self.classifyInput.setText(self.newBook['classify'])
        self.favourite.setChecked(bool(self.newBook['favourite']))
        self.unread.setChecked(bool(self.newBook['unread']))
        self.face0.setIcon(
            QIcon(os.path.join(self.path, self.newBook['original_name'], self.newBook['face_list'][0])))
        self.face1.setIcon(
            QIcon(os.path.join(self.path, self.newBook['original_name'], self.newBook['face_list'][1])))
        self.face2.setIcon(
            QIcon(os.path.join(self.path, self.newBook['original_name'], self.newBook['face_list'][2])))
        self.face0.setDown(False)
        self.face1.setDown(False)
        self.face2.setDown(False)
        self.faceSelected = self.newBook['face']
        self.face0.setText(self.newBook['face_list'][0])
        self.face1.setText(self.newBook['face_list'][1])
        self.face2.setText(self.newBook['face_list'][2])
        if self.face0.text() == self.newBook['face']:
            self.face0.setDown(True)
        if self.face1.text() == self.newBook['face']:
            self.face1.setDown(True)
        if self.face2.text() == self.newBook['face']:
            self.face2.setDown(True)

    # 选择封面
    def selectFace0Function(self):
        self.face0.setDown(True)
        self.face1.setDown(False)
        self.face2.setDown(False)
        self.faceSelected = self.newBook['face_list'][0]

    def selectFace1Function(self):
        self.face0.setDown(False)
        self.face1.setDown(True)
        self.face2.setDown(False)
        self.faceSelected = self.newBook['face_list'][1]

    def selectFace2Function(self):
        self.face0.setDown(False)
        self.face1.setDown(False)
        self.face2.setDown(True)
        self.faceSelected = self.newBook['face_list'][2]

    # 选择书籍
    def clickFunction(self):
        self.confirm()
        for i in self.bookList:
            if i['original_name'] == self.left.selectedIndexes()[0].data():
                self.newBook = i
                self.setInformation()
                break
        # print(self.newBook)

    # 关闭窗口，传回包含书本信息的list
    def finish(self):
        self.confirm()
        for i in range(len(self.bookList)):
            # 设置全局喜欢，未读，分类
            if self.publicFavourite.isChecked():
                self.bookList[i]['favourite'] = 1
            if self.publicUnread.isChecked():
                self.bookList[i]['unread'] = 1
            if len(self.publicAuthorInput.text()) != 0:
                if len(self.bookList[i]['classify']) != 0:
                    self.bookList[i]['classify'] += ' '
                self.bookList[i]['classify'] += self.publicClassifyInput.text()
            if len(self.publicAuthorInput.text()) != 0:
                self.bookList[i]['author'] = self.publicAuthorInput.text()
            # 生成最终决定的书名和地址
            self.bookList[i]['new_name'] = '[' + self.bookList[i]['author'] + ']' + self.bookList[i]['book_name'] + '[' + self.bookList[i]['chinesization'] + ']'
            if self.bookList[i]['Cxx'] != 'C00':
                self.bookList[i]['new_name'] += ('(' + self.bookList[i]['Cxx'] + ')')
            self.bookList[i]['address'] = os.path.join(
                './books', self.bookList[i]['author'], self.bookList[i]['new_name'])

        self.close()
        self.after_close_signal.emit(self.bookList)


def isPic(name: str):
    ext = os.path.splitext(name)[1]
    return ext == '.jpg' or ext == '.png'
