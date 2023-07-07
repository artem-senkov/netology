---
# Домашнее задание к занятию «ELK»

## Дополнительные ресурсы

При выполнении задания используйте дополнительные ресурсы:
- [docker-compose elasticsearch + kibana](11-03/docker-compose.yaml);
- [поднимаем elk в docker](https://www.elastic.co/guide/en/elasticsearch/reference/7.17/docker.html);
- [поднимаем elk в docker с filebeat и docker-логами](https://www.sarulabs.com/post/5/2019-08-12/sending-docker-logs-to-elasticsearch-and-kibana-with-filebeat.html);
- [конфигурируем logstash](https://www.elastic.co/guide/en/logstash/7.17/configuration.html);
- [плагины filter для logstash](https://www.elastic.co/guide/en/logstash/current/filter-plugins.html);
- [конфигурируем filebeat](https://www.elastic.co/guide/en/beats/libbeat/5.3/config-file-format.html);
- [привязываем индексы из elastic в kibana](https://www.elastic.co/guide/en/kibana/7.17/index-patterns.html);
- [как просматривать логи в kibana](https://www.elastic.co/guide/en/kibana/current/discover.html);
- [решение ошибки increase vm.max_map_count elasticsearch](https://stackoverflow.com/questions/42889241/how-to-increase-vm-max-map-count).

### Задание 1. Elasticsearch 

Установите и запустите Elasticsearch, после чего поменяйте параметр cluster_name на случайный. 

*Приведите скриншот команды 'curl -X GET 'localhost:9200/_cluster/health?pretty', сделанной на сервере с установленным Elasticsearch. Где будет виден нестандартный cluster_name*.


Настройку в итоге делал по другому , по леуции не получилось
https://serveradmin.ru/ustanovka-i-nastroyka-elasticsearch-logstash-kibana-elk-stack/#Ubuntu_Debian
Для себя привожу конфиги
~~~
http.host: 0.0.0.0

~~~
nano  /etc/elasticsearch/elasticsearch.yml

and replace this setting with false 
# Enable security features
xpack.security.enabled: false
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
![alt text](https://github.com/thecodebuzz/FileSizePOC/blob/master/TheCodebuzz.png?raw=true)

## Дополнительные задания (со звёздочкой*)
Эти задания дополнительные, то есть не обязательные к выполнению, и никак не повлияют на получение вами зачёта по этому домашнему заданию. Вы можете их выполнить, если хотите глубже шире разобраться в материале.

### Задание 5*. Доставка данных 

Настройте поставку лога в Elasticsearch через Logstash и Filebeat любого другого сервиса , но не Nginx. 
Для этого лог должен писаться на файловую систему, Logstash должен корректно его распарсить и разложить на поля. 

*Приведите скриншот интерфейса Kibana, на котором будет виден этот лог и напишите лог какого приложения отправляется.*
