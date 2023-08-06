import cv2
import matplotlib.pyplot as plt
import numpy as np
import pathlib
import os


def show_contours(path_origin,threshold1=100,threshold2=150):
    #ファイルの読み込み
    img = cv2.imread(path_origin)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    #エッジ抽出
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray,threshold1 ,threshold2 , L2gradient=True)
    ret, edges = cv2.threshold(edges, 120, 150, cv2.THRESH_BINARY)

    #輪郭抽出
    contours, hierarchy = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

    img2 = img.copy()
    
    global ellipse_lst
    global ellipse_area
    ellipse_lst = []
    ellipse_area = []
    for i in range(0, len(contours)):
        if len(contours[i]) > 0:
            area = cv2.contourArea(contours[i])
            if area < 80:
                continue
            rect = contours[i]

            ellipse = cv2.fitEllipse(rect) 
            ellipse_lst.append(ellipse)
            ellipse_area.append(ellipse[1][0]*ellipse[1][1])

            #たくさんの楕円を見たい時
            cv2.ellipse(img2,ellipse,(0,255,0),2)

    plt.imshow(img2)
    print('適切なサイズの輪郭を選択してください')
    plt.show()    
    
def detect_food(path_origin,area_lank):
    #画像のファイル名取得
    stem = pathlib.Path(path_origin).stem

    img = cv2.imread(path_origin)
    h, w = img.shape[:2]

    #マスク作成 (黒く塗りつぶす画素の値は0)
    mask = np.zeros((h, w), dtype=np.uint8)
    # 楕円を描画する関数 ellipse()を利用してマスクの残したい部分を 255 にしている。
    #cv2.ellipse(mask,ellipse_lst[max_index],color=255,thickness=-1)
    choose_value = sorted(ellipse_area)[-1*area_lank]
    choose_index =  ellipse_area.index(choose_value)
    cv2.ellipse(mask,ellipse_lst[choose_index],color=255,thickness=-1)

    img[mask==0] = [0, 0, 0]#maskの値が0の画素は黒で塗りつぶす。
    path_blackimg = "./{}背景黒.png".format(stem)
    cv2.imwrite(path_blackimg, img)

    #背景透過
    image = cv2.imread(path_blackimg, -1) # -1はAlphaを含んだ形式(0:グレー, 1:カラ-
    if image.ndim == 3: # RGBならアルファチャンネル追加
        image = cv2.cvtColor(image, cv2.COLOR_RGB2RGBA)

    width = image.shape[0]
    height = image.shape[1]
    out = np.zeros(image.shape[:4], np.uint8)

    for i in range(width):
        for j in range(height):
            b = image[i][j][0]
            r = image[i][j][1]
            g = image[i][j][2]
            a = image[i][j][3]

            if r==0 and g==0 and b==0:
              out[i][j][0] = 0
              out[i][j][1] = 0
              out[i][j][2] = 0
              out[i][j][3] = 0
            else:
              out[i][j][0] = b
              out[i][j][1] = r
              out[i][j][2] = g
              out[i][j][3] = 255

    path_result = './{}検知.png'.format(stem)
    cv2.imwrite(path_result, out)
    plt.imshow(cv2.cvtColor(out, cv2.COLOR_BGR2RGB))
    os.remove(path_blackimg)
    plt.show()