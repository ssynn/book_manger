import os
import time
from model import public_function as pf
from PyQt5.QtWidgets import (
    QWidget,
    QPushButton,
    QGridLayout,
    QLineEdit,
    QLabel,
    QCheckBox,
    QTextEdit,
    QHBoxLayout,
    QToolButton,
    QGroupBox
)
from PyQt5.QtGui import QIcon, QImage
from PyQt5.QtCore import Qt, pyqtSignal, QSize


# 传入完整路径初始化,返回装着书本信息的dict
class SetBookMessage(QWidget):
    after_close_signal = pyqtSignal(dict)
    stateChange = pyqtSignal(str)

    def __init__(self, book_):
        super().__init__()
        # 直接传入书目录则表示是建立新书
        if type(book_) == str:
            self.path = book_
            self.newBook = pf.bookNameCut(os.path.split(book_)[1])
        # 传入记录数信息的dict表示修改书信息
        else:
            self.path = book_['address']
            self.newBook = book_
        self.faceList = list(filter(isPic, os.listdir(self.path)[:6]))[:3]
        if len(self.faceList) < 3:
            self.stateChange.emit(time.strftime("%Y-%m-%d %H:%M") + "无法添加此目录!")
            return
        self.faceSelected = self.faceList[0]
        self.setMainWindow()
        self.initUI()

    def initUI(self):
        gLayOut = QGridLayout()
        bookNameLabel = QLabel('书名')
        # bookNameLabel.setAlignment(Qt.AlignBottom)
        self.bookNameInput = QLineEdit(self)
        self.bookNameInput.setText(self.newBook['book_name'])

        authorLabel = QLabel("作者")
        # authorLabel.setAlignment(Qt.AlignBottom)
        self.authorInput = QLineEdit(self)
        self.authorInput.setText(self.newBook['author'])

        chinesizationLabel = QLabel('汉化')
        # chinesizationLabel.setAlignment(Qt.AlignBottom)
        self.chinesizationInput = QLineEdit(self)
        self.chinesizationInput.setText(self.newBook['chinesization'])

        comicMarketLabel = QLabel("Comic Market")
        # comicMarketLabel.setAlignment(Qt.AlignBottom)
        self.comicMarketInput = QLineEdit(self)
        self.comicMarketInput.setText(self.newBook['Cxx'])

        classifyLabel = QLabel('分类')
        # classifyLabel.setAlignment(Qt.AlignBottom)
        self.classifyInput = QLineEdit(self)
        self.classifyInput.setText(self.newBook['classify'])

        originalLabel = QLabel("源文件名")
        # originalLabel.setAlignment(Qt.AlignCenter)
        self.originalInput = QTextEdit(self)
        self.originalInput.setText(self.newBook['original_name'])

        gLayOut.addWidget(bookNameLabel, 0, 0)
        gLayOut.addWidget(self.bookNameInput, 0, 1, 1, 3)
        gLayOut.addWidget(authorLabel, 1, 0)
        gLayOut.addWidget(self.authorInput, 1, 1, 1, 3)
        gLayOut.addWidget(chinesizationLabel, 2, 0)
        gLayOut.addWidget(self.chinesizationInput, 2, 1, 1, 3)
        gLayOut.addWidget(comicMarketLabel, 3, 0)
        gLayOut.addWidget(self.comicMarketInput, 3, 1, 1, 1)
        gLayOut.addWidget(originalLabel, 4, 0)
        gLayOut.addWidget(self.originalInput, 4, 1, 1, 3)
        gLayOut.addWidget(classifyLabel, 5, 0)
        gLayOut.addWidget(self.classifyInput, 5, 1, 1, 3)

        self.favourite = QCheckBox("喜欢", self)
        self.unread = QCheckBox('未看', self)
        gLayOut.addWidget(self.favourite, 6, 1)
        gLayOut.addWidget(self.unread, 6, 2)

        done = QPushButton('确认')
        done.clicked.connect(self.confirm)
        cancel = QPushButton('取消')
        cancel.clicked.connect(self.close)
        gLayOut.addWidget(done, 10, 2)
        gLayOut.addWidget(cancel, 10, 3)

        pics = QGroupBox()
        pics.setTitle('选择封面')
        self.pic_layout = QHBoxLayout(pics)

        self.face0 = QToolButton()
        self.face0.setText(self.faceList[0])
        self.face0.setIcon(QIcon(os.path.join(self.path, self.faceList[0])))
        self.face0.setIconSize(QSize(100, 100))
        self.face0.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.face0.clicked.connect(self.selectFace0Function)
        self.face0.setDown(True)
        self.face0.setMaximumWidth(100)
        self.pic_layout.addWidget(self.face0)

        self.face1 = QToolButton()
        self.face1.setText(self.faceList[1])
        self.face1.setIcon(QIcon(os.path.join(self.path, self.faceList[1])))
        self.face1.setIconSize(QSize(100, 100))
        self.face1.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.face1.clicked.connect(self.selectFace1Function)
        self.face1.setMaximumWidth(100)
        self.pic_layout.addWidget(self.face1)

        self.face2 = QToolButton()
        self.face2.setText(self.faceList[2])
        self.face2.setIcon(QIcon(os.path.join(self.path, self.faceList[2])))
        self.face2.setIconSize(QSize(100, 100))
        self.face2.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.face2.clicked.connect(self.selectFace2Function)
        self.face2.setMaximumWidth(100)
        self.pic_layout.addWidget(self.face2)

        gLayOut.addWidget(pics, 7, 0, 3, 5)

        self.setLayout(gLayOut)
        self.show()

    def setMainWindow(self):
        # 设置位置和大小
        self.setGeometry(300, 300, 600, 300)
        self.setWindowTitle('加入单本新书')
        self.setWindowIcon(QIcon('tx.jpg'))

    # 发送新书数据
    def confirm(self):
        # 除了时间和originalname其他都需要在这里做决定
        self.newBook['original_path'] = self.path
        self.newBook['author'] = self.authorInput.text().replace(' ', '')
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
        self.newBook['new_name'] = '[' + self.newBook['author'] + ']' + self.newBook['book_name'] + '[' + self.newBook['chinesization'] + ']'
        if self.newBook['Cxx'] != 'C00':
            self.newBook['new_name'] += ('(' + self.newBook['Cxx'] + ')')
        self.newBook['address'] = os.path.join(
            './books', self.newBook['author'], self.newBook['new_name'])
        self.close()
        self.after_close_signal.emit(self.newBook)

    # 选择封面
    def selectFace0Function(self):
        self.face0.setDown(True)
        self.face1.setDown(False)
        self.face2.setDown(False)
        self.faceSelected = self.faceList[0]

    def selectFace1Function(self):
        self.face0.setDown(False)
        self.face1.setDown(True)
        self.face2.setDown(False)
        self.faceSelected = self.faceList[1]

    def selectFace2Function(self):
        self.face0.setDown(False)
        self.face1.setDown(False)
        self.face2.setDown(True)
        self.faceSelected = self.faceList[2]


def isPic(name: str):
    ext = os.path.splitext(name)[1]
    return ext == '.jpg' or ext == '.png' or ext == '.jpeg'