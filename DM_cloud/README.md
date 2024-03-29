# Домашнее задание к занятию «Базы данных в облаке» Artem Senkov

### Задание 1


#### Создание кластера
1. Перейдите на главную страницу сервиса Managed Service for PostgreSQL.
1. Создайте кластер PostgreSQL со следующими параметрами:
- класс хоста: s2.micro, диск network-ssd любого размера;
- хосты: нужно создать два хоста в двух разных зонах доступности и указать необходимость публичного доступа, то есть публичного IP адреса, для них;
- установите учётную запись для пользователя и базы.

Остальные параметры оставьте по умолчанию либо измените по своему усмотрению.

* Нажмите кнопку «Создать кластер» и дождитесь окончания процесса создания, статус кластера = RUNNING. Кластер создаётся от 5 до 10 минут.

#### Подключение к мастеру и реплике 

* Используйте инструкцию по подключению к кластеру, доступную на вкладке «Обзор»: cкачайте SSL-сертификат и подключитесь к кластеру с помощью утилиты psql, указав hostname всех узлов и атрибут ```target_session_attrs=read-write```.

* Проверьте, что подключение прошло к master-узлу.
```
select case when pg_is_in_recovery() then 'REPLICA' else 'MASTER' end;
```
* Посмотрите количество подключенных реплик:
```
select count(*) from pg_stat_replication;
```

##### Мой процесс выполнения:

[инструкция](https://cloud.yandex.ru/docs/managed-postgresql/operations/connect?from=int-console-help-center-or-nav)
windows powershell
```powershell
mkdir $HOME\.postgresql; curl.exe -o $HOME\.postgresql\root.crt https://storage.yandexcloud.net/cloud-certs/CA.pem
```

Сертификат будет сохранен в файле $HOME\.postgresql\root.crt.

Перед подключением установите PostgreSQL для Windows той же версии, которая используется в кластере. Выберите только установку Command Line Tools.

Установить переменные окружения WINDOWS
```
$Env:PGSSLMODE="verify-full"; $Env:PGTARGETSESSIONATTRS="read-write"; $env:PGSSLROOTCERT="$HOME\.postgresql\root.crt"
```

Подключение
```
& "C:\Program Files\PostgreSQL\<версия>\bin\psql.exe" `
  --host=c-<идентификатор кластера>.rw.mdb.yandexcloud.net `
  --port=6432 `
  --username<имя пользователя> `
  <имя БД>
```

Проверка
```
SELECT version();
select case when pg_is_in_recovery() then 'REPLICA' else 'MASTER' end;
select count(*) from pg_stat_replication;
```

![img1](https://github.com/artem-senkov/netology/blob/main/DM_cloud/img/dbclud1-1.png)

### Проверьте работоспособность репликации в кластере

* Создайте таблицу и вставьте одну-две строки.
```
CREATE TABLE test_table(text varchar);
```
```
insert into test_table values('Строка 1');
```

* Выйдите из psql командой ```\q```.

* Теперь подключитесь к узлу-реплике. Для этого из команды подключения удалите атрибут ```target_session_attrs```  и в параметре атрибут ```host``` передайте только имя хоста-реплики. Роли хостов можно посмотреть на соответствующей вкладке UI консоли.

* Проверьте, что подключение прошло к узлу-реплике.
```
select case when pg_is_in_recovery() then 'REPLICA' else 'MASTER' end;
```
* Проверьте состояние репликации
```
select status from pg_stat_wal_receiver;
```

* Для проверки, что механизм репликации данных работает между зонами доступности облака, выполните запрос к таблице, созданной на предыдущем шаге:
```
select * from test_table;
```

*В качестве результата вашей работы пришлите скриншоты:*

*1) Созданной базы данных;*
*2) Результата вывода команды на реплике ```select * from test_table;```.*

##### Мой процесс выполнения:
```
$Env:PGTARGETSESSIONATTRS="read-only"

PS C:\Program Files\PostgreSQL\15\bin> & "C:\Program Files\PostgreSQL\15\bin\psql.exe" `
>> --host=rc1a-t1e9k9x5hji0k6f3.mdb.yandexcloud.net `
>> --port=6432 `
>> --username=artem `
>> testdb1

select case when pg_is_in_recovery() then 'REPLICA' else 'MASTER' end;
select status from pg_stat_wal_receiver;
select * from test_table;
```
![img1](https://github.com/artem-senkov/netology/blob/main/DM_cloud/img/dbclud1-2.png)

### Задание 2*

Создайте кластер, как в задании 1 с помощью Terraform.


*В качестве результата вашей работы пришлите скришоты:*

*1) Скриншот созданной базы данных.*
*2) Код Terraform, создающий базу данных.*

---

Задания, помеченные звёздочкой, — дополнительные, то есть не обязательные к выполнению, и никак не повлияют на получение вами зачёта по этому домашнему заданию. Вы можете их выполнить, если хотите глубже шире разобраться в материале.
