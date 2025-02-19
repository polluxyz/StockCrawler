import os
import json
import time
from pathlib import Path
from datetime import date

# 將每天的股價合併成一個檔
def open_file(path):
  with open(path,"r",encoding="utf-8") as JSON:
    date_info = json.load(JSON)
  if date_info["total"] != 0:
    for i in date_info["data"]:
      stock_dateinfo.append(i)

def data_storage(path, data):
  Path(path).parent.mkdir(parents=True, exist_ok=True)
  with open(path, "w", encoding="utf-8") as file:
    file.write(json.dumps(data,
                          indent=3,
                          ensure_ascii=False))

def sanitize_filename(filename):
    # Windows 不允許的字符: < > : " / \ | ? *
    return ''.join(c for c in filename if c not in '<>:"/\\|?*')

with open("../stock_data/stock_list/Listed_stock_info_list.json","r",encoding="utf-8") as f:
  stock_info_list = json.load(f)

for stock_info in stock_info_list["stock"]:
  stock_no = stock_info["stockNo"]
  stock_name = sanitize_filename(stock_info["stockName"])  # 清理文件名中的非法字符
  stock_date = stock_info["stockDate"] # 股票上市日期

  stock_dateinfo = []

  # 儲存路徑
  storage_PATH = "../stock_data/total_date//stocks/{2}_{3}.json".format(Y,M,stock_no,stock_name)

  # 開啟之前最新一筆的資料
  if os.path.exists(storage_PATH):
    with open(storage_PATH,"r",encoding="utf-8") as d:
      all_date = json.load(d)["data"]


  else:
    pass



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
      PATH = "../stock_data/date_info/stocks/{2} {3}/{0}_{1:02}.json".format(Y,M,stock_no,stock_name)

      # 判斷路徑存在並開啟
      if os.path.exists(PATH):
        open_file(PATH)
      else:
        continue

  # 輸出json
  data_total = {}
  data_total["data"] = stock_dateinfo
  data_storage(storage_PATH, data_total)