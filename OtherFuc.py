import socket
import ctypes
import csv
import os
import time
from time import gmtime, strftime


class UsefulFuction:
    # 將權限提升為系統管理員
    def is_admin():
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            a = input()
            return False

    def GetIPAdress():
        IpAdress = ""
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # DNS 位址
        IpAdress = s.getsockname()[0]
        s.close()

        return IpAdress

    def GetDeviceInfo(RepairFile):
        DeviceInfo = {}
        IP_Position = 1
        with open(RepairFile, newline='') as csvfile:
            rows = csv.reader(csvfile)
            for row in rows:
                DeviceInfo[row[0]] = IP_Position
                IP_Position += 1
            return DeviceInfo

    def WriteConfigFile(DeviceID, IP_Position):
        LocalDir = "./BV_FTPData/{}/TestMode".format(DeviceID)
        data = str(time.strftime("%Y%m%d%H%M"))
        content ='DeviceID,{}\nDeviceTime,{}\nLanLocalIP,192.168.1.{}\nLanHostIP,192.168.1.200\nWlanLocalIP,192.168.3.111\nWlanHostIP,192.168.3.1\nWlanSSID,FEcompany_6F\nWlanPassword,24323705'.format(DeviceID,data,IP_Position)
        tsa=bytes(content,encoding='utf-8')
        if not os.path.exists(LocalDir):  # 確認是否存在儲存路徑
            os.makedirs(LocalDir)

        # f = open("./BV_FTPData/{}/TestMode/Config.csv".format(DeviceID), 'wb')
        # f.write(content)
        # f.close()
        with open("./BV_FTPData/{}/TestMode/Config.csv".format(DeviceID), 'wb+') as open_file:
            open_file.write(tsa)


    def AddCPUSNFile(DeviceID,CPUSN):
        LocalDir = "./BV_FTPData/{}/TestMode".format(DeviceID)
        if not os.path.exists(LocalDir):  # 確認是否存在儲存路徑
            os.makedirs(LocalDir)
        f = open("./BV_FTPData/{}/CPUSN_{}.txt".format(DeviceID,CPUSN), 'w')
        f.close()

    def ErrReport(ErrMessage, DeviceID):
        f = open("ErrReport.csv", "a")
        f.write("{},,{}\n".format(DeviceID, ErrMessage))
        f.close()
    def MatchCPUSNDVIDTable(DeviceID,CPUSN):
        f=open('CPUSN_Table.csv','a+')
        f.write('{},{}\n'.format(DeviceID,CPUSN))
        f.close()

    def GetFTPLoginInfo(FTPInfoFileName):
        if os.path.exists(FTPInfoFileName):
            FTPFile = open(FTPInfoFileName)
            FTPUser = FTPFile.readline().strip()
            FTPPw = FTPFile.readline().strip()
        else:
            while (1):
                FTPUser = input('請輸入FTP帳號')
                if FTPUser != '':
                    FTPPw = input('請輸入密碼')
                    f = open(FTPInfoFileName, mode='a+')
                    f.write(FTPUser)
                    if FTPPw == '':
                        f.write(FTPPw)
                    break
                else:
                    print('帳號不可為空值!!')

        return FTPUser, FTPPw

    def InitTimeActionFuc(InitTimeAction):
        if InitTimeAction == '1':
            TargetInitTime = strftime("%m%d%H%M.%S", gmtime())
        elif InitTimeAction == '2':
            TargetInitTime = str(time.strftime("%m%d"))
            TargetInitTime = TargetInitTime + "0000.00"
        elif InitTimeAction == '3':
            TargetInitTime = strftime("%m%d%H%+8M.%S", time.localtime())
        return TargetInitTime

if __name__ == '__main__':
    TargetInitTime = strftime("%m%d%H%M.%S", time.localtime())
    print(TargetInitTime)