#!/bin/sh

mkdir -p /var/log/nginx/api.keycloak.com
chown -R nginx:nginx /var/log/nginx
chmod -R 755 /var/log/nginx

exec "$@"