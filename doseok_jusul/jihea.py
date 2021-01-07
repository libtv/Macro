import os
from macro import *
import time
import cropping_01

if os.path.isfile("junho.save"):
    with open('junho.save', 'rb') as file:  # james.p 파일을 바이너리 읽기 모드(rb)로 열기
        억경 = pickle.load(file)
        자동복구 = pickle.load(file)
else:
    cropping_01.crop()
    
#메인
job = int(input("현재 직업은 무엇입니까? [도적은 0, 주술사는 1 설정] >> "))
print("체력바와 억경이 ld플레이어에 보이지 않을시 오류가 계속 뜨게 됩니다. 주의해주시기 바랍니다.")

#카톡이 안될 시에 주석을 풀고 해결함
#1) https://kauth.kakao.com/oauth/authorize?response_type=code&client_id=c0b365f99bd3f43c2f410d340539d099&redirect_uri=https://localhost.com
#2) 코드를 getToken에 적음
#kakao.getToken()
#kakao.sendKaKaoToAga("카톡테스트1")
#kakao.refreshToken()
#kakao.sendKaKaoToAga("카톡테스트2")


# 10초마다 한번씩
macros = Macro(0, job) # 억경, 자동수리, 도사 자동부활
while True:
    #억경, 자동수리, 도사 자동부활 
    macros.ones()
    time.sleep(10)

