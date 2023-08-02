# Домашнее задание к занятию «Резервное копирование баз данных» Artem Senkov

---

### Задание 1. Резервное копирование

### Кейс

Финансовая компания решила увеличить надёжность работы баз данных и их резервного копирования. 

Необходимо описать, какие варианты резервного копирования подходят в случаях: 

1.1. Необходимо восстанавливать данные в полном объёме за предыдущий день.

Я бы предложил следующую схему.
* Еженедельно - full backup
* Ежедневно - differental backup
Время выполнения зависит от графика работы например ВС - 01-00 am

1.2. Необходимо восстанавливать данные за час до предполагаемой поломки.

* Еженедельно - full backup
* Ежедневно - differental backup
* Ежечастно - incremenental 
* Время выполнения зависит от графика работы например ВС -СБ - 01-00 am


1.3.* Возможен ли кейс, когда при поломке базы происходило моментальное переключение на работающую или починенную базу данных.

***Возможен если создать схему 
Возможно с помощью репликации ACTIVE MASTER -SLAVE и при выходе из строя MASTER автоматически переназначать роль мастера на SLAVE***

*Приведите ответ в свободной форме.*

---

### Задание 2. PostgreSQL

2.1. С помощью официальной документации приведите пример команды резервирования данных и восстановления БД (pgdump/pgrestore).

[https://postgrespro.ru](https://postgrespro.ru/docs/postgresql/15/app-pgdump?lang=en)

[https://selectel.ru/blog/postgresql-backup-tools/](https://selectel.ru/blog/postgresql-backup-tools/)

~~~
Резервное копирование и восстановление одной базы
pg_dump mydb > /backup/mydb.dump
pg_restore -d mydb /backup/mydb.dump

Полностью все данные можно забэкапить так
pg_dumpall > /backup/instance.bak

~~~

2.1.* Возможно ли автоматизировать этот процесс? Если да, то как?

*Приведите ответ в свободной форме.*

Скрипт для автобэкапа базы и поддержания глубины бэкапа 61 день
```
#!/bin/sh

PATH=/etc:/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin:/usr/local/sbin

PGPASSWORD=some_password
export PGPASSWORD
pathB=/mnt/backup
dbUser=dbadmin
database=zabbix


find $pathB \( -name "*-1[^5].*" -o -name "*-[023]?.*" \) -ctime +61 -delete
pg_dump -U $dbUser $database | gzip > $pathB/pgsql_$(date "+%Y-%m-%d").sql.gz


unset PGPASSWORD
```

Добавляем в планировщик
```
# crontab -e
3 0 * * * /etc/scripts/pgsql_dump.sh # postgres pg dump
```
---

### Задание 3. MySQL

3.1. С помощью официальной документации приведите пример команды инкрементного резервного копирования базы данных MySQL. 
На бесплатной версии нужно включить binary log

```
server-id        = 1
expire_logs_days = 10
binlog_format    = row
log_bin          = /var/log/mysql/mysql-bin
```

Сделать полный бэкап

А после бэкапить bin-log файлы.

Например таким скриптом
```
#!/bin/sh

# set up the date variable
NOW=$(date +%Y%m%d%H%M%S)
BINLOG_BACKUP=${NOW}_binlog.tar.gz

# set up the database credentials
DB_USER=root
DB_PASSWORD=root_password

# binary log files directory path
BINLOGS_PATH=/var/log/mysql/

# flush the current log and start writing to a new binary log file
mysql -u$DB_USER -p$DB_PASSWORD -E --execute='FLUSH BINARY LOGS;' mysql

# get a list of all binary log files
BINLOGS=$(mysql -u$DB_USER -p$DB_PASSWORD -E --execute='SHOW BINARY LOGS;' mysql | grep Log_name | sed -e 's/Log_name://g' -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')

# get the most recent binary log file
BINLOG_CURRENT=`echo "${BINLOGS}" | tail -n -1`

# get list of binary logs to be backed up (everything except the most recent one)
BINLOGS_FOR_BACKUP=`echo "${BINLOGS}" | head -n -1`

# create a list of the full paths to the binary logs to be backed up
BINLOGS_FULL_PATH=`echo "${BINLOGS_FOR_BACKUP}" | xargs -I % echo $BINLOGS_PATH%`

# compress the list of binary logs to be backed up into an archive in the backup location
tar -czvf /sites/backups/$BINLOG_BACKUP $BINLOGS_FULL_PATH

# delete the binary logs that have been backed up
echo $BINLOG_CURRENT | xargs -I % mysql -u$DB_USER -p$DB_PASSWORD -E --execute='PURGE BINARY LOGS TO "%";' mysql

```

Есть сторонние программы которые работают проще для пользователя
[xtra backup](https://docs.percona.com/percona-xtrabackup/2.4/index.html)



3.1.* В каких случаях использование реплики будет давать преимущество по сравнению с обычным резервным копированием?

*Приведите ответ в свободной форме.*

***Когда нужно быстро переключиться на резервный сервер БД и продолжить работу лучше использовать репликвцию, во многих сценариях может не быть времени на восстановление из бэкапа и простои невозможны. Но в целом это разные инструменты и использование реплики не отменяет резервное копирование.***

---

Задания, помеченные звёздочкой, — дополнительные, то есть не обязательные к выполнению, и никак не повлияют на получение вами зачёта по этому домашнему заданию. Вы можете их выполнить, если хотите глубже шире разобраться в материале.
