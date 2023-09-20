import __init
import os,datetime

SRC_MYSQL_DOCKER_CONTAINER_NAME="wsnCluster_zabbix-mysql-server"

#Change Workdir
os.chdir("/")
WORKDIR="/root/0_GIT_WSN_SERVER_CLUSTER/2_MySQL"

COMMAND_1 = f'tar -xzvf {WORKDIR}/All_DB_MySQL.tar.gz'
COMMAND_2 = f'docker exec -i {SRC_MYSQL_DOCKER_CONTAINER_NAME} mysql -u root -proot_pwd zabbix < {WORKDIR}/All_DB_MySQL.sql'
COMMAND_3 = f'rm -f {WORKDIR}/All_DB_MySQL.sql'


TIME = "\x1b[48;5;51m["+str(datetime.datetime.now())+"]\x1b[0m"
print(f'{TIME} ===> 1. Giải nén ra file sql')
os.system(COMMAND_1)

TIME = "\x1b[48;5;51m["+str(datetime.datetime.now())+"]\x1b[0m"
print(f'{TIME} ===> 2. Restore MySQL')
os.system(COMMAND_2)

TIME = "\x1b[48;5;51m["+str(datetime.datetime.now())+"]\x1b[0m"
print(f'{TIME} ===> 3. Xóa file sql cũ')
os.system(COMMAND_3)


TIME = "\x1b[48;5;51m["+str(datetime.datetime.now())+"]\x1b[0m"
print(f'{TIME} ===> 5. DONE')