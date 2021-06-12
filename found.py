# 導入 模組(module)
import requests
# 導入 BeautifulSoup 模組(module)：解析HTML 語法工具
from bs4 import BeautifulSoup
import bs4
#設定字典
PTTCOURSE_dct={}
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
# 發送get 請求 到 ptt course版
response = requests.get(PTT_test, headers = my_headers)
#標題
soup = BeautifulSoup(response.text, "html.parser")

results = soup.select("div.title")
#print(results)
#取得各篇文章網址
article_href=[]
for item in results:

    try:

        item_href = item.select_one("a").get("href")

        article_href.append(item_href)

    except:

        continue;
#print(article_href)
URLlist=[]
#for pcontent in range(len(article_href)):
    #URL = "https://www.ptt.cc"+article_href[pcontent]
for i in range(1):
    URL="https://www.ptt.cc/bbs/NTUcourse/M.1619532340.A.D2A.html"
    print(URL)
    # 發送get 請求 到 ptt 八卦版
    response = requests.get(URL, headers=my_headers)

    #  把網頁程式碼(HTML) 丟入 bs4模組分析
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    #主要資料
    header = soup.find_all('span', 'article-meta-value')
    #print(header)
    # 作者
    author= header[0].text
    # 看版
    board = header[1].text
    # 標題
    title = header[2].text
    # 日期
    date =  header[3].text
    #內文資料
    main_container = soup.find(id='main-container')
    content=main_container.find_all("span",class_="f3")
    print(main_container)
    print(content)
    for content in content:
        massage=content.getText()
        URLlist.append(massage)
    print(URLlist)
    #print(main_container)
    #print(content)

    #將資料儲存進字典
    PTTCOURSE_dct[title]=URLlist
print(PTTCOURSE_dct)

