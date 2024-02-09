CREATE DATABASE party_sync;

CREATE USER party_sync_admin WITH PASSWORD 'password';

GRANT ALL PRIVILEGES ON DATABASE party_sync TO party_sync_admin;

 ALTER DATABASE  party_sync OWNER TO party_sync_admin;

--execute by running psql -f create-database.sql 