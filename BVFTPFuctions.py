from FTPwork import myFtp

'''
            try:
                ftp = myFtp("BVIP")
                ftp.Login(FTPUserName,FTPPw)            
                #設定目標路徑
                ftp.ChangeRount('..') #turn back                
                ftp.ChangeRount('bv/InBox')
#-------------------------------------------------------------------------------------------- 

#-------------------------------------------------------------------------------------------- 
                ftp.close()


            except:
                print("請確認RJ45是否有接好!")



'''

class FTPFuc:
    def CheckFileExist(BVIP,FTPUserName,FTPPw):
        #try:
        ftp = myFtp(BVIP)
        ftp.Login(FTPUserName,FTPPw)
        # 設定目標路徑
        ftp.ChangeRount('bv/InBox')

        FolderList = ftp.CheckRountsFileName()
        TargetFolders = []
        for Folder in FolderList:
            ftp.ChangeRount(Folder)
            FileList = ftp.CheckRountsFileName()

            if len(FileList) > 0:
                TargetFolders.append(Folder)

            ftp.ChangeRount('..')  # turn back

        ftp.close()

        return TargetFolders


        #except:
         #   print("請確認RJ45是否有接好!")

    def GetInboxfile(FolderList, BVIP,FTPUserName,FTPPw):
        TestProjectName = "DeviceID:"

        try:
            ftp = myFtp(BVIP)
            ftp.Login(FTPUserName,FTPPw)

            # 設定目標路徑
            ftp.ChangeRount('bv')

            # 獲取需備份的檔案

            for TargetFolder in FolderList:
                local_path = 'Datas/' + TargetFolder
                romte_path = 'InBox/' + TargetFolder
                try:
                    ftp.DownLoadFileTree(local_path, romte_path, BVIP, TestProjectName)
                    print("資料取得完成")

                    ftp.ChangeRount('..')
                except:
                    print("InBox資料獲取失敗")

            ftp.close()

        except:
            print("請確認RJ45是否有接好!")

    def DeleteTargetFolder(FolderList, BVIP,FTPUserName,FTPPw):

        try:
            ftp = myFtp(BVIP)
            ftp.Login(FTPUserName,FTPPw)
            # 設定目標路徑
            ftp.ChangeRount('bv/InBox')
            # --------------------------------------------------------------------------------------------
            for Folder in FolderList:
                ftp.DeleteFoldersFlies(Folder)
                ftp.ChangeRount('..')
            # --------------------------------------------------------------------------------------------
            ftp.close()


        except:
            print("請確認RJ45是否有接好!")

if __name__ == '__main__':
    TKL=FTPFuc.CheckFileExist('10.42.0.51','pi','mitac2019pi')
    FTPFuc.DeleteTargetFolder(TKL,'10.42.0.51','pi','mitac2019pi')





