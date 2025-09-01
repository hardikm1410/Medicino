import requests
import json
import time

# Configuration
FLASK_BASE_URL = "http://localhost:5000"
DJANGO_BASE_URL = "http://localhost:8000"

def test_flask_api():
    """Test Flask API endpoints"""
    print("🧪 Testing Flask API...")
    print("=" * 50)

    # Test 1: Diagnosis API
    print("1. Testing Diagnosis API")
    diagnosis_data = {
        "symptoms": "fever, sore throat, headache, body ache, cold, vommiting,"
    }

    try:
        response = requests.post(f"{FLASK_BASE_URL}/api/diagnose",
                               json=diagnosis_data,
                               timeout=10)
        if response.status_code == 200:
            result = response.json()
            print("✅ Diagnosis API working")
            print(f"   Diagnosed: {result['data']['disease']}")
            print(f"   Confidence: {result['data']['confidence']}%")
            print(f"   Severity: {result['data']['severity']}")
        else:
            print(f"❌ Diagnosis API failed: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error: {e}")

    print()

    # Test 2: Medicine Search API
    print("2. Testing Medicine Search API")
    try:
        response = requests.get(f"{FLASK_BASE_URL}/api/medicine/Paracetamol", timeout=10)
        if response.status_code == 200:
            result = response.json()
            if result['success']:
                print("✅ Medicine Search API working")
                print(f"   Medicine: {result['data']['name']}")
                print(f"   Price: ₹{result['data']['price']}")
            else:
                print("❌ Medicine not found")
        else:
            print(f"❌ Medicine API failed: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error: {e}")

    print()

    # Test 3: List All Medicines API
    print("3. Testing List Medicines API")
    try:
        response = requests.get(f"{FLASK_BASE_URL}/api/medicines", timeout=10)
        if response.status_code == 200:
            result = response.json()
            print("✅ List Medicines API working")
            print(f"   Total medicines: {len(result['data'])}")
            print("   Sample medicines:")
            for medicine in result['data'][:3]:
                print(f"   - {medicine['name']} (₹{medicine['price']})")
        else:
            print(f"❌ List Medicines API failed: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error: {e}")

    print()

    # Test 4: History API
    print("4. Testing History API")
    try:
        response = requests.get(f"{FLASK_BASE_URL}/api/history", timeout=10)
        if response.status_code == 200:
            result = response.json()
            print("✅ History API working")
            print(f"   Total records: {len(result['data'])}")
        else:
            print(f"❌ History API failed: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error: {e}")

def test_django_api():
    """Test Django API endpoints"""
    print("\n🧪 Testing Django API...")
    print("=" * 50)

    # Test 1: Diagnosis API
    print("1. Testing Diagnosis API")
    diagnosis_data = {
        "symptoms": "sneezing, runny nose, congestion"
    }

    try:
        response = requests.post(f"{DJANGO_BASE_URL}/api/diagnose/",
                               json=diagnosis_data,
                               timeout=10)
        if response.status_code == 200:
            result = response.json()
            print("✅ Diagnosis API working")
            print(f"   Diagnosed: {result['data']['disease']}")
            print(f"   Confidence: {result['data']['confidence']}%")
        else:
            print(f"❌ Diagnosis API failed: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error: {e}")

    print()

    # Test 2: Medicine Search API
    print("2. Testing Medicine Search API")
    try:
        response = requests.get(f"{DJANGO_BASE_URL}/api/medicine/Ibuprofen/", timeout=10)
        if response.status_code == 200:
            result = response.json()
            if result['success']:
                print("✅ Medicine Search API working")
                print(f"   Medicine: {result['data']['name']}")
                print(f"   Category: {result['data']['category']}")
            else:
                print("❌ Medicine not found")
        else:
            print(f"❌ Medicine API failed: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error: {e}")

def performance_test():
    """Test API performance"""
    print("\n⚡ Performance Testing...")
    print("=" * 50)

    test_cases = [
        "fever, headache",
        "cough, cold",
        "stomach pain, nausea",
        "allergic reaction, itching",
        "migraine, sensitivity to light"
    ]

    total_time = 0
    successful_requests = 0

    for i, symptoms in enumerate(test_cases, 1):
        start_time = time.time()
        try:
            response = requests.post(f"{FLASK_BASE_URL}/api/diagnose",
                                   json={"symptoms": symptoms},
                                   timeout=5)
            end_time = time.time()

            if response.status_code == 200:
                response_time = end_time - start_time
                total_time += response_time
                successful_requests += 1
                result = response.json()
                print(f"   Test {i}: ✅ {response_time:.3f}s - {result['data']['disease']}")
            else:
                print(f"   Test {i}: ❌ Failed ({response.status_code})")
        except requests.exceptions.RequestException:
            print(f"   Test {i}: ❌ Timeout/Connection Error")

    if successful_requests > 0:
        avg_time = total_time / successful_requests
        print(f"\n📊 Performance Summary:")
        print(f"   Successful requests: {successful_requests}/{len(test_cases)}")
        print(f"   Average response time: {avg_time:.3f}s")
        print(f"   Total time: {total_time:.3f}s")

def test_error_handling():
    """Test API error handling"""
    print("\n🛡️ Testing Error Handling...")
    print("=" * 50)

    # Test empty symptoms
    print("1. Testing empty symptoms")
    try:
        response = requests.post(f"{FLASK_BASE_URL}/api/diagnose",
                               json={"symptoms": ""},
                               timeout=5)
        if response.status_code == 200:
            result = response.json()
            if not result['success']:
                print("✅ Empty symptoms handled correctly")
            else:
                print("❌ Empty symptoms not handled properly")
        else:
            print(f"❌ Unexpected status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error: {e}")

    # Test invalid medicine search
    print("\n2. Testing invalid medicine search")
    try:
        response = requests.get(f"{FLASK_BASE_URL}/api/medicine/NonExistentMedicine", timeout=5)
        if response.status_code == 200:
            result = response.json()
            if not result['success']:
                print("✅ Invalid medicine search handled correctly")
            else:
                print("❌ Invalid medicine search not handled properly")
        else:
            print(f"❌ Unexpected status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error: {e}")

    # Test malformed JSON
    print("\n3. Testing malformed request")
    try:
        response = requests.post(f"{FLASK_BASE_URL}/api/diagnose",
                               data="invalid json",
                               headers={'Content-Type': 'application/json'},
                               timeout=5)
        if response.status_code in [400, 500]:
            print("✅ Malformed JSON handled correctly")
        else:
            print(f"❌ Unexpected handling of malformed JSON: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Connection error: {e}")

def main():
    """Main testing function"""
    print("🏥 MEDICINO API TESTING SUITE")
    print("=" * 50)
    print("Make sure your Flask server is running on http://localhost:5000")
    print("Make sure your Django server is running on http://localhost:8000")
    print("=" * 50)

    # Test Flask API
    test_flask_api()

    # Test Django API (uncomment if Django server is running)
    # test_django_api()

    # Performance testing
    performance_test()

    # Error handling testing
    test_error_handling()

    print("\n🎉 Testing completed!")
    print("\nTo run the Flask server: python app.py")
    print("To run the Django server: python manage.py runserver")
    print("To setup database: python database_setup.py")

if __name__ == "__main__":
    main()
