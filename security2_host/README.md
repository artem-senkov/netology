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
**В debian 11 Каталог при логоне не подключается это баг нужно выполнить keyctl link @u @s
и затем ecryptfs-mount-private**

```
cryptouser@debian11NET1:/etc/pam.d$ keyctl link @u @s
cryptouser@debian11NET1:/etc/pam.d$ ecryptfs-mount-private
cryptouser@debian11NET1:/etc/pam.d$ cd ~
cryptouser@debian11NET1:~$ ls
 Desktop     Downloads   Pictures   Templates     'Untitled 1.txt'
 Documents   Music       Public    'test folder'   Videos
cryptouser@debian11NET1:~$ df -T
Filesystem                Type     1K-blocks    Used Available Use% Mounted on
udev                      devtmpfs    983856       0    983856   0% /dev
tmpfs                     tmpfs       201824    1192    200632   1% /run
/dev/sda1                 ext4      19480400 4638312  13827204  26% /
tmpfs                     tmpfs      1009112       4   1009108   1% /dev/shm
tmpfs                     tmpfs         5120       4      5116   1% /run/lock
tmpfs                     tmpfs       201820    3360    198460   2% /run/user/1000
/home/cryptouser/.Private ecryptfs  19480400 4638312  13827204  26% /home/cryptouser
cryptouser@debian11NET1:~$
```

**Теперь все подключено.**



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

Установка
```
sudo apt install apparmor-profiles apparmor-utils
apparmor-profiles-extra
```
```
root@debian11NET1:~/.secret# sudo apparmor_status
apparmor module is loaded.
35 profiles are loaded.
18 profiles are in enforce mode.
   /usr/bin/evince
   /usr/bin/evince-previewer
   /usr/bin/evince-previewer//sanitized_helper
   /usr/bin/evince-thumbnailer
   /usr/bin/evince//sanitized_helper
   /usr/bin/man
   /usr/lib/cups/backend/cups-pdf
   /usr/sbin/cups-browsed
   /usr/sbin/cupsd
   /usr/sbin/cupsd//third_party
   libreoffice-senddoc
   libreoffice-soffice//gpg
   libreoffice-xpdfimport
   lsb_release
   man_filter
   man_groff
   nvidia_modprobe
   nvidia_modprobe//kmod
17 profiles are in complain mode.
   /usr/sbin/dnsmasq
   /usr/sbin/dnsmasq//libvirt_leaseshelper
   avahi-daemon
   identd
   klogd
   libreoffice-oopslash
   libreoffice-soffice
   mdnsd
   nmbd
   nscd
   ping
   smbd
   smbldap-useradd
   smbldap-useradd///etc/init.d/nscd
   syslog-ng
   syslogd
   traceroute
3 processes have profiles defined.
3 processes are in enforce mode.
   /usr/sbin/cups-browsed (483)
   /usr/sbin/cupsd (462)
   /usr/lib/cups/notifier/dbus (481) /usr/sbin/cupsd
0 processes are in complain mode.
0 processes are unconfined but have a profile defined.
```
Проверяем работу защиты

```
root@debian11NET1:~/.secret# sudo man 8.8.8.8 -c 4
man: socket: Operation not permitted
root@debian11NET1:~/.secret# ping 8.8.8.8 -c2
PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
64 bytes from 8.8.8.8: icmp_seq=1 ttl=117 time=82.8 ms
64 bytes from 8.8.8.8: icmp_seq=2 ttl=117 time=64.4 ms

--- 8.8.8.8 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1001ms
rtt min/avg/max/mdev = 64.401/73.619/82.838/9.218 ms
root@debian11NET1:~/.secret# man ping
man: socket: Operation not permitted
root@debian11NET1:~/.secret# aa-complain /usr/bin/man
Setting /usr/bin/man to complain mode.
root@debian11NET1:~/.secret# man 8.8.8.8
PING 8.8.8.8 (8.8.8.8) 56(84) bytes of data.
64 bytes from 8.8.8.8: icmp_seq=1 ttl=117 time=84.8 ms
64 bytes from 8.8.8.8: icmp_seq=2 ttl=117 time=66.1 ms
64 bytes from 8.8.8.8: icmp_seq=3 ttl=117 time=57.4 ms
^C
--- 8.8.8.8 ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2002ms
rtt min/avg/max/mdev = 57.443/69.454/84.834/11.433 ms
root@debian11NET1:~/.secret# aa-enforce /usr/bin/man
Setting /usr/bin/man to enforce mode.
root@debian11NET1:~/.secret# man 8.8.8.8
man: socket: Operation not permitted
root@debian11NET1:~/.secret#

```
Защита работает и блокирует подмененный man
