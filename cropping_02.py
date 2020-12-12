import pytesseract as ocr
import numpy as np
import pickle
import ldimshow
import numpy
import cv2
import time

# 변수명 #
레벨 = []  # 레벨
cropping_레벨 = False  # 레벨 크로핑
총강화횟수 = []  # 총강화횟수
cropping_총강화횟수 = False  # 총강화횟수 크로핑
다음강화횟수 = []  # 총강화횟수
cropping_다음강화횟수 = False  # 다음강화횟수 크로핑
ocr_result = ""
ocr_result2 = ""
lower_white = np.array([0, 0, 168], dtype=np.uint8)
upper_white = np.array([172, 111, 255], dtype=np.uint8)
ocr.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

################## 레벨 ##################
def crop():

    def click_and_crop_1(event, x, y, flags, param):  # 레벨
        global 레벨, cropping_레벨

        # 왼쪽 마우스가 클릭되면 (x, y) 좌표 기록을 시작하고
        # cropping = True로 만들어 줍니다.
        if event == cv2.EVENT_LBUTTONDOWN:
            레벨 = [(x, y)]
            cropping_레벨 = True

        elif event == cv2.EVENT_LBUTTONUP:
            레벨.append((x, y))
            cropping_레벨 = False

            cv2.rectangle(image, 레벨[0], 레벨[1], (0, 255, 0), 2)
            cv2.imshow("image", image)

    def click_and_crop_2(event, x, y, flags, param):  # 총강화횟수
        global 총강화횟수, cropping_총강화횟수

        # 왼쪽 마우스가 클릭되면 (x, y) 좌표 기록을 시작하고
        # cropping = True로 만들어 줍니다.
        if event == cv2.EVENT_LBUTTONDOWN:
            총강화횟수 = [(x, y)]
            cropping_총강화횟수 = True

        elif event == cv2.EVENT_LBUTTONUP:
            총강화횟수.append((x, y))
            cropping_총강화횟수 = False

            cv2.rectangle(image, 총강화횟수[0], 총강화횟수[1], (0, 255, 0), 2)
            cv2.imshow("image", image)

    def click_and_crop_3(event, x, y, flags, param):  # 다음강화횟수
        global 다음강화횟수, cropping_다음강화횟수

        # 왼쪽 마우스가 클릭되면 (x, y) 좌표 기록을 시작하고
        # cropping = True로 만들어 줍니다.
        if event == cv2.EVENT_LBUTTONDOWN:
            다음강화횟수 = [(x, y)]
            cropping_다음강화횟수 = True

        elif event == cv2.EVENT_LBUTTONUP:
            다음강화횟수.append((x, y))
            cropping_다음강화횟수 = False

            cv2.rectangle(image, 다음강화횟수[0], 다음강화횟수[1], (0, 255, 0), 2)
            cv2.imshow("image", image)


################## 레벨 ##################
    time.sleep(5)
    image = ldimshow.showImage()
    image = cv2.cvtColor(numpy.array(image), cv2.COLOR_RGB2BGR)
    clone = image.copy()
    cv2.namedWindow("image")
    cv2.setMouseCallback("image", click_and_crop_1) # 레벨 확인하기
    print("레벨을 마킹해주세요 >> ")

    while True:
        cv2.imshow("image", image)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("r"):
            image = clone.copy()

        elif key == ord("c"):
            if len(레벨) == 2:
                roi = clone[레벨[0][1]:레벨[1][1], 레벨[0][0]:레벨[1][0]]
                hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

                mask = cv2.inRange(hsv, lower_white, upper_white)
                res = cv2.bitwise_and(roi, roi, mask=mask)
                res = cv2.bitwise_not(res)
                cv2.imshow("res",res)

                ocr_result = ocr.image_to_string(res, config='--psm 6 -c tessedit_char_whitelist=0123456789')
                ocr_result = ocr_result.replace('\n♀','')

                print("현재 레벨은 : "+ocr_result +" 입니까? (맞으면 'qq' 아니면 'rr'로 다시 마킹해주세요 ")
                cv2.waitKey(0)
        elif key == ord("q"):
                break

    ############### 총강화횟수 ###############

    cv2.destroyAllWindows()

    time.sleep(6)
    image = ldimshow.showImage()
    image = cv2.cvtColor(numpy.array(image), cv2.COLOR_RGB2BGR)
    clone = image.copy()
    cv2.namedWindow("image")
    cv2.setMouseCallback("image", click_and_crop_2) # 총강화횟수
    print("총강화횟수 를 마킹해주세요 >> ")

    while True:
        cv2.imshow("image", image)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("r"):
            image = clone.copy()

        elif key == ord("c"):
            if len(총강화횟수) == 2:
                roi2 = clone[총강화횟수[0][1]:총강화횟수[1][1], 총강화횟수[0][0]:총강화횟수[1][0]]

                hsv2 = cv2.cvtColor(roi2, cv2.COLOR_BGR2HSV)
                mask2 = cv2.inRange(hsv2, lower_white, upper_white)
                res2 = cv2.bitwise_and(roi2, roi2, mask=mask2)
                res2 = cv2.bitwise_not(res2)
                cv2.imshow("res2",res2)

                ocr_result2 = ocr.image_to_string(res2, config='--psm 6 -c tessedit_char_whitelist=0123456789')
                ocr_result2 = ocr_result2.replace('\n♀','')
                print("현재 총강화횟수는 : "+ocr_result2 +" 입니까? (맞으면 'qq' 아니면 'rr'로 다시 마킹해주세요 ")
                cv2.waitKey(0)
        elif key == ord("q"):
                break

    ############### 다음강화횟수 ###############

    cv2.destroyAllWindows()

    time.sleep(5)
    image = ldimshow.showImage()
    image = cv2.cvtColor(numpy.array(image), cv2.COLOR_RGB2BGR)
    clone = image.copy()
    cv2.namedWindow("image")
    cv2.setMouseCallback("image", click_and_crop_3) # 다음강화횟수
    print("다음강화횟수를 마킹해주세요 >> ")

    while True:
        cv2.imshow("image", image)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("r"):
            image = clone.copy()

        elif key == ord("c"):
            if len(다음강화횟수) == 2:
                roi3 = clone[다음강화횟수[0][1]:다음강화횟수[1][1], 다음강화횟수[0][0]:다음강화횟수[1][0]]

                hsv3 = cv2.cvtColor(roi3, cv2.COLOR_BGR2HSV)
                mask3 = cv2.inRange(hsv3, lower_white, upper_white)
                res3 = cv2.bitwise_and(roi3, roi3, mask=mask3)
                res3 = cv2.bitwise_not(res3)
                cv2.imshow("res3",res3)

                ocr_result3 = ocr.image_to_string(res3, config='--psm 6 -c tessedit_char_whitelist=0123456789')
                ocr_result3 = ocr_result3.replace('\n♀','')
                print("현재 다음강화횟수은 : "+ocr_result3 +" 입니까? (맞으면 'qq' 아니면 'rr'로 다시 마킹해주세요 ")
                cv2.waitKey(0)
        elif key == ord("q"):
                break

    with open('junho2.save', 'wb') as file:  # james.p 파일을 바이너리 쓰기 모드(wb)로 열기
        pickle.dump(레벨, file)
        pickle.dump(총강화횟수, file)
        pickle.dump(다음강화횟수, file)
    cv2.destroyAllWindows()
