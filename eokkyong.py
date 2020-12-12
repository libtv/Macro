import win32con, win32gui
import ctypes, ctypes.wintypes
import time, pickle
import ldimshow, cv2, numpy
import roitovalue, timetolog

테스트 = []
cropping_테스트 = False  # 크로핑

def char2key(c):
    result = ctypes.windll.user32.VkKeyScanW(ord(c))
    vk_key = result & 0xFF

    return vk_key

def sendKeyMsg(hwnd, key_code):
    """
    模拟按键
    :param hwnd: 窗体句柄
    :param key_code: 按键码，在win32con下，比如win32con.VK_F1
    :return:
    """
    SendMessage = ctypes.windll.user32.SendMessageW
    SendMessage(hwnd, win32con.WM_KEYDOWN, key_code, 0)
    time.sleep(0.2)
    SendMessage(hwnd, win32con.WM_KEYUP, key_code, 0)
    time.sleep(0.2)

def inClick(hwnd, x, y):
    x = x
    y = y -30
    lParam = (y << 16) | x
    SendMessage = ctypes.windll.user32.SendMessageW
    SendMessage(hwnd, win32con.WM_LBUTTONDOWN, 0, lParam)
    SendMessage(hwnd, win32con.WM_LBUTTONUP, 0, lParam)
    time.sleep(0.2)

def searchIMG(img, hwnd):
    src = ldimshow.showImage()
    src = cv2.cvtColor(numpy.array(src), cv2.COLOR_RGB2GRAY)
    templit = cv2.imread(img, cv2.IMREAD_GRAYSCALE)

    result = cv2.matchTemplate(src, templit, cv2.TM_CCOEFF_NORMED)
    minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(result)
    x, y = maxLoc
    h, w = templit.shape

    if (maxVal >= 0.8):
        cv2.destroyAllWindows()
        x = int((x + (x + w)) / 2)
        y = int((y + (y + h)) / 2)
        inClick(hwnd, x, y)
    else:
        cv2.destroyAllWindows()
        print("wait...")
        time.sleep(2)
        searchIMG(img, hwnd)

def searchIMGtoXY(img, hwnd):
    src = ldimshow.showImage()
    src = cv2.cvtColor(numpy.array(src), cv2.COLOR_RGB2GRAY)
    templit = cv2.imread(img, cv2.IMREAD_GRAYSCALE)

    result = cv2.matchTemplate(src, templit, cv2.TM_CCOEFF_NORMED)
    minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(result)
    x, y = maxLoc
    h, w = templit.shape

    if (maxVal >= 0.8):
        cv2.destroyAllWindows()
        x = int((x + (x + w)) / 2)
        y = int((y + (y + h)) / 2)
        return x, y
    else:
        cv2.destroyAllWindows()
        print("wait...")
        time.sleep(2)
        return searchIMGtoXY(img, hwnd)

def play():
    hwnd = win32gui.FindWindow(None, 'LDPlayer')
    hwnd = win32gui.FindWindowEx(hwnd, 0, "RenderWindow", "TheRender")
    with open('junho2.save', 'rb') as file:  # james.p 파일을 바이너리 읽기 모드(rb)로 열기
        레벨 = pickle.load(file)
        총강화횟수 = pickle.load(file)
        다음강화횟수 = pickle.load(file)
    time.sleep(1)

    # 키보드 입력
    sendKeyMsg(hwnd, char2key('m')) # 맵

    searchIMG("img/world.png", hwnd)                    # 세계전도
    timetolog.msg("세계전도 Click ,,,")
    time.sleep(1)

    searchIMG("img/bu.png", hwnd)                       # 부여성
    timetolog.msg("부여성 Click ,,,")
    time.sleep(1)

    searchIMG("img/small.png", hwnd)                    # 최소화
    timetolog.msg("최소화 Click ,,,")
    time.sleep(4)                                       # 좌표를 이용하기 때문에 시간적 여유를 준다.

    inClick(hwnd, 393, 599)                             # 도호귀인집(좌표만)
    timetolog.msg("도호귀인 Click ,,,")
    time.sleep(4)                                       # 좌표를 이용하기 때문에 시간적 여유를 준다.

    inClick(hwnd, 1150, 485)                            # 즉시이동(좌표만)
    timetolog.msg("즉시이동 Click ,,,")
    time.sleep(1)

    searchIMG("img/yes.png", hwnd)                      # 확인
    timetolog.msg("확인 Click ,,,")
    time.sleep(1)

    #레벨 체크하기
    # searchIMG 도호귀인 체크 후 ROI값 레벨 체크 후 레벨 변수에 넣음
    x, y = searchIMGtoXY("img/doho.png", hwnd)
    level = roitovalue.check(레벨, i=-1)
    timetolog.msg("현재 레벨의 뒷자리는 " + str(level) + " 입니다.")
    inClick(hwnd, x, y)                                 # 도호귀인 클릭
    timetolog.msg("도호귀인 Click ,,,.")
    time.sleep(1)

    searchIMG("img/strong.png", hwnd)                   # 신수강화 클릭
    timetolog.msg("신수강화 Click ,,,")
    time.sleep(4)                                       # 좌표를 이용하기 때문에 시간적 여유를 준다.

    inClick(hwnd, 336, 228)                             # 현무 클릭(좌표만)
    timetolog.msg("현무 Click ,,,")
    roitovalue.check(총강화횟수)                          # 시간 체크하기

    # 신수 팔기
    timetolog.msg("★★★신수를 팔도록 합니다.★★★")
    for i in range(25):
        inClick(hwnd, 1171, 492)    #위
        timetolog.msg(str(i+1) + "번째[위] 팔고있습니다...")

        if level == 3 or level == 8: # 레벨 3과 8에서
            totalcount = roitovalue.check(총강화횟수)
            nextcount = roitovalue.check(다음강화횟수)
            if nextcount - totalcount == 1:
                timetolog.msg("현재 레벨의 뒷자리가 " + str(level) + " 이므로 신수강화를 빠져나와 다시모읍니다.")
                break;
        time.sleep(0.5)

        inClick(hwnd, 1162, 669)    #아래
        timetolog.msg(str(i+1) + "번째[아래] 팔고있습니다...")

        if level == 3 or level == 8: # 레벨 3과 8에서
            totalcount = roitovalue.check(총강화횟수)
            nextcount = roitovalue.check(다음강화횟수)
            if nextcount - totalcount == 1:
                timetolog.msg("현재 레벨의 뒷자리가 " + str(level) + " 이므로 신수강화를 빠져나와 다시모읍니다.")
                break;
        time.sleep(0.5)

    sendKeyMsg(hwnd, char2key('m'))                         # 취소버튼
    timetolog.msg("취소 Click ,,,")
    time.sleep(4)                                           # 좌표를 이용하기 때문에 시간적 여유를 준다.

    # 그룹장으로 가기
    inClick(hwnd, 346, 94)                                  # 그룹클릭(좌표만)
    timetolog.msg("그룹 Click ,,,")
    time.sleep(1)

    searchIMG("img/king.png", hwnd)                         # 그룹장 클릭
    timetolog.msg("그룹장 Click ,,,")
    time.sleep(1)

    searchIMG("img/go.png", hwnd)
    timetolog.msg("따라가기 Click ,,,")                      # 그룹장 따라가기 클릭
    time.sleep(1)

    searchIMG("img/esc.png", hwnd)                          # 그룹닫기 클릭
    timetolog.msg("그룹 닫기 Click ,,,")
    time.sleep(4)                                           # 좌표를 이용하기 때문에 시간적 여유를 준다.

    inClick(hwnd, 888, 456)                                 # 따라가기(좌표만)
    time.sleep(0.5)
    sendKeyMsg(hwnd, char2key('v'))                         # 자동사냥
    timetolog.msg("자동사냥 Click ,,,")













# save 함수
# def searchIMG(img, hwnd):
#     src = ldimshow.showImage()
#     src = cv2.cvtColor(numpy.array(src), cv2.COLOR_RGB2GRAY)
#     templit = cv2.imread(img, cv2.IMREAD_GRAYSCALE)
# 
#     result = cv2.matchTemplate(src, templit, cv2.TM_CCOEFF_NORMED)
#     minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(result)
#     x, y = maxLoc
#     h, w = templit.shape
# 
#     if (maxVal >= 0.8):
#         #src = cv2.rectangle(src, (x, y), (x + w, y + h), (0, 255, 0), 2)
#         cv2.destroyAllWindows()
#         # print("이미지 발견")
#         # cv2.imshow("src", src)
#         # cv2.waitKey(0)
#         # cv2.destroyAllWindows()
#         x = int((x + (x + w)) / 2)
#         y = int((y + (y + h)) / 2)
#         inClick(hwnd, x, y)
#     else:
#         cv2.destroyAllWindows()
#         print("wait...")
#         time.sleep(2)
#         searchIMG(img, hwnd)

def show():
    def click_and_crop_3(event, x, y, flags, param):
        global 테스트, cropping_테스트

        if event == cv2.EVENT_LBUTTONDOWN:
            테스트 = [(x, y)]
            cropping_테스트 = True

        elif event == cv2.EVENT_LBUTTONUP:
            테스트.append((x, y))
            cropping_테스트 = False

            cv2.rectangle(image, 테스트[0], 테스트[1], (0, 255, 0), 2)
            cv2.imshow("image", image)
    image = ldimshow.showImage()
    image = cv2.cvtColor(numpy.array(image), cv2.COLOR_RGB2BGR)
    clone = image.copy()
    cv2.namedWindow("image")
    cv2.setMouseCallback("image", click_and_crop_3) # 억경 확인하기
    print("억경을 마킹해주세요 >> ")

    while True:
        cv2.imshow("image", image)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("r"):
            image = clone.copy()

        elif key == ord("c"):
            if len(테스트) == 2:
                print(str(테스트[0][0]+((테스트[1][0]-테스트[0][0])/2)) + " " + str(테스트[0][1]+((테스트[1][1]-테스트[0][1])/2)))
                cv2.waitKey(0)
        elif key == ord("q"):
            break