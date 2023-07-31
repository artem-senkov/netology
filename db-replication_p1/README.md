# Домашнее задание к занятию «Репликация и масштабирование. Часть 1» Artem Senkov

---

### Задание 1

На лекции рассматривались режимы репликации master-slave, master-master, опишите их различия.

*Ответить в свободной форме.*

---

### Задание 2

Выполните конфигурацию master-slave репликации, примером можно пользоваться из лекции.

*Приложите скриншоты конфигурации, выполнения работы: состояния и режимы работы серверов.*

```bash
curl -sSLO https://dev.mysql.com/get/mysql80-community-release-el7-9.noarch.rpm
sudo rpm -ivh  mysql80-community-release-el7-9.noarch.rpm
sudo yum install mysql-server
sudo mkdir -p /var/log/mysql
sudo mysqld --initialize
sudo chown - R mysql: /var/lib/mysql
sudo chown -R mysql: /var/log/mysql
sudo yum install nano
nano /etc/my.cnf
```
/etc/my.cnF модифицирую конфиг
```
bind-address=0.0.0.0
server-id=1
log_bin=/var/log/mysql/mybin.log
datadir=/var/lib/mysql
socket=/var/lib/mysql/mysql.sock
log-error=/var/log/mysqld.log
pid-file=/var/run/mysqld/mysqld.pid
```
```
sudo cat /var/log/mysqld.log
A temporary password is generated for root@localhost: FX>j3Xa%luw/
A temporary password is generated for root@localhost: Az*2K7tiGPKA
```
```
sudo systemctl start mysqld
mysql -u root -p
ALTER USER 'root'@'localhost' IDENTIFIED BY 'Passw0rd';
FLUSH PRIVILEGES;
CREATE USER 'replication'@'%' IDENTIFIED WITH mysql_native_password BY 'Reepl11Pass!';
GRANT REPLICATION SLAVE ON *.* TO 'replication'@'%';
mysql> show master status;
+--------------+----------+--------------+------------------+-------------------+
| File         | Position | Binlog_Do_DB | Binlog_Ignore_DB | Executed_Gtid_Set |
+--------------+----------+--------------+------------------+-------------------+
| mybin.000001 |     1388 |              |                  |                   |
+--------------+----------+--------------+------------------+-------------------+
1 row in set (0.00 sec)


CHANGE MASTER TO MASTER_HOST='10.128.0.27', MASTER_USER='replication', MASTER_LOG_FILE='mybin.000001', MASTER_LOG_POS=1388;

START SLAVE;
SHOW SLAVE STATUS\G;


```

## Дополнительные задания (со звёздочкой*)
Эти задания дополнительные, то есть не обязательные к выполнению, и никак не повлияют на получение вами зачёта по этому домашнему заданию. Вы можете их выполнить, если хотите глубже шире разобраться в материале.

---

### Задание 3* 

Выполните конфигурацию master-master репликации. Произведите проверку.

*Приложите скриншоты конфигурации, выполнения работы: состояния и режимы работы серверов.*
