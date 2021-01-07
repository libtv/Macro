import time, pickle
import ldimshow, cv2, numpy
import roitovalue, timetolog

테스트 = []
cropping_테스트 = False  # 크로핑

def play():
    hwnd = roitovalue.hwnd()

    # 키보드 입력
    roitovalue.sendKeyMsg(hwnd, roitovalue.char2key('m')) # 맵

    roitovalue.searchIMG("img/world.png", hwnd)                    # 세계전도
    timetolog.msg("세계전도 Click ,,,")
    time.sleep(1)

    roitovalue.searchIMG("img/bu.png", hwnd)                       # 부여성
    timetolog.msg("부여성 Click ,,,")
    time.sleep(1)

    roitovalue.searchIMG("img/small.png", hwnd)                    # 최소화
    timetolog.msg("최소화 Click ,,,")
    time.sleep(4)                                       # 좌표를 이용하기 때문에 시간적 여유를 준다.

    roitovalue.inClick(hwnd, 393, 599)                             # 도호귀인집(좌표만)
    timetolog.msg("도호귀인 Click ,,,")
    time.sleep(4)                                       # 좌표를 이용하기 때문에 시간적 여유를 준다.

    roitovalue.inClick(hwnd, 1150, 485)                            # 즉시이동(좌표만)
    timetolog.msg("즉시이동 Click ,,,")
    time.sleep(1)

    roitovalue.searchIMG("img/yes.png", hwnd)                      # 확인
    timetolog.msg("확인 Click ,,,")
    time.sleep(1)

    x, y = roitovalue.searchIMGtoXY("img/doho.png", hwnd)
    roitovalue.inClick(hwnd, x, y)                                 # 도호귀인 클릭
    timetolog.msg("도호귀인 Click ,,,.")
    time.sleep(1)

    roitovalue.searchIMG("img/strong.png", hwnd)                   # 신수강화 클릭
    timetolog.msg("신수강화 Click ,,,")
    time.sleep(1)                                       

############################################ 설정하는 곳 #################################################
##########################################################################################################
    roitovalue.searchIMG("img/jujak.png", hwnd)                    # 주작 클릭
    timetolog.msg("주작 Click ,,,")
    time.sleep(1)

    # 신수 팔기
    timetolog.msg("★★★신수를 팔도록 합니다.★★★")
    for i in range(14):             # 반복 횟수 ( 4신수 : 14, 3신수 : 26 )
        # 로직은 억경 클릭하고 다른데 한번 더 클릭 한 후 억경 비교 후 기다리기
        # 억경 클릭하고 다른데 한번 더 클릭한 후 억경 비교 후 기다리기
        
        roitovalue.inClick(hwnd, 1171, 492)    # 위 
        timetolog.msg(str(i+1) + "번째[위] 팔고있습니다...")
        time.sleep(0.2)
        roitovalue.inClick(hwnd, 930, 280)
        
        time.sleep(0.4)

        roitovalue.inClick(hwnd, 1162, 669)    # 아래
        timetolog.msg(str(i+1) + "번째[아래] 팔고있습니다...")
        time.sleep(0.2)
        roitovalue.inClick(hwnd, 930, 280)
        
        time.sleep(0.4)

    roitovalue.sendKeyMsg(hwnd, roitovalue.char2key('m'))       # 취소버튼
    timetolog.msg("취소 Click ,,,")
    time.sleep(4)                                               # 좌표를 이용하기 때문에 시간적 여유를 준다.

    # 그룹장으로 가기
    roitovalue.inClick(hwnd, 346, 94)                           # 그룹클릭(좌표만)
    timetolog.msg("그룹 Click ,,,")
    time.sleep(1)

    roitovalue.searchIMG("img/king.png", hwnd)                  # 그룹장 클릭
    timetolog.msg("그룹장 Click ,,,")
    time.sleep(1)

    roitovalue.searchIMG("img/go.png", hwnd)
    timetolog.msg("따라가기 Click ,,,")                         # 그룹장 따라가기 클릭
    time.sleep(1)

    roitovalue.searchIMG("img/esc.png", hwnd)                   # 그룹닫기 클릭
    timetolog.msg("그룹 닫기 Click ,,,")
    time.sleep(4)                                               # 좌표를 이용하기 때문에 시간적 여유를 준다.

    roitovalue.inClick(hwnd, 888, 456)                          # 따라가기(좌표만)
    time.sleep(0.5)
    roitovalue.sendKeyMsg(hwnd, roitovalue.char2key('v'))       # 자동사냥
    timetolog.msg("자동사냥 Click ,,,")


