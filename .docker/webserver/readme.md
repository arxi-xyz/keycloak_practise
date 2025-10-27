# Nginx

Webserver for Laravel service

## Features

| Feature                        | Status | Description                                                                                 |
| ------------------------------ | ------ | ------------------------------------------------------------------------------------------- |
| Serving Laravel Project        | ✅      | Serving Laravel project using fpm package for better performance here and in php containers |
| Logging                        | ✅      | Access and Error log generally and host specefied                                           |
| Dynamic log directory creation | ✅      | Generate Log directories in entrypoints                                                     |
| Template-based virtual hosts   | ✅      | Template for each host                                                                      |
| SSL/TLS                        | 🔴      | ?                                                                                           |

## Folder Structure

```tree
.
├── docker-compose.yml
├── Dockerfile
├── logs
│   ├── access.log
│   ├── backend.myproject.com # dir for domain specified logs
│   └── error.log
├── nginx.conf # general config
├── readme.md
├── scripts
│   └── entrypoint.sh # creating log dirs in container
└── templates # template for hosts config
    └── backend.conf.template
```

## Environment Variables

```env
BACKEND_DOMAIN=task.myproject.com
```

## Key Points

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
