import jwt
import time
import logging
import sqlite3 as sqlite
from be.model import error
from be.model.db import DataBase, User1

# encode a json string like:
#   {
#       "user_id": [user name],
#       "terminal": [terminal code],
#       "timestamp": [ts]} to a JWT
#   }


def jwt_encode(user_id: str, terminal: str) -> str:
    encoded = jwt.encode(
        {"user_id": user_id, "terminal": terminal, "timestamp": time.time()},
        key=user_id,
        algorithm="HS256",
    )
    return encoded.encode("utf-8").decode("utf-8")


# decode a JWT to a json string like:
#   {
#       "user_id": [user name],
#       "terminal": [terminal code],
#       "timestamp": [ts]} to a JWT
#   }
def jwt_decode(encoded_token, user_id: str) -> str:
    decoded = jwt.decode(encoded_token, key=user_id, algorithms="HS256")
    return decoded


# class User(db_conn.DBConn):
#     token_lifetime: int = 3600  # 3600 second
#
#     def __init__(self):
#         db_conn.DBConn.__init__(self)
#
#     def __check_token(self, user_id, db_token, token) -> bool:
#         try:
#             if db_token != token:
#                 return False
#             jwt_text = jwt_decode(encoded_token=token, user_id=user_id)
#             ts = jwt_text["timestamp"]
#             if ts is not None:
#                 now = time.time()
#                 if self.token_lifetime > now - ts >= 0:
#                     return True
#         except jwt.exceptions.InvalidSignatureError as e:
#             logging.error(str(e))
#             return False
#
#     def register(self, user_id: str, password: str):
#         try:
#             terminal = "terminal_{}".format(str(time.time()))
#             token = jwt_encode(user_id, terminal)
#             self.conn.execute(
#                 "INSERT into user(user_id, password, balance, token, terminal) "
#                 "VALUES (?, ?, ?, ?, ?);",
#                 (user_id, password, 0, token, terminal), )
#             self.conn.commit()
#         except sqlite.Error:
#             return error.error_exist_user_id(user_id)
#         return 200, "ok"
#
#     def check_token(self, user_id: str, token: str) -> (int, str):
#         cursor = self.conn.execute("SELECT token from user where user_id=?", (user_id,))
#         row = cursor.fetchone()
#         if row is None:
#             return error.error_authorization_fail()
#         db_token = row[0]
#         if not self.__check_token(user_id, db_token, token):
#             return error.error_authorization_fail()
#         return 200, "ok"
#
#     def check_password(self, user_id: str, password: str) -> (int, str):
#         cursor = self.conn.execute("SELECT password from user where user_id=?", (user_id,))
#         row = cursor.fetchone()
#         if row is None:
#             return error.error_authorization_fail()
#
#         if password != row[0]:
#             return error.error_authorization_fail()
#
#         return 200, "ok"
#
#     def login(self, user_id: str, password: str, terminal: str) -> (int, str, str):
#         token = ""
#         try:
#             code, message = self.check_password(user_id, password)
#             if code != 200:
#                 return code, message, ""
#
#             token = jwt_encode(user_id, terminal)
#             cursor = self.conn.execute(
#                 "UPDATE user set token= ? , terminal = ? where user_id = ?",
#                 (token, terminal, user_id), )
#             if cursor.rowcount == 0:
#                 return error.error_authorization_fail() + ("", )
#             self.conn.commit()
#         except sqlite.Error as e:
#             return 528, "{}".format(str(e)), ""
#         except BaseException as e:
#             return 530, "{}".format(str(e)), ""
#         return 200, "ok", token
#
#     def logout(self, user_id: str, token: str) -> bool:
#         try:
#             code, message = self.check_token(user_id, token)
#             if code != 200:
#                 return code, message
#
#             terminal = "terminal_{}".format(str(time.time()))
#             dummy_token = jwt_encode(user_id, terminal)
#
#             cursor = self.conn.execute(
#                 "UPDATE user SET token = ?, terminal = ? WHERE user_id=?",
#                 (dummy_token, terminal, user_id), )
#             if cursor.rowcount == 0:
#                 return error.error_authorization_fail()
#
#             self.conn.commit()
#         except sqlite.Error as e:
#             return 528, "{}".format(str(e))
#         except BaseException as e:
#             return 530, "{}".format(str(e))
#         return 200, "ok"
#
#     def unregister(self, user_id: str, password: str) -> (int, str):
#         try:
#             code, message = self.check_password(user_id, password)
#             if code != 200:
#                 return code, message
#
#             cursor = self.conn.execute("DELETE from user where user_id=?", (user_id,))
#             if cursor.rowcount == 1:
#                 self.conn.commit()
#             else:
#                 return error.error_authorization_fail()
#         except sqlite.Error as e:
#             return 528, "{}".format(str(e))
#         except BaseException as e:
#             return 530, "{}".format(str(e))
#         return 200, "ok"
#
#     def change_password(self, user_id: str, old_password: str, new_password: str) -> bool:
#         try:
#             code, message = self.check_password(user_id, old_password)
#             if code != 200:
#                 return code, message
#
#             terminal = "terminal_{}".format(str(time.time()))
#             token = jwt_encode(user_id, terminal)
#             cursor = self.conn.execute(
#                 "UPDATE user set password = ?, token= ? , terminal = ? where user_id = ?",
#                 (new_password, token, terminal, user_id), )
#             if cursor.rowcount == 0:
#                 return error.error_authorization_fail()
#
#             self.conn.commit()
#         except sqlite.Error as e:
#             return 528, "{}".format(str(e))
#         except BaseException as e:
#             return 530, "{}".format(str(e))
#         return 200, "ok"

class myUser(DataBase):

    def __init__(self):
        DataBase.__init__(self)
        self.token_lifetime: int = 3600

    def __check_token(self, user_id, db_token, token) -> bool:
        try:
            if db_token != token:
                return False
            jwt_text = jwt_decode(encoded_token=token, user_id=user_id)
            ts = jwt_text["timestamp"]
            if ts is not None:
                now = time.time()
                if self.token_lifetime > now - ts >= 0:
                    return True
        except jwt.exceptions.InvalidSignatureError as e:
            logging.error(str(e))
            return False

#用户注册
    def register(self, user_id: str, password: str):
        try:
            terminal = "terminal_{}".format(str(time.time()))
            token = jwt_encode(user_id, terminal)

            newUser = User1(
                user_id=user_id,
                password=password,
                balance=0,
                token=token,
                terminal=terminal,
            )

            session = self.DbSession()
            session.add(newUser)
            session.commit()
            session.close()

        except:
            return error.error_exist_user_id(user_id)
        return 200, "ok"

#用户查看权限
    def check_token(self, user_id: str, token: str) -> tuple((int, str)):
        session = self.DbSession()
        result = session.query(
            User1.token
        ).filter(
            User1.user_id == user_id
        ).first()
        session.close()

        if result is None:
            return error.error_authorization_fail()
        db_token = result[0]
        if not self.__check_token(user_id, db_token, token):
            return error.error_authorization_fail()
        return 200, "ok"

#用户检查密码
    def check_password(self, user_id: str, password: str) -> tuple((int, str)):
        session = self.DbSession()
        result = session.query(
            User1.password
        ).filter(
            User1.user_id == user_id
        ).first()
        session.close()
        if result is None:
            return error.error_authorization_fail()
        if password != result[0]:
            return error.error_authorization_fail()

        return 200, "ok"

#用户登录
    def login(self, user_id: str, password: str, terminal: str) -> tuple((int, str, str)):
        token = ""
        try:
            code, message = self.check_password(user_id, password)
            if code != 200:
                return code, message, ""

            token = jwt_encode(user_id, terminal)
            session = self.DbSession()
            user = session.query(
                User1
            ).filter(
                User1.user_id == user_id
            ).first()
            if user is None:
                session.close()
                return error.error_authorization_fail()

            user.token = token
            session.add(user)
            session.commit()
            session.close()

        except sqlite.Error as e:
            return 528, "{}".format(str(e)), ""
        except BaseException as e:
            return 530, "{}".format(str(e)), ""
        return 200, "ok", token

#用户登出
    def logout(self, user_id: str, token: str) -> bool:
        try:
            code, message = self.check_token(user_id, token)
            if code != 200:
                return code, message

            terminal = "terminal_{}".format(str(time.time()))
            dummy_token = jwt_encode(user_id, terminal)

            session = self.DbSession()
            user = session.query(
                User1
            ).filter(
                User1.user_id == user_id
            ).first()
            if user is None:
                session.close()
                return error.error_authorization_fail()

            user.terminal = terminal
            user.token = dummy_token
            session.add(user)
            session.commit()
            session.close()

        except sqlite.Error as e:
            return 528, "{}".format(str(e))
        except BaseException as e:
            return 530, "{}".format(str(e))
        return 200, "ok"

    # 用户修改密码
    def change_password(self, user_id: str, old_password: str, new_password: str) -> bool:
        try:
            code, message = self.check_password(user_id, old_password)
            if code != 200:
                return code, message

            terminal = "terminal_{}".format(str(time.time()))
            token = jwt_encode(user_id, terminal)

            session = self.DbSession()
            user = session.query(User1).filter(User1.user_id == user_id).first()
            if user is None:
                session.close()
                return error.error_authorization_fail()

            user.password = new_password
            user.terminal = terminal
            user.token = token
            session.add(user)
            session.commit()
            session.close()

        except sqlite.Error as e:
            return 528, "{}".format(str(e))
        except BaseException as e:
            return 530, "{}".format(str(e))
        return 200, "ok"

    #用户非注册状态
    def unregister(self, user_id: str, password: str) -> tuple((int, str)):
        try:
            code, message = self.check_password(user_id, password)
            if code != 200:
                return code, message

            session = self.DbSession()
            session.query(User1).filter(User1.user_id == user_id).delete()
            session.commit()
            session.close()

        except sqlite.Error as e:
            return 528, "{}".format(str(e))
        except BaseException as e:
            return 530, "{}".format(str(e))
        return 200, "ok"


