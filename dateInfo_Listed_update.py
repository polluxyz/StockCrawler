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
            print(path + " updated")
            with open(path, "w", encoding="utf-8") as file:
                file.write(json.dumps(stock_data, indent=3, ensure_ascii=False))
        else:
            print(path + " no_data")
            with open(path, "w", encoding="utf-8") as file:
                file.write(json.dumps(stock_data, indent=3, ensure_ascii=False))


def sanitize_filename(filename):
    # Windows 不允許的字符: < > : " / \ | ? *
    return "".join(c for c in filename if c not in '<>:"/\\|?*')


with open(
    "../stock_data/stock_list/Listed_stock_info_list.json", "r", encoding="utf-8"
) as f:
    stock_info_list = json.load(f)
print(len(stock_info_list["stock"]))

crawler = Crawler()
for stock_info in stock_info_list["stock"]:
    stock_no = stock_info["stockNo"]
    stock_name = sanitize_filename(stock_info["stockName"])  # 清理文件名中的非法字符

    # 今天日期
    today = date.today()
    year = today.year
    month = today.month
    day = today.day

    DATE = "{}{:02}{}".format(year, month, day)
    today_date = "{}/{:02}/{}".format(year - 1911, month, day)
    PATH = "../stock_data/date_info/stocks/{2} {3}/{0}_{1:02}.json".format(
        year, month, stock_no, stock_name
    )

    files_data = "../stock_data/date_info/stocks/{} {}".format(stock_no, stock_name)
    last_json = list(os.walk(files_data))[0][2][-1]
    today_json = "{}_{:02}.json".format(year, month)
    judge_json = "{}_{:02}.json".format(
        year if month < 12 else year + 1, month + 1 if month < 12 else 1
    )

    if last_json != today_json:
        # 先判斷是否有這個月的資料，沒有就更新到這個月為止
        while last_json != judge_json:
            last_path = "../stock_data/date_info/stocks/{} {}/{}".format(
                stock_no, stock_name, last_json
            )
            spl = last_json.split(".")[0].split("_")
            last_year = spl[0]
            last_month = spl[1]
            last_date = "{}{:02}01".format(last_year, last_month)
            try:
                crawler.save_file(last_date, stock_no, last_path)
                time.sleep(random.randint(1, 3))
            except Exception as e:
                print(e)
                crawler.save_file(last_date, stock_no, last_path)
                time.sleep(random.randint(1, 3))
            next_month = int(last_month) + 1 if int(last_month) < 12 else 1
            next_year = int(last_year) if int(last_month) < 12 else int(last_year) + 1
            last_json = "{}_{:02}.json".format(next_year, next_month)
    else:
        # 判斷路徑是否存在
        if os.path.exists(PATH):
            with open(PATH, "r", encoding="utf-8") as c:
                checkfile = json.load(c)

        try:
            if checkfile["data"][-1][0] == today_date:
                continue
            else:
                crawler.save_file(DATE, stock_no, PATH)
                time.sleep(random.randint(1, 3))
        except Exception as e:
            print(e)
            crawler.save_file(DATE, stock_no, PATH)
            time.sleep(random.randint(1, 3))

print("finish!")
time.sleep(5)
