# Keycloak

In this project i use keycloak as SSO and IDP system.

## Features

| Feature                                                    | Status | Description                                    |
| ---------------------------------------------------------- | ------ | ---------------------------------------------- |
| [Auth middleware client](./../python_middleware/readme.md) | ✅      | Client for checking jwt in python middleware   |
| Laravel backend client                                     | ✅      | Client for authorization in Laravel service    |
| Authentication service                                     | ⬜      | Client for Authentication Service used for SSO |
| Exporting configuration                                    | ⬜      | Export configuration for reusable environment   |
| Implement logging                                          | ⬜      | -                                              |
| Implement custom flow                                      | ⬜      | -                                              |
| Using postgresql as database                               | ✅      | -                                              |
| Using TLS/SSL                                              | ⬜      | -                                              |
| Passing Configuration to a config file                     | ⬜      | -                                              |

## Folder Structure

```tree
.
├── docker-compose.yml
└── readme.md
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

- Access the dashboard via `keycloak.myproject.com`.
  Username: admin
  Password: admin
- In this project we used **mkcert** for ssl. Good choice for local development but we recommend to use Lets Encrypt or any valid ssl certs in production environment.

## Info

Feature Status Emoji Meaning:

| Status              | Meaning |
| ------------------- | ------- |
| Not Started         | ⬜       |
| In Progress Started | 🟡       |
| On Track Progress   | 🟢       |
| Blocked             | 🔴       |
| Done                | ✅       |
