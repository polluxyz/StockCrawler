import os
import json
import time
import requests
from pathlib import Path
import pandas as pd
from io import StringIO
from datetime import datetime
from datetime import date


class Crawler:
    def __init__(self):
        self.req = requests.Session()
        self.url = "https://mops.twse.com.tw/mops/web/ajax_t164sb05"

        self.headers = self.req.headers
        self.headers["User-Agent"] = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"
        )

    def __get_data(self, stock_no, year, season):
        res = self.req.post(
            self.url,
            {
                "encodeURIComponent": 1,
                "step": 1,
                "firstin": 1,
                "off": 1,
                "TYPEK": "all",
                "isnew": "false",
                "co_id": stock_no,
                "year": year,
                "season": season,
            },
        )
        res.encoding = "utf-8"
        return res

    def __get_data2(self, stock_no, year, season):
        res2 = self.req.post(
            self.url,
            {
                "encodeURIComponent": 1,
                "step": 2,
                "firstin": 1,
                "TYPEK": "sii",
                "co_id": stock_no,
                "year": year,
                "season": season,
            },
        )
        res2.encoding = "utf-8"
        return res2

    def __data_check(self, stock_no, year, season, data):
        if data.__contains__("查無所需資料"):
            return None
        elif data.__contains__("詳細資料"):
            data = self.__get_data2(stock_no, year, season)
            # 確保資料內有完整的財報
            return self.__data_check(stock_no, year, season, data.text)
        return data

    def __solve_data(self, stock_no, year, season):
        pre_data = self.__get_data(stock_no, year, season)
        data = self.__data_check(stock_no, year, season, pre_data.text)
        if data == None:
            return None
        else:
            html_df = pd.read_html(StringIO(data))
            data_form = html_df[1] if len(html_df) == 2 else html_df[2]
            field = []
            field.append("Season")
            df = {}
            df["Season"] = "{}/{}".format(year + 1911, season)
            for n in range(0, len(data_form)):
                df_row = data_form.loc[n]  # 第n列
                field.append(df_row.iloc[0])
                df[df_row.iloc[0]] = (
                    int(df_row.iloc[1]) if not pd.isnull(df_row.iloc[1]) else None
                )  # 每一列數據
            result = {"field": field, "data": df}
            return result

    def __save_file(self, path, stock_data):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as file:
            file.write(json.dumps(stock_data, indent=3, ensure_ascii=False))

    def __trash(self, trash_path):
        Path(trash_path).parent.mkdir(parents=True, exist_ok=True)
        with open(trash_path, "w", encoding="utf-8") as file:
            file.write(json.dumps("no_data"))

    def Spider(self, stock_no, year, season, path, trash_path):
        stock_data = self.__solve_data(stock_no, year, season)
        if stock_data == None:
            print("{}/{}/{}_No Data".format(stock_no, year, season))
            if year == year_now:
                pass
            else:
                self.__trash(trash_path)
        else:
            print("{}/{}/{}_Success".format(stock_no, year, season))
            self.__save_file(path, stock_data)


def sanitize_filename(filename):
    # Windows 不允許的字符: < > : " / \ | ? *
    return "".join(c for c in filename if c not in '<>:"/\\|?*')


def implement(stock_no, year, season, path, trash_path):
    try:
        crawler.Spider(stock_no, year, season, path, trash_path)
    except Exception as e:
        print(
            "{}/{}/{}_Error {}: {}".format(stock_no, year, season, datetime.now(), e),
            flush=True,
        )
        time.sleep(60)
        implement(stock_no, year, season, path, trash_path)


def stocks(stock_info):
    stock_no = stock_info["stockNo"]
    stock_name = sanitize_filename(stock_info["stockName"])  # 清理文件名中的非法字符

    for Y in range(102, year_now + 1):
        ED_S = season_now[month_now] if Y == year_now else 4
        for S in range(1, ED_S + 1):
            PATH = "../stock_data/cashFlow_statement/{2} {3}/{0}_{1}.json".format(
                Y + 1911, S, stock_no, stock_name
            )
            trash_PATH = (
                "../stock_data/cashFlow_statement/TRASH/{2} {3}/{0}_{1}.json".format(
                    Y + 1911, S, stock_no, stock_name
                )
            )
            # 判斷路徑是否存在
            if os.path.exists(PATH) or os.path.exists(trash_PATH):
                continue
            else:
                implement(stock_no, Y, S, PATH, trash_PATH)
                time.sleep(3)


with open(
    "../stock_data/stock_list/Listed_stock_info_list.json", "r", encoding="utf-8"
) as f:
    stock_info_list = json.load(f)

with open(
    "../stock_data/stock_list/OTC_stock_info_list.json", "r", encoding="utf-8"
) as o:
    OTC_info_list = json.load(o)

# 今天日期
today = date.today()
year_now = today.year - 1911
month_now = today.month
day_now = today.day
season_now = {1: 4, 2: 4, 3: 4, 4: 1, 5: 1, 6: 1, 7: 2, 8: 2, 9: 2, 10: 3, 11: 3, 12: 3}

crawler = Crawler()
for Listed_stock in stock_info_list["stock"]:
    stocks(Listed_stock)

for OTC_stock in OTC_info_list["stock"]:
    stocks(OTC_stock)
