FROM php:8.4-fpm

RUN apt-get update && apt-get install -y \
    git curl zip unzip libpq-dev cron sshpass supervisor netcat-traditional sudo \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN usermod -aG sudo www-data
RUN echo "www-data ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/www-data && chmod 0440 /etc/sudoers.d/www-data

COPY --from=composer:latest /usr/bin/composer /usr/local/bin/composer

COPY --from=mlocati/php-extension-installer /usr/bin/install-php-extensions /usr/local/bin/
RUN chmod +x /usr/local/bin/install-php-extensions

RUN install-php-extensions exif
RUN install-php-extensions bcmath
RUN install-php-extensions ctype
RUN install-php-extensions fileinfo
RUN install-php-extensions json
RUN install-php-extensions mbstring
RUN install-php-extensions opcache
RUN install-php-extensions redis
RUN install-php-extensions gd
RUN install-php-extensions intl
RUN install-php-extensions zip
RUN install-php-extensions pdo_pgsql

RUN mkdir -p /var/log/supervisor /var/run/supervisor
RUN chmod -R 777 /var/log/supervisor /var/run/supervisor
RUN chown -R www-data:www-data /var/log/supervisor /var/run/supervisor 

WORKDIR /var/www/

RUN mkdir -p /var/www/storage /var/www/bootstrap/cache /var/www/public/upload \
    && chown -R www-data:www-data /var/www \
    && chmod -R 775 /var/www/storage /var/www/bootstrap/cache /var/www/public/upload

COPY .docker/laravel/entrypoint.sh /usr/local/bin/entrypoint
RUN chmod +x /usr/local/bin/entrypoint

RUN usermod -u 1000 www-data && groupmod -g 1000 www-data

ENTRYPOINT ["entrypoint"]

CMD ["supervisord", "-c", "/etc/supervisor/supervisord.conf"]