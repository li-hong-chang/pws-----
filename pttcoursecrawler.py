# 導入 模組(module)
import requests
# 導入 BeautifulSoup 模組(module)：解析HTML 語法工具
from bs4 import BeautifulSoup
import bs4
teacher=input()
course=input()
#設定字典
PTTCOURSE_dct={}
PTTCOURSE_alldct={}
#list設定
article_href = []
# 文章連結
PTT_URL = "https://www.ptt.cc/bbs/NTUcourse/search?page="
PTT_URL2="&q="
teacher_course=teacher+" "+course
course_teacher=course+" "+teacher
#PTT_test="https://www.ptt.cc/bbs/NTUcourse/search?q=%5B%E8%A9%95%E5%83%B9%5D"
#pages=int(input())#有284頁
for i in range(5):
    m=i+1
    PTTCOURSE_URL=PTT_URL+str(m)+PTT_URL2+teacher_course
    #print(PTTCOURSE_URL)
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
for i in range(5):
    m=i+1
    PTTCOURSE_URL=PTT_URL+str(m)+PTT_URL2+course_teacher
    #print(PTTCOURSE_URL)
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
    #清空檔案
    PTTCOURSE_dct={}
    URL = "https://www.ptt.cc"+article_href[pcontent]
    #print(URL)
    # 發送get 請求 到 ptt course版
    response = requests.get(URL, headers=my_headers)

    #  把網頁程式碼(HTML) 丟入 bs4模組分析
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    #主要資料
    header = soup.find_all('span', 'article-meta-value')
    # 作者
    author= header[0].text
    # 看版
    board = header[1].text
    # 標題
    title = header[2].text
    #print(title)
    # 日期
    #date =  header[3].text
    #內文資料
    main_container = soup.find(id='main-container')
    content=main_container.find_all("span")
    con=main_container.getText()
    #尋找各內容方塊
    z=con.find("哪")
    a=con.find("ψ 授課教師")
    b=con.find("λ")
    c=con.find("δ")
    d=con.find("Ω")
    e=con.find("η")
    f=con.find("μ")
    g=con.find("σ")
    h=con.find("ρ")
    j=con.find("ω")
    k = con.find("Ψ")
    l = con.find("--")
    if z==-1:
        z=a
    if a==-1:
        a=b
    if b==-1:
        b=c
    if c==-1:
        c=d
    if d==-1:
        d=f
    if g==-1:
        g=h
    if j==-1:
        j=k
    if k==-1:
        k=l
    #print(a,b,c,d,e,f,g,h,j,k,l)
    PTTCOURSE_dct["哪一學年度修課："]=con[z:a].replace("哪一學年度修課：","")
    PTTCOURSE_dct["ψ 授課教師 (若為多人合授請寫開課教師，以方便收錄)"] = con[a:b].replace("ψ 授課教師 (若為多人合授請寫開課教師，以方便收錄)","")
    PTTCOURSE_dct["δ λ 開課系所與授課對象 (是否為必修或通識課 / 內容是否與某些背景相關)"] = con[b:c].replace("λ 開課系所與授課對象 (是否為必修或通識課 / 內容是否與某些背景相關)","")
    PTTCOURSE_dct["δ 課程大概內容"] = con[c:d].replace("δ 課程大概內容","")
    PTTCOURSE_dct["Ω 私心推薦指數(以五分計) ★★★★★"] = con[d:e].replace("Ω 私心推薦指數(以五分計)","")
    PTTCOURSE_dct["η 上課用書(影印講義或是指定教科書)"] = con[e:f].replace("η 上課用書(影印講義或是指定教科書)","")
    PTTCOURSE_dct["μ 上課方式(投影片、團體討論、老師教學風格)"] = con[f:g].replace("μ 上課方式(投影片、團體討論、老師教學風格)","")
    PTTCOURSE_dct["σ 評分方式(給分甜嗎？是紮實分？)"] = con[g:h].replace("σ 評分方式(給分甜嗎？是紮實分？)","")
    PTTCOURSE_dct["ρ 考題型式、作業方式"] = con[h:j].replace("ρ 考題型式、作業方式：","")
    PTTCOURSE_dct["ω 其它(是否注重出席率？如果為外系選修，需先有什麼基礎較好嗎？老師個性？ 加簽習慣？嚴禁遲到等…)"] = con[j:k].replace("ω 其它(是否注重出席率？如果為外系選修，需先有什麼基礎較好嗎？老師個性？ 加簽習慣？嚴禁遲到等…)","")
    PTTCOURSE_dct["Ψ 總結"]=con[k:l].replace("Ψ 總結","")
    #print(con[k:l])
    #print(PTTCOURSE_dct)
    #
    comentment=[]
    num = 0
    for tag in soup.select('div.push'):
        num += 1
        push_tag = tag.find("span", {'class': 'push-tag'}).text
        # print "push_tag:",push_tag
        push_userid = tag.find("span", {'class': 'push-userid'}).text
        # print "push_userid:",push_userid
        push_content = tag.find("span", {'class': 'push-content'}).text.replace("\n","")
        push_content = push_content[1:]
        # print "push_content:",push_content
        time=tag.find("span", {'class': 'push-ipdatetime'}).text
        message=str(push_tag)+str(push_userid)+":"+str(push_content)+"     "+str(time)
        #print(message)
        comentment.append(message)
    #print(URLlist)
    #print(main_container)
    #print(comentment)
    #將資料儲存進字典
    PTTCOURSE_dct["留言"]=comentment
    PTTCOURSE_dct["文章網址"]=URL
    #print(PTTCOURSE_dct)
    PTTCOURSE_alldct[title]=PTTCOURSE_dct
print(PTTCOURSE_alldct)
print(PTTCOURSE_alldct.keys())