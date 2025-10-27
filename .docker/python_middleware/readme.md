# Python middleware

Middleware has duty to authenticate every request that passes the traefik for private routes

## Features

| Feature              | Status | Description                               |
| -------------------- | ------ | ----------------------------------------- |
| Checking Jwt         | 🟢      | Check jwt is valid or has time or not     |
| Check Authorization  | ⬜      | Check the user has permission to url      |
| Use Caching System   | ⬜      | Cache for authorization data              |
| Refactor Code        | ⬜      | middleware needs refactor                 |
| SSL/TLS verification | ⬜      | SSL/TLS needs to verified in this project |
| Central .env         | ⬜      | add env to main .env                      |

## Folder Structure

```tree
.
├── auth.py # Ai generated Code
├── docker-compose.yml
├── Dockerfile
├── projects.yml # currently middleware just checks user has access to project or not
├── readme.md
└── requirements.txt
```

## Environment Variables

```env
KEYCLOAK_PUBLIC_URL=http://keycloak.myproject.com
KEYCLOAK_INTERNAL_URL=http://keycloak:8080
REALM=platform
CLIENT_ID=middleware_auth
CLIENT_SECRET=b52Jqw86z0ZJn6w9wbpZUnb6unUi6LAh
JWKS_CACHE_TTL=3600
CONFIG_FILE=projects.yml
CONFIG_CACHE_TTL=5
```

## Key Points

- This service is completely Ai generated and not recommended
- Consider setting correct client_id and client_secret in env

## Info

Feature Status Emoji Meaning:

| Status              | Meaning |
| ------------------- | ------- |
| Not Started         | ⬜       |
| In Progress Started | 🟡       |
| On Track Progress   | 🟢       |
| Blocked             | 🔴       |
| Done                | ✅       |
