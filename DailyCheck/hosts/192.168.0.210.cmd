系统当前时间#date
系统内核版本#uname -a
各分区使用情况#df -lP
内存使用量和交换区使用量#free -m
所有监听端口#netstat -nltp
内存占用前10#ps aux | sort -k4nr | head -n 10