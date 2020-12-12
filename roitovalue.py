import ldimshow
import cv2
import numpy
import pytesseract as ocr
import time, timetolog, kakao

lower_white = numpy.array([0, 0, 168], dtype=numpy.uint8)
upper_white = numpy.array([172, 111, 255], dtype=numpy.uint8)
ocr.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

def check(reroi, i=None, j=None):
    try:
        image = ldimshow.showImage()
        image = cv2.cvtColor(numpy.array(image), cv2.COLOR_RGB2BGR)
        roi = image[reroi[0][1]:reroi[1][1], reroi[0][0]:reroi[1][0]]

        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower_white, upper_white)
        res = cv2.bitwise_and(roi, roi, mask=mask)
        res = cv2.bitwise_not(res)
        ocr_result = ocr.image_to_string(res, config='--psm 6 -c tessedit_char_whitelist=0123456789')
        ocr_result = ocr_result.replace('\n♀', '')
        ocr_result = ocr_result[i:j]
        ocr_result = int(ocr_result)
        return ocr_result
    except:
        timetolog.msg("일시적인 프레임 오류로 처리되지 않았습니다 잠시후 다시 시도합니다. 2초 후 다시 실행됩니다.")
        kakao.sendKaKaoToAga("이 오류가 지속적으로 발생 될 시 매크로와 화면을 확인하시기 바랍니다.")  # 카톡보내기
        time.sleep(2)
        return check(reroi, i, j)
