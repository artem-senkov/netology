# Домашнее задание к занятию «Репликация и масштабирование. Часть 1» Artem Senkov

---

### Задание 1

На лекции рассматривались режимы репликации master-slave, master-master, опишите их различия.

*Ответить в свободной форме.*

В репликации master-slave второй сервер читает все изменения с master, применяет на себе и отдает их в режиме чтения пользователю. Является полной копией MASTERA.

MASTER - MASTER оба сервера могут получать изменения данных от пользователя и также получать изменения друг от друга. Оба работают в режиме READ-WRITE и с пользователем и друг с другом.


---

### Задание 2

Выполните конфигурацию master-slave репликации, примером можно пользоваться из лекции.

*Приложите скриншоты конфигурации, выполнения работы: состояния и режимы работы серверов.*

Установка MYSQL8
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
/etc/my.cnF модифицирую конфиг на обоих серверах, различие только в server-id=1 и server-id=2
```
bind-address=0.0.0.0
server-id=1
log_bin=/var/log/mysql/mybin.log
datadir=/var/lib/mysql
socket=/var/lib/mysql/mysql.sock
log-error=/var/log/mysqld.log
pid-file=/var/run/mysqld/mysqld.pid
```
Узнаем временный пароль root на серверах
```
sudo cat /var/log/mysqld.log
A temporary password is generated for root@localhost: FX>j3Xa%luw/
A temporary password is generated for root@localhost: Az*2K7tiGPKA
```
запускаем сервис подключаемся по root и меняем пароль, создаем пользователя для репликации даем ему права
```
sudo systemctl start mysqld
mysql -u root -p
ALTER USER 'root'@'localhost' IDENTIFIED BY 'Passw0rd';
FLUSH PRIVILEGES;
CREATE USER 'replication'@'%' IDENTIFIED WITH mysql_native_password BY 'Reepl11Pass!';
GRANT REPLICATION SLAVE ON *.* TO 'replication'@'%';
```
Настраиваем репликацию - на первом - мастере уточняем данные лога репликации и смещения
```
mysql> show master status;
+--------------+----------+--------------+------------------+-------------------+
| File         | Position | Binlog_Do_DB | Binlog_Ignore_DB | Executed_Gtid_Set |
+--------------+----------+--------------+------------------+-------------------+
| mybin.000001 |     1388 |              |                  |                   |
+--------------+----------+--------------+------------------+-------------------+
1 row in set (0.00 sec)
~~~
На втором подключаемся по IP к мастер и запускаем репликацию
~~~

CHANGE MASTER TO MASTER_HOST='10.128.0.27', MASTER_USER='replication', MASTER_PASSWORD='Reepl11Pass!', MASTER_LOG_FILE='mybin.000001', MASTER_LOG_POS=1388;

START SLAVE;
SHOW SLAVE STATUS\G;
```


```
mysql> SHOW SLAVE STATUS\G;
*************************** 1. row ***************************
               Slave_IO_State: Waiting for source to send event
                  Master_Host: 10.128.0.27
                  Master_User: replication
                  Master_Port: 3306
                Connect_Retry: 60
              Master_Log_File: mybin.000001
          Read_Master_Log_Pos: 1615
               Relay_Log_File: mysql2-relay-bin.000002
                Relay_Log_Pos: 322
        Relay_Master_Log_File: mybin.000001
             Slave_IO_Running: Yes
            Slave_SQL_Running: Yes
              Replicate_Do_DB:
          Replicate_Ignore_DB:
           Replicate_Do_Table:
       Replicate_Ignore_Table:
      Replicate_Wild_Do_Table:
  Replicate_Wild_Ignore_Table:
                   Last_Errno: 0
                   Last_Error:
                 Skip_Counter: 0
          Exec_Master_Log_Pos: 1615
              Relay_Log_Space: 533
              Until_Condition: None
               Until_Log_File:
                Until_Log_Pos: 0
           Master_SSL_Allowed: No
           Master_SSL_CA_File:
           Master_SSL_CA_Path:
              Master_SSL_Cert:
            Master_SSL_Cipher:
               Master_SSL_Key:
        Seconds_Behind_Master: 0
Master_SSL_Verify_Server_Cert: No
                Last_IO_Errno: 0
                Last_IO_Error:
               Last_SQL_Errno: 0
               Last_SQL_Error:
  Replicate_Ignore_Server_Ids:
             Master_Server_Id: 1
                  Master_UUID: d7addf74-2fd1-11ee-b4f2-d00d1da94148
             Master_Info_File: mysql.slave_master_info
                    SQL_Delay: 0
          SQL_Remaining_Delay: NULL
      Slave_SQL_Running_State: Replica has read all relay log; waiting for more updates
           Master_Retry_Count: 86400
                  Master_Bind:
      Last_IO_Error_Timestamp:
     Last_SQL_Error_Timestamp:
               Master_SSL_Crl:
           Master_SSL_Crlpath:
           Retrieved_Gtid_Set:
            Executed_Gtid_Set:
                Auto_Position: 0
         Replicate_Rewrite_DB:
                 Channel_Name:
           Master_TLS_Version:
       Master_public_key_path:
        Get_master_public_key: 0
            Network_Namespace:
1 row in set, 1 warning (0.00 sec)
```
Проверяем создав на мастере базу
```
mysql> create database reptest1;
Query OK, 1 row affected (0.02 sec)
На SLAVE
mysql> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
| reptest1           |
| sys                |
+--------------------+
5 rows in set (0.00 sec)
```

## Дополнительные задания (со звёздочкой*)
Эти задания дополнительные, то есть не обязательные к выполнению, и никак не повлияют на получение вами зачёта по этому домашнему заданию. Вы можете их выполнить, если хотите глубже шире разобраться в материале.

---

### Задание 3* 

Выполните конфигурацию master-master репликации. Произведите проверку.

*Приложите скриншоты конфигурации, выполнения работы: состояния и режимы работы серверов.*

На серверу MYSQL2 который пока SLAVE 

~~~
mysql> show master status;
+--------------+----------+--------------+------------------+-------------------+
| File         | Position | Binlog_Do_DB | Binlog_Ignore_DB | Executed_Gtid_Set |
+--------------+----------+--------------+------------------+-------------------+
| mybin.000001 |     1591 |              |                  |                   |
+--------------+----------+--------------+------------------+-------------------+
1 row in set (0.00 sec)
~~~

На первом MYSQL1 указываем мастером MYSQL2
~~~
CHANGE MASTER TO MASTER_HOST='10.128.0.8', MASTER_USER='replication', MASTER_PASSWORD='Reepl11Pass!', MASTER_LOG_FILE='mybin.000001', MASTER_LOG_POS=1591;
START SLAVE;
SHOW SLAVE STATUS\G;
~~~


~~~
mysql> SHOW SLAVE STATUS\G;
*************************** 1. row ***************************
               Slave_IO_State: Waiting for source to send event
                  Master_Host: 10.128.0.8
                  Master_User: replication
                  Master_Port: 3306
                Connect_Retry: 60
              Master_Log_File: mybin.000001
          Read_Master_Log_Pos: 1591
               Relay_Log_File: mysql1-relay-bin.000002
                Relay_Log_Pos: 322
        Relay_Master_Log_File: mybin.000001
             Slave_IO_Running: Yes
            Slave_SQL_Running: Yes
              Replicate_Do_DB:
          Replicate_Ignore_DB:
           Replicate_Do_Table:
       Replicate_Ignore_Table:
      Replicate_Wild_Do_Table:
  Replicate_Wild_Ignore_Table:
                   Last_Errno: 0
                   Last_Error:
                 Skip_Counter: 0
          Exec_Master_Log_Pos: 1591
              Relay_Log_Space: 533
              Until_Condition: None
               Until_Log_File:
                Until_Log_Pos: 0
           Master_SSL_Allowed: No
           Master_SSL_CA_File:
           Master_SSL_CA_Path:
              Master_SSL_Cert:
            Master_SSL_Cipher:
               Master_SSL_Key:
        Seconds_Behind_Master: 0
Master_SSL_Verify_Server_Cert: No
                Last_IO_Errno: 0
                Last_IO_Error:
               Last_SQL_Errno: 0
               Last_SQL_Error:
  Replicate_Ignore_Server_Ids:
             Master_Server_Id: 2
                  Master_UUID: ddaaa591-2fd1-11ee-b666-d00d17ae2959
             Master_Info_File: mysql.slave_master_info
                    SQL_Delay: 0
          SQL_Remaining_Delay: NULL
      Slave_SQL_Running_State: Replica has read all relay log; waiting for more updates
           Master_Retry_Count: 86400
                  Master_Bind:
      Last_IO_Error_Timestamp:
     Last_SQL_Error_Timestamp:
               Master_SSL_Crl:
           Master_SSL_Crlpath:
           Retrieved_Gtid_Set:
            Executed_Gtid_Set:
                Auto_Position: 0
         Replicate_Rewrite_DB:
                 Channel_Name:
           Master_TLS_Version:
       Master_public_key_path:
        Get_master_public_key: 0
            Network_Namespace:
1 row in set, 1 warning (0.00 sec)
~~~

Создадим базу на MYSQL2

CREATE DATABASE TEST2;

```
На MYSQL1
mysql> SHOW DATABASES;
+--------------------+
| Database           |
+--------------------+
| TEST2              |
| information_schema |
| mysql              |
| performance_schema |
| reptest1           |
| sys                |
+--------------------+
6 rows in set (0.01 sec)
```
