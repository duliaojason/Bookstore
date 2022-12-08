# bookstore
[![Build Status](https://travis-ci.com/DaSE-DBMS/bookstore.svg?branch=master)](https://travis-ci.com/DaSE-DBMS/bookstore)
[![codecov](https://codecov.io/gh/DaSE-DBMS/bookstore/branch/master/graph/badge.svg)](https://codecov.io/gh/DaSE-DBMS/bookstore)


## 功能

实现一个提供网上购书功能的网站后端。<br>
网站支持书商在上面开商店，购买者可以通过网站购买。<br>
买家和卖家都可以注册自己的账号。<br>
一个卖家可以开一个或多个网上商店，
买家可以为自已的账户充值，在任意商店购买图书。<br>
支持 下单->付款->发货->收货 流程。<br>

1.实现对应接口的功能，见项目的doc文件夹下面的.md文件描述 （60%）<br>

其中包括：

1)用户权限接口，如注册、登录、登出、注销<br>

2)买家用户接口，如充值、下单、付款<br>

3)卖家用户接口，如创建店铺、填加书籍信息及描述、增加库存<br>

通过对应的功能测试，所有test case都pass <br>


2.为项目添加其它功能 ：（40%）<br>

1)实现后续的流程 <br>
发货 -> 收货

2)搜索图书 <br>
用户可以通过关键字搜索，参数化的搜索方式；
如搜索范围包括，题目，标签，目录，内容；全站搜索或是当前店铺搜索。
如果显示结果较大，需要分页
(使用全文索引优化查找)

3)订单状态，订单查询和取消定单<br>
用户可以查自已的历史订单，用户也可以取消订单。<br>
取消定单可由买家主动地取消定单，或者买家下单后，经过一段时间超时仍未付款，定单也会自动取消。 <br>


## bookstore目录结构
```
bookstore
  |-- be                            后端
        |-- model                     后端逻辑代码
        |-- view                      访问后端接口
        |-- ....
  |-- doc                           JSON API规范说明
  |-- fe                            前端访问与测试代码
        |-- access
        |-- bench                     效率测试
        |-- data                    
            |-- book.db                 sqlite 数据库(book.db，较少量的测试数据)
            |-- book_lx.db              sqlite 数据库(book_lx.db， 较大量的测试数据，要从网盘下载)
            |-- scraper.py              从豆瓣爬取的图书信息数据的代码
        |-- test                      功能性测试（包含对前60%功能的测试，不要修改已有的文件，可以提pull request或bug）
        |-- conf.py                   测试参数，修改这个文件以适应自己的需要
        |-- conftest.py               pytest初始化配置，修改这个文件以适应自己的需要
        |-- ....
  |-- ....
```


## 安装配置
安装python (需要python3.6以上) 

进入bookstore文件夹下：

安装依赖

    pip install -r requirements.txt

执行测试
    
    bash script/test.sh

bookstore/fe/data/book.db中包含测试的数据，从豆瓣网抓取的图书信息，其DDL为：
 
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


## 要求

3人一组，做好分工，完成下述内容：

1.bookstore文件夹是该项目的demo，采用flask后端框架与sqlite数据库，实现了前60%功能以及对应的测试用例代码。要求利用ORM使用postgreSQL数据库实现前60%功能，可以在demo的基础上进行修改，也可以采用其他后端框架重新实现。需要通过fe/test/下已有的全部测试用例。

2.在完成前60%功能的基础上，继续实现后40%功能，要有接口、后端逻辑实现、数据库操作、代码测试。对所有接口都要写test case，通过测试并计算测试覆盖率（尽量提高测试覆盖率）。

3.尽量使用索引、事务处理等关系数据库特性，对程序与数据库执行的性能有考量

4.尽量使用git等版本管理工具

5.不需要实现界面，通过代码测试体现功能与正确性


## 报告内容

1.每位组员的学号、姓名，以及分工

2.关系数据库设计：概念设计、ER图、关系模式等

3.对60%基础功能和40%附加功能的接口、后端逻辑、数据库操作、测试用例进行介绍，展示测试结果与测试覆盖率。

4.如果完成，可以展示本次大作业的亮点，比如要求中的“3 4”两点。

注：验收依据为报告，本次大作业所作的工作要完整展示在报告中。


## 验收与考核准测

- 提交 **代码+报告** 压缩包到 **第二次大作业提交** 入口，命名规则：2022_CDMS_PJ2_第几组
- 提交截止日期：**2022.12.10 22:00**

本次大作业不需要提交演示视频，验收的依据是报告：

1. 没有提交或没有实质的工作，得D
2. 完成"要求"中的第1点，可得C
3. 完成前2点，通过全部测试用例且有较高的测试覆盖率，可得B
4. 完成前2点的基础上，体现出第3 4点，可得A


## 附加任务

本次考核不做要求 

学有余力的同学可以尝试下述内容，可以写在报告里：

更多的数据 book_lx.db 可以从网盘下载，下载地址为：

    https://pan.baidu.com/s/1bjCOW8Z5N_ClcqU54Pdt8g

提取码：

    hj6q
    
这份数据同bookstore/fe/data/book.db的schema相同，但是有更多的数据(约3.5GB, 40000+行)

可以将book_lx.db导入到数据库中，测试下单及付款两个接口的性能（最好分离负载生成和后端），测出支持的每分钟交易数，延迟等。
