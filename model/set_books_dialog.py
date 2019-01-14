import os
import time
from PyQt5.QtWidgets import (QWidget, QGridLayout, QTableWidget,
                             QLabel, QLineEdit, QTableWidgetItem, QGroupBox,
                             QCheckBox, QHBoxLayout, QVBoxLayout, QToolButton,
                             QAbstractItemView)
from PyQt5.QtGui import QIcon, QImage
from PyQt5.QtCore import Qt, QSize, pyqtSignal
from model import public_function as pf


# self.newBook为当前显示的书本, 传入文件地址列表或书籍信息列表初始化
class SetMultiMessage(QWidget):
    stateChange = pyqtSignal(str)
    after_close_signal = pyqtSignal(list)

    # address 为 True说明传入的是地址否则为书籍信息
    def __init__(self, filelist: list, master, address=False):
        super().__init__()

        self.bookList = []

        # 传入的是地址
        if address:
            for i in filelist:
                dirName = os.path.split(i)[1]
                temp = pf.bookNameCut(dirName)
                temp['face_list'] = os.listdir(i)[:6]
                temp['face_list'] = list(filter(isPic, temp['face_list']))[:3]
                if len(temp['face_list']) < 3:
                    print(temp['original_name'])
                    continue
                temp['face'] = temp['face_list'][0]
                temp['original_path'] = i
                temp['drop'] = False
                self.bookList.append(temp)
        # 传入的是直接信息
        else:
            self.bookList = filelist
            for i in self.bookList:
                i['face_list'] = os.listdir(i['address'])
                i['face_list'] = list(filter(isPic, i['face_list']))[:3]
                i['original_path'] = i['address']
                i['drop'] = False

        if len(self.bookList) != 0:
            self.newBook = self.bookList[0]
            self.initUI()
        else:
            master.textOut.append(time.strftime(
                "%Y-%m-%d %H:%M") + "没有找到合法的书籍。")
            return

    def initUI(self):
        self.setGeometry(600, 200, 1000, 500)
        self.setFixedSize(1000, 500)
        self.body = QGridLayout(self)
        self.setWindowTitle("批量添加")
        self.setWindowIcon(QIcon('pic/tx.jpg'))

        # 列表视图
        self.left = self.createBookModel()
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

        # 结束操作
        self.done = QToolButton()
        self.done.setText('确认')
        self.done.clicked.connect(self.finish)
        self.done.setFixedSize(100, 30)

        self.cancel = QToolButton()
        self.cancel.setText('取消')
        self.cancel.clicked.connect(self.close)
        self.cancel.setFixedSize(100, 30)

        self.body.addWidget(self.done, 10, 9)
        self.body.addWidget(self.cancel, 10, 10)
        self.setInformation()
        self.setMyStyle()
        self.show()

    def createBookModel(self):
        table = QTableWidget(0, 1)
        table.setFixedWidth(470)
        table.verticalHeader().setVisible(False)
        table.horizontalHeader().setVisible(False)
        table.setFocusPolicy(Qt.NoFocus)
        table.setAlternatingRowColors(True)
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        table.itemClicked.connect(self.clickFunction)
        table.setColumnWidth(0, 470)

        for i in self.bookList:
            temp = QTableWidgetItem(i['original_name'])
            temp.info = i
            table.insertRow(0)
            table.setItem(0, 0, temp)

        table.verticalScrollBar().setStyleSheet('''
            QScrollBar{background:transparent; width: 10px;}
            QScrollBar::handle{background:lightgray; border:2px solid transparent; border-radius:5px;}
            QScrollBar::handle:hover{background:gray;}
            QScrollBar::sub-line{background:transparent;}
            QScrollBar::add-line{background:transparent;}
        ''')
        return table

    # 右侧设置详细信息部分
    def createMessageBox(self):
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
        self.drop = QCheckBox('丢弃', self)
        self.drop.setFixedWidth(80)

        checkBoxes = QHBoxLayout()
        checkBoxes.addWidget(self.favourite)
        checkBoxes.addWidget(self.unread)
        checkBoxes.addWidget(self.drop)

        # 选择封面
        pics = QGroupBox()
        pics.setTitle('选择封面')
        pics.setMinimumHeight(180)
        self.pic_layout = QHBoxLayout(pics)

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

        self.facesBtn = [self.face0, self.face1, self.face2]
        self.selectFace0Function()

        body = QVBoxLayout()
        body.addLayout(infoLine)
        body.addLayout(checkBoxes)
        body.addWidget(pics)
        return body

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
        self.newBook['drop'] = int(self.drop.isChecked())
        image = QImage()
        image.load(os.path.join(
            self.newBook['original_path'], self.newBook['face']))
        image.save(os.path.join(
            self.newBook['original_path'], self.newBook['face']))

    def setInformation(self):
        self.bookNameInput.setText(self.newBook['book_name'])
        self.authorInput.setText(self.newBook['author'])
        self.chinesizationInput.setText(self.newBook['chinesization'])
        self.comicMarketInput.setText(self.newBook['Cxx'])
        self.originalInput.setText(self.newBook['original_name'])
        self.classifyInput.setText(self.newBook['classify'])
        self.favourite.setChecked(bool(self.newBook['favourite']))
        self.unread.setChecked(bool(self.newBook['unread']))
        self.drop.setChecked(bool(self.newBook['drop']))
        if 'icon_list' not in self.newBook:
            self.newBook['icon_list'] = [
                QIcon(os.path.join(self.newBook['original_path'], self.newBook['face_list'][0])),
                QIcon(os.path.join(self.newBook['original_path'], self.newBook['face_list'][1])),
                QIcon(os.path.join(self.newBook['original_path'], self.newBook['face_list'][2]))
            ]
        self.face0.setIcon(self.newBook['icon_list'][0])
        self.face0.setMaximumWidth(110)
        self.face1.setIcon(self.newBook['icon_list'][0])
        self.face1.setMaximumWidth(110)
        self.face2.setIcon(self.newBook['icon_list'][2])
        self.face2.setMaximumWidth(110)

        self.refresh()
        self.faceSelected = self.newBook['face']
        self.face0.setText(self.newBook['face_list'][0])
        self.face1.setText(self.newBook['face_list'][1])
        self.face2.setText(self.newBook['face_list'][2])

        if self.face0.text() == self.newBook['face']:
            self.selectFace0Function()
        if self.face1.text() == self.newBook['face']:
            self.selectFace1Function()
        if self.face2.text() == self.newBook['face']:
            self.selectFace2Function()

    # 选择封面
    def selectFace0Function(self):
        self.faceSelected = self.newBook['face_list'][0]
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
        self.faceSelected = self.newBook['face_list'][1]
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
        self.faceSelected = self.newBook['face_list'][2]
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

    # 选择书籍
    def clickFunction(self):
        self.confirm()
        self.newBook = self.left.selectedItems()[0].info
        self.setInformation()

    # 关闭窗口，传回包含书本信息的list
    def finish(self):
        self.confirm()
        result = []

        for i in self.bookList:
            if i['drop']:
                continue

            # 设置全局喜欢，未读，分类
            if self.publicFavourite.isChecked():
                i['favourite'] = 1
            if self.publicUnread.isChecked():
                i['unread'] = 1

            # 添加公共分类
            if len(self.publicClassifyInput.text()) != 0:
                if len(i['classify']) != 0:
                    i['classify'] += ' '
                i['classify'] += self.publicClassifyInput.text()

            # 设置公共作者
            if len(self.publicAuthorInput.text()) != 0:
                i['author'] = self.publicAuthorInput.text()

            # 生成最终决定的书名和地址
            i['new_name'] = f"[{i['author']}]{i['book_name']}[{i['chinesization']}]"

            if i['Cxx'] != 'C00':
                i['new_name'] += ('(' + i['Cxx'] + ')')

            i['address'] = os.path.join(
                './books',
                i['author'],
                i['new_name']
            )
            result.append(i)
        self.close()
        self.after_close_signal.emit(result)

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
                border-radius: 5px;
                font-family: 微软雅黑;
                font-size: 18px;
                color: #6d6d6d;
            }
            QLabel{
                font-family: 微软雅黑;
                font-size: 18px;
            }
            QTableWidget{
                border-radius: 3px;
                border: 1px solid #BDBDBD;
            }
            QTableWidget::item:selected { background-color: #99d1ff; }
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


def isPic(name: str):
    ext = os.path.splitext(name)[1]
    return ext == '.jpg' or ext == '.png' or ext == '.jpeg' or ext == '.JPG'
