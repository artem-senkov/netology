# Домашнее задание к занятию «SQL. Часть 2» Artem Senkov

---

Задание можно выполнить как в любом IDE, так и в командной строке.

### Задание 1

Одним запросом получите информацию о магазине, в котором обслуживается более 300 покупателей, и выведите в результат следующую информацию: 
- фамилия и имя сотрудника из этого магазина;
- город нахождения магазина;
- количество пользователей, закреплённых в этом магазине.

```SQL
SELECT st.store_id, CONCAT(stf.last_name, ' ', stf.first_name) AS manager, cy.city, COUNT(customer_id) as Nom_of_customers
FROM customer c
JOIN store st ON c.store_id = st.store_id
JOIN address a ON a.address_id = st.address_id
JOIN city cy ON cy.city_id = a.city_id
JOIN staff stf ON stf.staff_id  = st.manager_staff_id
GROUP BY st.store_id
HAVING COUNT(c.customer_id) > 300;
```

```
1	Hillyer Mike	Lethbridge	326
```

### Задание 2

Получите количество фильмов, продолжительность которых больше средней продолжительности всех фильмов.
```SQL
SELECT COUNT(film_id)
FROM film
WHERE(length) > (SELECT SUM(length)/COUNT(film_id) from film);
```

```
489
```
### Задание 3

Получите информацию, за какой месяц была получена наибольшая сумма платежей, и добавьте информацию по количеству аренд за этот месяц.
```SQL
-- Находим месяц с макс доходом
SELECT MONTH(payment_date) bestmonth, COUNT(payment_id) nom_of_rent, SUM(amount) as INCOME
FROM payment
GROUP BY MONTH(payment_date)
HAVING SUM(amount) = (SELECT MAX(income1) from(SELECT MONTH(payment_date) month1, SUM(amount) income1 FROM payment GROUP BY MONTH(payment_date)) AVM)
```

```
7	6709	28368.91
```

## Дополнительные задания (со звёздочкой*)
Эти задания дополнительные, то есть не обязательные к выполнению, и никак не повлияют на получение вами зачёта по этому домашнему заданию. Вы можете их выполнить, если хотите глубже шире разобраться в материале.

### Задание 4*

Посчитайте количество продаж, выполненных каждым продавцом. Добавьте вычисляемую колонку «Премия». Если количество продаж превышает 8000, то значение в колонке будет «Да», иначе должно быть значение «Нет».

```SQL
-- Вычисляем у кого из продовцов сколько продаж
SELECT p.staff_id, stf.last_name, stf.first_name, count(p.payment_id) nom_of_payments,
	CASE
		WHEN count(p.payment_id) > 8000 THEN 'Да'
		ELSE 'Нет'
	END AS Премия
FROM payment p
JOIN staff stf ON stf.staff_id  = p.staff_id
GROUP BY staff_id
```
```
1	Hillyer	Mike	8054	Да
2	Stephens	Jon	7990	Нет
```

### Задание 5*

Найдите фильмы, которые ни разу не брали в аренду.

```SQL
  -- найдем все фильмы
SELECT f.film_id, f.title   from film f

-- найдем все фильмы присутствующие в таблице rental 
SELECT i.film_id, r.inventory_id, f.title   from rental r 
JOIN inventory i ON i.inventory_id = r.inventory_id
JOIN film f ON f.film_id = i.film_id

-- Вычтем результаты из вех фильмов результат выборки

SELECT f.film_id, f.title  from film f
WHERE f.film_id NOT IN (SELECT i.film_id r_f_id from rental r 
JOIN inventory i ON i.inventory_id = r.inventory_id
JOIN film f ON f.film_id = i.film_id);
```
```
14	ALICE FANTASIA
33	APOLLO TEEN
36	ARGONAUTS TOWN
38	ARK RIDGEMONT
41	ARSENIC INDEPENDENCE
87	BOONDOCK BALLROOM
108	BUTCH PANTHER
128	CATCH AMISTAD
144	CHINATOWN GLADIATOR
148	CHOCOLATE DUCK
171	COMMANDMENTS EXPRESS
192	CROSSING DIVORCE
195	CROWDS TELEMARK
198	CRYSTAL BREAKING
217	DAZED PUNK
221	DELIVERANCE MULHOLLAND
318	FIREHOUSE VIETNAM
325	FLOATS GARDEN
332	FRANKENSTEIN STRANGER
359	GLADIATOR WESTWARD
386	GUMP DATE
404	HATE HANDICAP
419	HOCUS FRIDA
495	KENTUCKIAN GIANT
497	KILL BROTHERHOOD
607	MUPPET MILE
642	ORDER BETRAYED
669	PEARL DESTINY
671	PERDITION FARGO
701	PSYCHO SHRUNK
712	RAIDERS ANTITRUST
713	RAINBOW SHOCK
742	ROOF CHAMPION
801	SISTER FREDDY
802	SKY MIRACLE
860	SUICIDES SILENCE
874	TADPOLE PARK
909	TREASURE COMMAND
943	VILLAIN DESPERATE
950	VOLUME HOUSE
954	WAKE JAWS
955	WALLS ARTIST
```

