#coding: utf-8
import random

import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

def getValidationCode(validationCodeLength=4):
    lowerCharValidation = "abcdefghjkmnpqrstuvwxy"  # 小写字母，去除可能干扰的i，l，o，z
    uperCharValidation = lowerCharValidation.upper();
    numberValidation = ''.join(map(str, range(3,9)));
    validationCodeEmailedPool = ''.join((lowerCharValidation, uperCharValidation, numberValidation));

    return ''.join(random.sample(validationCodeEmailedPool, validationCodeLength))

def sendEmail(aimEmail, content, subject="我的抽屉，用户注册"):
    emailObject = MIMEText(content, "plain", 'utf-8')
    emailObject["from"] = formataddr(["我的抽屉", "13131412952@163.com"])
    emailObject["Subject"] = subject

    server = smtplib.SMTP("smtp.163.com", 25)
    server.login("13131412952@163.com", "123456")
    server.sendmail("13131412952@163.com", aimEmail, emailObject.as_string())
    server.quit()


class BaseResponse:
    def __init__(self):
        self.status = True
        self.summary = None

