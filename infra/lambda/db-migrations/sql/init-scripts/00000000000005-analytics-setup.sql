-- migrate:up

-- Create _supabase database for analytics if it doesn't exist
-- Note: We need to connect to the default database first, then create _supabase
-- This will be handled by the Lambda function

-- Create _analytics schema in the main database for now
-- (In production, this should be in a separate _supabase database)
CREATE SCHEMA IF NOT EXISTS _analytics AUTHORIZATION supabase_admin;

-- Grant necessary permissions to roles that need to access _analytics schema
GRANT USAGE ON SCHEMA _analytics TO postgres, supabase_admin;
GRANT ALL ON SCHEMA _analytics TO postgres, supabase_admin;

-- Allow creating tables in _analytics schema
GRANT CREATE ON SCHEMA _analytics TO postgres, supabase_admin;

-- Set default privileges for future objects in _analytics schema
ALTER DEFAULT PRIVILEGES FOR ROLE supabase_admin IN SCHEMA _analytics GRANT ALL ON TABLES TO postgres;
ALTER DEFAULT PRIVILEGES FOR ROLE supabase_admin IN SCHEMA _analytics GRANT ALL ON SEQUENCES TO postgres;
ALTER DEFAULT PRIVILEGES FOR ROLE supabase_admin IN SCHEMA _analytics GRANT ALL ON ROUTINES TO postgres;

-- Ensure the supabase user (RDS master user) can work with _analytics schema
GRANT ALL ON SCHEMA _analytics TO supabase;
ALTER DEFAULT PRIVILEGES FOR ROLE supabase IN SCHEMA _analytics GRANT ALL ON TABLES TO postgres, supabase_admin;
ALTER DEFAULT PRIVILEGES FOR ROLE supabase IN SCHEMA _analytics GRANT ALL ON SEQUENCES TO postgres, supabase_admin;
ALTER DEFAULT PRIVILEGES FOR ROLE supabase IN SCHEMA _analytics GRANT ALL ON ROUTINES TO postgres, supabase_admin;

-- migrate:down
DROP SCHEMA IF EXISTS _analytics CASCADE;
