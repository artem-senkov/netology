По инструкции создаем service account и генерирум токен доступа
https://cloud.yandex.ru/docs/tutorials/infrastructure-management/terraform-quickstart#get-credentials

инициируем среду
yc init
генерируем ключ доступа
yc iam key create --service-account-id ajebhg1s6g3t7guncgl3 --folder-name webserver --output key.json

