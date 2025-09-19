-- postgres user for developers (idempotent)
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'postgres') THEN
        CREATE USER postgres WITH LOGIN;
    END IF;
END
$$;
GRANT rds_replication TO postgres;
