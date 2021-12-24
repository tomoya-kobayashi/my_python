import cv2
# from tkinter import *
import tkinter as tk
# from tkinter import ttk
import tkinter.ttk as ttk
import tkinter.filedialog
from PIL import Image,ImageTk
from skimage import io, segmentation, color


from Data import Data
from kuwahara2 import Kuwahara
from my_convert import *
from saliency import *
from segmentation import *


"""
拡張子は今後.jpegではなく.jpgで統一
透過画像を使うため、.pngのほうが都合よさそう。
変換後はすべてpngとして保存できるといい

"""


data = Data()


class Application(tkinter.Tk):
    def __init__(self):
        super().__init__()

        ### dataクラスのオブジェクトをインスタンス変数に取り込む（以降こちらを変更）
        self.data = data


        ### キャンバスのサイズ
        self.canvas_width = 400
        self.canvas_height = 400
        ### アプリのウィンドウのサイズ設定
        self.geometry("1000x430")


        # １つ目のキャンバスの作成と配置
        self.before_canvas = tk.Canvas(self, width=self.canvas_width, height=self.canvas_height, bg="black")
        self.before_canvas.grid(row=1, column=1)

        # （いずれ消す）２つ目のキャンバスの作成と配置
        self.after_canvas = tk.Canvas(self, width=self.canvas_width, height=self.canvas_height, bg="black")
        # self.after_canvas.grid(row=1, column=2)




        ### 各手法の関数と関数名リスト
        self.saliency_func_list = [itti_saliency, itti_saliency]
        self.saliency_name_list = [itti_saliency.__name__, itti_saliency.__name__]
        self.segmentation_func_list = [slic, slic_opencv]
        self.segmentation_name_list = [slic.__name__, slic_opencv.__name__]



        #############################################################################
        ### Notebook作成
        self.note = ttk.Notebook(self, height=400, width=400)

        ### Tab用フレーム作成
        self.tab1 = tk.Frame(self)
        self.tab2 = tk.Frame(self)
        self.tab3 = tk.Frame(self)
        self.tab4 = tk.Frame(self)
        self.tab5 = tk.Frame(self)
        self.tab6 = tk.Frame(self)

        ### Tab内のウィジェット作成と配置
        self.tab1_set()
        self.tab2_set()
        self.tab3_set()
        self.tab4_set()
        self.tab5_set()
        self.tab6_set()

        ### TabをNotebookに追加
        self.note.add(self.tab1, text="入力画像") 
        self.note.add(self.tab2, text="顕著性マップ") 
        self.note.add(self.tab3, text="領域分割") 
        self.note.add(self.tab4, text="領域顕著度") 
        self.note.add(self.tab5, text="塗分け") 
        self.note.add(self.tab6, text="未定") 

        ### notebookをグリッド
        self.note.grid(row=1, column=2)

        #############################################################################




        #############################################################################
        ### いずれ消すウィジェットたち

        # ボタンを配置するフレームの作成と配置
        self.button_frame = tkinter.Frame()
        self.button_frame.grid(row=1, column=3)

        # ファイル読み込みボタンの作成と配置
        self.load_button = tkinter.Button(self.button_frame, text="ファイル選択", command=self.push_load_button)
        self.load_button.pack()

        #　スケールバー1 作成と配置
        self.scale_bar1 = tkinter.Scale(self.button_frame, orient=tkinter.HORIZONTAL)
        self.scale_bar1.pack()
        #マウスを離したときにSLIC実行
        self.scale_bar1.bind("<ButtonRelease>", slic)

        #　スケールバー2 作成と配置
        self.scale_bar2 = tkinter.Scale(self.button_frame, orient=tkinter.HORIZONTAL)
        self.scale_bar2.pack()
        #  マウスを離したときに桑原フィルタ実行
        self.scale_bar2.bind("<ButtonRelease>", self.compute_Kuwahara)

        self.saliency_button = tkinter.Button(
            self.button_frame,
            text="saliency map",
            command=self.compute_saliency
        )
        self.saliency_button.pack()
        #############################################################################


        # # 画像オブジェクトの設定（初期はNone）
        # self.before_image = None
        # self.after_image = None

        # # キャンバスに描画中の画像（初期はNone）
        # self.before_canvas_obj= None
        # self.after_canvas_obj = None



        




    #############################################################################
    """【Tab1】ファイル選択ボタンが押された時の処理"""
    def push_load_button(self):
        # ファイル選択画面を表示
        self.file_path = tkinter.filedialog.askopenfilename(
            initialdir="."
        )

        if len(self.file_path) != 0:
            ###データオブジェクトに入力画像のパスを保存（本当はリサイズ後がいい）
            self.data.input_path = self.file_path
            ### 画像読み込み（jpgも扱うためPILからImageTk使用）
            image = Image.open(self.file_path)
            
            ### 最大辺を基準にキャンバスサイズの1/2に合うようリサイズ
            max_size = max([image.width, image.height])
            w_size = int(image.width*(self.canvas_height/2)/max_size)
            h_size = int(image.height*(self.canvas_height/2)/max_size)
            self.tk_image = ImageTk.PhotoImage(image=image.resize((w_size,h_size)))

            ### 読み込んだ画像をデータオブジェクトに保存（型：PIL）
            self.data.input = image

            ### 画像の描画位置を1/2キャンバス中心に調節
            x = int(self.canvas_width / 4)
            y = int(self.canvas_height / 4)

            ### キャンバスに描画中の画像を削除
            if self.tab1_canvas_obj is not None:
                self.tab1_canvas.delete(self.tab1_canvas_obj)
                print("tab1 canvas object is deleted!")

            ### 画像をキャンバスに描画
            self.tab1_canvas_obj = self.tab1_canvas.create_image(x, y, image=self.tk_image)

    #############################################################################





    #############################################################################     
    """【Tab2】プルダウン選択時の関数＆更新ボタン"""
    def compute_saliency(self, event):
        """
        １：プルダウン（saliency_combobox）のindex_numberを取得
        ２：該当する関数をsaliency_func_listから取得し、入力画像（データオブジェクトの中はImageTkだが大丈夫か？）に適用
        ３：出力画像をデータオブジェクトに保存
        ４：データオブジェクトから参照しキャンバスに貼り付け
        """
        ### 1 : index取得　関数取得
        index = self.saliency_combobox.current()
        func = self.saliency_func_list[index]
        print(index, func.__name__)

        ### 2 : 入力に合わせ型変換　該当する関数で顕著度計算
        image_cv2 = pil_to_cv2(self.data.input)
        out = func(image_cv2)

        ### 3 : 出力画像をデータオブジェクトに保存（PIL型にしてから）
        self.data.saliency = cv2_to_pil(out)
        
        ### 4 : ローカル変数imageに保存し、リサイズなどしてキャンバス貼り付け
        image = self.data.saliency
        ### 最大辺を基準にキャンバスサイズの1/2に合うようリサイズ
        max_size = max([image.width, image.height])
        w_size = int(image.width*(self.canvas_height/2)/max_size)
        h_size = int(image.height*(self.canvas_height/2)/max_size)
        self.tk_image = ImageTk.PhotoImage(image=image.resize((w_size,h_size)))
        ### 画像の描画位置を1/2キャンバス中心に調節
        x = int(self.canvas_width / 4)
        y = int(self.canvas_height / 4)
        ### キャンバスに描画中の画像を削除
        if self.tab2_canvas_obj is not None:
            self.tab2_canvas.delete(self.tab2_canvas_obj)
            print("tab2 canvas object is deleted!")
        ### 画像をキャンバスに描画
        self.tab2_canvas_obj = self.tab2_canvas.create_image(x, y, image=self.tk_image)
    #############################################################################






    #############################################################################
    def compute_segmentation(self, event):
        """
        １：プルダウン（segmentation_combobox）からindex numberを取得
        ２：スケールバーからパラメタを取得
        ３：該当する関数をsegmentation_func_listから取得し、パラメタ値も含め入力画像に適用
        ４：出力画像をデータオブジェクトに保存
        ５：データオブジェクトから参照しキャンバス貼り付け
        """
        ### 1 : index取得　関数取得
        index = self.segmentation_combobox.current()
        func = self.segmentation_func_list[index]
        print(index, func.__name__)
        ### 2 : スケールバーの値（パラメタ）取得
        parameter = self.scale_bar_tab3.get()
        ### 3 : 入力に合わせ型変換　該当する関数で領域分割
        image_cv2 = pil_to_cv2(self.data.input)
        out = func(image_cv2, parameter)
        ### 4 : ローカル変数imageに保存し、リサイズなどしてキャンバス貼り付け
        self.data.segmentation = cv2_to_pil(out)
        image = self.data.segmentation
        ### 最大辺を基準にキャンバスサイズの1/2に合うようリサイズ
        max_size = max([image.width, image.height])
        w_size = int(image.width*(self.canvas_height/2)/max_size)
        h_size = int(image.height*(self.canvas_height/2)/max_size)
        self.tk_image = ImageTk.PhotoImage(image=image.resize((w_size,h_size)))
        ### 画像の描画位置を1/2キャンバス中心に調節
        x = int(self.canvas_width / 4)
        y = int(self.canvas_height / 4)
        ### キャンバスに描画中の画像を削除
        if self.tab3_canvas_obj is not None:
            self.tab3_canvas.delete(self.tab3_canvas_obj)
            print("tab3 canvas object is deleted!")
        ### 画像をキャンバスに描画
        self.tab3_canvas_obj = self.tab3_canvas.create_image(x, y, image=self.tk_image)

        pass
        # #スケールバーから値を取得
        # a = self.scale_bar1.get()

        # image = io.imread(self.file_path)
        # label = segmentation.slic(image, compactness=a, start_label=1)
        # self.slic_out = color.label2rgb(label, image, kind = 'avg', bg_label=0)

 
        # # 画像保存
        # io.imsave("C:\\Users\\mieli\\my_python\\img\\cat1_slic.jpeg", self.slic_out)

        # # 画像の描画位置を調節
        # x = int(self.canvas_width / 2)
        # y = int(self.canvas_height / 2)

        # #画像削除
        # if self.after_canvas_obj is not None:
        #     self.after_canvas.delete(self.after_canvas_obj)

        # image = Image.open("C:\\Users\\mieli\\my_python\\img\\cat1_slic.jpeg")
        # w_size = int(image.width/4)
        # h_size = int(image.height/4)
        # tk_image = ImageTk.PhotoImage(image=image.resize((w_size,h_size)))
        # self.after_image = tk_image

        # # 画像を2つ目のキャンバスに描画
        # self.after_canvas_obj = self.after_canvas.create_image(
        #     x, y,
        #     image=self.after_image
        # )
    #############################################################################      





    def compute_Kuwahara(self, event):
        a = self.scale_bar2.get()

        img = cv2.imread(self.file_path)

        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        out = Kuwahara(img_rgb,a,True,0.5)

        io.imsave("C:\\Users\\mieli\\my_python\\img\\kuwahara_out.jpeg", out)

        # 画像の描画位置を調節
        x = int(self.canvas_width / 2)
        y = int(self.canvas_height / 2)

        #画像削除
        if self.after_canvas_obj is not None:
            self.after_canvas.delete(self.after_canvas_obj)

        image = Image.open("C:\\Users\\mieli\\my_python\\img\\kuwahara_out.jpeg")
        w_size = int(image.width/4)
        h_size = int(image.height/4)
        tk_image = ImageTk.PhotoImage(image=image.resize((w_size,h_size)))
        self.after_image = tk_image

        # 画像を2つ目のキャンバスに描画
        self.after_canvas_obj = self.after_canvas.create_image(
            x, y,
            image=self.after_image
        )


    def test(self, event):
        a = self.scale_bar.get()
        print(a)

    def getNoteName(self,event):
        note =event.widget
        self.label["text"]=note.tab(note.select(),"text")








    #################################################################################
    ### Tabたち

    """Tab1のウィジェット作成関数【入力画像】"""
    def tab1_set(self):
        ### ファイル読み込みボタンの作成と配置
        self.load_button = tk.Button(self.tab1, text="ファイル選択", command=self.push_load_button)
        self.load_button.pack()

        ### 入力画像表示用キャンバス
        self.tab1_canvas = tk.Canvas(self.tab1, width=self.canvas_width/2, height=self.canvas_height/2, bg="black")
        self.tab1_canvas.pack()
        # 画像オブジェクトの設定（初期はNone）⇒これ使う？
        self.tab1_image = None
        ### キャンバスに描画中の画像（初期はNone）
        self.tab1_canvas_obj= None



    """Tab2のウィジェット作成関数【顕著性マップ】"""
    def tab2_set(self):
        ### comboboxのオブジェクト生成　リスト指定
        self.saliency_combobox = ttk.Combobox(self.tab2, values=self.saliency_name_list)
        ### comboboxの貼り付け
        self.saliency_combobox.pack()
        ### comboboxの初期値設定変更（index=1が初期値）
        # self.saliency_combobox.current(0)
        ### 【重要】プルダウン選択時に呼び出す関数をバインド
        self.saliency_combobox.bind("<<ComboboxSelected>>", self.compute_saliency)


        ### 入力画像表示用キャンバス
        self.tab2_canvas = tk.Canvas(self.tab2, width=self.canvas_width/2, height=self.canvas_height/2, bg="black")
        self.tab2_canvas.pack()
        # 画像オブジェクトの設定（初期はNone）⇒これ使う？
        self.tab2_image = None
        ### キャンバスに描画中の画像（初期はNone）
        self.tab2_canvas_obj= None



    """Tab3のウィジェット作成関数【領域分割】"""
    def tab3_set(self):
        ### comboboxのオブジェクト生成　リスト指定
        self.segmentation_combobox = ttk.Combobox(self.tab3, values=self.segmentation_name_list)
        ### comboboxの貼り付け
        self.segmentation_combobox.pack()
        ### comboboxの初期値設定変更（index=1が初期値）
        # self.saliency_combobox.current(0)
        ### 【重要】プルダウン選択時に呼び出す関数をバインド
        self.segmentation_combobox.bind("<<ComboboxSelected>>", self.compute_segmentation)


        ### 入力画像表示用キャンバス
        self.tab3_canvas = tk.Canvas(self.tab3, width=self.canvas_width/2, height=self.canvas_height/2, bg="black")
        self.tab3_canvas.pack()
        # 画像オブジェクトの設定（初期はNone）⇒これ使う？
        self.tab3_image = None
        ### キャンバスに描画中の画像（初期はNone）
        self.tab3_canvas_obj= None

        ### スケールバー 作成と配置
        self.scale_bar_tab3 = tk.Scale(self.tab3, orient=tkinter.HORIZONTAL, from_=0, to=200, variable=100)
        self.scale_bar_tab3.set(100)
        self.scale_bar_tab3.pack()
        #マウスを離したときにcompute_segmentation実行
        self.scale_bar_tab3.bind("<ButtonRelease>", self.compute_segmentation)

    
    """Tab4のウィジェット作成関数【領域顕著度】"""
    def tab4_set(self):
        pass

    
    """Tab5のウィジェット作成関数【塗分け】"""
    def tab5_set(self):
        pass

    
    """Tab6のウィジェット作成関数【未定】"""
    def tab6_set(self):
        pass



    """いらないかも"""
    def save(self):
        global data
        data = self.data


    #################################################################################



app = Application()

app.mainloop()