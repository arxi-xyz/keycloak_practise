FROM nginx:stable

COPY ./.docker/nginx/scripts/entrypoint.sh /docker-entrypoint.d/entrypoint.sh
RUN chmod +x /docker-entrypoint.d/entrypoint.sh

CMD ["nginx", "-g", "daemon off;"]