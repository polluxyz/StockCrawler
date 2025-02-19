import os
import json
import time
import random
import requests
from pathlib import Path
from datetime import date
from fake_useragent import UserAgent

class Crawler():
  def __init__(self):
    self.req = requests.Session()
    self.url = "https://www.twse.com.tw/rwd/zh/afterTrading/STOCK_DAY"

    self.headers = self.req.headers

    # 偽裝 User-Agent
    ua = UserAgent()
    self.headers["User-Agent"] = ua.random

  def __get_data(self, date, stock_no):
    res = self.req.get(self.url,
                       params={
                         "response": "json",
                         "date": date,
                         "stockNo": stock_no
                       })
    return res.json()

  def save_file(self, date, stock_no, path):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    stock_data = self.__get_data(date, stock_no)
    # 資料不為0
    if stock_data["total"] != 0:
      with open(path, "w", encoding="utf-8") as file:
        file.write(json.dumps(stock_data,
                            indent=3,
                            ensure_ascii=False))

with open("./Listed_stock_info_list.json","r",encoding="utf-8") as f:
  stock_info_list = json.load(f)

for stock_info in stock_info_list["stock"]:
  stock_no = stock_info["stockNo"]
  stock_name = stock_info["stockName"]
  stock_industry = stock_info["stockIndustry"]
  stock_date = stock_info["stockDate"] # 股票上市日期

  # 證交所最早的資料(民國99年)
  start_year = int(stock_date[:4]) if int(stock_date[:4]) > 2010 else 2010
  start_month = int(stock_date.split("/")[1])

  # 今天日期
  today = date.today()
  end_year = today.year
  end_month = today.month
  for Y in range(start_year, end_year+1):
    ST_M = start_month if Y == start_year & int(stock_date[:4]) >= 2010 else 1
    ED_M = end_month if Y == end_year else 12
    for M in range(ST_M, ED_M+1):
      D = "01"
      DATE = "{}{:02}{}".format(Y,M,D)
      PATH = "./stock_data/{2} {3}/date_info/{0}_{1:02}.json".format(Y,M,stock_no,stock_name)
      # 判斷路徑是否存在
      if os.path.exists(PATH) == True:
        continue
      else:
        try:
          Crawler().save_file(DATE,stock_no,PATH)
        except:
          print(PATH)
          pass
        time.sleep(random.randint(3,5))