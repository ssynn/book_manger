import os
import time
from model import public_function as pf
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLineEdit,
    QLabel,
    QCheckBox,
    QHBoxLayout,
    QToolButton,
    QGroupBox
)
from PyQt5.QtGui import QIcon, QImage
from PyQt5.QtCore import Qt, pyqtSignal, QSize


# 传入完整路径初始化,返回装着书本信息的dict
class SetBookMessage(QWidget):
    '''
    传入书地址或者书籍信息和主窗体的实例
    '''
    after_close_signal = pyqtSignal(dict)
    stateChange = pyqtSignal(str)

    def __init__(self, book_, master):
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
            master.textOut.append(time.strftime("%Y-%m-%d %H:%M") + "无法添加此目录!")
            return

        self.faceSelected = self.faceList[0]
        self.setMainWindow()
        self.initUI()

    def initUI(self):
        # 标题列
        bookNameLabel = QLabel('书名')
        bookNameLabel.setAlignment(Qt.AlignRight)
        authorLabel = QLabel("作者")
        authorLabel.setAlignment(Qt.AlignRight)
        chinesizationLabel = QLabel('汉化')
        chinesizationLabel.setAlignment(Qt.AlignRight)
        comicMarketLabel = QLabel("Comic Market")
        comicMarketLabel.setAlignment(Qt.AlignRight)
        classifyLabel = QLabel('分类')
        classifyLabel.setAlignment(Qt.AlignRight)
        originalLabel = QLabel("源文件名")
        originalLabel.setAlignment(Qt.AlignRight)

        labelList = QVBoxLayout()
        labelList.addWidget(bookNameLabel)
        labelList.addWidget(authorLabel)
        labelList.addWidget(chinesizationLabel)
        labelList.addWidget(comicMarketLabel)
        labelList.addWidget(classifyLabel)
        labelList.addWidget(originalLabel)

        # 输入列
        self.bookNameInput = QLineEdit(self)
        self.bookNameInput.setText(self.newBook['book_name'])

        self.authorInput = QLineEdit(self)
        self.authorInput.setText(self.newBook['author'])

        self.chinesizationInput = QLineEdit(self)
        self.chinesizationInput.setText(self.newBook['chinesization'])

        self.comicMarketInput = QLineEdit(self)
        self.comicMarketInput.setText(self.newBook['Cxx'])

        self.classifyInput = QLineEdit(self)
        self.classifyInput.setText(self.newBook['classify'])

        self.originalInput = QLineEdit(self)
        self.originalInput.setText(self.newBook['original_name'])

        inputList = QVBoxLayout()
        inputList.addWidget(self.bookNameInput)
        inputList.addWidget(self.authorInput)
        inputList.addWidget(self.chinesizationInput)
        inputList.addWidget(self.comicMarketInput)
        inputList.addWidget(self.classifyInput)
        inputList.addWidget(self.originalInput)

        # 把上面两列装入一行
        infoLine = QHBoxLayout()
        infoLine.addLayout(labelList)
        infoLine.addLayout(inputList)

        # 选择框
        self.favourite = QCheckBox("喜欢", self)
        self.favourite.setFixedWidth(80)
        self.unread = QCheckBox('未看', self)
        self.unread.setFixedWidth(80)
        self.favourite.setChecked(bool(self.newBook['favourite']))
        self.unread.setChecked(bool(self.newBook['unread']))

        checkBoxes = QHBoxLayout()
        checkBoxes.addWidget(self.favourite)
        checkBoxes.addWidget(self.unread)

        # 选择封面
        pics = QGroupBox()
        pics.setTitle('选择封面')
        pics.setMinimumHeight(180)
        self.pic_layout = QHBoxLayout(pics)

        self.face0 = QToolButton()
        self.face0.setText(self.faceList[0])
        self.face0.setIcon(QIcon(os.path.join(self.path, self.faceList[0])))
        self.face0.setIconSize(QSize(100, 100))
        self.face0.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.face0.clicked.connect(self.selectFace0Function)
        self.face0.setMaximumWidth(110)
        self.pic_layout.addWidget(self.face0)

        self.face1 = QToolButton()
        self.face1.setText(self.faceList[1])
        self.face1.setIcon(QIcon(os.path.join(self.path, self.faceList[1])))
        self.face1.setIconSize(QSize(100, 100))
        self.face1.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.face1.clicked.connect(self.selectFace1Function)
        self.face1.setMaximumWidth(110)
        self.pic_layout.addWidget(self.face1)

        self.face2 = QToolButton()
        self.face2.setText(self.faceList[2])
        self.face2.setIcon(QIcon(os.path.join(self.path, self.faceList[2])))
        self.face2.setIconSize(QSize(100, 100))
        self.face2.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.face2.clicked.connect(self.selectFace2Function)
        self.face2.setMaximumWidth(110)
        self.pic_layout.addWidget(self.face2)

        self.facesBtn = [self.face0, self.face1, self.face2]
        self.selectFace0Function()

        if self.face0.text() == self.newBook['face']:
            self.selectFace0Function()
        if self.face1.text() == self.newBook['face']:
            self.selectFace1Function()
        if self.face2.text() == self.newBook['face']:
            self.selectFace2Function()

        # 结束操作
        self.done = QToolButton()
        self.done.setText('确认')
        self.done.clicked.connect(self.confirm)
        self.done.setFixedSize(100, 30)

        self.cancel = QToolButton()
        self.cancel.setText('取消')
        self.cancel.clicked.connect(self.close)
        self.cancel.setFixedSize(100, 30)

        lastLine = QHBoxLayout()
        lastLine.addStretch()
        lastLine.addWidget(self.done)
        lastLine.addWidget(self.cancel)

        body = QVBoxLayout()
        body.addLayout(infoLine)
        body.addLayout(checkBoxes)
        body.addWidget(pics)
        body.addLayout(lastLine)

        self.setLayout(body)
        self.setMyStyle()
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
        self.newBook['new_name'] = f"[{self.newBook['author']}]{self.newBook['book_name']}[{self.newBook['chinesization']}]"

        if self.newBook['Cxx'] != 'C00':
            self.newBook['new_name'] += ('(' + self.newBook['Cxx'] + ')')

        self.newBook['address'] = os.path.join(
            './books',
            self.newBook['author'],
            self.newBook['new_name']
        )

        self.close()
        self.after_close_signal.emit(self.newBook)

    # 选择封面
    def selectFace0Function(self):
        self.faceSelected = self.faceList[0]
        self.refresh()
        self.face0.setStyleSheet('''
            QToolButton{
                background-color:#e5f3ff;
                border: 1px solid #99d1ff;
            }
            QToolButton:hover{
                background-color: #e5f3ff;
            }
        ''')

    def selectFace1Function(self):
        self.faceSelected = self.faceList[1]
        self.refresh()
        self.face1.setStyleSheet('''
            QToolButton{
                background-color:#e5f3ff;
                border: 1px solid #99d1ff;
            }
            QToolButton:hover{
                background-color: #e5f3ff;
            }
        ''')

    def selectFace2Function(self):
        self.faceSelected = self.faceList[2]
        self.refresh()
        self.face2.setStyleSheet('''
            QToolButton{
                background-color:#e5f3ff;
                border: 1px solid #99d1ff;
            }
            QToolButton:hover{
                background-color: #e5f3ff;
            }
        ''')

    def refresh(self):
        for i in self.facesBtn:
            i.setStyleSheet('''
                QToolButton{
                    background-color:white;
                    border: 1px solid white;
                }
                QToolButton:hover{
                    background-color: #e5f3ff;
                }
            ''')

    def setMyStyle(self):
        self.setStyleSheet('''
            QWidget{
                background-color: white;
            }
            QToolButton{
                font-family: 微软雅黑;
                font-size: 15px;
                border-radius: 5px;
            }
            QGroupBox{
                border-radius: 10px;
                border: 1px solid #BDBDBD;
            }
            QLineEdit{
                border: 1px solid #BDBDBD;
                border-radius: 3px;
                font-family: 微软雅黑;
                font-size: 18px;
                color: #6d6d6d;
            }
            QLabel{
                font-family: 微软雅黑;
                font-size: 18px;
            }
        ''')
        self.done.setStyleSheet('''
            QToolButton{
                color: #448AFF;
                border: 1px solid #448AFF;
            }
            QToolButton:hover{
                background: #448AFF;
                color: white;
            }
        ''')

        self.cancel.setStyleSheet('''
            QToolButton{
                color: #D32F2F;
                border: 1px solid #D32F2F;
                margin-right: 5px;
            }
            QToolButton:hover{
                background: #D32F2F;
                color: white;
            }
        ''')

# 识别图片文件


def isPic(name: str):
    ext = os.path.splitext(name)[1]
    return ext == '.jpg' or ext == '.png' or ext == '.jpeg'
