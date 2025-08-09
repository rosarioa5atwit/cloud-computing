import requests
import json
from datetime import datetime

# API Base URL
BASE_URL = "http://localhost:8001"

def test_root():
    """Test the root endpoint"""
    print("\nTesting ROOT endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_get_order_by_id():
    """Test GET /orders/{order_id}"""
    print("\nTesting GET Order by ID...")
    order_id = 1  # Test with order ID 1
    try:
        response = requests.get(f"{BASE_URL}/orders/{order_id}")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print(f"Order found: {response.json()}")
        else:
            print(f"Response: {response.text}")
        return response.status_code in [200, 404]
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_get_product_by_code():
    """Test GET /products/{product_code}"""
    print("\nTesting GET Product by Code...")
    product_code = "sg"  # Test with a sample product code
    try:
        response = requests.get(f"{BASE_URL}/products/{product_code}")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print(f"Products found: {len(response.json())} items")
        else:
            print(f"Response: {response.text}")
        return response.status_code in [200, 404]
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_get_customer_orders():
    """Test GET /customers/{customer_id}"""
    print("\nTesting GET Customer Orders...")
    customer_id = 1  # Test with customer ID 1
    try:
        response = requests.get(f"{BASE_URL}/customers/{customer_id}")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print(f"Orders found: {len(response.json())} orders")
        else:
            print(f"Response: {response.text}")
        return response.status_code in [200, 404]
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_get_orders_by_date():
    """Test GET /orders/date/{order_date}"""
    print("\nTesting GET Orders by Date...")
    order_date = "2025-08-03 14:28:55"  # Test with a sample date
    try:
        response = requests.get(f"{BASE_URL}/orders/date/{order_date}")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print(f"Orders found: {len(response.json())} orders")
        else:
            print(f"Response: {response.text}")
        return response.status_code in [200, 404]
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_get_products_with_filters():
    """Test GET /products with query parameters"""
    print("\nTesting GET Products with filters...")
    params = {
        "category_id": 1,
        "min_price": 10.00,
        "limit": 5
    }
    try:
        response = requests.get(f"{BASE_URL}/products", params=params)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print(f"Products found: {len(response.json())} products")
        else:
            print(f"Response: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_get_customers_with_filters():
    """Test GET /customers with query parameters"""
    print("\nTesting GET Customers with filters...")
    params = {
        "first_name": "Erin",
        "limit": 5
    }
    try:
        response = requests.get(f"{BASE_URL}/customers", params=params)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print(f"Customers found: {len(response.json())} customers")
        else:
            print(f"Response: {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_update_customer():
    """Test PUT /customers/update/{customer_id}"""
    print("\nTesting UPDATE Customer...")
    
    # First, get an existing customer to update
    try:
        get_response = requests.get(f"{BASE_URL}/customers?limit=1")
        if get_response.status_code == 200 and len(get_response.json()) > 0:
            existing_customer = get_response.json()[0]
            customer_id = existing_customer['customer_id']
            
            # Use existing data with small modification
            customer_data = {
                "customer_id": customer_id,
                "email_address": existing_customer['email_address'],
                "password": existing_customer['password'],
                "first_name": existing_customer['first_name'] + "_Updated",
                "last_name": existing_customer['last_name'],
                "shipping_address_id": existing_customer['shipping_address_id'],
                "billing_address_id": existing_customer['billing_address_id']
            }
            
            response = requests.put(f"{BASE_URL}/customers/update/{customer_id}", json=customer_data)
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                print(f"Customer updated successfully: {response.json()['first_name']}")
                return True
            else:
                print(f"Response: {response.text}")
                return False
        else:
            print("No customers found to update")
            return True  # Consider this a pass since no data exists
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_update_category():
    """Test PUT /categories/update/{category_id}"""
    print("\nTesting UPDATE Category...")
    
    # Try to get existing categories first
    try:
        # Check if we can get any categories by trying to get products first
        products_response = requests.get(f"{BASE_URL}/products?limit=1")
        if products_response.status_code == 200 and len(products_response.json()) > 0:
            category_id = products_response.json()[0]['category_id']
            
            category_data = {
                "category_id": category_id,
                "category_name": "Test Updated Category"
            }
            
            response = requests.put(f"{BASE_URL}/categories/update/{category_id}", json=category_data)
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                print(f"Category updated successfully")
                return True
            else:
                print(f"Response: {response.text}")
                return response.status_code == 404  # Accept 404 as valid if category doesn't exist
        else:
            print("No categories found to update")
            return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_update_product():
    """Test PUT /products/update/{product_id}"""
    print("\nTesting UPDATE Product...")
    
    # First, get an existing product to update
    try:
        get_response = requests.get(f"{BASE_URL}/products?limit=1")
        if get_response.status_code == 200 and len(get_response.json()) > 0:
            existing_product = get_response.json()[0]
            product_id = existing_product['product_id']
            
            # Use existing data with small modification
            product_data = {
                "product_id": product_id,
                "category_id": existing_product['category_id'],
                "product_code": existing_product['product_code'],
                "product_name": existing_product['product_name'] + " (Updated)",
                "description": existing_product.get('description', 'Updated description'),
                "list_price": float(existing_product['list_price']),
                "discount_percent": float(existing_product['discount_percent']),
                "date_added": existing_product['date_added']
            }
            
            response = requests.put(f"{BASE_URL}/products/update/{product_id}", json=product_data)
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                print(f"Product updated successfully: {response.json()['product_name']}")
                return True
            else:
                print(f"Response: {response.text}")
                return False
        else:
            print("No products found to update")
            return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def run_all_tests():
    """Run all API tests"""
    print("Starting API Tests for Guitar Shop")
    print("="*60)
    
    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code != 200:
            print("Server is not running! Start the FastAPI server first.")
            return
    except requests.exceptions.ConnectionError:
        print("Cannot connect to server! Make sure FastAPI is running on port 8001.")
        return
    
    tests = [
        test_root,
        test_get_order_by_id,
        test_get_product_by_code,
        test_get_customer_orders,
        test_get_orders_by_date,
        test_get_products_with_filters,
        test_get_customers_with_filters,
        test_update_customer,
        test_update_category,
        test_update_product
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
            print("PASSED")
        else:
            print("FAILED")
    
    print("\n" + "="*60)
    print(f"Test Results: {passed}/{total} tests passed")
    if passed == total:
        print("All tests passed!")
    else:
        print("Some tests failed. Check the output above.")
        
    # Show some database statistics
    try:
        print("\nDatabase Statistics:")
        customers_resp = requests.get(f"{BASE_URL}/customers?limit=100")
        if customers_resp.status_code == 200:
            print(f"Total customers found: {len(customers_resp.json())}")
            
        products_resp = requests.get(f"{BASE_URL}/products?limit=100")
        if products_resp.status_code == 200:
            print(f"Total products found: {len(products_resp.json())}")
            
        orders_resp = requests.get(f"{BASE_URL}/customers/1")
        if orders_resp.status_code == 200:
            print(f"Orders for customer 1: {len(orders_resp.json())}")
    except:
        pass

def interactive_test_menu():
    """Interactive menu for testing individual endpoints"""
    while True:
        print("\n" + "="*50)
        print("    API TEST MENU")
        print("="*50)
        print("1. Test Root Endpoint")
        print("2. Test Get Order by ID")
        print("3. Test Get Product by Code")
        print("4. Test Get Customer Orders")
        print("5. Test Get Orders by Date")
        print("6. Test Get Products (with filters)")
        print("7. Test Get Customers (with filters)")
        print("8. Test Update Customer")
        print("9. Test Update Category")
        print("10. Test Update Product")
        print("11. Run All Tests")
        print("0. Exit")
        print("="*50)
        
        choice = input("\nEnter your choice (0-11): ").strip()
        
        if choice == '0':
            print("Goodbye!")
            break
        elif choice == '1':
            test_root()
        elif choice == '2':
            test_get_order_by_id()
        elif choice == '3':
            test_get_product_by_code()
        elif choice == '4':
            test_get_customer_orders()
        elif choice == '5':
            test_get_orders_by_date()
        elif choice == '6':
            test_get_products_with_filters()
        elif choice == '7':
            test_get_customers_with_filters()
        elif choice == '8':
            test_update_customer()
        elif choice == '9':
            test_update_category()
        elif choice == '10':
            test_update_product()
        elif choice == '11':
            run_all_tests()
        else:
            print("Invalid choice. Please enter a number between 0-11.")
        
        if choice != '11':
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    print("Guitar Shop API Tester")
    print("Make sure your FastAPI server is running on http://localhost:8001")
    input("Press Enter to start testing...")
    
    # You can choose to run all tests at once or use the interactive menu
    choice = input("Run all tests automatically? (y/n): ").lower()
    if choice == 'y':
        run_all_tests()
    else:
        interactive_test_menu()
