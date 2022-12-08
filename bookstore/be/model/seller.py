import sqlite3 as sqlite
from be.model import error
from be.model.db import DataBase
from be.model.db import StoreBook1, Store1, StoreUser1, Order1


# class Seller(db_conn.DBConn):
#
#     def __init__(self):
#         db_conn.DBConn.__init__(self)
#
#     def add_book(self, user_id: str, store_id: str, book_id: str, book_json_str: str, stock_level: int):
#         try:
#             if not self.user_id_exist(user_id):
#                 return error.error_non_exist_user_id(user_id)
#             if not self.store_id_exist(store_id):
#                 return error.error_non_exist_store_id(store_id)
#             if self.book_id_exist(store_id, book_id):
#                 return error.error_exist_book_id(book_id)
#
#             self.conn.execute("INSERT into store(store_id, book_id, book_info, stock_level)"
#                               "VALUES (?, ?, ?, ?)", (store_id, book_id, book_json_str, stock_level))
#             self.conn.commit()
#         except sqlite.Error as e:
#             return 528, "{}".format(str(e))
#         except BaseException as e:
#             return 530, "{}".format(str(e))
#         return 200, "ok"
#
#     def add_stock_level(self, user_id: str, store_id: str, book_id: str, add_stock_level: int):
#         try:
#             if not self.user_id_exist(user_id):
#                 return error.error_non_exist_user_id(user_id)
#             if not self.store_id_exist(store_id):
#                 return error.error_non_exist_store_id(store_id)
#             if not self.book_id_exist(store_id, book_id):
#                 return error.error_non_exist_book_id(book_id)
#
#             self.conn.execute("UPDATE store SET stock_level = stock_level + ? "
#                               "WHERE store_id = ? AND book_id = ?", (add_stock_level, store_id, book_id))
#             self.conn.commit()
#         except sqlite.Error as e:
#             return 528, "{}".format(str(e))
#         except BaseException as e:
#             return 530, "{}".format(str(e))
#         return 200, "ok"
#
#     def create_store(self, user_id: str, store_id: str) -> (int, str):
#         try:
#             if not self.user_id_exist(user_id):
#                 return error.error_non_exist_user_id(user_id)
#             if self.store_id_exist(store_id):
#                 return error.error_exist_store_id(store_id)
#             self.conn.execute("INSERT into user_store(store_id, user_id)"
#                               "VALUES (?, ?)", (store_id, user_id))
#             self.conn.commit()
#         except sqlite.Error as e:
#             return 528, "{}".format(str(e))
#         except BaseException as e:
#             return 530, "{}".format(str(e))
#         return 200, "ok"

#定义一个卖家，方便随时调试测试
class mySeller(DataBase):

    def __init__(self):
        DataBase.__init__(self)

#添加书本
    def add_book(self, user_id: str, store_id: str, book_id: str, book_json_str: str, stock_level: int):
        try:
            if not self.user_id_exist(user_id):
                return error.error_non_exist_user_id(user_id)
            if not self.store_id_exist(store_id):
                return error.error_non_exist_store_id(store_id)
            if self.book_id_exist(store_id, book_id):
                return error.error_exist_book_id(book_id)

            storebook = StoreBook1(
                stock_level=stock_level,
                book_info=book_json_str,
                fk_store_id=store_id,
                fk_book_id=book_id
            )
            session = self.DbSession()
            session.add(storebook)
            session.commit()
            session.close()

        except sqlite.Error as e:
            return 528, "{}".format(str(e))
        except BaseException as e:
            return 530, "{}".format(str(e))
        return 200, "ok"

#添加级别，设置主键
    def add_stock_level(self, user_id: str, store_id: str, book_id: str, add_stock_level: int):
        try:
            if not self.user_id_exist(user_id):
                return error.error_non_exist_user_id(user_id)
            if not self.store_id_exist(store_id):
                return error.error_non_exist_store_id(store_id)
            if not self.book_id_exist(store_id, book_id):
                return error.error_non_exist_book_id(book_id)

            session = self.DbSession()
            result = session.query(
                StoreBook1
            ).filter(
                StoreBook1.fk_store_id == store_id, StoreBook1.fk_book_id == book_id
            ).first()

            if result:
                result.stock_level += add_stock_level
                session.add(result)
                session.commit()
            session.close()

        except sqlite.Error as e:
            return 528, "{}".format(str(e))
        except BaseException as e:
            return 530, "{}".format(str(e))
        return 200, "ok"

#创建商店
    def create_store(self, user_id: str, store_id: str) -> tuple((int, str)):
        try:
            if not self.user_id_exist(user_id):
                return error.error_non_exist_user_id(user_id)
            if self.store_id_exist(store_id):
                return error.error_exist_store_id(store_id)

            session = self.DbSession()
            newStore = Store1(store_id=store_id)
            newStoreUser = StoreUser1(fk_store_id=store_id, fk_user_id=user_id)
            session.add(newStore)
            session.add(newStoreUser)
            session.commit()
            session.close()

        except sqlite.Error as e:
            return 528, "{}".format(str(e))
        except BaseException as e:
            return 530, "{}".format(str(e))
        return 200, "ok"

#成功寄件
    def deliver_goods(self, order_id, store_id) -> tuple((int, str)):
        try:
            if not self.store_id_exist(store_id):
                return error.error_non_exist_store_id(store_id)

            session = self.DbSession()
            order = session.query(
                Order1
            ).filter(
                Order1.order_id == order_id,
                Order1.fk_store_id == store_id
            ).first()
            if order is None:
                session.close()
                return error.error_change_other_store_order(store_id, order_id)
            if order.status != 1:
                session.close()
                return error.error_order_status_not_fit(order_id)

            order.status = 2
            session.add(order)
            session.commit()
            session.close()

        except sqlite.Error as e:
            return 528, "{}".format(str(e))
        except BaseException as e:
            return 530, "{}".format(str(e))
        return 200, "ok"
