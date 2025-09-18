#!/bin/sh

mkdir -p /var/log/nginx/$BACKEND_DOMAIN /var/log/nginx/$KEYCLOAK_DOMAIN
chown -R nginx:nginx /var/log/nginx
chmod -R 755 /var/log/nginx

exec "$@"