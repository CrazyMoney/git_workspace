import openpyxl
import matplotlib
import pandas as pd
from pandas import *
from numpy import *
import tushare as ts
import numpy as np
import matplotlib.pyplot as plt
import math
import xlrd
import time
ts.set_token("8d29f89b7cc516c302a9d0e50bf6a3cce8d0ef886d93d30be66b1374")
pro = ts.pro_api()


def get_all_further():
    #获取交易所所有交易品种并保存到excel中
    Allfuther = pro.fut_basic(exchange='CZCE', fut_type='1', fields='ts_code,symbol,name,list_date,delist_date')
    print(Allfuther)
    print(type(Allfuther))
    Allfuther.to_csv("Allfurther")


get_all_further()