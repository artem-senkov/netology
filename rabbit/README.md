
# Домашнее задание к занятию  «Очереди RabbitMQ» Artem Senkov

---

### Задание 1. Установка RabbitMQ

Используя Vagrant или VirtualBox, создайте виртуальную машину и установите RabbitMQ.
Добавьте management plug-in и зайдите в веб-интерфейс.

*Итогом выполнения домашнего задания будет приложенный скриншот веб-интерфейса RabbitMQ.*
![img1](https://github.com/artem-senkov/netology/blob/main/rabbit/img/1-1.png)
![img1](https://github.com/artem-senkov/netology/blob/main/rabbit/img/1-2.png)

---

### Задание 2. Отправка и получение сообщений

Используя приложенные скрипты, проведите тестовую отправку и получение сообщения.
Для отправки сообщений необходимо запустить скрипт producer.py.

Для работы скриптов вам необходимо установить Python версии 3 и библиотеку Pika.
Также в скриптах нужно указать IP-адрес машины, на которой запущен RabbitMQ, заменив localhost на нужный IP.

для теста поставил phyton3 и pika 
https://serverspace.io/support/help/debian-install-python/
```
$ pip install pika
```
Код для отправки сообщений (добавил ваторизацию, без нее не подключалось на второй хост)
```
#!/usr/bin/env python
# coding=utf-8
import pika
credentials = pika.PlainCredentials('test', 'test')
connection = pika.BlockingConnection(pika.ConnectionParameters('machine2',5672,'/',credentials))
channel = connection.channel()
channel.queue_declare(queue='QueueAVS')
channel.basic_publish(exchange='', routing_key='QueueAVS', body='You got message 2')
connection.close()
```

Код для чтения очереди
```
#!/usr/bin/env python
# coding=utf-8
import pika
credentials = pika.PlainCredentials('test', 'test')
connection = pika.BlockingConnection(pika.ConnectionParameters('machine1',5672,'/',credentials))
channel = connection.channel()
channel.queue_declare(queue='QueueAVS')
def callback(ch, method, properties, body): print(" [x] Received %r" % body)
channel.basic_consume(queue='QueueAVS', on_message_callback=callback,auto_ack=False)
channel.start_consuming()
```

Зайдите в веб-интерфейс, найдите очередь под названием hello и сделайте скриншот.
После чего запустите второй скрипт consumer.py и сделайте скриншот результата выполнения скрипта

*В качестве решения домашнего задания приложите оба скриншота, сделанных на этапе выполнения.*

Для закрепления материала можете попробовать модифицировать скрипты, чтобы поменять название очереди и отправляемое сообщение.
![img1](https://github.com/artem-senkov/netology/blob/main/rabbit/img/2-1.png)
![img1](https://github.com/artem-senkov/netology/blob/main/rabbit/img/2-2.png)
![img1](https://github.com/artem-senkov/netology/blob/main/rabbit/img/2-3.png)

---

### Задание 3. Подготовка HA кластера

Используя Vagrant или VirtualBox, создайте вторую виртуальную машину и установите RabbitMQ.
Добавьте в файл hosts название и IP-адрес каждой машины, чтобы машины могли видеть друг друга по имени.

Vagrant для кластера из даух нод 
```
Vagrant.configure("2") do |config|

        # machine1
        config.vm.define "machine1" do |machine1|
                machine1.vm.hostname = "machine1"
                machine1.vm.box = "hashicorp/bionic64"
                machine1.vm.network "public_network", ip: "192.168.0.141"
                machine1.vm.provider "virtualbox" do |vb|
                        vb.customize ["modifyvm", :id, "--memory", "2048" ]
                        vb.customize ["modifyvm", :id, "--cpus", "1" ]
                        vb.customize ["modifyvm", :id, "--name", "machine1" ]
                end
                machine1.vm.provision "shell", inline: <<-SHELL
                sudo echo "192.168.0.141 machine1" | sudo tee -a /etc/hosts
                sudo echo "192.168.0.142 machine2" | sudo tee -a /etc/hosts
                sudo apt update
                sudo apt upgrade
        sudo apt install rabbitmq-server -y
        sudo systemctl start rabbitmq-server
        sudo systemctl enable rabbitmq-server
                sudo rabbitmq-plugins enable rabbitmq_management
        sudo systemctl restart rabbitmq-server
            sudo ufw allow ssh
        sudo ufw enable
        sudo ufw allow 5672,15672,4369,25672/tcp
        sudo cp /var/lib/rabbitmq/.erlang.cookie /vagrant/
                SHELL
        end

        # machine2
        config.vm.define "machine2" do |machine2|
                machine2.vm.hostname = "machine2"
                machine2.vm.box = "hashicorp/bionic64"
                machine2.vm.network "public_network", ip: "192.168.0.142"
                machine2.vm.provider "virtualbox" do |vb|
                        vb.customize ["modifyvm", :id, "--memory", "2048" ]
                        vb.customize ["modifyvm", :id, "--cpus", "1" ]
                        vb.customize ["modifyvm", :id, "--name", "machine2" ]
                end
                machine2.vm.provision "shell", inline: <<-SHELL
                sudo echo "192.168.0.141 machine1" | sudo tee -a /etc/hosts
                sudo echo "192.168.0.142 machine2" | sudo tee -a /etc/hosts
                sudo apt update
                sudo apt upgrade
                sudo apt install rabbitmq-server -y
                sudo systemctl start rabbitmq-server
                sudo systemctl enable rabbitmq-server
                sudo rabbitmq-plugins enable rabbitmq_management
                sudo systemctl restart rabbitmq-server
                sudo ufw allow ssh
                sudo ufw enable
                sudo ufw allow 5672,15672,4369,25672/tcp
                sudo cp /vagrant/.erlang.cookie /var/lib/rabbitmq/
                sudo rm -rf /var/log/rabbitmq/*
                sudo systemctl restart rabbitmq-server
        sudo rabbitmqctl stop_app
        sudo rabbitmqctl join_cluster rabbit@machine1
        sudo rabbitmqctl start_app
        sudo rabbitmqctl set_policy ha-all ".*" '{"ha-mode":"all"}'
                sudo rabbitmqctl add_user rabbit 123456
        sudo rabbitmqctl set_user_tags rabbit administrator
        sudo rabbitmqctl set_permissions -p / rabbit ".*" ".*" ".*"
                SHELL
        end
end
```

Пример содержимого hosts файла:
```shell script
$ cat /etc/hosts
192.168.0.10 rmq01
192.168.0.11 rmq02
```
После этого ваши машины могут пинговаться по имени.

Затем объедините две машины в кластер и создайте политику ha-all на все очереди.

sudo rabbitmqctl set_policy ha-all ".*" '{"ha-mode":"all"}'

*В качестве решения домашнего задания приложите скриншоты из веб-интерфейса с информацией о доступных нодах в кластере и включённой политикой.*

Также приложите вывод команды с двух нод:

```shell script
$ rabbitmqctl cluster_status
```

Для закрепления материала снова запустите скрипт producer.py и приложите скриншот выполнения команды на каждой из нод:

```shell script
$ rabbitmqadmin get queue='hello'
```
![img1](https://github.com/artem-senkov/netology/blob/main/rabbit/img/3-1.png)

После чего попробуйте отключить одну из нод, желательно ту, к которой подключались из скрипта, затем поправьте параметры подключения в скрипте consumer.py на вторую ноду и запустите его.

*Приложите скриншот результата работы второго скрипта.*
![img1](https://github.com/artem-senkov/netology/blob/main/rabbit/img/3-2.png)
![img1](https://github.com/artem-senkov/netology/blob/main/rabbit/img/3-3.png)

## Дополнительные задания (со звёздочкой*)
Эти задания дополнительные, то есть не обязательные к выполнению, и никак не повлияют на получение вами зачёта по этому домашнему заданию. Вы можете их выполнить, если хотите глубже шире разобраться в материале.

### * Задание 4. Ansible playbook

Напишите плейбук, который будет производить установку RabbitMQ на любое количество нод и объединять их в кластер.
При этом будет автоматически создавать политику ha-all.

*Готовый плейбук разместите в своём репозитории.*

