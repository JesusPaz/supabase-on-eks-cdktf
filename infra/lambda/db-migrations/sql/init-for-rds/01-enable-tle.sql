-- Create supabase_admin if it doesn't exist (needed for pg_tle grants)
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'supabase_admin') THEN
        CREATE USER supabase_admin WITH LOGIN CREATEDB CREATEROLE BYPASSRLS;
    END IF;
END
$$;

-- Grant admin roles to the RDS master user so it can execute admin commands
GRANT supabase_admin TO supabase;
GRANT rds_replication TO supabase_admin;

-- Create other admin roles that may be needed and grant them to supabase
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'supabase_auth_admin') THEN
        CREATE USER supabase_auth_admin NOINHERIT CREATEROLE LOGIN NOREPLICATION;
    END IF;
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'supabase_storage_admin') THEN
        CREATE USER supabase_storage_admin NOINHERIT CREATEROLE LOGIN NOREPLICATION;
    END IF;
END
$$;

-- Grant all admin roles to the master user
GRANT supabase_auth_admin TO supabase;
GRANT supabase_storage_admin TO supabase;

CREATE EXTENSION IF NOT EXISTS pg_tle;
GRANT pgtle_admin TO supabase_admin;
GRANT pgtle_admin TO postgres;
