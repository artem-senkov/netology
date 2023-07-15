# Домашнее задание к занятию «Работа с данными (DDL/DML)» Artem Senkov

Задание можно выполнить как в любом IDE, так и в командной строке.

### Задание 1
1.1. Поднимите чистый инстанс MySQL версии 8.0+. Можно использовать локальный сервер или контейнер Docker.

Для ускорения процесса поднял с помощью vagrant, скомбинировал из нескольких источников
```
Vagrant.configure("2") do |config|

        # dbmachine1
        config.vm.define "dbdbmachine1" do |dbmachine1|
                dbmachine1.vm.hostname = "dbmachine1"
                dbmachine1.vm.box = "ubuntu/xenial64"
                dbmachine1.vm.network "public_network", ip: "192.168.0.141"
				dbmachine1.vm.network "forwarded_port", guest: 3306, host: 3306
				dbmachine1.vm.network "forwarded_port", guest: 80, host: 8306
                dbmachine1.vm.provider "virtualbox" do |vb|
                        vb.customize ["modifyvm", :id, "--memory", "2048" ]
                        vb.customize ["modifyvm", :id, "--cpus", "2" ]
                        vb.customize ["modifyvm", :id, "--name", "dbdbmachine1" ]
                end
                dbmachine1.vm.provision "shell", inline: <<-SHELL
                DBHOST=localhost
                DBNAME=netologydb
                DBUSER=dbadmin
                DBPASSWD=password1234

                apt-get update
                apt-get install vim curl build-essential python-software-properties git

                debconf-set-selections <<< "mysql-server mysql-server/root_password password $DBPASSWD"
                debconf-set-selections <<< "mysql-server mysql-server/root_password_again password $DBPASSWD"
                debconf-set-selections <<< "phpmyadmin phpmyadmin/dbconfig-install boolean true"
                debconf-set-selections <<< "phpmyadmin phpmyadmin/app-password-confirm password $DBPASSWD"
                debconf-set-selections <<< "phpmyadmin phpmyadmin/mysql/admin-pass password $DBPASSWD"
                debconf-set-selections <<< "phpmyadmin phpmyadmin/mysql/app-pass password $DBPASSWD"
                debconf-set-selections <<< "phpmyadmin phpmyadmin/reconfigure-webserver multiselect none"

                # install mysql and admin interface

                apt-get -y install mysql-server phpmyadmin

                mysql -uroot -p$DBPASSWD -e "CREATE DATABASE $DBNAME"
                mysql -uroot -p$DBPASSWD -e "grant all privileges on $DBNAME.* to '$DBUSER'@'%' identified by '$DBPASSWD'"

                cd /vagrant

                # update mysql conf file to allow remote access to the db

                sudo sed -i "s/.*bind-address.*/bind-address = 0.0.0.0/" /etc/mysql/mysql.conf.d/mysqld.cnf

                sudo service mysql restart

                # setup phpmyadmin

                apt-get -y install php apache2 libapache2-mod-php php-curl php-gd php-mysql php-gettext a2enmod rewrite

                sed -i "s/AllowOverride None/AllowOverride All/g" /etc/apache2/apache2.conf

                rm -rf /var/www/html
                ln -fs /vagrant/public /var/www/html

                sed -i "s/error_reporting = .*/error_reporting = E_ALL/" /etc/php/7.0/apache2/php.ini
                sed -i "s/display_errors = .*/display_errors = On/" /etc/php/7.0/apache2/php.ini

                service apache2 restart 
                SHELL
        end

end
```

1.2. Создайте учётную запись sys_temp. 

https://www.mysqltutorial.org/mysql-create-user.aspx

CREATE USER 'sys_temp'@'%' IDENTIFIED BY '12345';
или одной командой создание пользователя и полные права - 
grant all privileges on *.* to 'username'@'%' identified by 'password'"

1.3. Выполните запрос на получение списка пользователей в базе данных. (скриншот)

![1](https://github.com/artem-senkov/netology/blob/main/work_with_db/img/1-3-1.png)

https://github.com/artem-senkov/netology/blob/main/work_with_db/img/1-3-1.png

1.4. Дайте все права для пользователя sys_temp. 

```sql
GRANT ALL PRIVILEGES ON *.* TO 'sys_temp'@'%';
```sql

1.5. Выполните запрос на получение списка прав для пользователя sys_temp. (скриншот)

```sql
select * from mysql.user WHERE  User = "sys_temp";
SHOW GRANTS FOR 'sys_temp'@'%';
```
Я создал нескольео userов
удаляю лишние
DROP USER sys_temp@localhost;
![1](https://github.com/artem-senkov/netology/blob/main/work_with_db/img/1-5-1.png)

1.6. Переподключитесь к базе данных от имени sys_temp.

Для смены типа аутентификации с sha2 используйте запрос: 
```sql
ALTER USER 'sys_test'@'localhost' IDENTIFIED WITH mysql_native_password BY 'password';
```
1.6. По ссылке https://downloads.mysql.com/docs/sakila-db.zip скачайте дамп базы данных.

wget https://downloads.mysql.com/docs/sakila-db.zip
apt install unzip
unzip sakila-db.zip
~/sakila-db/sakila-schema.sql
~/sakila-db/sakila-data.sql
cp /*.sql /tmp

1.7. Восстановите дамп в базу данных.
mysql -u sys_test -p

```sql
CREATE DATABASE sakila;
USE sakila;
SOURCE /tmp/sakila-schema.sql;
SOURCE /tmp/sakila-data.sql;
```

1.8. При работе в IDE сформируйте ER-диаграмму получившейся базы данных. При работе в командной строке используйте команду для получения всех таблиц базы данных. (скриншот)

*Результатом работы должны быть скриншоты обозначенных заданий, а также простыня со всеми запросами.*
![1](https://github.com/artem-senkov/netology/blob/main/work_with_db/img/1-8-1.png)

### Задание 2
Составьте таблицу, используя любой текстовый редактор или Excel, в которой должно быть два столбца: в первом должны быть названия таблиц восстановленной базы, во втором названия первичных ключей этих таблиц. Пример: (скриншот/текст)
```
Название таблицы | Название первичного ключа
customer         | customer_id
actor	| actor_id

```
Такой странной работой я заниматься не хочу ) не на того учился, сделяю проще как сисадмин

```sql
SELECT TABLE_NAME, COLUMN_NAME 
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA='sakila'
	AND COLUMN_KEY='PRI';
```

 Искал как сделать зтакой запрос 2 часа, но оно того стоило )

actor	actor_id
address	address_id
category	category_id
city	city_id
country	country_id
customer	customer_id
film	film_id
film_actor	actor_id
film_actor	film_id
film_category	film_id
film_category	category_id
film_text	film_id
inventory	inventory_id
language	language_id
payment	payment_id
rental	rental_id
staff	staff_id
store	store_id

![1](https://github.com/artem-senkov/netology/blob/main/work_with_db/img/2.png)

## Дополнительные задания (со звёздочкой*)
Эти задания дополнительные, то есть не обязательные к выполнению, и никак не повлияют на получение вами зачёта по этому домашнему заданию. Вы можете их выполнить, если хотите глубже шире разобраться в материале.

### Задание 3*
3.1. Уберите у пользователя sys_temp права на внесение, изменение и удаление данных из базы sakila.

```sql
SHOW GRANTS FOR 'sys_temp'@'%';
GRANT SELECT, INSERT, UPDATE, DELETE ON sakila.* TO 'sys_temp'@'%';
REVOKE INSERT, UPDATE, DELETE ON sakila.* FROM 'sys_temp'@'%';
```

3.2. Выполните запрос на получение списка прав для пользователя sys_temp. (скриншот)
SHOW GRANTS FOR 'sys_temp'@'%';

![1](https://github.com/artem-senkov/netology/blob/main/work_with_db/img/3-2-1.png)
![1](https://github.com/artem-senkov/netology/blob/main/work_with_db/img/3-2-2.png)



*Результатом работы должны быть скриншоты обозначенных заданий, а также простыня со всеми запросами.*

https://dev.mysql.com/doc/refman/8.0/en/grant.html#grant-database-privileges

