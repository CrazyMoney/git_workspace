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

class fur:
    def api_engin_init(self):
        # 初始化mysql工具,连接tusahre  api


        self.engine = create_engine('mysql+pymysql://root:zhou1234@localhost:3306/furture?charset=utf8', pool_size=150,
                               echo=False)
        ts.set_token("8d29f89b7cc516c302a9d0e50bf6a3cce8d0ef886d93d30be66b1374")
        self.pro = ts.pro_api()

    def get_day(self):
        #获取某个品种最近几年的数据
        df = self.pro.fut_daily(ts_code='TA.ZCE')
        df = pd.DataFrame(df)
        pd.io.sql.to_sql(df, 'PTA', schema='furture', con=self.engine, if_exists="replace")


    def read_sql(self):
        #读取sql表格
        furture_list = ["apple", "dadou", "egg", "pta"]
        l = len(furture_list)
        for i in range(l):
            rd2 = pd.read_sql(furture_list[i], self.engine)


    def cash_supply(self):
        #获取货币 月度货币投放量
        cash_supply = ts.get_money_supply()
        print(cash_supply)
        cash_supply = pd.DataFrame(cash_supply)
        cash_supply.to_excel("cash_supply.xls")

def main():
    furture1 =fur()
    furture1.api_engin_init()
    furture1.cash_supply()
if __name__ == '__main__':
    main()


