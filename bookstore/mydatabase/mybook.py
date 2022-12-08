import sqlite3
from sqlalchemy import create_engine  # , Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, create_engine, Text, LargeBinary
from sqlalchemy.orm import sessionmaker

engine = create_engine(
    "postgresql://stu10205501457:Stu10205501457@dase-cdms-2022-pub.pg.rds.aliyuncs.com:5432/stu10205501457")

Base = declarative_base()
DBSession = sessionmaker(bind=engine)
session = DBSession()

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

#更新书本库存
def init():
    global DBSession, Base
    DBSession = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)

    # 这里的路径一定要记得修改
    conn = sqlite3.connect(r"E:\当代数据管理系统\Bookstore\main reference\2022_CDMS_PJ2_REQUIRE\bookstore\fe\data\book.db")
    cursor = conn.cursor()
    sql = """select * from book;"""
    cursor.execute(sql)
    result = cursor.fetchall()
    conn.close()
    print("Load data from database, Done.")

    print("Data size %d" % (len(result)))
    session = DBSession()
    for b in result:
        book = Book1(
            id=b[0],
            title=b[1],
            author=b[2],
            publisher=b[3],
            original_title=b[4],
            translator=b[5],
            pub_year=b[6],
            pages=b[7],
            price=b[8],
            currency_unit=b[9],
            binding=b[10],
            isbn=b[11],
            author_intro=b[12],
            book_intro=b[13],
            content=b[14],
            tags=b[15],
            picture=b[16],
        )
        session.add(book)
    del result
    session.commit()
    session.close()
    print("Passed")

    #检查书本是否被正确插入表格
    session = DBSession()
    result = session.query(Book1.title).first()
    session.close()
    print(result)




