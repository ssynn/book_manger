import sys
import os
import sqlite3
from PyQt5.QtWidgets import QApplication
from model import main_widget

if __name__ == '__main__':
    if 'data' not in os.listdir('./'):
        os.mkdir('data')
        with open('./data/path.json', 'w') as p:
            p.write('./')
    if 'books' not in os.listdir('./'):
        os.mkdir('books')
    # 检查数据库
    conn = sqlite3.connect('./data/data.db')
    cursor = conn.cursor()
    database = os.listdir("./data")
    tables = cursor.execute("select name from sqlite_master where type='table'").fetchall()
    # 如果是第一次使用则初始化数据库
    if not ('books',) in tables:
        cursor.execute('''create table books (
                address text primary key,
                face text,
                classify text,
                book_name text,
                Cxx varchar(10),
                chinesization text,
                author text,
                favourite int,
                date text,
                unread int,
                original_name text,
                new_name text
                )''')
    if not ('classify',) in tables:
        cursor.execute('''create table classify(
            name text primary key
        )''')
    cursor.close()
    conn.commit()
    conn.close()

    app = QApplication(sys.argv)
    ex = main_widget.MainWidget()
    sys.exit(app.exec_())
