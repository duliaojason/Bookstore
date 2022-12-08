from sqlalchemy import Column, String, create_engine, Integer, Text, Date, LargeBinary, ForeignKey
from sqlalchemy.orm import sessionmaker, scoped_session, relationship
from sqlalchemy.ext.declarative import declarative_base

engine = None
Base = declarative_base()
DbSession = None


# Postgresql，orm连接数据库
class DataBase:
    def __init__(self):
        self.engine = engine
        self.Base = Base
        self.DbSession = DbSession

    def user_id_exist(self, user_id):
        session = self.DbSession()
        result = session.query(User1.user_id).filter(User1.user_id == user_id).first()
        session.close()
        if result is None:
            return False
        else:
            return True

    def book_id_exist(self, store_id, book_id):
        session = self.DbSession()
        result = session.query(
            StoreBook1
        ).filter(
            StoreBook1.fk_store_id == store_id, StoreBook1.fk_book_id == book_id
        ).first()
        session.close()
        if result is None:
            return False
        else:
            return True

    def store_id_exist(self, store_id):
        session = self.DbSession()
        result = session.query(Store1.store_id).filter(Store1.store_id == store_id).first()
        session.close()
        if result is None:
            return False
        else:
            return True

#在这里我们需要更新数据库，需要更新的分别是链接池的大小，还有就是需要设置报警的时间，防止出现卡顿，最后对进程进行回收
def init_database():
    global engine, Base, DbSession
    engine = create_engine(
        "postgresql://stu10205501457:Stu10205501457@dase-cdms-2022-pub.pg.rds.aliyuncs.com:5432/stu10205501457",
        max_overflow=0,
        pool_size=5,
        pool_timeout=10,
        pool_recycle=1
    )
    Session = sessionmaker(bind=engine)
    session = scoped_session(Session)
    DbSession = sessionmaker(bind=engine)
    Base = declarative_base()
    # all tables are deleted
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    init_database()
    print("done")

#定义user表格，用户可以拥有买书和卖书的双权限
class User1(Base):
    __tablename__ = "User"
    user_id = Column(String(128), primary_key=True, comment="用户名")
    password = Column(String(128), nullable=False, comment="登录密码")
    balance = Column(Integer, nullable=False, comment="余额")
    token = Column(Text, nullable=False, comment="标志")
    terminal = Column(String(32), nullable=False, comment="终端代码")

#定义书店（商铺）表格
class Store1(Base):
    __tablename__ = "Store"
    store_id = Column(String(128), primary_key=True, comment="商铺")

#定义书本表格
class Book1(Base):
    __tablename__ = "Book"
    id = Column(String(8), primary_key=True, comment="序列号")
    title = Column(String(32), nullable=False, comment="书本标题")
    author = Column(String(16), nullable=True, comment="作者")
    publisher = Column(String(16), nullable=False, comment="发布者")
    original_title = Column(Text, nullable=True, comment="书本原名")
    translator = Column(String(32), nullable=True, comment="编译者名")
    pub_year = Column(String(16), nullable=False, comment="发布年份")
    pages = Column(Integer, nullable=False, comment="书本页码")
    price = Column(Integer, nullable=False, comment="书本价格")
    currency_unit = Column(String(16), nullable=False, comment="货币")
    binding = Column(String(8), nullable=False, comment="书本装订")
    isbn = Column(String(16), nullable=False, comment="书本序列号")
    author_intro = Column(Text, nullable=False, comment="作者简介")
    book_intro = Column(Text, nullable=False, comment="书本简介")
    content = Column(Text, nullable=False, comment="目录")
    tags = Column(Text, nullable=False, comment="标记")
    picture = Column(LargeBinary, nullable=False, comment="图片")

#定义用户和书店的关系表（此处运用到正反查询）
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
    id = Column(Integer, primary_key=True, autoincrement=True, comment="序列号")
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

    """用于正反查询，书店和书本"""
    store = relationship(
        "Store",
        backref="store_book",
    )
    book = relationship(
        "Book",
        backref="store_book",
    )

#定义订单的各类状态，status存在5个状态，0表示待付款，1表示尚未发货，2表示已经发货，3表示已经收货，-1表示订单已经取消
class Order1(Base):
    __tablename__ = "Order"
    order_id = Column(String(200), primary_key=True, comment="序列号")
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
        comment="买家"
    )
    fk_store_id = Column(
        String(128),
        ForeignKey(
            "Store.store_id",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        nullable=False,
        comment="商铺"
    )

#定义账单和书本之间的关系，这里一定要注意账单可以订到重复的同样的书本，同时相同的书本也可以被多个账单涉及（涉及正反查询）
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



