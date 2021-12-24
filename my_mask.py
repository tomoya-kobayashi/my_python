"""
https://pystyle.info/opencv-image-binarization/#:~:text=OpenCV%20%E3%81%A7%E3%81%AF%E3%80%812%E5%80%A4%E5%8C%96%E3%81%AF%E4%BB%A5%E4%B8%8B%E3%81%AE%E9%96%A2%E6%95%B0%E3%81%A7%E8%A1%8C%E3%81%88%E3%81%BE%E3%81%99%E3%80%82%20%E5%A4%A7%E5%9F%9F%E7%9A%842%E5%80%A4%E5%8C%96%20threshold%28%29%3A%20%E3%81%82%E3%82%8B%E9%96%BE%E5%80%A4%E4%BB%A5%E4%B8%8B%E3%81%8B%E3%81%A9%E3%81%86%E3%81%8B%E3%81%A72%E5%80%A4%E5%8C%96%E3%81%97%E3%81%BE%E3%81%99%E3%80%82,inRange%28%29%3A%202%E3%81%A4%E3%81%AE%E9%96%BE%E5%80%A4%E3%81%AE%E7%AF%84%E5%9B%B2%E5%86%85%E3%81%8B%E3%81%A9%E3%81%86%E3%81%8B%E3%81%A72%E5%80%A4%E5%8C%96%E3%81%97%E3%81%BE%E3%81%99%E3%80%82%20%E9%81%A9%E5%BF%9C%E7%9A%842%E5%80%A4%E5%8C%96%20adaptiveThreshold%28%29%3A%20%E9%A0%98%E5%9F%9F%E3%81%94%E3%81%A8%E3%81%AB%E9%81%A9%E5%BF%9C%E7%9A%84%E3%81%AB%E9%96%BE%E5%80%A4%E3%82%92%E6%B1%BA%E3%82%81

マスク作成関数
引数：入力画像パス、閾値、出力（マスク）パス

動作：入力画像を閾値で２値化
閾値より小さいとマスクする
値を２５５倍（０，１→０，２５５）
マスクを保存

出力：出力画像（マスク）パス
"""

"""
マスク適用関数
引数：入力画像パス、入力マスクパス、出力レイヤーパス

動作：入力画像をマスクして保存

出力：出力画像（レイヤー）のパス

"""

import cv2
from PIL import Image
# from my_convert import jpg_to_png, png_to_rgb
from skimage import io, segmentation, color
import numpy as np



def make_mask(file_path, threshold, file_path_out):
    saliency_rgb = cv2.imread(file_path)
    saliency_gray = cv2.cvtColor(saliency_rgb, cv2.COLOR_BGR2GRAY)

    # ２値化
    ret, binary = cv2.threshold(saliency_gray, threshold, 255, cv2.THRESH_BINARY)
    # binary = binary.astype(np.uint8)
    io.imsave(file_path_out, binary)




def do_mask(file_path, mask_path, file_path_out):
    # PNGをRGBA方式で読み込み（第２引数は'-1'）
    image = cv2.imread(file_path, -1)
    mask_rgb = cv2.imread(mask_path)
    mask_gray = cv2.cvtColor(mask_rgb, cv2.COLOR_BGR2GRAY)
    # 透明度だけ抽出
    img_alpha = image[:, :, 3].copy()

    # 透明度にマスクの値を乗算　０，１から０，２５５に変換
    out = np.multiply(img_alpha, mask_gray)
    out = np.multiply(out, 255)
    # 入力画像の透明度を更新
    image[:, :, 3] = out
    # 画像保存
    io.imsave(file_path_out, image)

    # print(binary)
    # print(image)


def make_do_mask(file_path, saliency_path, threshold, file_path_out):
    # マスク用画像読み込み
    saliency_rgb = cv2.imread(saliency_path)
    saliency_gray = cv2.cvtColor(saliency_rgb, cv2.COLOR_BGR2GRAY)

    # マスク用画像の２値化
    ret, binary = cv2.threshold(saliency_gray, threshold, 255, cv2.THRESH_BINARY)
    # binary = binary.astype(np.uint8)
    # io.imsave(file_path_out, binary)

    # PNGをRGBA方式で読み込み（第２引数は'-1'）
    image = cv2.imread(file_path, -1)
    # 透明度だけ抽出
    img_alpha = image[:, :, 3].copy()

    # 透明度にマスクの値を乗算　０，１から０，２５５に変換
    out = np.multiply(img_alpha, binary)
    out = np.multiply(out, 255)
    # 入力画像の透明度を更新
    image[:, :, 3] = out
    # 画像保存
    io.imsave(file_path_out, image)


