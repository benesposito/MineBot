# I, Ben Esposito, copied most of this file from Sentdex's https://github.com/Sentdex/pygta5, who copied it from a Stack Overflow post linked below. I modified it slightly.
# If this is in any way illegal, I will immediately take it down and modify

# direct inputs
# source to this solution and code:
# http://stackoverflow.com/questions/14489013/simulate-python-keypresses-for-controlling-a-game
# http://www.gamespp.com/directx/directInputKeyboardScanCodes.html

import ctypes
import time
import win32api, win32con

SendInput = ctypes.windll.user32.SendInput

keyCodes = {
    'W': 0x11,
    'A': 0x1E,
    'S': 0x1F,
    'D': 0x20,
    'SHIFT': 0x2A
}

NP_2 = 0x50
NP_4 = 0x4B
NP_6 = 0x4D
NP_8 = 0x48

def mouseDown(button='left'):
    x = 1050
    y = 1050
    #win32api.SetCursorPos((x,y))

    if button == 'left':
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
    elif button == 'right':
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,x,y,0,0)

def mouseUp(button='left'):
    x = int(1920 / 2)
    y = int(1080 / 2)
    #win32api.SetCursorPos((x,y))

    if button == 'left':
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)
    elif button == 'right':
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,x,y,0,0)

def rotate(deg):
    x = int(1920 / 2)
    y = int(1080 / 2)
    win32api.SetCursorPos((x,y))

    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)


def getKey(key):
    return win32api.GetAsyncKeyState(ord(key))

def keyPWM(key):
    if int(time.time() * 10) % 10 < 5:
        PressKey(key)
    else:
        ReleaseKey(key)

# C struct redefinitions
PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

# Actuals Functions

def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, keyCodes[hexKeyCode], 0x0008, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, keyCodes[hexKeyCode], 0x0008 | 0x0002, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

if __name__ == '__main__':
    PressKey(0x11)
    time.sleep(1)
    ReleaseKey(0x11)
    time.sleep(1)
