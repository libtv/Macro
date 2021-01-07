import time
import roitovalue, timetolog

def play(who):
    hwnd = roitovalue.hwnd()

    roitovalue.inClick(hwnd, 346, 94)                           # 그룹클릭(좌표만)
    timetolog.msg("그룹 Click ,,,")
    time.sleep(1)

    roitovalue.searchIMG(who, hwnd)                             # 그룹장 클릭
    timetolog.msg("넘길 사람 Click ,,,")
    time.sleep(1)

    roitovalue.searchIMG("img/mandating_group.png", hwnd)       # 그룹장 위임 클릭
    timetolog.msg("그룹장 위임 ,,,")
    time.sleep(1)
    
    roitovalue.searchIMG("img/esc.png", hwnd)                   # 그룹닫기 클릭
    timetolog.msg("그룹 닫기 Click ,,,")
    time.sleep(1)                                               # 좌표를 이용하기 때문에 시간적 여유를 준다.
