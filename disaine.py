
import handtrakingmodule as htm
import cv2
import os
import numpy as np



draw  = False
erase = False
BRUSH_THICKNESS = 25
ERASE_THICKNSS = 100 
draw_color = (0, 0, 0)
width = 1920
height = 1080

imgCanvas = np.zeros((height, width, 3), np.uint8)


folderPath = 'HeaderGuts'
header_list = []
listHeader = os.listdir(folderPath)
for imgPath in listHeader:
    image= cv2.imread(folderPath+'/'+imgPath)
    header_list.append(image)
header  = header_list[-1]
cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)


cv2.namedWindow('window', cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty('window', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

detector = htm.handDetector()
while cap.isOpened():  # пока камера "работает"
        success, image = cap.read()  # полчаем кадр с web-камеры (True/False, image)
        if not success:  # если не удалось получить кадр
            print("Не удалось получить изображение с web-камеры")
            continue  # переход к ближайшему циклу (while)
            
        image = cv2.flip(image, 1)  # зеркальное отражение картинки
        detector.findHands(image)
        detector.findFingersPosition(image)
        mhl =detector.result.multi_hand_landmarks
        h, w, c = header.shape
        if mhl:
            handCount = len(mhl)
            for i in range(handCount):
                x1, y1  =detector.pointPosition[i][4][0],detector.pointPosition[i][4][1]
                x2, y2  =detector.pointPosition[i][8][0],detector.pointPosition[i][8][1]
                cx ,cy = (x1 + x2) // 2, (y1 + y2) // 2

                distance  = detector.findDistance(4,8,i)
                if distance < 50:
                    if cy <= h:
                        if 183 <= cx <= 492:
                            header = header_list[0]
                        elif 600 <= cx <= 908:
                            header = header_list[1]
                        elif 1023 <= cx <= 1332:
                            header = header_list[2]
                        elif 1425 <= cx <= 1568:
                            header = header_list[3]
                        


        

        image[0:h,0:w]= header
        cv2.imshow("window", image)
        if cv2.waitKey(1) &  0xFF == 27:  # esc
            break