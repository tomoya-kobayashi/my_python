"""
データ保存用クラス
input_resizeはいらないかも。inputにresizeしたやつ入れちゃう
"""

import cv2
from PIL import ImageTk, Image

class Data():
    def __init__(self):

        ### 初期の画像を事前に作っておくか？
        self.input = Image.open("img\\ramen.jpeg")
        self.input_resize = Image.open("img\\ramen.jpeg")
        self.input_path = "img\\ramen.jpeg"
        self.saliency = self.input_resize
        self.segmentation = self.input_resize
        self.saliency_segmentation = self.input_resize
        self.layer_1 = self.input_resize
        self.layer_2 = self.input_resize
        self.func_saliency = self.func
        self.func_segmentation = self.func
        self.segmentation_threshold = 50
        self.dict_paint_1 = dict()
        self.dict_paint_2 = dict()
        self.output = self.input_resize

    def func():
        pass
