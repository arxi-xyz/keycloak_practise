#!/bin/bash

set -e

mkdir -p /var/www/storage /var/www/bootstrap/cache /var/www/public/upload \
    && chown -R www-data:www-data /var/www \
    && chmod -R 775 /var/www/storage /var/www/bootstrap/cache /var/www/public/upload


if [ -f /var/www/.env ]; then
    export $(grep -v '^#' /var/www/.env | xargs)
else
    echo "Error: .env file not found"
    exit 1
fi

composer install

health_check() {
    php -r "try { new PDO('pgsql:host=$DB_HOST;port=$DB_PORT;dbname=$DB_DATABASE', '$DB_USERNAME', '$DB_PASSWORD'); echo 'Database is healthy'; exit(0); } catch (Exception \$e) { echo 'Database is not healthy: ' . \$e->getMessage(); exit(1); }" 2>/dev/null
}

echo "Checking database health..."
attempts=0
max_attempts=30
while [ $attempts -lt $max_attempts ]; do
    if health_check; then
        echo " Database is up and running!"
        break
    else
        echo " Waiting for database to be ready... Attempt $((attempts + 1))/$max_attempts"
        sleep 3
        attempts=$((attempts + 1))
    fi
done

php artisan db:wipe
php artisan migrate

php artisan optimize:clear --no-interaction || true
php artisan optimize --no-interaction || true


echo "* * * * * /usr/local/bin/php /var/www/artisan schedule:run >> /var/www/storage/logs/cron.log 2>&1" | crontab -u www-data -

sudo /usr/sbin/cron -f &
exec "$@"