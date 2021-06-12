import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk
from snownlp import SnowNLP
import time
from bs4 import BeautifulSoup
import requests
import os

t = {"哪一學年度修課：":"109-1","ψ 授課教師 (若為多人合授請寫開課教師，以方便收錄)":"楊典錕",
        "λ 開課系所與授課對象 (是否為必修或通識課 / 內容是否與某些背景相關)":"歷史系選修。",
        "δ 課程大概內容":"想講什麼就講什麼，大綱只會在第一周出現",
        "Ω 私心推薦指數(以五分計) ★★★★★":"★★★★★ 無需贅言",
        "η 上課用書(影印講義或是指定教科書)":"手寫精美板書，密密麻麻一整片黑板\n有一本日本近代史，但不用買",
        "μ 上課方式(投影片、團體討論、老師教學風格)":"佈道三小時上好上滿\n慷慨激昂的講課還有政治傾向也不用多提\n但那學期被寄去的信件激怒兩次，寄信詢問記得不要下指導棋，也不要抱怨課程問題\n不然除了台語老歌以外，會接受到滿滿的暴怒",
        "σ 評分方式(給分甜嗎？是紮實分？)":'''100%期末考定生死
蠻甜的，板書全部背下來就可以考試了
而且是14選4，可以選自己擅長的題目作答
A+比率32%
''',
        "ρ 考題型式、作業方式":"寫在上面了",
        "ω 其它(是否注重出席率？如果為外系選修，需先有什麼基礎較好嗎？老師個性？\n加簽習慣？嚴禁遲到等…)":'''原本不點名，但大概第三還第四周，缺席率太嚴重，導致之後幾乎每周都點
加簽全簽 不須基礎
這堂課的好處是只需看板書就可以應考，也不會像日近人一樣加課
但不會晚下課是相對而言，通常還是會晚十五到二十分鐘
然後學期評鑑不會有任何作用，可以不用浪費時間填寫了，老師明言不會看
所以有什麼想寫的可以寫在期末考最後一題，直接送25分
以後看到老師臉很臭走進來 有可能跟這學期一樣 有論文要趕
這時候千萬不要講話 前後幾週也不要寄信 否則會被瘋狂暴怒''',
        "Ψ 總結":'''千萬不要寄信詢問老師為什麼都在講課外的東西，老師真的會爆氣，也不要干涉上課教法
期末考也不要寫太多
否則這學期的悲劇會重演，未來要修的人耗子尾汁
但大概是歷史系世界史群組最好過的課
有需求的人可以考慮

--
推 kfclikeshit:麻美有漏打馬賽克的片段 ○還挺美的                   01/06 18:49
→ TwinzLewis:真想知道麻美那部漏打馬賽克的是哪部!!!???             01/06 20:25
→ TwinzLewis:請問肯德基像屎大大!!!                                01/06 20:26
→ kfclikeshit:另外我是kfc likes hit 是指它的雞肉經過許多敲打很韌  01/07 13:03
→ kfclikeshit:很好吃 別誤解意思了 感恩                            01/07 13:04

--''',
        "文章網址:":"https://www.ptt.cc/bbs/NTUcourse/M.1618991632.A.5AF.html",
        "留言":""}



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
        self.intro = tk.Button(self, text="1.輸入教師名稱\n2.輸入課程名稱\n3.選擇資料數量和排序方式\n4.點擊開始", width=40, bg='orange', font=f4, state='disable').place(x=32, y=20)
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
        self.num = ttk.Combobox(self, values=["1", "2", "3", "4", '5', '6'], font=f3, textvariable=tk.StringVar(), state="readonly")
        self.num.place(x=200, y=270)
        self.num.current(0)
        self.arrange = ttk.Combobox(self, values=["年度", "留言數"], font=f3, state="readonly")
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
            self.output.insert(1.0, '載入中....\n', "tag_1")
            txt = []
            for i in t.keys():
                if t[i] != '':
                    s = SnowNLP(u'' + t[i])
                    txt.append(s)
            with open('魏聖倫吾皇萬福金安.txt', 'w', encoding='utf-8') as w:
                for i in txt:
                    w.write(i.han)
            w.close()
            num = 0
            pt = 0
            with open('魏聖倫吾皇萬福金安.txt', 'r', encoding='utf-8') as w:
                for i in w:
                    s1 = SnowNLP(u'' + i)
                    num += 1
                    pt += float(s1.sentiments)
            w.close()
            grade = pt/num

            nn = list(t.keys())
            for i in range(0, len(nn)):
                self.output.insert('end', nn[i] + '\n', "tag_2")
                self.output.insert('end', t[nn[i]] + '\n') # 內文從頭插入
            self.output.delete(1.0, 1.8)
            if grade > 0.5:
                self.output.insert(1.0, '課程分析: 推', "tag_1")
            else:
                self.output.insert(1.0, '課程分析: 不推', "tag_1")
            self.output.insert(1.0, '完成', "tag_1")
            self.output.insert('end', "======================我是分隔線=====================", 'tag_1')
            self.output['state'] = 'disable'
            print(grade)

            t_grade += grade
            # t_grade平均
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
