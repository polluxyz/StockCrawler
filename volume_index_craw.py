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
        self.url = "https://www.twse.com.tw/rwd/zh/afterTrading/FMTQIK"

        self.headers = self.req.headers

        self.headers["User-Agent"] = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"
        )

    def __get_data(self, date):
        res = self.req.get(
            self.url,
            params={
                "response": "json",
                "date": date,
            },
        )
        return res.json()

    def save_file(self, date, path):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        index_data = self.__get_data(date)
        # 資料不為0
        try:
            if len(index_data["data"]) != 0:
                print(path + " succeed")
                with open(path, "w", encoding="utf-8") as file:
                    file.write(json.dumps(index_data, indent=3, ensure_ascii=False))
            else:
                print(path + " no_data")
                with open(path, "w", encoding="utf-8") as file:
                    file.write(json.dumps(index_data, indent=3, ensure_ascii=False))
        except:
            print(path + " no_data")
            with open(path, "w", encoding="utf-8") as file:
                file.write(json.dumps(index_data, indent=3, ensure_ascii=False))


def sanitize_filename(filename):
    # Windows 不允許的字符: < > : " / \ | ? *
    return "".join(c for c in filename if c not in '<>:"/\\|?*')


def check():
    if checkfile["stat"].__contains__("沒有符合"):
        pass
    else:
        try:
            crawler.save_file(DATE, PATH)
            time.sleep(random.randint(1, 3))
        except:
            pass


crawler = Crawler()

start_year = 1999

# 今天日期
today = date.today()
end_year = today.year
end_month = today.month
for Y in range(start_year, end_year + 1):
    ED_M = end_month if Y == end_year else 12
    for M in range(1, ED_M + 1):
        D = "01"
        DATE = "{}{:02}{}".format(Y, M, D)
        PATH = "../stock_data/date_info/stock_indexs/TAIEX 加權指/volume/{0}_{1:02}.json".format(
            Y, M
        )

        # 判斷路徑是否存在
        if os.path.exists(PATH):
            with open(PATH, "r", encoding="utf-8") as c:
                checkfile = json.load(c)
            try:
                if len(checkfile["data"]) == 0:
                    check()
                    print(PATH)
                else:
                    continue
            except:
                crawler.save_file(DATE, PATH)
                time.sleep(random.randint(1, 3))
        else:
            crawler.save_file(DATE, PATH)
            time.sleep(random.randint(1, 3))
print("finish!")
time.sleep(5)
