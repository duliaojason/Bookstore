import jwt
import time
import logging
import sqlite3 as sqlite
from be.model import error
from be.model.db import DB, Book

class mySearch(DB):
    def __init__(self):
        DB.__init__(self)

    def search(self, args: dict):
        # 用字典传参，也可以传入json格式的，然后在这个函数内部把json转成字典
        # 对于数字的参数，比如页数这些，最好套一个int()，因为可能转出来还是字符串
        pass