import datetime
import future
import time
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


def today():
    # 截取当日日期 格式为字符串: 20190115
    today = time.localtime()
    year = str(today.tm_year)
    mouth = str(today.tm_mon)
    mouth = mouth.zfill(2)
    date = str(today.tm_mday)
    date = date.zfill(2)
    today_date = year + mouth + date
    return today_date


def date_get(i):
    # 获取过去i 天的的日期  日期格式:str 20190516
    # return 列表
    date_list = []
    for j in range(-i, 1):
        date = datetime.date.today() + datetime.timedelta(days=j)
        year = str(date.year)
        mouth = str(date.month)
        mouth = mouth.zfill(2)
        day = str(date.day)
        day = day.zfill(2)
        date_ge = year + mouth + day
        date_list.append(date_ge)
    return date_list


s = date_get(360)
#获取过去360天的日期

furture2 = future.fur()
furture2.api_engin_init()
cctv_news = pd.DataFrame()
for x in range(360):
    df = furture2.pro.cctv_news(date=s[x])
    df =pd.DataFrame(df)
    cctv_news.append(df)
    time.sleep(0.3)
cctv_news.to_excel("cctv_news.csv")


