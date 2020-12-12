import win32gui

def getWindowList():
    def callback(hwnd, hwnd_list: list):
        title = win32gui.GetWindowText(hwnd)
        if win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd) and title:
            hwnd_list.append((title, hwnd))
        return True
    output = []
    win32gui.EnumWindows(callback, output)
    return output

if __name__ == "__main__":
    print("\n".join("{: 9d} {}".format(h, t) for t, h in getWindowList()))