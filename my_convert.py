import cv2
from PIL import Image
import numpy
from tkinter import *
from PIL import Image,ImageTk


# jpgをpngに変換
# 第一引数：jpg画像のパス　第二引数：変換後のファイルパス　
def jpg_to_png(file_path, file_path_out):
    # JPEG画像を読み込む
    image = cv2.imread(file_path)

    # file_path_out = "img\\" + file_name + ".png"
    # PNG画像として保存する
    cv2.imwrite(file_path_out, image, [int(cv2.IMWRITE_PNG_COMPRESSION ), 1])


# pngに透過率αを追加しRGBAに
# 第一引数：jpg画像のパス　第二引数：変換後のファイルパス　第三引数：透過率（デフォ：255）
def png_to_rgba(file_path, file_path_out, alpha=255):
    # 画像オブジェクトに変換
    im_obj = Image.open(file_path)

    ## アルファチャンネル追加
    im_obj.putalpha(alpha=alpha)
    # im_rotate90 = im_obj.rotate(90)
    im_obj.save(file_path_out)

    # print(im_obj.mode)



"""ImageTkからcv2imageへ変換"""
def tk_to_cv2(tk_image):
    'Tkinter -> CV2'

    # 画像の縦横サイズを取得
    height = tk_image.height()
    width = tk_image.width()

    # ピクセルデータの３次元リストを作成

    # 空のリストを作成
    bitmap = []
    for y in range(height):
        # 空のリストを作成
        line = []
        for x in range(width):

            # 座標(x,y)のピクセルデータを取得
            pixel = list(tk_image.get(x, y))

            # 取得したピクセルデータをリストに追加
            line.append(pixel)

        # 1行分のピクセルデータを追加
        bitmap.append(line)

    # 作成したリストをNumPy配列に変換
    cv2_rgb_image = numpy.array(bitmap, dtype='uint8')

    # RGB -> BGRによりCV2画像オブジェクトに変換
    cv2_image = cv2.cvtColor(cv2_rgb_image, cv2.COLOR_RGB2BGR)

    return cv2_image




def pil_to_cv2(pil_image):
    'PIL -> CV2'

    # pil_imageをNumPy配列に変換
    pil_image_array = numpy.array(pil_image)

    # RGB -> BGR によりCV2画像オブジェクトに変換
    cv2_image = cv2.cvtColor(pil_image_array, cv2.COLOR_RGB2BGR)

    return cv2_image




def cv2_to_pil(cv2_image):
    'CV2 -> PIL'

    # BGR -> RGB
    rgb_cv2_image = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB)

    # NumPy配列からPIL画像オブジェクトを生成
    pil_image = Image.fromarray(rgb_cv2_image)

    return pil_image




def tk_to_cv2(tk_image):
    'Tkinter -> CV2'

    # 画像の縦横サイズを取得
    height = tk_image.height()
    width = tk_image.width()

    # ピクセルデータの３次元リストを作成

    # 空のリストを作成
    bitmap = []
    for y in range(height):
        # 空のリストを作成
        line = []
        for x in range(width):

            # 座標(x,y)のピクセルデータを取得
            pixel = list(tk_image.get(x, y))

            # 取得したピクセルデータをリストに追加
            line.append(pixel)

        # 1行分のピクセルデータを追加
        bitmap.append(line)

    # 作成したリストをNumPy配列に変換
    cv2_rgb_image = numpy.array(bitmap, dtype='uint8')

    # RGB -> BGRによりCV2画像オブジェクトに変換
    cv2_image = cv2.cvtColor(cv2_rgb_image, cv2.COLOR_RGB2BGR)

    return cv2_image



def pil_to_tk(pil_image):
    'PIL -> Tkinter'

    # Tkinter画像オブジェクトをPIL画像オブジェクトから生成
    tk_image = ImageTk.PhotoImage(pil_image)

    return tk_image


def cv2_to_tk(cv2_image):
    'CV2 -> Tkinter'

    # BGR -> RGB
    rgb_cv2_image = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB)

    # NumPy配列からPIL画像オブジェクトを生成
    pil_image = Image.fromarray(rgb_cv2_image)

    # PIL画像オブジェクトをTkinter画像オブジェクトに変換
    tk_image = ImageTk.PhotoImage(pil_image)

    return tk_image



