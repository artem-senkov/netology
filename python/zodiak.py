# ; Разработать приложение для определения знака зодиака по дате рождения.
# ; Пример:

# ; Введите месяц: март
# ; Введите число: 6

# ; Вывод:
# ; Рыбы

#подключаем regexp модуль
import re

input_date = input("Введите дату рождения DD.MM.YYYY ")

#Проверяем ввод на соответствие формату даты

birth_date = re.match(r"^(0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[012])\.(19|20)\d\d$", input_date)

if birth_date:
    birth_date=birth_date.group()
    print(birth_date)

    #подключаем datetime модуль
    from datetime import *

    # переводим строку в дату
    date_object = datetime.strptime(birth_date, '%d.%m.%Y').date()

    # присваеваем части даты переменным
    month_number = date_object.month
    day_number = date_object.day
    year_number = date_object.year

    #Меняем год на 1980 чтобы сравнивать даты с таблицей
    newdate = (str(day_number) +"."+str(month_number)+".1980")

    # Козерог
    # 22 декабря – 20 января
    if datetime.strptime("01.01.1980", '%d.%m.%Y').date() <= datetime.strptime(newdate, '%d.%m.%Y').date() <= datetime.strptime("20.01.1980", '%d.%m.%Y').date():
        print ("Козерог")

    # Водолей
    # 21 января – 18 февраля
    elif datetime.strptime("21.01.1980", '%d.%m.%Y').date() <= datetime.strptime(newdate, '%d.%m.%Y').date() <= datetime.strptime("18.02.1980", '%d.%m.%Y').date():
        print ("Водолей")

    # Рыбы
    # 19 февраля – 20 марта
    elif datetime.strptime("19.02.1980", '%d.%m.%Y').date() <= datetime.strptime(newdate, '%d.%m.%Y').date() <= datetime.strptime("20.03.1980", '%d.%m.%Y').date():
        print ("Рыбы")

    # Овен
    # 21 марта – 20 апреля
    elif datetime.strptime("21.03.1980", '%d.%m.%Y').date() <= datetime.strptime(newdate, '%d.%m.%Y').date() <= datetime.strptime("20.04.1980", '%d.%m.%Y').date():
        print ("Овен")

    # Телец
    # 21 апреля – 21 мая
    elif datetime.strptime("21.04.1980", '%d.%m.%Y').date() <= datetime.strptime(newdate, '%d.%m.%Y').date() <= datetime.strptime("21.05.1980", '%d.%m.%Y').date():
        print ("Телец")

    # Близнецы
    # 22 мая – 21 июня
    elif datetime.strptime("22.05.1980", '%d.%m.%Y').date() <= datetime.strptime(newdate, '%d.%m.%Y').date() <= datetime.strptime("21.06.1980", '%d.%m.%Y').date():
        print ("Близнецы")

    # Рак
    # 22 июня – 22 июля
    elif datetime.strptime("20.06.1980", '%d.%m.%Y').date() <= datetime.strptime(newdate, '%d.%m.%Y').date() <= datetime.strptime("22.07.1980", '%d.%m.%Y').date():
        print ("Рак")

    # Лев
    # 23 июля – 23 августа
    elif datetime.strptime("23.07.1980", '%d.%m.%Y').date() <= datetime.strptime(newdate, '%d.%m.%Y').date() <= datetime.strptime("23.08.1980", '%d.%m.%Y').date():
        print ("Лев")

    # Дева
    # 24 августа – 22 сентября
    elif datetime.strptime("24.08.1980", '%d.%m.%Y').date() <= datetime.strptime(newdate, '%d.%m.%Y').date() <= datetime.strptime("22.09.1980", '%d.%m.%Y').date():
        print ("Дева")

    # Весы
    # 23 сентября – 23 октября
    elif datetime.strptime("23.09.1980", '%d.%m.%Y').date() <= datetime.strptime(newdate, '%d.%m.%Y').date() <= datetime.strptime("23.10.1980", '%d.%m.%Y').date():
        print ("Весы")

    # Скорпион
    # 24 октября – 22 ноября
    elif datetime.strptime("24.10.1980", '%d.%m.%Y').date() <= datetime.strptime(newdate, '%d.%m.%Y').date() <= datetime.strptime("22.11.1980", '%d.%m.%Y').date():
        print ("Скорпион")

    # Стрелец
    # 23 ноября – 21 декабря
    elif datetime.strptime("23.11.1980", '%d.%m.%Y').date() <= datetime.strptime(newdate, '%d.%m.%Y').date() <= datetime.strptime("21.12.1980", '%d.%m.%Y').date():
        print ("Стрелец")

    # Козерог
    # 22 декабря – 20 января
    elif datetime.strptime("22.12.1980", '%d.%m.%Y').date() <= datetime.strptime(newdate, '%d.%m.%Y').date() <= datetime.strptime("31.12.1980", '%d.%m.%Y').date():
        print ("Козерог")

else:
    print("Ошибка формата даты")
