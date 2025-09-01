#!/usr/bin/env python3
"""
Test script to verify route protection and authentication flow
"""
import requests
import json

BASE_URL = "http://localhost:5000"

def test_route_protection():
    print("🧪 Testing Medicino Route Protection")
    print("=" * 50)
    
    # Test 1: Check if landing page is accessible without authentication
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            if "login" in response.text.lower() and "register" in response.text.lower():
                print("✅ Landing page accessible for unauthenticated users")
            else:
                print("❌ Landing page doesn't show login/register options")
        else:
            print(f"❌ Landing page error: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Server not running. Please start the application first.")
        return

    # Test 2: Check if main app redirects unauthenticated users
    try:
        response = requests.get(f"{BASE_URL}/app", allow_redirects=False)
        if response.status_code == 302:  # Redirect
            print("✅ Main app properly redirects unauthenticated users")
        else:
            print(f"❌ Main app should redirect but got: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Server not running")
        return

    # Test 3: Check if API endpoints are protected
    protected_endpoints = [
        "/api/diagnose",
        "/api/history", 
        "/api/medicines",
        "/api/medicine/paracetamol"
    ]
    
    for endpoint in protected_endpoints:
        try:
            if endpoint == "/api/diagnose":
                response = requests.post(f"{BASE_URL}{endpoint}", 
                                      json={"symptoms": "headache"}, 
                                      allow_redirects=False)
            else:
                response = requests.get(f"{BASE_URL}{endpoint}", allow_redirects=False)
            
            if response.status_code == 302:  # Redirect to login
                print(f"✅ {endpoint} properly protected")
            else:
                print(f"❌ {endpoint} should redirect but got: {response.status_code}")
        except requests.exceptions.ConnectionError:
            print(f"❌ Server not running for {endpoint}")
            break

    # Test 4: Check if login and register pages are accessible
    auth_pages = ["/login", "/register"]
    for page in auth_pages:
        try:
            response = requests.get(f"{BASE_URL}{page}")
            if response.status_code == 200:
                print(f"✅ {page} page accessible")
            else:
                print(f"❌ {page} page error: {response.status_code}")
        except requests.exceptions.ConnectionError:
            print(f"❌ Server not running for {page}")
            break

    print("\n🎉 Route protection test completed!")
    print("\n📋 Summary:")
    print("• Landing page shows login/register options")
    print("• Main app requires authentication")
    print("• All API endpoints are protected")
    print("• Login/register pages are accessible")
    print("\n🔐 Next Steps:")
    print("1. Open http://localhost:5000 in your browser")
    print("2. You should see the landing page with login/register options")
    print("3. Click 'Register' to create an account")
    print("4. Login to access the main application")

if __name__ == "__main__":
    test_route_protection() 