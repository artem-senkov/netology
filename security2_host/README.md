# Домашнее задание к занятию  «Защита хоста» Artem Senkov

------

### Задание 1

1. Установите **eCryptfs**.
2. Добавьте пользователя cryptouser.
3. Зашифруйте домашний каталог пользователя с помощью eCryptfs.

[debian homefolder encrypt](https://wiki.debian.org/TransparentEncryptionForHomeFolder)

```shell
sudo apt-get install ecryptfs-utils rsync lsof
sudo adduser cryptouser
sudo modprobe ecryptfs
sudo nano /etc/modules-load.d/modules.conf
sudo ecryptfs-migrate-home -u cryptouser
```

```
artem@debian11NET1:~$ sudo ecryptfs-migrate-home -u cryptouser
INFO:  Checking disk space, this may take a few moments.  Please be patient.
INFO:  Checking for open files in /home/cryptouser
lsof: WARNING: can't stat() fuse.gvfsd-fuse file system /run/user/1000/gvfs
      Output information may be incomplete.
Enter your login passphrase [cryptouser]:

************************************************************************
YOU SHOULD RECORD YOUR MOUNT PASSPHRASE AND STORE IT IN A SAFE LOCATION.
  ecryptfs-unwrap-passphrase ~/.ecryptfs/wrapped-passphrase
THIS WILL BE REQUIRED IF YOU NEED TO RECOVER YOUR DATA AT A LATER TIME.
************************************************************************


Done configuring.

chown: cannot access '/dev/shm/.ecryptfs-cryptouser': No such file or directory
INFO:  Encrypted home has been set up, encrypting files now...this may take a while.
sending incremental file list
./
.bash_logout
            220 100%    0.00kB/s    0:00:00 (xfr#1, to-chk=2/4)
.bashrc
          3,526 100%    3.36MB/s    0:00:00 (xfr#2, to-chk=1/4)
.profile
            807 100%  788.09kB/s    0:00:00 (xfr#3, to-chk=0/4)
Could not unlink the key(s) from your keying. Please use `keyctl unlink` if you wish to remove the key(s). Proceeding with umount.

========================================================================
Some Important Notes!

 1. The file encryption appears to have completed successfully, however,
    cryptouser MUST LOGIN IMMEDIATELY, _BEFORE_THE_NEXT_REBOOT_,
    TO COMPLETE THE MIGRATION!!!

 2. If cryptouser can log in and read and write their files, then the migration is complete,
    and you should remove /home/cryptouser.JT12n0Uh.
    Otherwise, restore /home/cryptouser.JT12n0Uh back to /home/cryptouser.

 3. cryptouser should also run 'ecryptfs-unwrap-passphrase' and record
    their randomly generated mount passphrase as soon as possible.

 4. To ensure the integrity of all encrypted data on this system, you
    should also encrypt swap space with 'ecryptfs-setup-swap'.
========================================================================

artem@debian11NET1:~$

```
Passphrase 12345 

Логинимся под пользователем cryptouser создаем пару файлов, создаем фразу для восстановления

```shell
artem@debian11NET1:~$ su cryptouser
Password:
cryptouser@debian11NET1:/home/artem$ cd ~
cryptouser@debian11NET1:~$ ls
cryptouser@debian11NET1:~$ pwd
/home/cryptouser
cryptouser@debian11NET1:~$ touch cryptouserhome.txt
cryptouser@debian11NET1:~$ touch test.txt
cryptouser@debian11NET1:~$ ecryptfs-unwrap-passphrase
Passphrase:
72f4cb08dd34d8ede4ad531f79d616b7
cryptouser@debian11NET1:~$
```

После перезагрузке домашний каталог пользователя cryptouser из под root
```
root@debian11NET1:/home# ls
artem  cryptouser  cryptouser.JT12n0Uh
root@debian11NET1:/home# cd cryptouser
root@debian11NET1:/home/cryptouser# ls
Access-Your-Private-Data.desktop  README.txt
root@debian11NET1:/home/cryptouser#
```



*В качестве ответа  пришлите снимки экрана домашнего каталога пользователя с исходными и зашифрованными данными.*  

### Задание 2

1. Установите поддержку **LUKS**.
2. Создайте небольшой раздел, например, 100 Мб.
3. Зашифруйте созданный раздел с помощью LUKS.

*В качестве ответа пришлите снимки экрана с поэтапным выполнением задания.*
```
root@debian11NET1:~# cryptsetup -y -v --type luks2 luksFormat /dev/sdb1
WARNING: Device /dev/sdb1 already contains a 'ext4' superblock signature.

WARNING!
========
This will overwrite data on /dev/sdb1 irrevocably.

Are you sure? (Type 'yes' in capital letters): yes
Operation aborted.

Command failed with code -1 (wrong or missing parameters).
root@debian11NET1:~# cryptsetup -y -v --type luks2 luksFormat /dev/sdb1
WARNING: Device /dev/sdb1 already contains a 'ext4' superblock signature.

WARNING!
========
This will overwrite data on /dev/sdb1 irrevocably.

Are you sure? (Type 'yes' in capital letters): YES
Enter passphrase for /dev/sdb1:
Verify passphrase:
Existing 'ext4' superblock signature (offset: 1080 bytes) on device /dev/sdb1 will be wiped.
Key slot 0 created.
Command successful.
root@debian11NET1:~# sudo cryptsetup luksOpen /dev/sdb1 disk
Enter passphrase for /dev/sdb1:
root@debian11NET1:~# ls /dev/mapper/disk
/dev/mapper/disk
root@debian11NET1:~# sudo dd if=/dev/zero of=/dev/mapper/disk

dd: writing to '/dev/mapper/disk': No space left on device
10448897+0 records in
10448896+0 records out
5349834752 bytes (5.3 GB, 5.0 GiB) copied, 341.328 s, 15.7 MB/s
root@debian11NET1:~#
root@debian11NET1:~# sudo mkfs.ext4 /dev/mapper/disk
mke2fs 1.46.2 (28-Feb-2021)
Creating filesystem with 1306112 4k blocks and 327040 inodes
Filesystem UUID: 99a6bf8e-7b94-4ee8-a06d-30416b304f43
Superblock backups stored on blocks:
        32768, 98304, 163840, 229376, 294912, 819200, 884736

Allocating group tables: done
Writing inode tables: done
Creating journal (16384 blocks): done
Writing superblocks and filesystem accounting information: done

root@debian11NET1:~# mkdir .secret
root@debian11NET1:~# mount /dev/mapper/disk .secret
root@debian11NET1:~# ls
root@debian11NET1:~# cd .secret
root@debian11NET1:~/.secret# ls
lost+found
root@debian11NET1:~/.secret# touch 123.txt
root@debian11NET1:~/.secret# ls
123.txt  lost+found
```

## Дополнительные задания (со звёздочкой*)

Эти задания дополнительные, то есть не обязательные к выполнению, и никак не повлияют на получение вами зачёта по этому домашнему заданию. Вы можете их выполнить, если хотите глубже шире разобраться в материале

### Задание 3 *

1. Установите **apparmor**.
2. Повторите эксперимент, указанный в лекции.
3. Отключите (удалите) apparmor.


*В качестве ответа пришлите снимки экрана с поэтапным выполнением задания.*


