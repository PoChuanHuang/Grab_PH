# -*- coding: cp950 -*-

import smtplib

def send_gmail(gmail_name,send_msg):
    from_user = 'peter02589@gmail.com'
    from_password = 'peter110246'
    
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
        smtp.login(from_user, from_password) ##�i��n�J
        smtp.sendmail(from_user , gmail_name , email_text) ##sendmail(�H�H��,�����,�H��)
        smtp.close()
        print('Email sent!')
    except:
        print ('Email sent failed!!!')



