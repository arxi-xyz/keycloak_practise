# Postgresql

Database for backend services and keycloak

## Features

| Feature                         | Status | Description                                         |
| ------------------------------- | ------ | --------------------------------------------------- |
| Generate Keycloak Prerequisites | 🟢      | Creating Database & user & permissions for keycloak |
| Generate Laravel Prerequisites  | ⬜      | Creating Database & user & permissions for Laravel  |
| Backup                          | ⬜      | Backup from all of the databases                    |
| automatic backup restore        | ⬜      | restore backup                                      |

## Folder Structure

```tree
.
├── docker-compose.yml
├── Dockerfile
├── readme.md
└── scripts
    └── keycloak_init_db.sh
```

## Environment Variables

```env
POSTGRES_USER=${POSTGRES_USERNAME}
POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
POSTGRES_DB=${POSTGRES_DATABASE}
PGDATA=/var/lib/postgresql/17/docker

KEYCLOAK_DATABASE=${KEYCLOAK_DATABASE}
KEYCLOAK_DATABASE_USER=${KEYCLOAK_DATABASE_USER}
KEYCLOAK_DATABASE_PASSWORD=${KEYCLOAK_DATABASE_PASSWORD}
```

## Key Points

## Info

Feature Status Emoji Meaning:

| Status              | Meaning |
| ------------------- | ------- |
| Not Started         | ⬜       |
| In Progress Started | 🟡       |
| On Track Progress   | 🟢       |
| Blocked             | 🔴       |
| Done                | ✅       |
