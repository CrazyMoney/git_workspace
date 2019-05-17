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

list_daima = ["CF.ZCE", "SR.ZCE", "TA.ZCE", 'RB.SHF', 'SP.SHF', 'AU.SHF', 'A.DCE', 'M.DCE', 'I.DCE', 'JD.DCE']
list_name = ['棉花主力', "白糖主力", 'PTA主力', '螺纹钢主力', '纸浆主力', '黄金主力', '豆一主力', '豆粕主力', '铁矿石主力', '鸡蛋主力']


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

for i in range(10):
    daima = list_daima[i]
    name = list_name[i]
    # engine = create_engine('mysql+pymysql://root:zhou1234@localhost:3306/furture?charset=utf8', pool_size=150, echo=False)
    df = pro.fut_daily(ts_code=daima, start_date="20190326", end_date=today_date,
                       fields='ts_code,trade_date,pre_close,pre_settle,open,high,low,close,settle,vol')
    """"在线获取数据"""
    df = pd.DataFrame(df)

    close = np.array(df.ix[::1]["close"])
    high = np.array(df.ix[::1]["high"])
    low = np.array(df.ix[::1]["low"])
    close_boll = np.array(df.ix[::-1]["close"])

    atr = func.ATR(high, low, close, timeperiod=14)

    a = atr[-1]

    close_lastday = df.ix[0]["close"]

    bbands = func.BBANDS(close_boll, timeperiod=5)

    b_uppter = bbands[0][-1]

    b_mid = bbands[1][-1]
    b_bottom = bbands[2][-1]
    if bbands[0][-1] > bbands[0][-2] > bbands[0][-3] and close_lastday < b_mid:
        result = "品种:%s  日期：%s  \n 收盘价：%.2f \n 真实波动率：%.2f \n 布林线上轨 %.2f  \n 布林线中轨 %.2f  \n 布林线下轨 %.2f \n" % (
            name, today_date, close_lastday, a, b_uppter, b_mid, b_bottom)
        up_begin += 1
        with open("further_5月4号.csv", "a", encoding="gbk") as f:
            f.write(result)
        print("上涨初期:上涨趋势 在中轨以下\n", result)
    elif bbands[0][-1] > bbands[0][-2] > bbands[0][-3] and close_lastday > b_uppter:
        result = "品种:%s  日期：%s  \n 收盘价：%.2f \n 真实波动率：%.2f \n 布林线上轨 %.2f  \n 布林线中轨 %.2f  \n 布林线下轨 %.2f \n" % (
            name, today_date, close_lastday, a, b_uppter, b_mid, b_bottom)
        up_end += 1
        print("上涨回调压低大:上涨趋势 在下轨以下\n", result)
        with open("further_5月4号.csv", "a", encoding="gbk") as f:
            f.write(result)
    elif bbands[0][-1] < bbands[0][-2] < bbands[0][-3] and close_lastday > b_mid:
        result = "品种:%s  日期：%s  \n 收盘价：%.2f \n 真实波动率：%.2f \n 布林线上轨 %.2f  \n 布林线中轨 %.2f  \n 布林线下轨 %.2f \n" % (
            name, today_date, close_lastday, a, b_uppter, b_mid, b_bottom)
        down_bedin += 1
        print("下跌初期:下跌趋势 在中轨以下\n", result)
        with open("further_5月4号.csv", "a", encoding="gbk") as f:
            f.write(result)

    elif bbands[0][-1] < bbands[0][-2] < bbands[0][-3] and close_lastday < b_bottom:
        result = "品种:%s  日期：%s  \n 收盘价：%.2f \n 真实波动率：%.2f \n 布林线上轨 %.2f  \n 布林线中轨 %.2f  \n 布林线下轨 %.2f \n" % (
            name, today_date, close_lastday, a, b_uppter, b_mid, b_bottom)
        down_end += 1
        print("超跌:下跌趋势 在下轨以下\n", result)
        with open("further_5月4号.csv", "a", encoding="gbk") as f:
            f.write(result)
    else:
        result = "品种:%s  日期：%s  \n 收盘价：%.2f \n 真实波动率：%.2f \n 布林线上轨 %.2f  \n 布林线中轨 %.2f  \n 布林线下轨 %.2f \n" % (
            name, today_date, close_lastday, a, b_uppter, b_mid, b_bottom)
        no_trend += 1
        print("没有趋势或在趋势中途:", result)
        with open("further_5月4号.csv", "a", encoding="utf-8") as f:
            f.write(result)
total_num = up_begin + up_end + down_bedin + down_end + no_trend
up_begin_per = up_begin / total_num
up_end_per = up_end / total_num
down_bedin_per = down_bedin / total_num
down_end_per = down_end / total_num
no_trend_per = no_trend / total_num

dapan_trend = ("日期：%s\n 上涨初期数量为:%d占比为:%.1f\n上涨后期数量为: %d 占比为: %.1f\n下跌初期数量为: %d 占比为: %.1f\n下跌后期数量为: %d 占比为%.1f \n无趋势数量为: %d  占比为: %.1f\n" %(today_date, up_begin,
      up_begin_per, up_end, up_end_per, down_bedin, down_bedin_per, down_end, down_end_per, no_trend, no_trend_per))
print(dapan_trend)
with open("further_dapan.csv", "a", encoding="utf-8") as f:
    f.write(dapan_trend)