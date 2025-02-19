import os
import shutil
import json
from pathlib import Path
from datetime import date
import time

def sanitize_filename(filename):
    # Windows 不允許的字符: < > : " / \ | ? *
    return ''.join(c for c in filename if c not in '<>:"/\\|?*')

def date_info(stock_date, stock_no, stock_name, types):
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
            string_M = "{:02}".format(M)
            move_file(stock_no, stock_name, types, Y, string_M)

def balance_sheet(stock_no, stock_name, types):
    for Y in range(102, 114):
        ED_S = 1 if Y == 113 else 4
        for S in range(1, ED_S+1):
            move_file(stock_no, stock_name, types, Y+1911, S)

def move_file(stock_no, stock_name, types, year, season_month):
    old_path = "./stock_data/{} {}/{}/{}_{}.json".format(stock_no, stock_name, types, year, season_month)
    new_path = "./stock_data/{}/{} {}/{}_{}.json".format(types, stock_no, stock_name, year, season_month)

    # 移動資料
    if os.path.exists(old_path):
        Path(new_path).parent.mkdir(parents=True, exist_ok=True)
        shutil.move(old_path, new_path)
    else:
        pass

def del_files(stock_no, stock_name, types):
    if types == "":
        folder_path = "./stock_data/{} {}".format(stock_no, stock_name)
    else:
        folder_path = "./stock_data/{} {}/{}".format(stock_no, stock_name, types)

    if os.path.exists(folder_path):
        os.rmdir(folder_path)
    else:
        pass

def change_path(types):
    with open("./Listed_stock_info_list.json","r",encoding="utf-8") as f:
        stock_info_list = json.load(f)

    for stock_info in stock_info_list["stock"]:
        stock_no = stock_info["stockNo"]
        stock_name = sanitize_filename(stock_info["stockName"])
        stock_date = stock_info["stockDate"] # 股票上市日期

        if types == "date_info":
            date_info(stock_date, stock_no, stock_name, types)
        elif types == "balance_sheet":
            balance_sheet(stock_no, stock_name, types)
        del_files(stock_no, stock_name, types)

        if list(os.walk("./stock_data/{} {}".format(stock_no, stock_name)))[0][1] == []:
            del_files(stock_no, stock_name, "")


if __name__ == "__main__":
    file_type = ["date_info", "balance_sheet"]
    for i in file_type:
        change_path(i)