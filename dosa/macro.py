import pickle
import eokkyong, revive, suri
import kakao
import roitovalue, timetolog

class Macro:
    
    def __init__(self, flag):
        self.__flag = flag

        with open('junho.save', 'rb') as file:                                                  # james.p 파일을 바이너리 읽기 모드(rb)로 열기
            self.__억경 = pickle.load(file)
            self.__자동복구 = pickle.load(file)
            
        self.__flag = int(roitovalue.check_revive(self.__자동복구))
    
    def ones(self):
        hwnd = roitovalue.hwnd()

        #죽었을 때 체크하기(1)
        maxVal, x, y = roitovalue.searchIMGtoValue("img/die.png", hwnd)                     # 유령상태 확인
        if (maxVal >= 0.8):                                                                 # 죽었을 때
            roitovalue.inClick(hwnd, x, y)                                                  # 유령상태 클릭
            self.__flag = int(roitovalue.check_revive(self.__자동복구))
            return None

        #죽었을 때 체크하기(2)
        if (self.__flag == 1):
            revive.play()
            self.__flag = int(roitovalue.check_revive(self.__자동복구))
            timetolog.msg("체력바가 보이지 않거나 죽었을 경우 나타나는 메시지입니다. 캐릭터가 죽은 경우에 잠시 후 복구됩니다.")
            kakao.sendKaKaoToAga("체력바가 보이지 않거나 죽었을 경우 나타나는 메시지입니다. 캐릭터가 죽은 경우에 잠시 후 복구됩니다.")                                            # 카톡보내기
            return None
        
        else:
            #죽지 않았으면 억경 체크함
            억경_value = roitovalue.check(self.__억경, j=-3) # -3으로 변경하자
            timetolog.msg("현재 억경 : " + str(억경_value))
            suri_max, x2, y2 = roitovalue.searchIMGtoValue("img/weaponbreak.png", hwnd)                     # 수리해야하는지 확인
            

            if (억경_value >= 200): # 억경이 200개 이상이면 
                timetolog.msg("억경이 꽉 찼습니다. 카톡과 억경팔러 갈게요~")
                kakao.sendKaKaoToAga("억경이 다 꽉찼네요!!")                                            # 카톡보내기
                eokkyong.play()
                timetolog.msg("억경을 정상적으로 처리하였습니다.")
                kakao.sendKaKaoToAga("억경을 정상적으로 처리하였습니다.")                                  # 카톡보내기
                return None
                
            # 수리를 해야할 때
            if (suri_max >= 0.8):                                                                
                timetolog.msg("장비를 수리하도록 하겠습니다.")
                suri.play()
                return None        
