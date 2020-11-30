import cv2
from PIL import ImageGrab
import numpy
import time
import pytesseract as ocr
import numpy as np
import pyautogui
ocr.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
import json
import requests
import pickle
import os
# lower_white = np.array([0, 0, 0], dtype=np.uint8)
# upper_white = np.array([0, 0, 255], dtype=np.uint8)

#lower_white2 = np.array([0, 0, 212], dtype=np.uint8)
#upper_white2 = np.array([131, 255, 255], dtype=np.uint8)

def refreshToken():
    kakao_tokken = ''
    with open('kakao_token.json') as json_file:
        kakao_tokken = json.load(json_file)
        
    url = "https://kauth.kakao.com/oauth/token"
    data = {
        "grant_type" : "refresh_token",
        "client_id"  : " ",
        "refresh_token" : str(kakao_tokken.get('refresh_token'))
    }
    response = requests.post(url, data=data)
    tokens = response.json()
    print(tokens)
    with open("kakao_token.json", "w") as fp:
        json.dump(tokens, fp)

def getToken():
    url = "https://kauth.kakao.com/oauth/token"

    data = {
        "grant_type" : "authorization_code",
        "client_id" : " ", # input rest API
        "redirect_uri" : " ", # input uri
        "code"         : " " # input code
        
    }
    response = requests.post(url, data=data)
    tokens = response.json()
    print(tokens)
    with open("kakao_token.json", "w") as fp:
        json.dump(tokens, fp)

def getFriendsList():
    kakao_tokken = ''
    with open('kakao_token.json') as json_file:
        kakao_tokken = json.load(json_file)
    
    header = {"Authorization": 'Bearer ' + str(kakao_tokken.get('access_token')) }
    url = "https://kapi.kakao.com/v1/api/talk/friends?limit=1" #친구 정보 요청

    result = json.loads(requests.get(url, headers=header).text)

    friends_list = result.get("elements")
    friends_id = []

    print(requests.get(url, headers=header).text)
    print(friends_list)

    for friend in friends_list:
        friends_id.append(str(friend.get("uuid")))

        return friends_id


def sendKaKaoToAga(text):
    kakao_tokken = ''
    with open('kakao_token.json') as json_file:
        kakao_tokken = json.load(json_file)
    
    url = "https://kapi.kakao.com/v1/api/talk/friends/message/default/send"

    # 사용자 토큰
    headers = {
        "Authorization": "Bearer " + str(kakao_tokken.get('access_token'))
    }

    data = {
        "receiver_uuids": " ", #친구 uuid
        "template_object": json.dumps({"object_type": "text",
                                       "text": text,
                                       "link": {
                                           "web_url": "www.naver.com"
                                       }
                                       })
    }

    response = requests.post(url, headers=headers, data=data)
    print(str(response.json()))
    if str(response.json().get('msg')).find("exist") != -1:
        refreshToken() #만료되어서 찾아야함

def sendKaKao(text):
    kakao_tokken = ''
    with open('kakao_token.json') as json_file:
        kakao_tokken = json.load(json_file)
        
    url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"

    # 사용자 토큰
    headers = {
        "Authorization": "Bearer " + str(kakao_tokken.get('access_token'))
    }

    data = {
        "template_object": json.dumps({"object_type": "text",
                                       "text": text,
                                       "link": {
                                           "web_url": "https://developers.kakao.com",
                                           "mobile_web_url": "https://developers.kakao.com"
                                       },
                                       "button_title": "바로 확인"
                                       })
    }

    response = requests.post(url, headers=headers, data=data)
    if response.json().get('result_code') == 0:
        print('메시지를 성공적으로 보냈습니다.')
    else:
        print('메시지를 성공적으로 보내지 못했습니다. 오류메시지 : ' + str(response.json()))

def click_and_crop_1(event, x, y, flags, param): #억경
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

def click_and_crop_2(event, x, y, flags, param): #자동복구
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

# 변수명 #
억경 = [] #억경
cropping_억경 = False #억경 크로핑
자동복구 = [] #자동복구
cropping_자동복구 = False #자동복구 크로핑
ocr_result = ""

lower_white = np.array([0,0,168], dtype=np.uint8)
upper_white = np.array([172,111,255], dtype=np.uint8)
ocr_result2 = ""
lower_white2 = np.array([0,0,168], dtype=np.uint8)
upper_white2 = np.array([172,111,255], dtype=np.uint8)

if os.path.isfile("junho.save"):
    with open('junho.save', 'rb') as file:  # james.p 파일을 바이너리 읽기 모드(rb)로 열기
        억경 = pickle.load(file)
        자동복구 = pickle.load(file)
else:
#########################################
################## 억경 ##################
#########################################

    time.sleep(5)
    image = ImageGrab.grab()
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
                ocr_result = ocr_result.replace('\n♀','')
                print("현재 억경은 : "+ocr_result +" 입니까? (맞으면 'qq' 아니면 'rr'로 다시 마킹해주세요 ")
                cv2.waitKey(0)
        elif key == ord("q"):
                break

    #########################################
    ############### 자동복구 ###############
    #########################################

    cv2.destroyAllWindows()

    time.sleep(5)
    image = ImageGrab.grab()
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
                mask2 = cv2.inRange(hsv2, lower_white2, upper_white2)
                res2 = cv2.bitwise_and(roi2, roi2, mask=mask2)
                res2 = cv2.bitwise_not(res2)
                cv2.imshow("res2",res2)
                
                ocr_result2 = ocr.image_to_string(res2, config='--psm 6 -c tessedit_char_whitelist=0123456789')
                ocr_result2 = ocr_result2.replace('\n♀','')
                print("현재 체력은 : "+ocr_result2 +" 입니까? (맞으면 'qq' 아니면 'rr'로 다시 마킹해주세요 ")
                cv2.waitKey(0)
        elif key == ord("q"):
                break

#########################################
################## 메인 ##################
#########################################
cv2.destroyAllWindows()

with open('junho.save', 'wb') as file:    # james.p 파일을 바이너리 쓰기 모드(wb)로 열기
    pickle.dump(억경, file)
    pickle.dump(자동복구, file)

while True:
    try:  # 반복처리 구문
        time.sleep(10)
        image = ImageGrab.grab()
        image = cv2.cvtColor(numpy.array(image), cv2.COLOR_RGB2BGR)
        clone = image.copy()
        clone2 = image.copy()
        roi = clone[억경[0][1]:억경[1][1], 억경[0][0]:억경[1][0]]
        roi2 = clone2[자동복구[0][1]:자동복구[1][1], 자동복구[0][0]:자동복구[1][0]]

        #억경
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower_white, upper_white)
        res = cv2.bitwise_and(roi, roi, mask=mask)
        res = cv2.bitwise_not(res)
        ocr_result = ocr.image_to_string(res, config='--psm 6 -c tessedit_char_whitelist=0123456789')
        ocr_result = ocr_result.replace('\n♀','')
        print("현재 억경 : " + ocr_result)

        #자동부활
        hsv2 = cv2.cvtColor(roi2, cv2.COLOR_BGR2HSV)
        mask2 = cv2.inRange(hsv2, lower_white2, upper_white2)
        res2 = cv2.bitwise_and(roi2, roi2, mask=mask2)
        res2 = cv2.bitwise_not(res2)
        ocr_result2 = ocr.image_to_string(res2, config='--psm 6 -c tessedit_char_whitelist=0123456789')
        ocr_result2 = ocr_result2.replace('\n♀','')
        print("현재 채력 : " + ocr_result2)

        # 억경이 다 꽉찼으면~~
        if "127" in ocr_result:
            sendKaKaoToAga("억경이 다 꽉찼네요!!")        #카톡보내기
            time.sleep(2)

        if (ocr_result2 == 'Q' or ocr_result2 == 'o' or ocr_result2 == '0' or ocr_result2 == 'O' or ocr_result2 == 'o0' or ocr_result2 == 'Oo'
         or ocr_result2 == 'oO' or ocr_result2 == 'Oo' or ocr_result2 == '0o' or ocr_result2 == '00'):
            sendKaKaoToAga("죽었어용 다시 부활할게요")  # 카톡보내기
            print("please wait...")
            time.sleep(25)
            pyautogui.press('~')
            time.sleep(2)
            pyautogui.press('num9')
            time.sleep(2)
            pyautogui.press('~')
            time.sleep(2)
        cv2.destroyAllWindows()
    except:
        print("일시적인 프레임 오류로 처리되지 않았습니다 잠시후 다시 시도합니다.")
        pass

cv2.destroyAllWindows()
