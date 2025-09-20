# API Test Suite

Comprehensive test suite for validating Supabase deployment functionality.

## Test Coverage

**Core Services:**
- **Auth** - Authentication, user management, JWT validation
- **PostgREST** - REST API with full CRUD operations
- **Storage** - File operations with S3 integration
- **Realtime** - WebSocket connectivity

**Operations Tested:**
- Service health checks
- Database CRUD (CREATE, READ, UPDATE, DELETE)
- User management (signup, listing, verification)
- File operations (upload, download, listing, bucket management)

## Usage

```bash
# Automated test execution
make all        # Install dependencies + Run tests

# Manual execution
make install    # Setup virtual environment
make test       # Run test suite
make clean      # Cleanup environment
```

## Configuration

**JWT tokens extracted from AWS Secrets Manager via Kubernetes:**
- `SUPABASE_URL` - Supabase instance endpoint (https://supabase.stack-ai.jesuspaz.com)
- `anonKey` - Anonymous access token (from AWS secret `supabase/jwt`)
- `serviceKey` - Service role token (from AWS secret `supabase/jwt`)

**Setup required:**
```bash
# Extract tokens from Kubernetes secret (sourced from AWS)
kubectl get secret -n supabase supabase-jwt -o jsonpath='{.data}' | jq -r 'to_entries[] | "\(.key)=\(.value | @base64d)"' > .env
echo "SUPABASE_URL=https://supabase.stack-ai.jesuspaz.com" >> .env
```

## Expected Results

```
✅ Tests passed: 13-14/14 (93-100%)
✅ Auth, PostgREST, Storage functional
✅ CRUD operations working
⚠️  Realtime may show minor auth issues
```

## Test Details

**14 comprehensive tests covering:**

| **Service** | **Operations** | **Endpoints** |
|-------------|----------------|---------------|
| **Auth** | Health, user CRUD | `/auth/v1/health`, `/auth/v1/signup`, `/auth/v1/admin/users` |
| **PostgREST** | Health, database CRUD | `/rest/v1/`, `/rest/v1/test_items` |
| **Storage** | Health, file CRUD, bucket management | `/storage/v1/status`, `/storage/v1/object/*` |
| **Realtime** | WebSocket connectivity | `/realtime/v1/websocket` |

**Automated setup:**
- Creates test database table
- Creates private S3 bucket
- Generates unique test data
- Cleans up after execution

**Validation:**
- Service availability and response codes
- Data persistence and retrieval
- File upload/download integrity
- User authentication flows
