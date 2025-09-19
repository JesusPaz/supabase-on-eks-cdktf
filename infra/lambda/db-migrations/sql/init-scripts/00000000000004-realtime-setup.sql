-- migrate:up

-- Create realtime schema and ensure proper permissions
CREATE SCHEMA IF NOT EXISTS realtime AUTHORIZATION supabase_admin;

-- Grant necessary permissions to roles that need to access realtime schema
GRANT USAGE ON SCHEMA realtime TO postgres, anon, authenticated, service_role;
GRANT ALL ON SCHEMA realtime TO postgres, supabase_admin;

-- Allow creating tables in realtime schema
GRANT CREATE ON SCHEMA realtime TO postgres, supabase_admin;

-- Set default privileges for future objects in realtime schema
ALTER DEFAULT PRIVILEGES FOR ROLE supabase_admin IN SCHEMA realtime GRANT ALL ON TABLES TO postgres;
ALTER DEFAULT PRIVILEGES FOR ROLE supabase_admin IN SCHEMA realtime GRANT ALL ON SEQUENCES TO postgres;
ALTER DEFAULT PRIVILEGES FOR ROLE supabase_admin IN SCHEMA realtime GRANT ALL ON ROUTINES TO postgres;

-- Ensure the supabase user (RDS master user) can work with realtime schema
GRANT ALL ON SCHEMA realtime TO supabase;
ALTER DEFAULT PRIVILEGES FOR ROLE supabase IN SCHEMA realtime GRANT ALL ON TABLES TO postgres, supabase_admin;
ALTER DEFAULT PRIVILEGES FOR ROLE supabase IN SCHEMA realtime GRANT ALL ON SEQUENCES TO postgres, supabase_admin;
ALTER DEFAULT PRIVILEGES FOR ROLE supabase IN SCHEMA realtime GRANT ALL ON ROUTINES TO postgres, supabase_admin;

-- migrate:down
