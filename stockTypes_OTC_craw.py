from bs4 import BeautifulSoup
import json
import requests

# 送出 HTTP Request
url = "https://isin.twse.com.tw/isin/class_main.jsp"
res = requests.get(
    url, params={"market": "2", "issuetype": "4", "Page": "1", "chklike": "Y"}
)

# 處理編碼，使用預設 utf-8 的話 res.text 的內容會有亂碼
res.encoding = "MS950"
res_html = res.text

# Parse
soup = BeautifulSoup(res_html, "lxml")

tr_list = soup.select("table")[1].select("tr")
tr_list.pop(0)

# 開始處理資料
result = []
for tr in tr_list:

    td_list = tr.select("td")

    # 股票代碼
    stock_no_val = td_list[2].text

    # 股票名稱
    stock_name_val = td_list[3].text

    # 股票產業類別
    stock_industry_val = td_list[6].text

    # 股票上市日期

    stock_date_val = td_list[7].text

    # 整理成 dict 存起來
    result.append(
        {
            "stockNo": stock_no_val,
            "stockName": stock_name_val,
            "stockIndustry": stock_industry_val,
            "stockDate": stock_date_val,
        }
    )

# 將 dict 輸出成檔案
stock_list_dict = {"stock": result}
with open(
    "../stock_data/stock_list/OTC_stock_info_list.json", "w", encoding="utf-8"
) as f:
    f.write(json.dumps(stock_list_dict, indent=3, ensure_ascii=False))
