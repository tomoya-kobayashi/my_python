import tkinter as tk
from tkinter import ttk



### テスト用クラス　Test & Data
class Test():
    def __init__(self):
        self.func = self.add

    def add(self, a, b):
        return a+b

class Data():
    def __init__(self, t):
        self.dict_paint_1 = {'effect':self.func1, 'size':3}
        self.func = t.add

    def func1(self):
        print("in func1 !!")

    def func2(self):
        print("in func2 !!")



t = Test()
data = Data(t)


### combobox選択時に呼び出す関数
def callbackFunc(event):
    index = comboExample.current()
    current_func = func_list[comboExample.current()]
    print(index, current_func.__name__)
    current_func()


### tkinter 初期設定
app = tk.Tk() 
app.geometry('500x500')
labelTop = tk.Label(app, text = "Choose your favourite month")
labelTop.grid(column=0, row=0)


### 【重要】プルダウンのインデックスから参照して関数を使うためのリスト
func_list = [data.func1, data.func2]

### 【重要】プルダウンに渡す関数名リスト
func_list_name = [data.func1.__name__, data.func2.__name__]

### 【重要】comboboxのオブジェクト生成　リスト指定
comboExample = ttk.Combobox(app, values=func_list_name)

### combpbpxの貼り付け
comboExample.grid(column=0, row=1)

### comboboxの初期値設定変更（index=1が初期値）
comboExample.current(1)

### 【重要】プルダウン選択時に呼び出す関数をバインド
comboExample.bind("<<ComboboxSelected>>", callbackFunc)




app.mainloop()
