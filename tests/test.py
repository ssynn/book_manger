# %%
from model import public_function as pf
import sqlite3
conn = sqlite3.connect('./data/data.db')
cursor = conn.cursor()
cursor.execute("select name from sqlite_master where type='table'")
print(cursor.fetchall())

# %%
print(cursor.execute("pragma table_info(classify)").fetchall())

# %%
print(cursor.execute('select * from classify').fetchall())

# %%
print(pf.addNewClassify(['11']))

# %%
print(pf.deleteClassify('23'))

# %%
a = [1, 2, 4]
print(a.reverse(), a)
