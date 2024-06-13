# -*- coding: utf-8 -*-
import cv2
import numpy as np
import time

# フレーム差分の計算
def frame_sub(img1, img2, img3, th):
    # フレームの絶対差分
    diff1 = cv2.absdiff(img1, img2)
    diff2 = cv2.absdiff(img2, img3)

    # 2つの差分画像の論理積
    diff = cv2.bitwise_and(diff1, diff2)

    # 二値化処理
    diff[diff < th] = 0
    diff[diff >= th] = 255
    
    # メディアンフィルタ処理（ゴマ塩ノイズ除去）
    mask = cv2.medianBlur(diff, 3) #３はフィルタサイズ

    return  mask


# 動画ファイルのキャプチャ
cap = cv2.VideoCapture("pexels-engin-akyurt-6613336.mp4")
    
# フレームを3枚取得してグレースケール変換
frame1 = cv2.cvtColor(cap.read()[1], cv2.COLOR_RGB2GRAY)
frame2 = cv2.cvtColor(cap.read()[1], cv2.COLOR_RGB2GRAY)
frame3 = cv2.cvtColor(cap.read()[1], cv2.COLOR_RGB2GRAY)

while(cap.isOpened()):
    # フレーム間差分を計算
    mask = frame_sub(frame1, frame2, frame3, th=200)

    # 結果を表示
    cv2.imshow("Frame1", frame1)
    cv2.imshow("Frame2", frame2)
    cv2.imshow("Frame3", frame3)
    cv2.imshow("Mask", mask)

    # 3枚のフレームを更新
    frame1 = frame2
    frame2 = frame3
    frame3 = cv2.cvtColor(cap.read()[1], cv2.COLOR_RGB2GRAY)

    # 待機(0.03sec)
    time.sleep(0.03)

    # qキーが押されたら途中終了
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()