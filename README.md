# Bookstore Postgres数据库项目

[![Build Status](https://travis-ci.org/1012598167/bookstore.svg?branch=master)](https://travis-ci.org/1012598167/bookstore)[![codecov](https://codecov.io/gh/1012598167/bookstore/branch/master/graph/badge.svg?token=8T1NB3GUYR)](https://codecov.io/gh/1012598167/bookstore)


Postgres实现类似淘宝书店的功能并进行50000笔订单吞吐量测试，CI-> .travis.yml

演示页[https://mathskiller909.com/auth/login](https://mathskiller909.com/auth/login) (updated 20211205)

注：主分支未加入前端(updated 20201219)

前端请去分支[developercn](https://github.com/1012598167/bookstore/tree/developercn)查看，该分支只有/be/view与/be/templates的内容与master不同

不将前端写到master分支的原因是前端使用render_template会无法测覆盖率


## 安装配置

安装python (>=3.6)

安装依赖

```bash
pip install -r requirements.txt
```

执行测试

```bash
bash script/test.sh
```

(先在本地创建bookstore数据库!)初始化数据库(python>=3.6)

```bash
python ./initialize_database/initialize_books.py
python ./initialize_database/initialize_database.py
python ./initialize_database/initialize_search_database.py
```

bookstore/fe/data/book.db中包含测试的数据，从豆瓣网抓取的图书信息， 其DDL为：

```
create table book
(
    id TEXT primary key,
    title TEXT,
    author TEXT,
    publisher TEXT,
    original_title TEXT,
    translator TEXT,
    pub_year TEXT,
    pages INTEGER,
    price INTEGER,
    currency_unit TEXT,
    binding TEXT,
    isbn TEXT,
    author_intro TEXT,
    book_intro text,
    content TEXT,
    tags TEXT,
    picture BLOB
);
```

更多的数据可以从网盘下载，下载地址为，链接：

```
https://pan.baidu.com/s/1bjCOW8Z5N_ClcqU54Pdt8g
```

提取码：

```
hj6q
```

这份数据同bookstore/fe/data/book.db的schema相同，但是有更多的数据(约3.5GB, 40000+行)
