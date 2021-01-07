import time
import roitovalue, timetolog

def play():
    hwnd = roitovalue.hwnd()

    maxVal, x, y = roitovalue.searchIMGtoValue("img/revive.png", hwnd)                      # revive 확인해서
    
    if (maxVal >= 0.8):
        roitovalue.inClick(hwnd, x, y)                                                      # revive 클릭
        time.sleep(5)
        roitovalue.inClick(hwnd, 888, 456)                                                  # 따라가기(좌표만)
        time.sleep(0.5)
        roitovalue.sendKeyMsg(hwnd, roitovalue.char2key('v'))                               # 자동사냥
        timetolog.msg("자동사냥 Click ,,,")
        return None

    roitovalue.searchIMG("img/first.png", hwnd)                                             # 1번 클릭

    maxVal, x, y = roitovalue.searchIMGtoValue("img/revive.png", hwnd)                      # revive 확인해서
    
    if (maxVal >= 0.8):
        roitovalue.inClick(hwnd, x, y)                                                      # revive 클릭
        time.sleep(4)
        roitovalue.inClick(hwnd, 888, 456)                                                  # 따라가기(좌표만)
        time.sleep(0.5)
        roitovalue.sendKeyMsg(hwnd, roitovalue.char2key('v'))                               # 자동사냥
        timetolog.msg("자동사냥 Click ,,,")
        return None

    return None


