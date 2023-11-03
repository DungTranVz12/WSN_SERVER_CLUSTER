#!/bin/bash
BACKUP_DIR="/mySqlBackupDir"
ADMIN_PASS="root_pwd"
#Run every day at 11:59 PM
#Run if argument is RUN_NOW
if [ "$1" == "RUN_NOW" ]
then
  DATE=$(date +%Y-%m-%d__%Hh%M)
  mysqldump -u root -padmin --all-databases > $BACKUP_DIR/backup_$DATE.sql
  tar -zcvf $BACKUP_DIR/backup_$DATE.tar.gz $BACKUP_DIR/backup_$DATE.sql
  rm -f $BACKUP_DIR/backup_$DATE.sql
  exit 0
fi

#Run every day at 11:58 PM
while true
do
  #Backup every day at 11:58 PM
  if [ `date +%H` -eq 23 ] && [ `date +%M` -eq 58 ]
  then
    DATE=$(date +%d-%m-%Y__%Hh%M)
    mysqldump -u root -p$ADMIN_PASS --all-databases > backup_$DATE.sql
    tar -zcvf $BACKUP_DIR/backup_$DATE.tar.gz backup_$DATE.sql
    rm backup_$DATE.sql
  fi
  #Backup every 1 hour
  if [ `date +%M` -eq 0 ]
  then
    #Delete backup of last_24h. Then rename last_23h to last_24h, last_22h to last_23h, etc. If they exist.
    if [ -f $BACKUP_DIR/backup_last_24h.sql ]
    then
      rm $BACKUP_DIR/backup_last_24h.sql
    fi
    for i in {23..1}
    do
      if [ -f $BACKUP_DIR/backup_last_$i\h.sql ]
      then
        mv $BACKUP_DIR/backup_last_$i\h.sql $BACKUP_DIR/backup_last_$(($i+1))\h.sql
      fi
    done
    #Backup current database to backup_last_1h.sql
    mysqldump -u root -p$ADMIN_PASS --all-databases > $BACKUP_DIR/backup_last_1h.sql
  fi
  sleep 60
done
