import time
import cv2
import pickle
import eokkyong
import kakao
import roitovalue, timetolog

# 현재 자동복구는 시행하지않음
# if (int(자동복구_value) == 0):
#     kakao.sendKaKaoToAga("죽었어용 다시 부활할게요")  # 카톡보내기
#     print("please wait...")
#     time.sleep(25)

def ones():
    with open('junho.save', 'rb') as file:                                                  # james.p 파일을 바이너리 읽기 모드(rb)로 열기
        억경 = pickle.load(file)
        자동복구 = pickle.load(file)

    억경_value = roitovalue.check(억경, j=-2)
    자동복구_value = roitovalue.check(자동복구)

    timetolog.msg("현재 억경 : " + str(억경_value) + ", 현재 채력 : " + str(자동복구_value))

    if 억경_value > 174:
        timetolog.msg("억경이 꽉 찼습니다. 카톡과 억경팔러 갈게요~")
        kakao.sendKaKaoToAga("억경이 다 꽉찼네요!!")                                            # 카톡보내기
        eokkyong.play()
        time.sleep(2)
        timetolog.msg("억경을 정상적으로 처리하였습니다.")
        kakao.sendKaKaoToAga("억경을 정상적으로 처리하였습니다.")                                  # 카톡보내기

    cv2.destroyAllWindows()
