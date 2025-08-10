import requests
import time
from typing import Optional

class HeadersCookiesDriver:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
        
    def display_menu(self):
        print("\n" + "="*50)
        print("    HEADERS AND COOKIES LAB DRIVER")
        print("="*50)
        print("1. Signup (creates account)")
        print("2. Login (sets cookies)")
        print("3. Users endpoint (reads cookies)")
        print("4. Profile (headers + cookies)")
        print("5. Secure API (headers with rate limiting)")
        print("6. Set Preferences (POST with cookies)")
        print("7. Get Preferences (GET with cookies)")
        print("8. Logout (clears cookies)")
        print("9. Run All")
        print("10. Show Current Cookies")
        print("11. Custom Headers")
        print("0. Exit")
        print("="*50)

    def test_signup(self):
        print("\n--- Signup ---")
        
        username = input("Enter username: ").strip()
        password = input("Enter password (min 6 chars): ").strip()
        
        headers = {
            "User-Agent": "HeadersCookiesDriver/1.0",
            "X-Forwarded-For": "192.168.1.100"
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/signup",
                params={"username": username, "password": password},
                headers=headers
            )
            
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.json()}")
            print(f"Cookies Set: {dict(response.cookies)}")
            print(f"Response Headers: {dict(response.headers)}")
            
        except Exception as e:
            print(f"Error: {e}")

    def test_login(self):
        print("\n--- Login ---")
        
        username = input("Enter username (default: admin): ").strip() or "admin"
        password = input("Enter password (default: password): ").strip() or "password"
        
        headers = {
            "User-Agent": "HeadersCookiesDriver/1.0"
        }
        
        try:
            response = self.session.get(
                f"{self.base_url}/login",
                params={"username": username, "password": password},
                headers=headers
            )
            
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.json()}")
            print(f"Cookies Set: {dict(response.cookies)}")
            
        except Exception as e:
            print(f"Error: {e}")

    def test_users(self):
        print("\n--- Users Endpoint ---")
        
        try:
            response = self.session.get(f"{self.base_url}/users/")
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.json()}")
            
        except Exception as e:
            print(f"Cookie auth failed: {e}")
            
        print("\n--- with Authorization Header ---")
        try:
            headers = {"Authorization": "Bearer valid-token"}
            response = requests.get(f"{self.base_url}/users/", headers=headers)
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.json()}")
            
        except Exception as e:
            print(f"Header auth failed: {e}")

    def test_profile(self):
        print("\nProfile Endpoint")

        user_id = input("Enter User ID header (optional): ").strip()
        request_id = input("Enter Request ID (optional): ").strip()
        language = input("Enter Accept-Language (default: en): ").strip() or "en"
        
        headers = {}
        if user_id:
            headers["User-ID"] = user_id
        if request_id:
            headers["X-Request-ID"] = request_id
        headers["Accept-Language"] = language
        
        try:
            response = self.session.get(f"{self.base_url}/profile/", headers=headers)
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.json()}")
            print(f"Response Headers: {dict(response.headers)}")
            
        except Exception as e:
            print(f"Error: {e}")

    def test_secure_api(self):
        print("\n Secure API ")
        
        api_key = input("Enter API Key (admin-key-123 or user-key-456): ").strip()
        client_version = input("Enter Client Version (optional): ").strip()
        
        headers = {
            "X-API-Key": api_key,
            "User-Agent": "HeadersCookiesDriver/1.0"
        }
        
        if client_version:
            headers["X-Client-Version"] = client_version
        
        try:
            for i in range(3):
                response = requests.get(f"{self.base_url}/api/secure", headers=headers)
                print(f"Request {i+1} - Status: {response.status_code}")
                print(f"Response: {response.json()}")
                print(f"Rate Limit Headers: {response.headers.get('X-Rate-Limit-Remaining', 'N/A')} remaining")
                time.sleep(1)
                
        except Exception as e:
            print(f"Error: {e}")

    def test_set_preferences(self):
        print("\n Set Preferences")
        
        language = input("Enter language (default: en): ").strip() or "en"
        timezone = input("Enter timezone (default: UTC): ").strip() or "UTC"
        
        try:
            response = self.session.post(
                f"{self.base_url}/preferences",
                params={
                    "language": language,
                    "timezone": timezone
                }
            )
            
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.json()}")
            print(f"New Cookies: {dict(response.cookies)}")
            
        except Exception as e:
            print(f"Error: {e}")

    def test_get_preferences(self):
        print("\n  Get Preferences ")
        
        try:
            response = self.session.get(f"{self.base_url}/preferences")
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.json()}")
            
        except Exception as e:
            print(f"Error: {e}")

    def test_logout(self):
        print("\n  Logout ")
        
        try:
            response = self.session.post(f"{self.base_url}/logout")
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.json()}")
            print("Cookies cleared from session")
            
        except Exception as e:
            print(f"Error: {e}")

    def show_cookies(self):
        print("\n Current Session Cookies ")
        
        if self.session.cookies:
            for cookie in self.session.cookies:
                print(f"{cookie.name}: {cookie.value}")
        else:
            print("No cookies in session")

    def test_custom_headers(self):
        print("\n Custom Headers ")
        
        endpoint = input("Enter endpoint (e.g., /profile/): ").strip()
        header_name = input("Enter header name: ").strip()
        header_value = input("Enter header value: ").strip()
        
        if endpoint and header_name and header_value:
            headers = {header_name: header_value}
            
            try:
                response = self.session.get(f"{self.base_url}{endpoint}", headers=headers)
                print(f"Status Code: {response.status_code}")
                print(f"Response: {response.json()}")
                
            except Exception as e:
                print(f"Error: {e}")

    def run_all_tests(self):
        print("\n--- Running All Tests ---")
        
        print("1.  signup...")
        headers = {"User-Agent": "AutoTester/1.0", "X-Forwarded-For": "127.0.0.1"}
        response = self.session.post(
            f"{self.base_url}/signup",
            params={"username": "testuser", "password": "testpass123"},
            headers=headers
        )
        print(f"Signup Status: {response.status_code}")
        
        print("\n2. Logging in with default credentials...")
        headers = {"User-Agent": "AutoTester/1.0"}
        response = self.session.get(
            f"{self.base_url}/login",
            params={"username": "admin", "password": "password"},
            headers=headers
        )
        print(f"Login Status: {response.status_code}")
        
        print("\n3.  users endpoint...")
        response = self.session.get(f"{self.base_url}/users/")
        print(f"Users Status: {response.status_code}")
        
        print("\n4.  profile...")
        headers = {"User-ID": "123", "Accept-Language": "es"}
        response = self.session.get(f"{self.base_url}/profile/", headers=headers)
        print(f"Profile Status: {response.status_code}")
        
        print("\n5.  secure API...")
        headers = {"X-API-Key": "admin-key-123", "X-Client-Version": "2.0"}
        response = requests.get(f"{self.base_url}/api/secure", headers=headers)
        print(f"API Status: {response.status_code}")
        
        print("\n preferences...")
        response = self.session.post(
            f"{self.base_url}/preferences",
            params={"theme": "dark", "language": "fr"}
        )
        print(f"Set Preferences Status: {response.status_code}")
        
        response = self.session.get(f"{self.base_url}/preferences")
        print(f"Get Preferences Status: {response.status_code}")
        
        print("\nAll tests completed!")

    def run(self):
        print("Headers and Cookies Lab Driver")
        print("Make sure the FastAPI server is running on http://localhost:8000")
        
        try:
            response = requests.get(self.base_url, timeout=5)
            print(f"Server connection: OK (Status: {response.status_code})")
        except requests.exceptions.ConnectionError:
            print("\nERROR: Cannot connect to FastAPI server!")
            print("Please start the server first:")
            print("1. Open another terminal/command prompt")
            print("2. Navigate to the lab7 folder")
            print("3. Run: python main.py")
            print("4. Wait for 'Server is running at http://localhost:8000'")
            print("5. Then run this driver again")
            return
        except Exception as e:
            print(f"Connection error: {e}")
            return
        
        while True:
            self.display_menu()
            choice = input("\nEnter your choice (0-11): ").strip()
            
            try:
                if choice == '0':
                    break
                elif choice == '1':
                    self.test_signup()
                elif choice == '2':
                    self.test_login()
                elif choice == '3':
                    self.test_users()
                elif choice == '4':
                    self.test_profile()
                elif choice == '5':
                    self.test_secure_api()
                elif choice == '6':
                    self.test_set_preferences()
                elif choice == '7':
                    self.test_get_preferences()
                elif choice == '8':
                    self.test_logout()
                elif choice == '9':
                    self.run_all_tests()
                elif choice == '10':
                    self.show_cookies()
                elif choice == '11':
                    self.test_custom_headers()
                else:
                    print("Invalid choice. Please enter 0-11.")
                    
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Unexpected error: {e}")
            
            if choice != '9':
                input("\nPress Enter to continue...")

if __name__ == "__main__":
    driver = HeadersCookiesDriver()
    driver.run()
    driver.run()
