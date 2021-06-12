# 導入 模組(module)
import requests
# 導入 BeautifulSoup 模組(module)：解析HTML 語法工具
from bs4 import BeautifulSoup

# 文章連結
PTT_URL = "https://www.ptt.cc/bbs/NTUcourse/search?page="
PTT_URL2="&q=[評價]"
PTT_test="https://www.ptt.cc/bbs/NTUcourse/search?q=%5B%E8%A9%95%E5%83%B9%5D"
pages=285
for i in range(pages):
    PTTCOURSE_URL=PTT_URL+str(i)+PTT_URL2
    #print(PTTCOURSE_URL)

# 設定Header與Cookie
my_headers = {'cookie': 'over18=1;'}
# 發送get 請求 到 ptt 八卦版
response = requests.get(PTT_test, headers = my_headers)
#標題
soup = BeautifulSoup(response.text, "html.parser")

results = soup.select("div.title")
print(results)
#取得各篇文章網址
article_href=[]
for item in results:

    try:

        item_href = item.select_one("a").get("href")

        article_href.append(item_href)

    except:

        continue;
print(article_href)
#  把網頁程式碼(HTML) 丟入 bs4模組分析
#soup = BeautifulSoup(response.text, "html.parser")
#print(soup)
## PTT 上方4個欄位
#header = soup.find_all('span','article-meta-value')
#print(header)