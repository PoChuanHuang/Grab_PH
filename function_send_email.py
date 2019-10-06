# -*- coding: cp950 -*-

import smtplib

def send_gmail(gmail_name,send_msg):
    from_user = ''//輸入寄件者電子郵件帳號
    from_password = ''//輸入寄件者電子郵件密碼
    
    subject = 'Hello'
    
    tmp = ""
    for i in send_msg:
      tmp += i+"\n"
    
    email_text = """\  
    From: %s  
    To: %s  
    Subject: %s
    %s
    """ % (from_user, ", ".join(gmail_name), subject, tmp)

    try:
        smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp.ehlo()
        smtp.login(from_user, from_password) ##進行登入
        smtp.sendmail(from_user , gmail_name , email_text) ##sendmail(寄信方,收件方,信件)
        smtp.close()
        print('Email sent!')
    except:
        print ('Email sent failed!!!')



