import json
import requests
import win32con, win32api, win32gui, time

def refreshToken():
    with open('kakao_token.json') as json_file:
        kakao_tokken = json.load(json_file)
        json_file.close()

    url = "https://kauth.kakao.com/oauth/token"
    data = {
        "grant_type": "refresh_token",
        "client_id": "", #rest API
        "refresh_token": str(kakao_tokken.get('refresh_token'))
    }
    response = requests.post(url, data=data)
    tokens = response.json()

    kakao_tokken['access_token'] = str(tokens.get('access_token'))
    kakao_tokken['token_type'] = str(tokens.get('token_type'))
    kakao_tokken['expires_in'] = str(tokens.get('expires_in'))

    if tokens.get('refresh_token') != None:
        kakao_tokken['refresh_token'] = str(tokens.get('refresh_token'))
    if tokens.get('refresh_token_expires_in') != None:
        kakao_tokken['refresh_token_expires_in'] = str(tokens.get('refresh_token_expires_in'))
        
    with open("kakao_token.json", "w") as fp:
        json.dump(kakao_tokken, fp)
        fp.close()
    print("카카오톡의 Access Token을 새로 변경하였습니다.")


def getToken():
    url = "https://kauth.kakao.com/oauth/token"

    data = {
        "grant_type": "authorization_code",
        "client_id": "",  # rest API
        "redirect_uri": "https://localhost.com",
        "code": ""  # code

    }
    response = requests.post(url, data=data)
    tokens = response.json()
    print(tokens)
    with open("kakao_token.json", "w") as fp:
        json.dump(tokens, fp)
        fp.close()


def getFriendsList():
    with open('kakao_token.json') as json_file:
        kakao_tokken = json.load(json_file)
        json_file.close()

    header = {"Authorization": 'Bearer ' + str(kakao_tokken.get('access_token'))}
    url = "https://kapi.kakao.com/v1/api/talk/friends?limit=1"  # 친구 정보 요청

    result = json.loads(requests.get(url, headers=header).text)

    friends_list = result.get("elements")
    friends_id = []

    print(requests.get(url, headers=header).text)
    print(friends_list)

    for friend in friends_list:
        friends_id.append(str(friend.get("uuid")))

        return friends_id


def sendKaKaoToAga(text):
    with open('kakao_token.json') as json_file:
        kakao_tokken = json.load(json_file)
        json_file.close()

    url = "https://kapi.kakao.com/v1/api/talk/friends/message/default/send"

    # 사용자 토큰
    headers = {
        "Authorization": "Bearer " + str(kakao_tokken.get('access_token'))
    }

    data = {
        "receiver_uuids": json.dumps(['친구 코드 번호']),
        "template_object": json.dumps({"object_type": "text",
                                       "text": text,
                                       "link": {
                                           "web_url": "www.naver.com"
                                       }
                                       })
    }

    response = requests.post(url, headers=headers, data=data)
    if str(response.json().get('msg')).find("exist") != -1:
        refreshToken()  # 만료되어서 찾아야함
    elif str(response.json().get('msg')).find("expired") != -1:
        refreshToken()  # 만료되어서 찾아야함
    elif str(response.json().get('msg')).find("API limit") != -1:
        limitAPItoSend(text) # 제한이 끝나서 카톡을 유동적으로 보냄

def limitAPItoSend(text):
    hwnd = win32gui.FindWindow(None, '울애기^^❤')
    hwnd = win32gui.FindWindowEx(hwnd, None, "RICHEDIT50W", None)
    win32api.SendMessage(hwnd, win32con.WM_SETTEXT, 0, text)
    SendReturn(hwnd)

def SendReturn(hwnd):
    win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
    time.sleep(0.01)
    win32api.PostMessage(hwnd, win32con.WM_KEYUP, win32con.VK_RETURN, 0)

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
