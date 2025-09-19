-- Check available extensions
SELECT name, default_version, installed_version 
FROM pg_available_extensions 
WHERE name IN ('pgsodium', 'safeupdate', 'supautils', 'pg_cron', 'pg_net')
ORDER BY name;

-- Check if pgsodium is installed
SELECT extname, extversion FROM pg_extension WHERE extname = 'pgsodium';

-- Check what roles exist
SELECT rolname FROM pg_roles WHERE rolname LIKE '%sodium%' ORDER BY rolname;
