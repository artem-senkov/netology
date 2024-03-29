# Домашнее задание к занятию «SQL. Часть 1» Artem Senkov

Задание можно выполнить как в любом IDE, так и в командной строке.

### Задание 1

Получите уникальные названия районов из таблицы с адресами, которые начинаются на “K” и заканчиваются на “a” и не содержат пробелов.
```SQL
SELECT DISTINCT district FROM address
WHERE district  NOT LIKE '% %' AND district LIKE 'K%a'
ORDER BY district;
```
```
Kaduna
Kalmykia
Kanagawa
Karnataka
Kerala
Kitaa
Kütahya
```

### Задание 2

Получите из таблицы платежей за прокат фильмов информацию по платежам, которые выполнялись в промежуток с 15 июня 2005 года по 18 июня 2005 года **включительно** и стоимость которых превышает 10.00.

```SQL
SELECT CAST(payment_date AS DATE) , payment_id, amount
FROM payment
WHERE amount > 10 AND CAST(payment_date AS DATE) <= '2005-06-18' AND CAST(payment_date AS DATE) >= '2005-06-15'
ORDER BY payment_date;
```
```
2005-06-15	908	10.99
2005-06-15	14620	10.99
2005-06-16	13892	10.99
2005-06-17	15313	10.99
2005-06-17	7017	10.99
2005-06-17	8272	11.99
2005-06-18	12888	10.99
```

### Задание 3

Получите последние пять аренд фильмов.

```SQL
SELECT *
FROM rental r 
ORDER BY rental_date DESC
LIMIT 5;
```
```
11739	2006-02-14 15:16:03	4568	373		2
14616	2006-02-14 15:16:03	4537	532		1
11676	2006-02-14 15:16:03	4496	216		2
15966	2006-02-14 15:16:03	4472	374		1
13486	2006-02-14 15:16:03	4460	274		1
```

### Задание 4

Одним запросом получите активных покупателей, имена которых Kelly или Willie. 

Сформируйте вывод в результат таким образом:
- все буквы в фамилии и имени из верхнего регистра переведите в нижний регистр,
- замените буквы 'll' в именах на 'pp'.

```SQL
SELECT customer_id , REPLACE(LOWER(first_name), 'll', 'pp'), LOWER(last_name)
FROM customer
WHERE first_name LIKE 'Kelly' OR first_name LIKE 'Willie'
ORDER BY first_name , last_name;
```
```
546	keppy	knott
67	keppy	torres
219	wippie	howell
359	wippie	markham
```

## Дополнительные задания (со звёздочкой*)
Эти задания дополнительные, то есть не обязательные к выполнению, и никак не повлияют на получение вами зачёта по этому домашнему заданию. Вы можете их выполнить, если хотите глубже шире разобраться в материале.

### Задание 5*

Выведите Email каждого покупателя, разделив значение Email на две отдельных колонки: в первой колонке должно быть значение, указанное до @, во второй — значение, указанное после @.

```SQL
select email,
LEFT (email, POSITION('@' IN email)-1) as ename,
RIGHT (email, CHAR_LENGTH(email)-POSITION('@' IN email)) as edomain
from customer;
```
```
MARY.SMITH@sakilacustomer.org	MARY.SMITH	sakilacustomer.org
PATRICIA.JOHNSON@sakilacustomer.org	PATRICIA.JOHNSON	sakilacustomer.org
LINDA.WILLIAMS@sakilacustomer.org	LINDA.WILLIAMS	sakilacustomer.org
BARBARA.JONES@sakilacustomer.org	BARBARA.JONES	sakilacustomer.org
ELIZABETH.BROWN@sakilacustomer.org	ELIZABETH.BROWN	sakilacustomer.org
JENNIFER.DAVIS@sakilacustomer.org	JENNIFER.DAVIS	sakilacustomer.org
MARIA.MILLER@sakilacustomer.org	MARIA.MILLER	sakilacustomer.org
SUSAN.WILSON@sakilacustomer.org	SUSAN.WILSON	sakilacustomer.org
MARGARET.MOORE@sakilacustomer.org	MARGARET.MOORE	sakilacustomer.org
DOROTHY.TAYLOR@sakilacustomer.org	DOROTHY.TAYLOR	sakilacustomer.org
LISA.ANDERSON@sakilacustomer.org	LISA.ANDERSON	sakilacustomer.org
NANCY.THOMAS@sakilacustomer.org	NANCY.THOMAS	sakilacustomer.org
```

### Задание 6*

Доработайте запрос из предыдущего задания, скорректируйте значения в новых колонках: первая буква должна быть заглавной, остальные — строчными.
```SQL
select email,
INSERT(LOWER(LEFT (email, POSITION('@' IN email)-1)), 1, 1, LEFT(UPPER (LEFT (email, POSITION('@' IN email)-1)),1)) AS 1UPmail,
INSERT(LOWER(RIGHT (email, CHAR_LENGTH(email)-POSITION('@' IN email))), 1, 1, LEFT(UPPER (RIGHT (email, CHAR_LENGTH(email)-POSITION('@' IN email))),1)) AS 1UPdomain
from customer;
```
```
MARY.SMITH@sakilacustomer.org	Mary.smith	Sakilacustomer.org
PATRICIA.JOHNSON@sakilacustomer.org	Patricia.johnson	Sakilacustomer.org
LINDA.WILLIAMS@sakilacustomer.org	Linda.williams	Sakilacustomer.org
BARBARA.JONES@sakilacustomer.org	Barbara.jones	Sakilacustomer.org
ELIZABETH.BROWN@sakilacustomer.org	Elizabeth.brown	Sakilacustomer.org
JENNIFER.DAVIS@sakilacustomer.org	Jennifer.davis	Sakilacustomer.org
MARIA.MILLER@sakilacustomer.org	Maria.miller	Sakilacustomer.org
SUSAN.WILSON@sakilacustomer.org	Susan.wilson	Sakilacustomer.org
MARGARET.MOORE@sakilacustomer.org	Margaret.moore	Sakilacustomer.org
DOROTHY.TAYLOR@sakilacustomer.org	Dorothy.taylor	Sakilacustomer.org
LISA.ANDERSON@sakilacustomer.org	Lisa.anderson	Sakilacustomer.org
NANCY.THOMAS@sakilacustomer.org	Nancy.thomas	Sakilacustomer.org
```

