import __init
import os,datetime
############# USER DEFINE #############
### SOURCE HOST ###
# mysqldump -u root -proot_pwd zabbix history history_log history_str history_text history_uint > ./history.sql
SRC_HOST_IP="157.65.24.169" # SERVER ZABBIX JAPAN
SRC_HOST_PORT="22"
SRC_HOST_USER="root"
SRC_MYSQL_TABLE_LIST=["history","history_log","history_str","history_text","history_uint"]
SRC_MYSQL_DATABASE="zabbix"
SRC_MYSQL_DOCKER_CONTAINER_NAME="mysql-server"

### DESTINATION HOST ###
# docker exec -i wsnCluster_zabbix-mysql-server mysql -u root -proot_pwd zabbix < ./history.sql
DES_MYSQL_TABLE_LIST=["history","history_log","history_str","history_text","history_uint"]
DES_MYSQL_DATABASE="zabbix"
DES_MYSQL_DOCKER_CONTAINER_NAME="wsnCluster_zabbix-mysql-server"
DES_DOCKER_EXEC = "docker exec -i "+DES_MYSQL_DOCKER_CONTAINER_NAME+" mysql -u root -proot_pwd "+DES_MYSQL_DATABASE+" < ./history.sql"

#########################################
# 1. Build docker exec for backup MySQL database command
TIME = "\x1b[48;5;51m["+str(datetime.datetime.now())+"]\x1b[0m"
print(f'{TIME} ===> START BACKUP DATABASE...')
SRC_TABLE_LIST = " ".join(SRC_MYSQL_TABLE_LIST)
SRC_SSH_CMD=f'ssh -p {SRC_HOST_PORT} {SRC_HOST_USER}@{SRC_HOST_IP}'

COMMAND_1 = f'docker exec -i {SRC_MYSQL_DOCKER_CONTAINER_NAME} mysqldump -u root -proot_pwd {SRC_MYSQL_DATABASE} {SRC_TABLE_LIST} > /history.sql'
COMMAND_2 = f'tar -czvf /history.tar.gz /history.sql'
COMMAND_3 = f'rm -f \/history.sql'
COMMAND_4 = f'chmod 666 \/history.tar.gz'

MERGE_COMMAND = SRC_SSH_CMD+" \""+f'{COMMAND_1}&&{COMMAND_2}&&{COMMAND_3}&&{COMMAND_4}'+"\""
print("MERGE_COMMAND: ",MERGE_COMMAND)

os.system(MERGE_COMMAND)

# 2. Dùng SCP để tải file backup về máy local
TIME = "\x1b[48;5;51m["+str(datetime.datetime.now())+"]\x1b[0m"
print(f'{TIME} ===> START DOWNLOAD DATABASE...')
SRC_FILE_PATH = "/history.tar.gz"
DES_FILE_PATH = "history.tar.gz"
SCP_DOWNLOAD_CMD = f'scp -P {SRC_HOST_PORT} {SRC_HOST_USER}@{SRC_HOST_IP}:{SRC_FILE_PATH} {DES_FILE_PATH}'
os.system(SCP_DOWNLOAD_CMD)

# 3. Xóa file backup trên host
TIME = "\x1b[48;5;51m["+str(datetime.datetime.now())+"]\x1b[0m"
print(f'{TIME} ===> START DELETE DATABASE...')
SRC_DELETE_FILE_CMD = f'{SRC_SSH_CMD} rm -f {SRC_FILE_PATH}'
os.system(SRC_DELETE_FILE_CMD)

# 4. Giải nén file backup trên máy local
TIME = "\x1b[48;5;51m["+str(datetime.datetime.now())+"]\x1b[0m"
print(f'{TIME} ===> START UNZIP DATABASE...')
DES_UNZIP_CMD = f'tar -xzvf {DES_FILE_PATH}'
os.system(DES_UNZIP_CMD)

# 5. Xóa file backup trên máy local
TIME = "\x1b[48;5;51m["+str(datetime.datetime.now())+"]\x1b[0m"
print(f'{TIME} ===> START DELETE DATABASE...')
DES_DELETE_FILE_CMD = f'rm -f {DES_FILE_PATH}'
os.system(DES_DELETE_FILE_CMD)

# 6. Restore database from backup file to destination host
TIME = "\x1b[48;5;51m["+str(datetime.datetime.now())+"]\x1b[0m"
print(f'{TIME} ===> START RESTORE DATABASE...')
os.system(DES_DOCKER_EXEC)
TIME = "\x1b[48;5;51m["+str(datetime.datetime.now())+"]\x1b[0m"
print(f'{TIME} === DONE ===')










