# Supabase API Tests

Simple Python script to test Supabase API functionality.

## What it tests

- ✅ **Auth service** - Health check
- ✅ **PostgREST** - Database API health + Full CRUD operations
- ✅ **User creation** - Create test user
- ✅ **User listing** - List all users
- ✅ **User verification** - Verify created user exists
- ✅ **Storage service** - Health check + Full file operations
- ✅ **File upload** - Upload test file to Storage
- ✅ **File listing** - List files in Storage
- ✅ **File download** - Download uploaded file
- ✅ **Realtime** - WebSocket connection

## How to run

### Option 1: Using Makefile (recommended)
```bash
make all        # Install + Test (uses virtual environment)
# OR step by step:
make install    # Create venv and install dependencies
make test       # Run tests (creates table automatically)
make clean      # Remove virtual environment
```

### Option 2: Manual
1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the test:**
   ```bash
   python test_api.py
   ```

## Configuration

The script uses JWT tokens from `.env` file:
- `SUPABASE_URL` - Your Supabase instance URL
- `anonKey` - Anonymous access key
- `serviceKey` - Service role key (admin access)

## Expected output

```
🚀 Starting Supabase API Tests
✅ Tests passed: 14/14
🎉 ALL TESTS PASSED! Supabase is working correctly
```

## What each test does

1. **Auth Health** - `GET /auth/v1/health`
2. **PostgREST Health** - `GET /rest/v1/`
3. **Create Table** - Check/create `test_items` table
4. **PostgREST CREATE** - `POST /rest/v1/test_items` (INSERT)
5. **PostgREST READ** - `GET /rest/v1/test_items` (SELECT)
6. **PostgREST UPDATE** - `PATCH /rest/v1/test_items?id=eq.{id}` 
7. **PostgREST DELETE** - `DELETE /rest/v1/test_items?id=eq.{id}`
8. **Create User** - `POST /auth/v1/signup`
9. **List Users** - `GET /auth/v1/admin/users`
10. **Verify User** - Check user exists in list
11. **Storage Health** - `GET /storage/v1/status`
12. **Create Bucket** - `POST /storage/v1/bucket` (private bucket)
13. **File Upload** - `POST /storage/v1/object/test-bucket/{file}`
14. **File Listing** - `POST /storage/v1/object/list/test-bucket`
15. **File Download** - `GET /storage/v1/object/test-bucket/{file}`
16. **Realtime** - `GET /realtime/v1/websocket`

## CRUD Operations Tested

### PostgREST Database CRUD
- **CREATE** - Insert new items into `test_items` table
- **READ** - Query and list items from database  
- **UPDATE** - Modify existing items
- **DELETE** - Remove items from database

### Storage File CRUD
- **CREATE** - Upload files to private S3 bucket
- **READ** - Download and verify file contents
- **LIST** - Browse files in bucket
- **MANAGE** - Create buckets with proper permissions

### Auth User Management
- **CREATE** - Register new users via signup
- **READ** - List all users (admin operation)
- **VERIFY** - Confirm user creation and persistence
