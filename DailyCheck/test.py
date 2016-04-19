'''

@author: lenovo
'''

import paramiko  

def ssh():
    pkey="D:\Hostkey\id_rsa_zabbixServer"  
    key=paramiko.RSAKey.from_private_key_file(pkey,password='zhd9152$**') 
    paramiko.util.log_to_file('paramiko.log')  
    ssh = paramiko.SSHClient()  
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
    #ssh.load_system_host_keys() 
    ssh.connect('192.168.1.241',username = 'czzhd',password='zhd9152$**',pkey=key) 
    stdin,stdout,stderr=ssh.exec_command('hostname')  
    print stdout.read()  
    
    
if __name__ == '__main__':
    ssh()
    
    '''   
    host = open("./hosts/keyInfo.dat")
    hostinfo = dict()
    with host as f:
        host = f.readlines()
        for i in host:
            info = i.strip("\n").split(" ")
            hostinfo[info[0]] = info[1]
    
    commandFile = open("dailyCheck.sh")
    host = open("./hosts/host.dat","r")
    with host as f:
        host = f.readlines()
        for i in host:
            aa = i.strip("\n").split(" ")
            if aa[-1]=="NoKey":
                ssh_Sess = ssh_ConnWithPasswd(aa[0], int(aa[1]), aa[2], aa[3])
#                 info = exec_cmd(ssh_Sess, COMMAND)
            else:
                ssh_Sess = ssh_ConnWithKey(aa[0], int(aa[1]), aa[2], aa[3], aa[4])
#                 info = normal_Root(ssh_Sess, hostinfo[aa[0]])
            info = exec_cmd(ssh_Sess, COMMAND)
            file = open(time+'_'+aa[0],'wb')
            file.write(info)
            file.close()
            ssh_Close(ssh_Sess)   
'''