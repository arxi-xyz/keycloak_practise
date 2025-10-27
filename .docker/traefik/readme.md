# Traefik

In this project traefik used as Reverse proxy and routing manager and providing secure and dynamic routing for all services

## Features

| Feature                                             | Status | Description                                                             |
| --------------------------------------------------- | ------ | ----------------------------------------------------------------------- |
| Dynamic configuration                               | ✅      | Supporting dynamic configuration (without restarting container)         |
| Load balancing                                      | ✅      | Load balancing accross multiple containers                              |
| Monitoring dashboard                                | ✅      | Traefik Dashboard                                                       |
| Https redirection Middleware                        | ✅      | -                                                                       |
| [Auth Middleware](./../python_middleware/readme.md) | ✅      | Checking for valid jwt                                                  |
| Content Type Middleware                             | ✅      | `Content:application/json accept:application/json` for backend services |
| Rate limiting Middleware                            | ⬜      | 100 rps                                                                 |
| SSL/TLS managment                                   | 🔴      | In this phase we just used mkcert but [...](#key-points)                           |
| Routing based on domain and api                     | ✅      | Routing the incoming requests to the correct service                    |

## Folder Structure

```tree
.
├── certs # SSL certificates
├── config
│   ├── dynamic # Dynamic configuration should placed here
│   │   ├── middlewares
│   │   ├── routers
│   │   ├── services
│   │   └── tls.yml
│   └── traefik.yml # Treafik configs and Entrypoints
├── docker-compose.yml
├── logs
│   ├── access.log
│   └── traefik.log
└── readme.md
```

## Key Points

- Access the dashboard via `traefik.myproject.com`.
  Username: admin
  Password: password
- In this project we used **mkcert** for ssl. mkcert is good choice for local development but we suggest to use Lets Encrypt or any valid ssl certs in production environment.

## Info

Feature Status Emoji Meaning:

| Status              | Meaning |
| ------------------- | ------- |
| Not Started         | ⬜       |
| In Progress Started | 🟡       |
| On Track Progress   | 🟢       |
| Blocked             | 🔴       |
| Done                | ✅       |
