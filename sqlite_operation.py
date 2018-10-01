import sqlite3
import json
from model import public_function

add = ".\\books\呵呵呵\[chin] サクセックスストーリーズ"
conn = sqlite3.connect('./data/data.db')
cursor = conn.cursor()
# 书本
# cursor.execute('''create table books (
#                 address text primary key,
#                 face text,
#                 classify text,
#                 book_name text,
#                 Cxx varchar(10),
#                 chinesization text,
#                 author text,
#                 favourite int,
#                 date text,
#                 unread int,
#                 original_name text,
#                 new_name text,
#                 )''')

# cursor.execute('select * from user')  # 查找
# cursor.execute("drop table books")  # 删除表，没有的话会报错
# cursor.execute("select name from sqlite_master where type='table'")  # 查找所有表
# cursor.execute("pragma table_info(books)")  # 查询表结构
# cursor.execute(''' insert into books values (?,?,?,?,?,?,?,?,?,?,?,?)''', 
                #   [add+'3', '01.jpg', 'NTR', add, 'C94', '肿脸', 1, '2018-09-05', 1, add, add, 'hehe'])  # 插入新字段
# cursor.execute("alter table books add column author text")   # 在表内插入新属性
# cursor.execute("select new_name from books where address=?", [add + '1'])  # 查看table内所有内容, 如果没有找到就返回空列表

# cursor.execute("delete from books") # 删除记录, 如果没有就返回空列表
# cursor.execute("update books set classify='纯爱 NTR' where address=?", [add+'0'])
book_list = cursor.execute("select * from books ").fetchall()  # 查找所有字段
# book_list = cursor.execute("select * from books where classify glob ? ", ['*'+'纯爱'+'*']).fetchall()
# 分类
# cursor.execute('''create table classify(
#     name text primary key,
#     book_list text
# )''')
# cursor.execute("insert into classify values (?,?)", ["unclassified", ""])  # 插入分类
# data = json.dumps([add+'3', add+'0', add+'1'])
# cursor.execute("update classify set name='NTR' where name='ntr' ")
# cursor.execute("select book_list from classify where name='NTR'")
# cursor.execute("delete from classify", [])
# cursor.execute("select * from classify")
# book_list = cursor.fetchall()
# book_list = json.loads(book_list)
# print(book_list)
# print(cursor.fetchall())
# print(all_books)
# for i in range(len(book_list)):
#     book_list[i] = book_list[i][0]
    # print(i[0])
print(book_list)
# for i in public_function.toDictList(book_list):
    # print(i)

cursor.close()
conn.commit()
conn.close()