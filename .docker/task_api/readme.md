# Laravel

Laravel Service with simple crud

## Features

| Feature                                       | Status | Description                                                                                                  |
| --------------------------------------------- | ------ | ------------------------------------------------------------------------------------------------------------ |
| Implement simple crud                         | ✅      | Simple crud for implementing authorization on different routes                                               |
| Implement jwt check middeware                 | ✅      |                                                                                                              |
| Implement authorization middeware             | 🟢      | This Feature should be implement in python service but bcz i have lack of expreince with python i do it here |
| Implement caching for authorization middeware | ⬜      |                                                                                                              |
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
KEYCLOAK_BOOT_ADMIN_USERNAME=admin
KEYCLOAK_BOOT_ADMIN_PASSWORD=admin
KEYCLOAK_VERSION=26.3.4
KEYCLOAK_PORT=8083
KEYCLOAK_DATABASE=keycloak
KEYCLOAK_DATABASE_USER=keycloak_user
KEYCLOAK_DATABASE_PASSWORD=your_keycloak_password
KEYCLOAK_DOMAIN=keycloak.myproject.com
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
