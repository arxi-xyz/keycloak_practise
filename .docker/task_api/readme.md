# Laravel

Laravel Service with simple crud

## Features

| Feature                                       | Status | Description                                                                                                  |
| --------------------------------------------- | ------ | ------------------------------------------------------------------------------------------------------------ |
| Implement simple crud                         | ✅      | Simple crud for implementing authorization on different routes                                               |
| Implement jwt check middeware                 | ✅      |                                                                                                              |
| Implement authorization middeware             | ✅      | This Feature should be implement in python service but bcz i have lack of expreince with python i do it here |
| Implement caching for authorization middeware | ✅      |                                                                                                              |
| central .env file                             | ⬜      |                                                                                                              |

## Folder Structure

```tree
.
├── app # backend buisness logics
├── artisan
├── bootstrap
├── composer.json
├── config
│   ├── other config files ...
│   └── keycloak.php
├── database
├── docker-compose.yml
├── public
├── readme.md
├── resources
├── routes
├── storage
└── tests
```

## Environment Variables

```env
# keycloak 
AUTHZ_BASE_URL=http://keycloak:8080
AUTHZ_REALM=platform
AUTHZ_CLIENT_ID=authorization

# database
DB_CONNECTION=pgsql
DB_HOST=db
DB_PORT=5432
DB_DATABASE=laravel_database
DB_USERNAME=admin
DB_PASSWORD=admin

# cache
REDIS_CLIENT=predis
REDIS_HOST=redis
REDIS_PASSWORD=secret
REDIS_PORT=6379

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
