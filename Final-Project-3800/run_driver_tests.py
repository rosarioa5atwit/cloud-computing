#!/usr/bin/env python3
"""
Test runner for driver.py tests
Handles missing dependencies gracefully
"""

import subprocess
import sys
import os
from pathlib import Path

def check_and_install_pytest():
    """Check if pytest is available and install if needed"""
    try:
        import pytest
        print(f"✅ pytest is available (version: {pytest.__version__})")
        return True
    except ImportError:
        print("❌ pytest not found, installing...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "pytest"], check=True)
            print("✅ pytest installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install pytest")
            return False

def run_driver_tests():
    """Run all driver tests with error handling"""
    
    # Get the project directory
    project_dir = Path(__file__).parent
    
    print("🧪 Running Driver Tests...")
    print("=" * 50)
    print(f"📁 Project Directory: {project_dir}")
    print(f"🔍 Test File: test_driver.py")
    print("=" * 50)
    
    # Check pytest availability
    if not check_and_install_pytest():
        print("❌ Cannot run tests without pytest")
        return 1
    
    # Basic test configuration (no coverage)
    test_args = [
        str(project_dir / "test_driver.py"),
        "-v",  # Verbose output
        "--tb=short",  # Short traceback format
    ]
    
    # Try to import pytest and run tests
    try:
        import pytest
        print("🚀 Starting tests...")
        exit_code = pytest.main(test_args)
        
        print("\n" + "=" * 50)
        if exit_code == 0:
            print("✅ All tests passed!")
        else:
            print("❌ Some tests failed!")
            print(f"Exit code: {exit_code}")
        
        print("=" * 50)
        return exit_code
        
    except ImportError:
        print("❌ Could not import pytest after installation")
        return 1
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(run_driver_tests())
