import tkinter as tk
import tkinter.font as tkFont
from functools import partial
from tkinter import ttk

class Action(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.grid()
        self.master.geometry('1300x600')
        self.master.minsize(1300, 600)
        self.master.maxsize(1300, 600)
        self.master.title('聖倫吾皇萬福金安')
        self.createWidgets()

    def createWidgets(self):
        f1 = tkFont.Font(size=30, family="Courier New")
        f2 = tkFont.Font(size=25, family="Courier New")
        f3 = tkFont.Font(size=20, family="Courier New")
        f4 = tkFont.Font(size=16, family="Courier New")
        # 背景
        self.background = tk.Canvas(self, height=600, width=1300, bg='white').pack()
        # 文字
        self.output = tk.Text(self, width=52, height=22, font=f4, bg='#4DFFFF')
        self.output.place(x=600, y=75)
        # 按鈕
        self.start = tk.Button(self, text="開始", height=1, width=4, bg='#ffcc00', font=f3, command=self.click).place(x=250, y=400)
        self.intro = tk.Button(self, text="1.輸入教師名稱\n2.輸入課程名稱\n3.選擇排序和數量\n4.點擊開始", width=40, bg='white', font=f4, state='disable').place(x=32, y=20)
        # 標題
        self.concequence = tk.Label(self, text="結果:", height=1, width=5, bg='white', font=f2).place(x=590, y=25)
        self.arrange_label = tk.Label(self, text="排序方式:", height=1, width=10, bg='white', font=f2).place(x=17, y=340)
        self.course_label = tk.Label(self, text="教師:", height=1, width=5, bg='white', font=f2).place(x=100, y=130)
        self.teacher_label = tk.Label(self, text="課程:", height=1, width=5, bg='white', font=f2).place(x=100, y=200)
        self.num_label = tk.Label(self, text="資料數量:", height=1, width=10, bg='white', font=f2).place(x=17, y=270)
        # 輸入
        self.teacher =  tk.Entry(self, textvariable=tk.StringVar(), bg='pink', font=f3).place(x=200, y=135)
        self.course =  tk.Entry(self, textvariable=tk.StringVar(), bg='pink', font=f3).place(x=200, y=205)
        self.num = ttk.Combobox(self, state="readonly").place(x=200, y=270)
        self.num['values'] = ["1", "2", "3", "4", '5', '6']
        self.arrange = ttk.Combobox(self, values=["年度", "留言數"], font=f3, state="readonly").place(x=200, y=340)

    def click(self):
        self.output.delete(1.0, "end")
        self.output.tag_config("tag_1", backgroun="yellow", foreground="red")
        if self.num is None:
            self.output.insert(1.0, '請選擇資料數量', "tag_1")
        elif self.arrange is None:
            self.output.insert(1.0, '請選擇排序方式', "tag_1")
        else:
            self.output.insert(1.0, '載入中....\n', "tag_1")
            self.output.insert(2.0, 'jojo\n') # 內文從頭插入
            self.output.insert(2.0, '666\n') # 內文從頭插入
            self.output.delete(1.0, 1.8)
            self.output.insert(1.0, '完成', "tag_1")


if __name__ == "__main__":
    app = Action()
    app.mainloop()
