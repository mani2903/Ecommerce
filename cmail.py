# import smtplib
# from smtplib import SMTP
# from email.message import EmailMessage

# def sendmail(to,subject,body):
#     server=smtplib.SMTP_SSL('smtp.gmail.com',465)
#     server.login('manikumarthanikonda@gmail.com','smjf crzc oqzt uooa')
#     msg=EmailMessage()
#     msg['Form']='manikumarthanikonda@gmail.com'
#     msg['Subject']=subject
#     msg['To']=to
#     msg.set_content(body)
#     server.send_message(msg)
#     server.quit()


import smtplib
from smtplib import SMTP 
from email.message import EmailMessage

def sendmail(to,subject,body):
    server=smtplib.SMTP_SSL('smtp.gmail.com',465)
    server.login('manikumarthanikonda@gmail.com','smjf crzc oqzt uooa')
    msg=EmailMessage()
    msg['From']='manikumarthanikonda@gmail.com'
    msg['Subject']=subject
    msg['To']=to
    msg.set_content(body)
    server.send_message(msg)
    server.quit()