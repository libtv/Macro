from datetime import datetime

def whattime():
    return "{:%Y-%m-%d %H.%M.%S}".format(datetime.now())

def msg(txt):
    print(whattime(), " : ", txt)