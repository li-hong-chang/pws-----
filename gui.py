import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk
from snownlp import SnowNLP
import time
from bs4 import BeautifulSoup
import requests
import os


class Action(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.grid()
        self.master.geometry('1300x600')  # 設定視窗初始大小
        self.master.minsize(1300, 600)  # 最大
        self.master.maxsize(1300, 600)  # 最小
        self.master.title('聖倫吾皇萬福金安')  # 名稱
        self.createWidgets()  # 其他東東

    def createWidgets(self):
        # 字型設定
        f1 = tkFont.Font(size=30, family="Courier New")
        f2 = tkFont.Font(size=25, family="Courier New")
        f3 = tkFont.Font(size=20, family="Courier New")
        f4 = tkFont.Font(size=16, family="Courier New")
        # 白色背景
        self.background = tk.Canvas(self, height=600, width=1300, bg='white').pack()
        # 輸出文字
        self.output = tk.Text(self, width=52, height=22, font=f4, bg='#4DFFFF')
        self.output.place(x=600, y=75)
        # 按鈕
        self.start = tk.Button(self, text="開始", height=1, width=4, bg='#ffcc00', font=f3, command=self.click).place(x=250, y=400)
        self.intro = tk.Button(self, text="1.輸入完整教師、課程名稱\n2.選擇資料數量和排序方式\n3.點擊開始\n4.總共有5種結果", width=40, bg='orange', font=f4, state='disable').place(x=32, y=20)
        # 標題
        self.consequence = tk.Label(self, text="結果:", height=1, width=5, bg='white', font=f2).place(x=590, y=25)  # 結果
        self.arrange_label = tk.Label(self, text="排序方式:", height=1, width=10, bg='white', font=f2).place(x=17, y=340)
        self.course_label = tk.Label(self, text="教師:", height=1, width=5, bg='white', font=f2).place(x=100, y=130)
        self.teacher_label = tk.Label(self, text="課程:", height=1, width=5, bg='white', font=f2).place(x=100, y=200)
        self.num_label = tk.Label(self, text="資料數量:", height=1, width=10, bg='white', font=f2).place(x=17, y=270)
        self.sequence = tk.Label(self, text="大不推", height=1, width=5, fg='red', bg='white', font=f2)
        # 輸入
        self.teacher = tk.Entry(self, textvariable=tk.StringVar(), bg='pink', font=f3)  # 老師的
        self.teacher.place(x=200, y=135)  # 位置
        self.course = tk.Entry(self, textvariable=tk.StringVar(), bg='pink', font=f3)
        self.course.place(x=200, y=205)
        self.num = ttk.Combobox(self, values=["1", "2", "3", "4"], font=f3, textvariable=tk.StringVar(), state="readonly")
        self.num.place(x=200, y=270)
        self.num.current(0)
        self.arrange = ttk.Combobox(self, values=["年度", "留言數"], textvariable=tk.StringVar(), font=f3, state="readonly")
        self.arrange.place(x=200, y=340)
        self.arrange.current(0)

    def click(self):  # 點擊程序
        self.sequence['text'] = ''
        t_grade = 0
        self.output['state'] = 'normal'
        self.output.delete(1.0, "end")  # 清空所有文字
        self.output.tag_config("tag_1", backgroun="yellow", foreground="red")  # 明顯的標示
        self.output.tag_config("tag_2", backgroun="#9AFF02", foreground="mediumblue")
        if self.teacher.get().strip() == '':
            self.output.insert(1.0, '請輸入教師姓名', "tag_1")
        elif self.course.get().strip() == '':
            self.output.insert(1.0, '請輸入課堂名稱', "tag_1")
        else:
            txt = []
            
            teacher = self.teacher.get().strip()
            course = self.course.get().strip()
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
                        continue

            for pcontent in range(len(article_href)):
    #清空檔案
                PTTCOURSE_dct={}
                URL = "https://www.ptt.cc"+article_href[pcontent]
    #print(URL)
    # 發送get 請求 到 ptt course版
                response = requests.get(URL, headers=my_headers)
    #  把網頁程式碼(HTML) 丟入 bs4模組分析
                soup = BeautifulSoup(response.text, "html.parser")
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

            alldct_list = list(PTTCOURSE_alldct.values())
            lim = min(int(self.num.get()), len(alldct_list))
            if lim != int(self.num.get()):
                self.output.insert(1.0, '課程數量不足' + self.num.get(), "tag_1")
            for j in range(0, lim):
                t = alldct_list[j]
                nn = list(t.keys())
                for i in range(0, len(nn)):
                    if nn[i] != '留言':
                        s = SnowNLP(u'' + t[nn[i]])
                        txt.append(s)
                with open('魏聖倫吾皇萬福金安.txt', 'w', encoding='utf-8') as w:
                    for k in txt:
                        w.write(k.han)
                w.close()
                num = 0
                pt = 0
                with open('魏聖倫吾皇萬福金安.txt', 'r', encoding='utf-8') as w:
                    for i in w:
                        if i == '':
                            continue
                        s1 = SnowNLP(u'' + i)
                        num += 1
                        pt += float(s1.sentiments)
                w.close()
                grade = pt/num

                if grade > 0.5:
                    self.output.insert(1.0, '文章分析: 推', "tag_1")
                else:
                    self.output.insert(1.0, '文章分析: 不推', "tag_1")
                for i in range(0, len(nn)):
                    self.output.insert('end', nn[i] + '\n', "tag_2")
                    if nn[i] != '留言':
                        self.output.insert('end', t[nn[i]].strip().replace('\n\n', '\n') + '\n') # 內文從頭插入
                    else:
                        self.output.insert('end', (''.join(t[nn[i]])) + '\n') # 內文從頭插入
                self.output.insert(1.0, '完成', "tag_1")
                self.output.insert('end', "======================我是分隔線=====================", 'tag_1')
                print(grade)
                t_grade += grade
                # t_grade平均

            self.output['state'] = 'disable'
            if t_grade < 0.2:
                self.sequence['text'] = "大不推"
                self.sequence.place(x=700, y=25)  # 結果
            elif t_grade < 0.4:
                self.sequence['text'] = "不推"
                self.sequence.place(x=700, y=25)                
            elif t_grade < 0.6:
                self.sequence['text'] = "普通"
                self.sequence.place(x=700, y=25)                
            elif t_grade < 0.8:
                self.sequence['text'] = "推"
                self.sequence.place(x=700, y=25)                
            else:
                self.sequence['text'] = "大推"
                self.sequence.place(x=700, y=25)


if __name__ == "__main__":
    app = Action()
    app.mainloop()
