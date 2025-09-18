#!/bin/bash

set -e

# Check if required environment variables are set
if [ -z "$KEYCLOAK_DATABASE" ] || [ -z "$KEYCLOAK_DATABASE_USER" ] || [ -z "$KEYCLOAK_DATABASE_PASSWORD" ]; then
  echo "Error: KEYCLOAK_DATABASE, KEYCLOAK_DATABASE_USER, and KEYCLOAK_DATABASE_PASSWORD must be set"
  exit 1
fi

# Create the Keycloak database if it doesn't exist
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname postgres <<-EOSQL
  SELECT 'CREATE DATABASE $KEYCLOAK_DATABASE' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = '$KEYCLOAK_DATABASE')\gexec
EOSQL

# Create Keycloak user and grant all necessary privileges
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$KEYCLOAK_DATABASE" <<-EOSQL
    DO \$\$
    BEGIN
        IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = '$KEYCLOAK_DATABASE_USER') THEN
            CREATE USER "$KEYCLOAK_DATABASE_USER" WITH PASSWORD '$KEYCLOAK_DATABASE_PASSWORD';
        END IF;
    END
    \$\$;

    -- Grant database-level privileges
    GRANT ALL PRIVILEGES ON DATABASE "$KEYCLOAK_DATABASE" TO "$KEYCLOAK_DATABASE_USER";

    -- Grant full privileges on the public schema
    GRANT ALL ON SCHEMA public TO "$KEYCLOAK_DATABASE_USER";

    -- Grant privileges for all existing tables and sequences in public schema
    GRANT ALL ON ALL TABLES IN SCHEMA public TO "$KEYCLOAK_DATABASE_USER";
    GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO "$KEYCLOAK_DATABASE_USER";

    -- Grant privileges for all future tables and sequences in public schema
    ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO "$KEYCLOAK_DATABASE_USER";
    ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO "$KEYCLOAK_DATABASE_USER";
EOSQL