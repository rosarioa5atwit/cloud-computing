from typing import Any, Dict, List
import mysql.connector

def connect_to_db():
    mydb = None
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="C@t23321",
            database="my_guitar_shop"
        )
        print("Successfully connected to MySQL database!")
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        return None
    
    return mydb

def query1(mydb) :
    if mydb is None:
        print("No database connection available")
        return []

    mycursor = None
    try:
        mycursor = mydb.cursor()
        sql_query = """
            select product_code, product_name, list_price, discount_percent
            from products p
            order by p.list_price desc;
        """
        mycursor.execute(sql_query)
        results = mycursor.fetchall()

        print("\n=== Query 1: Products by Price ===")
        for row in results:
            print(f"product_code: {row[0]}, product_name: {row[1]}, list_price: {row[2]}, discount_percent: {row[3]}")
        
        return results

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return []
    finally:
        if mycursor:
            mycursor.close()

def query_addresses(mydb):
    if mydb is None:
        print("No database connection available")
        return
        
    try:
        mycursor = mydb.cursor()

        sql_query = "select address_id, line1 from addresses a"

        mycursor.execute(sql_query)

        results = mycursor.fetchall()

        for row in results:
            print(f"address_id: {row[0]}, address_line1: {row[1]}")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if mydb and mydb.is_connected():
            mydb.close()
        print("MySQL connection closed.")

def query2(mydb):
    """Query customers with last names between M and Zz"""
    if mydb is None:
        print("No database connection available")
        return []

    mycursor = None
    try:
        mycursor = mydb.cursor()
        sql_query = """
            select first_name, last_name, 
            Concat(last_name,', ',first_name) as full_name  
            from customers c 
            where last_name between 'M' and 'Zz'
            order by last_name asc;
        """
        mycursor.execute(sql_query)
        results = mycursor.fetchall()

        print("\n=== Query 2: Customers M-Z ===")
        for row in results:
            print(f"first_name: {row[0]}, last_name: {row[1]}, full_name: {row[2]}")
        
        return results 

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return []
    finally:
        if mycursor:
            mycursor.close()

def query3(mydb):
    """Query products with price between 500 and 2000"""
    if mydb is None:
        print("No database connection available")
        return []

    mycursor = None
    try:
        mycursor = mydb.cursor()
        sql_query = """
            select product_name, list_price, date_added
            from products p 
            where list_price > 500 and list_price < 2000
            order by date_added desc;
        """
        mycursor.execute(sql_query)
        results = mycursor.fetchall()

        print("\n=== Query 3: Products $500-$2000 ===")
        for row in results:
            print(f"product_name: {row[0]}, list_price: {row[1]}, date_added: {row[2]}")
        
        return results 
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return []
    finally:
        if mycursor:
            mycursor.close()

def query4(mydb):
    """Query order items with calculated totals > 500"""
    if mydb is None:
        print("No database connection available")
        return []

    mycursor = None
    try:
        mycursor = mydb.cursor()
        sql_query = """
            select item_id, item_price, discount_amount, quantity, 
            (item_price * quantity) as price_total,
            (discount_amount * quantity) as discount_total,
            ((item_price - discount_amount) * quantity) as item_total
            from Order_items
            where ((item_price - discount_amount) * quantity) > 500
            order by item_total desc;
        """
        mycursor.execute(sql_query)
        results = mycursor.fetchall()

        print("\n=== Query 4: Order Items > $500 ===")
        for row in results:
            print(f"item_id: {row[0]}, item_price: {row[1]}, discount_amount: {row[2]}, quantity: {row[3]}, price_total: {row[4]}, discount_total: {row[5]}, item_total: {row[6]}")
        
        return results 

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return []
    finally:
        if mycursor:
            mycursor.close()

def query5(mydb):
    """Query categories and products joined"""
    if mydb is None:
        print("No database connection available")
        return []

    mycursor = None
    try:
        mycursor = mydb.cursor()
        sql_query = """
            select category_name, product_name, list_price 
            from categories c2  
            join products p on c2.category_id = p.category_id 
            order by 
            c2.category_name asc,
            p.product_name asc;
        """
        mycursor.execute(sql_query)
        results = mycursor.fetchall()

        print("\n=== Query 5: Categories and Products ===")
        for row in results:
            print(f"category_name: {row[0]}, product_name: {row[1]}, list_price: {row[2]}")
        
        return results  

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return []
    finally:
        if mycursor:
            mycursor.close()

def query6(mydb):
    """Query specific customer address"""
    if mydb is None:
        print("No database connection available")
        return []

    mycursor = None
    try:
        mycursor = mydb.cursor()
        sql_query = """
            select first_name, last_name, line1, city, state, zip_code 
            from customers c 
            join addresses a on c.customer_id = a.customer_id
            where c.email_address = 'allan.sherwood@yahoo.com'
            order by zip_code asc;
        """
        mycursor.execute(sql_query)
        results = mycursor.fetchall()

        print("\n=== Query 6: Allan Sherwood's Address ===")
        for row in results:
            print(f"first_name: {row[0]}, last_name: {row[1]}, line1: {row[2]}, city: {row[3]}, state: {row[4]}, zip_code: {row[5]}")
        
        return results

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return []
    finally:
        if mycursor:
            mycursor.close()

def query7(mydb):
    """Query all customer addresses"""
    if mydb is None:
        print("No database connection available")
        return []

    mycursor = None
    try:
        mycursor = mydb.cursor()
        sql_query = """
            select first_name, last_name , line1, city, state, zip_code
            from customers c
            join addresses a on c.shipping_address_id = a.address_id 
            order by zip_code asc;
        """
        mycursor.execute(sql_query)
        results = mycursor.fetchall()

        print("\n=== Query 7: All Customer Addresses ===")
        for row in results:
            print(f"first_name: {row[0]}, last_name: {row[1]}, line1: {row[2]}, city: {row[3]}, state: {row[4]}, zip_code: {row[5]}")
        
        return results 

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return []
    finally:
        if mycursor:
            mycursor.close()

def main():
    mydb = connect_to_db()
    if mydb:
        query1(mydb)
        query2(mydb)
        query3(mydb)
        query4(mydb)
        query5(mydb)
        query6(mydb)
        query7(mydb)
        
        if mydb.is_connected():
            mydb.close()
            print("\nMain MySQL connection closed.")

if __name__ == "__main__":
    main()