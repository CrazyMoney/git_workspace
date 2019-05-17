#!/usr/bin/env python
# -*- coding: utf-8 -*-

import openpyxl
import pandas as pd
import tushare as ts
import numpy as np
import xlrd
import time
import sqlalchemy
from sqlalchemy import create_engine
import pymysql
import threading
import sklearn




ts.set_token("b32c8489a54a0ad664a035b5fb974c4f25bf5e2a2adfb5c68353017b")
pro = ts.pro_api()
# Today = ts.get_day_all()   #获取当天股票数据
# 遍历所有股票
# AllStock = pro.query("stock_basic",exchange="",list_status ="L",fields="ts_code,symbol,name,area,industry,list_date")
# AllStock.to_csv('AllStock.csv')
p = pd.read_csv("AllStock.csv")
s = p["symbol"]
# print(type(s))
engine = create_engine('mysql+pymysql://root:zhou1234@localhost:3306/stock?charset=utf8', pool_size=150, echo=False)
ls1 = []  # 这是所有股票的列表  数值型的
for i in s:
    ls1.append(i)
# 查看数据类型
round_1 = []
change = []



def get_date_fromsql():
    for j in ls1:
        j = str(j)
        j = j.zfill(6)
        hist_day = pd.read_sql(j, engine)
        return  hist_day

def get_DaPan_fromsql():
        hist_DaPan = pd.read_sql("sh", engine)
        return hist_DaPan

hist_day =get_date_fromsql()
hist_DaPan =get_DaPan_fromsql()


