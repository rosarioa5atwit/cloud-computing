import requests
import time

BASE_URL = "http://localhost:8000"

def test_login_and_cookies():
    print("=== Testing Login and Cookie Setting ===")
    
    response = requests.get(f"{BASE_URL}/login?username=admin&password=password")
    print(f"Login Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print(f"Cookies: {dict(response.cookies)}")
    
    session = requests.Session()
    session.cookies.update(response.cookies)
    return session

def test_users_endpoint(session):
    print("\n=== Testing Users Endpoint with Cookies ===")
    
    response = session.get(f"{BASE_URL}/users/")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    print("\n--- Testing with Authorization Header ---")
    headers = {"Authorization": "Bearer valid-token"}
    response = requests.get(f"{BASE_URL}/users/", headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

def test_profile_with_headers(session):
    print("\n=== Testing Profile with Headers and Cookies ===")
    
    headers = {
        "User-ID": "test123",
        "X-Request-ID": "req-456",
        "Accept-Language": "es"
    }
    
    response = session.get(f"{BASE_URL}/profile/", headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print(f"Response Headers: {dict(response.headers)}")

def test_secure_api_with_rate_limiting():
    print("\n=== Testing Secure API with Rate Limiting ===")
    
    headers = {
        "X-API-Key": "admin-key-123",
        "X-Client-Version": "1.0.0",
        "User-Agent": "TestClient/1.0"
    }
    
    for i in range(5):
        response = requests.get(f"{BASE_URL}/api/secure", headers=headers)
        print(f"Request {i+1} - Status: {response.status_code}")
        print(f"Rate Limit Remaining: {response.headers.get('X-Rate-Limit-Remaining')}")
        time.sleep(0.5)

def test_preferences_cookies(session):
    print("\n=== Testing Preferences with Cookies ===")
    
    response = session.post(f"{BASE_URL}/preferences?language=fr&timezone=PST")
    print(f"Set Preferences Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print(f"New Cookies: {dict(response.cookies)}")
    
    response = session.get(f"{BASE_URL}/preferences")
    print(f"Get Preferences Status: {response.status_code}")
    print(f"Response: {response.json()}")

def test_logout_and_cookie_clearing(session):
    print("\n=== Testing Logout and Cookie Clearing ===")
    
    response = session.post(f"{BASE_URL}/logout")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    response = session.get(f"{BASE_URL}/users/")
    print(f"Users after logout - Status: {response.status_code}")

def test_invalid_credentials():
    print("\n=== Testing Invalid Credentials ===")
    
    response = requests.get(f"{BASE_URL}/login?username=wrong&password=wrong")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

def test_missing_headers():
    print("\n=== Testing Missing Required Headers ===")
    
    response = requests.get(f"{BASE_URL}/api/secure")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

def test_signup():
    print("\n=== Testing Signup ===")
    
    headers = {
        "User-Agent": "TestClient/1.0",
        "X-Forwarded-For": "192.168.1.100"
    }
    
    response = requests.post(
        f"{BASE_URL}/signup?username=testuser123&password=testpass123",
        headers=headers
    )
    print(f"Signup Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print(f"Cookies: {dict(response.cookies)}")

def run_all_tests():
    print("Starting Comprehensive Headers and Cookies Tests")
    print("="*60)
    
    try:
        response = requests.get(BASE_URL, timeout=5)
        print(f"Server connection: OK (Status: {response.status_code})")
    except requests.exceptions.ConnectionError:
        print("ERROR: Server not running! Start with: python main.py")
        return
    
    test_signup()
    session = test_login_and_cookies()
    test_users_endpoint(session)
    test_profile_with_headers(session)
    test_secure_api_with_rate_limiting()
    test_preferences_cookies(session)
    test_logout_and_cookie_clearing(session)
    test_invalid_credentials()
    test_missing_headers()
    
    print("\n" + "="*60)
    print("All tests completed!")

if __name__ == "__main__":
    run_all_tests()
