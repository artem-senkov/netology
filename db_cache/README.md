# Домашнее задание к занятию «Кеширование Redis/memcached» Артем Сеньков

---

### Задание 1. Кеширование 

Приведите примеры проблем, которые может решить кеширование. 

*Приведите ответ в свободной форме.*

Медленная работа с данными - кэш позволяет ускорить работу с наиболее востребованными данными.

Повышенное потребление ресурсов - можно снизить обращения к медленным ресурсам закэшировав данные

Низская скорость ответа на запросы - с помощью кэширования можно увеличить скорость ответа на запрос

Износ железа - кэш находящийся в памяти позволяет реже обращаться к накопителям и снизить износ


---

### Задание 2. Memcached

Установите и запустите memcached.

*Приведите скриншот systemctl status memcached, где будет видно, что memcached запущен.*
![img1](https://github.com/artem-senkov/netology/blob/main/db_cache/img/memcachedstatus.png)
---

### Задание 3. Удаление по TTL в Memcached

https://shouts.dev/articles/test-memcached-using-telnet-commands

```
# structure
set key_name meta_data expiry_time length_in_bytes

# example
set Test1 0 5 5 # press enter
Hello # press enter

STORED # you'll see this message after storing
```

Запишите в memcached несколько ключей с любыми именами и значениями, для которых выставлен TTL 5. 

set Test1 0 5 5
Hello

set Test2 1 5 7
HELLO!!

---
![img1](https://github.com/artem-senkov/netology/blob/main/db_cache/img/ttl5.png)

### Задание 4. Запись данных в Redis

Запишите в Redis несколько ключей с любыми именами и значениями. 
https://habr.com/ru/articles/204354/

```
set test:1:string "Sample string 1"
rpush cat-breeds persian ragdoll bengal
```
*Через redis-cli достаньте все записанные ключи и значения из базы, приведите скриншот этой операции.*
```
get test:1:string
lrange cat-breeds 0 -1
```
![img1](https://github.com/artem-senkov/netology/blob/main/db_cache/img/add2redis.png)
## Дополнительные задания (со звёздочкой*)
Эти задания дополнительные, то есть не обязательные к выполнению, и никак не повлияют на получение вами зачёта по этому домашнему заданию. Вы можете их выполнить, если хотите глубже разобраться в материале.

### Задание 5*. Работа с числами 

Запишите в Redis ключ key5 со значением типа "int" равным числу 5. Увеличьте его на 5, чтобы в итоге в значении лежало число 10.  
```
set test:1:int 5
incrby test:1:int 5
```

*Приведите скриншот, где будут проделаны все операции и будет видно, что значение key5 стало равно 10.*
![img1](https://github.com/artem-senkov/netology/blob/main/db_cache/img/mathsinredis.png)
