-- migrate:up

-- Set up realtime
-- defaults to empty publication
create publication supabase_realtime;

-- Supabase super admin
-- Create supabase_admin user if it doesn't exist
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'supabase_admin') THEN
        CREATE USER supabase_admin WITH LOGIN;
    END IF;
END
$$;
alter user supabase_admin with createdb createrole bypassrls;
grant rds_replication to supabase_admin; -- for RDS

-- Supabase replication user (idempotent)
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'supabase_replication_admin') THEN
        CREATE USER supabase_replication_admin WITH LOGIN;
    END IF;
END
$$;
grant rds_replication to supabase_replication_admin; -- for RDS

-- Supabase read-only user (idempotent)
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'supabase_read_only_user') THEN
        CREATE ROLE supabase_read_only_user WITH LOGIN BYPASSRLS;
    END IF;
END
$$;
grant pg_read_all_data to supabase_read_only_user;

-- Extension namespacing
create schema if not exists extensions;
create extension if not exists "uuid-ossp"      with schema extensions;
create extension if not exists pgcrypto         with schema extensions;
-- pgjwt is installed via pg_tle in init-for-rds scripts
-- create extension if not exists pgjwt            with schema extensions;

-- Set up auth roles for the developer (idempotent)
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'anon') THEN
        CREATE ROLE anon NOLOGIN NOINHERIT;
    END IF;
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'authenticated') THEN
        CREATE ROLE authenticated NOLOGIN NOINHERIT; -- "logged in" user: web_user, app_user, etc
    END IF;
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'service_role') THEN
        CREATE ROLE service_role NOLOGIN NOINHERIT BYPASSRLS; -- allow developers to create JWT's that bypass their policies
    END IF;
END
$$;

-- Create authenticator user (idempotent)
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'authenticator') THEN
        CREATE USER authenticator NOINHERIT;
    END IF;
END
$$;
grant anon              to authenticator;
grant authenticated     to authenticator;
grant service_role      to authenticator;
grant supabase_admin    to authenticator;

grant usage                     on schema public to postgres, anon, authenticated, service_role;
alter default privileges in schema public grant all on tables to postgres, anon, authenticated, service_role;
alter default privileges in schema public grant all on functions to postgres, anon, authenticated, service_role;
alter default privileges in schema public grant all on sequences to postgres, anon, authenticated, service_role;

-- Allow Extensions to be used in the API
grant usage                     on schema extensions to postgres, anon, authenticated, service_role;

-- Set up namespacing
alter user supabase_admin SET search_path TO public, extensions; -- don't include the "auth" schema

-- These are required so that the users receive grants whenever "supabase_admin" creates tables/function
alter default privileges for user supabase_admin in schema public grant all
    on sequences to postgres, anon, authenticated, service_role;
alter default privileges for user supabase_admin in schema public grant all
    on tables to postgres, anon, authenticated, service_role;
alter default privileges for user supabase_admin in schema public grant all
    on functions to postgres, anon, authenticated, service_role;

-- Set short statement/query timeouts for API roles
alter role anon set statement_timeout = '3s';
alter role authenticated set statement_timeout = '8s';

-- migrate:down