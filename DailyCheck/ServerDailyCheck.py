# coding:utf-8
#!/bin/env python
'''
Created on 2015年12月9日

@author: zhiwen Xu
'''

import paramiko
import time
from sys import stderr

# 打开ssh连接，返回ssh连接session
def ssh_ConnWithPasswd(ipAddress, port, username, password):
    try:
        ssh_Conn = paramiko.SSHClient()
        ssh_Conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_Conn.connect(ipAddress, port, username, password)
        return ssh_Conn
    except Exception , e:
        print "ERROR:ssh_ConnWithPasswd" + str(e)

def ssh_ConnWithKey(ipAddress, port, username, password,keyPath):
    
    key=paramiko.RSAKey.from_private_key_file(keyPath,password) 
    #paramiko.util.log_to_file('paramiko.log')  
    ssh_Conn = paramiko.SSHClient()  
    ssh_Conn.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
    ssh_Conn.connect(ipAddress,port,username,password,pkey=key) 
    
    return ssh_Conn

def ssh_Close(ssh_Session):
    ssh_Session.close()

# 在ssh中执行相关的命令
def exec_cmd(ssh_Session, command):
    try :
        stdin,stdout,stderr = ssh_Session.exec_command(command)
        out = stdout.read()
        err = stderr.read()
        if out != "":
            return  out
        if err != "":
            return err
    except Exception,e:
        print 'ERROR:exec_cmd: exec_cmd - %s' % e

'''
# 使用ssh_Session打开sftp连接
def sftp_Open(ssh_Session):
    sftp_Session = ssh_Session.open_sftp()
    return sftp_Session
# 关闭sftp连接   
def sftp_Close(sftp_Session):
    sftp_Session.close()
# 使用Sftp上传文件
def sftp_Upload(sftp_Session, localPath, remotePath):
    try:
        sftp_Session.put(localPath, remotePath)
    except Exception, e:
        print 'ERROR: sftp_Upload - %s' % e
# 使用sftp下载文件
def sftp_Download(sftp_Session, remotePath,localPath):
    try:
        sftp_Session.get(remotePath, localPath)  
    except Exception, e:
        print 'ERROR: sftp_Download -%s' % e    

def _callback(self,a,b):
    sys.stdout.write('Data Transmission %10d [%3.2f%%]\r' %(a,a*100./int(b)))
    sys.stdout.flush()
'''

#普通用户使用密钥登陆，切换到root用户
def normal_Root(ssh_Session,password,command):
    ssh = ssh_Session.invoke_shell()
    ssh.send("su \n")
    buff=''
    while not buff.endswith("密码："):
        resp = ssh.recv(9999)
        buff +=resp
    ssh.send(password)
    ssh.send("\n") 
    buff = ''
    while not buff.endswith('# '):
        resp = ssh.recv(9999)
        buff +=resp 
    ssh.send(command)
    ssh.send('\n')
    buff = ''
    while not buff.endswith('# '):
        resp = ssh.recv(9999)
        buff +=resp
    ssh.close()
    result = buff
    return result

#读取各个IP的命令文件
def readCommandFile(filePath):
    file = open(filePath)
    commandList=[]
    for line in file.readlines():
        commandList.append(line)
    return commandList

if __name__ == '__main__':
    time = time.strftime('%Y-%m-%d',time.localtime(time.time()))
     
    hostInfo = dict()
    keyInfo = open("./hosts/keyInfo.dat")
    with keyInfo as f:
        keyinfo = f.readlines()
        for i in keyinfo:
            info = i.strip("\n").split(" ")
            hostInfo[info[0]] = info[1]
    
    print hostInfo
    hosts = open("./hosts/host.dat")
    with hosts as host:
        for i in hosts:
            info = i.strip("\n").split(" ")
            commandList = readCommandFile("./hosts/"+info[0]+".cmd")
            result=""
            for element in commandList:
                command = element.split("#")
                if info[-1] == "NoKey":
                    ssh_Sess = ssh_ConnWithPasswd(info[0], int(info[1]), info[2], info[3])
                    result = result+"\n"+command[0]+":"+command[-1]+"\n"
                    result = result+" "+exec_cmd(ssh_Sess, command[-1])
                else:
                    ssh_Sess = ssh_ConnWithKey(info[0], int(info[1]), info[2], info[3], info[4])
                    result = result+" "+normal_Root(ssh_Sess, hostInfo[info[0]],command[-1])
                
            file = open("./result/Server_"+time+'_'+info[0],'wb')
            file.write(result)
            file.close()
            ssh_Close(ssh_Sess)