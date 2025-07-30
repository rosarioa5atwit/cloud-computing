from datetime import datetime
from fastapi import FastAPI, HTTPException, Depends
import mysql.connector
from mysql.connector import Error
from pydantic import BaseModel
from typing import Optional, List
from dotenv import load_dotenv
import os
from contextlib import contextmanager

load_dotenv()
app = FastAPI()

# MySQL Configuration (from your DBeaver screenshot)
DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",  # Replace with your actual username
    "password": "C@t23321",  # Replace with your actual password
    "database": "my_guitar_shop"
}

# Database Connection Manager
@contextmanager
def get_db_connection():
    conn = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        yield conn
    except Error as e:
        print(f"MySQL Connection Error: {e}")
        raise HTTPException(status_code=500, detail="Database connection failed")
    finally:
        if conn and conn.is_connected():
            conn.close()

# Database Cursor Manager
@contextmanager
def get_db_cursor(dictionary=True):
    with get_db_connection() as conn:
        cursor = conn.cursor(dictionary=dictionary)
        try:
            yield cursor
            conn.commit()
        except Error as e:
            conn.rollback()
            print(f"MySQL Error: {e}")
            raise HTTPException(status_code=500, detail="Database operation failed")
        finally:
            cursor.close()

# Pydantic Models (same as before)
class Product(BaseModel):  # Renamed from Item to Product
    product_id: int
    category_id: int
    product_code: str
    product_name: str
    description: Optional[str] = None
    list_price: float
    discount_percent: float
    date_added: datetime

class Item(BaseModel):  # Keep this if you have an items table, or remove it
   item_id: int
   order_id: int
   product_id: int
   item_price: float
   discount_percent: float
   quantity: int

class address(BaseModel):
    address_id: int
    line1: str
    line2: str
    city: str
    state: str
    zip_code: str
    phone: str
    disabled: int

class category(BaseModel):
    category_id: int
    category_name: str

class Customer(BaseModel):
    customer_id: int
    email_address: str
    password: str
    first_name: str
    last_name: str
    shipping_address_id: int
    billing_address_id: int

class Order(BaseModel):
    order_id: int
    customer_id: int
    order_date: datetime  # Changed to string for MySQL date handling
    ship_amount: float
    tax_amount: float
    ship_date: datetime
    ship_address_id: int
    card_type: str
    card_number: str
    card_expires: str
    billing_address_id: int
@app.get("/")
async def root():
    return {
        "message": "Guitar Shop API", 
        "endpoints": {
            "orders": "/orders",
            "order_detail": "/orders/{id}",
            "users": "/users",
            "items": "/items"
        }
    }
# Endpoints (updated for MySQL)
@app.get("/orders/{order_id}", response_model=Order)
async def get_order(order_id: int):
    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM orders WHERE order_id = %s", (order_id,))
        order = cursor.fetchone()
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        return order
    
@app.get("/products/{product_code}", response_model=List[Product])
async def get_product(product_code: str):
    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM products WHERE product_code = %s", (product_code,))
        products = cursor.fetchall()
        if not products:
            raise HTTPException(status_code=404, detail="Product not found")
        return products

@app.get("/customers/{customer_id}", response_model=List[Order])
async def get_customer_orders(customer_id: int):
    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM orders WHERE customer_id = %s", (customer_id,))
        orders = cursor.fetchall()
        if not orders:
            raise HTTPException(status_code=404, detail="No orders found for this customer")
        return orders
    
@app.get("/orders/date/{order_date}", response_model=List[Order])
async def get_orders_by_date(order_date: str):
    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM orders WHERE order_date = %s", (order_date,))
        orders = cursor.fetchall()
        if not orders:
            raise HTTPException(status_code=404, detail="No orders found for this date")
        return orders

@app.put("/customers/update/{customer_id}", response_model=Customer)
async def update_customer(customer_id: int, customer: Customer):
    with get_db_cursor() as cursor:
        cursor.execute(
            "UPDATE customers SET email_address = %s, password = %s, first_name = %s, last_name = %s, shipping_address_id = %s, billing_address_id = %s WHERE customer_id = %s",
            (
                customer.email_address,
                customer.password,
                customer.first_name,
                customer.last_name,
                customer.shipping_address_id,
                customer.billing_address_id,
                customer_id,
            ),
        )
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Customer not found")
        # Fetch the updated customer to return
        cursor.execute("SELECT * FROM customers WHERE customer_id = %s", (customer_id,))
        updated_customer = cursor.fetchone()
        return updated_customer
@app.put("/categories/update/{category_id}", response_model=Category)
async def update_category(category_id: int, category: Category):
    with get_db_cursor() as cursor:
        cursor.execute(
            "UPDATE categories SET name = %s, description = %s WHERE category_id = %s",
            (
                category.name,
                category.description,
                category_id,
            ),
        )
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Category not found")
        # Fetch the updated category to return
        cursor.execute("SELECT * FROM categories WHERE category_id = %s", (category_id,))
        updated_category = cursor.fetchone()
        return updated_category

@app.put("/orders/update/{order_id}", response_model=Order)
async def update_order(order_id: int, order: Order):
    with get_db_cursor() as cursor:
        cursor.execute(
            "UPDATE orders SET customer_id = %s, order_date = %s, ship_amount = %s, tax_amount = %s, ship_date = %s, ship_address_id = %s, card_type = %s, card_number = %s, card_expires = %s, billing_address_id = %s WHERE order_id = %s",
            (
                order.customer_id,
                order.order_date.strftime("%Y-%m-%d %H:%M:%S"),
                order.ship_amount,
                order.tax_amount,
                order.ship_date.strftime("%Y-%m-%d %H:%M:%S"),
                order.ship_address_id,
                order.card_type,
                order.card_number,
                order.card_expires,
                order.billing_address_id,
                order_id,
            ),
        )
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Order not found")
        # Fetch the updated order to return
        cursor.execute("SELECT * FROM orders WHERE order_id = %s", (order_id,))
        updated_order = cursor.fetchone()
        return updated_order

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)