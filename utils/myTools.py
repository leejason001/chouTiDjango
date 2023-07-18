#coding: utf-8
import random

def getValidationCode(validationCodeLength=4):
    lowerCharValidation = "abcdefghjkmnpqrstuvwxy"  # 小写字母，去除可能干扰的i，l，o，z
    uperCharValidation = lowerCharValidation.upper();
    numberValidation = ''.join(map(str, range(3,9)));
    validationCodeEmailedPool = ''.join((lowerCharValidation, uperCharValidation, numberValidation));

    return ''.join(random.sample(validationCodeEmailedPool, validationCodeLength));

class BaseResponse:
    def __init__(self):
        self.status = True;
        self.summary = None;
