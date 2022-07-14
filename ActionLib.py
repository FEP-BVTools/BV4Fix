from FTPwork import myFtp
from OtherFuc import UsefulFuction
from SSHFuction import SSHClass
import time

class FTPFuc:
    def SaveBackupDataProcess(RetryCount, DeviceID, IP_Position, FtpUser, FtpPw):

        SSH = SSHClass('192.168.1.{}'.format(IP_Position),'pi', 'mitac2019pi')
        SSH.InitAdmin()

        while (RetryCount > 0):
            try:
                ftp = myFtp("192.168.1.{}".format(IP_Position))
                ftp.Login(FtpUser, FtpPw)
                print()

                # 設定目標路徑
                ftp.ChangeRount('/home/pi/bv')

                # 獲取需備份的檔案
                local_path = './BV_FTPData/' + DeviceID + '/InBox'
                romte_path = 'InBox'
                try:
                    ftp.DownLoadFileTree(local_path, romte_path, "192.168.1.{}".format(IP_Position), DeviceID)
                except:
                    print("InBox資料獲取失敗")
                    UsefulFuction.ErrReport("Get InBox Fail", DeviceID)

                local_path = './BV_FTPData/' + DeviceID + '/Transfered'
                romte_path = 'Transfered'
                try:
                    ftp.DownLoadFileTree(local_path, romte_path, "192.168.1.{}".format(IP_Position), DeviceID)
                except:
                    print("Transfered資料獲取失敗")
                    UsefulFuction.ErrReport("Get Transfered Fail", DeviceID)

                # 獲取SD卡資料(待補)



                break

            except:
                print("Log in Retry...")
                UsefulFuction.ErrReport("Log in Retry", DeviceID)
                RetryCount -= 1

        ftp.close()

    def SaveBurnTestData(RetryCount, DeviceID, IP_Position, FtpUser, FtpPw):
        SSH = SSHClass('192.168.1.{}'.format(IP_Position),'pi', 'mitac2019pi')
        SSH.InitAdmin()
        while (RetryCount > 0):
            try:
                ftp = myFtp("192.168.1.{}".format(IP_Position))
                ftp.Login(FtpUser, FtpPw)
                print()

                # 設定目標路徑
                ftp.ChangeRount('/home/pi/bv')

                # 獲取需燒機後結果報告
                local_path = './LogReport'
                romte_path = 'LogReport'
                ftp.DownLoadFileTree(local_path, romte_path, "192.168.1.{}".format(IP_Position), DeviceID)
                break

            except:
                print("Log in Retry...")
                RetryCount -= 1

        ftp.close()
    def BackupBurnTestData(RetryCount, DeviceID, IP_Position, FtpUser, FtpPw):
        SSH = SSHClass('192.168.1.{}'.format(IP_Position),'pi', 'mitac2019pi')
        SSH.InitAdmin()
        while (RetryCount > 0):
            date=str(time.strftime("%Y-%m-%d-%H"))
            try:
                ftp = myFtp("192.168.1.{}".format(IP_Position))
                ftp.Login(FtpUser, FtpPw)
                print()

                # 設定目標路徑
                ftp.ChangeRount('/home/pi/bv')
                # 將燒機結果進行備份
                local_path = './BackUpLogReport/{}'.format(date)
                romte_path = 'LogReport'
                ftp.DownLoadFileTree(local_path, romte_path, "192.168.1.{}".format(IP_Position), DeviceID)

                break

            except:
                print("Log in Retry...")
                RetryCount -= 1

        ftp.close()

    def EraseTestData(RetryCount,IP_Position, FtpUser, FtpPw):
        SSH = SSHClass('192.168.1.{}'.format(IP_Position),'pi', 'mitac2019pi')
        SSH.InitAdmin()

        while (RetryCount > 0):
            try:
                ftp = myFtp("192.168.1.{}".format(IP_Position))
                ftp.Login(FtpUser, FtpPw)
                print()

                # 設定目標路徑
                ftp.ChangeRount('/home/pi/bv')

                ftp.DeleteFoldersFlies('LogReport')

                break

            except:
                print("Log in Retry...")
                RetryCount -= 1

        ftp.close()

    def DeleteConfig(RetryCount, IP_Position, FtpUser, FtpPw):
        SSH = SSHClass('192.168.1.{}'.format(IP_Position), 'pi', 'mitac2019pi')
        SSH.InitAdmin()

        while (RetryCount > 0):
            try:
                ftp = myFtp("192.168.1.{}".format(IP_Position))
                ftp.Login(FtpUser, FtpPw)
                print()

                # 設定目標路徑
                ftp.ChangeRount('/home/pi/bv')

                ftp.DeleteFoldersFlies('TestMode')

                break

            except:
                print("Log in Retry...")
                RetryCount -= 1

        ftp.close()
    def SetDeviceStatus(RetryCount, DeviceID, IP_Position, FtpUser, FtpPw):
        while (RetryCount > 0):
            try:
                ftp = myFtp("192.168.1.{}".format(IP_Position))
                ftp.Login(FtpUser, FtpPw)
                print()

                # 設定目標路徑
                ftp.ChangeRount('/home/pi/bv')  # 返回根目錄
                try:
                    ftp.CreatFolder(DeviceID)
                except:
                    print("已存在該設備ID資料夾")

                #ftp.ChangeRount('bv')
                print("上傳設備設定值")
                # 創建該設備ID並上傳
                UsefulFuction.WriteConfigFile(DeviceID, IP_Position)

                local_path = './BV_FTPData/' + DeviceID + '/TestMode'
                romte_path = 'TestMode'

                ftp.UploadfileTree(local_path, romte_path)
                print("成功")
                break

            except:
                print("Log in Retry...")
                RetryCount -= 1

        ftp.close()

    def UploadApp(RetryCount, DeviceID, IP_Position, FtpUser, FtpPw):
        while (RetryCount > 0):
            try:
                ftp = myFtp("192.168.1.{}".format(IP_Position))
                ftp.Login(FtpUser, FtpPw)
                print()

                # 設定目標路徑
                ftp.ChangeRount('/home/pi/')  # 返回根目錄
                print("上傳現行版程式與設定")
                local_path = './updataFix'
                romte_path = 'bv'

                ftp.UploadfileTree(local_path, romte_path)
                print("成功")
                break

            except:
                print("Log in Retry...")
                RetryCount -= 1

def FixAction(SelectNum,DeviceInfo):
    RetryCount = 1
    FTPUser='pi'
    FTPPw='mitac2019pi'
    SLN=int(SelectNum)
    if SLN==1:
        for DVID in DeviceInfo.keys():
            print("\nLogin Device:{}".format(DVID))
            try:
                SSH = SSHClass('192.168.1.{}'.format(DeviceInfo[DVID]), 'pi', 'mitac2019pi')
                # 取得CPU序號
                BVCPUSN = SSH.GetCPUSerial()
                UsefulFuction.AddCPUSNFile(DVID, BVCPUSN)
                #
                UsefulFuction.MatchCPUSNDVIDTable(DVID,BVCPUSN)
                # 參數設定
                FTPFuc.SetDeviceStatus(RetryCount, BVCPUSN, DeviceInfo[DVID], FTPUser, FTPPw)
                #移除SD無用資料
                SSH.RemoveSDcardUselessData()

            except:
                print("Unknow FTP Err")
                continue
    elif SLN==2:
        for DVID in DeviceInfo.keys():
            print("\nLogin Device:{}".format(DVID))
            try:
                # 取得CPU序號
                SSH = SSHClass('192.168.1.{}'.format(DeviceInfo[DVID]), 'pi', 'mitac2019pi')
                SSH.RebootBV4()

            except:
                print("Reboot Err!!")
                continue
    elif SLN == 3:
        for DVID in DeviceInfo.keys():
            print("\nLogin Device:{}".format(DVID))
            try:
                FTPFuc.SaveBurnTestData(RetryCount, DVID, DeviceInfo[DVID], FTPUser, FTPPw)
                FTPFuc.BackupBurnTestData(RetryCount, DVID, DeviceInfo[DVID], FTPUser, FTPPw)
            except:
                print("Reboot Err!!")
                continue
    elif SLN == 4:
        for DVID in DeviceInfo.keys():
            print("\nLogin Device:{}".format(DVID))
            try:

                FTPFuc.SaveBackupDataProcess(RetryCount, DVID, DeviceInfo[DVID], FTPUser, FTPPw)
            except:
                print("Reboot Err!!")
                continue
    elif SLN == 5:
        for DVID in DeviceInfo.keys():
            print("\nLogin Device:{}".format(DVID))
            try:
                # 取得CPU序號
                FTPFuc.UploadApp(RetryCount, DVID, DeviceInfo[DVID], FTPUser, FTPPw)
            except:
                print("Reboot Err!!")
                continue
    elif SLN == 6:
        for DVID in DeviceInfo.keys():
            print("\nLogin Device:{}".format(DVID))
            try:
                # 取得CPU序號
                FTPFuc.EraseTestData(RetryCount,DeviceInfo[DVID], FTPUser, FTPPw)
            except:
                print("EraseTestData Err!!")
                continue

    elif SLN == 7:
        for DVID in DeviceInfo.keys():
            print("\nLogin Device:{}".format(DVID))
            try:
                InitTimeAction='3'
                SSH = SSHClass('192.168.1.{}'.format(DeviceInfo[DVID]), 'pi', 'mitac2019pi')
                SSH.InitTimeProcess(InitTimeAction)



            except:
                print("Unknow Err!!")
                continue
    elif SLN == 8:
        for DVID in DeviceInfo.keys():
            print("\nLogin Device:{}".format(DVID))
            try:
                FTPFuc.DeleteConfig(RetryCount, DeviceInfo[DVID], FTPUser, FTPPw)
            except:
                print("DeleteConfig Err!!")
                continue


if __name__ == '__main__':


    FTPUser='pi'
    FTPPw='mitac2019pi'
    FTPFuc.BackupBurnTestData(1, 'DVID', '1', FTPUser, FTPPw)