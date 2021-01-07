import time
import roitovalue, timetolog

def play():
    hwnd = roitovalue.hwnd()

    maxVal, x, y = roitovalue.searchIMGtoValue("img/suri.png", hwnd)                        # 수리 아이콘이 있으면
    
    if (maxVal >= 0.8):
        roitovalue.inClick(hwnd, x, y)                                                      # revive 클릭
        time.sleep(1)

        roitovalue.searchIMG("img/bobu.png", hwnd)                                          # 보부상 클릭 
        timetolog.msg("보부상 Click ,,,")
        time.sleep(2)

        maxVal, x, y = roitovalue.searchIMGtoValue("img/usingstore.png", hwnd)              # 상점이동 클릭
        if (maxVal >= 0.8):
            roitovalue.inClick(hwnd, x, y)
            timetolog.msg("상점 이동  Click ,,,")
            time.sleep(3)

            maxVal, x, y = roitovalue.searchIMGtoValue("img/suri2.png", hwnd)               # 수리2 클릭
            if (maxVal >= 0.8):
                roitovalue.inClick(hwnd, x, y)
                timetolog.msg("수리  Click ,,,")
                time.sleep(1)

                maxVal, x, y = roitovalue.searchIMGtoValue("img/allsuri.png", hwnd)         # allsuri 클릭
                if (maxVal >= 0.8):
                    roitovalue.inClick(hwnd, x, y)
                    timetolog.msg("전체 수리  Click ,,,")
                    time.sleep(1)

                    roitovalue.sendKeyMsg(hwnd, roitovalue.char2key('m'))                   # 수리 완료
                    timetolog.msg("수리 완료 ,,,")
    return None


