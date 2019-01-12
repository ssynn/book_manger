from PyQt5.QtWidgets import QTableWidget, QApplication, QTableWidgetItem, QWidget, QHBoxLayout, QAbstractItemView
import sys


class MyTable(QWidget):
    def __init__(self, info: list):
        super().__init__()
        self.table = QTableWidget(0, 1)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.itemClicked.connect(self.clickFunction)
        for i in info:
            temp = QTableWidgetItem(i)
            temp.name = i
            self.table.insertRow(0)
            self.table.setItem(0, 0, temp)

        self.table.verticalScrollBar().setStyleSheet('''
            QScrollBar{background:transparent; width: 10px;}
            QScrollBar::handle{background:lightgray; border:2px solid transparent; border-radius:5px;}
            QScrollBar::handle:hover{background:gray;}
            QScrollBar::sub-line{background:transparent;}
            QScrollBar::add-line{background:transparent;}
        ''')

        t = QHBoxLayout()
        t.addWidget(self.table)
        self.setLayout(t)
        self.show()

    def clickFunction(self):
        print(dir(self.table.selectedItems()[0]),
              self.table.selectedItems()[0].name)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MyTable(['1', '2', '3'])
    sys.exit(app.exec_())
