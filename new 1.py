import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk
from snownlp import SnowNLP
import time
from bs4 import BeautifulSoup
import requests
import os

t = ('哪一學年度修課：\n'
'        108-1\n'

'      ψ 授課教師 (若為多人合授請寫開課教師，以方便收錄)\n'
'        蔡忠潤、陳世昕助教\n'

'      λ 開課系所與授課對象 (是否為必修或通識課 / 內容是否與某些背景相關)\n'
'        國企系、工管系、會計系、財金系、地理系 必修\n'

'      δ 課程大概內容\n'
'        積分(定積分、不定積分、分部積分、瑕積分......)\n'

'      Ω 私心推薦指數(以五分計) ★★★★★\n'
'        ★★★★★，老師笑起來超可愛又教得很清楚\n'
'        助教更是超級用心！！(給助教的★加到爆)\n'
'        不過俗話說的好，微積分三分靠老師，兩分靠天意，\n'
'        剩下的還是要靠自己苦讀啊......\n'

'      η 上課用書(影印講義或是指定教科書)\n'
'        James Stewart, Calculus Early Transcendentals, 8th edition.\n'
'        不過跟第7版基本上長的一模模一樣樣，\n'
'        所以直接用上一版的電子檔上課準沒問題XD\n'

'      μ 上課方式(投影片、團體討論、老師教學風格)\n'
'        教授大多英文版書，中文授課，口條清晰，\n'
'        但老師的手速真的快到爆炸......\n'
'        板書絕對要快速抄下(不過可以趁老師在解釋算式時補上，所以也還行XD)\n'
'        最重要的是教授人超可愛的！！！\n'
'        每次在被微積分Ｋ個殘花敗柳的時候，\n'
'        看著教授對著數學式子笑了笑就覺得好療癒(≧▽≦)/！！(敲碗)\n'

'        而陳世昕助教也教得超好！\n'
'        我每次在考前都和同學抱佛腳(真的建議大家不要把問題卡到最後TT)，\n'
'        帶著一堆問題纏著助教，害助教不能好好吃飯快點回家，\n'
'        但助教都很友善、教得又很仔細！\n'
'        真的覺得是佛陀轉世啊~~~~\n'

'        想當年108-2時，我修到兩個教得不太好的教授開的微積分3和4(有夠悲催)，\n'
'        真的幸好有世昕助教幫忙撐起來><......！\n'
'        所以本人認真覺得，遇到一個不好的教授絕對不要氣餒，\n'
'        因為一個好的助教絕對是幫助你微積分pass的關鍵！\n'

'        所以我大推陳世昕助教！\n'
'        希望他之後可以快快升成教授，造福後代無數被微積分摧殘的子孫啊！！\n'

'        (不過每次助教在的班級都不一定，建議大家到以下網址看看助教在哪上課唷：\n'
'        http://www.math.ntu.edu.tw/~calc/cp_n_34652.html)\n'

'      σ 評分方式(給分甜嗎？是紮實分？)\n'
'        期考            50% (統一教學考試)\n'
'        小考            20% 兩次(各班獨立)\n'
'        紙本作業        20% 四次\n'
'        WebWork         10%\n'

'      ρ 考題型式、作業方式\n'
'        請看微積分統一教學網唷~~\n'
'        http://www.math.ntu.edu.tw/~calc/Default.html\n'

'      ω 其它(是否注重出席率？如果為外系選修，需先有什麼基礎較好嗎？老師個性？\n'
'              加簽習慣？嚴禁遲到等…)\n'
'        不點名，但因為課程是環環相扣的，翹一節必死^^\n'

'      Ψ 總結\n')



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
        self.output['state'] = 'normal'
        self.output.delete(1.0, "end")  # 清空所有文字
        self.output.tag_config("tag_1", backgroun="yellow", foreground="red")  # 明顯的標示
        self.output.tag_config("tag_2", backgroun="#9AFF02", foreground="mediumblue")
        if self.num.get() is None:
            self.output.insert(1.0, '請選擇資料數量', "tag_1")
        elif self.arrange.get() is None:
            self.output.insert(1.0, '請選擇排序方式', "tag_1")
        elif self.teacher.get().strip() == '':
            self.output.insert(1.0, '請輸入教師姓名', "tag_1")
        elif self.course.get().strip() == '':
            self.output.insert(1.0, '請輸入課堂名稱', "tag_1")
        else:
            self.output.insert(1.0, '載入中....\n', "tag_1")
            self.output.insert('end', self.course.get().strip() + self.teacher.get().strip() + '\n', 'tag_2')

            s = SnowNLP(u'' + t)
            with open('C:/Users/RRR/Desktop/新文字文件.txt', 'w', encoding='utf-8') as w:
                w.write(s.han)
            w.close()
            num = 0
            pt = 0
            with open('C:/Users/RRR/Desktop/新文字文件.txt', 'r', encoding='utf-8') as w:
                for i in w:
                    s1 = SnowNLP(u'' + i)
                    num += 1
                    pt += float(s1.sentiments)
            w.close()
            grade = pt/num

            self.output.insert('end', t) # 內文從頭插入
            self.output.delete(1.0, 1.8)
            if grade > 0.5:
                self.output.insert(1.0, '課程分析: 推', "tag_1")
            else:
                self.output.insert(1.0, '課程分析: 不推', "tag_1")
            self.output.insert(1.0, '完成\n', "tag_1")
            self.output['state'] = 'disable'


if __name__ == "__main__":
    app = Action()
    app.mainloop()
