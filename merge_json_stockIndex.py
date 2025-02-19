import os
import json
import time
from pathlib import Path
from datetime import date

# 將每天的股價合併成一個檔
def open_file(path):
  with open(path,"r",encoding="utf-8") as JSON:
    date_info = json.load(JSON)
  try:
    if len(date_info["data"]) != 0:
      for i in date_info["data"]:
        if path == PATH1:
          index_dateinfo.append(i)
        elif path == PATH2:
          index_volume.append(i)
  except:
    pass

def data_storage(path, data):
  Path(path).parent.mkdir(parents=True, exist_ok=True)
  with open(path, "w", encoding="utf-8") as file:
    file.write(json.dumps(data,
                          indent=3,
                          ensure_ascii=False))

def sanitize_filename(filename):
    # Windows 不允許的字符: < > : " / \ | ? *
    return ''.join(c for c in filename if c not in '<>:"/\\|?*')

index_dateinfo = []
index_volume = []

# 證交所最早的資料(民國88年)
start_year = 1999

# 今天日期
today = date.today()
end_year = today.year
end_month = today.month

for Y in range(start_year, end_year+1):

  ED_M = end_month if Y == end_year else 12
  for M in range(1, ED_M+1):
    PATH1 = "../stock_data/date_info/stock_indexs/TAIEX 加權指/total_index/{0}_{1:02}.json".format(Y,M)
    PATH2 = "../stock_data/date_info/stock_indexs/TAIEX 加權指/volume/{0}_{1:02}.json".format(Y,M)
    print(os.path.exists(PATH2))
    if os.path.exists(PATH1):
      open_file(PATH1)
    else:
      continue
    if os.path.exists(PATH2):
      open_file(PATH2)
    else:
      continue
print(len(index_dateinfo), len(index_volume))
# 輸出json
data_total1 = {}
data_total2 = {}
data_total1["data"] = index_dateinfo
data_total2["data"] = index_volume
storage_PATH1 = "../stock_data/total_date/stock_indexs/TAIEX 加權指/total_index.json".format(Y,M)
storage_PATH2 = "../stock_data/total_date/stock_indexs/TAIEX 加權指/volume.json".format(Y,M)
data_storage(storage_PATH1, data_total1)
data_storage(storage_PATH2, data_total2)