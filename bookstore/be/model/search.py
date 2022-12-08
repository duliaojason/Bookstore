import jwt
import time
import logging
import sqlite3 as sqlite
from be.model import error
from be.model.db import DataBase, Book1

#这个函数需要实现的是将json格式直接转化成字典格式，一定要注意参数的存在形式
class mySearch(DataBase):
    def __init__(self):
        DataBase.__init__(self)

    def search(self, args: dict):
        pass