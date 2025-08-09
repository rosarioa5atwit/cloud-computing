import mysql.connector
from mysql.connector import Error
from contextlib import contextmanager
from fastapi import HTTPException

# MySQL Configuration
DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "C@t23321",
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

def display_menu():
    print("\n" + "="*50)
    print("    GUITAR SHOP API MENU")
    print("="*50)
    print("1. Get Order by ID")
    print("2. Get Product by Code")
    print("3. Get Customer Orders by Customer ID")
    print("4. Get Orders by Date")
    print("5. Update Customer")
    print("6. Update Category")
    print("7. Update Order")
    print("8. Get Products (with filters)")
    print("9. Get Customers (with filters)")
    print("10. Update Product")
    print("11. Test Database Connection")
    print("0. Exit")
    print("="*50)

def test_database_connection():
    print("Testing database connection...")
    try:
        with get_db_cursor() as cursor:
            cursor.execute("SELECT COUNT(*) as count FROM products")
            result = cursor.fetchone()
            print(f"Connection successful! Found {result['count']} products in database.")
            return True
    except Exception as err:
        print(f"Connection failed: {err}")
        return False

def get_order_by_id():
    try:
        order_id = int(input("Enter Order ID: "))
        with get_db_cursor() as cursor:
            cursor.execute("SELECT * FROM orders WHERE order_id = %s", (order_id,))
            order = cursor.fetchone()
            if order:
                print(f"Order found: {order}")
            else:
                print("Order not found")
    except ValueError:
        print("Please enter a valid number")
    except Exception as err:
        print(f"Error: {err}")

def get_product_by_code():
    try:
        product_code = input("Enter Product Code: ")
        with get_db_cursor() as cursor:
            cursor.execute("SELECT * FROM products WHERE product_code = %s", (product_code,))
            products = cursor.fetchall()
            if products:
                print(f"Products found: {products}")
            else:
                print("Product not found")
    except Exception as err:
        print(f"Error: {err}")

def get_customer_orders():
    try:
        customer_id = int(input("Enter Customer ID: "))
        with get_db_cursor() as cursor:
            cursor.execute("SELECT * FROM orders WHERE customer_id = %s", (customer_id,))
            orders = cursor.fetchall()
            if orders:
                print(f"Found {len(orders)} orders for customer {customer_id}")
                for order in orders:
                    print(f"  Order ID: {order['order_id']}, Date: {order['order_date']}")
            else:
                print("No orders found for this customer")
    except ValueError:
        print("Please enter a valid number")
    except Exception as err:
        print(f"Error: {err}")

def get_orders_by_date():
    try:
        order_date = input("Enter Order Date (YYYY-MM-DD): ")
        with get_db_cursor() as cursor:
            cursor.execute("SELECT * FROM orders WHERE DATE(order_date) = %s", (order_date,))
            orders = cursor.fetchall()
            if orders:
                print(f"Found {len(orders)} orders for {order_date}")
                for order in orders:
                    print(f"  Order ID: {order['order_id']}, Customer: {order['customer_id']}")
            else:
                print("No orders found for this date")
    except Exception as err:
        print(f"Error: {err}")

def get_products_with_filters():
    try:
        print("Optional filters (press Enter to skip):")
        category_input = input("Category ID: ")
        price_input = input("Minimum Price: ")
        limit_input = input("Limit (default 10): ")
        
        query = "SELECT * FROM products WHERE 1=1"
        params = []
        
        if category_input:
            query += " AND category_id = %s"
            params.append(int(category_input))
        
        if price_input:
            query += " AND list_price >= %s"
            params.append(float(price_input))
        
        limit = int(limit_input) if limit_input else 10
        query += " LIMIT %s"
        params.append(limit)
        
        with get_db_cursor() as cursor:
            cursor.execute(query, params)
            products = cursor.fetchall()
            print(f"Found {len(products)} products")
            for product in products:
                print(f"  {product['product_name']} - ${product['list_price']}")
                
    except ValueError:
        print("Please enter valid numbers")
    except Exception as err:
        print(f"Error: {err}")

def start_fastapi_server():
    print("Starting the FastAPI server...")
    try:
        with get_db_connection() as connection:
            if connection.is_connected():
                mycursor = connection.cursor()
                # Add your SQL query here
                mycursor.execute("SELECT * FROM products LIMIT 5")
                results = mycursor.fetchall()
                return results
    except Error as err:
        print(f"Database Error: {err}")
        return []

def update_customer():
    try:
        customer_id = int(input("Enter Customer ID to update: "))
        
        # First check if customer exists
        with get_db_cursor() as cursor:
            cursor.execute("SELECT * FROM customers WHERE customer_id = %s", (customer_id,))
            existing_customer = cursor.fetchone()
            if not existing_customer:
                print("Customer not found")
                return
            
            print(f"Current customer data: {existing_customer}")
            print("Enter new values (press Enter to keep current value):")
            
            email = input(f"Email ({existing_customer['email_address']}): ").strip()
            if not email:
                email = existing_customer['email_address']
            
            password = input(f"Password ({existing_customer['password']}): ").strip()
            if not password:
                password = existing_customer['password']
            
            first_name = input(f"First Name ({existing_customer['first_name']}): ").strip()
            if not first_name:
                first_name = existing_customer['first_name']
            
            last_name = input(f"Last Name ({existing_customer['last_name']}): ").strip()
            if not last_name:
                last_name = existing_customer['last_name']
            
            ship_addr = input(f"Shipping Address ID ({existing_customer['shipping_address_id']}): ").strip()
            if not ship_addr:
                ship_addr = existing_customer['shipping_address_id']
            else:
                ship_addr = int(ship_addr)
            
            bill_addr = input(f"Billing Address ID ({existing_customer['billing_address_id']}): ").strip()
            if not bill_addr:
                bill_addr = existing_customer['billing_address_id']
            else:
                bill_addr = int(bill_addr)
            
            # Update the customer
            cursor.execute(
                "UPDATE customers SET email_address = %s, password = %s, first_name = %s, last_name = %s, shipping_address_id = %s, billing_address_id = %s WHERE customer_id = %s",
                (email, password, first_name, last_name, ship_addr, bill_addr, customer_id)
            )
            
            if cursor.rowcount > 0:
                print("Customer updated successfully")
            else:
                print("No changes made")
                
    except ValueError:
        print("Please enter valid numbers for ID fields")
    except Exception as err:
        print(f"Error: {err}")

def update_category():
    try:
        category_id = int(input("Enter Category ID to update: "))
        
        with get_db_cursor() as cursor:
            cursor.execute("SELECT * FROM categories WHERE category_id = %s", (category_id,))
            existing_category = cursor.fetchone()
            if not existing_category:
                print("Category not found")
                return
            
            print(f"Current category: {existing_category['category_name']}")
            new_name = input("Enter new category name: ").strip()
            
            if new_name:
                cursor.execute(
                    "UPDATE categories SET category_name = %s WHERE category_id = %s",
                    (new_name, category_id)
                )
                print("Category updated successfully")
            else:
                print("No changes made")
                
    except ValueError:
        print("Please enter a valid category ID")
    except Exception as err:
        print(f"Error: {err}")

def update_product():
    try:
        product_id = int(input("Enter Product ID to update: "))
        
        with get_db_cursor() as cursor:
            cursor.execute("SELECT * FROM products WHERE product_id = %s", (product_id,))
            existing_product = cursor.fetchone()
            if not existing_product:
                print("Product not found")
                return
            
            print(f"Current product data: {existing_product}")
            print("Enter new values (press Enter to keep current value):")
            
            category_id = input(f"Category ID ({existing_product['category_id']}): ").strip()
            if not category_id:
                category_id = existing_product['category_id']
            else:
                category_id = int(category_id)
            
            product_code = input(f"Product Code ({existing_product['product_code']}): ").strip()
            if not product_code:
                product_code = existing_product['product_code']
            
            product_name = input(f"Product Name ({existing_product['product_name']}): ").strip()
            if not product_name:
                product_name = existing_product['product_name']
            
            description = input(f"Description ({existing_product.get('description', 'None')}): ").strip()
            if not description:
                description = existing_product.get('description')
            
            list_price = input(f"List Price ({existing_product['list_price']}): ").strip()
            if not list_price:
                list_price = existing_product['list_price']
            else:
                list_price = float(list_price)
            
            discount_percent = input(f"Discount Percent ({existing_product['discount_percent']}): ").strip()
            if not discount_percent:
                discount_percent = existing_product['discount_percent']
            else:
                discount_percent = float(discount_percent)
            
            # Update the product
            cursor.execute(
                "UPDATE products SET category_id = %s, product_code = %s, product_name = %s, description = %s, list_price = %s, discount_percent = %s WHERE product_id = %s",
                (category_id, product_code, product_name, description, list_price, discount_percent, product_id)
            )
            
            if cursor.rowcount > 0:
                print("Product updated successfully")
            else:
                print("No changes made")
                
    except ValueError:
        print("Please enter valid numbers for numeric fields")
    except Exception as err:
        print(f"Error: {err}")

def update_order():
    try:
        order_id = int(input("Enter Order ID to update: "))
        
        with get_db_cursor() as cursor:
            cursor.execute("SELECT * FROM orders WHERE order_id = %s", (order_id,))
            existing_order = cursor.fetchone()
            if not existing_order:
                print("Order not found")
                return
            
            print(f"Current order data: {existing_order}")
            print("Enter new values (press Enter to keep current value):")
            
            customer_id = input(f"Customer ID ({existing_order['customer_id']}): ").strip()
            if not customer_id:
                customer_id = existing_order['customer_id']
            else:
                customer_id = int(customer_id)
            
            ship_amount = input(f"Ship Amount ({existing_order['ship_amount']}): ").strip()
            if not ship_amount:
                ship_amount = existing_order['ship_amount']
            else:
                ship_amount = float(ship_amount)
            
            tax_amount = input(f"Tax Amount ({existing_order['tax_amount']}): ").strip()
            if not tax_amount:
                tax_amount = existing_order['tax_amount']
            else:
                tax_amount = float(tax_amount)
            
            ship_address_id = input(f"Ship Address ID ({existing_order['ship_address_id']}): ").strip()
            if not ship_address_id:
                ship_address_id = existing_order['ship_address_id']
            else:
                ship_address_id = int(ship_address_id)
            
            card_type = input(f"Card Type ({existing_order['card_type']}): ").strip()
            if not card_type:
                card_type = existing_order['card_type']
            
            card_number = input(f"Card Number ({existing_order['card_number']}): ").strip()
            if not card_number:
                card_number = existing_order['card_number']
            
            card_expires = input(f"Card Expires ({existing_order['card_expires']}): ").strip()
            if not card_expires:
                card_expires = existing_order['card_expires']
            
            billing_address_id = input(f"Billing Address ID ({existing_order['billing_address_id']}): ").strip()
            if not billing_address_id:
                billing_address_id = existing_order['billing_address_id']
            else:
                billing_address_id = int(billing_address_id)
            
            # Update the order (keeping original dates)
            cursor.execute(
                "UPDATE orders SET customer_id = %s, ship_amount = %s, tax_amount = %s, ship_address_id = %s, card_type = %s, card_number = %s, card_expires = %s, billing_address_id = %s WHERE order_id = %s",
                (customer_id, ship_amount, tax_amount, ship_address_id, card_type, card_number, card_expires, billing_address_id, order_id)
            )
            
            if cursor.rowcount > 0:
                print("Order updated successfully")
            else:
                print("No changes made")
                
    except ValueError:
        print("Please enter valid numbers for numeric fields")
    except Exception as err:
        print(f"Error: {err}")

def get_customers_with_filters():
    try:
        print("Optional filters (press Enter to skip):")
        first_name = input("First Name: ").strip()
        email = input("Email: ").strip()
        limit_input = input("Limit (default 10): ").strip()
        
        query = "SELECT * FROM customers WHERE 1=1"
        params = []
        
        if first_name:
            query += " AND first_name LIKE %s"
            params.append(f"%{first_name}%")
        
        if email:
            query += " AND email_address LIKE %s"
            params.append(f"%{email}%")
        
        limit = int(limit_input) if limit_input else 10
        query += " LIMIT %s"
        params.append(limit)
        
        with get_db_cursor() as cursor:
            cursor.execute(query, params)
            customers = cursor.fetchall()
            print(f"Found {len(customers)} customers")
            for customer in customers:
                print(f"  ID: {customer['customer_id']}, Name: {customer['first_name']} {customer['last_name']}, Email: {customer['email_address']}")
                
    except ValueError:
        print("Please enter valid numbers")
    except Exception as err:
        print(f"Error: {err}")

def driver():
    print("Welcome to Guitar Shop API Driver!")
    
    while True:
        display_menu()
        try:
            choice = input("\nEnter your choice (0-11): ").strip()
            
            if choice == '0':
                print("Goodbye!")
                break
            elif choice == '1':
                get_order_by_id()
            elif choice == '2':
                get_product_by_code()
            elif choice == '3':
                get_customer_orders()
            elif choice == '4':
                get_orders_by_date()
            elif choice == '5':
                update_customer()
            elif choice == '6':
                update_category()
            elif choice == '7':
                update_order()
            elif choice == '8':
                get_products_with_filters()
            elif choice == '9':
                get_customers_with_filters()
            elif choice == '10':
                update_product()
            elif choice == '11':
                test_database_connection()
            else:
                print("Invalid choice. Please enter a number between 0-11.")
                
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as err:
            print(f"Unexpected error: {err}")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    driver()