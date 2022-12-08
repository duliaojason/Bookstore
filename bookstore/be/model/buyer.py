import sqlite3 as sqlite
import uuid
import json
import logging
from be.model import error
#自己添加的包
import datetime
from be.model.db import DataBase
from be.model.db import User1, Book1, StoreBook1, StoreUser1, Order1, OrderBook1

class Buyer(DataBase):
    def __init__(self):
        DataBase.__init__(self)

    def new_order(self, user_id: str, store_id: str, id_and_count: list[(str, int)]) -> tuple((int, str, str)):
        order_id = ""
        try:
            if not self.user_id_exist(user_id):
                return error.error_non_exist_user_id(user_id) + (order_id, )
            if not self.store_id_exist(store_id):
                return error.error_non_exist_store_id(store_id) + (order_id, )
            order_id = "{}_{}_{}".format(user_id, store_id, str(uuid.uuid1()))

            new_order = Order1(
                order_id=order_id,
                time=datetime.datetime.now(),
                total_price=0,
                status=0,
                fk_buyer_id=user_id,
                fk_store_id=store_id,
            )
            details = []
            session = self.DbSession()
            for book_id, count in id_and_count:
                result = session.query(
                    Book1.price,
                    StoreBook1
                ).join(
                    StoreBook1,
                    Book1.id == StoreBook1.fk_book_id
                ).filter(
                    Book1.id == book_id,
                    StoreBook1.fk_store_id == store_id
                ).first()
                if result is None:
                    session.close()
                    return error.error_none_exist_book_id(book_id)+(order_id,)
                stock_level = result[1].stock_level
                price = result[0]

                if stock_level < count:
                    session.close()
                    return error.error_stock_level_low(book_id) + (order_id,)

                result[1].stock_level -= count
                session.add(result[1])
                new_order.total_price += price * count
                details.append((count, price, book_id))

            session.add(new_order)

            for d in details:
                o_b = OrderBook1(
                    num=d[0],
                    price=d[1],
                    fk_book_id=d[2],
                    fk_order_id=order_id
                )
                session.add(o_b)

            session.commit()
            session.close()
            del details
        except sqlite.Error as e:
            logging.info("528, {}".format(str(e)))
            return 528, "{}".format(str(e)), ""
        except BaseException as e:
            logging.info("530, {}".format(str(e)))
            return 530, "{}".format(str(e)), ""
        return 200, "ok", order_id

    #支付
    def payment(self, user_id: str, password: str, order_id: str) -> tuple((int, str)):
        try:
            session = self.DbSession()
            order = session.query(
                Order1
            ).filter(
                Order1.order_id == order_id
            ).first()

            if order is None:
                session.close()
                return error.error_invalid_order_id(order_id)

            buyer_id = order.fk_buyer_id
            store_id = order.fk_store_id
            total_price = order.total_price

            if buyer_id != user_id:
                session.close()
                return error.error_authorization_fail()

            buyer = session.query(
                User1
            ).filter(
                User1.user_id == buyer_id
            ).first()
            if buyer is None:
                session.close()
                return error.error_non_exist_user_id(buyer_id)

            balance = buyer.balance
            if password != buyer.password:
                session.close()
                return error.error_authorization_fail()

            seller_id = session.query(
                StoreUser1.fk_user_id
            ).filter(
                StoreUser1.fk_store_id == store_id
            ).first()
            seller_id = seller_id[0]

            if seller_id is None:
                session.close()
                return error.error_non_exist_store_id(store_id)
            if balance < total_price:
                session.close()
                return error.error_not_sufficient_funds(order_id)

            seller = session.query(
                User1
            ).filter(
                User1.user_id == seller_id
            ).first()

            cur_time = datetime.datetime.now()
            cur_time = datetime.date(cur_time.year, cur_time.month, cur_time.day)
            if (cur_time - order.time).days >= 1:
                order.status = -1
                session.add(order)
                session.commit()
                session.close()
                return error.error_order_timed_out(order_id)

            buyer.balance -= total_price
            seller.balance += total_price
            order.status = 1
            session.add(buyer)
            session.add(seller)
            session.add(order)
            session.commit()
            session.close()

        except sqlite.Error as e:
            return 528, "{}".format(str(e))
        except BaseException as e:
            return 530, "{}".format(str(e))
        return 200, "ok"

    #用户添加存款
    def add_funds(self, user_id, password, add_value) -> tuple((int, str)):
        try:
            session = self.DbSession()
            user = session.query(
                User1
            ).filter(
                User1.user_id == user_id
            ).first()

            if user is None:
                session.close()
                return error.error_authorization_fail()
            if user.password != password:
                session.close()
                return error.error_authorization_fail()

            user.balance += add_value
            session.add(user)
            session.commit()
            session.close()

        except sqlite.Error as e:
            return 528, "{}".format(str(e))
        except BaseException as e:
            return 530, "{}".format(str(e))
        return 200, "ok"

