import json
import requests
import win32con, win32api, win32gui, time

def sendKaKaoToAga(text):
    limitAPItoSend(text)

def limitAPItoSend(text):
    hwnd = win32gui.FindWindow(None, '울애기^^❤')
    hwnd = win32gui.FindWindowEx(hwnd, None, "RICHEDIT50W", None)
    win32api.SendMessage(hwnd, win32con.WM_SETTEXT, 0, text)
    SendReturn(hwnd)

def SendReturn(hwnd):
    win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
    time.sleep(0.01)
    win32api.PostMessage(hwnd, win32con.WM_KEYUP, win32con.VK_RETURN, 0)

