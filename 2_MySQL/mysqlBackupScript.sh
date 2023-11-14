# This script is used to backup all MySQL databases on an hourly and daily basis.
# The backups are stored in a specified directory and are compressed using tar.
# The script also has a feature to limit the number of hourly backups
# (If backup sql is less than 10MBz -> Ingnore) to a specified number.
# The script can be run manually by passing the argument "RUN_NOW" or "RUN_NOW_HOURLY".
# The script requires the MySQL root password to be set in the ADMIN_PASS variable.
# The maximum number of hourly backups can be set in the MAX_HOURLY_BACKUP variable.
#!/bin/bash
BACKUP_DIR="/mySqlBackupDir" #Directory to store backup files.
ADMIN_PASS="root_pwd"        #MySQL root password.
MAX_HOURLY_BACKUP=24          #Max number of hourly backup. Default is 24.
MIN_SQL_FILE_SIZE_MB=20      #Min size of backup sql file. If less than it -> Ignore backup process.
# echo "DEBUG 1"

#Check BACKUP_DIR. If not exist, create it.
if [ ! -d "$BACKUP_DIR" ]
then
  mkdir $BACKUP_DIR
fi

# echo "DEBUG 2"

#Run every day at 11:59 PM
#Run if argument is RUN_NOW
if [ "$1" = "RUN_NOW" ]
then
  echo "Running backup with RUN_NOW argument"
  DATE=$(date +%d-%m-%Y__%Hh%M)
  mysqldump -u root -p$ADMIN_PASS --all-databases > $BACKUP_DIR/backup_$DATE.sql
  tar -zcvf $BACKUP_DIR/backup_$DATE.tar.gz $BACKUP_DIR/backup_$DATE.sql
  rm -f $BACKUP_DIR/backup_$DATE.sql
  exit 0
fi

# echo "DEBUG 3"

#Run every day at 11:58 PM
while true
do
  # echo "DEBUG 4"
  #Backup every day at 11:58 PM
  if [ `date +%H` -eq 23 ] && [ `date +%M` -eq 45 ]
  then
    echo "Running backup at 11:45 PM"
    DATE=$(date +%d-%m-%Y__%Hh%M)
    mysqldump -u root -p$ADMIN_PASS --all-databases > backup_$DATE.sql
    tar -zcvf $BACKUP_DIR/backup_$DATE.tar.gz backup_$DATE.sql
    rm backup_$DATE.sql
  fi
  #Backup every 1 hour
  if [ `date +%M` -eq 0 ] || [ "$1" == "RUN_NOW_HOURLY" ]
  then
    echo "Running backup at $(date +%H):00"
    #Backup current database to backup_last_1h.sql
    mysqldump -u root -p$ADMIN_PASS --all-databases > $BACKUP_DIR/backup_on_processing.sql
    #Check if size of backup sql file is larger than $MIN_SQL_FILE_SIZE_MB (Ex: 10MB) -> Accept. If not -> Reject.
    if [ -f $BACKUP_DIR/backup_on_processing.sql ]
    then
      if [ `du -m $BACKUP_DIR/backup_on_processing.sql | cut -f1` -lt $MIN_SQL_FILE_SIZE_MB ]
      then
        exit 0
      fi
    fi

    for i in {24..1}
    do
      #if i >= MAX_HOURLY_BACKUP -> Delete backup_last_ih.sql
      if [ $i -ge $MAX_HOURLY_BACKUP ]
      then
        if [ -f $BACKUP_DIR/backup_last_$i\h.sql ]
        then
          rm $BACKUP_DIR/backup_last_$i\h.sql
        fi
        continue
      fi
      #if i < MAX_HOURLY_BACKUP -> Rename backup_last_ih.sql to backup_last_(i+1)h.sql
      if [ -f $BACKUP_DIR/backup_last_$i\h.sql ]
      then
        mv $BACKUP_DIR/backup_last_$i\h.sql $BACKUP_DIR/backup_last_$(($i+1))\h.sql
      fi
    done
    #Backup current database to backup_last_1h.sql
    if [ -f $BACKUP_DIR/backup_on_processing.sql ]
    then
      mv $BACKUP_DIR/backup_on_processing.sql $BACKUP_DIR/backup_last_1h.sql
    fi
  fi
  sleep 60
done

