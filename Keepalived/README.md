# Домашнее задание к занятию 10.1 «Keepalived/vrrp» ARTEM SENKOV
---

### Задание 1

Разверните топологию из лекции и выполните установку и настройку сервиса Keepalived. 

```
vrrp_instance test {

state "name_mode"

interface "name_interface"

virtual_router_id "number id"

priority "number priority"

advert_int "number advert"

authentication {

auth_type "auth type"

auth_pass "password"

}

unicast_peer {

"ip address host"

}

virtual_ipaddress {

"ip address host" dev "interface" label "interface":vip

}

}

```

*В качестве решения предоставьте:*   
*- рабочую конфигурацию обеих нод, оформленную как блок кода в вашем md-файле;*   
*- скриншоты статуса сервисов, на которых видно, что одна нода перешла в MASTER, а вторая в BACKUP state.*   

https://keepalived.readthedocs.io/en/latest/case_study_failover.html

HOST1 CONFIG
```yaml
vrrp_instance VI_1 {
        state MASTER
        interface enp0s8
        virtual_router_id 51
        priority 255
        advert_int 1
        authentication {
              auth_type PASS
              auth_pass 12345
        }
        virtual_ipaddress {
              192.168.56.200/24 dev enp0s8 label enp0s8:vip
        }
}
```
![img1](https://github.com/artem-senkov/netology/blob/main/Keepalived/imgs/keep1.png)

HOST2 CONFIG
```yaml
vrrp_instance VI_1 {

        state BACKUP
        interface enp0s8
        virtual_router_id 51
        priority 254
        advert_int 1
        authentication {
              auth_type PASS
              auth_pass 12345
        }
        virtual_ipaddress {
              192.168.56.200/24 dev enp0s8 label enp0s8:vip
        }
}
```
![img2](https://github.com/artem-senkov/netology/blob/main/Keepalived/imgs/keep2.png)


## Дополнительные задания со звёздочкой*

Эти задания дополнительные. Их можно не выполнять. На зачёт это не повлияет. Вы можете их выполнить, если хотите глубже разобраться в материале.
 
### Задание 2*

Проведите тестирование работы ноды, когда один из интерфейсов выключен. Для этого:
- добавьте ещё одну виртуальную машину и включите её в сеть;
- на машине установите Wireshark и запустите процесс прослеживания интерфейса;
- запустите процесс ping на виртуальный хост;
- выключите интерфейс на одной ноде (мастер), остановите Wireshark;
- найдите пакеты ICMP, в которых будет отображён процесс изменения MAC-адреса одной ноды на другой. 

 *В качестве решения пришлите скриншот до и после выключения интерфейса из Wireshark.*
 ![img3](https://github.com/artem-senkov/netology/blob/main/Keepalived/imgs/keep3.png)
 ![img4](https://github.com/artem-senkov/netology/blob/main/Keepalived/imgs/keep4.png)
 
