# Домашнее задание к занятию «Защита сети» Artem Senkov


### Подготовка к выполнению заданий

1. Подготовка защищаемой системы:

- установите **Suricata**,

```
sudo apt install software-properties-common
sudo add-apt-repository ppa:oisf/suricata-stable
sudo apt update
sudo apt install suricata
sudo suricata-update
sudo systemctl status suricata
```
**Нужно внести настройки интерфейса для мониторинга в конфиг**

```
artem@debian11NET1:~$ sudo nano /etc/suricata/suricata.yaml
artem@debian11NET1:~$ sudo systemctl restart suricata
artem@debian11NET1:~$ sudo systemctl status suricata
● suricata.service - Suricata IDS/IDP daemon
     Loaded: loaded (/lib/systemd/system/suricata.service; enabled; vendor preset: enabled)
     Active: active (running) since Sun 2023-08-20 18:15:23 IDT; 7s ago
       Docs: man:suricata(8)
             man:suricatasc(8)
             https://suricata-ids.org/docs/
    Process: 2101 ExecStart=/usr/bin/suricata -D --af-packet -c /etc/suricata/suricata.yaml --pidfile /run/suricata.pid (code=exited, status=0/SUCC>
   Main PID: 2102 (Suricata-Main)
      Tasks: 8 (limit: 2305)
     Memory: 46.9M
        CPU: 924ms
     CGroup: /system.slice/suricata.service
             └─2102 /usr/bin/suricata -D --af-packet -c /etc/suricata/suricata.yaml --pidfile /run/suricata.pid

Aug 20 18:15:22 debian11NET1 systemd[1]: Starting Suricata IDS/IDP daemon...
Aug 20 18:15:22 debian11NET1 suricata[2101]: 20/8/2023 -- 18:15:22 - <Notice> - This is Suricata version 6.0.1 RELEASE running in SYSTEM mode
Aug 20 18:15:23 debian11NET1 systemd[1]: Started Suricata IDS/IDP daemon.

```

- установите **Fail2Ban**.

```
```

2. Подготовка системы злоумышленника: установите **nmap** и **thc-hydra** либо скачайте и установите **Kali linux**.

Обе системы должны находится в одной подсети.

------

### Задание 1

Проведите разведку системы и определите, какие сетевые службы запущены на защищаемой системе:

**sudo nmap -sA < ip-адрес >**
```
└─$ sudo nmap -sA 192.168.124.137
Starting Nmap 7.93 ( https://nmap.org ) at 2023-08-20 11:32 EDT
Nmap scan report for 192.168.124.137
Host is up (0.00045s latency).
All 1000 scanned ports on 192.168.124.137 are in ignored states.
Not shown: 1000 unfiltered tcp ports (reset)
MAC Address: 08:00:27:06:94:C0 (Oracle VirtualBox virtual NIC)
Nmap done: 1 IP address (1 host up) scanned in 0.50 seconds
```
**sudo nmap -sT < ip-адрес >**
```
└─$ sudo nmap -sT 192.168.124.137
Starting Nmap 7.93 ( https://nmap.org ) at 2023-08-20 11:33 EDT
Nmap scan report for 192.168.124.137
Host is up (0.0010s latency).
Not shown: 999 closed tcp ports (conn-refused)
PORT   STATE SERVICE
22/tcp open  ssh
MAC Address: 08:00:27:06:94:C0 (Oracle VirtualBox virtual NIC)

Nmap done: 1 IP address (1 host up) scanned in 0.47 seconds
```
**sudo nmap -sS < ip-адрес >**
```
└─$ sudo nmap -sS 192.168.124.137
Starting Nmap 7.93 ( https://nmap.org ) at 2023-08-20 11:29 EDT
Nmap scan report for 192.168.124.137
Host is up (0.00089s latency).
Not shown: 999 closed tcp ports (reset)
PORT   STATE SERVICE
22/tcp open  ssh
MAC Address: 08:00:27:06:94:C0 (Oracle VirtualBox virtual NIC)
Nmap done: 1 IP address (1 host up) scanned in 0.47 seconds
```
**sudo nmap -sV < ip-адрес >**
```
└─$ sudo nmap -sV 192.168.124.137
Starting Nmap 7.93 ( https://nmap.org ) at 2023-08-20 11:34 EDT
Nmap scan report for 192.168.124.137
Host is up (0.00040s latency).
Not shown: 999 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.4p1 Debian 5+deb11u1 (protocol 2.0)
MAC Address: 08:00:27:06:94:C0 (Oracle VirtualBox virtual NIC)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 1.44 seconds
```

По желанию можете поэкспериментировать с опциями: https://nmap.org/man/ru/man-briefoptions.html.


*В качестве ответа пришлите события, которые попали в логи Suricata и Fail2Ban, прокомментируйте результат.*

Сканирование в лог не попало, нужно настраивать правила Suricata

sudo nano /etc/suricata/rules/suricata.rules

В результате получаем предупреждение:
```
artem@debian11NET1:~$ sudo tail -f /var/log/suricata/fast.log
08/20/2023-19:47:08.407349  [**] [1:2009582:3] ET SCAN NMAP -sS window 1024 [**] [Classification: Attempted Information Leak] [Priority: 2] {TCP} 192.168.124.72:64967 -> 192.168.124.137:554
08/20/2023-19:47:08.407182  [**] [1:2009582:3] ET SCAN NMAP -sS window 1024 [**] [Classification: Attempted Information Leak] [Priority: 2] {TCP} 192.168.124.72:64967 -> 192.168.124.137:21
08/20/2023-19:48:16.756553  [**] [1:2009582:3] ET SCAN NMAP -sS window 1024 [**] [Classification: Attempted Information Leak] [Priority: 2] {TCP} 192.168.124.72:52210 -> 192.168.124.137:53
```

------

### Задание 2

Проведите атаку на подбор пароля для службы SSH:

**hydra -L users.txt -P pass.txt < ip-адрес > ssh**

1. Настройка **hydra**: 
 
 - создайте два файла: **users.txt** и **pass.txt**;
 - в каждой строчке первого файла должны быть имена пользователей, второго — пароли. В нашем случае это могут быть случайные строки, но ради эксперимента можете добавить имя и пароль существующего пользователя.

Дополнительная информация по **hydra**: https://kali.tools/?p=1847.

2. Включение защиты SSH для Fail2Ban:

-  открыть файл /etc/fail2ban/jail.conf,
-  найти секцию **ssh**,
-  установить **enabled**  в **true**.

Дополнительная информация по **Fail2Ban**:https://putty.org.ru/articles/fail2ban-ssh.html.



*В качестве ответа пришлите события, которые попали в логи Suricata и Fail2Ban, прокомментируйте результат.*
