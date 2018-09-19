import sys
from PyQt5.QtWidgets import QApplication
from model import main_widget

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = main_widget.MainWidget()
    sys.exit(app.exec_())
