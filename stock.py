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


def today():
    # 截取当日日期 格式为字符串: 20190115
    today = time.localtime()
    year = str(today.tm_year)
    mouth = str(today.tm_mon)
    mouth = mouth.zfill(2)
    date = str(today.tm_mday)
    date = date.zfill(2)
    today_date = str(year) +"-"+ str(mouth)  +"-"+str(date)
    return today_date



today_date = today()
print(type(today_date))
'''
对数据进行选取
def round(stock):
    rd2 = pd.read_sql(stock, engine)
    if rd2.ix[1]['close'] > rd2.ix[5]['close'] and rd2.ix[5]['close'] > rd2.ix[10]['close']:  #
        if  0 <rd2.ix[1]['close'] < 3 and 0 < rd2.ix[2]['close'] < 3 and 0 < rd2.ix[3]['close'] < 3 and 0 < rd2.ix[4][
            'close'] < 3 :

            print("++++++++++")
            change.append(rd2.ix[0]['p_change'])
            round_1.append(j)
    else:
        pass
    print(threading.current_thread().name)

for j in ls1:
    j = str(j)
    j = j.zfill(6)
    try:
        threading.Thread(target=round, args=(j,)).start()
        time.sleep(0.3)
    except:
        pass

print(len(round_1))
data_1 = pd.Series(data=change, index=round_1)
data_1.to_excel("Demo_1.xls")
'''


def get_hist_day_tosql():
    # # 获取所有股票的 日线行并分别保存到中stock数据库中的同名的表里,表名为: "000036"
    for j in ls1:
        j = str(j)
        j = j.zfill(6)
        df =ts.get_hist_data(j,start=today_date,end=today_date)
        df = pd.DataFrame(df)
        print(df)
        try:
            df.to_sql(j, con=engine,if_exists="append")
            # 将数据写入数据库如果存在则添加
            time.sleep(0.5)
            print("%s okokok" % j)

        except Exception as  e:
            df.to_sql(j,engine,if_exists='append')
            time.sleep(0.5)
            print(e)

def get_dapan_date():
    df = ts.get_hist_data("sh")
    df = pd.DataFrame(df)
    print(df)
    try:
        df.to_sql("sh", con=engine, if_exists="append")
        # 将数据写入数据库如果存在则添加
        print("%s okokok" % j)

    except Exception as  e:
        df.to_sql("sh", engine, if_exists='append')
        print(e)



def look_for(j):
    try:

        # print(threading.current_thread().name)
        # print(j)
        hist_day = pd.read_sql(j, engine)
        # print(hist_day.sort_values(["open"]).head(50))
        # print(hist_day.query("open> 16"))   000693
        o = 0
        n = 0
        for i in range(10):
            if  hist_day.ix[i]["p_change"] > 0:
                o += 1
                while o > 7:
                    if (hist_day.ix[0]["volume"]- hist_day.ix[0]["v_ma5"])/hist_day.ix[0]["v_ma5"] >1.5:
                        print("符合条件1:",j)
                        continue
                    else:
                        pass

            else :
                n +=1
                while n >7:
                    if (hist_day.ix[0]["volume"]- hist_day.ix[0]["v_ma5"])/hist_day.ix[0]["v_ma5"] >1.5:
                        print("符合条件2:",j)
                        continue
                    else:
                        pass

    except Exception as e:
        print("错误:*******",j)

def getdate_from_sql():
    """  时间间隔 ,下跌趋势时间长度 和上涨时间长度"""
    for j in ls1:
        if j < 2623:
            j = str(j)
            j = j.zfill(6)
            time.sleep(0.5)

            look_for_threading  = threading .Thread(target= look_for,args=(j,))
            look_for_threading.start()
        else:
            break




#  每个交易日跑一次即可
get_hist_day_tosql()
#  每个交易日跑一次即可
get_dapan_date()
# getdate_from_sql()












''''    

取三天股票行情
print("开始遍历")
list2 =[]
de = DataFrame()
for j in ls1:
    df = pro.query('daily', ts_code=j, start_date='20190329', end_date='20190402')
    de = de.append(df)
    time.sleep(1)
    print(de)
de.to_csv("round1.csv")


'''
'''

第一次选取
try:
    for j in range(10706):
        if rd2.ix[j]['pct_chg'] > 3 and 3 > rd2.ix[j + 1]['pct_chg'] > 0 and 3 > rd2.ix[j + 2]['pct_chg'] > 0:
            # if rd2.ix[j]['amount'] > rd2.ix[j + 1]['amount'] > rd2.ix[j + 2]['amount']:
                if rd2.ix[j]['amount'] > 2.5 * (rd2.ix[j + 1]['amount'] + rd2.ix[j + 2]['amount']):
                    if rd2.ix[j]['close'] > (rd2.ix[j]['close']+rd2.ix[j+1]['close']+rd2.ix[j+2]['close'])/3:
                        list2.append(rd2.ix[j]['ts_code'])
                        j += 3
        else:
            continue
except:
    pass

print(list2)
print(len(list2))
'''
