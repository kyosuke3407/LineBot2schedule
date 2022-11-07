import cv2
import numpy as np
import PIL.ImageDraw

#コマンドライン引数だが画像をクリップした先からいれるようにする
def img2schedule(dt_now):
    year = dt_now.year
    month = dt_now.month
    print(str(year) + str(month))
    img = cv2.imread("./optimize_imgs/" + str(year) + str(month) + ".jpg")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    blue_min = np.array([70, 20, 0])
    blue_max = np.array([150, 255, 255])
    mask = cv2.inRange(img, blue_min, blue_max)
    output = cv2.bitwise_and(img, img, mask = mask)
    gray = cv2.bitwise_not(img, img, mask = mask)
    cv2.imwrite("./optimize_imgs/202211_bl.jpg", output)


    lower_color = np.array([20, 80, 10])
    upper_color = np.array([40, 255, 255])
    mask = cv2.inRange(img, lower_color, upper_color)
    output1 = cv2.bitwise_and(img, img, mask = mask)
    gray = cv2.bitwise_not(gray, gray, mask = mask)
    cv2.imwrite("./optimize_imgs/202211_out.jpg", output1)

    gray = cv2.cvtColor(gray, cv2.COLOR_HSV2BGR)
    gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
    cv2.imwrite("./optimize_imgs/202211_gray.jpg", gray)

    blend = cv2.addWeighted(src1=output,alpha=1,src2=output1,beta=1,gamma=0)
    #blend = cv2.cvtColor(img, cv2.COLOR_HSV2BGR)
    cv2.imwrite("./optimize_imgs/202211_solve.jpg", blend)

    h,w = img.shape[:2]
    index = w/31
    minh = int(h/5 * 2)
    maxh = int(h/5 * 3)

    day =[]
    for i in range(31):
        maxpi = int((i+1) * index)
        minpi = int(i * index)

        split_bl = output[minh:maxh, minpi:maxpi, :]
        split_ye = output1[minh:maxh, minpi:maxpi, :]
        split_gr = gray[minh:maxh, minpi:maxpi]

        split_bl = int(np.mean(split_bl))
        split_ye = int(np.mean(split_ye))
        split_gr = int(np.mean(split_gr))

        #print(split_bl,split_ye,split_gr,i+1)

        # 1:休み 2:通し 3:短縮 4:通常
        if split_gr<155 and split_gr>120:
            #print("短縮")
            day.append(3)
        elif abs(split_bl - split_ye) < 30:
            #print("休み")
            day.append(1)
        elif split_bl > split_ye:
            #print("通常")
            day.append(4)
        else:
            #print("通し")
            day.append(2)

    return day


