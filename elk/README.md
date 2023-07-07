---
# Домашнее задание к занятию «ELK» Artem Senkov



### Задание 1. Elasticsearch 

Установите и запустите Elasticsearch, после чего поменяйте параметр cluster_name на случайный. 

*Приведите скриншот команды 'curl -X GET 'localhost:9200/_cluster/health?pretty', сделанной на сервере с установленным Elasticsearch. Где будет виден нестандартный cluster_name*.


Настройку в итоге делал по другому , по леуции не получилось.
[https://serveradmin.ru/ustanovka-i-nastroyka-elasticsearch-logstash-kibana-elk-stack/](https://serveradmin.ru/ustanovka-i-nastroyka-elasticsearch-logstash-kibana-elk-stack/)
Для себя привожу конфиги

![alt text](https://github.com/artem-senkov/netology/blob/main/elk/img/elk1-1.png)
![alt text](https://github.com/artem-senkov/netology/blob/main/elk/img/elk1-2.png)

---

### Задание 2. Kibana

Установите и запустите Kibana.
```
apt install kibana
systemctl daemon-reload
systemctl enable kibana.service
systemctl start kibana.service
```
*Приведите скриншот интерфейса Kibana на странице http://<ip вашего сервера>:5601/app/dev_tools#/console, где будет выполнен запрос GET /_cluster/health?pretty*.
GET /_cluster/health

![alt text](https://github.com/artem-senkov/netology/blob/main/elk/img/elk2-1.png)
![alt text](https://github.com/artem-senkov/netology/blob/main/elk/img/elk2-2.png)

---

### Задание 3. Logstash

Установите и запустите Logstash и Nginx. С помощью Logstash отправьте access-лог Nginx в Elasticsearch. 

*Приведите скриншот интерфейса Kibana, на котором видны логи Nginx.*
```
apt install logstash
systemctl daemon-reload
systemctl enable logstash.service
systemctl start logstash.service
```
/etc/logstash/conf.d/input.conf
```
input {
  beats {
    port => 5044
  }
}

input {
  file {
    path => "/var/log/nginx/access.log"
    start_position => "beginning"
  }
}

input {
  file {
    path => "/var/log/nginx/error.log"
    start_position => "beginning"
  }
}

```

filter.conf
```
filter {
 if [type] == "nginx_access" {
    grok {
        match => { "message" => "%{IPORHOST:remote_ip} - %{DATA:user} \[%{HTTPDATE:access_time}\] \"%{WORD:http_met$
    }
  }
  date {
        match => [ "timestamp" , "dd/MMM/YYYY:HH:mm:ss Z" ]
  }
}

```

output.conf
```
output {
        elasticsearch {
            hosts    => "https://localhost:9200"
            data_stream => "true"
            user => "elastic"
            password => "yB*Xnymz90OMmAUKypTG"
            cacert => "/etc/logstash/certs/http_ca.crt"
        }
}

```
![alt text](https://github.com/artem-senkov/netology/blob/main/elk/img/elk3-1.png)

---

### Задание 4. Filebeat. 

Установите и запустите Filebeat. Переключите поставку логов Nginx с Logstash на Filebeat. 

 /etc/filebeat/filebeat.yml
```
filebeat.inputs:
  - type: log
    enabled: true
    paths:
      - /var/log/nginx/access.log
processors:
  - drop_fields:
      fields: ["beat", "input_type", "prospector", "input", "host", "agent","ecs"]
processors:
  - add_fields:
      fields:
        logger: filebeat
        importe: 'log imported with filebeat'

output.logstash:
  hosts: ["localhost:5044"]

```

*Приведите скриншот интерфейса Kibana, на котором видны логи Nginx, которые были отправлены через Filebeat.*
![alt text](https://github.com/artem-senkov/netology/blob/main/elk/img/elk-4-1.png)
![alt text](https://github.com/artem-senkov/netology/blob/main/elk/img/elk4-2.png)
![alt text](https://github.com/artem-senkov/netology/blob/main/elk/img/elk4-3.png)

Добавил поля в filebeat чтобы отличать записи которые попадают через этот источник от logstash так как в input.conf несколько источников прописал для эксперимента


## Дополнительные задания (со звёздочкой*)
Эти задания дополнительные, то есть не обязательные к выполнению, и никак не повлияют на получение вами зачёта по этому домашнему заданию. Вы можете их выполнить, если хотите глубже шире разобраться в материале.

### Задание 5*. Доставка данных 

Настройте поставку лога в Elasticsearch через Logstash и Filebeat любого другого сервиса , но не Nginx. 
Для этого лог должен писаться на файловую систему, Logstash должен корректно его распарсить и разложить на поля. 
```
filebeat.inputs:
  - type: log
    enabled: true
    paths:
      - /var/log/nginx/access.log
  - type: log
    enabled: true
    paths:
      - /var/log/logstash/logstash-plain.log
processors:
  - drop_fields:
      fields: ["beat", "input_type", "prospector", "input", "host", "agent","ecs"]
processors:
  - add_fields:
      fields:
        logger: filebeat
        importe: 'log imported with filebeat'

output.logstash:
  hosts: ["localhost:5044"]

```


*Приведите скриншот интерфейса Kibana, на котором будет виден этот лог и напишите лог какого приложения отправляется.*
/var/log/logstash/logstash-plain.log
![alt text](https://github.com/artem-senkov/netology/blob/main/elk/img/elk5-1.png)

