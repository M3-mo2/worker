# --- Dockerfile المحصن والمنظف ---

FROM php:8.2-fpm-bullseye

# تثبيت Caddy
RUN apt-get update && apt-get install -y \
    debian-keyring \
    debian-archive-keyring \
    apt-transport-https \
    curl \
    gnupg \
    --no-install-recommends

RUN curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
RUN curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | tee /etc/apt/sources.list.d/caddy-stable.list
RUN apt-get update && apt-get install -y caddy && rm -rf /var/lib/apt/lists/*

# إنشاء مجلد العمل
WORKDIR /app
RUN chown www-data:www-data /app

# نسخ ملفات الإعدادات والأمان (كـ root)
COPY docker/custom.ini /usr/local/etc/php/conf.d/99-custom-security.ini
COPY docker/php-fpm-custom.conf /usr/local/etc/php-fpm.d/zz-custom.conf
COPY docker/Caddyfile.txt /etc/caddy/Caddyfile
COPY docker/entrypoint.sh /usr/local/bin/entrypoint.sh

# إعطاء صلاحيات التنفيذ للسكربت
RUN chmod 755 /usr/local/bin/entrypoint.sh

# 🟢 إضافة صلاحيات لمجلد /var/www لتفادي خطأ Caddy
RUN mkdir -p /var/www/.config /var/www/.local && \
    chown -R www-data:www-data /var/www

# 🟢 الآن فقط نتحول للمستخدم المقيد
USER www-data

# 🟢 استخدم ENTRYPOINT بدل CMD لتشغيل السكربت بشكل مضمون
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
