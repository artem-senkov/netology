# Домашнее задание к занятию 10.4 «Резервное копирование» Artem Senkov
---

### Задание 1

В чём разница между:

- полным резервным копированием,
Full backup создается полная копия всех данных

- дифференциальным резервным копированием,
При каждом копирование отсчет изменений идет от последней полной копии

- инкрементным резервным копированием.
При каждом копирование отсчет изменений идет от предыдущей копии n-1
*Приведите ответ в свободной форме.*

---

### Задание 2

Установите программное обеспечении Bacula, настройте bacula-dir, bacula-sd,  bacula-fd. Протестируйте работу сервисов.

*Пришлите:*   
*- конфигурационные файлы для bacula-dir, bacula-sd,  bacula-fd,*   
*- скриншот, подтверждающий успешное прохождение резервного копирования.*

#### bacula-dir.conf
```
Director {                            # define myself
  Name = deb11-10-dir
  DIRport = 9101                # where we listen for UA connections
  QueryFile = "/etc/bacula/scripts/query.sql"
  WorkingDirectory = "/var/lib/bacula"
  PidDirectory = "/run/bacula"
  Maximum Concurrent Jobs = 20
  Password = "8YuTZ-ru0D_6H_X17YtaSWGUBBAD4-aLC"         # Console password
  Messages = Daemon
  DirAddress = 127.0.0.1
}

JobDefs {
  Name = "DefaultJob"
  Type = Backup
  Level = Incremental
  Client = deb11-10-fd
  FileSet = "Full Set"
  Schedule = "WeeklyCycle"
  Storage = File1
  Messages = Standard
  Pool = File
  SpoolAttributes = yes
  Priority = 10
  Write Bootstrap = "/var/lib/bacula/%c.bsr"
}


#
# Define the main nightly save backup job
#   By default, this job will back up to disk in /nonexistant/path/to/file/archive/dir
Job {
  Name = "BackupClient1"
  JobDefs = "DefaultJob"
}

# Backup the catalog database (after the nightly save)
Job {
  Name = "BackupCatalog"
  JobDefs = "DefaultJob"
  Level = Full
  FileSet="Catalog"
  Schedule = "WeeklyCycleAfterBackup"
  # This creates an ASCII copy of the catalog
  # Arguments to make_catalog_backup.pl are:
  #  make_catalog_backup.pl <catalog-name>
  RunBeforeJob = "/etc/bacula/scripts/make_catalog_backup.pl MyCatalog"
  # This deletes the copy of the catalog
  RunAfterJob  = "/etc/bacula/scripts/delete_catalog_backup"
  Write Bootstrap = "/var/lib/bacula/%n.bsr"
  Priority = 11                   # run after main backup
}

#
# Standard Restore template, to be changed by Console program
#  Only one such job is needed for all Jobs/Clients/Storage ...
#
Job {
  Name = "RestoreFiles"
  Type = Restore
  Client=deb11-10-fd
  Storage = File1
# The FileSet and Pool directives are not used by Restore Jobs
# but must not be removed
  FileSet="Full Set"
  Pool = File
  Messages = Standard
  Where = /nonexistant/path/to/file/archive/dir/bacula-restores
}


# List of files to be backed up
FileSet {
  Name = "Full Set"
  Include {
    Options {
      signature = MD5
    }
#
#  Put your list of files here, preceded by 'File =', one per line
#    or include an external list with:
#
#    File = <file-name
#
#  Note: / backs up everything on the root partition.
#    if you have other partitions such as /usr or /home
#    you will probably want to add them too.
#
#  By default this is defined to point to the Bacula binary
#    directory to give a reasonable FileSet to backup to
#    disk storage during initial testing.
#
    File = /usr/sbin
  }

#
# If you backup the root directory, the following two excluded
#   files can be useful
#
  Exclude {
    File = /var/lib/bacula
    File = /nonexistant/path/to/file/archive/dir
    File = /proc
    File = /tmp
    File = /sys
    File = /.journal
    File = /.fsck
  }
}

#
# When to do the backups, full backup on first sunday of the month,
#  differential (i.e. incremental since full) every other sunday,
#  and incremental backups other days
Schedule {
  Name = "WeeklyCycle"
  Run = Full 1st sun at 23:05
  Run = Differential 2nd-5th sun at 23:05
  Run = Incremental mon-sat at 23:05
}

# This schedule does the catalog. It starts after the WeeklyCycle
Schedule {
  Name = "WeeklyCycleAfterBackup"
  Run = Full sun-sat at 23:10
}

# This is the backup of the catalog
FileSet {
  Name = "Catalog"
  Include {
    Options {
      signature = MD5
    }
    File = "/var/lib/bacula/bacula.sql"
  }
}

# Client (File Services) to backup
Client {
  Name = deb11-10-fd
  Address = localhost
  FDPort = 9102
  Catalog = MyCatalog
  Password = "J8DMQJBAO0YLC7qXp8l_6F7fi8BTRsk8B"          # password for FileDaemon
  File Retention = 60 days            # 60 days
  Job Retention = 6 months            # six months
  AutoPrune = yes                     # Prune expired Jobs/Files
}


# Definition of file Virtual Autochanger device
Autochanger {
  Name = File1
# Do not use "localhost" here
  Address = localhost                # N.B. Use a fully qualified name here
  SDPort = 9103
  Password = "EFvH2r4KISX3AZIfWVJgOwhohNZGa1hnz"
  Device = FileChgr1
  Media Type = File1
  Maximum Concurrent Jobs = 10        # run up to 10 jobs a the same time
  Autochanger = File1                 # point to ourself
}

# Definition of a second file Virtual Autochanger device
#   Possibly pointing to a different disk drive
Autochanger {
  Name = File2
# Do not use "localhost" here
  Address = localhost                # N.B. Use a fully qualified name here
  SDPort = 9103
  Password = "EFvH2r4KISX3AZIfWVJgOwhohNZGa1hnz"
  Device = FileChgr2
  Media Type = File2
  Autochanger = File2                 # point to ourself
  Maximum Concurrent Jobs = 10        # run up to 10 jobs a the same time
}



# Generic catalog service
Catalog {
  Name = MyCatalog
  dbname = "bacula"; DB Address = "localhost"; dbuser = "bacula"; dbpassword = "Japan2013"
}

# Reasonable message delivery -- send most everything to email address
#  and to the console
Messages {
  Name = Standard
  mailcommand = "/usr/sbin/bsmtp -h localhost -f \"\(Bacula\) \<%r\>\" -s \"Bacula: %t %e of %c %l\" %r"
  operatorcommand = "/usr/sbin/bsmtp -h localhost -f \"\(Bacula\) \<%r\>\" -s \"Bacula: Intervention needed for %j\" %r"
  mail = root = all, !skipped
  operator = root = mount
  console = all, !skipped, !saved
  append = "/var/log/bacula/bacula.log" = all, !skipped
  catalog = all
}


#
# Message delivery for daemon messages (no job).
Messages {
  Name = Daemon
  mailcommand = "/usr/sbin/bsmtp -h localhost -f \"\(Bacula\) \<%r\>\" -s \"Bacula daemon message\" %r"
  mail = root = all, !skipped
  console = all, !skipped, !saved
  append = "/var/log/bacula/bacula.log" = all, !skipped
}

# Default pool definition
Pool {
  Name = Default
  Pool Type = Backup
  Recycle = yes                       # Bacula can automatically recycle Volumes
  AutoPrune = yes                     # Prune expired volumes
  Volume Retention = 365 days         # one year
  Maximum Volume Bytes = 50G          # Limit Volume size to something reasonable
  Maximum Volumes = 100               # Limit number of Volumes in Pool
}

# File Pool definition
Pool {
  Name = File
  Pool Type = Backup
  Recycle = yes                       # Bacula can automatically recycle Volumes
  AutoPrune = yes                     # Prune expired volumes
  Volume Retention = 365 days         # one year
  Maximum Volume Bytes = 50G          # Limit Volume size to something reasonable
  Maximum Volumes = 100               # Limit number of Volumes in Pool
  Label Format = "Vol-"               # Auto label
}


# Scratch pool definition
Pool {
  Name = Scratch
  Pool Type = Backup
}

#
# Restricted console used by tray-monitor to get the status of the director
#
Console {
  Name = deb11-10-mon
  Password = "xx9yDWNgJJwmKi2HbcJJ6Zeofvl3z-Dyi"
  CommandACL = status, .status
}

```
#### bacula-fd.conf
```
#
# Default  Bacula File Daemon Configuration file
#
#  For Bacula release 9.6.7 (10 December 2020) -- debian bullseye/sid
#
# There is not much to change here except perhaps the
# File daemon Name to
#
#
# Copyright (C) 2000-2020 Kern Sibbald
# License: BSD 2-Clause; see file LICENSE-FOSS
#

#
# List Directors who are permitted to contact this File daemon
#
Director {
  Name = deb11-10-dir
  Password = "J8DMQJBAO0YLC7qXp8l_6F7fi8BTRsk8B"
}

#
# Restricted Director, used by tray-monitor to get the
#   status of the file daemon
#
Director {
  Name = deb11-10-mon
  Password = "OQwq4r6S2i7gOOm1hngIwHct3NJD_I1_S"
  Monitor = yes
}

#
# "Global" File daemon configuration specifications
#
FileDaemon {                          # this is me
  Name = deb11-10-fd
  FDport = 9102                  # where we listen for the director
  WorkingDirectory = /var/lib/bacula
  Pid Directory = /run/bacula
  Maximum Concurrent Jobs = 20
  Plugin Directory = /usr/lib/bacula
  FDAddress = 127.0.0.1
}

# Send all messages except skipped files back to Director
Messages {
  Name = Standard
  director = deb11-10-dir = all, !skipped, !restored
}

```
#### bacula-sd.conf
```
#
# Default Bacula Storage Daemon Configuration file
#
#  For Bacula release 9.6.7 (10 December 2020) -- debian bullseye/sid
#
Storage {                             # definition of myself
  Name = deb11-10-sd
  SDPort = 9103                  # Director's port
  WorkingDirectory = "/var/lib/bacula"
  Pid Directory = "/run/bacula"
  Plugin Directory = "/usr/lib/bacula"
  Maximum Concurrent Jobs = 5
  SDAddress = 127.0.0.1
}

#
# List Directors who are permitted to contact Storage daemon
#
Director {
  Name = deb11-10-dir
  Password = "EFvH2r4KISX3AZIfWVJgOwhohNZGa1hnz"
}

#
# Restricted Director, used by tray-monitor to get the
#   status of the storage daemon
#
Director {
  Name = deb11-10-mon
  Password = "6DVtN3koVeKNIBKLzp6plhCi0swQjyboO"
  Monitor = yes
}
# Define a Virtual autochanger
#
Autochanger {
  Name = FileChgr1
  Device = FileChgr1-Dev1, FileChgr1-Dev2
  Changer Command = ""
  Changer Device = /dev/null
}

Device {
  Name = FileChgr1-Dev1
  Media Type = File1
  Archive Device = /backup1
  LabelMedia = yes;                   # lets Bacula label unlabeled media
  Random Access = Yes;
  AutomaticMount = yes;               # when device opened, read it
  RemovableMedia = no;
  AlwaysOpen = no;
  Maximum Concurrent Jobs = 5
}

Device {
  Name = FileChgr1-Dev2
  Media Type = File1
  Archive Device = /backup2
  LabelMedia = yes;                   # lets Bacula label unlabeled media
  Random Access = Yes;
  AutomaticMount = yes;               # when device opened, read it
  RemovableMedia = no;
  AlwaysOpen = no;
  Maximum Concurrent Jobs = 5
}

#
# Define a second Virtual autochanger
#
Autochanger {
  Name = FileChgr2
  Device = FileChgr2-Dev1, FileChgr2-Dev2
  Changer Command = ""
  Changer Device = /dev/null
}

Device {
  Name = FileChgr2-Dev1
  Media Type = File2
  Archive Device = /backup1
  LabelMedia = yes;                   # lets Bacula label unlabeled media
  Random Access = Yes;
  AutomaticMount = yes;               # when device opened, read it
  RemovableMedia = no;
  AlwaysOpen = no;
  Maximum Concurrent Jobs = 5
}

Device {
  Name = FileChgr2-Dev2
  Media Type = File2
  Archive Device = /backup2
  LabelMedia = yes;                   # lets Bacula label unlabeled media
  Random Access = Yes;
  AutomaticMount = yes;               # when device opened, read it
  RemovableMedia = no;
  AlwaysOpen = no;
  Maximum Concurrent Jobs = 5
}

Messages {
  Name = Standard
  director = deb11-10-dir = all
}

```
![img1](https://github.com/artem-senkov/netology/blob/main/backup/img/bacula-status.png)
---

### Задание 3

Установите программное обеспечении Rsync. Настройте синхронизацию на двух нодах. Протестируйте работу сервиса.

*Пришлите рабочую конфигурацию сервера и клиента Rsync блоком кода в вашем md-файле.*

#### server
```
pid file = /var/run/rsyncd.pid
log file = /var/log/rsyncd.log
transfer logging = true
munge symlinks = yes
# use chroot = yes
# папка источник для бэкапа

[data]
path = /data
uid = root
read only = yes
list = yes
comment = Data backup Dir
auth users = backup
hosts allow = *
secrets file = /etc/rsyncd.scrt

[root]
path = /root
uid = root
read only = yes
list = yes
comment = Root backup Dir
auth users = backup
hosts allow = *
secrets file = /etc/rsyncd.scrt

```
#### client
```
#!/bin/bash
date
# Папка, куда будем складывать архивы — ее либо сразу создать либо не создавать а положить в уже существующие
syst_dir=/backup/
# Имя сервера, который архивируем
srv_name=deb11-20
# Адрес сервера, который архивируем
srv_ip=192.168.56.20
# Пользователь rsync на сервере, который архивируем
srv_user=backup
# Ресурс на сервере для бэкапа
srv_dir=data
echo "Start backup ${srv_name}"
# Создаем папку для инкрементных бэкапов
mkdir -p ${syst_dir}${srv_name}/increment/
/usr/bin/rsync --debug=ALL -avz --progress --delete --password-file=/etc/rsyncd.scrt ${srv_user}@${srv_ip}::${srv_dir} ${syst_dir}${srv_name}/current/ --backup --backup-dir=${syst_dir}${srv_name}/increment/`date +%Y-%m-%d`/
/usr/bin/find ${syst_dir}${srv_name}/increment/ -maxdepth 1 -type d -mtime +30 -exec rm -rf {} \;
date
echo "Finish backup ${srv_name}"

```

---

### Задание со звёздочкой*
Это задание дополнительное. Его можно не выполнять. На зачёт это не повлияет. Вы можете его выполнить, если хотите глубже разобраться в материале.

---

### Задание 4*

Настройте резервное копирование двумя или более методами, используя одну из рассмотренных команд для папки /etc/default. Проверьте резервное копирование.

*Пришлите рабочую конфигурацию выбранного сервиса по поставленной задаче.*
#### rsync server
```

[etcdefault]
path = /etc/default
uid = root
read only = yes
list = yes
comment = etc/default  backup Dir
auth users = backup
hosts allow = *
secrets file = /etc/rsyncd.scrt



```
### bacula

#### client
```
#!/bin/bash
date
# Папка, куда будем складывать архивы — ее либо сразу создать либо не создавать а положить в уже существующие
syst_dir=/backup/
# Имя сервера, который архивируем
srv_name=deb11-20
# Адрес сервера, который архивируем
srv_ip=192.168.56.20
# Пользователь rsync на сервере, который архивируем
srv_user=backup
# Ресурс на сервере для бэкапа
srv_dir=etcdefault
echo "Start backup ${srv_name}"
# Создаем папку для инкрементных бэкапов
mkdir -p ${syst_dir}${srv_name}/increment/
/usr/bin/rsync --debug=ALL -avz --progress --delete --password-file=/etc/rsyncd.scrt ${srv_user}@${srv_ip}::${srv_dir} ${syst_dir}${srv_name}/current/ --backup --backup-dir=${syst_dir}${srv_name}/increment/`date +%Y-%m-%d`/
/usr/bin/find ${syst_dir}${srv_name}/increment/ -maxdepth 1 -type d -mtime +30 -exec rm -rf {} \;
date
echo "Finish backup ${srv_name}"

```
### bacula


#### bacula client
```
Director {
  Name = deb11-10-dir
  Password = "J8DMQJBAO0YLC7qXp8l_6F7fi8BTRsk8B"
}

#
# Restricted Director, used by tray-monitor to get the
#   status of the file daemon
#
Director {
  Name = deb11-10-mon
  Password = "OQwq4r6S2i7gOOm1hngIwHct3NJD_I1_S"
  Monitor = yes
}
#
# "Global" File daemon configuration specifications
#
FileDaemon {                          # this is me
  Name = deb11-20-fd
  FDport = 9102                  # where we listen for the director
  WorkingDirectory = /var/lib/bacula
  Pid Directory = /run/bacula
  Maximum Concurrent Jobs = 20
  Plugin Directory = /usr/lib/bacula
  FDAddress = 192.168.56.20
}

# Send all messages except skipped files back to Director
Messages {
  Name = Standard
  director = deb11-10-dir = all, !skipped, !restored
}
```
#### bacula director добавил
```
Client {
  Name = deb11-20-fd
  Address = 192.168.56.20
  FDPort = 9102
  Catalog = MyCatalog
  Password = "J8DMQJBAO0YLC7qXp8l_6F7fi8BTRsk8B"          # password for FileDaemon
  File Retention = 60 days            # 60 days
  Job Retention = 6 months            # six months
  AutoPrune = yes                     # Prune expired Jobs/Files
}
  
JobDefs {
  Name = "deb11-20Job"
  Type = Backup
  Level = Incremental
  Client = deb11-20-fd
  FileSet = "etcdefault"
  Schedule = "WeeklyCycle"
  Storage = File1
  Messages = Standard
  Pool = File
  SpoolAttributes = yes
  Priority = 10
  Write Bootstrap = "/var/lib/bacula/%c.bsr"
}
  

Job {
  Name = "Backup-deb11-20"
  JobDefs = "deb11-20Job"
  Level = Full
  FileSet="etcdefault"
  Schedule = "WeeklyCycleAfterBackup"
  RunBeforeJob = "/etc/bacula/scripts/make_catalog_backup.pl MyCatalog"
  RunAfterJob  = "/etc/bacula/scripts/delete_catalog_backup"
  Write Bootstrap = "/var/lib/bacula/%n.bsr"
  Priority = 11                   # run after main backup
}

FileSet {
  Name = "etcdefault"
  Include {
    Options {
      signature = MD5
    }
    File = /etc/default
  }

 Exclude {
    File = /.fsck
  }
}
  
  

```
