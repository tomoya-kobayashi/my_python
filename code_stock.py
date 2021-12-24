
#画像のリサイズ（アスペクト率保持）
# re_length = 300
# # 縦横のサイズを取得(h:縦、ｗ：横)
# h, w = image.shape[:2]
# # 変換する倍率を計算
# re_h = re_w = re_length/max(h,w)
# # アスペクト比を固定して画像を変換
# img2 = cv2.resize(image, dsize=None, fx=re_h , fy=re_w)
# h2, w2 = img2.shape[:2]
# io.imsave('img\\cat1_rgba_resize300.png', img2)
