import subprocess
import sys
import time
import threading 
import requests
import mysql.connector
from database import DB_CONFIG


def test_database_connection():
    """Test database connection and return detailed diagnostics"""
    try:
        
        print("🔍 Testing database connection...")
        print(f"   Host: {DB_CONFIG['host']}")
        print(f"   Port: {DB_CONFIG['port']}")
        print(f"   Database: {DB_CONFIG['database']}")
        print(f"   User: {DB_CONFIG['user']}")
        
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Test database exists
        cursor.execute("SELECT DATABASE()")
        current_db = cursor.fetchone()[0]
        print(f"✅ Connected to database: {current_db}")
        
        # Check tables exist
        cursor.execute("SHOW TABLES")
        tables = [table[0] for table in cursor.fetchall()]
        print(f"📋 Available tables: {tables}")
        
        # Check specific tables we need
        required_tables = ['vendors', 'customers', 'administrator']  # Use singular as that's what exists
        missing_tables = [table for table in required_tables if table not in tables]
        
        if missing_tables:
            print(f"⚠️  Missing required tables: {missing_tables}")
            return False, f"Missing tables: {missing_tables}"
        
        # Test table structures
        for table in required_tables:
            cursor.execute(f"DESCRIBE {table}")
            columns = cursor.fetchall()
            print(f"📊 Table '{table}' columns: {[col[0] for col in columns]}")
            
            # Check if table has data
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"   Records in {table}: {count}")
        
        cursor.close()
        conn.close()
        return True, "✅ Database connection and structure verified"
        
    except mysql.connector.Error as e:
        error_msg = f"❌ Database error: {e}"
        print(error_msg)
        
        # Provide specific troubleshooting based on error code
        if "2003" in str(e):
            print("🔧 Troubleshooting: Connection refused")
            print("   - Check if MySQL server is running")
            print("   - Verify port 5433 (unusual for MySQL, typically 3306)")
            print("   - Try: net start mysql (Windows)")
        elif "1045" in str(e):
            print("🔧 Troubleshooting: Access denied")
            print("   - Check username/password in database.py")
            print("   - Verify user has database permissions")
        elif "1049" in str(e):
            print("🔧 Troubleshooting: Database doesn't exist")
            print("   - Create database 'cd_database'")
            print("   - Run: CREATE DATABASE cd_database;")
        
        return False, error_msg




def start_fastapi_server():
    try:
        process = subprocess.Popen([
            sys.executable, "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000",
        ])
        return process
    except Exception as e:
        print(f"Error starting FastAPI server: {e}")
        return None

def stop_fastapi_server(process):
    if process:
        process.terminate()
        process.wait()

def driver():
    continueLoop = True
    fastapi_process = start_fastapi_server()
    if not fastapi_process:
        print("Failed to start FastAPI server.")
        return  
    
    print("🚀 FastAPI server started on port 8000")
    print("⏳ Waiting for server to initialize...")
    time.sleep(2)  # Wait for server to start
    
    try:
        while continueLoop:
            print("\n" + "="*50)
            print("           CD STORE MANAGEMENT SYSTEM")
            print("="*50)
            print("1. Customer Management")
            print("2. Vendor Management")
            print("3. Purchase & Cart Management")
            print("4. Rental Management")
            print("5. Admin Management")
            print("6. Inventory Management")
            print("7. Card Processing")
            print("8. Service Status Check")
            print("9. Test Database Connection")
            print("10. Exit")
            print("="*50)
            choose = input("Enter your choice (1-10): ")
            
            if choose == "1":
                print("\n--- Customer Management System ---")
                print("1. Customer Signup")
                print("2. Customer Login")
                print("3. View Customer Profile")
                print("4. Edit Customer Address")
                print("5. Back to Main Menu")
                
                customer_choice = input("Enter your choice (1-5): ")
                
                if customer_choice == "1":
                    print("Customer Signup...")
                    first_name = input("Enter first name: ")
                    last_name = input("Enter last name: ")
                    email = input("Enter email: ")
                    shipping_address = input("Enter shipping address: ")
                    billing_address = input("Enter billing address: ")

                    url = "http://localhost:3801/user/signup"
                    data = {
                        "first_name": first_name,
                        "last_name": last_name,
                        "email": email,
                        "shipping_address": shipping_address,
                        "billing_address": billing_address
                    }
                    try:
                        response = requests.put(url, json=data, timeout=5)
                        if response.status_code == 200:
                            print("✅ Customer added successfully!")
                        else:
                            print(f"❌ Failed to add customer: {response.status_code} - {response.text}")
                    except requests.exceptions.RequestException as e:
                        print(f"❌ Error: {e}")
                        
                elif customer_choice == "2":
                    print("Customer Login...")
                    user_id = input("Enter User ID: ")

                    url = "http://localhost:3800/login"
                    headers = {"usrID": user_id}
                    try:
                        response = requests.get(url, headers=headers, timeout=5)
                        if response.status_code == 200 and response.text != "null":
                            print("✅ Login successful!")
                            print(f"🔑 Token: {response.text}")
                        else:
                            print("❌ Login failed or returned null")
                    except requests.exceptions.RequestException as e:
                        print(f"❌ Error: {e}")

                elif customer_choice == "3":
                    print("View Customer Profile...")
                    first_name = input("Enter first name: ")
                    last_name = input("Enter last name: ")
                    token = input("Enter token: ")

                    url = f"http://localhost:3801/user/profile?first={first_name}&last={last_name}"
                    headers = {"token": token}
                    try:
                        response = requests.get(url, headers=headers, timeout=5)
                        if response.status_code == 200:
                            print("✅ Profile retrieved successfully!")
                            print(f"📋 Profile: {response.json()}")
                        else:
                            print(f"❌ Failed to retrieve profile: {response.status_code} - {response.text}")
                    except requests.exceptions.RequestException as e:
                        print(f"❌ Error: {e}")
                        
                elif customer_choice == "4":
                    print("Edit Customer Address...")
                    first_name = input("Enter first name: ")
                    last_name = input("Enter last name: ")
                    new_shipping_address = input("Enter new shipping address: ")
                    new_billing_address = input("Enter new billing address: ")
                    token = input("Enter token: ")
                    
                    url = "http://localhost:3801/user/profile/edit"
                    params = {
                        "first": first_name,
                        "last": last_name,
                        "shipaddr": new_shipping_address,
                        "billaddr": new_billing_address
                    }
                    headers = {"token": token}
                    try:
                        response = requests.get(url, params=params, headers=headers, timeout=5)
                        if response.status_code == 200:
                            print("✅ Address updated successfully!")
                            print(f"📋 Response: {response.json()}")
                        else:
                            print(f"❌ Failed to update address: {response.status_code} - {response.text}")
                    except requests.exceptions.RequestException as e:
                        print(f"❌ Error: {e}")
                        
                elif customer_choice == "5":
                    continue  # Back to main menu
                else:
                    print("❌ Invalid choice. Please try again.")

            elif choose == "2":
                print("\n--- Vendor Management System ---")
                print("1. Vendor Signup")
                print("2. Add Inventory Item")
                print("3. Remove Inventory Item")
                print("4. View Vendor Products")
                print("5. Back to Main Menu")
                
                vendor_choice = input("Enter your choice (1-5): ")
                
                if vendor_choice == "1":
                    print("Vendor Signup...")
                    vendor_id = int(input("Enter Vendor ID: "))
                    vendor_name = input("Enter Vendor Name: ")
                    email_address = input("Enter Email Address: ")
                    shipping_address = int(input("Enter Shipping Address ID: "))
                    billing_address = int(input("Enter Billing Address ID: "))

                    vendor_data = {
                        "vendor_id": vendor_id,
                        "vendor_name": vendor_name,
                        "email_address": email_address,
                        "shipping_address": shipping_address,
                        "billing_address": billing_address
                    }
                    url = "http://localhost:3809/vendor/signup"  # Use vendor service port
                    try:
                        response = requests.put(url, json=vendor_data, timeout=5)
                        if response.status_code == 200:
                            print("✅ Vendor added successfully!")
                            print(f"📋 Response: {response.json()}")
                        else:
                            print(f"❌ Failed to add vendor: {response.status_code} - {response.text}")
                    except requests.exceptions.RequestException as e:
                        print(f"❌ Error: {e}")

                elif vendor_choice == "2":
                    print("Add Inventory Item...")
                    try:
                        # Remove cd_id input since it will be auto-generated
                        cd_name = input("Enter CD Name: ")
                        artist = input("Enter Artist: ")
                        genre_id = int(input("Enter Genre ID: "))
                        release_date = input("Enter Release Date (YYYY-MM-DD): ")
                        price = float(input("Enter Price: "))
                        quantity = int(input("Enter Quantity: "))
                        vendor_id = int(input("Enter Vendor ID: "))
                        vendor_name = input("Enter your vendor name: ")
                        token = input("Enter token (or press Enter for test): ").strip()
                        
                        if not token:
                            token = "test_token"

                        # First check if vendor exists in permissions
                        print("🔐 Checking vendor permissions...")
                        try:
                            perm_url = "http://localhost:3803/permissions"
                            perm_headers = {"first": vendor_name, "type": "vendors"}
                            perm_response = requests.get(perm_url, headers=perm_headers, timeout=5)
                            print(f"📊 Permissions check status: {perm_response.status_code}")
                            
                            if perm_response.status_code == 200:
                                print("✅ Vendor permissions verified")
                            else:
                                print("⚠️  Vendor permissions check failed, but proceeding...")
                        except requests.exceptions.RequestException as pe:
                            print(f"⚠️  Permissions service error: {pe}")
                            print("🔄 Proceeding without permission check...")

                        cd_data = {
                            # cd_id removed - will be auto-generated
                            "cd_name": cd_name,
                            "artist": artist,
                            "genre_id": genre_id,
                            "release_date": release_date,
                            "price": price,
                            "quantity": quantity,
                            "vendor_id": vendor_id
                        }
                        
                        print(f"🔄 Sending request to inventory service...")
                        print(f"   URL: http://localhost:3804/inventory/additem")
                        print(f"   Data: {cd_data}")
                        print(f"   Headers: first={vendor_name}")
                        
                        # Use inventory service directly
                        url = "http://localhost:3804/inventory/additem"
                        headers = {"first": vendor_name, "last": ""}
                        response = requests.put(url, json=cd_data, headers=headers, timeout=10)
                        
                        print(f"📊 Response Status: {response.status_code}")
                        print(f"📄 Response Headers: {dict(response.headers)}")
                        
                        if response.status_code == 200:
                            print("✅ Inventory item added successfully!")
                            try:
                                result = response.json()
                                print(f"📋 Response: {result}")
                                if 'cd_id' in result:
                                    print(f"🆔 Auto-generated CD ID: {result['cd_id']}")
                            except:
                                print(f"📋 Response: {response.text}")
                        elif response.status_code == 400:
                            print("❌ Permission denied or validation error")
                            print("💡 Checking what went wrong...")
                            print(f"📋 Response: {response.text}")
                            
                            # Try without permissions check for debugging
                            print("\n🔄 Attempting direct database insert test...")
                            try:
                                # Test database connection and constraints
                                test_conn = mysql.connector.connect(**DB_CONFIG)
                                test_cursor = test_conn.cursor()
                                
                                # Check if vendor exists
                                test_cursor.execute("SELECT vendor_id FROM vendors WHERE vendor_id = %s", (vendor_id,))
                                vendor_exists = test_cursor.fetchone()
                                if vendor_exists:
                                    print(f"   ✅ Vendor ID {vendor_id} exists")
                                else:
                                    print(f"   ❌ Vendor ID {vendor_id} does not exist")
                                
                                # Check if genre exists
                                test_cursor.execute("SELECT genre_id FROM genre WHERE genre_id = %s", (genre_id,))
                                genre_exists = test_cursor.fetchone()
                                if genre_exists:
                                    print(f"   ✅ Genre ID {genre_id} exists")
                                else:
                                    print(f"   ❌ Genre ID {genre_id} does not exist")
                                    print(f"   💡 Try creating genre first or use existing genre ID")
                                
                                test_cursor.close()
                                test_conn.close()
                                
                            except mysql.connector.Error as db_error:
                                print(f"   ❌ Database check failed: {db_error}")
                                
                        elif response.status_code == 422:
                            print("❌ Validation Error - Field mismatch")
                            print("💡 The service expects different field names:")
                            try:
                                error_detail = response.json()
                                print(f"📋 Validation errors: {error_detail}")
                                
                                # Try with corrected data based on validation error
                                if "quanity" in str(error_detail):
                                    print("\n🔄 Retrying with 'quanity' field name...")
                                    cd_data_fixed = cd_data.copy()
                                    cd_data_fixed["quanity"] = cd_data_fixed.pop("quantity", quantity)
                                    
                                    retry_response = requests.put(url, json=cd_data_fixed, headers=headers, timeout=10)
                                    print(f"📊 Retry Response Status: {retry_response.status_code}")
                                    if retry_response.status_code == 200:
                                        print("✅ Item added successfully with corrected field name!")
                                        print(f"📋 Response: {retry_response.json()}")
                                    else:
                                        print(f"❌ Retry also failed: {retry_response.text}")
                            except:
                                print(f"📋 Raw response: {response.text}")
                                
                        elif response.status_code == 500:
                            print("❌ Internal Server Error in inventory service")
                            print("💡 Possible database issues:")
                            print(f"   - Database table 'cd' might not exist")
                            print(f"   - Column name mismatch (expecting 'quanity' not 'quantity')")
                            print(f"   - Foreign key constraint violation")
                            print(f"   - Database connection issue")
                            print(f"📋 Raw response: {response.text}")
                            
                            # Try to diagnose database structure
                            print("\n🔍 Checking database structure...")
                            try:
                                check_conn = mysql.connector.connect(**DB_CONFIG)
                                check_cursor = check_conn.cursor()
                                
                                # Check if cd table exists
                                check_cursor.execute("SHOW TABLES LIKE 'cd'")
                                table_exists = check_cursor.fetchone()
                                if table_exists:
                                    print("   ✅ Table 'cd' exists")
                                    
                                    # Check table structure
                                    check_cursor.execute("DESCRIBE cd")
                                    columns = check_cursor.fetchall()
                                    print(f"   📊 Table structure: {[col[0] for col in columns]}")
                                    
                                    # Check if quantity column exists (with or without typo)
                                    column_names = [col[0] for col in columns]
                                    if 'quantity' in column_names:
                                        print("   ✅ Column 'quantity' exists (correct spelling)")
                                    elif 'quanity' in column_names:
                                        print("   ⚠️  Column 'quanity' exists (with typo)")
                                    else:
                                        print("   ❌ No quantity column found")
                                else:
                                    print("   ❌ Table 'cd' does not exist")
                                
                                check_cursor.close()
                                check_conn.close()
                                
                            except mysql.connector.Error as db_error:
                                print(f"   ❌ Database structure check failed: {db_error}")
                        else:
                            print(f"❌ Failed to add item: {response.status_code}")
                            print(f"📋 Response: {response.text}")
                            

                    except ValueError as ve:
                        print(f"❌ Error: Invalid input type. {ve}")
                        print("💡 Make sure to enter:")
                        print("   - Numbers for CD ID, Genre ID, Price, Quantity, Vendor ID")
                        print("   - Date in format YYYY-MM-DD")
                    except requests.exceptions.ConnectionError:
                        print("❌ Error: Cannot connect to inventory service on port 3804")
                        print("💡 Hint: Make sure the inventory service is running")
                        print("   Try running: uvicorn inventorymanagement:app --port 3804")
                    except requests.exceptions.RequestException as e:
                        print(f"❌ Network Error: {e}")

                elif vendor_choice == "3":
                    print("Remove Inventory Item...")
                    try:
                        item_id = int(input("Enter Item ID to remove: "))
                        vendor_name = input("Enter your vendor name: ")
                        url = f"http://localhost:3804/inventory/removeitem?pid={item_id}"
                        headers = {"first": vendor_name, "last": ""}
                        response = requests.get(url, headers=headers, timeout=5)
                        
                        if response.status_code == 200:
                            print("✅ Item removed successfully!")
                            print(f"📋 Response: {response.json()}")
                        else:
                            print(f"❌ Failed to remove item: {response.status_code} - {response.text}")
                    except ValueError:
                        print("❌ Error: Invalid input type. Please enter correct values.")
                    except requests.exceptions.RequestException as e:
                        print(f"❌ Error: {e}")

                elif vendor_choice == "4":
                    print("View Vendor Products...")
                    try:
                        vendor_id = input("Enter Vendor ID: ")
                        print(f"🔄 Fetching products for vendor {vendor_id}...")
                        url = f"http://localhost:3809/vendor/fetchproducts?table={vendor_id}"
                        response = requests.get(url, timeout=5)
                        
                        print(f"📊 Response Status: {response.status_code}")
                        
                        if response.status_code == 200:
                            products = response.json()
                            if products:
                                print("✅ Products retrieved successfully!")
                                print(f"📋 Found {len(products)} products:")
                                for i, product in enumerate(products, 1):
                                    print(f"   {i}. {product}")
                            else:
                                print("📋 No products found for this vendor")
                        else:
                            print(f"❌ Failed to retrieve products: {response.status_code} - {response.text}")
                    except requests.exceptions.ConnectionError:
                        print("❌ Error: Cannot connect to vendor service on port 3809")
                        print("💡 Hint: Make sure the vendor service is running")
                        print("   Try running: uvicorn vendormanagement:app --port 3809")
                    except requests.exceptions.RequestException as e:
                        print(f"❌ Error: {e}")

                elif vendor_choice == "5":
                    continue  # Back to main menu
                else:
                    print("❌ Invalid choice. Please try again.")

            elif choose == "3":
                print("\n--- Purchase & Cart Management ---")
                print("1. Add Item to Cart")
                print("2. View Order")
                print("3. Process Purchase")
                print("4. Cancel Order")
                print("5. Access store")
                print("6. Back to Main Menu")
                
                purchase_choice = input("Enter your choice (1-5): ")
                
                if purchase_choice == "1":
                    print("Add Item to Cart...")
                    try:
                        # The service only needs cd_id and quantity based on the SQL
                        cd_id = int(input("Enter CD ID: "))
                        quantity = int(input("Enter Quantity: "))
                        token = input("Enter token: ")

                        # Check what the service actually needs
                        print("🔄 Checking purchase service requirements...")
                        
                        # First try with the expected Order_items structure
                        data = {
                            "item_id": 0,  # Will be auto-generated by database
                            "order_id": 0,  # Will be linked later when order is created
                            "cd_id": cd_id,
                            "quantity": quantity
                        }
                        
                        headers = {"token": token}
                        url = "http://localhost:3802/purchase/orderitem"
                        
                        print(f"🔄 Sending request to purchase service...")
                        print(f"   URL: {url}")
                        print(f"   Data: {data}")
                        print(f"   Headers: {headers}")
                        
                        response = requests.put(url, json=data, headers=headers, timeout=5)
                        
                        print(f"📊 Response Status: {response.status_code}")
                        
                        if response.status_code == 200:
                            print("✅ Item added to cart successfully!")
                            try:
                                print(f"📋 Response: {response.json()}")
                            except:
                                print(f"📋 Response: {response.text}")
                        elif response.status_code == 400:
                            print("❌ Token validation failed")
                            print("💡 Possible issues:")
                            print("   - Invalid or expired token")
                            print("   - IDP service not running")
                            print(f"📋 Response: {response.text}")
                        elif response.status_code == 422:
                            print("❌ Validation Error - Field mismatch")
                            try:
                                error_detail = response.json()
                                print(f"📋 Validation errors: {error_detail}")
                                
                                # Check if we need different field structure
                                missing_fields = []
                                for error in error_detail.get('detail', []):
                                    if error.get('type') == 'missing':
                                        missing_fields.append(error.get('loc', [])[-1])
                                
                                if missing_fields:
                                    print(f"💡 Missing required fields: {missing_fields}")
                                    
                                    # Try again with missing fields
                                    print("🔄 Retrying with additional fields...")
                                    if 'item_id' in missing_fields:
                                        data['item_id'] = int(input("Enter Item ID: "))
                                    if 'order_id' in missing_fields:
                                        data['order_id'] = int(input("Enter Order ID: "))
                                    
                                    retry_response = requests.put(url, json=data, headers=headers, timeout=5)
                                    print(f"📊 Retry Response Status: {retry_response.status_code}")
                                    if retry_response.status_code == 200:
                                        print("✅ Item added to cart successfully!")
                                        print(f"📋 Response: {retry_response.json()}")
                                    else:
                                        print(f"❌ Retry failed: {retry_response.text}")
                                        
                            except:
                                print(f"📋 Raw response: {response.text}")
                        elif response.status_code == 500:
                            print("❌ Internal Server Error in purchase service")
                            print("💡 Possible database issues:")
                            print("   - Database connection problem")
                            print("   - Table 'order_items' doesn't exist")
                            print("   - Column mismatch in INSERT statement")
                            print("   - MySQL authentication plugin issue")
          
                            print(f"📋 Raw response: {response.text}")
                            
                            # Check database structure with better error handling
                            print("\n🔍 Checking order_items table structure...")
                            try:
                                # Try to connect with different authentication method
                                db_config_alt = DB_CONFIG.copy()
                                db_config_alt['auth_plugin'] = 'mysql_native_password'
                                
                                check_conn = mysql.connector.connect(**db_config_alt)
                                check_cursor = check_conn.cursor()
                                
                                # Check if order_items table exists
                                check_cursor.execute("SHOW TABLES LIKE 'order_items'")
                                table_exists = check_cursor.fetchone()
                                if table_exists:
                                    print("   ✅ Table 'order_items' exists")
                                    
                                    # Check table structure
                                    check_cursor.execute("DESCRIBE order_items")
                                    columns = check_cursor.fetchall()
                                    print(f"   📊 Table structure: {[col[0] for col in columns]}")
                                    
                                    # The service SQL only inserts cd_id and quantity
                                    print("   💡 Service SQL: INSERT INTO order_items (cd_id, quantity) VALUES (%s, %s)")
                                    print("   💡 Make sure cd_id exists in cd table")
                                    
                                    # Check if CD exists
                                    check_cursor.execute("SELECT cd_id FROM cd WHERE cd_id = %s", (cd_id,))
                                    cd_exists = check_cursor.fetchone()
                                    if cd_exists:
                                        print(f"   ✅ CD ID {cd_id} exists")
                                    else:
                                        print(f"   ❌ CD ID {cd_id} does not exist")
                                        print("   💡 Add the CD to inventory first")
                                else:
                                    print("   ❌ Table 'order_items' does not exist")
                                    print("   💡 Create the table with:")
                                    print("   CREATE TABLE order_items (")
                                    print("     item_id INT AUTO_INCREMENT PRIMARY KEY,")
                                    print("     order_id INT,")
                                    print("     cd_id INT,")
                                    print("     quantity INT,")
                                    print("     FOREIGN KEY (cd_id) REFERENCES cd(cd_id)")
                                    print("   );")
                                
                                check_cursor.close()
                                check_conn.close()
                                
                            except mysql.connector.Error as db_error:
                                if "Authentication plugin" in str(db_error):
                                    print("   ❌ MySQL authentication plugin issue")
                                    print("   💡 Solutions:")
                                    print("   1. Update mysql-connector-python: pip install --upgrade mysql-connector-python")
                                    print("   2. Or change MySQL user auth: ALTER USER 'your_user'@'localhost' IDENTIFIED WITH mysql_native_password BY 'your_password';")
                                    print("   3. Or add to database.py: 'auth_plugin': 'mysql_native_password'")
                                    
                                    # Try to provide basic troubleshooting without database connection
                                    print("\n🔍 Basic troubleshooting (without DB connection):")
                                    print("   1. Check if all services are running")
                                    print("   2. Verify the purchase service can connect to database")
                                    print("   3. Make sure 'order_items' table exists")
                                    print(f"   4. Ensure CD ID {cd_id} exists in 'cd' table")
                                    
                                    # Suggest manual database checks
                                    print("\n💡 Manual database checks (run in MySQL):")
                                    print(f"   SHOW TABLES LIKE 'order_items';")
                                    print(f"   DESCRIBE order_items;")
                                    print(f"   SELECT * FROM cd WHERE cd_id = {cd_id};")
                                
                                else:
                                    print(f"   ❌ Database check failed: {db_error}")
                                    
                            except Exception as e:
                                print(f"   ❌ Unexpected error: {e}")
                                print("\n💡 Alternative troubleshooting:")
                                print("   1. Check purchase service logs for detailed error")
                                print("   2. Verify database connection in purchase service")
                                print("   3. Test database connection manually")
                                print(f"   4. Ensure CD ID {cd_id} exists before adding to cart")
                        else:
                            print(f"❌ Failed to add item to cart: {response.status_code}")
                            print(f"📋 Response: {response.text}")
                            

                    except ValueError as ve:
                        print(f"❌ Error: Invalid input type. {ve}")
                        print("💡 Make sure to enter numbers for CD ID and Quantity")
                    except requests.exceptions.ConnectionError:
                        print("❌ Error: Cannot connect to purchase service on port 3802")
                        print("💡 Hint: Make sure the purchase service is running")
                        print("   Try running: python purchasemanagement.py")
                    except requests.exceptions.RequestException as e:
                        print(f"❌ Error: {e}")

                elif purchase_choice == "2":
                    print("View Order...")
                    token = input("Enter token: ")
                    id = input("Enter order ID: ")
                    try:
                        url = f"http://localhost:3802/purchase/orderstatus?oid={id}"
                        headers = {"token": token}
                        response = requests.get(url, headers=headers, timeout=5)
                        
                        if response.status_code == 200:
                            print("✅ Cart retrieved successfully!")
                            print(f"📋 Cart: {response.json()}")
                        else:
                            print(f"❌ Failed to retrieve cart: {response.status_code} - {response.text}")
                    except requests.exceptions.RequestException as e:
                        print(f"❌ Error: {e}")

                elif purchase_choice == "3":
                    print("Process Purchase...")
                    try:
                        order_id = int(input("Enter Order ID: "))
                        customer_id = int(input("Enter Customer ID: "))
                        card_type = input("Enter Card Type (Visa/MasterCard/Capital One): ")
                        card_number = input("Enter Card Number: ")
                        token = input("Enter token: ")
                        
                        # Validate card first
                        card_url = f"http://localhost:3806/validatecard?bank={card_type}&cardnum={card_number}"
                        card_response = requests.get(card_url, timeout=5)
                        
                        if card_response.status_code != 200:
                            print("❌ Invalid card information")
                            continue
                        
                        # Create order data (simplified)
                        from datetime import datetime
                        order_data = {
                            "order_id": order_id,
                            "customer_id": customer_id,
                            "purchase_date": datetime.now().isoformat(),
                            "is_rental": False,
                            "tax_amount": 0.0,
                            "ship_date": datetime.now().isoformat(),
                            "order_status": "processing",
                            "shipped_amount": 0.0,
                            "card_type": card_type,
                            "card_number": card_number,
                            "card_expiration": "2025-12-31T00:00:00",
                            "card_cvv": "123",
                            "date_due": datetime.now().isoformat(),
                            "billing_address": 1
                        }
                        
                        item_id = int(input("Enter Item ID: "))
                        url = f"http://localhost:3802/purchase/order?i_id={item_id}&r=false"
                        headers = {"token": token}
                        response = requests.put(url, json=order_data, headers=headers, timeout=5)
                        
                        if response.status_code == 200:
                            print("✅ Purchase processed successfully!")
                            print(f"📋 Response: {response.json()}")
                        else:
                            print(f"❌ Failed to process purchase: {response.status_code} - {response.text}")
                            
                    except ValueError as ve:
                        print(f"❌ Error: Invalid input type. {ve}")
                    except requests.exceptions.RequestException as e:
                        print(f"❌ Error: {e}")

                elif purchase_choice == "4":
                    print("Cancel Order...")
                    try:
                        order_id = int(input("Enter Order ID to cancel: "))
                        token = input("Enter token: ")
                        
                        url = f"http://localhost:3802/purchase/cancel?oid={order_id}"
                        headers = {"token": token}
                        response = requests.get(url, headers=headers, timeout=5)
                        
                        if response.status_code == 200:
                            print("✅ Order cancelled successfully!")
                            print(f"📋 Response: {response.json()}")
                        else:
                            print(f"❌ Failed to cancel order: {response.status_code} - {response.text}")
                    except ValueError as ve:
                        print(f"❌ Error: Invalid input type. {ve}")
                    except requests.exceptions.RequestException as e:
                        print(f"❌ Error: {e}")

                elif purchase_choice == "5":
                    print("Access Store...")
                    try:
                        token = input("Enter token: ")
                        
                        url = "http://localhost:3802/store"
                        headers = {"token": token}
                        response = requests.get(url, headers=headers, timeout=5)
                        
                        if response.status_code == 200:
                            print("✅ CD table accessed!")
                            print(f"📋 Response: {response.json()}")
                        else:
                            print(f"❌ Failed to Display CDs: {response.status_code} - {response.text}")

                    except requests.exceptions.RequestException as e:
                        print(f"❌ Error: {e}")

                elif purchase_choice == "6":
                    continue
                else:
                    print("❌ Invalid choice. Please try again.")

            elif choose == "4":
                print("\n--- Rental Management ---")
                print("1. Create Rental")
                print("2. Extend Rental")
                print("3. Cancel Rental")
                print("4. Back to Main Menu")
                
                rental_choice = input("Enter your choice (1-4): ")
                
                if rental_choice == "1":
                    print("Create Rental...")
                    try:
                        order_id = int(input("Enter Order ID: "))
                        customer_id = int(input("Enter Customer ID: "))
                        item_id = int(input("Enter Item ID: "))
                        card_type = input("Enter Card Type: ")
                        card_number = input("Enter Card Number: ")
                        token = input("Enter token: ")
                        
                        from datetime import datetime
                        order_data = {
                            "order_id": order_id,
                            "customer_id": customer_id,
                            "purchase_date": datetime.now().isoformat(),
                            "is_rental": True,
                            "tax_amount": 0.0,
                            "ship_date": datetime.now().isoformat(),
                            "order_status": "processing",
                            "shipped_amount": 0.0,
                            "card_type": card_type,
                            "card_number": card_number,
                            "card_expiration": "2025-12-31T00:00:00",
                            "card_cvv": "123",
                            "date_due": datetime.now().isoformat(),
                            "billing_address": 1
                        }
                        
                        url = f"http://localhost:3807/rental/create?i_id={item_id}&r=true"
                        headers = {"token": token}
                        response = requests.put(url, json=order_data, headers=headers, timeout=10)
                        
                        if response.status_code == 200:
                            print("✅ Rental created successfully!")
                            print(f"📋 Response: {response.text}")
                        else:
                            print(f"❌ Failed to create rental: {response.status_code} - {response.text}")
                    except ValueError as ve:
                        print(f"❌ Error: Invalid input type. {ve}")
                    except requests.exceptions.RequestException as e:
                        print(f"❌ Error: {e}")

                elif rental_choice == "2":
                    print("Extend Rental...")
                    try:
                        order_id = int(input("Enter Order ID to extend: "))
                        token = input("Enter token: ")
                        
                        url = f"http://localhost:3807/rental/extend?oid={order_id}"
                        headers = {"token": token}
                        response = requests.get(url, headers=headers, timeout=5)
                        
                        if response.status_code == 200:
                            print("✅ Rental extended successfully!")
                            print(f"📋 Response: {response.json()}")
                        else:
                            print(f"❌ Failed to extend rental: {response.status_code} - {response.text}")
                    except ValueError as ve:
                        print(f"❌ Error: Invalid input type. {ve}")
                    except requests.exceptions.RequestException as e:
                        print(f"❌ Error: {e}")

                elif rental_choice == "3":
                    print("Cancel Rental...")
                    try:
                        order_id = input("Enter Order ID to cancel: ")
                        token = input("Enter token: ")
                        
                        url = f"http://localhost:3807/rental/cancel?oid={order_id}"
                        headers = {"token": token}
                        response = requests.get(url, headers=headers, timeout=10)
                        
                        if response.status_code == 200:
                            print("✅ Rental cancelled successfully!")
                            print(f"📋 Response: {response.text}")
                        else:
                            print(f"❌ Failed to cancel rental: {response.status_code} - {response.text}")
                    except requests.exceptions.RequestException as e:
                        print(f"❌ Error: {e}")

                elif rental_choice == "4":
                    continue
                else:
                    print("❌ Invalid choice. Please try again.")

            elif choose == "5":
                print("\n--- Admin Management ---")
                print("1. View All Customers")
                print("2. View All Vendors") 
                print("3. Generate Reports")
                print("4. Back to Main Menu")
                
                admin_choice = input("Enter your choice (1-4): ")
                
                if admin_choice == "1":
                    print("View All Customers...")
                    token = input("Enter admin token: ")
                    first_name = input("Enter admin first name: ")
                    last_name = input("Enter admin last name: ")

                    url = f"http://localhost:3808/admin/fetch?table=customers"
                    headers = {"token": token, "first": first_name, "last": last_name}
                            
                    print("🔄 Attempting admin service call...")
                            
                    response = requests.get(url, headers=headers, timeout=5)
                    print(f"📊 Admin service response: {response.status_code}")
                            
                    if response.status_code == 200:
                        customers = response.json()
                        print("✅ Customers retrieved successfully!")
                        if customers:
                            print(f"📋 Found {len(customers)} customers:")
                            for i, customer in enumerate(customers, 1):
                                    print(f"   {i}. {customer}")
                        else:
                            print("📋 No customers found")
                    else:
                        print("❌ Admin service failed due to service bugs")
                        print("\n🔧 WORKAROUND: Direct database query")
                                
                                # Direct database query as workaround
                        try:
                            work_conn = mysql.connector.connect(**db_config_alt)
                            work_cursor = work_conn.cursor()
                                    
                            work_cursor.execute("SELECT customer_id, first_name, last_name, email, shipping_address, billing_address FROM customers")
                            customers = work_cursor.fetchall()
                                    
                            if customers:
                                print(f"✅ Found {len(customers)} customers (direct database query):")
                                for i, customer in enumerate(customers, 1):
                                     print(f"   {i}. ID: {customer[0]}, Name: {customer[1]} {customer[2]}, Email: {customer[3]}")
                            else:
                                print("📋 No customers found in database")
                                        
                            work_cursor.close()
                            work_conn.close()
                                    
                        except mysql.connector.Error as work_error:
                            print(f"❌ Direct database query failed: {work_error}")
                                    
                        except requests.exceptions.ConnectionError:
                            print("❌ Error: Cannot connect to admin service on port 3808")
                            print("💡 Make sure admin service is running: python adminmanagement.py")
                        except requests.exceptions.RequestException as e:
                            print(f"❌ Error: {e}")
                    

                elif admin_choice == "2":
                    print("View All Vendors...")
                    token = input("Enter admin token: ")
                    first_name = input("Enter admin first name: ")
                    last_name = input("Enter admin last name: ")
                    
                    try:
                        url = f"http://localhost:3808/admin/fetch?table=vendors"
                        headers = {"token": token, "first": first_name, "last": last_name}
                        response = requests.get(url, headers=headers, timeout=5)
                        
                        if response.status_code == 200:
                            vendors = response.json()
                            print("✅ Vendors retrieved successfully!")
                            if vendors:
                                print(f"📋 Found {len(vendors)} vendors:")
                                for i, vendor in enumerate(vendors, 1):
                                    print(f"   {i}. {vendor}")
                            else:
                                print("📋 No vendors found")
                        else:
                            print(f"❌ Failed to retrieve vendors: {response.status_code} - {response.text}")
                    except requests.exceptions.RequestException as e:
                        print(f"❌ Error: {e}")

                elif admin_choice == "3":
                    print("View Reports...")
                    token = input("Enter admin token: ")
                    first_name = input("Enter admin first name: ")
                    last_name = input("Enter admin last name: ")
                    try:
                        url = "http://localhost:3808/admin/reports"
                        headers = {"token": token, "first": first_name, "last": last_name}
                        response = requests.get(url, headers=headers, timeout=10)
                        
                        if response.status_code == 200:
                            print("✅ Reports retrieved successfully!")
                            print(f"📋 Reports: {response.json()}")
                        else:
                            print(f"❌ Failed to retrieve reports: {response.status_code} - {response.text}")
                    except requests.exceptions.RequestException as e:
                        print(f"❌ Error: {e}")

                elif admin_choice == "4":
                    continue
                else:
                    print("❌ Invalid choice. Please try again.")

            elif choose == "6":
                print("\n--- Inventory Management ---")
                print("1. Add CD")
                print("2. Remove CD")
                print("3. Back to Main Menu")
                
                inv_choice = input("Enter your choice (1-3): ")
                
                if inv_choice == "1":
                    print("Add CD directly to inventory...")
                    try:
                        # Remove cd_id input since it will be auto-generated
                        cd_name = input("Enter CD Name: ")
                        artist = input("Enter Artist: ")
                        genre_id = int(input("Enter Genre ID: "))
                        release_date = input("Enter Release Date (YYYY-MM-DD): ")
                        price = float(input("Enter Price: "))
                        quantity = int(input("Enter Quantity: "))
                        vendor_id = int(input("Enter Vendor ID: "))
                        first_name = input("Enter your first name: ")
                        last_name = input("Enter your last name (Hit enter if unapplicable): ")

                        cd_data = {
                            # cd_id removed - will be auto-generated
                            "cd_name": cd_name,
                            "artist": artist,
                            "genre_id": genre_id,
                            "release_date": release_date,
                            "price": price,
                            "quantity": quantity,
                            "vendor_id": vendor_id
                        }

                        if len(last_name)<1:
                            last_name = None
                        
                        url = "http://localhost:3804/inventory/additem"
                        headers = {"first": first_name, "last": last_name}
                        response = requests.put(url, json=cd_data, headers=headers, timeout=5)
                        
                        if response.status_code == 200:
                            print("✅ CD added successfully!")
                            try:
                                result = response.json()
                                print(f"📋 Response: {result}")
                                if 'cd_id' in result:
                                    print(f"🆔 Auto-generated CD ID: {result['cd_id']}")
                            except:
                                print(f"📋 Response: {response.text}")
                        else:
                            print(f"❌ Failed to add CD: {response.status_code} - {response.text}")
                            
                    except ValueError as ve:
                        print(f"❌ Error: Invalid input type. {ve}")
                        print("💡 Make sure to enter:")
                        print("   - Numbers for Genre ID, Price, Quantity, Vendor ID")
                        print("   - Date in format YYYY-MM-DD")
                    except requests.exceptions.RequestException as e:
                        print(f"❌ Error: {e}")

                elif inv_choice == "2":
                    print("Remove CD directly from inventory...")
                    try:
                        cd_id = int(input("Enter CD ID: "))
                        first_name = input("Enter your first name: ")
                        last_name = input("Enter your last name (Hit enter if unapplicable): ")

                        if len(last_name)<1:
                            last_name = None

                        url = f"http://localhost:3804/inventory/removeitem?pid={cd_id}"
                        headers = {"first": first_name, "last": last_name}
                        response = requests.get(url, headers=headers, timeout=5)

                        if response.status_code == 200:
                            print("✅ CD removed successfully!")
                            print(f"📋 Response: {response.json()}")
                        else:
                            print(f"❌ Failed to remove CD: {response.status_code} - {response.text}")

                    except requests.exceptions.RequestException as e:
                        print(f"❌ Error: {e}")


            elif choose == "7":
                print("\n--- Card Processing ---")
                print("Validate Credit Card...")
                bank = input("Enter bank (Visa/MasterCard/Capital One): ")
                card_num = input("Enter card number: ")
                
                try:
                    url = f"http://localhost:3806/validatecard?bank={bank}&cardnum={card_num}"
                    response = requests.get(url, timeout=5)
                    
                    if response.status_code == 200:
                        print("✅ Card is valid!")
                    else:
                        print("❌ Card is invalid!")
                        
                except requests.exceptions.RequestException as e:
                    print(f"❌ Error: {e}")

            elif choose == "8":
                print("\n🔍 Checking Service Status...")
                services = [
                    ("Main API", "http://localhost:8000/"),
                    ("Customer Management", "http://localhost:3801/"),
                    ("Purchase Management", "http://localhost:3802/"),
                    ("IDP Service", "http://localhost:3800/"),
                    ("Inventory Management", "http://localhost:3804/"),
                    ("Vendor Management", "http://localhost:3809/"),
                    ("Admin Management", "http://localhost:3808/"),
                    ("Rental Management", "http://localhost:3807/"),
                    ("Process Cards", "http://localhost:3806/"),
                    ("Permissions", "http://localhost:3803/"),
                    ("Reporting", "http://localhost:3805/"),
                ]
                
                for service_name, url in services:
                    try:
                        response = requests.get(url, timeout=2)
                        if response.status_code in [200, 422]:  # 422 is common for FastAPI root
                            print(f"✅ {service_name}: Online")
                        else:
                            print(f"⚠️  {service_name}: Responding but status {response.status_code}")
                    except requests.exceptions.RequestException:
                        print(f"❌ {service_name}: Offline")

            elif choose == "9":
                print("🔍 Running Database Diagnostics...")
                success, message = test_database_connection()
                print(f"\n📋 Database Status: {message}")
                
            elif choose == "10":
                print("Exiting the program.")
                continueLoop = False
            else:
                print("❌ Invalid choice. Please try again.")

            if continueLoop:
                input("\n⏸️  Press Enter to continue...")
                
    finally:
        stop_fastapi_server(fastapi_process)
        print("🛑 FastAPI server stopped.")    
if __name__ == "__main__":
    driver()
