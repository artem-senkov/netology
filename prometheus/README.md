# Домашнее задание к занятию "`DEVOPS`" - `Senkov Artem`



### Задание 1

`В качестве ответа пришлите скриншоты с настройками проекта и результатами выполнения сборки`
[Репозиторий с тестами для ДЗ](https://github.com/artem-senkov/sdvps-materials)
```
```

![screen 1](https://github.com/artem-senkov/8-03-hw/blob/main/img/config1.png)
![screen 2](https://github.com/artem-senkov/8-03-hw/blob/main/img/config2.png)
![screen 3](https://github.com/artem-senkov/8-03-hw/blob/main/img/result1.png)
![screen 4](https://github.com/artem-senkov/8-03-hw/blob/main/img/result2.png)
![screen 5](https://github.com/artem-senkov/8-03-hw/blob/main/img/repo1.png)
![screen 6](https://github.com/artem-senkov/8-03-hw/blob/main/img/repo2.png)


---

### Задание 2

`Создайте новый проект pipeline.
Перепишите сборку из задания 1 на declarative в виде кода.`

![screen 1](https://github.com/artem-senkov/8-03-hw/blob/main/img/pipeconfig.png)
![screen 2](https://github.com/artem-senkov/8-03-hw/blob/main/img/piperesult.png)
![screen 3](https://github.com/artem-senkov/8-03-hw/blob/main/img/pipeconsole.png)

---

### Задание 3

`Установите на машину Nexus.
Создайте raw-hosted репозиторий.
Измените pipeline так, чтобы вместо Docker-образа собирался бинарный go-файл. Команду можно скопировать из Dockerfile.
Загрузите файл в репозиторий с помощью jenkins.
В качестве ответа пришлите скриншоты с настройками проекта и результатами выполнения сборки.`
---
pipeline {
    agent any

    stages {
        stage('Git') {
            steps {
                git url:'https://github.com/artem-senkov/sdvps-materials.git', branch: 'main'
            }
        }
        stage('Test') {
            steps {
                sh '/usr/local/go/bin/go test .'
            }
        }
        stage('Build') {
            steps {
                sh 'ls'
                sh 'CGO_ENABLED=0 GOOS=linux /usr/local/go/bin/go build -a -installsuffix nocgo -o goapp.v.$BUILD_NUMBER'
                sh 'ls'
            }
        }
        stage('Push') {
            steps {
                sh 'curl -u "admin:passw" http://192.168.56.10:8081/repository/raw_repo1/ --upload-file goapp.v.$BUILD_NUMBER'
            }
        }
    }
}
---
![screen 1](https://github.com/artem-senkov/8-03-hw/blob/main/img/stageview.png)
![screen 2](https://github.com/artem-senkov/8-03-hw/blob/main/img/3consoleoutput.png)
---
Задание 4* Выполнил в Задании 3
Придумайте способ версионировать приложение, чтобы каждый следующий запуск сборки присваивал имени файла новую версию. Таким образом, в репозитории Nexus будет храниться история релизов.

Подсказка: используйте переменную BUILD_NUMBER.

В качестве ответа пришлите скриншоты с настройками проекта и результатами выполнения сборки.
---
![screen 3](https://github.com/artem-senkov/8-03-hw/blob/main/img/rawrepo.png)

