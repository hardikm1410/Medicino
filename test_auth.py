#!/usr/bin/env python3
"""
Test script for authentication functionality
"""

import requests
import json

BASE_URL = "http://localhost:5000"

def test_authentication():
    """Test the authentication system."""
    print("🧪 Testing Medicino Authentication System")
    print("=" * 50)
    
    # Test 1: Check if login page is accessible
    try:
        response = requests.get(f"{BASE_URL}/login")
        if response.status_code == 200:
            print("✅ Login page accessible")
        else:
            print(f"❌ Login page error: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Server not running. Please start the application first.")
        return
    
    # Test 2: Check if register page is accessible
    try:
        response = requests.get(f"{BASE_URL}/register")
        if response.status_code == 200:
            print("✅ Register page accessible")
        else:
            print(f"❌ Register page error: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Server not running")
        return
    
    # Test 3: Check if main page shows authentication buttons
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            if "login" in response.text.lower() and "register" in response.text.lower():
                print("✅ Main page shows authentication buttons")
            else:
                print("❌ Authentication buttons not found on main page")
        else:
            print(f"❌ Main page error: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Server not running")
        return
    
    print("\n🎉 Authentication system test completed!")
    print("\n📋 Next Steps:")
    print("1. Open http://localhost:5000 in your browser")
    print("2. Click 'Register' to create a new account")
    print("3. Login with your credentials")
    print("4. Test the symptom diagnosis feature")

if __name__ == "__main__":
    test_authentication() 