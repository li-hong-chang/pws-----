# 導入 模組(module)
import requests
# 導入 BeautifulSoup 模組(module)：解析HTML 語法工具
from bs4 import BeautifulSoup
import bs4
#設定字典
PTTCOURSE_dct={}
PTTCOURSE_alldct={}
#list設定
article_href = []
# 文章連結
PTT_URL = "https://www.ptt.cc/bbs/NTUcourse/search?page="
PTT_URL2="&q=[評價]"
#PTT_test="https://www.ptt.cc/bbs/NTUcourse/search?q=%5B%E8%A9%95%E5%83%B9%5D"
pages=int(input())#有284頁
for i in range(pages):
    m=i+1
    PTTCOURSE_URL=PTT_URL+str(m)+PTT_URL2
    print(PTTCOURSE_URL)
    # 設定Header與Cookie
    my_headers = {'cookie': 'over18=1;'}
    # 發送get 請求 到 ptt course版
    response = requests.get(PTTCOURSE_URL, headers=my_headers)
    # 標題
    soup = BeautifulSoup(response.text, "html.parser")

    results = soup.select("div.title")
    # print(results)
    # 取得各篇文章網址
    for item in results:

        try:

            item_href = item.select_one("a").get("href")

            article_href.append(item_href)

        except:

            continue;
for pcontent in range(len(article_href)):
    URL = "https://www.ptt.cc"+article_href[pcontent]
    #print(URL)
    # 發送get 請求 到 ptt course版
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
    #date =  header[3].text
    #內文資料
    main_container = soup.find(id='main-container')
    content=main_container.find_all("span")
    con=main_container.getText()
    z=con.find("哪")
    a=con.find("ψ")
    PTTCOURSE_dct["哪一學年度修課"]=con[z:a].replace("哪一學年度修課：","")
    b=con.find("λ")
    PTTCOURSE_dct["授課教師"] = con[a:b].replace("ψ 授課教師 (若為多人合授請寫開課教師，以方便收錄) ","")
    c=con.find("δ")
    PTTCOURSE_dct["開課系所與授課對象"] = con[b:c].replace("λ 開課系所與授課對象 (是否為必修或通識課 / 內容是否與某些背景相關)  ","")
    d=con.find("Ω")
    PTTCOURSE_dct["課程大概內容"] = con[c:d].replace("δ 課程大概內容 ","")
    e=con.find("η")
    PTTCOURSE_dct["私心推薦指數"] = con[d:e].replace("Ω 私心推薦指數(以五分計) ","")
    f=con.find("μ")
    PTTCOURSE_dct["上課用書"] = con[e:f].replace("η 上課用書(影印講義或是指定教科書) ","")
    g=con.find("σ")
    PTTCOURSE_dct["上課方式"] = con[f:g].replace("μ 上課方式(投影片、團體討論、老師教學風格) ","")
    h=con.find("ρ")
    PTTCOURSE_dct["評分方式"] = con[g:h].replace("σ 評分方式(給分甜嗎？是紮實分？) ","")
    j=con.find("ω")
    PTTCOURSE_dct["考題型式作業方式"] = con[h:j].replace("ρ 考題型式、作業方式：","")
    k=con.find("Ψ")
    PTTCOURSE_dct["其它"] = con[j:k].replace("ω 其它(是否注重出席率？如果為外系選修，需先有什麼基礎較好嗎？老師個性？ 加簽習慣？嚴禁遲到等…) ","")
    l=con.find("--")
    PTTCOURSE_dct["總結"]=con[k:l].replace("Ψ 總結 ","")
    #print(PTTCOURSE_dct)
    #
    comentment=[]
    articles=soup.find_all("div","push")
    for article in articles:
        messages = article.find('span', 'f3 push-content').getText()
        messages =messages.replace(':',"")
        comentment.append(messages)
    #print(URLlist)
    #print(main_container)
    #print(content)
    #將資料儲存進字典
    PTTCOURSE_dct["留言"]=comentment
    PTTCOURSE_dct["文章網址"]=URL
    #print(PTTCOURSE_dct)
    PTTCOURSE_alldct[title]=PTTCOURSE_dct
print(PTTCOURSE_alldct)
print(PTTCOURSE_alldct.keys())
print(PTTCOURSE_alldct['Re: [評價] 108-2 集合論 呂學一'])