# --- Railway Dockerfile ---
# Python + PHP-FPM + Caddy + Node.js في حاوية واحدة

FROM python:3.11-slim-bookworm

# تثبيت PHP 8.2 FPM عبر Sury PPA
RUN apt-get update && apt-get install -y \
    apt-transport-https curl gnupg ca-certificates lsb-release debian-keyring debian-archive-keyring \
    && curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg \
    && curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | tee /etc/apt/sources.list.d/caddy-stable.list \
    && curl -sSL https://packages.sury.org/php/apt.gpg | gpg --dearmor -o /usr/share/keyrings/php.gpg \
    && echo "deb [signed-by=/usr/share/keyrings/php.gpg] https://packages.sury.org/php/ $(lsb_release -sc) main" > /etc/apt/sources.list.d/php.list \
    && apt-get update && apt-get install -y \
    php8.2-fpm php8.2-cli php8.2-curl php8.2-mbstring php8.2-xml php8.2-zip php8.2-gd php8.2-sqlite3 \
    caddy \
    && rm -rf /var/lib/apt/lists/*

# تثبيت Node.js 20
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs && rm -rf /var/lib/apt/lists/*

# تثبيت supervisord
RUN pip install --no-cache-dir supervisor

WORKDIR /app

# نسخ ملفات إعدادات PHP والأمان
RUN mkdir -p /etc/php/8.2/fpm/conf.d /etc/php/8.2/fpm/pool.d
COPY docker/custom.ini /etc/php/8.2/fpm/conf.d/99-custom-security.ini
COPY docker/php-fpm-custom.conf /etc/php/8.2/fpm/pool.d/zz-custom.conf

# نسخ Caddyfile للـ Railway
COPY Caddyfile.railway /app/Caddyfile.railway

# نسخ supervisord config
COPY supervisord.conf /app/supervisord.conf

# نسخ متطلبات Python وتثبيتها
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# نسخ المشروع كامل
COPY . .

# إنشاء المجلدات المطلوبة
RUN mkdir -p /app/data /app/user_bots /app/logs /app/marketplace

# تشغيل supervisord
CMD ["supervisord", "-c", "/app/supervisord.conf"]
