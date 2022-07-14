from OtherFuc import UsefulFuction
from ActionLib import FixAction
import os

Version='220610_ReMoveSD'

if __name__ == "__main__":
    print('目前版本:',Version)

    while (1):
        print('1.初始化設定')
        print('2.機台重啟')
        print('3.燒機資料下載')
        print('4.交易資料下載')
        print('5.主程式上傳')
        print('6.測試資料清除')
        print('7.設為現在時間')
        print('8.刪除設定檔')
        #每分鐘詢問一次
        #測試項時間不同
        #取得 時間 溫度 設備
        print('99.離開')
        FixActionNum = input('請輸入指令:\n')

        if FixActionNum=='99':
            break

        if not os.path.exists("./RepairList.txt"):  # 確認是否存在儲存路徑
            print("RepairList.txt不存在!請重新確認!")

        else:
            DeviceInfo = UsefulFuction.GetDeviceInfo("./RepairList.txt")
            FixAction(FixActionNum,DeviceInfo)

