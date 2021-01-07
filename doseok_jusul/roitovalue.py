import ldimshow
import cv2
import numpy
import pytesseract as ocr
import time, timetolog, kakao
import win32con, win32gui
import ctypes, ctypes.wintypes
import revive

lower_white = numpy.array([0, 0, 168], dtype=numpy.uint8)
upper_white = numpy.array([172, 111, 255], dtype=numpy.uint8)

ocr.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

def check(reroi, i=None, j=None): # 숫자가 인식이 안되면 재귀호출 
    try:
        image = ldimshow.showImage()
        image = cv2.cvtColor(numpy.array(image), cv2.COLOR_RGB2BGR)
        roi = image[reroi[0][1]:reroi[1][1], reroi[0][0]:reroi[1][0]]

        # 억경
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower_white, upper_white)
        res = cv2.bitwise_and(roi, roi, mask=mask)
        res = cv2.bitwise_not(res)
        cv2.destroyAllWindows()                                                     # 공용
        
        ocr_result = ocr.image_to_string(res, config='--psm 6 -c tessedit_char_whitelist=0123456789')
        ocr_result = ocr_result.replace('\n', '')
        ocr_result = ocr_result[i:j]
        ocr_result = int(ocr_result)
        return ocr_result
    except:
        timetolog.msg("일시적인 프레임 오류로 처리되지 않았습니다 잠시후 다시 시도합니다. 2초 후 다시 실행됩니다.")
        kakao.sendKaKaoToAga("이 오류가 지속적으로 발생 될 시 매크로와 화면을 확인하시기 바랍니다.")  # 카톡보내기
        time.sleep(4)
        return check(reroi, i, j)

def check_revive(reroi, i=None, j=None): # 체력바가 0이거나 오류가 뜨면 return 1, 아닐 경우 return 0 
    try:
        image = ldimshow.showImage()
        image = cv2.cvtColor(numpy.array(image), cv2.COLOR_RGB2BGR)
        roi = image[reroi[0][1]:reroi[1][1], reroi[0][0]:reroi[1][0]]

        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower_white, upper_white)
        res = cv2.bitwise_and(roi, roi, mask=mask)
        res = cv2.bitwise_not(res)
        cv2.destroyAllWindows()                                                     # 공용
        
        ocr_result = ocr.image_to_string(res, config='--psm 6 -c tessedit_char_whitelist=0123456789')
        ocr_result = ocr_result.replace('\n', '')
        ocr_result = ocr_result[i:j]
        ocr_result = int(ocr_result)
        
        if (ocr_result == 0):
            return 1
        else:
            return 0
    except:
        return 1

def hwnd():
    hwnd = win32gui.FindWindow(None, 'LDPlayer')
    hwnd = win32gui.FindWindowEx(hwnd, 0, "RenderWindow", "TheRender")
    return hwnd

def inClick(hwnd, x, y):
    x = x
    y = y -30
    lParam = (y << 16) | x
    SendMessage = ctypes.windll.user32.SendMessageW
    SendMessage(hwnd, win32con.WM_LBUTTONDOWN, 0, lParam)
    SendMessage(hwnd, win32con.WM_LBUTTONUP, 0, lParam)
    time.sleep(0.2)

def inDrag(hwnd, x1, y1, x2, y2, drag_cnt): # 드래그함수
#hwnd = roitovalue.hwnd()
#roitovalue.inDrag(hwnd, 987, 652,985, 379, 2)
    x_move = x1 - x2
    y_move = y1 - y2
    SendMessage = ctypes.windll.user32.SendMessageW
    
    for i in range(1, drag_cnt):
        time.sleep(0.5)
        lParam = x1|y1 << 16
        SendMessage(hwnd, 0x201, 1, lParam)

        x_cnt = 1
        y_cnt = 1

        for i in range(1, int(abs(x_move))):
            for i in range(1, int(abs(y_move))):
                time.sleep(0.001)

                if (x_move >= 0) & (y_move >= 0):
                    x = x1 - x_cnt
                    y = y1 - y_cnt
                    lParam = x | y << 16
                    x_cnt = x_cnt + 1
                    y_cnt = y_cnt + 1
                elif (x_move >= 0) & (y_move <= 0):
                    x = x1 - x_cnt
                    y = y1 + y_cnt
                    lParam = x | y << 16
                    x_cnt = x_cnt + 1
                    y_cnt = y_cnt + 1
                elif (x_move <= 0) & (y_move >= 0):
                    x = x1 + x_cnt
                    y = y1 - y_cnt
                    lParam = x | y << 16
                    x_cnt = x_cnt + 1
                    y_cnt = y_cnt + 1
                elif (x_move <= 0) & (y_move <= 0):
                    x = x1 + x_cnt
                    y = y1 + y_cnt
                    lParam = x | y << 16
                    x_cnt = x_cnt + 1
                    y_cnt = y_cnt + 1

                SendMessage(hwnd, 0x200, 1, lParam)

        SendMessage(hwnd, 0x202, 0, lParam)
    

def searchIMG(img, hwnd):
    src = ldimshow.showImage()
    src = cv2.cvtColor(numpy.array(src), cv2.COLOR_RGB2GRAY)
    templit = cv2.imread(img, cv2.IMREAD_GRAYSCALE)

    result = cv2.matchTemplate(src, templit, cv2.TM_CCOEFF_NORMED)
    minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(result)
    x, y = maxLoc
    h, w = templit.shape
    cv2.destroyAllWindows()                                                     # 공용

    if (maxVal >= 0.8):
        x = int((x + (x + w)) / 2)
        y = int((y + (y + h)) / 2)
        inClick(hwnd, x, y)
    else:
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
    cv2.destroyAllWindows()                                                     # 공용

    if (maxVal >= 0.8):
        x = int((x + (x + w)) / 2)
        y = int((y + (y + h)) / 2)
        return x, y
    else:
        print("wait...")
        time.sleep(2)
        return searchIMGtoXY(img, hwnd)

def searchIMGtoValue(img, hwnd):
    src = ldimshow.showImage()
    src = cv2.cvtColor(numpy.array(src), cv2.COLOR_RGB2GRAY)
    templit = cv2.imread(img, cv2.IMREAD_GRAYSCALE)

    result = cv2.matchTemplate(src, templit, cv2.TM_CCOEFF_NORMED)
    minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(result)
    x, y = maxLoc
    h, w = templit.shape

    cv2.destroyAllWindows()                                                     # 공용
    return maxVal, x, y

def char2key(c):
    result = ctypes.windll.user32.VkKeyScanW(ord(c))
    vk_key = result & 0xFF

    return vk_key

def sendKeyMsg(hwnd, key_code):
    SendMessage = ctypes.windll.user32.SendMessageW
    SendMessage(hwnd, win32con.WM_KEYDOWN, key_code, 0)
    time.sleep(0.2)
    SendMessage(hwnd, win32con.WM_KEYUP, key_code, 0)
    time.sleep(0.2)
