import time
import pickle
import os
import macro
import cropping_01, cropping_02

if os.path.isfile("junho.save"):
    with open('junho.save', 'rb') as file:  # james.p 파일을 바이너리 읽기 모드(rb)로 열기
        억경 = pickle.load(file)
        자동복구 = pickle.load(file)
else:
    cropping_01.crop()

if os.path.isfile("junho2.save"):
    with open('junho2.save', 'rb') as file:  # james.p 파일을 바이너리 읽기 모드(rb)로 열기
        레벨 = pickle.load(file)
        총강화횟수 = pickle.load(file)
        다음강화횟수 = pickle.load(file)
else:
    cropping_02.crop()

#메인
print("------지히는 노예사장-------")

#카톡이 안될 시에 주석을 풀고 해결함
#1) https://kauth.kakao.com/oauth/authorize?response_type=code&client_id=c0b365f99bd3f43c2f410d340539d099&redirect_uri=https://localhost.com
#2) 코드를 getToken에 적음
#kakao.getToken()
#kakao.sendKaKaoToAga("카톡테스트1")
#kakao.refreshToken()
#kakao.sendKaKaoToAga("카톡테스트2")
#
while True:
    macro.ones()
    time.sleep(10)
