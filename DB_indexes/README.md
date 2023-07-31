# Домашнее задание к занятию «Индексы» Artem Senkov

### Задание 1

Напишите запрос к учебной базе данных, который вернёт процентное отношение общего размера всех индексов к общему размеру всех таблиц.

```
SELECT SUM(data_length) all_data, SUM(index_length) all_index, SUM(index_length)/SUM(data_length) * 100 AS 'index percent'
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_SCHEMA = 'sakila'
```
```
1179648	671744	56.9444
```


### Задание 2

Выполните explain analyze следующего запроса:
```sql
select distinct concat(c.last_name, ' ', c.first_name), sum(p.amount) over (partition by c.customer_id, f.title)
from payment p, rental r, customer c, inventory i, film f
where date(p.payment_date) = '2005-07-30' and p.payment_date = r.rental_date and r.customer_id = c.customer_id and i.inventory_id = r.inventory_id
```
- перечислите узкие места;
- оптимизируйте запрос: внесите корректировки по использованию операторов, при необходимости добавьте индексы.

```
-- Изначальный запрос
EXPLAIN ANALYZE
select distinct concat(c.last_name, ' ', c.first_name), sum(p.amount) over (partition by c.customer_id, f.title)
from payment p, rental r, customer c, inventory i, film f
where date(p.payment_date) = '2005-07-30' and p.payment_date = r.rental_date and r.customer_id = c.customer_id and i.inventory_id = r.inventory_id

JOHNSON PATRICIA	30.95
WILLIAMS LINDA	5.98
JONES BARBARA	11.98
BROWN ELIZABETH	6.98
MOORE MARGARET	4.99
ANDERSON LISA	16.98
THOMAS NANCY	11.97
JACKSON KAREN	10.98
WHITE BETTY	4.99
HARRIS HELEN	4.99
16618s

-> Limit: 200 row(s)  (cost=0..0 rows=0) (actual time=20524..20524 rows=200 loops=1)
    -> Table scan on <temporary>  (cost=2.5..2.5 rows=0) (actual time=20524..20524 rows=200 loops=1)
        -> Temporary table with deduplication  (cost=0..0 rows=0) (actual time=20524..20524 rows=391 loops=1)
            -> Window aggregate with buffering: sum(payment.amount) OVER (PARTITION BY c.customer_id,f.title )   (actual time=9164..19910 rows=642000 loops=1)
                -> Sort: c.customer_id, f.title  (actual time=9164..9448 rows=642000 loops=1)
                    -> Stream results  (cost=10.6e+6 rows=16.7e+6) (actual time=1.04..5168 rows=642000 loops=1)
                        -> Nested loop inner join  (cost=10.6e+6 rows=16.7e+6) (actual time=1.03..4207 rows=642000 loops=1)
                            -> Nested loop inner join  (cost=8.97e+6 rows=16.7e+6) (actual time=1.03..3605 rows=642000 loops=1)
                                -> Nested loop inner join  (cost=7.3e+6 rows=16.7e+6) (actual time=1.02..2986 rows=642000 loops=1)
                                    -> Inner hash join (no condition)  (cost=1.61e+6 rows=16.1e+6) (actual time=1..191 rows=634000 loops=1)
                                        -> Filter: (cast(p.payment_date as date) = '2005-07-30')  (cost=1.68 rows=16086) (actual time=0.0814..21.8 rows=634 loops=1)
                                            -> Table scan on p  (cost=1.68 rows=16086) (actual time=0.0514..12.7 rows=16044 loops=1)
                                        -> Hash
                                            -> Covering index scan on f using idx_title  (cost=103 rows=1000) (actual time=0.0583..0.653 rows=1000 loops=1)
                                    -> Covering index lookup on r using rental_date (rental_date=p.payment_date)  (cost=0.25 rows=1.04) (actual time=0.0027..0.00392 rows=1.01 loops=634000)
                                -> Single-row index lookup on c using PRIMARY (customer_id=r.customer_id)  (cost=250e-6 rows=1) (actual time=442e-6..511e-6 rows=1 loops=642000)
                            -> Single-row covering index lookup on i using PRIMARY (inventory_id=r.inventory_id)  (cost=250e-6 rows=1) (actual time=378e-6..463e-6 rows=1 loops=642000)

```
Узкое место 
Sort: c.customer_id, f.title  (actual time=9164..9448 rows=642000 loops=1)
убрал film так как данные из этой таблицы не нужны для результата, время сильно улучшилось.

```
EXPLAIN ANALYZE                            
select distinct concat(c.last_name, ' ', c.first_name), sum(p.amount) over (partition by c.customer_id)
from payment p, rental r, customer c, inventory i
where date(p.payment_date) = '2005-07-30' and p.payment_date = r.rental_date and r.customer_id = c.customer_id and i.inventory_id = r.inventory_id

JOHNSON PATRICIA	30.95
WILLIAMS LINDA	5.98
JONES BARBARA	11.98
BROWN ELIZABETH	6.98
MOORE MARGARET	4.99
ANDERSON LISA	16.98
THOMAS NANCY	11.97
JACKSON KAREN	10.98
WHITE BETTY	4.99
HARRIS HELEN	4.99

-> Limit: 200 row(s)  (cost=0..0 rows=0) (actual time=44.5..44.6 rows=200 loops=1)
    -> Table scan on <temporary>  (cost=2.5..2.5 rows=0) (actual time=44.5..44.6 rows=200 loops=1)
        -> Temporary table with deduplication  (cost=0..0 rows=0) (actual time=44.5..44.5 rows=391 loops=1)
            -> Window aggregate with buffering: sum(payment.amount) OVER (PARTITION BY c.customer_id )   (actual time=38.7..43.7 rows=642 loops=1)
                -> Sort: c.customer_id  (actual time=38.6..38.8 rows=642 loops=1)
                    -> Stream results  (cost=19015 rows=16700) (actual time=0.183..37.9 rows=642 loops=1)
                        -> Nested loop inner join  (cost=19015 rows=16700) (actual time=0.173..36.7 rows=642 loops=1)
                            -> Nested loop inner join  (cost=13170 rows=16700) (actual time=0.166..34.2 rows=642 loops=1)
                                -> Nested loop inner join  (cost=7325 rows=16700) (actual time=0.154..31.8 rows=642 loops=1)
                                    -> Filter: (cast(p.payment_date as date) = '2005-07-30')  (cost=1633 rows=16086) (actual time=0.132..25.7 rows=634 loops=1)
                                        -> Table scan on p  (cost=1633 rows=16086) (actual time=0.0939..17.4 rows=16044 loops=1)
                                    -> Covering index lookup on r using rental_date (rental_date=p.payment_date)  (cost=0.25 rows=1.04) (actual time=0.00652..0.00902 rows=1.01 loops=634)
                                -> Single-row index lookup on c using PRIMARY (customer_id=r.customer_id)  (cost=0.25 rows=1) (actual time=0.00296..0.00304 rows=1 loops=642)
                            -> Single-row covering index lookup on i using PRIMARY (inventory_id=r.inventory_id)  (cost=0.25 rows=1) (actual time=0.00322..0.00331 rows=1 loops=642)

```

Пробовал добавлять индексы 

CREATE INDEX payment_date_id ON payment(payment_date, amount);
CREATE INDEX rental_date_id ON rental(rental_date);

Скорость выполнения увеличилась в 4 раза... 

Удалил 

DROP INDEX payment_date_id ON payment;
DROP INDEX rental_date_id ON rental;

Убрал оконную функцию

```
EXPLAIN ANALYZE                           
select distinct concat(c.last_name, ' ', c.first_name), sum(p.amount)
from payment p, rental r, customer c, inventory i
where date(p.payment_date) = '2005-07-30' and p.payment_date = r.rental_date and r.customer_id = c.customer_id and i.inventory_id = r.inventory_id
GROUP BY c.customer_id
```

-- индексировал даты и поменял условия

```
CREATE INDEX payment_date_id ON payment(payment_date);

EXPLAIN ANALYZE
select distinct concat(c.last_name, ' ', c.first_name), sum(p.amount)
from payment p, rental r, customer c, inventory i
where p.payment_date >= '2005-07-30' and p.payment_date < DATE_ADD('2005-07-30', INTERVAL 1 DAY) and p.payment_date = r.rental_date and r.customer_id = c.customer_id and i.inventory_id = r.inventory_id
GROUP BY c.customer_id
```
```
-> Limit: 200 row(s)  (actual time=16.9..17 rows=200 loops=1)
    -> Sort with duplicate removal: `concat(c.last_name, ' ', c.first_name)`, `sum(p.amount)`  (actual time=16.9..16.9 rows=200 loops=1)
        -> Table scan on <temporary>  (actual time=16.2..16.3 rows=391 loops=1)
            -> Aggregate using temporary table  (actual time=16.2..16.2 rows=391 loops=1)
                -> Nested loop inner join  (cost=798 rows=645) (actual time=0.0844..14.1 rows=642 loops=1)
                    -> Nested loop inner join  (cost=575 rows=645) (actual time=0.0775..11 rows=642 loops=1)
                        -> Nested loop inner join  (cost=349 rows=634) (actual time=0.0498..4.16 rows=634 loops=1)
                            -> Filter: ((r.rental_date >= TIMESTAMP'2005-07-30 00:00:00') and (r.rental_date < <cache>(('2005-07-30' + interval 1 day))))  (cost=127 rows=634) (actual time=0.0345..1.83 rows=634 loops=1)
                                -> Covering index range scan on r using rental_date over ('2005-07-30 00:00:00' <= rental_date < '2005-07-31 00:00:00')  (cost=127 rows=634) (actual time=0.0311..1.24 rows=634 loops=1)
                            -> Single-row index lookup on c using PRIMARY (customer_id=r.customer_id)  (cost=0.25 rows=1) (actual time=0.0031..0.00317 rows=1 loops=634)
                        -> Index lookup on p using payment_date_id (payment_date=r.rental_date)  (cost=0.254 rows=1.02) (actual time=0.00814..0.00976 rows=1.01 loops=634)
                    -> Single-row covering index lookup on i using PRIMARY (inventory_id=r.inventory_id)  (cost=0.246 rows=1) (actual time=0.00422..0.00429 rows=1 loops=642)

```

Время уменьшилось еще в три раза (actual time=16.9..17


## Дополнительные задания (со звёздочкой*)
Эти задания дополнительные, то есть не обязательные к выполнению, и никак не повлияют на получение вами зачёта по этому домашнему заданию. Вы можете их выполнить, если хотите глубже шире разобраться в материале.

### Задание 3*

Самостоятельно изучите, какие типы индексов используются в PostgreSQL. Перечислите те индексы, которые используются в PostgreSQL, а в MySQL — нет.

*Приведите ответ в свободной форме.*

https://habr.com/ru/articles/102785/

Bitmap index, Reverse index, Partial index, Function based index
