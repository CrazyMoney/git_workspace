import time

from talib import func
import xlrd
import pandas as pd
import numpy as np
import sqlalchemy
from sqlalchemy import create_engine
import tushare as ts

ts.set_token("e46eb78808b424f271f9f4d6f65c0c731750e86829ae4b3967325e47")
pro = ts.pro_api()

ls1 = []
p = pd.read_csv("AllStock.csv")
s = p["ts_code"]
for i in s:
    ls1.append(i)  # 这是所有股票的列表  数值型的


# 查看数据类型

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


today_date = today()

up_begin = 0
up_end = 0
down_bedin = 0
down_end = 0
no_trend = 0
for j in ls1:
    try:
        df = pro.daily(ts_code=j, start_date='20190101', end_date=today_date)
        df = pd.DataFrame(df)
        time.sleep(0.3)

        close = np.array(df.ix[::1]["close"])
        high = np.array(df.ix[::1]["high"])
        low = np.array(df.ix[::1]["low"])
        close_boll = np.array(df.ix[::-1]["close"])

        atr = func.ATR(high, low, close, timeperiod=14)

        a = atr[-1]
        ht_trade_period = func.HT_TRENDMODE(close)
        close_lastday = df.ix[0]["close"]

        bbands = func.BBANDS(close_boll, timeperiod=5)

        b_bottom = bbands[0][-1]
        b_mid = bbands[1][-1]
        b_uppter = bbands[2][-1]
        list_up_gegin = []
        list_down_end =[]


        if bbands[0][-1] > bbands[0][-2] > bbands[0][-3] and close_lastday < b_mid:
            result = "上涨初期:上涨趋势 在中轨以下\n品种:%s  日期：%s  \n 收盘价：%.2f \n 真实波动率：%.2f \n 布林线上轨 %.2f  \n 布林线中轨 %.2f  \n 布林线下轨 %.2f \n" % (
                j, today_date, close_lastday, a, b_uppter, b_mid, b_bottom)
            up_begin += 1
            print("上涨初期:上涨趋势 在中轨以下\n", result)
            with open("stock_5月4号.csv", "a", encoding="gbk") as f:
                f.write(result)
        elif bbands[0][-1] > bbands[0][-2] > bbands[0][-3] and close_lastday > b_uppter:
            result = "上涨回调压低大:上涨趋势 在下轨以下\n品种:%s  日期：%s  \n 收盘价：%.2f \n 真实波动率：%.2f \n 布林线上轨 %.2f  \n 布林线中轨 %.2f  \n 布林线下轨 %.2f \n" % (
                j, today_date, close_lastday, a, b_uppter, b_mid, b_bottom)
            up_end += 1
            print("上涨回调压低大:上涨趋势 在下轨以下\n", result)
            with open("stock_5月4号.csv", "a", encoding="gbk") as f:
                f.write(result)
        elif bbands[0][-1] < bbands[0][-2] < bbands[0][-3] and close_lastday > b_mid:
            result = "下跌初期:下跌趋势 在中轨以下\n品种:%s  日期：%s  \n 收盘价：%.2f \n 真实波动率：%.2f \n 布林线上轨 %.2f  \n 布林线中轨 %.2f  \n 布林线下轨 %.2f \n" % (
                j, today_date, close_lastday, a, b_uppter, b_mid, b_bottom)
            down_bedin += 1
            print("下跌初期:下跌趋势 在中轨以下\n", result, )
            with open("stock_5月4号.csv", "a", encoding="gbk") as f:
                f.write(result)

        elif bbands[0][-1] < bbands[0][-2] < bbands[0][-3] and close_lastday < b_bottom:
            result = "超跌:下跌趋势 在下轨以下\n品种:%s  日期：%s  \n 收盘价：%.2f \n 真实波动率：%.2f \n 布林线上轨 %.2f  \n 布林线中轨 %.2f  \n 布林线下轨 %.2f \n" % (
                j, today_date, close_lastday, a, b_uppter, b_mid, b_bottom)
            down_end += 1
            print("超跌:下跌趋势 在下轨以下:\n", result)
            with open("stock_5月4号.csv", "a", encoding="utf-8") as f:
                f.write(result)
        else:
            result = "没有趋势或在趋势中途:\n品种:%s  日期：%s  \n 收盘价：%.2f \n 真实波动率：%.2f \n 布林线上轨 %.2f  \n 布林线中轨 %.2f  \n 布林线下轨 %.2f \n" % (
                j, today_date, close_lastday, a, b_uppter, b_mid, b_bottom)
            no_trend += 1
            print("没有趋势或在趋势中途:", )
            with open("stock_5月4号.csv", "a", encoding="utf-8") as f:
                f.write(result)
    except:
        pass
total_num = up_begin + up_end + down_bedin + down_end + no_trend
up_begin_per = up_begin / total_num
up_end_per = up_end / total_num
down_bedin_per = down_bedin / total_num
down_end_per = down_end / total_num
no_trend_per = no_trend / total_num

dapan_trend = (
            "日期：%s\n 上涨初期数量为:%d占比为:%.2f\n上涨后期数量为: %d占比为: %.2f\n下跌初期数量为: %d占比为: %.2f\n下跌后期数量为: %d占比为%.2f \n无趋势数量为: %d 占比为: %.2f\n" % (
    today_date, up_begin,
    up_begin_per, up_end, up_end_per, down_bedin, down_bedin_per, down_end, down_end_per, no_trend, no_trend_per))
print(dapan_trend)
with open("stock_dapan.csv", "a", encoding="gbk") as f:
    f.write(dapan_trend)
    #     result = "  代码:%s  日期：%s  \n收盘价：%.2f \n真实波动率：%.2f \n布林线上轨 %.2f  \n布林线中轨 %.2f  \n布林线下轨 %.2f\n\n\n " % (
    #         j, today_date, close_lastday, a, b_bottom, b_mid, b_uppter)
    #     with open ("all.txt","a") as f :
    #             f.write(result)
    # except:
    #     pass


