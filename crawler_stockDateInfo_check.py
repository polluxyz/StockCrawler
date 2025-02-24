import os
import json
import time
import random
import requests
from pathlib import Path
from datetime import date


class Crawler:
    def __init__(self):
        self.req = requests.Session()
        self.url = "https://www.twse.com.tw/rwd/zh/afterTrading/STOCK_DAY"

        self.headers = self.req.headers

        self.headers["User-Agent"] = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"
        )

    def __get_data(self, date, stock_no):
        res = self.req.get(
            self.url, params={"response": "json", "date": date, "stockNo": stock_no}
        )
        return res.json()

    def save_file(self, date, stock_no, path):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        stock_data = self.__get_data(date, stock_no)
        # 資料不為0
        if stock_data["total"] != 0:
            # print(path+" succeed")
            with open(path, "w", encoding="utf-8") as file:
                file.write(json.dumps(stock_data, indent=3, ensure_ascii=False))
        else:
            print(path + " error")
            with open(path, "w", encoding="utf-8") as file:
                file.write(json.dumps(stock_data, indent=3, ensure_ascii=False))


def sanitize_filename(filename):
    # Windows 不允許的字符: < > : " / \ | ? *
    return "".join(c for c in filename if c not in '<>:"/\\|?*')


def check():
    if checkfile["stat"].__contains__("沒有符合"):
        pass
    else:
        try:
            crawler.save_file(DATE, stock_no, PATH)
            time.sleep(random.randint(1, 3))
        except:
            pass


with open("./Listed_stock_info_list.json", "r", encoding="utf-8") as f:
    stock_info_list = json.load(f)
print(len(stock_info_list["stock"]))

crawler = Crawler()
for stock_info in stock_info_list["stock"]:
    stock_no = stock_info["stockNo"]
    stock_name = sanitize_filename(stock_info["stockName"])  # 清理文件名中的非法字符
    stock_industry = stock_info["stockIndustry"]
    stock_date = stock_info["stockDate"]  # 股票上市日期

    # 證交所最早的資料(民國99年)
    start_year = int(stock_date[:4]) if int(stock_date[:4]) > 2010 else 2010
    start_month = int(stock_date.split("/")[1])

    # 今天日期
    today = date.today()
    end_year = today.year
    end_month = today.month
    for Y in range(start_year, end_year + 1):
        ST_M = start_month if Y == start_year & int(stock_date[:4]) >= 2010 else 1
        ED_M = end_month if Y == end_year else 12
        for M in range(ST_M, ED_M + 1):
            D = "01"
            DATE = "{}{:02}{}".format(Y, M, D)
            PATH = "./stock_data/{2} {3}/date_info/{0}_{1:02}.json".format(
                Y, M, stock_no, stock_name
            )

            # print("{} {}/{}_{}".format(stock_no,stock_name,Y,M))

            # 判斷路徑是否存在
            if os.path.exists(PATH):
                with open(PATH, "r", encoding="utf-8") as c:
                    checkfile = json.load(c)
                if checkfile["total"] == 0:
                    check()
                    print(PATH)
            else:
                crawler.save_file(DATE, stock_no, PATH)
                time.sleep(random.randint(1, 3))
print("finish!")
time.sleep(5)
