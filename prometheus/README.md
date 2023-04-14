# Домашнее задание к занятию "`Система мониторинга Prometheus`" - `Senkov Artem`

### Задание 1
Установите Prometheus.

#### Процесс выполнения
1. Выполняя задание, сверяйтесь с процессом, отражённым в записи лекции
2. Создайте пользователя prometheus
3. Скачайте prometheus и в соответствии с лекцией разместите файлы в целевые директории
4. Создайте сервис как показано на уроке
5. Проверьте что prometheus запускается, останавливается, перезапускается и отображает статус с помощью systemctl

#### Требования к результату
- [ ] Прикрепите к файлу README.md скриншот systemctl status prometheus, где будет написано: prometheus.service — Prometheus Service Netology Lesson 9.4 — [Ваши ФИО]

```bash
echo "Создаем пользователя Prometheus"
sudo useradd --no-create-home --shell /bin/false prometheus
echo "Скачиваем с git последний релиз извлекаем архив и копируем файлы в необходимые директории"
mkdir prometheus 
cd prometheus
wget https://github.com/prometheus/prometheus/releases/download/v2.43.0%2Bstringlabels/prometheus-2.43.0+stringlabels.linux-amd64.tar.gz
tar xvfz prometheus-2.43.0+stringlabels.linux-amd64.tar.gz
cd prometheus-2.43.0+stringlabels.linux-amd64
mkdir /etc/prometheus
mkdir /var/lib/prometheus
cp ./prometheus promtool /usr/local/bin/
cp -R ./console_libraries /etc/prometheus
cp -R ./consoles /etc/prometheus
cp ./prometheus.yml /etc/prometheus
echo "Даем права на файлы пользователю Prometheus"
chown -R prometheus:prometheus /etc/prometheus /var/lib/prometheus
chown prometheus:prometheus /usr/local/bin/prometheus
chown prometheus:prometheus /usr/local/bin/promtool
```

```bash
echo "Создаем сервис Prometheus"
echo "
[Unit]
Description=Prometheus Service Netology Lesson 9.4 Artem Senkov
After=network.target
[Service]
User=prometheus
Group=prometheus
Type=simple
ExecStart=/usr/local/bin/prometheus \
--config.file /etc/prometheus/prometheus.yml \
--storage.tsdb.path /var/lib/prometheus/ \
--web.console.templates=/etc/prometheus/consoles \
--web.console.libraries=/etc/prometheus/console_libraries
ExecReload=/bin/kill -HUP $MAINPID Restart=on-failure
[Install]
WantedBy=multi-user.target
" >> /etc/systemd/system/prometheus.service

echo "Задаем права на файл"

chown -R prometheus:prometheus /var/lib/prometheus
echo "Включаем и запускаем сервис"
sudo systemctl enable prometheus
sudo systemctl start prometheus
sudo systemctl status prometheus
```
![screen 1](https://github.com/artem-senkov/netology/blob/main/prometheus/img/prom_result1.png)
---


### Задание 2
Установите Node Exporter.

#### Процесс выполнения
1. Выполняя ДЗ сверяйтесь с процессом отражённым в записи лекции.
3. Скачайте node exporter приведённый в презентации и в соответствии с лекцией разместите файлы в целевые директории
4. Создайте сервис для как показано на уроке
5. Проверьте что node exporter запускается, останавливается, перезапускается и отображает статус с помощью systemctl

#### Требования к результату
- [ ] Прикрепите к файлу README.md скриншот systemctl status node-exporter, где будет написано: node-exporter.service — Node Exporter Netology Lesson 9.4 — [Ваши ФИО]


```bash
echo "Создаем пользователя Prometheus"
sudo useradd --no-create-home --shell /bin/false prometheus
echo "Скачиваем архив и распаковываем"
wget https://github.com/prometheus/node_exporter/releases/download/v1.5.0/node_exporter-1.5.0.linux-amd64.tar.gz
tar xvfz node_exporter-*.*-amd64.tar.gz
cd node_exporter-*.*-amd64

echo "Создаем папку, копируем и даем права пользователю"
mkdir /etc/prometheus
mkdir /etc/prometheus/node-exporter
cp ./* /etc/prometheus/node-exporter
chown -R prometheus:prometheus /etc/prometheus/node-exporter/
echo "Создаём сервис для работы с Node Explorer"
echo "
[Unit]
Description=Node Exporter Lesson 9.4 Artem Senkov
After=network.target
[Service]
User=prometheus
Group=prometheus
Type=simple
ExecStart=/etc/prometheus/node-exporter/node_exporter
[Install]
WantedBy=multi-user.target 
" >> /etc/systemd/system/node-exporter.service

echo "атозапуск и старт сервиса"
systemctl enable node-exporter
systemctl start node-exporter
systemctl status node-exporter


```
![screen 1](https://github.com/artem-senkov/netology/blob/main/prometheus/img/prom_result2.png)
![screen 1](https://github.com/artem-senkov/netology/blob/main/prometheus/img/prom_result3.png)
---

### Задание 3
Подключите Node Exporter к серверу Prometheus.

#### Процесс выполнения
1. Выполняя ДЗ сверяйтесь с процессом отражённым в записи лекции.
2. Отредактируйте prometheus.yaml, добавив в массив таргетов установленный в задании 2 node exporter
3. Перезапустите prometheus
4. Проверьте что он запустился

```bash
nano /etc/prometheus/prometheus.yml
systemctl restart prometheus
```
---
Добавляем target /etc/prometheus/prometheus.yml
    static_configs:
      - targets: ["localhost:9090","192.168.7.245:9100"]
---


#### Требования к результату
- [ ] Прикрепите к файлу README.md скриншот конфигурации из интерфейса Prometheus вкладки Status > Configuration
- [ ] Прикрепите к файлу README.md скриншот из интерфейса Prometheus вкладки Status > Targets, чтобы было видно минимум два эндпоинта
![screen 1](https://github.com/artem-senkov/netology/blob/main/prometheus/img/prom_result4.png)
![screen 1](https://github.com/artem-senkov/netology/blob/main/prometheus/img/prom_result5.png)
---
## Дополнительные задания со звёздочкой*
Эти задания дополнительные. Их можно не выполнять. Это не повлияет на зачёт. Вы можете их выполнить, если хотите глубже разобраться в материале.

---

### Задание 4*
Установите Grafana.

```bash
echo "Скачиваем и устанавливаем DEB-пакет"
wget https://dl.grafana.com/oss/release/grafana_9.2.4_amd64.deb
dpkg -i grafana_9.2.4_amd64.deb
echo "автозапуск и запуск сервера Grafana"
systemctl enable grafana-server
systemctl start grafana-server
systemctl status grafana-server
echo "(Сервер доступен по адресуhttps://<наш сервер>:3000
Стандартный логин и пароль admin \ admin)"
```

#### Требования к результату
- [ ] Прикрепите к файлу README.md скриншот левого нижнего угла интерфейса, чтобы при наведении на иконку пользователя были видны ваши ФИО
![screen 1](https://github.com/artem-senkov/netology/blob/main/prometheus/img/prom_result6.png)
---

### Задание 5*
Интегрируйте Grafana и Prometheus.

#### Требования к результату
- [ ] Прикрепите к файлу README.md скриншот дашборда (ID:11074) с поступающими туда данными из Node Exporter

![screen 1](https://github.com/artem-senkov/netology/blob/main/prometheus/img/prom_result7.png)

## Критерии оценки
1. Выполнено минимум 3 обязательных задания
2. Прикреплены требуемые скриншоты
3. Задание оформлено в шаблоне с решением и опубликовано на GitHub
