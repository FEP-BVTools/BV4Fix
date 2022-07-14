import paramiko
from OtherFuc import UsefulFuction

class SSHClass:
    def __init__(self, server,user,pw):

        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(server, username=user, password=pw, timeout=1)

        print('登入成功')
    def CmdMode(self):
        print('已進入命令模式,離開輸入qq')

        while(1):
            cmd=input('(CmdMode):')
            if cmd=='qq':
                print('離開命令模式')
                break

            stdin, stdout, stderr = self.ssh.exec_command(cmd)
            result = stdout.readlines()
            print (result)
    def CheckOnline(self):
        stdin, stdout, stderr = self.ssh.exec_command('cat ./bv/EventOnlineInfo.txt')
        result = stdout.readlines()
        for data in range(len(result)):
            print(result[data])
        print('總筆數:',len(result))
    def ReaderPowerOff(self):
        self.ssh.exec_command('echo 0 >/sys/class/gpio/gpio16/value')
    def ActiveMainProcess(self):
        self.ssh.exec_command('cd /bv')
        self.ssh.exec_command('sudo Mitac_BV&')
    def InitAdmin(self):
        self.ssh.exec_command('sudo chown -R pi:pi bv')         #將BV擁有者變更為pi
        self.ssh.exec_command('sudo chmod -R 777 bv')        #將檔案變更讀寫權限
    def GetCPUSerial(self):
        stdin, stdout, stderr = self.ssh.exec_command('cat /proc/cpuinfo | grep Serial')
        result = stdout.readline()
        SN=result[10:26]
        return SN
    def RebootBV4(self):
        self.ssh.exec_command('sudo reboot')
        print('重啟指令發送成功!')

    def MeatureTemperature(self):
        stdin, stdout, stderr = self.ssh.exec_command('vcgencmd measure_temp')
        result = stdout.readline()
        print(result)

    def RemoveSDcardUselessData(self):
        MntSDcardcmd='cd ~;sudo umount /home/pi/mnt/SDBackup;sudo mount /dev/mmcblk1p1 /home/pi/mnt/SDBackup -o uid=pi -o gid=pi;cd /home/pi/mnt/SDBackup;ls'
        RemoveSDcardDatacmd='sudo rm 2021-01 -rf;sudo rm 978MB -rf;sudo rm CF_BACKUP/ -rf;ls'
        UnMntSDcardcmd='cd ~;sudo umount /home/pi/mnt/SDBackup'
        stdin, stdout, stderr = self.ssh.exec_command(MntSDcardcmd+';'+RemoveSDcardDatacmd+';'+UnMntSDcardcmd)
        result = stdout.readlines()
        print(result)
        print('移除SD無用資料')

    def InitTimeProcess(self,InitTimeAction):
        TargetInitTime=UsefulFuction.InitTimeActionFuc(InitTimeAction)
        self.ssh.exec_command('sudo date {}'.format(TargetInitTime).encode())
        self.ssh.exec_command('sudo hwclock --systohc'.encode())#同步到硬體時間
        print('已設為現在時間:',TargetInitTime)

if __name__ == '__main__':
    while 1:
        SSH=SSHClass('10.42.0.51','pi','mitac2019pi')
        SSH.RemoveSDcardUselessData()
        a=input()



