#!/bin/bash
BACKUP_DIR="/mySqlBackupDir"
#Run every day at 11:59 PM
while true
do
  if [ `date +%H` -eq 23 ] && [ `date +%M` -eq 59 ]
  then
    DATE=$(date +%d-%m-%Y__%Hh%M)
    mysqldump -u root -p'!Da#ImU%VuF3V' --all-databases > backup_$DATE.sql
    tar -zcvf $BACKUP_DIR/backup_$DATE.tar.gz backup_$DATE.sql
    rm backup_$DATE.sql
  fi
  sleep 60
done
