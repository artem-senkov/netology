# Домашнее задание к занятию «Уязвимости и атаки на информационные системы» Artem Senkov

------

### Задание 1

Скачайте и установите виртуальную машину Metasploitable: https://sourceforge.net/projects/metasploitable/.

Это типовая ОС для экспериментов в области информационной безопасности, с которой следует начать при анализе уязвимостей.

Просканируйте эту виртуальную машину, используя **nmap**.

Попробуйте найти уязвимости, которым подвержена эта виртуальная машина.

Сами уязвимости можно поискать на сайте https://www.exploit-db.com/.

Для этого нужно в поиске ввести название сетевой службы, обнаруженной на атакуемой машине, и выбрать подходящие по версии уязвимости.

Ответьте на следующие вопросы:

- Какие сетевые службы в ней разрешены?

```
C:\WINDOWS\system32>nmap -sV 192.168.24.3
Starting Nmap 7.94 ( https://nmap.org ) at 2023-08-14 21:49 RTZ 2 (чшьр)
Nmap scan report for 192.168.24.3
Host is up (0.00092s latency).
Not shown: 977 closed tcp ports (reset)
PORT     STATE SERVICE     VERSION
21/tcp   open  ftp         vsftpd 2.3.4
22/tcp   open  ssh         OpenSSH 4.7p1 Debian 8ubuntu1 (protocol 2.0)
23/tcp   open  telnet      Linux telnetd
25/tcp   open  smtp        Postfix smtpd
53/tcp   open  domain      ISC BIND 9.4.2
80/tcp   open  http        Apache httpd 2.2.8 ((Ubuntu) DAV/2)
111/tcp  open  rpcbind     2 (RPC #100000)
139/tcp  open  netbios-ssn Samba smbd 3.X - 4.X (workgroup: WORKGROUP)
445/tcp  open  netbios-ssn Samba smbd 3.X - 4.X (workgroup: WORKGROUP)
512/tcp  open  exec        netkit-rsh rexecd
513/tcp  open  login?
514/tcp  open  shell       Netkit rshd
1099/tcp open  java-rmi    GNU Classpath grmiregistry
1524/tcp open  bindshell   Metasploitable root shell
2049/tcp open  nfs         2-4 (RPC #100003)
2121/tcp open  ftp         ProFTPD 1.3.1
3306/tcp open  mysql       MySQL 5.0.51a-3ubuntu5
5432/tcp open  postgresql  PostgreSQL DB 8.3.0 - 8.3.7
5900/tcp open  vnc         VNC (protocol 3.3)
6000/tcp open  X11         (access denied)
6667/tcp open  irc         UnrealIRCd
8009/tcp open  ajp13       Apache Jserv (Protocol v1.3)
8180/tcp open  http        Apache Tomcat/Coyote JSP engine 1.1
MAC Address: 08:00:27:49:B5:8C (Oracle VirtualBox virtual NIC)
Service Info: Hosts:  metasploitable.localdomain, irc.Metasploitable.LAN; OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 19.13 seconds
```

- Какие уязвимости были вами обнаружены? (список со ссылками: достаточно трёх уязвимостей)
- 
[ProFTPd IAC 1.3.x - Remote Command Execution](https://www.exploit-db.com/exploits/15449)

[OpenSSH < 6.6 SFTP - Command Execution](https://www.exploit-db.com/exploits/45001)

[Apache < 2.2.34 / < 2.4.27 - OPTIONS Memory Leak](https://www.exploit-db.com/exploits/42745)

[PostgreSQL 8.2/8.3/8.4 - UDF for Command Execution](https://www.exploit-db.com/exploits/7855)



*Приведите ответ в свободной форме.*  

### Задание 2

Проведите сканирование Metasploitable в режимах SYN, FIN, Xmas, UDP.

Запишите сеансы сканирования в Wireshark.

Ответьте на следующие вопросы:

- Чем отличаются эти режимы сканирования с точки зрения сетевого трафика?

SYN и FIN, XMAS отличается флагами в пакете TCP

SYN Flags: 0x002 (SYN)

FIN -Flags: 0x001 (FIN)

XMAX -Flags: 0x029 (FIN, PSH, URG)

UDP использует транспорьный протокол UDP



[Manual SYN -s](https://nmap.org/book/synscan.html)

[-sX -sF](https://nmap.org/book/scan-methods-null-fin-xmas-scan.html)

[UDP -sU](https://nmap.org/book/scan-methods-udp-scan.html)



- Как отвечает сервер?
При сканировании SYN сервер пытается устанвить сессию или отвечает RST если порт закрыт
![img](https://github.com/artem-senkov/netology/blob/main/security1/img/syn.png)

При сканировании XMAX  и FIN сервер не отвечает если порт открыт, RST если закрыт
![img](https://github.com/artem-senkov/netology/blob/main/security1/img/fin.png)

Ксли при сканировании по UDP сервер отвечает все кроме ICMP port unreachable error (type 3, code 3) то порт либо открыт либо filtred
![img](https://github.com/artem-senkov/netology/blob/main/security1/img/udp.png)



