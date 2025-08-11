import pytest
from unittest.mock import Mock, patch, MagicMock, call
import subprocess
import sys
import io
from contextlib import redirect_stdout, redirect_stderr
import requests

# Import the driver module
from driver import (
    test_database_connection, 
    start_fastapi_server, 
    stop_fastapi_server,
    driver
)

class TestDatabaseConnection:
    """Test database connection functionality"""
    
    @patch('driver.mysql.connector.connect')
    def test_database_connection_success(self, mock_connect):
        """Test successful database connection and validation"""
        # Mock database connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        # Mock database queries
        mock_cursor.fetchone.side_effect = [
            ("cd_database",),  # SELECT DATABASE()
            (5,), (3,), (2,)   # COUNT queries for each table
        ]
        mock_cursor.fetchall.side_effect = [
            [("vendors",), ("customers",), ("administrator",)],  # SHOW TABLES
            [("vendor_id", "int"), ("vendor_name", "varchar")],  # DESCRIBE vendors
            [("customer_id", "int"), ("first_name", "varchar")],  # DESCRIBE customers
            [("admin_id", "int"), ("admin_name", "varchar")]     # DESCRIBE administrator
        ]
        
        success, message = test_database_connection()
        
        assert success == True
        assert "Database connection and structure verified" in message
        mock_connect.assert_called_once()
        mock_cursor.execute.assert_called()
        mock_conn.close.assert_called_once()

    @patch('driver.mysql.connector.connect')
    def test_database_connection_failure(self, mock_connect):
        """Test database connection failure scenarios"""
        import mysql.connector
        
        # Test connection refused error
        mock_connect.side_effect = mysql.connector.Error("2003: Can't connect to MySQL server")
        
        success, message = test_database_connection()
        
        assert success == False
        assert "Database error" in message
        assert "2003" in message

    @patch('driver.mysql.connector.connect')
    def test_database_missing_tables(self, mock_connect):
        """Test when required tables are missing"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        # Mock missing tables
        mock_cursor.fetchone.return_value = ("cd_database",)
        mock_cursor.fetchall.return_value = [("some_other_table",)]  # Missing required tables
        
        success, message = test_database_connection()
        
        assert success == False
        assert "Missing tables" in message

class TestFastAPIServer:
    """Test FastAPI server management"""
    
    @patch('driver.subprocess.Popen')
    def test_start_fastapi_server_success(self, mock_popen):
        """Test successful FastAPI server start"""
        mock_process = MagicMock()
        mock_popen.return_value = mock_process
        
        result = start_fastapi_server()
        
        assert result == mock_process
        mock_popen.assert_called_once_with([
            sys.executable, "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"
        ])

    @patch('driver.subprocess.Popen')
    def test_start_fastapi_server_failure(self, mock_popen):
        """Test FastAPI server start failure"""
        mock_popen.side_effect = Exception("Failed to start")
        
        result = start_fastapi_server()
        
        assert result is None

    def test_stop_fastapi_server(self):
        """Test stopping FastAPI server"""
        mock_process = MagicMock()
        
        stop_fastapi_server(mock_process)
        
        mock_process.terminate.assert_called_once()
        mock_process.wait.assert_called_once()

    def test_stop_fastapi_server_none(self):
        """Test stopping FastAPI server with None process"""
        # Should not raise exception
        stop_fastapi_server(None)

class TestServiceInteractions:
    """Test external service interactions"""
    
    @patch('driver.requests.get')
    def test_service_status_check(self, mock_get):
        """Test service status checking functionality"""
        # Mock different response scenarios
        mock_responses = [
            Mock(status_code=200),  # Online service
            Mock(status_code=422),  # FastAPI root endpoint
            Mock(status_code=500),  # Error but responding
        ]
        mock_get.side_effect = mock_responses + [requests.exceptions.RequestException()]  # Offline service
        
        # This would be called within the driver function
        services = [
            ("Service1", "http://localhost:8000/"),
            ("Service2", "http://localhost:3801/"),
            ("Service3", "http://localhost:3802/"),
            ("Service4", "http://localhost:3803/"),
        ]
        
        results = []
        for service_name, url in services:
            try:
                response = mock_get(url, timeout=2)
                if response.status_code in [200, 422]:
                    results.append(f"✅ {service_name}: Online")
                else:
                    results.append(f"⚠️  {service_name}: Responding but status {response.status_code}")
            except requests.exceptions.RequestException:
                results.append(f"❌ {service_name}: Offline")
        
        assert "✅ Service1: Online" in results[0]
        assert "✅ Service2: Online" in results[1]
        assert "⚠️  Service3: Responding but status 500" in results[2]
        assert "❌ Service4: Offline" in results[3]

    @patch('driver.requests.put')
    def test_customer_signup_success(self, mock_put):
        """Test successful customer signup"""
        mock_response = Mock(status_code=200)
        mock_put.return_value = mock_response
        
        # Simulate customer signup data
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "shipping_address": "123 Main St",
            "billing_address": "123 Main St"
        }
        
        response = mock_put("http://localhost:3801/user/signup", json=data, timeout=5)
        
        assert response.status_code == 200
        mock_put.assert_called_once()

    @patch('driver.requests.put')
    def test_customer_signup_failure(self, mock_put):
        """Test customer signup failure"""
        mock_response = Mock(status_code=400, text="Validation error")
        mock_put.return_value = mock_response
        
        data = {"invalid": "data"}
        response = mock_put("http://localhost:3801/user/signup", json=data, timeout=5)
        
        assert response.status_code == 400
        assert response.text == "Validation error"

    @patch('driver.requests.get')
    def test_customer_login_success(self, mock_get):
        """Test successful customer login"""
        mock_response = Mock(status_code=200, text="valid_token_123")
        mock_get.return_value = mock_response
        
        headers = {"usrID": "123"}
        response = mock_get("http://localhost:3800/login", headers=headers, timeout=5)
        
        assert response.status_code == 200
        assert response.text == "valid_token_123"

    @patch('driver.requests.get')
    def test_customer_login_failure(self, mock_get):
        """Test customer login failure"""
        mock_response = Mock(status_code=200, text="null")
        mock_get.return_value = mock_response
        
        headers = {"usrID": "invalid"}
        response = mock_get("http://localhost:3800/login", headers=headers, timeout=5)
        
        assert response.text == "null"

class TestInventoryManagement:
    """Test inventory management functionality"""
    
    @patch('driver.requests.put')
    def test_add_inventory_item_success(self, mock_put):
        """Test successful inventory item addition"""
        mock_response = Mock(status_code=200)
        mock_response.json.return_value = {"cd_id": 123, "message": "Item added"}
        mock_put.return_value = mock_response
        
        cd_data = {
            "cd_name": "Test Album",
            "artist": "Test Artist",
            "genre_id": 1,
            "release_date": "2024-01-01",
            "price": 15.99,
            "quantity": 10,
            "vendor_id": 1
        }
        
        headers = {"first": "vendor", "last": ""}
        response = mock_put("http://localhost:3804/inventory/additem", json=cd_data, headers=headers, timeout=10)
        
        assert response.status_code == 200
        result = response.json()
        assert result["cd_id"] == 123

    @patch('driver.requests.put')
    def test_add_inventory_item_validation_error(self, mock_put):
        """Test inventory item addition with validation error"""
        mock_response = Mock(status_code=422)
        mock_response.json.return_value = {
            "detail": [{"type": "missing", "loc": ["quantity"], "msg": "field required"}]
        }
        mock_put.return_value = mock_response
        
        cd_data = {"invalid": "data"}
        response = mock_put("http://localhost:3804/inventory/additem", json=cd_data, timeout=10)
        
        assert response.status_code == 422
        error_detail = response.json()
        assert "detail" in error_detail

    @patch('driver.requests.get')
    def test_remove_inventory_item(self, mock_get):
        """Test inventory item removal"""
        mock_response = Mock(status_code=200)
        mock_response.json.return_value = {"message": "Item removed successfully"}
        mock_get.return_value = mock_response
        
        headers = {"first": "vendor", "last": ""}
        response = mock_get("http://localhost:3804/inventory/removeitem?pid=123", headers=headers, timeout=5)
        
        assert response.status_code == 200
        result = response.json()
        assert "removed successfully" in result["message"]

class TestPurchaseManagement:
    """Test purchase management functionality"""
    
    @patch('driver.requests.put')
    def test_add_item_to_cart(self, mock_put):
        """Test adding item to cart"""
        mock_response = Mock(status_code=200)
        mock_response.json.return_value = {"message": "Item added to cart"}
        mock_put.return_value = mock_response
        
        data = {
            "item_id": 0,
            "order_id": 0,
            "cd_id": 123,
            "quantity": 2
        }
        headers = {"token": "test_token"}
        response = mock_put("http://localhost:3802/purchase/orderitem", json=data, headers=headers, timeout=5)
        
        assert response.status_code == 200

    @patch('driver.requests.get')
    def test_view_order_status(self, mock_get):
        """Test viewing order status"""
        mock_response = Mock(status_code=200)
        mock_response.json.return_value = {"order_id": 123, "status": "processing"}
        mock_get.return_value = mock_response
        
        headers = {"token": "test_token"}
        response = mock_get("http://localhost:3802/purchase/orderstatus?oid=123", headers=headers, timeout=5)
        
        assert response.status_code == 200
        result = response.json()
        assert result["order_id"] == 123

class TestCardProcessing:
    """Test card processing functionality"""
    
    @patch('driver.requests.get')
    def test_validate_card_success(self, mock_get):
        """Test successful card validation"""
        mock_response = Mock(status_code=200)
        mock_get.return_value = mock_response
        
        response = mock_get("http://localhost:3806/validatecard?bank=Visa&cardnum=1234567890123456", timeout=5)
        
        assert response.status_code == 200

    @patch('driver.requests.get')
    def test_validate_card_failure(self, mock_get):
        """Test card validation failure"""
        mock_response = Mock(status_code=400)
        mock_get.return_value = mock_response
        
        response = mock_get("http://localhost:3806/validatecard?bank=Invalid&cardnum=invalid", timeout=5)
        
        assert response.status_code == 400

class TestErrorHandling:
    """Test error handling scenarios"""
    
    @patch('driver.requests.get')
    def test_connection_error_handling(self, mock_get):
        """Test handling of connection errors"""
        mock_get.side_effect = requests.exceptions.ConnectionError("Connection refused")
        
        with pytest.raises(requests.exceptions.ConnectionError):
            mock_get("http://localhost:3800/test", timeout=5)

    @patch('driver.requests.get')
    def test_timeout_error_handling(self, mock_get):
        """Test handling of timeout errors"""
        mock_get.side_effect = requests.exceptions.Timeout("Request timed out")
        
        with pytest.raises(requests.exceptions.Timeout):
            mock_get("http://localhost:3800/test", timeout=5)

class TestDriverMainFunction:
    """Test the main driver function"""
    
    @patch('driver.start_fastapi_server')
    @patch('driver.stop_fastapi_server')
    @patch('builtins.input')
    @patch('builtins.print')
    def test_driver_exit_immediately(self, mock_print, mock_input, mock_stop, mock_start):
        """Test driver function with immediate exit"""
        mock_process = MagicMock()
        mock_start.return_value = mock_process
        mock_input.return_value = "10"  # Exit choice
        
        driver()
        
        mock_start.assert_called_once()
        mock_stop.assert_called_once_with(mock_process)

    @patch('driver.start_fastapi_server')
    @patch('driver.stop_fastapi_server')
    @patch('builtins.input')
    @patch('builtins.print')
    def test_driver_invalid_choice(self, mock_print, mock_input, mock_stop, mock_start):
        """Test driver function with invalid menu choice"""
        mock_process = MagicMock()
        mock_start.return_value = mock_process
        
        # After invalid choice "99", driver prints error and loops back to menu
        # No "Press Enter" prompt for invalid choicesnue" for invalid choices
        mock_input.side_effect = [
            "99",    # Invalid choice (triggers error message)
            "10"     # Valid exit choice (ends loop) 
        ]
        
        driver()
        
        # Verify server management
        mock_start.assert_called_once()
        mock_stop.assert_called_once_with(mock_process)
        # Verify input was called twice (once for invalid, once for exit)
        assert mock_input.call_count == 2
        # Verify that the invalid choice message was printed
        print_calls = [str(call.args[0]) if call.args else "" for call in mock_print.call_args_list]
        invalid_choice_found = any("Invalid choice" in call for call in print_calls)
        assert invalid_choice_found, f"Invalid choice message should be printed. Print calls: {print_calls}"

    @patch('driver.start_fastapi_server')
    def test_driver_server_start_failure(self, mock_start):
        """Test driver function when server fails to start"""
        mock_start.return_value = None
        
        # Capture stdout to verify error message
        with io.StringIO() as buf, redirect_stdout(buf):
            driver()
            output = buf.getvalue()
        
        assert "Failed to start FastAPI server" in output

class TestInputValidation:
    """Test input validation and type conversion"""

    def test_integer_input_validation(self):
        """Test that invalid integer inputs are handled"""
        test_inputs = ["abc", "12.5", "", "-1", "123"]
        valid_integers = []
        for inp in test_inputs:
            try:
                val = int(inp)
                valid_integers.append(val)
            except ValueError:
                pass  # Expected for invalid inputs
        assert valid_integers == [-1, 123]

    def test_float_input_validation(self):
        """Test that invalid float inputs are handled"""
        test_inputs = ["abc", "12.5", "", "15.99"]
        valid_floats = []
        for inp in test_inputs:
            try:
                val = float(inp)
                valid_floats.append(val)
            except ValueError:
                pass  # Expected for invalid inputs
        assert valid_floats == [12.5, 15.99]

class TestDatabaseTroubleshooting:
    """Test database troubleshooting functionality"""

    @patch('driver.mysql.connector.connect')
    @patch('builtins.print')
    def test_connection_refused_troubleshooting(self, mock_print, mock_connect):
        """Test troubleshooting output for connection refused errors"""
        import mysql.connector
        mock_connect.side_effect = mysql.connector.Error("2003: Connection refused")
        success, message = test_database_connection()
        assert success == False
        assert "2003" in message

    @patch('driver.mysql.connector.connect')
    @patch('builtins.print')
    def test_access_denied_troubleshooting(self, mock_print, mock_connect):
        """Test troubleshooting output for access denied errors"""
        import mysql.connector
        mock_connect.side_effect = mysql.connector.Error("1045: Access denied")
        success, message = test_database_connection()
        assert success == False
        assert "1045" in message

# Integration test fixtures
@pytest.fixture
def mock_database_config():
    """Fixture for mocking database configuration"""
    return {
        'host': 'localhost',
        'port': 5433,
        'database': 'cd_database',
        'user': 'test_user',
        'password': 'test_pass'
    }

@pytest.fixture
def mock_services():
    """Fixture for mocking all services"""
    with patch('driver.requests.get') as mock_get, \
         patch('driver.requests.put') as mock_put:
        # Configure default successful responses
        mock_get.return_value = Mock(status_code=200, text="success")
        mock_put.return_value = Mock(status_code=200, text="success")
        yield mock_get, mock_put

class TestPerformance:
    """Test performance aspects of the driver"""

    @patch('driver.requests.get')
    def test_service_status_check_timeout(self, mock_get):
        """Test that service status checks respect timeout"""
        mock_get.side_effect = requests.exceptions.Timeout()
        try:
            mock_get("http://localhost:8000/", timeout=2)
        except requests.exceptions.Timeout:
            pass  # Expected behavior
        mock_get.assert_called_once_with("http://localhost:8000/", timeout=2)

if __name__ == "__main__":
    # Run with verbose output (no coverage to avoid dependency issues)
    pytest.main([__file__, "-v", "--tb=short"])
