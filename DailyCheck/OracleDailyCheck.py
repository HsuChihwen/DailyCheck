# coding:utf-8
#!/bin/env python
'''
Created on 2016年4月5日

@author: lenovo
'''

import cx_Oracle  
import time

#读取sql文件
def readSQL(filePath):
    file = open(filePath)
    sqlList=[]
    for line in file.readlines():
        sqlList.append(line)
    return sqlList




if __name__ == '__main__':
    time = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    connInfo = open("./OracleInfo/SQLConnInfo.dat")
    with connInfo as connInfos:
        for i in connInfos:
            hostInfo = i.strip("\n")
            conn = cx_Oracle.connect(hostInfo)
            cursor = conn.cursor()
            sqlList = readSQL("./OracleInfo/OracleDailyCheck.dat")
            
            for element in sqlList:
                str = ""
                sql = element.split(";")
                cursor.execute(sql[0])
                rows = cursor.fetchall()
                print sql[0]
                for i in range(len(rows)):
                    for j in range(len(rows[i])):
                        str = str+rows[i][j]+"    "
                    str = str+"\n"
                print str
            cursor.close ()  
            conn.close ()

