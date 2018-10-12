# 这是一个书籍管理系统

## 功能

* 查找书籍（名称，作者，分类）
* 文件的排序功能
* 添加新书籍的功能（填入作者、名字、系列、Cxx、分类、封面，是否喜欢, 汉化者）
* 修改书籍的属性（同上）
* 分类的添加和删除和修改
* 喜欢的书籍
* 未看的书籍

## 使用注意

* ！！重要！！千万不要手动修改books文件夹内的任何内容，否则会引起不可预料的错误

* 点击书目时右侧会有预览，但是一些图片由于质量太高所以加载时会很慢所以为了提高预览速度软件会自动生成一个小质量的预览图（宽度400）,而原来那张高质量的图片放在文件夹最后名字为：备份XXX.jpg

* 在添加新书时点击会有延迟：图片加载的锅

* 添加新书时会产生密集的文件转移，所以在添加新书期间不要做文件操作，估计大家的龟速机械马上就爆炸了

* 这只是一个管理软件，由于生命有限我暂时不会加入本子浏览器，浏览就交给文件管理器了

* 不是很（懒得）理解QTreeView和QStandardItemModel的运作原理，依葫芦画瓢搞出了列表界面

* 这个东西是我一边学Python一边学PyQt一边写的，所以质量什么的。。。。

* classify表内意义不明的book_list是早期设计的残留，不知道以后会不会有用

* 自动分割书名只是给用户减少一些操作，不能完全依赖

## 设计

### Book表

<pre>
('''create table books (
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
    new_name text,
)''')
</pre>

## Classify表

<pre>
('''create table classify(
    name text primary key,
    book_list text
)''')
</pre>

## 开发日志

* 2018-8-29:
  * 主页面框架开发
  * 文件读取，文件名处理
  * 完成加入新书的弹出窗口
* 2018-8-30
  * 加入新书基本功能完成
  * 加入新分类功能完成
  * QTreeView加入新功能
  * 完成book类
  * 完成classify类
* 2018-08-31
  * 树状图加入点击切换列表
  * 书名列表加入左键，双击打开资源管理器，右键菜单
  * book类加入给单个书本加入分类和删除分类的功能
  * 主界面加入增加分类的功能
  * textBrowser能显示的信息增加
  * 加入复制书本信息功能
  * 加入未读类，喜欢类，未分类类的保存方法
* 2018-09-07
  * 发现了SQlite这种嵌入式数据库，用不着我自己写数据存储模块了emmmmm，所以上面的数据操作基本上重写
* 2018-09-12
  * 分类以字符串的形式存储
* 2018-09-19
  * 除了搜索和修改书本信息基本上搞完
  * 加入修改书本信息方法
  * 加入标签图标
  * 美化界面了（可能）
  * 加入图片预览
  * 临危受命去参加CCPC秦皇岛区域赛，项目先鸽了
* 2018-09-29
  * CCPC区域赛归来，不出意料打铁。。。。嘤嘤嘤
* 2018-10-01
  * 加入添加多本书方法
  * 设置图标
  * 加入搜索功能
  * 当软件第一次运行时会初始化数据库
* 2018-10-03
  * 调试改BUG(快速迭代。。。)
* 2018-10-06
  * 多线程加入
  * 加入新书和修改书本信息方法通过信号槽来进行线程间的通讯
  * 批量修改功能
* 2018-10-07
  * 创建预览图以提升体验
  * 小修小补
  * 拖拽添加（感觉有了灵魂）

<!-- 
### 加载
* 读入全部作者名保存为列表
* 读入classify.json: dict
* 读入favourite.json: list
* 读入unread.json: list
* 读入books.json: dict
* 把分类显示到左侧栏
* 读取封面，把unread的书籍显示到内容区

### Book类部分功能设计
* add(self, book: dict)
    * 传入新书
    * 检查是否存在相同的书
    * 检查是否有类似的书名，显示类似的书名
    * 在总books: dict加入新书
    * 保存books.json
    * 返回是否喜欢，分类
* remove(self, address: str)
    * 检查是否已经存在
    * 删除book信息
    * 保存books.json
    * 返回分类
* modify(self, book:dict)
    * 检查是否存在书
    * 更改books:dict内地信息
    * 保存books.json
    * 返回是否喜欢, 分类
### Classify类功能部分设计
* add(self, classify_name: str)
    * 检查是否已经存在分类
    * 把分类加入list
    * 保存classify.json
* remove(self, classift_name: str)
    * 检查是否存在当前分类
    * 删除list内当前分类
    * 保存classify.json
    * 返回当前分类下的所有书籍
### 彻底删除书籍信息
* def deleteBook(book_address: str)
    * 判断此书是否存在
    * 删除book_class内的书
    * 返回当前书的dict
    * 删除unread_all表内该书，保存
    * 删除favourite表内该书，保存
    * 删除对应分类下该书，保存
    * 显示结果于textBrowser

 -->