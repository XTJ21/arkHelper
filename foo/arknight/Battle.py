from os import getcwd, listdir
from sys import path
from time import sleep

path.append(getcwd())
from foo.pictureR import pictureFind

class BattleLoop:
    def __init__(self, adb, cwd, app):
        self.cwd = cwd
        self.adb = adb
        self.app = app
        self.listBattleImg = listdir(cwd + "/res/battle")
        self.switch = False
    
    def run(self):
        self.switch = True
        self.adb.connect()
        while self.switch:
            self.app.setState("正在获取并分析屏幕信息")
            self.adb.screenShot()
            sleep(1)
            for eachObj in self.listBattleImg:
                if self.switch:
                    if eachObj == "end.png":
                        confidence = 0.8
                    else:
                        confidence = 0.9
                    print(self.cwd + '/bin/adb/arktemp.png', self.cwd + '/res/battle/' + eachObj)
                    picInfo = pictureFind.matchImg(self.cwd + '/bin/adb/arktemp.png', self.cwd + '/res/battle/' + eachObj, confidence)
                    print(eachObj+ '：', picInfo)
                    if picInfo != None:
                        picPos = picInfo['result']
                        self.adb.click(picPos[0], picPos[1])
                        if eachObj == "cancel.png":
                            self.switch = False
                            self.app.setState("理智耗尽")
                            self.app.setButton(1)
                            break
            sleep(1)
    def stop(self):
        self.switch = False