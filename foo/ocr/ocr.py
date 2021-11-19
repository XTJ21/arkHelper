#需要程序ocrForArkhelper,见https://github.com/MangetsuC/chineseocr_lite
import requests
import json
from base64 import b64encode


def getPid():
    try:
        res = requests.post(url='http://localhost:1616/api/tr-run/', data={'pid':1})
    except ConnectionError:
        return -1
    ans = json.loads(res.text)
    return ans['pid']

def getText(img):
    b64str = b64encode(img)
    try:
        res = requests.post(url='http://localhost:1616/api/tr-run/', data={'compress': 960, 'img': b64str})
    except ConnectionError:
        return -1
    ans = json.loads(res.text)
    return ans['data']['raw_out']

def findTextPos(ocrResult, textInclude, textExcept):
    isFound = False
    if ocrResult != -1:
        for i in range(len(ocrResult)):
            for j in textInclude:
                if j in ocrResult[i][1]:
                    if textExcept != []:
                        for k in textExcept:
                            if k in ocrResult[i][1]:
                                break
                        else:
                            isFound = True
                    else:
                        isFound = True
            if isFound:
                centerPoint = (int((ocrResult[i][0][0][0] + ocrResult[i][0][1][0])/2), int((ocrResult[i][0][0][1] + ocrResult[i][0][2][1])/2))
                return [centerPoint, ocrResult[i][0], ocrResult[i][1].split('、')[1]]
    
        else:
            return None
    else:
        return None

def findTextPos_withConficende(ocrResult, textInclude, textExcept, confidence = 0.9):
    isFound = False
    if ocrResult != -1:
        for i in range(len(ocrResult)):
            for j in textInclude:
                num  = 0
                for char in j:
                    if char in ocrResult[i][1]:
                        num += 1

                if (num/len(j)) >= confidence:
                    if textExcept != []:
                        for k in textExcept:
                            if k in ocrResult[i][1]:
                                break
                        else:
                            isFound = True
                    else:
                        isFound = True
            if isFound:
                centerPoint = (int((ocrResult[i][0][0][0] + ocrResult[i][0][1][0])/2), int((ocrResult[i][0][0][1] + ocrResult[i][0][2][1])/2))
                return [centerPoint, ocrResult[i][0], ocrResult[i][1].split('、')[1]]
    
        else:
            return None
    else:
        return None

def findTextPos_all(ocrResult, textInclude, textExcept):
    ans = []
    isFound = False
    if ocrResult != -1:
        for i in range(len(ocrResult)):
            for j in textInclude:
                if j in ocrResult[i][1]:
                    if textExcept != []:
                        for k in textExcept:
                            if k in ocrResult[i][1]:
                                break
                        else:
                            isFound = True
                    else:
                        isFound = True
            if isFound:
                centerPoint = (int((ocrResult[i][0][0][0] + ocrResult[i][0][1][0])/2), int((ocrResult[i][0][0][1] + ocrResult[i][0][2][1])/2))
                ans.append([centerPoint, ocrResult[i][0], ocrResult[i][1].split('、')[1].strip()])
                isFound = False
    
    return ans


