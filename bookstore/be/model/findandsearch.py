from sqlalchemy import create_engine
from sqlalchemy import Column, String, create_engine, Integer, Text, Date, LargeBinary, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import sessionmaker, scoped_session, relationship
from sqlalchemy.ext.declarative import declarative_base
import re, jieba
import jieba.analyse

engine = create_engine("postgresql://stu10205501457:Stu10205501457@dase-cdms-2022-pub.pg.rds.aliyuncs.com:5432/stu10205501457")
Base = declarative_base()
DBSession = sessionmaker(bind=engine)

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

#对标题进行搜索
class SearchByTitle(Base):
    __tablename__ = 'SearchByTitle'
    title = Column(Text, nullable=False)
    rank = Column(Integer, nullable=False)
    book_id = Column(
        String(8),
        ForeignKey(
            'Book.id',
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        nullable=False
    )
    __table_args__ = (
        PrimaryKeyConstraint('title', 'rank'),
    )

#对标志进行搜索
class SearchByTag(Base):
    __tablename__ = 'SearchByTag'
    tags = Column(Text, nullable=False)
    rank = Column(Integer, nullable=False)
    book_id = Column(
        String(8),
        ForeignKey(
            'Book.id',
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        nullable=False
    )
    __table_args__ = (
        PrimaryKeyConstraint('tag', 'rank'),
    )

#对作者进行搜索
class SearchByAuthor(Base):
    __tablename__ = 'SearchByAuthor'
    author = Column(String(32), nullable=False)
    rank = Column(Integer, nullable=False)
    book_id = Column(
        String(8),
        ForeignKey(
            'Book.id',
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        nullable=False
    )
    __table_args__ = (
        PrimaryKeyConstraint('author', 'rank'),
    )

#对书本内容进行搜索
class SearchByBookIntro(Base):
    __tablename__ = 'SearchByBookIntro'
    book_intro = Column(Text, nullable=False)
    rank = Column(Integer, nullable=False)
    book_id = Column(
        String(8),
        ForeignKey(
            'Book.id',
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        nullable=False
    )
    __table_args__ = (
        PrimaryKeyConstraint('book_intro', 'rank'),
    )

#函数实现搜索功能(将书本信息不需要的内容删去)
def insert_SearchByTitle():
    session = DBSession()
    result = session.query(
        Book1.id,
        Book1.title
    ).all()
    session.close()
    words_bookid={}
    for bk in result:
        book_id, title = bk
        title = re.sub(r'[]\(\[\{（【][^）)]*[\)\]\{\】\】]\s?', '', title)
        title = re.sub(r'[^\w\s]','', title)
        if title == "":
            continue
        words_list = jieba.cut_for_search(title)
        for word in words_list:
            if word in words_bookid:
                words_bookid[word].append(book_id)
            else:
                words_bookid[word] = [book_id]
    session = DBSession()
    for word, book_ids in words_bookid.items():
        rank = 0
        for book_id in book_ids:
            new_row = SearchByTitle(
                title = word,
                rank = rank,
                book_id = book_id
            )
            session.add(new_row)
            rank += 1
    session.commit()
    session.close()
    del result, words_bookid

# def search_author(self, author:str,page:int)-> (int,[dict]):
#     ret=[]
#     #已付款
#     records=self.session.execute(
#         " SELECT title,book.author,publisher,book_intro,tags,picture "
#         "FROM book WHERE book_id in "
#         "(select book_id from search_author where author='%s' and search_id BETWEEN %d and %d)" % (author,10*page-10,10*page-1)).fetchall()#约对"小说"约0.09s
#     if len(records)!=0:
#         for i in range(len(records)):
#             record = records[i]
#             title = record[0]
#             author_ = record[1]
#             publisher = record[2]
#             book_intro =record[3]
#             tags = record[4]
#             picture = record[5]#为达到搜索速度 得到未decode的byte 待前端时解析
#
#             try:
#                 from .hash import hashTool
#                 print('hashTool.HashTool.buffer_pil(picture)',hashTool.HashTool.get_pil(picture))
#                 ret.append(
#                     {'title': title, 'author': author_, 'publisher': publisher,
#                      'book_intro': book_intro,
#                      'tags': tags,'picture':hashTool.HashTool.get_pil(picture)})
#             except :
#                 ret.append(
#                     {'title': title, 'author': author_, 'publisher': publisher,
#                      'book_intro': book_intro,
#                      'tags': tags, 'picture': ''})
#
#         return 200,  ret
#     else:
#         return 200,  []
#
# def search_book_intro(self, book_intro:str,page:int)-> (int,[dict]):
#     ret = []
#     records = self.session.execute(
#         " SELECT title,author,publisher,book.book_intro,tags,picture "
#         "FROM book WHERE book_id in "
#         "(select book_id from search_book_intro where book_intro='%s' and search_id BETWEEN %d and %d)" % (
#         book_intro, 10*page-10,10*page-1)).fetchall()  # 约对"小说"约0.09s
#     if len(records) != 0:
#         for i in range(len(records)):
#             record = records[i]
#             title = record[0]
#             author = record[1]
#             publisher = record[2]
#             book_intro_ =record[3]
#             tags = record[4]
#             picture = record[5]  # 为达到搜索速度 得到未decode的byte 待前端时解析
#             try:
#                 from .hash import hashTool
#                 ret.append(
#                 {'title': title, 'author': author, 'publisher': publisher,
#
#                  'book_intro': book_intro_,
#                  'tags': tags, 'picture':hashTool.HashTool.get_pil(picture)})
#             except :
#                 ret.append(
#                     {'title': title, 'author': author, 'publisher': publisher,
#                      'book_intro': book_intro_,
#                      'tags': tags, 'picture': ''})
#         return 200,  ret
#     else:
#         return 200,  []
# def search_tags(self, tags:str,page:int)-> (int,[dict]):
#     ret = []
#     records = self.session.execute(
#         " SELECT title,author,publisher,book_intro,book.tags,picture "
#         "FROM book WHERE book_id in "
#         "(select book_id from search_tags where tags='%s' and search_id BETWEEN %d and %d)" % (
#         tags, 10*page-10,10*page-1)).fetchall()  # 约对"小说"约0.09s
#     if len(records) != 0:
#         for i in range(len(records)):
#             record = records[i]
#             title = record[0]
#             author = record[1]
#             publisher = record[2]
#             book_intro =record[3]
#             tags_ = record[4]
#             picture = record[5]  # 为达到搜索速度 得到未decode的byte 待前端时解析
#             try:
#                 from .hash import hashTool
#                 print('hashTool.HashTool.buffer_pil(picture)',hashTool.HashTool.get_pil(picture))
#                 ret.append(
#                     {'title': title, 'author': author, 'publisher': publisher,
#                      'book_intro': book_intro,
#                      'tags': tags_,'picture':hashTool.HashTool.get_pil(picture)})
#             except :
#                 ret.append(
#                     {'title': title, 'author': author, 'publisher': publisher,
#                      'book_intro': book_intro,
#                      'tags': tags_, 'picture': ''})
#         return 200,  ret
#     else:
#         return 200,  []
# def search_title(self, title:str,page:int)-> (int,[dict]):
#     ret = []
#     records = self.session.execute(
#         " SELECT book.title,author,publisher,book_intro,tags,picture "
#         "FROM book WHERE book_id in "
#         "(select book_id from search_title where title='%s' and search_id BETWEEN %d and %d)" % (
#         title, 10*page-10,10*page-1)).fetchall()  # 约对"小说"约0.09s
#     if len(records) != 0:
#         for i in range(len(records)):
#             record = records[i]
#             title_ = record[0]
#             author = record[1]
#             publisher = record[2]
#             book_intro =record[3]
#             tags = record[4]
#             picture = record[5]  # 为达到搜索速度 得到未decode的byte 待前端时解析
#             try:
#                 from .hash import hashTool
#                 print('hashTool.HashTool.buffer_pil(picture)',hashTool.HashTool.get_pil(picture))
#                 ret.append(
#                     {'title': title_, 'author': author, 'publisher': publisher,
#                      'book_intro': book_intro,
#                      'tags': tags,'picture':hashTool.HashTool.get_pil(picture)})
#             except :
#                 ret.append(
#                     {'title': title_, 'author': author, 'publisher': publisher,
#                      'book_intro': book_intro,
#                      'tags': tags, 'picture': ''})
#         return 200,  ret
#     else:
#         return 200,  []
# def search_author_in_store(self, author:str,store_id:str,page:int)-> (int,[dict]):
#     ret = []
#     records = self.session.execute(
#         " SELECT title,book.author,publisher,book_intro,tags,picture "
#         "FROM book WHERE book_id in "
#         "(select book_id from search_author where author='%s') and "
#         "book_id in (select book_id from store where store_id='%s')"
#         "LIMIT 10 OFFSET %d"% (author, store_id,10*page-10)).fetchall()  # 约对"小说"+"store_id=x"约0.09s storeid时间忽略不计
#     if len(records) != 0:
#         for i in range(len(records)):
#             record = records[i]
#             title = record[0]
#             author_ = record[1]
#             publisher = record[2]
#             book_intro = record[3]
#             tags = record[4]
#             picture = record[5]  # 为达到搜索速度 得到未decode的byte 待前端时解析
#             try:
#                 from .hash import hashTool
#                 print('hashTool.HashTool.buffer_pil(picture)', hashTool.HashTool.get_pil(picture))
#                 ret.append(
#                     {'title': title, 'author': author_, 'publisher': publisher,
#                      'book_intro': book_intro,
#                      'tags': tags, 'picture': hashTool.HashTool.get_pil(picture)})
#             except:
#                 ret.append(
#                     {'title': title, 'author': author_, 'publisher': publisher,
#                      'book_intro': book_intro,
#                      'tags': tags, 'picture': ''})#有byte类会倒是JSON unserializeable 所以需要base64.encode一下 可能会浪费时间
#         return 200,  ret
#     else:
#         return 200, []
# def search_book_intro_in_store(self, book_intro:str,store_id:str,page:int)-> (int,[dict]):
#     ret = []
#     records = self.session.execute(
#         " SELECT title,author,publisher,book.book_intro,tags,picture "
#         "FROM book WHERE book_id in "
#         "(select book_id from search_book_intro where book_intro='%s') and "
#         "book_id in (select book_id from store where store_id='%s')"
#         "LIMIT 10 OFFSET %d"% (book_intro, store_id,10*page-10)).fetchall()  # 约对"小说"+"store_id=x"约0.09s storeid时间忽略不计
#     if len(records) != 0:
#         for i in range(len(records)):
#             record = records[i]
#             title = record[0]
#             author = record[1]
#             publisher = record[2]
#             book_intro_ = record[3]
#             tags = record[4]
#             picture = record[5]  # 为达到搜索速度 得到未decode的byte 待前端时解析
#             try:
#                 from .hash import hashTool
#                 print('hashTool.HashTool.buffer_pil(picture)',hashTool.HashTool.get_pil(picture))
#                 ret.append(
#                     {'title': title, 'author': author, 'publisher': publisher,
#                      'book_intro': book_intro_,
#                      'tags': tags,'picture':hashTool.HashTool.get_pil(picture)})
#             except :
#                 ret.append(
#                     {'title': title, 'author': author, 'publisher': publisher,
#                      'book_intro': book_intro_,
#                      'tags': tags, 'picture': ''})
#         return 200,  ret
#     else:
#         return 200,  []
# def search_tags_in_store(self, tags:str,store_id:str,page:int)-> (int,[dict]):
#     ret = []
#     records = self.session.execute(
#         " SELECT title,author,publisher,book_intro,book.tags,picture "
#         "FROM book WHERE book_id in "
#         "(select book_id from search_tags where tags='%s') and "
#         "book_id in (select book_id from store where store_id='%s')"
#         "LIMIT 10 OFFSET %d"% (tags, store_id,10*page-10)).fetchall()  # 约对"小说"+"store_id=x"约0.09s storeid时间忽略不计
#     if len(records) != 0:
#         for i in range(len(records)):
#             record = records[i]
#             title = record[0]
#             author = record[1]
#             publisher = record[2]
#             book_intro = record[3]
#             tags_ = record[4]
#             picture = record[5]  # 为达到搜索速度 得到未decode的byte 待前端时解析
#             try:
#                 from .hash import hashTool
#                 print('hashTool.HashTool.buffer_pil(picture)',hashTool.HashTool.get_pil(picture))
#                 ret.append(
#                     {'title': title, 'author': author, 'publisher': publisher,
#                      'book_intro': book_intro,
#                      'tags': tags_,'picture':hashTool.HashTool.get_pil(picture)})
#             except :
#                 ret.append(
#                     {'title': title, 'author': author, 'publisher': publisher,
#                      'book_intro': book_intro,
#                      'tags': tags_, 'picture': ''})
#         return 200, ret
#     else:
#         return 200,  []
# def search_title_in_store(self, title:str,store_id:str,page:int)-> (int,[dict]):
#     ret = []
#     records = self.session.execute(
#         " SELECT book.title,author,publisher,book_intro,tags,picture "
#         "FROM book WHERE book_id in "
#         "(select book_id from search_title where title='%s') and "
#         "book_id in (select book_id from store where store_id='%s')"
#         "LIMIT 10 OFFSET %d"% (title, store_id,10*page-10)).fetchall()  # 约对"小说"+"store_id=x"约0.09s storeid时间忽略不计
#     if len(records) != 0:
#         for i in range(len(records)):
#             record = records[i]
#             title_ = record[0]
#             author = record[1]
#             publisher = record[2]
#             book_intro = record[3]
#             tags = record[4]
#             picture = record[5]  # 为达到搜索速度 得到未decode的byte 待前端时解析
#             try:
#                 from .hash import hashTool
#                 print('hashTool.HashTool.buffer_pil(picture)',hashTool.HashTool.get_pil(picture))
#                 ret.append(
#                     {'title': title_, 'author': author, 'publisher': publisher,
#                      'book_intro': book_intro,
#                      'tags': tags,'picture':hashTool.HashTool.get_pil(picture)})
#             except :
#                 ret.append(
#                     {'title': title_, 'author': author, 'publisher': publisher,
#                      'book_intro': book_intro,
#                      'tags': tags, 'picture': ''})
#         return 200,  ret
#     else:
#         return 200,  []
#
#
# def search_pic(self, picture,page=1)-> (int,[(int,int)]):#picture is FileStorage#[(book_id,相似度)]输出前十个
#     if isinstance(picture,str) or not picture:
#         code, mes = error.error_no_file_commit()
#         return code, mes
#     print(picture.content_type)
#     if picture and picture.content_type in ['png','image/png']:
#         from .hash import hashTool
#         picture=hashTool.HashTool.file_pil(picture)
#         photo_list=self.session.execute(
#             "SELECT book_id,picture "
#             "FROM book where book_id between 260 and 360"
#             "LIMIT 100").fetchall()
#         thelist=[]
#         for i in range(len(photo_list)):
#             record = photo_list[i]
#             book_id = record[0]
#             picture_ = record[1]#memoryview
#             print(type(picture_))
#             # try:
#             picture_=hashTool.HashTool.buffer_pil(picture_)#imagehash
#             print('after:',type(picture_))
#             thelist.append((picture_,book_id))
#             # except OSError:
#             #     print(OSError)
#         final=hashTool.HashTool.n_smallest(thelist, picture, 10)
#         print([i[1] for i in final])
#         print([1-hashTool.HashEngine.mean_distance([i],picture)/64 for i in final])
#         return 200,[(i[1],1-hashTool.HashEngine.mean_distance([i],picture)/64) for i in final] #[(book_id,相似度)]
#     else:
#         code, mes = error.error_bad_type()
#         return code, mes

#实现作者名字搜索函数
def insert_SearchByAuthor():
    session = DBSession()
    result = session.query(
        Book1.id,
        Book1.author
    ).all()
    session.close()

    words_bookid = {}
    for bk in result:
        book_id, author = bk
        if author is None or author == 'None':
            continue
        res = re.findall(r'[(\[（](.*?[)\]）])', author)
        if len(res) != 0:
            if res[0] in words_bookid:
                words_bookid[res[0]].append(book_id)
            else:
                words_bookid[res[0]] = [book_id]
    session = DBSession()
    for word,book_ids in words_bookid.items():
        rank = 0
        for book_id in book_ids:
            new_row = SearchByAuthor(
                author = word,
                rank = rank,
                book_id = book_id
            )
            session.add(new_row)
            rank += 1
    session.commit()
    session.close()
    del result, words_bookid


#实现标志搜索函数
def insert_SearchByTags():
    session = DBSession()
    result = session.query(
        Book1.id,
        Book1.tags
    ).all()
    session.close()
    words_bookid = {}
    for bk in result:
        book_id, tags = bk
        tag_list = tags.strip().split('\n')
        for tag in tag_list:
            tag = tag.strip()
            if tag in words_bookid:
                words_bookid[tag].append(book_id)
            else:
                words_bookid[tag] = [book_id]
    session = DBSession()
    for word, book_ids in words_bookid.items():
        rank = 0
        for book_id in book_ids:
            new_row = SearchByTag(
                tag = word,
                rank = rank,
                book_id = book_id
            )
            session.add(new_row)
            rank += 1
    session.commit()
    session.close()
    del result, words_bookid

#书本内容搜索
def insert_SearchByBookIntro():
    session = DBSession()
    result = session.query(
        Book1.id,
        Book1.book_intro
    ).all()
    session.close()

    words_bookid = {}
    tr = jieba.analyse.TextRank()
    for bk in result:
        book_id, book_intro = bk
        key_words = tr.textrank(book_intro, topK=3)
        for word in key_words:
            if word in words_bookid:
                words_bookid[word].append(book_id)
            else:
                words_bookid[word] = [book_id]
    session = DBSession()
    for word, book_ids in words_bookid.items():
        rank = 0
        for book_id in book_ids:
            new_row = SearchByBookIntro(
                book_intro = word,
                rank = rank,
                book_id = book_id
            )
            session.add(new_row)
            rank += 1
    session.commit()
    session.close()
    del result, words_bookid

#运行
    if __name__ == '__main__':
        Base.metadata.create_all(engine)
        insert_SearchByTags()
        insert_SearchByAuthor()
        insert_SearchByTitle()
        insert_SearchByBookIntro()