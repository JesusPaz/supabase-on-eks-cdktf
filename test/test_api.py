#!/usr/bin/env python3
"""
Simple Supabase API Test Script
- Create a test user
- List all users  
- Verify the created user exists
"""

import os
import requests
import json
import time
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
SUPABASE_URL = os.getenv('SUPABASE_URL')
ANON_KEY = os.getenv('anonKey')
SERVICE_KEY = os.getenv('serviceKey')

print("🚀 Starting Supabase API Tests")
print(f"URL: {SUPABASE_URL}")
print(f"Anon Key: {ANON_KEY[:20]}...")
print(f"Service Key: {SERVICE_KEY[:20]}...")
print("-" * 50)

def test_auth_health():
    """Test 1: Check if Auth service is working"""
    print("🔍 Test 1: Checking Auth health...")
    
    try:
        url = f"{SUPABASE_URL}/auth/v1/health"
        headers = {
            'apikey': ANON_KEY,
            'Content-Type': 'application/json'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Auth service is working")
            return True
        else:
            print(f"❌ Auth failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error connecting to Auth: {e}")
        return False

def test_postgrest_health():
    """Test 2: Check if PostgREST is working"""
    print("\n🔍 Test 2: Checking PostgREST health...")
    
    try:
        url = f"{SUPABASE_URL}/rest/v1/"
        headers = {
            'apikey': ANON_KEY,
            'Content-Type': 'application/json'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ PostgREST is working")
            return True
        else:
            print(f"❌ PostgREST failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error connecting to PostgREST: {e}")
        return False

def create_test_table():
    """Test 2.1: Create a test table for CRUD operations"""
    print("\n🔍 Test 2.1: Creating test table...")
    
    try:
        # First check if table exists
        check_url = f"{SUPABASE_URL}/rest/v1/test_items?limit=1"
        headers = {
            'apikey': SERVICE_KEY,
            'Authorization': f'Bearer {SERVICE_KEY}',
            'Content-Type': 'application/json'
        }
        
        check_response = requests.get(check_url, headers=headers, timeout=10)
        
        if check_response.status_code == 200:
            print("✅ test_items table already exists")
            return True
        elif check_response.status_code == 404:
            print("📝 test_items table doesn't exist, creating via SQL...")
            
            # Create table using PostgREST SQL function
            sql_url = f"{SUPABASE_URL}/rest/v1/rpc/exec_sql"
            sql_data = {
                "sql": "CREATE TABLE IF NOT EXISTS test_items (id SERIAL PRIMARY KEY, name TEXT, description TEXT, created_at TIMESTAMP DEFAULT NOW()); GRANT ALL ON test_items TO anon, authenticated, service_role;"
            }
            
            sql_response = requests.post(sql_url, headers=headers, json=sql_data, timeout=10)
            
            if sql_response.status_code in [200, 201]:
                print("✅ test_items table created successfully")
                return True
            else:
                print(f"⚠️  Could not create table via RPC: {sql_response.text}")
                print("💡 Table will be created manually if needed")
                # Try to continue anyway - table might exist but not be accessible via REST
                return True
        else:
            print(f"⚠️  Unexpected response checking table: {check_response.text}")
            # Assume table exists and continue
            return True
            
    except Exception as e:
        print(f"❌ Error checking/creating table: {e}")
        # Don't fail completely - continue with tests
        return True

def test_postgrest_create():
    """Test 2.2: Create (INSERT) test data via PostgREST"""
    print("\n🔍 Test 2.2: Creating test data via PostgREST...")
    
    try:
        timestamp = int(time.time())
        url = f"{SUPABASE_URL}/rest/v1/test_items"
        headers = {
            'apikey': SERVICE_KEY,
            'Authorization': f'Bearer {SERVICE_KEY}',
            'Content-Type': 'application/json',
            'Prefer': 'return=representation'
        }
        
        data = {
            "name": f"Test Item {timestamp}",
            "description": f"Test description created at {datetime.now()}"
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code in [200, 201]:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                item_id = result[0].get('id')
                print(f"✅ Test item created successfully")
                print(f"   ID: {item_id}")
                print(f"   Name: {result[0].get('name')}")
                return item_id
            else:
                print(f"✅ Item created but no data returned")
                return True
        else:
            print(f"❌ Error creating item: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error creating item: {e}")
        return None

def test_postgrest_read():
    """Test 2.3: Read (SELECT) data via PostgREST"""
    print("\n🔍 Test 2.3: Reading data via PostgREST...")
    
    try:
        url = f"{SUPABASE_URL}/rest/v1/test_items?limit=5"
        headers = {
            'apikey': SERVICE_KEY,
            'Authorization': f'Bearer {SERVICE_KEY}',
            'Content-Type': 'application/json'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            items = response.json()
            print(f"✅ Items found: {len(items)}")
            
            for i, item in enumerate(items[:3]):  # Show first 3
                item_id = item.get('id', 'No ID')
                name = item.get('name', 'No name')
                created_at = item.get('created_at', 'Unknown')
                print(f"   {i+1}. {name} (ID: {item_id}) - {created_at}")
            
            if len(items) > 3:
                print(f"   ... and {len(items) - 3} more items")
                
            return items
        else:
            print(f"❌ Error reading items: {response.text}")
            return []
            
    except Exception as e:
        print(f"❌ Error reading items: {e}")
        return []

def test_postgrest_update(item_id):
    """Test 2.4: Update (PATCH) data via PostgREST"""
    if not item_id:
        print("\n🔍 Test 2.4: Skipping update test (no item created)")
        return False
        
    print(f"\n🔍 Test 2.4: Updating item {item_id} via PostgREST...")
    
    try:
        url = f"{SUPABASE_URL}/rest/v1/test_items?id=eq.{item_id}"
        headers = {
            'apikey': SERVICE_KEY,
            'Authorization': f'Bearer {SERVICE_KEY}',
            'Content-Type': 'application/json',
            'Prefer': 'return=representation'
        }
        
        data = {
            "description": f"Updated description at {datetime.now()}"
        }
        
        response = requests.patch(url, headers=headers, json=data, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code in [200, 204]:
            print(f"✅ Item updated successfully")
            return True
        else:
            print(f"❌ Error updating item: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error updating item: {e}")
        return False

def test_postgrest_delete(item_id):
    """Test 2.5: Delete data via PostgREST"""
    if not item_id:
        print("\n🔍 Test 2.5: Skipping delete test (no item created)")
        return False
        
    print(f"\n🔍 Test 2.5: Deleting item {item_id} via PostgREST...")
    
    try:
        url = f"{SUPABASE_URL}/rest/v1/test_items?id=eq.{item_id}"
        headers = {
            'apikey': SERVICE_KEY,
            'Authorization': f'Bearer {SERVICE_KEY}',
            'Content-Type': 'application/json'
        }
        
        response = requests.delete(url, headers=headers, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code in [200, 204]:
            print(f"✅ Item deleted successfully")
            return True
        else:
            print(f"❌ Error deleting item: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error deleting item: {e}")
        return False

def create_test_user():
    """Test 3: Create a test user"""
    print("\n🔍 Test 3: Creating test user...")
    
    # Generate unique email with timestamp
    timestamp = int(time.time())
    test_email = f"test-user-{timestamp}@example.com"
    test_password = "TestPassword123!"
    
    try:
        url = f"{SUPABASE_URL}/auth/v1/signup"
        headers = {
            'apikey': ANON_KEY,
            'Content-Type': 'application/json'
        }
        
        data = {
            "email": test_email,
            "password": test_password
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code in [200, 201]:
            result = response.json()
            user_id = result.get('user', {}).get('id')
            print(f"✅ User created successfully")
            print(f"   Email: {test_email}")
            print(f"   ID: {user_id}")
            return user_id, test_email
        else:
            print(f"❌ Error creating user: {response.text}")
            return None, test_email
            
    except Exception as e:
        print(f"❌ Error creating user: {e}")
        return None, test_email

def list_users():
    """Test 4: List users using Service Key"""
    print("\n🔍 Test 4: Listing users (requires Service Key)...")
    
    try:
        url = f"{SUPABASE_URL}/auth/v1/admin/users"
        headers = {
            'apikey': SERVICE_KEY,
            'Authorization': f'Bearer {SERVICE_KEY}',
            'Content-Type': 'application/json'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            users = result.get('users', [])
            print(f"✅ Users found: {len(users)}")
            
            for i, user in enumerate(users[:5]):  # Show only first 5
                email = user.get('email', 'No email')
                user_id = user.get('id', 'No ID')
                created_at = user.get('created_at', 'Unknown')
                print(f"   {i+1}. {email} (ID: {user_id[:8]}...) - {created_at}")
            
            if len(users) > 5:
                print(f"   ... and {len(users) - 5} more users")
                
            return users
        else:
            print(f"❌ Error listing users: {response.text}")
            return []
            
    except Exception as e:
        print(f"❌ Error listing users: {e}")
        return []

def verify_user_exists(users, test_email):
    """Test 5: Verify the created user exists in the list"""
    print(f"\n🔍 Test 5: Verifying user {test_email} exists...")
    
    for user in users:
        if user.get('email') == test_email:
            print(f"✅ User found in list")
            print(f"   Email: {user.get('email')}")
            print(f"   ID: {user.get('id')}")
            print(f"   Created: {user.get('created_at')}")
            return True
    
    print(f"❌ User {test_email} NOT found in list")
    return False

def test_storage_health():
    """Test 6: Check Storage service health"""
    print("\n🔍 Test 6: Checking Storage health...")
    
    try:
        url = f"{SUPABASE_URL}/storage/v1/status"
        headers = {
            'apikey': ANON_KEY,
            'Content-Type': 'application/json'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Storage service is working")
            return True
        else:
            print(f"❌ Storage failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error connecting to Storage: {e}")
        return False

def create_storage_bucket():
    """Create test bucket if it doesn't exist"""
    print("\n🔍 Creating test bucket if needed...")
    
    try:
        # First check if bucket exists
        url = f"{SUPABASE_URL}/storage/v1/bucket"
        headers = {
            'apikey': SERVICE_KEY,
            'Authorization': f'Bearer {SERVICE_KEY}',
            'Content-Type': 'application/json'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            buckets = response.json()
            bucket_names = [bucket.get('name') for bucket in buckets]
            
            if 'test-bucket' in bucket_names:
                print("✅ test-bucket already exists")
                return True
        
        # Create bucket if it doesn't exist
        print("📝 Creating test-bucket...")
        create_data = {
            "id": "test-bucket",
            "name": "test-bucket",
            "public": False
        }
        
        create_response = requests.post(url, headers=headers, json=create_data, timeout=10)
        print(f"Create Status: {create_response.status_code}")
        
        if create_response.status_code in [200, 201]:
            print("✅ test-bucket created successfully")
            return True
        else:
            print(f"❌ Error creating bucket: {create_response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error managing bucket: {e}")
        return False

def test_storage_upload():
    """Test 7: Upload a test file to Storage"""
    print("\n🔍 Test 7: Testing file upload...")
    
    try:
        # Create a simple test file
        test_content = f"Test file created at {datetime.now()}"
        timestamp = int(time.time())
        filename = f"test-file-{timestamp}.txt"
        
        url = f"{SUPABASE_URL}/storage/v1/object/test-bucket/{filename}"
        headers = {
            'apikey': SERVICE_KEY,
            'Authorization': f'Bearer {SERVICE_KEY}',
            'Content-Type': 'text/plain'
        }
        
        response = requests.post(url, headers=headers, data=test_content, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code in [200, 201]:
            print(f"✅ File uploaded successfully")
            print(f"   Filename: {filename}")
            return filename
        else:
            print(f"❌ Error uploading file: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error uploading file: {e}")
        return None

def test_storage_list():
    """Test 8: List files in Storage"""
    print("\n🔍 Test 8: Listing files in Storage...")
    
    try:
        url = f"{SUPABASE_URL}/storage/v1/object/list/test-bucket"
        headers = {
            'apikey': SERVICE_KEY,
            'Authorization': f'Bearer {SERVICE_KEY}',
            'Content-Type': 'application/json'
        }
        
        # Include required prefix property
        data = {
            "prefix": "",
            "limit": 100,
            "offset": 0
        }
        
        response = requests.post(url, headers=headers, json=data, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            files = response.json()
            print(f"✅ Files found: {len(files)}")
            
            for i, file in enumerate(files[:3]):  # Show only first 3
                name = file.get('name', 'Unknown')
                size = file.get('metadata', {}).get('size', 'Unknown')
                print(f"   {i+1}. {name} ({size} bytes)")
            
            if len(files) > 3:
                print(f"   ... and {len(files) - 3} more files")
                
            return files
        else:
            print(f"❌ Error listing files: {response.text}")
            return []
            
    except Exception as e:
        print(f"❌ Error listing files: {e}")
        return []

def test_storage_download(filename):
    """Test 9: Download a file from Storage"""
    if not filename:
        print("\n🔍 Test 9: Skipping download test (no file uploaded)")
        return False
        
    print(f"\n🔍 Test 9: Downloading file {filename}...")
    
    try:
        url = f"{SUPABASE_URL}/storage/v1/object/test-bucket/{filename}"
        headers = {
            'apikey': SERVICE_KEY,
            'Authorization': f'Bearer {SERVICE_KEY}'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            content = response.text
            print(f"✅ File downloaded successfully")
            print(f"   Content preview: {content[:50]}...")
            return True
        else:
            print(f"❌ Error downloading file: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error downloading file: {e}")
        return False

def test_realtime_connection():
    """Test 10: Check Realtime connection"""
    print("\n🔍 Test 10: Checking Realtime connection...")
    
    try:
        # Test WebSocket endpoint
        url = f"{SUPABASE_URL}/realtime/v1/websocket"
        headers = {
            'apikey': ANON_KEY,
        }
        
        # Just do a GET to see if endpoint responds
        response = requests.get(url, headers=headers, timeout=5)
        print(f"Status: {response.status_code}")
        
        # For WebSocket, 400 or similar can be normal
        if response.status_code in [400, 426]:  # 426 = Upgrade Required
            print("✅ Realtime endpoint responds (WebSocket upgrade required)")
            return True
        elif response.status_code == 200:
            print("✅ Realtime endpoint responds")
            return True
        else:
            print(f"⚠️  Realtime unexpected response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error connecting to Realtime: {e}")
        return False

def main():
    """Run all tests"""
    print(f"⏰ Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Counters
    tests_passed = 0
    tests_total = 14
    
    # Test 1: Auth Health
    if test_auth_health():
        tests_passed += 1
    
    # Test 2: PostgREST Health  
    if test_postgrest_health():
        tests_passed += 1
    
    # Test 2.1: Create test table (prerequisite for CRUD)
    table_exists = create_test_table()
    
    # Test 2.2-2.5: PostgREST CRUD operations
    item_id = None
    if table_exists:
        # Test 2.2: Create item
        item_id = test_postgrest_create()
        if item_id:
            tests_passed += 1
        
        # Test 2.3: Read items
        items = test_postgrest_read()
        if items:
            tests_passed += 1
        
        # Test 2.4: Update item
        if test_postgrest_update(item_id):
            tests_passed += 1
        
        # Test 2.5: Delete item
        if test_postgrest_delete(item_id):
            tests_passed += 1
    else:
        print("⚠️  Skipping PostgREST CRUD tests (table doesn't exist)")
    
    # Test 3: Create user
    user_id, test_email = create_test_user()
    if user_id:
        tests_passed += 1
    
    # Test 4: List users
    users = list_users()
    if users:
        tests_passed += 1
    
    # Test 5: Verify user exists
    if user_id and users and verify_user_exists(users, test_email):
        tests_passed += 1
    
    # Test 6: Storage Health
    if test_storage_health():
        tests_passed += 1
    
    # Test 6.5: Create Storage Bucket (prerequisite)
    bucket_created = create_storage_bucket()
    
    # Test 7: Storage Upload
    uploaded_filename = None
    if bucket_created:
        uploaded_filename = test_storage_upload()
        if uploaded_filename:
            tests_passed += 1
    else:
        print("⚠️  Skipping upload test (bucket creation failed)")
    
    # Test 8: Storage List
    files = test_storage_list()
    if files:
        tests_passed += 1
    
    # Test 9: Storage Download
    if test_storage_download(uploaded_filename):
        tests_passed += 1
    
    # Test 10: Realtime
    if test_realtime_connection():
        tests_passed += 1
    
    # Final summary
    print("\n" + "="*50)
    print("📊 TEST SUMMARY")
    print("="*50)
    print(f"✅ Tests passed: {tests_passed}/{tests_total}")
    print(f"❌ Tests failed: {tests_total - tests_passed}/{tests_total}")
    
    if tests_passed == tests_total:
        print("🎉 ALL TESTS PASSED! Supabase is working correctly")
    elif tests_passed >= tests_total * 0.7:  # 70%
        print("⚠️  Most tests passed, but there are some issues")
    else:
        print("🚨 Many tests failed, check Supabase configuration")
    
    print(f"⏰ Finished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
