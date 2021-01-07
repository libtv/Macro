import pytesseract as ocr
import numpy as np
import pickle
import ldimshow
import numpy
import cv2
import time

# 변수명 #
억경 = []  # 억경
cropping_억경 = False  # 억경 크로핑
자동복구 = []  # 자동복구
cropping_자동복구 = False  # 자동복구 크로핑
ocr_result = ""
ocr_result2 = ""
lower_white = np.array([0, 0, 168], dtype=np.uint8)
upper_white = np.array([172, 111, 255], dtype=np.uint8)

################## 억경 ##################
def crop():

    ocr.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

    def click_and_crop_1(event, x, y, flags, param):  # 억경
        global 억경, cropping_억경

        # 왼쪽 마우스가 클릭되면 (x, y) 좌표 기록을 시작하고
        # cropping = True로 만들어 줍니다.
        if event == cv2.EVENT_LBUTTONDOWN:
            억경 = [(x, y)]
            cropping_억경 = True

        elif event == cv2.EVENT_LBUTTONUP:
            억경.append((x, y))
            cropping_억경 = False

            cv2.rectangle(image, 억경[0], 억경[1], (0, 255, 0), 2)
            cv2.imshow("image", image)

    def click_and_crop_2(event, x, y, flags, param):  # 자동복구
        global 자동복구, 자동복구

        # 왼쪽 마우스가 클릭되면 (x, y) 좌표 기록을 시작하고
        # cropping = True로 만들어 줍니다.
        if event == cv2.EVENT_LBUTTONDOWN:
            자동복구 = [(x, y)]
            cropping_자동복구 = True

        elif event == cv2.EVENT_LBUTTONUP:
            자동복구.append((x, y))
            cropping_자동복구 = False

            cv2.rectangle(image, 자동복구[0], 자동복구[1], (0, 255, 0), 2)
            cv2.imshow("image", image)


################## 억경 ##################
    time.sleep(5)
    image = ldimshow.showImage()
    image = cv2.cvtColor(numpy.array(image), cv2.COLOR_RGB2BGR)
    clone = image.copy()
    cv2.namedWindow("image")
    cv2.setMouseCallback("image", click_and_crop_1) # 억경 확인하기
    print("억경을 마킹해주세요 >> ")

    while True:
        cv2.imshow("image", image)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("r"):
            image = clone.copy()

        elif key == ord("c"):
            if len(억경) == 2:
                roi = clone[억경[0][1]:억경[1][1], 억경[0][0]:억경[1][0]]
                hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

                mask = cv2.inRange(hsv, lower_white, upper_white)
                res = cv2.bitwise_and(roi, roi, mask=mask)
                res = cv2.bitwise_not(res)
                cv2.imshow("res",res)

                ocr_result = ocr.image_to_string(res, config='--psm 6 -c tessedit_char_whitelist=0123456789')
                ocr_result = ocr_result.replace('\n','')
                ocr_result = ocr_result[:-3]
                print("현재 억경은 : "+ocr_result +" 입니까? (맞으면 'qq' 아니면 'rr'로 다시 마킹해주세요 ")
                cv2.waitKey(0)
        elif key == ord("q"):
                break

    ############### 자동복구 ###############

    cv2.destroyAllWindows()

    time.sleep(5)
    image = ldimshow.showImage()
    image = cv2.cvtColor(numpy.array(image), cv2.COLOR_RGB2BGR)
    clone = image.copy()
    cv2.namedWindow("image")
    cv2.setMouseCallback("image", click_and_crop_2) # 자동복구
    print("체력바를 마킹해주세요 >> ")

    while True:
        cv2.imshow("image", image)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("r"):
            image = clone.copy()

        elif key == ord("c"):
            if len(자동복구) == 2:
                roi2 = clone[자동복구[0][1]:자동복구[1][1], 자동복구[0][0]:자동복구[1][0]]

                hsv2 = cv2.cvtColor(roi2, cv2.COLOR_BGR2HSV)
                mask2 = cv2.inRange(hsv2, lower_white, upper_white)
                res2 = cv2.bitwise_and(roi2, roi2, mask=mask2)
                res2 = cv2.bitwise_not(res2)
                cv2.imshow("res2",res2)

                ocr_result2 = ocr.image_to_string(res2, config='--psm 6 -c tessedit_char_whitelist=0123456789')
                ocr_result2 = ocr_result2.replace('\n','')
                print("현재 체력은 : "+ocr_result2 +" 입니까? (맞으면 'qq' 아니면 'rr'로 다시 마킹해주세요 ")
                cv2.waitKey(0)
        elif key == ord("q"):
                break
    with open('junho.save', 'wb') as file:  # james.p 파일을 바이너리 쓰기 모드(wb)로 열기
        pickle.dump(억경, file)
        pickle.dump(자동복구, file)
    cv2.destroyAllWindows()
    time.sleep(5)
