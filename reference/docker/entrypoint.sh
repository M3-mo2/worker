#!/bin/sh

# هذا السكربت يعمل الآن كمستخدم www-data المقيد
# مهمته الوحيدة هي تشغيل الخدمات

echo "Starting PHP-FPM..."
# بدء تشغيل PHP-FPM في الخلفية
php-fpm &

echo "Starting Caddy as $(whoami)..."
# بدء تشغيل Caddy في الواجهة (وهو ما يبقي الحاوية تعمل)
caddy run --config /etc/caddy/Caddyfile --adapter caddyfile
