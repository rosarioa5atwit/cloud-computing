select product_code, product_name, list_price, discount_percent
from products p
order by p.list_price desc;

select first_name, last_name,
Concat(last_name,', ',first_name) as full_name
from customers c
where last_name between 'M' and 'Zz'
order by last_name asc;

select product_name, list_price, date_added
from products p
where list_price > 500 and list_price < 2000
order by date_added desc;

select item_id, item_price, discount_amount, quantity,
(item_price * quantity )as price_total,
(discount_amount * quantity )as discount_total,
((item_price - discount_amount ) * quantity ) as item_total
from Order_items
where ((item_price - discount_amount ) * quantity ) > 500
order by item_total desc;

select category_name, product_name, list_price
from categories c2
join products p on c2.category_id = p.category_id
order by
c2.category_name asc,
p.product_name asc;

select first_name, last_name , line1, city, state, zip_code
from customers c
join addresses a on c.customer_id = a.customer_id
where c.email_address = 'allan.sherwood@yahoo.com'
order by zip_code asc;

select first_name, last_name , line1, city, state, zip_code
from customers c
join addresses a on c.shipping_address_id = a.address_id 
order by zip_code asc;
