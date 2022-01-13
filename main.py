import cv2
# from tkinter import *
import tkinter as tk
# from tkinter import ttk
import tkinter.ttk as ttk
import tkinter.filedialog
from PIL import Image,ImageTk, ImageDraw
from skimage import io, segmentation, color
import glob
import os.path

from Data import Data
from config import Config
from kuwahara2 import Kuwahara
from my_convert import *
from saliency import *
from segmentation import *
from paint import *
from normal_distribution import *



tk_images = []
config_dict_list = []
### configフォルダ内のjsonファイルを全て呼び出し，configリストに保存．
###（後にプルダウンに表示される）
for f in glob.glob("config\\*.json"):
    config_dict_list.append(os.path.basename(f)[0:-5])
config_index = 0
print(config_dict_list)




class Application(tkinter.Tk):
    def __init__(self):
        super().__init__()

        global tk_images
        global config_dict_list
        global config_index
        self.config = Config()


        ### カラーリスト
        self.colors = []
        self.colors.append("#E0ECF8")
        self.colors.append("#002B40")
        self.colors.append("#3F83A6")
        self.colors.append("#D9E9E5")
        self.colors.append("#6CB2D3")
        self.colors.append("#1D4B69")
        self.colors.append("#B1C7D4")
        self.colors.append("#F4F2DB")
        self.colors.append("#94A1A9")
        self.colors.append("#424F56")

        ### 【色の変更はここ】パーツの色を設定
        self.tab_color = self.colors[3]
        self.window_color = "#fdfdfd"
        self.button_color = self.colors[5]


        ### キャンバスのサイズ
        self.canvas_width = 600
        self.canvas_height = 600
        ### アプリのウィンドウのサイズ設定
        self.geometry("1200x700")
        ### windowの色変更
        self.configure(bg=self.window_color)


        # １つ目のキャンバスの作成と配置
        self.out_canvas = tk.Canvas(self, width=self.canvas_width, height=self.canvas_height, bg="black")
        self.out_canvas.grid(row=1, column=1)
        # 画像オブジェクトの設定（初期はNone）⇒これ使う？
        self.out_image = None
        ### キャンバスに描画中の画像（初期はNone）
        self.out_canvas_obj= None



        ### 各手法の関数と関数名リスト
        self.saliency_func_list = [Hou_saliency, Hou_saliency]
        self.saliency_name_list = [Hou_saliency.__name__, Hou_saliency.__name__]
        self.segmentation_func_list = [slic, slic_opencv]
        self.segmentation_name_list = [slic.__name__, slic_opencv.__name__]
        self.paint_func_list = [kuwahara, watercolor, pencil, Gaussian, flat, oilpaint, watercolor_reformed]
        self.paint_name_list = [
            "油彩１:{}".format(kuwahara.__name__),
            "水彩:{}".format(watercolor.__name__), 
            "鉛筆:{}".format(pencil.__name__),
            "ガウスぼかし:{}".format(Gaussian.__name__),
            "フラット塗り:{}".format(flat.__name__),
            "油彩２:{}".format(oilpaint.__name__),
            "水彩２:{}".format(watercolor_reformed.__name__)

        ]
        

        #############################################################################
        ### Notebook作成
        self.note = ttk.Notebook(self, height=578, width=600)
        
        ### Tab用フレーム作成
        self.tab1 = tk.Frame(self, background=self.tab_color)
        self.tab2 = tk.Frame(self, background=self.tab_color)
        self.tab3 = tk.Frame(self, background=self.tab_color)
        self.tab4 = tk.Frame(self, background=self.tab_color)
        self.tab5 = tk.Frame(self, background=self.tab_color)
        self.tab6 = tk.Frame(self, background=self.tab_color)


        ### Tab内のウィジェット作成と配置
        self.tab1_set()
        self.tab2_set()
        self.tab3_set()
        self.tab4_set()
        self.tab5_set()
        # self.tab6_set()

        ### TabをNotebookに追加
        self.note.add(self.tab1, text="入力画像") 
        self.note.add(self.tab2, text="顕著性マップ") 
        self.note.add(self.tab3, text="領域分割") 
        self.note.add(self.tab4, text="領域顕著度") 
        self.note.add(self.tab5, text="塗分け") 
        # self.note.add(self.tab6, text="未定") 

        ### notebookをグリッド
        self.note.grid(row=1, column=2)
        #############################################################################




        # ボタンを配置するフレームの作成と配置
        self.button_frame1 = tkinter.Frame(width=self.canvas_width, height=35, bg=self.window_color)
        self.button_frame1.grid(row=2, column=1)
        # ボタンを配置するフレームの作成と配置
        self.button_frame2 = tkinter.Frame(width=self.canvas_width, height=35, bg=self.window_color)
        self.button_frame2.grid(row=2, column=2)
        # ラベルを配置するフレームの作成と配置
        self.label_frame1 = tkinter.Frame(width=self.canvas_width, height=70, bg=self.window_color)
        self.label_frame1.grid(row=3, column=1)
        # ラベルを配置するフレームの作成と配置
        self.label_frame2 = tkinter.Frame(width=self.canvas_width, height=70, bg=self.window_color)
        self.label_frame2.grid(row=3, column=2)
        
        
        # レイヤ合成ボタンの作成と配置
        self.synthesize_button = tkinter.Button(
            self.button_frame1, 
            text="合成", 
            command=self.synthesize_layers,
            #bg=self.button_color
        )
        # self.synthesize_button.grid(row=2, column=1)
        self.synthesize_button.place(x=260, y=5)

        # 名前を付けて保存ボタン作成と配置
        self.save_as_button = tkinter.Button(self.button_frame1, text="名前を付けて保存", command=self.save_as)
        self.save_as_button.place(x=300, y=5)

        # 設定保存ボタンの作成と配置
        self.save_config_button = tkinter.Button(self.button_frame2, text="設定保存", command=self.save_config)
        self.save_config_button.place(x=100, y=5)

        ### comboboxのオブジェクト生成　リスト指定
        self.config_combobox = ttk.Combobox(self.button_frame2, values=config_dict_list)
        ### comboboxの貼り付け
        self.config_combobox.place(x=200, y=5)
        ### comboboxの初期値設定変更（index=1が初期値）
        self.config_combobox.current(0)
        ### 【重要】プルダウン選択時に呼び出す関数をバインド
        self.config_combobox.bind("<<ComboboxSelected>>", self.pre_compute_all)

        # おまかせボタンの作成と配置
        self.default_button = tkinter.Button(self.button_frame2, text="おまかせ", command=self.compute_all)
        self.default_button.place(x=380, y=5)


        ### パラメタ表示用ラベルの文字列を入れる変数の辞書
        self.label_dict = dict()
        self.label_dict['name']                            = tk.StringVar()
        self.label_dict['saliency_func_index']             = tk.StringVar()
        self.label_dict['segmentation_func_index']         = tk.StringVar()
        self.label_dict['segmentation_k']                  = tk.StringVar()
        self.label_dict['segmentation_saliency_threshold'] = tk.StringVar()
        self.label_dict['paint1_func_index']               = tk.StringVar()
        self.label_dict['paint1_func_parameter']           = tk.StringVar()
        self.label_dict['paint2_func_index']               = tk.StringVar()
        self.label_dict['paint2_func_parameter']           = tk.StringVar()
        
        ### ラベルの文字列を入れる変数の辞書に，現在のパラメタを代入
        param_dict = self.config.get_dict()
        self.label_dict['name'].set("名前："+str(param_dict['name']))
        self.label_dict['saliency_func_index'].set("顕著性マップ："+str(param_dict['saliency_func_index']))
        self.label_dict['segmentation_func_index'].set("領域分割："+str(param_dict['segmentation_func_index']))
        self.label_dict['segmentation_k'].set("分割数："+str(param_dict['segmentation_k']))
        self.label_dict['segmentation_saliency_threshold'].set("領域顕著度_閾値："+str(param_dict['segmentation_saliency_threshold']))
        self.label_dict['paint1_func_index'].set("画材１："+str(param_dict['paint1_func_index']))
        self.label_dict['paint1_func_parameter'].set("画材１_param："+str(param_dict['paint1_func_parameter']))
        self.label_dict['paint2_func_index'].set("画材２："+str(param_dict['paint2_func_index']))         
        self.label_dict['paint2_func_parameter'].set("画材２_param："+str(param_dict['paint2_func_parameter']))

        ### ラベル作成
        self.label_name                            = tk.ttk.Label(self.label_frame2, textvariable=self.label_dict['name'])
        self.label_saliency_func_index             = tk.ttk.Label(self.label_frame2, textvariable=self.label_dict['saliency_func_index'])
        self.label_segmentation_func_index         = tk.ttk.Label(self.label_frame2, textvariable=self.label_dict['segmentation_func_index'])
        self.label_segmentation_k                  = tk.ttk.Label(self.label_frame2, textvariable=self.label_dict['segmentation_k'])
        self.label_segmentation_saliency_threshold = tk.ttk.Label(self.label_frame2, textvariable=self.label_dict['segmentation_saliency_threshold'])
        self.label_paint1_func_index               = tk.ttk.Label(self.label_frame2, textvariable=self.label_dict['paint1_func_index'])
        self.label_paint1_func_parameter           = tk.ttk.Label(self.label_frame2, textvariable=self.label_dict['paint1_func_parameter'])
        self.label_paint2_func_index               = tk.ttk.Label(self.label_frame2, textvariable=self.label_dict['paint2_func_index'])
        self.label_paint2_func_parameter           = tk.ttk.Label(self.label_frame2, textvariable=self.label_dict['paint2_func_parameter'])

        ### ラベル配置
        self.label_name.grid(row=0, column=0)
        self.label_saliency_func_index.grid(row=0, column=1)
        self.label_segmentation_func_index.grid(row=0, column=2)
        self.label_segmentation_k.grid(row=1, column=0)
        self.label_segmentation_saliency_threshold.grid(row=1, column=1)
        self.label_paint1_func_index.grid(row=1, column=2)
        self.label_paint1_func_parameter.grid(row=1, column=3)
        self.label_paint2_func_index.grid(row=1, column=4)
        self.label_paint2_func_parameter.grid(row=1, column=5)
    
    ### ラベル更新関数．パラメタ更新する度これを実行（？）
    def update_label(self):
        param_dict = self.config.get_dict()
        self.label_dict['name'].set("名前："+str(param_dict['name']))
        self.label_dict['saliency_func_index'].set("顕著性マップ："+str(param_dict['saliency_func_index']))
        self.label_dict['segmentation_func_index'].set("領域分割："+str(param_dict['segmentation_func_index']))
        self.label_dict['segmentation_k'].set("分割数："+str(param_dict['segmentation_k']))
        self.label_dict['segmentation_saliency_threshold'].set("領域顕著度_閾値："+str(param_dict['segmentation_saliency_threshold']))
        self.label_dict['paint1_func_index'].set("画材１："+str(param_dict['paint1_func_index']))
        self.label_dict['paint1_func_parameter'].set("画材１_param："+str(param_dict['paint1_func_parameter']))
        self.label_dict['paint2_func_index'].set("画材２："+str(param_dict['paint2_func_index']))         
        self.label_dict['paint2_func_parameter'].set("画材２_param："+str(param_dict['paint2_func_parameter']))



    #############################################################################
    """【Tab1】ファイル選択ボタンが押された時の処理"""
    def push_load_button(self):

        # ファイル選択画面を表示
        self.file_path = tkinter.filedialog.askopenfilename(
            initialdir="."
        )

        if len(self.file_path) != 0:
            ### 画像読み込み（jpgも扱うためPILからImageTk使用）
            image = Image.open(self.file_path)
            
            ### 最大辺を基準にキャンバスサイズの1/2に合うようリサイズ
            max_size = max([image.width, image.height])
            w_size = int(image.width*(self.canvas_height/2)/max_size)
            h_size = int(image.height*(self.canvas_height/2)/max_size)
            self.tk_image = ImageTk.PhotoImage(image=image.resize((w_size,h_size)))
            ### グローバル変数のリストに保存（キャンバスに画像保持）
            tk_images.append(self.tk_image)

            w_resize = int(image.width*500/max_size)
            h_resize = int(image.height*500/max_size)
            image_resize = image.resize((w_resize, h_resize))
            self.file_path = "img\\input.jpeg"
            image_resize.save(self.file_path)

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
    def pre_compute_saliency(self, event):
        ###１：プルダウン（saliency_combobox）のindex_numberを取得
        self.config.saliency_func_index = self.saliency_combobox.current()
        self.compute_saliency()

    """【Tab2】プルダウン選択時の関数＆更新ボタン"""
    def compute_saliency(self):
        """     
        ２：該当する関数をsaliency_func_listから取得し、入力画像（データオブジェクトの中はImageTkだが大丈夫か？）に適用
        ３：出力画像をデータオブジェクトに保存
        ４：データオブジェクトから参照しキャンバスに貼り付け
        """
        ### 1 : index取得　関数取得
        # index = self.saliency_combobox.current()
        index = self.config.saliency_func_index
        func = self.saliency_func_list[index]
        print(index, func.__name__)

        ### 2 : 該当する関数で顕著度計算
        image_cv2 = cv2.imread(self.file_path)
        out = func(image_cv2)

        ### 3.5 : 画像として一度保存　パスをself.saliency_pathに保存
        self.saliency_path = "img\\saliency.jpeg"
        io.imsave(self.saliency_path, out)
        
        ### 4.5 : 保存してあった顕著性マップをpilで読み込み
        image = Image.open(self.saliency_path)

        ### 最大辺を基準にキャンバスサイズの1/2に合うようリサイズ
        max_size = max([image.width, image.height])
        w_size = int(image.width*(self.canvas_height/2)/max_size)
        h_size = int(image.height*(self.canvas_height/2)/max_size)
        self.tk_image = ImageTk.PhotoImage(image=image.resize((w_size,h_size)))

        ### グローバル変数のリストに保存（キャンバスに画像保持）
        tk_images.append(self.tk_image)

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
    def pre1_compute_segmentation(self, event):
        self.config.segmentation_func_index = self.segmentation_combobox.current()
        self.compute_segmentation()

    def pre2_compute_segmentation(self, event):
        self.config.segmentation_k = self.scale_bar_tab3.get()
        self.compute_segmentation()

    def compute_segmentation(self):
        """
        １：プルダウン（segmentation_combobox）からindex numberを取得
        ２：スケールバーからパラメタを取得
        ３：該当する関数をsegmentation_func_listから取得し、パラメタ値も含め入力画像に適用
        ４：出力画像をデータオブジェクトに保存
        ５：データオブジェクトから参照しキャンバス貼り付け
        """
        ### 1 : index取得　関数取得
        # index = self.segmentation_combobox.current()
        index = self.config.segmentation_func_index
        func = self.segmentation_func_list[index]
        print(index, func.__name__)
        ### 2 : スケールバーの値（パラメタ）取得
        # parameter = self.scale_bar_tab3.get()
        parameter = self.config.segmentation_k
        print(parameter)
        ### 3 : 該当する関数で領域分割　領域顕著度で使用するためslicオブジェクトを保存
        image_cv2 = cv2.imread(self.file_path)
        out, self.slic = func(image_cv2, parameter)

        self.segmentation_path = "img\\segmentation.jpeg"
        io.imsave(self.segmentation_path, out)

        ### 4 : ローカル変数imageに保存し、リサイズなどしてキャンバス貼り付け
        image = Image.open(self.segmentation_path)
        ### 最大辺を基準にキャンバスサイズの1/2に合うようリサイズ
        max_size = max([image.width, image.height])
        w_size = int(image.width * (self.canvas_height / 2) / max_size)
        h_size = int(image.height * (self.canvas_height / 2) / max_size)
        self.tk_image = ImageTk.PhotoImage(image=image.resize((w_size,h_size)))

        ### グローバル変数のリストに保存（キャンバスに画像保持）
        tk_images.append(self.tk_image)

        ### 画像の描画位置を1/2キャンバス中心に調節
        x = int(self.canvas_width / 4)
        y = int(self.canvas_height / 4)
        ### キャンバスに描画中の画像を削除
        if self.tab3_canvas_obj is not None:
            self.tab3_canvas.delete(self.tab3_canvas_obj)
            print("tab3 canvas object is deleted!")
        ### 画像をキャンバスに描画
        self.tab3_canvas_obj = self.tab3_canvas.create_image(x, y, image=self.tk_image)
    #############################################################################      




    #############################################################################   
    def compute_saliency_segmentation(self):
        saliency_map = io.imread(self.saliency_path)
        out = slic_saliency(saliency_map, self.slic)

        self.saliency_segmentation_path = "img\\saliency_segmentation.jpeg"
        io.imsave(self.saliency_segmentation_path, out)

        image = Image.open(self.saliency_segmentation_path)
        ### 最大辺を基準にキャンバスサイズの1/2に合うようリサイズ
        max_size = max([image.width, image.height])
        w_size = int(image.width * (self.canvas_height / 2) / max_size)
        h_size = int(image.height * (self.canvas_height / 2) / max_size)
        self.tk_image = ImageTk.PhotoImage(image=image.resize((w_size,h_size)))

        ### グローバル変数のリストに保存（キャンバスに画像保持）
        tk_images.append(self.tk_image)

        ### 画像の描画位置を1/2キャンバス中心に調節
        x = int(self.canvas_width / 4)
        y = int(self.canvas_height / 4)
        ### キャンバスに描画中の画像を削除
        if self.tab4_canvas_obj is not None:
            self.tab4_canvas.delete(self.tab4_canvas_obj)
            print("tab4 canvas object is deleted!")
        ### 画像をキャンバスに描画
        self.tab4_canvas_obj = self.tab4_canvas.create_image(x, y, image=self.tk_image)



    def pre_compute_masked_image(self, event):
        self.config.segmentation_saliency_threshold = self.scale_bar_tab4.get()
        self.compute_masked_image()

    def compute_masked_image(self):
        ### 1 : スケールバーの値（パラメタ）取得
        # threshold = self.scale_bar_tab4.get()
        threshold = self.config.segmentation_saliency_threshold

        image = cv2.imread(self.saliency_segmentation_path)
        mask1 = self.mask(image, threshold)
        mask2 = cv2.bitwise_not(mask1)
        self.mask1_path = "img\\mask1.png"
        self.mask2_path = "img\\mask2.png"
        cv2.imwrite(self.mask1_path, mask1)
        cv2.imwrite(self.mask2_path, mask2)

        h, w, _ = image.shape

        ### 真っ黒な画像（ベース）
        blank = np.zeros((h, w, 3))
        cv2.imwrite('blank.jpeg', blank)

        input = Image.open(self.file_path)
        base = Image.open("blank.jpeg")
        mask1 = Image.open(self.mask1_path)
        mask2 = Image.open(self.mask2_path)
        

        out1 = Image.composite(base, input, mask1)
        out2 = Image.composite(base, input, mask2)
        
        self.masked_image1_path = "img\\masked_image1.jpeg"
        self.masked_image2_path = "img\\masked_image2.jpeg"
        out1.save(self.masked_image1_path)
        out2.save(self.masked_image2_path)
        

        image1 = Image.open(self.masked_image1_path)
        ### 最大辺を基準に「ミニ」キャンバスサイズの1/2に合うようリサイズ
        max_size = max([image1.width, image1.height])
        w_size = int(image1.width * 200 / max_size)
        h_size = int(image1.height * 200 / max_size)
        self.tk_image = ImageTk.PhotoImage(image=image1.resize((w_size,h_size)))
        ### グローバル変数のリストに保存（キャンバスに画像保持）
        tk_images.append(self.tk_image)
        ### 画像の描画位置を1/2キャンバス中心に調節
        x = int(200 / 2)
        y = int(200 / 2)
        ### キャンバスに描画中の画像を削除
        if self.tab4_minicanvas1_obj is not None:
            self.tab4_minicanvas1.delete(self.tab4_minicanvas1_obj)
            print("tab4 minicanvas1 object is deleted!")
        ### 画像をキャンバスに描画
        self.tab4_minicanvas1_obj = self.tab4_minicanvas1.create_image(x, y, image=self.tk_image)



        image2 = Image.open(self.masked_image2_path)
        self.tk_image2 = ImageTk.PhotoImage(image=image2.resize((w_size,h_size)))
        ### グローバル変数のリストに保存（キャンバスに画像保持）
        tk_images.append(self.tk_image2)
        ### キャンバスに描画中の画像を削除
        if self.tab4_minicanvas2_obj is not None:
            self.tab4_minicanvas2.delete(self.tab4_minicanvas2_obj)
            print("tab4 minicanvas2 object is deleted!")
        ### 画像をキャンバスに描画
        self.tab4_minicanvas2_obj = self.tab4_minicanvas2.create_image(x, y, image=self.tk_image2)



    def mask(self, image, threshold):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY)
        return binary
    #############################################################################   



    ############################################################################# 
    def pre1_compute_paint1(self, event):
        self.config.paint1_func_index = self.paint_combobox1.current()
        self.compute_paint1()

    def pre2_compute_paint1(self, event):
        self.config.paint1_func_parameter = self.scale_bar1_tab5.get()
        self.compute_paint1()

    def compute_paint1(self):
        ### 1 : index取得　関数取得
        # index = self.paint_combobox1.current()
        index = self.config.paint1_func_index
        func = self.paint_func_list[index]
        print(index, func.__name__)
        ### 2 : スケールバーの値（パラメタ）取得
        # parameter = self.scale_bar1_tab5.get()
        parameter = self.config.paint1_func_parameter
        print("paint1  index:{}, parameter:{}".format(index, parameter))
        ### 3 : 該当する関数でペイント
        out = func(self.file_path, parameter)
        self.paint1_path = "img\\paint1.jpeg"
        io.imsave(self.paint1_path, out)
        ### 4 : マスク参照して切り取ったペイント画像表示
        paint1 = Image.open(self.paint1_path)
        base = Image.open("blank.jpeg")
        mask1 = Image.open(self.mask1_path)
        out1 = Image.composite(base, paint1, mask1)
        ### 5 : 作成した画像をpaint1レイヤとして保存
        self.paint1_layer_path = "img\\paint1_layer.jpeg"
        out1.save(self.paint1_layer_path)
        
        image1 = Image.open(self.paint1_layer_path)
        ### 最大辺を基準にキャンバスサイズの1/2に合うようリサイズ
        max_size = max([image1.width, image1.height])
        w_size = int(image1.width * (self.canvas_height / 2 - 11) / max_size)
        h_size = int(image1.height * (self.canvas_height / 2 - 11) / max_size)
        self.tk_image = ImageTk.PhotoImage(image=image1.resize((w_size,h_size)))
        ### グローバル変数のリストに保存（キャンバスに画像保持）
        tk_images.append(self.tk_image)
        ### 画像の描画位置を1/2キャンバス中心に調節
        x = int(self.canvas_width / 4 - 5)
        y = int(self.canvas_height / 4 - 5)
        ### キャンバスに描画中の画像を削除
        if self.tab5_canvas1_obj is not None:
            self.tab5_canvas1.delete(self.tab5_canvas1_obj)
            print("tab5 canvas1 object is deleted!")
        ### 画像をキャンバスに描画
        self.tab5_canvas1_obj = self.tab5_canvas1.create_image(x, y, image=self.tk_image)




    def pre1_compute_paint2(self, event):
        self.config.paint2_func_index = self.paint_combobox2.current()
        self.compute_paint2()

    def pre2_compute_paint2(self, event):
        self.config.paint2_func_parameter = self.scale_bar2_tab5.get()
        self.compute_paint2()

    def compute_paint2(self):
        ### 1 : index取得　関数取得
        # index = self.paint_combobox2.current()
        index = self.config.paint2_func_index
        func = self.paint_func_list[index]
        print(index, func.__name__)
        ### 2 : スケールバーの値（パラメタ）取得
        # parameter = self.scale_bar2_tab5.get()
        parameter = self.config.paint2_func_parameter
        print("paint2  index:{}, parameter:{}".format(index, parameter))
        ### 3 : 該当する関数でペイント
        out = func(self.file_path, parameter)
        self.paint2_path = "img\\paint2.jpeg"
        io.imsave(self.paint2_path, out)
        ### 4 : マスク参照して切り取ったペイント画像表示
        paint2 = Image.open(self.paint2_path)
        base = Image.open("blank.jpeg")
        mask1 = Image.open(self.mask2_path)
        out1 = Image.composite(base, paint2, mask1)
        ### 5 : 作成した画像をpaint1レイヤとして保存
        self.paint2_layer_path = "img\\paint2_layer.jpeg"
        out1.save(self.paint2_layer_path)
        
        image2 = Image.open(self.paint2_layer_path)
        ### 最大辺を基準にキャンバスサイズの1/2に合うようリサイズ
        max_size = max([image2.width, image2.height])
        w_size = int(image2.width * (self.canvas_height / 2 - 11) / max_size)
        h_size = int(image2.height * (self.canvas_height / 2 - 11) / max_size)
        self.tk_image = ImageTk.PhotoImage(image=image2.resize((w_size,h_size)))
        ### グローバル変数のリストに保存（キャンバスに画像保持）
        tk_images.append(self.tk_image)
        ### 画像の描画位置を1/2キャンバス中心に調節
        x = int(self.canvas_width / 4 - 5)
        y = int(self.canvas_height / 4 - 5)
        ### キャンバスに描画中の画像を削除
        if self.tab5_canvas2_obj is not None:
            self.tab5_canvas2.delete(self.tab5_canvas2_obj)
            print("tab5 canvas2 object is deleted!")
        ### 画像をキャンバスに描画
        self.tab5_canvas2_obj = self.tab5_canvas2.create_image(x, y, image=self.tk_image)

    #############################################################################   



    def synthesize_layers(self):
        paint1 = Image.open(self.paint1_path)
        paint2 = Image.open(self.paint2_path)
        mask = Image.open(self.mask1_path)
        out = Image.composite(paint2, paint1, mask)
        # out1 = Image.composite(watercolor, kuwahara, mask1)
        
        self.out_path = "img\\output.jpeg"
        out.save(self.out_path)

        image = Image.open(self.out_path)
        ### 最大辺を基準にキャンバスサイズに合うようリサイズ
        max_size = max([image.width, image.height])
        w_size = int(image.width * self.canvas_height / max_size)
        h_size = int(image.height * self.canvas_height / max_size)
        self.tk_image = ImageTk.PhotoImage(image=image.resize((w_size,h_size)))

        ### グローバル変数のリストに保存（キャンバスに画像保持）
        tk_images.append(self.tk_image)

        ### 画像の描画位置を1/2キャンバス中心に調節
        x = int(self.canvas_width / 2)
        y = int(self.canvas_height / 2)
        ### キャンバスに描画中の画像を削除
        if self.out_canvas_obj is not None:
            self.out_canvas.delete(self.out_canvas_obj)
            print("out canvas object is deleted!")
        ### 画像をキャンバスに描画
        self.out_canvas_obj = self.out_canvas.create_image(x, y, image=self.tk_image)




    """名前を付けて保存（fileダイアログ表示⇒パス取得⇒表示中の画像保存）"""
    def save_as(self):
        filename = tk.filedialog.asksaveasfilename(
            title = "名前を付けて保存",
            filetypes = [("PNG", ".png"), ("JPEG", ".jpg"), ("Tiff", ".tif"), ("Bitmap", ".bmp")], # ファイルフィルタ
            initialdir = "./", # 自分自身のディレクトリ
            defaultextension = "png"
        )
        print(filename)
        image = io.imread(self.out_path)
        io.imsave(filename, image)


    def pre_compute_all(self, event):
        global config_index
        config_index = self.config_combobox.current()
        self.compute_all()

    def compute_all(self):
        self.update_label()
        index = config_index
        # print("{}.json".format(config_dict_list[index]))
        dict = self.config.load_para_from_json("config\\{}.json".format(config_dict_list[index]))
        self.config.update_param(dict)
        if self.file_path is None:
            print("入力がありません")
            exit()

        ### ウィジェットの設定値に現在のパラメタをセット
        self.fix_widget_setting()
        
        ### まとめて最後まで処理
        self.compute_saliency()
        self.compute_segmentation()
        # self.scale_bar_tab3['variable'] = self.config.segmentation_k
        self.compute_saliency_segmentation()
        self.compute_masked_image()
        self.compute_paint1()
        self.compute_paint2()
        self.synthesize_layers()


    def save_config(self):
        filename = tk.filedialog.asksaveasfilename(
            title = "名前を付けて保存",
            initialdir = "config\\", # 自分自身のディレクトリ
            defaultextension = "json"
        )
        self.config.name = filename
        self.config.make_json(filename)
        config_dict_list.append(os.path.basename(filename)[0:-5])
        print(os.path.basename(filename)[0:-5])
        self.config_combobox['values'] = config_dict_list


    def fix_widget_setting(self):
        ### パラメタに合うようにウィジェットの設定値をセット
        self.saliency_combobox.current(self.config.saliency_func_index)
        self.segmentation_combobox.current(self.config.segmentation_func_index)
        self.scale_bar_tab3.set(self.config.segmentation_k)
        self.scale_bar_tab4.set(self.config.segmentation_saliency_threshold)
        self.paint_combobox1.current(self.config.paint1_func_index)
        self.scale_bar1_tab5.set(self.config.paint1_func_parameter)
        self.paint_combobox2.current(self.config.paint2_func_index)
        self.scale_bar2_tab5.set(self.config.paint2_func_parameter)



    def getNoteName(self,event):
        note =event.widget
        self.label["text"]=note.tab(note.select(),"text")


    def correct_saliency(self, event):
        print("x:{} y:{}".format(event.x, event.y))

        image = Image.open(self.saliency_path)
        image_w = image.width
        image_h = image.height
        canvas_h = self.canvas_height/2
        canvas_w = self.canvas_width/2

        if(image_w>image_h):
            dh = (canvas_h - image_h*canvas_h/image_w)/2
            X = int(event.x * image_w / canvas_w)
            Y = int((event.y-dh) * image_w / canvas_w)
        else:
            dw = (canvas_w - image_w*canvas_w/image_h)/2
            X = int((event.x-dw) * image_h / canvas_h)
            Y = int(event.y * image_h / canvas_h)

        Z = norm_dist()
        print("Z:", Z)
        # print("saliency_x:{} saliency_y:{}".format(image_w, image_h))
        print("X:{} Y:{}".format(X, Y))

        ### drawオブジェクト作成，クリック座標に円を描画，変更を保存
        self.radius_size = self.scale_bar_tab2.get()
        draw = ImageDraw.Draw(image)
        
        if self.radio_value.get()==255:
            draw.pieslice((X-self.radius_size, Y-self.radius_size, X+self.radius_size, Y+self.radius_size), start=0, end=360, fill=255, outline=0)
        elif self.radio_value.get()==0:
            draw.pieslice((X-self.radius_size, Y-self.radius_size, X+self.radius_size, Y+self.radius_size), start=0, end=360, fill=0, outline=0)
        image.save(self.saliency_path)

        # image = Image.open(self.saliency_path)

        ### 最大辺を基準にキャンバスサイズの1/2に合うようリサイズ
        max_size = max([image.width, image.height])
        w_size = int(image.width*(self.canvas_height/2)/max_size)
        h_size = int(image.height*(self.canvas_height/2)/max_size)
        self.tk_image = ImageTk.PhotoImage(image=image.resize((w_size,h_size)))

        ### グローバル変数のリストに保存（キャンバスに画像保持）
        tk_images.append(self.tk_image)

        ### 画像の描画位置を1/2キャンバス中心に調節
        x = int(self.canvas_width / 4)
        y = int(self.canvas_height / 4)
        ### キャンバスに描画中の画像を削除
        if self.tab2_canvas_obj is not None:
            self.tab2_canvas.delete(self.tab2_canvas_obj)
            print("tab2 canvas object is deleted!")
        ### 画像をキャンバスに描画
        self.tab2_canvas_obj = self.tab2_canvas.create_image(x, y, image=self.tk_image)

        





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
        self.saliency_combobox.bind("<<ComboboxSelected>>", self.pre_compute_saliency)


        ### 画像表示用キャンバス
        self.tab2_canvas = tk.Canvas(self.tab2, width=self.canvas_width/2, height=self.canvas_height/2, bg="black")
        self.tab2_canvas.pack()
        self.tab2_canvas.bind('<ButtonPress-1>', self.correct_saliency)
        # 画像オブジェクトの設定（初期はNone）⇒これ使う？
        self.tab2_image = None
        ### キャンバスに描画中の画像（初期はNone）
        self.tab2_canvas_obj = None

         # ラジオボタンの値
        self.radio_value = tk.IntVar(value = 1)     # 初期値を設定する場合
        #self.radio_value = tk.IntVar()             # 初期値を設定しないと0になる
        
        # ラジオボタンの作成
        self.tab2_radio0 = tk.Radiobutton(self.tab2, 
                           text = "顕著度＋",      # ラジオボタンの表示名
                           command = self.radio_click,  # クリックされたときに呼ばれるメソッド
                           variable = self.radio_value, # 選択の状態を設定する
                           value = 255                    # ラジオボタンに割り付ける値の設定
                           )

        self.tab2_radio1 = tk.Radiobutton(self.tab2, 
                           text = "顕著度ー",      # ラジオボタンの表示名
                           command = self.radio_click,  # クリックされたときに呼ばれるメソッド
                           variable = self.radio_value, # 選択の状態を設定する
                           value = 0                    # ラジオボタンに割り付ける値の設定
                           )

        self.tab2_radio0.pack()
        self.tab2_radio1.pack()

        ### スケールバー 作成と配置
        self.scale_bar_tab2 = tk.Scale(
            self.tab2, 
            orient=tkinter.HORIZONTAL, 
            from_=0, 
            to=100, 
            background=self.tab_color
        )
        self.scale_bar_tab2.set(20)
        self.scale_bar_tab2.pack()
        #マウスを離したときにcompute_segmentation実行
        # self.scale_bar_tab2.bind("<ButtonRelease>", self.pre2_compute_segmentation)


    def radio_click(self):
        # ラジオボタンの値を取得
        value = self.radio_value.get()
        print(f"ラジオボタンの値は {value} です")


    """Tab3のウィジェット作成関数【領域分割】"""
    def tab3_set(self):
        ### comboboxのオブジェクト生成　リスト指定
        self.segmentation_combobox = ttk.Combobox(self.tab3, values=self.segmentation_name_list)
        ### comboboxの貼り付け
        self.segmentation_combobox.pack()
        ### comboboxの初期値設定変更（index=1が初期値）
        self.segmentation_combobox.current(0)
        ### 【重要】プルダウン選択時に呼び出す関数をバインド
        self.segmentation_combobox.bind("<<ComboboxSelected>>", self.pre1_compute_segmentation)


        ### 画像表示用キャンバス
        self.tab3_canvas = tk.Canvas(self.tab3, width=self.canvas_width/2, height=self.canvas_height/2, bg="black")
        self.tab3_canvas.pack()
        # 画像オブジェクトの設定（初期はNone）⇒これ使う？
        self.tab3_image = None
        ### キャンバスに描画中の画像（初期はNone）
        self.tab3_canvas_obj= None

        ### スケールバー 作成と配置
        self.scale_bar_tab3 = tk.Scale(
            self.tab3, 
            orient=tkinter.HORIZONTAL, 
            from_=0, 
            to=200, 
            background=self.tab_color
        )
        self.scale_bar_tab3.set(100)
        self.scale_bar_tab3.pack()
        #マウスを離したときにcompute_segmentation実行
        self.scale_bar_tab3.bind("<ButtonRelease>", self.pre2_compute_segmentation)


    
    """Tab4のウィジェット作成関数【領域顕著度】"""
    def tab4_set(self):
        ### 領域顕著度計算ボタン
        self.saliency_segmentation_button = tkinter.Button(
            self.tab4,
            text="saliency segmentation",
            command=self.compute_saliency_segmentation
        )
        self.saliency_segmentation_button.pack()


        ### 画像表示用キャンバス
        self.tab4_canvas = tk.Canvas(self.tab4, width=self.canvas_width/2, height=self.canvas_height/2, bg="black")
        self.tab4_canvas.pack()
        # 画像オブジェクトの設定（初期はNone）⇒これ使う？
        self.tab4_image = None
        ### キャンバスに描画中の画像（初期はNone）
        self.tab4_canvas_obj= None

        ### スケールバー 作成と配置
        self.scale_bar_tab4 = tk.Scale(
            self.tab4, orient=tkinter.HORIZONTAL, 
            from_=0, 
            to=255, 
            background=self.tab_color
        )
        self.scale_bar_tab4.set(100)
        self.scale_bar_tab4.pack()
        #マウスを離したときにcompute_masked_image実行
        self.scale_bar_tab4.bind("<ButtonRelease>", self.pre_compute_masked_image)

        ### マスク画像貼り付け用フレーム
        self.minicanvas_frame = tk.Frame(self.tab4, height=225,width=600, background="gray")
        self.minicanvas_frame.pack() 

        ### マスク適用画像キャンバス１
        self.tab4_minicanvas1 = tk.Canvas(self.minicanvas_frame, width=200, height=200, bg="black")
        self.tab4_minicanvas1.grid(column=0, row=0)
        # 画像オブジェクトの設定（初期はNone）⇒これ使う？
        self.tab4_minicanvas1_image = None
        ### キャンバスに描画中の画像（初期はNone）
        self.tab4_minicanvas1_obj= None

        ### マスク適用画像キャンバス２
        self.tab4_minicanvas2 = tk.Canvas(self.minicanvas_frame, width=200, height=200, bg="black")
        self.tab4_minicanvas2.grid(column=1, row=0)
        # 画像オブジェクトの設定（初期はNone）⇒これ使う？
        self.tab4_minicanvas2_image = None
        ### キャンバスに描画中の画像（初期はNone）
        self.tab4_minicanvas2_obj= None


    
    """Tab5のウィジェット作成関数【塗分け】"""
    def tab5_set(self):
        ### ペイント1の画像貼り付け用フレーム
        self.paint_frame1 = tk.Frame(self.tab5, height=289,width=300, background="gray")
        self.paint_frame1.grid(row=0, column=0)
        ### ペイント2の画像貼り付け用フレーム
        self.paint_frame2 = tk.Frame(self.tab5, height=289,width=300, background="gray")
        self.paint_frame2.grid(row=1, column=0)
        ### ペイント1のボタン用フレーム
        self.button_frame1 = tk.Frame(self.tab5, height=289,width=300, background=self.tab_color)
        self.button_frame1.grid(row=0, column=1)
        ### ペイント2のボタン用フレーム
        self.button_frame2 = tk.Frame(self.tab5, height=289,width=300, background=self.tab_color)
        self.button_frame2.grid(row=1, column=1)


        ### 画像表示用キャンバス
        self.tab5_canvas1 = tk.Canvas(self.paint_frame1, width=self.canvas_width/2-11, height=self.canvas_height/2-11, bg="black")
        self.tab5_canvas1.pack()
        # 画像オブジェクトの設定（初期はNone）⇒これ使う？
        self.tab5_image1 = None
        ### キャンバスに描画中の画像（初期はNone）
        self.tab5_canvas1_obj= None

        ### 画像表示用キャンバス
        self.tab5_canvas2 = tk.Canvas(self.paint_frame2, width=self.canvas_width/2-11, height=self.canvas_height/2-11, bg="black")
        self.tab5_canvas2.pack()
        # 画像オブジェクトの設定（初期はNone）⇒これ使う？
        self.tab5_image2 = None
        ### キャンバスに描画中の画像（初期はNone）
        self.tab5_canvas2_obj= None



        ### comboboxのオブジェクト生成　リスト指定
        self.paint_combobox1 = ttk.Combobox(self.button_frame1, values=self.paint_name_list)
        ### comboboxの貼り付け
        self.paint_combobox1.pack()
        ### comboboxの初期値設定変更（index=1が初期値）
        self.paint_combobox1.current(1)
        ### 【重要】プルダウン選択時に呼び出す関数をバインド
        self.paint_combobox1.bind("<<ComboboxSelected>>", self.pre1_compute_paint1)

        ### スケールバー 作成と配置
        self.scale_bar1_tab5 = tk.Scale(
            self.button_frame1, 
            orient=tkinter.HORIZONTAL, 
            from_=0, 
            to=200,
            background=self.tab_color
        )
        self.scale_bar1_tab5.set(18)
        self.scale_bar1_tab5.pack()
        #マウスを離したときにcompute_segmentation実行
        self.scale_bar1_tab5.bind("<ButtonRelease>", self.pre2_compute_paint1)


        ### comboboxのオブジェクト生成　リスト指定
        self.paint_combobox2 = ttk.Combobox(self.button_frame2, values=self.paint_name_list)
        ### comboboxの貼り付け
        self.paint_combobox2.pack()
        ### comboboxの初期値設定変更（index=1が初期値）
        self.paint_combobox2.current(0)
        ### 【重要】プルダウン選択時に呼び出す関数をバインド
        self.paint_combobox2.bind("<<ComboboxSelected>>", self.pre1_compute_paint2)


        ### スケールバー 作成と配置
        self.scale_bar2_tab5 = tk.Scale(
            self.button_frame2, 
            orient=tkinter.HORIZONTAL, 
            from_=0, 
            to=30,
            background=self.tab_color
        )
        self.scale_bar2_tab5.set(4)
        self.scale_bar2_tab5.pack()
        #マウスを離したときにcompute_segmentation実行
        self.scale_bar2_tab5.bind("<ButtonRelease>", self.pre2_compute_paint2)

    
    """Tab6のウィジェット作成関数【未定】"""
    # def tab6_set(self):
    #     pass


    

    #################################################################################



app = Application()

app.mainloop()