# Домашнее задание к занятию 10.5 «Балансировка нагрузки. HAProxy/Nginx» Artem Senkov
---

### Задание 1

Что такое балансировка нагрузки и зачем она нужна? 

Распределение нагрузки между несколькими серверами для повышения отказоустойчивости и доступности. Удобно применять при масштабировании.
---

### Задание 2

Чем отличаются алгоритмы балансировки Round Robin и Weighted Round Robin? В каких случаях каждый из них лучше применять? 

Round robin распределяет не анализируя загрузку - распределяет по очереди на каждый следующий сервер , подходит для сбалансированной нагрузки , когда все запросы примерно одинаковые. Wheighted RR назначает вес каждому каналу и учитывает мощность , распределяет часть пакетов соответствующую весу на более мощный канал или сервер, другую часть на следующие.
---

### Задание 3

Установите и запустите Haproxy.

*Приведите скриншот systemctl status haproxy, где будет видно, что Haproxy запущен.*
![img](https://github.com/artem-senkov/netology/blob/main/HAProxy/img/haproxy_status.png)
---

### Задание 4

Установите и запустите Nginx.

*Приведите скриншот systemctl status nginx, где будет видно, что Nginx запущен.*
![img](https://github.com/artem-senkov/netology/blob/main/HAProxy/img/nginx_status.png)
---

### Задание 5

Настройте Nginx на виртуальной машине таким образом, чтобы при запросе:

`curl http://localhost:8088/ping`

он возвращал в ответе строчку: 

"nginx is configured correctly".

*Приведите конфигурации настроенного Nginx сервиса и скриншот результата выполнения команды curl http://localhost:8088/ping.*
```
server {
listen 8088;
location /ping {
return 200 'nginx is configured correctly ';
}
}
```
![img](https://github.com/artem-senkov/netology/blob/main/HAProxy/img/curl.png)
---

## Задания со звёздочкой*

Эти задания дополнительные. Их выполнять не обязательно. На зачёт это не повлияет. Вы можете их выполнить, если хотите глубже разобраться в материале.

---

### Задание 6*

Настройте Haproxy таким образом, чтобы при ответе на запрос:

`curl http://localhost:8080/`

он проксировал его в Nginx на порту 8088, который был настроен в задании 5 и возвращал от него ответ: 

"nginx is configured correctly". 

*Приведите конфигурации настроенного Haproxy и скриншоты результата выполнения команды curl http://localhost:8080/.*
```
listen stats # описание конфига для показа статистики в интерфейсе HAProxy
 bind :::888
 mode http
 stats enable
 stats uri /local
 stats refresh 15s
 stats realm Haproxy\ Statistics

frontend example # правила роутинга входящих HTTP-запросов
 mode http
 bind :::8080
 default_backend web_servers
backend web_servers # конфигурация балансировки для пула серверов web_servers
 mode http
 balance roundrobin
 server s1 192.168.56.10:8088
```
![img](https://github.com/artem-senkov/netology/blob/main/HAProxy/img/haproxy2.png)
