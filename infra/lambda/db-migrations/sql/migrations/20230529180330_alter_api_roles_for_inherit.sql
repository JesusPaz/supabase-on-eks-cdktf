-- migrate:up

ALTER ROLE authenticated inherit;
ALTER ROLE anon inherit;
ALTER ROLE service_role inherit;

-- Grant pgsodium_keyholder only if it exists (pgsodium extension creates this role)
DO $$
BEGIN
    IF EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'pgsodium_keyholder') THEN
        GRANT pgsodium_keyholder to service_role;
    ELSE
        RAISE NOTICE 'pgsodium_keyholder role does not exist - pgsodium extension may not be installed';
    END IF;
END
$$;

-- migrate:down
