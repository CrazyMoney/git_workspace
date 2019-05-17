import future
import time
import pandas as pd
import tushare as ts
import numpy as np
import sqlalchemy
from sqlalchemy import create_engine
import pymysql
import talib

furture2 = future.fur()
furture2.api_engin_init()


def get_cpi():
    #获取cpi并保存到文档
    pf = ts.get_cpi()
    pf = pd.DataFrame(pf)
    pf.to_excel("cpi.xls")



cpi = pd.read_excel("cpi.xls")
print(type(cpi))
s = cpi["cpi"]
s= np.array(s)
x = talib.func.APO(s)
print(x)