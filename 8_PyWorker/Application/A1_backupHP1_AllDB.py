import __init
import os,datetime

SRC_MYSQL_DOCKER_CONTAINER_NAME="wsnCluster_zabbix-mysql-server"
COMMAND_1 = f'docker exec -i {SRC_MYSQL_DOCKER_CONTAINER_NAME} mysqldump -u root -proot_pwd zabbix > /root/0_GIT_WSN_SERVER_CLUSTER/2_MySQL/All_DB_MySQL.sql'
COMMAND_2 = f'tar -czvf /root/0_GIT_WSN_SERVER_CLUSTER/2_MySQL/All_DB_MySQL.tar.gz /root/0_GIT_WSN_SERVER_CLUSTER/2_MySQL/All_DB_MySQL.sql'
COMMAND_3 = f'rm -f /root/0_GIT_WSN_SERVER_CLUSTER/2_MySQL/All_DB_MySQL.sql'
COMMAND_4 = f'chmod 666 /root/0_GIT_WSN_SERVER_CLUSTER/2_MySQL/All_DB_MySQL.tar.gz'

TIME = "\x1b[48;5;51m["+str(datetime.datetime.now())+"]\x1b[0m"
print(f'{TIME} ===> 1. Xuất file sql')
os.system(COMMAND_1)

TIME = "\x1b[48;5;51m["+str(datetime.datetime.now())+"]\x1b[0m"
print(f'{TIME} ===> 2. Nén file.tar.gz')
os.system(COMMAND_2)

TIME = "\x1b[48;5;51m["+str(datetime.datetime.now())+"]\x1b[0m"
print(f'{TIME} ===> 3. Xóa file sql cũ')
os.system(COMMAND_3)

TIME = "\x1b[48;5;51m["+str(datetime.datetime.now())+"]\x1b[0m"
print(f'{TIME} ===> 4. Đổi mode 666 cho tar.gz')
os.system(COMMAND_4)

TIME = "\x1b[48;5;51m["+str(datetime.datetime.now())+"]\x1b[0m"
print(f'{TIME} ===> 5. DONE')