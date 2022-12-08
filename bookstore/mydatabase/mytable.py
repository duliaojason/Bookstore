from sqlalchemy import Column, String, create_engine, Integer, Text, Date, LargeBinary, JSON
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
import datetime

#在这里我们需要更新数据库，需要更新的分别是链接池的大小，还有就是需要设置报警的时间，防止出现卡顿，最后对进程进行回收
engine = create_engine(
    "postgresql://stu10205501457:Stu10205501457@dase-cdms-2022-pub.pg.rds.aliyuncs.com:5432/stu10205501457",
    max_overflow=0,
    pool_size=5,
    pool_timeout=10,
    pool_recycle=1,
    echo=True
    )
Session = sessionmaker(bind=engine)
session = scoped_session(Session)
DbSession = sessionmaker(bind=engine)
session = DbSession()

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()


#定义user表格，用户可以拥有买书和卖书的双权限
class User1(Base):
    __tablename__ = "User"
    user_id = Column(String(128), primary_key=True, comment="用户名")
    password = Column(String(128), nullable=False, comment="密码")
    balance = Column(Integer, nullable=False, comment="余额")
    token = Column(Text, nullable=False, comment="token")
    terminal = Column(String(32), nullable=False, comment="terminal")

#定义书店（商铺）表格
class Store1(Base):
    __tablename__ = "Store"
    store_id = Column(String(128), primary_key=True, comment="书店id")

#定义书本表格
class Book1(Base):
    __tablename__ = "Book"
    id = Column(String(8), primary_key=True, comment="主键")
    title = Column(String(32), nullable=False, comment="书名")
    author = Column(String(16), nullable=True, comment="作者")
    publisher = Column(String(16), nullable=False, comment="出版社")
    original_title = Column(Text, nullable=True, comment="原名")
    translator = Column(String(32), nullable=True, comment="译者")
    pub_year = Column(String(16), nullable=False, comment="出版年")
    pages = Column(Integer, nullable=False, comment="页数")
    price = Column(Integer, nullable=False, comment="价格")
    currency_unit = Column(String(16), nullable=False, comment="货币单位")
    binding = Column(String(8), nullable=False, comment="装订")
    isbn = Column(String(16), nullable=False, comment="书号")
    author_intro = Column(Text, nullable=False, comment="作者简介")
    book_intro = Column(Text, nullable=False, comment="书本简介")
    content = Column(Text, nullable=False, comment="目录")
    tags = Column(Text, nullable=False, comment="标记")
    picture = Column(LargeBinary, nullable=False, comment="图片")

#定义用户和书店的关系表
class StoreUser1(Base):
    __tablename__ = "StoreUser"
    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键")
    fk_store_id = Column(
        String(128),
        ForeignKey(
            "Store.store_id",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        nullable=False,
        comment="书店"
    )
    fk_user_id = Column(
        String(128),
        ForeignKey(
            "User.user_id",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        nullable=False,
        comment="店主"
    )
    owner = relationship(
        "User",
        backref="store_user",
    )
    store = relationship(
        "Store",
        backref="store_user",
    )

#定义书店和里面藏书的关系
class StoreBook1(Base):
    __tablename__ = "StoreBook"
    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键")
    stock_level = Column(Integer, nullable=False, comment="库存")
    book_info = Column(Text, nullable=False, comment="书本信息")
    fk_store_id = Column(
        String(128),
        ForeignKey(
            "Store.store_id",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        nullable=False,
        comment="书店"
    )
    fk_book_id = Column(
        String(8),
        ForeignKey(
            "Book.id",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        nullable=False,
        comment="书本"
    )

    store = relationship(
        "Store",
        backref="store_book",
    )
    book = relationship(
        "Book",
        backref="store_book",
    )

#定义订单的各类状态
class Order1(Base):
    __tablename__ = "Order"
    order_id = Column(String(200), primary_key=True, comment="主键")
    time = Column(Date, nullable=False, comment="时间")
    total_price = Column(Integer, nullable=False, comment="总价")
    status = Column(Integer, nullable=False, comment="状态")

    fk_buyer_id = Column(
        String(128),
        ForeignKey(
            "User.user_id",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        nullable=False,
        comment="买方"
    )
    fk_store_id = Column(
        String(128),
        ForeignKey(
            "Store.store_id",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        nullable=False,
        comment="书店"
    )

#定义账单和书本之间的关系，这里一定要注意账单可以订到重复的同样的书本，同时相同的书本也可以被多个账单涉及
class OrderBook1(Base):
    __tablename__ = "OrderBook"
    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键")
    num = Column(Integer, nullable=False, comment="数量")
    price = Column(Integer, nullable=False, comment="总价")

    fk_order_id = Column(
        String(200),
        ForeignKey(
            "Order.order_id",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        nullable=False,
        comment="订单"
    )
    fk_book_id = Column(
        String(8),
        ForeignKey(
            "Book.id",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        nullable=False,
        comment="书本"
    )
    order = relationship(
        "Order",
        backref="order_book",
    )
    book = relationship(
        "Book",
        backref="order_book",
    )


# 连接数据库
def init():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    Base.metadata.create_all(engine)  # 创建所有继承于Base的类对应的表
    session.commit()
    session.close()


# 少量测试用例
def test_sample():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    # 创建 测试用户
    test_user_1 = User1(
        user_id = 'red',
        password = '111111',
        balance = 100,
        token = '***',
        terminal = 'Chrome'
    )
    test_user_2 = User1(
        user_id = 'blue',
        password = '222222',
        balance = 200,
        token = '***',
        terminal = 'Edge'
    )
    # 创建 测试用户-商店
    test_user_store_1 = StoreUser1(
        user_id = 'red',
        store_id = 'bookstore1'
    )
    test_user_store_2 = StoreUser1(
        user_id = 'red',
        store_id = 'bookstore2'
    )
    # 创建 测试商店
    test_store_1 = Store1(
        store_id = 'bookstore1',
        book_id = 1,
        stock_level = 10,
        price = 2000, # 价格单位是分
    )
    test_store_2 = Store1(
        store_id = 'bookstore2',
        book_id = 2,
        stock_level = 10,
        price = 2580, # 价格单位是分
    )

    #创建 测试书本添加
    test_store_book = StoreBook1(
        id = '1',
        stock_level= 2,
        book_info = 'hahaha',
    )

    # 创建 测试订单
    test_order_paid = Order1(
        order_id = 'order1',
        buyer_id = 'blue',
        store_id = 'bookstore1',
        price = 2000,
        purchase_time = datetime.now(),
        status = 0  # 未发货
    )
    test_order_detail_paid = OrderBook1(
        order_id = 'order1',
        book_id = 1,
        count = 2,
        price = 4000
    )
    test_order_unpaid = OrderBook1(
        order_id = 'order2',
        buyer_id = 'blue',
        store_id = 'bookstore2',
        price = 2580,
        purchase_time = datetime.now(),
    )
    test_order_detail_unpaid = OrderBook1(
        order_id = 'order1',
        book_id = 1,
        count = 1,
        price = 2580
    )
    session.add_all((test_user_1, test_user_2, test_user_store_1, test_user_store_2, test_store_1, test_store_2,
                     test_order_paid, test_order_detail_paid, test_order_unpaid, test_order_detail_unpaid))
    session.commit()
    session.close()

if __name__ == '__main__':
    # 连接数据库
    init()
    # 执行测试用例
    test_sample()
# if __name__ == "__main__":
#     # 删除表
#     Base.metadata.drop_all(engine)
#     # 创建表
#     Base.metadata.create_all(engine)