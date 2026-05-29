# 🏗️ خطة معمارية متقدمة - بوت استضافة PHP على تليجرام

## 📋 نظرة عامة

**اسم المشروع:** PHP Bot Hosting Platform v2  
**الهدف:** بناء منصة استضافة بوتات PHP على تليجرام بمعمارية قوية وقابلة للتوسع  
**منصة النشر:** Railway  
**التاريخ:** 28 مايو 2026

---

## 🎯 المميزات المطلوبة (Scope)

### ✅ المميزات الأساسية
1. **نظام إدارة الملفات**
   - رفع ملفات PHP عبر تليجرام
   - حذف وتعديل الملفات
   - إنشاء وحذف المجلدات
   - عرض شجرة الملفات

2. **نظام استضافة البوتات**
   - إعداد Webhook تلقائي
   - تشغيل PHP عبر PHP-FPM
   - عزل تام بين المستخدمين
   - مراقبة حالة البوت

3. **نظام الاشتراكات (Free/Pro)**
   - خطة Free: 50MB، 30 ملف، 5 مجلدات
   - خطة Pro: 1GB، 500 ملف، 50 مجلد
   - نظام انتهاء الاشتراك
   - تخفيض تلقائي عند الانتهاء

4. **نظام الحصص (Quota System)**
   - مراقبة استهلاك التخزين
   - حساب عدد الملفات والمجلدات
   - منع تجاوز الحدود

### ❌ المميزات المستبعدة (Out of Scope)
- Marketplace
- AI Integration
- Web Interface
- Developer API (في المرحلة الأولى)

---

## 🏛️ المعمارية الجديدة (Architecture)

### 📐 المبادئ المعمارية

1. **Separation of Concerns** - فصل واضح بين الطبقات
2. **Single Responsibility** - كل module له مسؤولية واحدة
3. **Dependency Injection** - تقليل الاعتماديات المباشرة
4. **Event-Driven Architecture** - استخدام الأحداث للتواصل بين المكونات
5. **Scalability First** - تصميم قابل للتوسع من البداية
6. **Security by Design** - الأمان جزء أساسي من التصميم
7. **Fail-Safe Mechanisms** - آليات حماية من الأخطاء

### 🏗️ البنية الطبقية (Layered Architecture)

```
┌─────────────────────────────────────────────────────────┐
│                    Presentation Layer                    │
│              (Telegram Bot Interface)                    │
│  - Command Handlers                                      │
│  - Callback Handlers                                     │
│  - Message Handlers                                      │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                   Application Layer                      │
│                  (Business Logic)                        │
│  - FileManager Service                                   │
│  - BotHosting Service                                    │
│  - SubscriptionManager Service                           │
│  - QuotaManager Service                                  │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                     Domain Layer                         │
│                   (Core Models)                          │
│  - User Model                                            │
│  - Bot Model                                             │
│  - File Model                                            │
│  - Subscription Model                                    │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                 Infrastructure Layer                     │
│              (External Services)                         │
│  - Database (PostgreSQL)                                 │
│  - File Storage (Volume)                                 │
│  - Cache (Redis)                                         │
│  - Queue (Redis Queue)                                   │
└─────────────────────────────────────────────────────────┘
```

---

## 🗄️ قاعدة البيانات (Database Design)

### ⚠️ تحسين كبير: PostgreSQL بدلاً من SQLite

**لماذا PostgreSQL؟**
- ✅ أداء أفضل مع concurrent requests
- ✅ دعم أفضل للـ transactions
- ✅ قابلية توسع أعلى
- ✅ Railway توفر PostgreSQL مجاناً
- ✅ دعم JSON native للبيانات المعقدة
- ✅ Full-text search مدمج

### 📊 Database Schema

```sql
-- ============================================
-- 1. جدول المستخدمين (Users Table)
-- ============================================
CREATE TABLE users (
    user_id BIGINT PRIMARY KEY,
    username VARCHAR(255),
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    plan VARCHAR(20) NOT NULL DEFAULT 'free', -- 'free' or 'pro'
    plan_expiry TIMESTAMP,
    plan_source VARCHAR(50), -- 'purchase', 'gift', 'trial'
    total_storage_bytes BIGINT DEFAULT 0,
    total_files INTEGER DEFAULT 0,
    total_folders INTEGER DEFAULT 0,
    is_banned BOOLEAN DEFAULT FALSE,
    ban_reason TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_activity TIMESTAMP,
    metadata JSONB -- للبيانات الإضافية المرنة
);

CREATE INDEX idx_users_plan ON users(plan);
CREATE INDEX idx_users_plan_expiry ON users(plan_expiry) WHERE plan_expiry IS NOT NULL;
CREATE INDEX idx_users_created_at ON users(created_at);

-- ============================================
-- 2. جدول البوتات (Bots Table)
-- ============================================
CREATE TABLE bots (
    bot_id SERIAL PRIMARY KEY,
    owner_id BIGINT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    bot_token VARCHAR(255) NOT NULL UNIQUE,
    bot_username VARCHAR(255),
    webhook_url TEXT,
    webhook_path VARCHAR(500), -- المسار النسبي للملف PHP
    is_active BOOLEAN DEFAULT TRUE,
    last_webhook_call TIMESTAMP,
    total_requests BIGINT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB
);

CREATE INDEX idx_bots_owner ON bots(owner_id);
CREATE INDEX idx_bots_token ON bots(bot_token);
CREATE INDEX idx_bots_active ON bots(is_active);

-- ============================================
-- 3. جدول الملفات (Files Table)
-- ============================================
CREATE TABLE files (
    file_id SERIAL PRIMARY KEY,
    owner_id BIGINT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    file_path TEXT NOT NULL, -- المسار الكامل نسبة للمستخدم
    file_name VARCHAR(500) NOT NULL,
    file_size BIGINT NOT NULL,
    file_type VARCHAR(50), -- 'php', 'txt', 'json', etc.
    parent_folder TEXT, -- المجلد الأب
    is_directory BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(owner_id, file_path)
);

CREATE INDEX idx_files_owner ON files(owner_id);
CREATE INDEX idx_files_parent ON files(owner_id, parent_folder);
CREATE INDEX idx_files_type ON files(file_type);

-- ============================================
-- 4. جدول الاشتراكات (Subscriptions Table)
-- ============================================
CREATE TABLE subscriptions (
    subscription_id SERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    plan VARCHAR(20) NOT NULL,
    start_date TIMESTAMP NOT NULL,
    end_date TIMESTAMP NOT NULL,
    payment_method VARCHAR(50), -- 'manual', 'stripe', 'paypal', etc.
    payment_amount DECIMAL(10, 2),
    payment_currency VARCHAR(10),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB
);

CREATE INDEX idx_subscriptions_user ON subscriptions(user_id);
CREATE INDEX idx_subscriptions_active ON subscriptions(is_active);
CREATE INDEX idx_subscriptions_end_date ON subscriptions(end_date);

-- ============================================
-- 5. جدول سجلات الـ Webhook (Webhook Logs)
-- ============================================
CREATE TABLE webhook_logs (
    log_id BIGSERIAL PRIMARY KEY,
    bot_id INTEGER REFERENCES bots(bot_id) ON DELETE CASCADE,
    request_method VARCHAR(10),
    request_path TEXT,
    response_status INTEGER,
    response_time_ms INTEGER,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_webhook_logs_bot ON webhook_logs(bot_id);
CREATE INDEX idx_webhook_logs_created ON webhook_logs(created_at);

-- Partition by month for better performance
-- يمكن تقسيم الجدول حسب الشهر لتحسين الأداء

-- ============================================
-- 6. جدول الإحصائيات اليومية (Daily Stats)
-- ============================================
CREATE TABLE daily_stats (
    stat_id SERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(user_id) ON DELETE CASCADE,
    stat_date DATE NOT NULL,
    stat_type VARCHAR(50) NOT NULL, -- 'webhook_calls', 'file_uploads', etc.
    stat_value BIGINT DEFAULT 0,
    UNIQUE(user_id, stat_date, stat_type)
);

CREATE INDEX idx_daily_stats_user_date ON daily_stats(user_id, stat_date);
CREATE INDEX idx_daily_stats_date ON daily_stats(stat_date);

-- ============================================
-- 7. جدول الإشعارات (Notifications Queue)
-- ============================================
CREATE TABLE notifications (
    notification_id SERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    notification_type VARCHAR(50) NOT NULL, -- 'subscription_expiry', 'quota_warning', etc.
    message TEXT NOT NULL,
    is_sent BOOLEAN DEFAULT FALSE,
    scheduled_at TIMESTAMP NOT NULL,
    sent_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_notifications_user ON notifications(user_id);
CREATE INDEX idx_notifications_scheduled ON notifications(scheduled_at) WHERE is_sent = FALSE;

-- ============================================
-- 8. جدول الأنشطة (Activity Logs)
-- ============================================
CREATE TABLE activity_logs (
    log_id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(user_id) ON DELETE SET NULL,
    action_type VARCHAR(100) NOT NULL, -- 'file_upload', 'file_delete', 'bot_create', etc.
    action_details JSONB,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_activity_logs_user ON activity_logs(user_id);
CREATE INDEX idx_activity_logs_created ON activity_logs(created_at);
CREATE INDEX idx_activity_logs_action ON activity_logs(action_type);
```

### 🔄 Database Triggers & Functions

```sql
-- Trigger لتحديث updated_at تلقائياً
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_bots_updated_at BEFORE UPDATE ON bots
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_files_updated_at BEFORE UPDATE ON files
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Function لحساب استهلاك المستخدم
CREATE OR REPLACE FUNCTION calculate_user_usage(p_user_id BIGINT)
RETURNS TABLE(total_bytes BIGINT, total_files INTEGER, total_folders INTEGER) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        COALESCE(SUM(file_size), 0)::BIGINT as total_bytes,
        COUNT(*) FILTER (WHERE is_directory = FALSE)::INTEGER as total_files,
        COUNT(*) FILTER (WHERE is_directory = TRUE)::INTEGER as total_folders
    FROM files
    WHERE owner_id = p_user_id;
END;
$$ LANGUAGE plpgsql;
```

---

## 🏗️ هيكل المشروع (Project Structure)

```
php-bot/
├── src/
│   ├── __init__.py
│   ├── __main__.py                 # Entry point
│   │
│   ├── core/                       # Core infrastructure
│   │   ├── __init__.py
│   │   ├── config.py              # Configuration management
│   │   ├── database.py            # Database connection pool
│   │   ├── cache.py               # Redis cache manager
│   │   ├── logger.py              # Structured logging
│   │   ├── exceptions.py          # Custom exceptions
│   │   └── events.py              # Event system
│   │
│   ├── models/                     # Domain models
│   │   ├── __init__.py
│   │   ├── user.py                # User model
│   │   ├── bot.py                 # Bot model
│   │   ├── file.py                # File model
│   │   ├── subscription.py        # Subscription model
│   │   └── enums.py               # Enums (PlanType, FileType, etc.)
│   │
│   ├── repositories/               # Data access layer
│   │   ├── __init__.py
│   │   ├── base.py                # Base repository
│   │   ├── user_repository.py
│   │   ├── bot_repository.py
│   │   ├── file_repository.py
│   │   └── subscription_repository.py
│   │
│   ├── services/                   # Business logic
│   │   ├── __init__.py
│   │   ├── file_manager.py        # File operations
│   │   ├── bot_hosting.py         # Bot hosting logic
│   │   ├── subscription_manager.py # Subscription management
│   │   ├── quota_manager.py       # Quota enforcement
│   │   ├── webhook_dispatcher.py  # Webhook handling
│   │   └── notification_service.py # Notifications
│   │
│   ├── handlers/                   # Telegram handlers
│   │   ├── __init__.py
│   │   ├── start.py               # /start command
│   │   ├── files.py               # File management
│   │   ├── bots.py                # Bot management
│   │   ├── subscription.py        # Subscription commands
│   │   └── admin.py               # Admin commands
│   │
│   ├── middleware/                 # Middleware
│   │   ├── __init__.py
│   │   ├── auth.py                # Authentication
│   │   ├── rate_limit.py          # Rate limiting
│   │   └── logging.py             # Request logging
│   │
│   ├── tasks/                      # Background tasks
│   │   ├── __init__.py
│   │   ├── subscription_checker.py # Check expired subscriptions
│   │   ├── quota_calculator.py    # Recalculate quotas
│   │   ├── notification_sender.py # Send notifications
│   │   └── cleanup.py             # Cleanup old logs
│   │
│   ├── utils/                      # Utilities
│   │   ├── __init__.py
│   │   ├── validators.py          # Input validation
│   │   ├── formatters.py          # Text formatting
│   │   ├── security.py            # Security helpers
│   │   └── helpers.py             # General helpers
│   │
│   └── web/                        # Web servers
│       ├── __init__.py
│       ├── webhook_receiver.py    # Receive webhooks from Telegram
│       └── php_gateway.py         # Proxy to PHP-FPM
│
├── config/
│   ├── host_bootstrap.php         # PHP bootstrap file
│   └── php-fpm.conf               # PHP-FPM configuration
│
├── migrations/                     # Database migrations
│   ├── 001_initial_schema.sql
│   ├── 002_add_indexes.sql
│   └── ...
│
├── tests/                          # Tests
│   ├── unit/
│   ├── integration/
│   └── e2e/
│
├── scripts/                        # Utility scripts
│   ├── setup_db.py
│   ├── migrate.py
│   └── seed_data.py
│
├── docker/                         # Docker configs (for local dev)
│   └── Dockerfile.dev
│
├── .env.example                    # Environment variables template
├── requirements.txt                # Python dependencies
├── railway.json                    # Railway configuration
├── Procfile                        # Railway process definition
└── README.md
```

---

## 🔧 التقنيات المستخدمة (Tech Stack)

### Backend Stack

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| **Runtime** | Python | 3.11+ | Main application |
| **Bot Framework** | python-telegram-bot | 21.x | Telegram bot (أفضل من Telethon) |
| **Web Framework** | FastAPI | 0.110+ | Webhook receiver & API |
| **Database** | PostgreSQL | 16+ | Primary database |
| **Cache** | Redis | 7+ | Caching & queues |
| **PHP Runtime** | PHP-FPM | 8.3 | Execute user bots |
| **Reverse Proxy** | Caddy | 2.7+ | Route requests |
| **ORM** | SQLAlchemy | 2.0+ | Database ORM |
| **Async DB** | asyncpg | 0.29+ | Async PostgreSQL driver |
| **Task Queue** | APScheduler | 3.10+ | Background tasks |
| **Validation** | Pydantic | 2.6+ | Data validation |
| **Logging** | structlog | 24.x | Structured logging |

### 🔄 لماذا python-telegram-bot بدلاً من Telethon؟

**المشاكل في Telethon:**
- ❌ مصمم للـ MTProto (user accounts) وليس Bot API
- ❌ معقد للبوتات البسيطة
- ❌ Documentation أقل وضوحاً للبوتات
- ❌ Community support أقل

**مميزات python-telegram-bot:**
- ✅ مصمم خصيصاً للبوتات
- ✅ API واضح وسهل
- ✅ Built-in support للـ webhooks
- ✅ Job queue مدمج
- ✅ Conversation handlers قوية
- ✅ Documentation ممتاز
- ✅ Community كبير ونشط

---

## 🚀 النشر على Railway (Deployment)

### 📦 Railway Configuration

**railway.json:**
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "numReplicas": 1,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

**Procfile:**
```
web: caddy run --config Caddyfile --adapter caddyfile
bot: python -m src
worker: python -m src.tasks
```

### 🔌 Railway Services

```
┌─────────────────────────────────────────────────────────┐
│                    Railway Project                       │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │   Main App   │  │  PostgreSQL  │  │    Redis     │ │
│  │              │  │              │  │              │ │
│  │ - Bot        │  │ - Database   │  │ - Cache      │ │
│  │ - Webhook    │  │              │  │ - Queue      │ │
│  │ - PHP-FPM    │  │              │  │              │ │
│  │ - Caddy      │  │              │  │              │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
│                                                          │
│  ┌──────────────────────────────────────────────────┐  │
│  │              Volume (Persistent)                  │  │
│  │          /data/user_bots/{user_id}/              │  │
│  └──────────────────────────────────────────────────┘  │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### 🌍 Environment Variables

```bash
# Telegram Bot
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_WEBHOOK_URL=https://your-app.railway.app/webhook
TELEGRAM_WEBHOOK_SECRET=random_secret_string

# Database
DATABASE_URL=postgresql://user:pass@host:5432/dbname
DATABASE_POOL_SIZE=20
DATABASE_MAX_OVERFLOW=10

# Redis
REDIS_URL=redis://host:6379/0
REDIS_CACHE_TTL=3600

# Application
APP_ENV=production
APP_DEBUG=false
LOG_LEVEL=INFO
SECRET_KEY=your_secret_key

# PHP
PHP_FPM_SOCKET=/run/php/php8.3-fpm.sock
PHP_MAX_EXECUTION_TIME=30
PHP_MEMORY_LIMIT=128M

# Storage
USER_BOTS_DIR=/data/user_bots
MAX_UPLOAD_SIZE_MB=10

# Plans
FREE_PLAN_STORAGE_MB=50
FREE_PLAN_MAX_FILES=30
FREE_PLAN_MAX_FOLDERS=5
PRO_PLAN_STORAGE_MB=1024
PRO_PLAN_MAX_FILES=500
PRO_PLAN_MAX_FOLDERS=50

# Security
ALLOWED_FILE_EXTENSIONS=php,txt,json,html,css,js
DANGEROUS_PHP_FUNCTIONS=exec,shell_exec,system,passthru,eval,popen,proc_open

# Rate Limiting
RATE_LIMIT_PER_MINUTE=30
RATE_LIMIT_PER_HOUR=500
```

### 🐳 Dockerfile (للنشر على Railway)

```dockerfile
# Multi-stage build for optimization
FROM python:3.11-slim-bookworm AS base

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    ca-certificates \
    lsb-release \
    && rm -rf /var/lib/apt/lists/*

# Install PHP 8.3 from Sury repository
RUN curl -sSL https://packages.sury.org/php/apt.gpg | gpg --dearmor -o /usr/share/keyrings/php.gpg \
    && echo "deb [signed-by=/usr/share/keyrings/php.gpg] https://packages.sury.org/php/ $(lsb_release -sc) main" > /etc/apt/sources.list.d/php.list \
    && apt-get update \
    && apt-get install -y \
        php8.3-fpm \
        php8.3-cli \
        php8.3-curl \
        php8.3-mbstring \
        php8.3-xml \
        php8.3-zip \
        php8.3-gd \
        php8.3-pgsql \
    && rm -rf /var/lib/apt/lists/*

# Install Caddy
RUN curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg \
    && curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | tee /etc/apt/sources.list.d/caddy-stable.list \
    && apt-get update \
    && apt-get install -y caddy \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy PHP configuration
COPY config/php-fpm.conf /etc/php/8.3/fpm/pool.d/www.conf
COPY config/host_bootstrap.php /app/config/host_bootstrap.php

# Copy Caddyfile
COPY Caddyfile /app/Caddyfile

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p /data/user_bots /app/logs /run/php

# Set permissions
RUN chmod -R 755 /app && chmod -R 777 /data/user_bots /app/logs /run/php

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Start services
CMD ["sh", "-c", "php-fpm8.3 -D && caddy start --config /app/Caddyfile --adapter caddyfile && python -m src"]
```

### 📝 Caddyfile

```caddyfile
:{$PORT:8000} {
    # Health check endpoint
    handle /health {
        respond "OK" 200
    }

    # Webhook endpoint (from Telegram)
    handle /webhook* {
        reverse_proxy localhost:8001
    }

    # User bots (PHP execution)
    @user_bot path_regexp bot ^/bot/(\d+)/(.+)$
    handle @user_bot {
        root * /data/user_bots/{re.bot.1}
        rewrite * /{re.bot.2}
        
        php_fastcgi unix/{$PHP_FPM_SOCKET} {
            env PHP_ADMIN_VALUE "open_basedir=/data/user_bots/{re.bot.1}:/tmp/ \n auto_prepend_file=/app/config/host_bootstrap.php"
            env PHP_VALUE "display_errors=Off \n log_errors=On \n error_log=/app/logs/php_errors.log"
        }
    }

    # Security: Block path traversal
    @path_traversal path_regexp \.\.
    handle @path_traversal {
        respond "Forbidden" 403
    }

    # Default: 404
    handle {
        respond "Not Found" 404
    }
}
```

---

## 🔐 الأمان (Security)

### 🛡️ Security Layers

1. **Input Validation**
   - التحقق من جميع المدخلات
   - Sanitization للملفات المرفوعة
   - منع Path Traversal

2. **PHP Sandbox**
   - `open_basedir` لعزل المستخدمين
   - `disable_functions` لمنع الدوال الخطرة
   - Resource limits (memory, execution time)

3. **Rate Limiting**
   - حد أقصى للطلبات في الدقيقة
   - حد أقصى للطلبات في الساعة
   - IP-based rate limiting

4. **File Security**
   - فحص امتدادات الملفات
   - فحص محتوى الملفات
   - منع رفع ملفات تنفيذية خطرة

5. **Database Security**
   - Prepared statements (SQLAlchemy ORM)
   - Connection pooling
   - Encrypted sensitive data

### 🔒 PHP Security Configuration

**config/php-fpm.conf:**
```ini
[www]
user = www-data
group = www-data
listen = /run/php/php8.3-fpm.sock
listen.owner = www-data
listen.group = www-data
pm = dynamic
pm.max_children = 20
pm.start_servers = 5
pm.min_spare_servers = 5
pm.max_spare_servers = 10

; Security settings
php_admin_value[disable_functions] = exec,passthru,shell_exec,system,proc_open,popen,curl_exec,curl_multi_exec,parse_ini_file,show_source
php_admin_value[allow_url_fopen] = Off
php_admin_value[allow_url_include] = Off
php_admin_value[expose_php] = Off
php_admin_value[display_errors] = Off
php_admin_value[log_errors] = On
php_admin_value[error_log] = /app/logs/php_errors.log
php_admin_value[max_execution_time] = 30
php_admin_value[memory_limit] = 128M
php_admin_value[upload_max_filesize] = 10M
php_admin_value[post_max_size] = 10M
```

**config/host_bootstrap.php:**
```php
<?php
// Auto-loaded before every PHP script execution
// Provides helper functions for user bots

// Prevent direct access
if (basename($_SERVER['SCRIPT_FILENAME']) === 'host_bootstrap.php') {
    http_response_code(403);
    exit('Forbidden');
}

// Helper function to get bot info
function getBotInfo() {
    $path = $_SERVER['REQUEST_URI'];
    preg_match('/^\/bot\/(\d+)\//', $path, $matches);
    return [
        'user_id' => $matches[1] ?? null,
        'base_url' => 'https://' . $_SERVER['HTTP_HOST'] . '/bot/' . ($matches[1] ?? ''),
    ];
}

// Helper function to log messages
function botLog($message, $level = 'INFO') {
    $info = getBotInfo();
    $log = sprintf(
        "[%s] [User: %s] %s\n",
        date('Y-m-d H:i:s'),
        $info['user_id'] ?? 'unknown',
        $message
    );
    error_log($log, 3, '/app/logs/user_bots.log');
}
```

---

## 📊 نظام الحصص (Quota System)

### 🎯 Quota Limits

| Feature | Free Plan | Pro Plan |
|---------|-----------|----------|
| Storage | 50 MB | 1 GB |
| Max Files | 30 | 500 |
| Max Folders | 5 | 50 |
| Max Bots | 1 | 5 |
| Webhook Calls/Day | 10,000 | 100,000 |
| File Upload Size | 5 MB | 10 MB |

### ⚙️ Quota Enforcement Flow

```
User Action (Upload File)
         ↓
Check Current Usage
         ↓
Calculate New Usage
         ↓
Compare with Plan Limits
         ↓
    ┌────┴────┐
    ↓         ↓
  Allow     Reject
    ↓         ↓
 Execute   Return Error
    ↓
Update Database
    ↓
Update Cache
```

### 🔄 Quota Calculation Strategy

**Real-time vs Cached:**
- استخدام Redis للـ caching
- تحديث الـ cache عند كل عملية
- Fallback للـ database عند فشل الـ cache
- إعادة حساب كل 1 ساعة للتأكد من الدقة

---

## 🎨 واجهة المستخدم (User Interface)

### 📱 Telegram Bot Commands

```
/start - بدء استخدام البوت
/help - عرض المساعدة
/myplan - عرض خطتك الحالية
/usage - عرض الاستهلاك
/upgrade - الترقية لـ Pro

📁 إدارة الملفات:
/files - عرض الملفات
/upload - رفع ملف
/delete - حذف ملف
/newfolder - إنشاء مجلد

🤖 إدارة البوتات:
/mybots - عرض بوتاتك
/newbot - إضافة بوت جديد
/setwebhook - إعداد webhook
/deletebot - حذف بوت

👑 Admin Commands:
/stats - إحصائيات النظام
/users - عرض المستخدمين
/grantpro - منح Pro لمستخدم
/ban - حظر مستخدم
```

### 🎯 User Flow Examples

**1. إنشاء بوت جديد:**
```
User: /newbot
Bot: أرسل لي Bot Token الخاص بالبوت
User: 123456:ABC-DEF...
Bot: ✅ تم التحقق من البوت @example_bot
     الآن ارفع ملف bot.php الخاص بك
User: [uploads bot.php]
Bot: ✅ تم رفع الملف بنجاح
     هل تريد إعداد الـ webhook الآن؟
     [نعم] [لا]
User: [نعم]
Bot: ✅ تم إعداد الـ webhook بنجاح!
     رابط البوت: https://your-app.railway.app/bot/123456/bot.php
```

**2. رفع ملف:**
```
User: /upload
Bot: أرسل الملف الذي تريد رفعه
User: [uploads file.php]
Bot: اختر المجلد:
     [📁 /] [📁 includes/] [📁 config/]
User: [📁 includes/]
Bot: ✅ تم رفع file.php إلى /includes/
     الاستهلاك: 2.5 MB / 50 MB
```

---

## 🔄 Data Flow Architecture

### 📥 Webhook Flow (من Telegram للبوت)

```
Telegram API
     ↓
Railway Domain (https://your-app.railway.app)
     ↓
Caddy (Port 8000)
     ↓
FastAPI Webhook Receiver (Port 8001)
     ↓
python-telegram-bot Handler
     ↓
Business Logic (Services)
     ↓
Database / Cache
```

### 📤 User Bot Webhook Flow (من Telegram لبوت المستخدم)

```
Telegram API
     ↓
Railway Domain (https://your-app.railway.app/bot/USER_ID/bot.php)
     ↓
Caddy (Port 8000)
     ↓
PHP-FPM (Unix Socket)
     ↓
User's bot.php (with open_basedir isolation)
     ↓
[Optional] Database / External APIs
```

---

## 🚦 Background Tasks

### ⏰ Scheduled Tasks

| Task | Frequency | Purpose |
|------|-----------|---------|
| **Subscription Checker** | Every 1 hour | فحص الاشتراكات المنتهية وتخفيض المستخدمين |
| **Quota Calculator** | Every 6 hours | إعادة حساب استهلاك المستخدمين |
| **Notification Sender** | Every 5 minutes | إرسال الإشعارات المجدولة |
| **Log Cleanup** | Daily at 3 AM | حذف السجلات القديمة (أكثر من 30 يوم) |
| **Cache Warmup** | Every 12 hours | تحديث الـ cache للمستخدمين النشطين |
| **Health Check** | Every 1 minute | فحص صحة الخدمات |

### 📋 Task Implementation Example

```python
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta

scheduler = AsyncIOScheduler()

@scheduler.scheduled_job('interval', hours=1)
async def check_expired_subscriptions():
    """Check and downgrade expired subscriptions"""
    now = datetime.utcnow()
    expired_users = await subscription_repo.get_expired(now)
    
    for user in expired_users:
        await subscription_manager.downgrade_to_free(user.user_id)
        await notification_service.send(
            user.user_id,
            "⚠️ انتهت صلاحية اشتراكك Pro. تم تخفيضك إلى Free."
        )
```

---

## 📈 Performance Optimization

### ⚡ Optimization Strategies

1. **Database Optimization**
   - Connection pooling (20 connections)
   - Proper indexing على الـ queries الشائعة
   - Query optimization باستخدام EXPLAIN
   - Partitioning للجداول الكبيرة (logs)

2. **Caching Strategy**
   - User data: 1 hour TTL
   - Bot data: 30 minutes TTL
   - Quota data: 5 minutes TTL
   - File tree: 10 minutes TTL

3. **File Operations**
   - Async file I/O باستخدام aiofiles
   - Streaming للملفات الكبيرة
   - Compression للملفات المخزنة

4. **API Rate Limiting**
   - Redis-based rate limiting
   - Per-user limits
   - Per-IP limits
   - Exponential backoff

---

## 🧪 Testing Strategy

### 🎯 Test Coverage

```
tests/
├── unit/                           # Unit tests (70% coverage target)
│   ├── test_quota_manager.py
│   ├── test_file_manager.py
│   ├── test_subscription_manager.py
│   └── test_validators.py
│
├── integration/                    # Integration tests
│   ├── test_database.py
│   ├── test_redis.py
│   └── test_file_operations.py
│
└── e2e/                           # End-to-end tests
    ├── test_bot_creation_flow.py
    ├── test_file_upload_flow.py
    └── test_subscription_flow.py
```

### 🔬 Test Examples

```python
# Unit Test Example
async def test_quota_check_free_user():
    user = User(user_id=123, plan='free')
    quota_manager = QuotaManager()
    
    # Test: Free user uploading 51 MB (should fail)
    result = await quota_manager.can_upload(
        user_id=123,
        file_size=51 * 1024 * 1024
    )
    
    assert result.allowed == False
    assert "تجاوزت مساحة التخزين" in result.message
```

---

## 🔍 Monitoring & Logging

### 📊 Metrics to Track

1. **System Metrics**
   - CPU usage
   - Memory usage
   - Disk usage
   - Network I/O

2. **Application Metrics**
   - Active users
   - Total bots
   - Webhook calls/minute
   - File uploads/minute
   - Database query time
   - Cache hit rate

3. **Business Metrics**
   - Free vs Pro users
   - Subscription conversions
   - Average storage per user
   - Most active users

### 📝 Structured Logging

```python
import structlog

logger = structlog.get_logger()

logger.info(
    "file_uploaded",
    user_id=123,
    file_name="bot.php",
    file_size=1024,
    duration_ms=150
)
```

---

## 🗺️ Implementation Roadmap

### 📅 Phase 1: Core Infrastructure (Week 1)

**Day 1-2: Setup & Database**
- ✅ إعداد بيئة التطوير
- ✅ إنشاء PostgreSQL schema
- ✅ إعداد Redis
- ✅ إنشاء هيكل المشروع
- ✅ إعداد logging system

**Day 3-4: Core Models & Repositories**
- ✅ تطوير Domain Models
- ✅ تطوير Repository Layer
- ✅ كتابة Unit Tests للـ models
- ✅ إعداد Database migrations

**Day 5-7: Basic Services**
- ✅ FileManager Service
- ✅ QuotaManager Service
- ✅ SubscriptionManager Service
- ✅ Integration tests

### 📅 Phase 2: Bot & File Management (Week 2)

**Day 8-10: Telegram Bot**
- ✅ إعداد python-telegram-bot
- ✅ تطوير Command Handlers
- ✅ تطوير Callback Handlers
- ✅ Conversation flows

**Day 11-12: File Operations**
- ✅ رفع الملفات
- ✅ حذف الملفات
- ✅ إنشاء المجلدات
- ✅ عرض شجرة الملفات

**Day 13-14: Bot Hosting**
- ✅ BotHosting Service
- ✅ Webhook setup logic
- ✅ PHP-FPM integration
- ✅ Testing

### 📅 Phase 3: Subscription & Quota (Week 3)

**Day 15-17: Subscription System**
- ✅ Subscription management
- ✅ Plan upgrade/downgrade
- ✅ Expiry checking
- ✅ Notification system

**Day 18-19: Quota Enforcement**
- ✅ Real-time quota checking
- ✅ Cache integration
- ✅ Usage calculation
- ✅ Limit enforcement

**Day 20-21: Background Tasks**
- ✅ Subscription checker task
- ✅ Quota calculator task
- ✅ Notification sender task
- ✅ Cleanup tasks

### 📅 Phase 4: Deployment & Testing (Week 4)

**Day 22-24: Railway Deployment**
- ✅ Dockerfile optimization
- ✅ Railway configuration
- ✅ Environment setup
- ✅ Volume configuration
- ✅ PostgreSQL & Redis setup

**Day 25-26: Security & Performance**
- ✅ Security hardening
- ✅ Rate limiting
- ✅ Performance optimization
- ✅ Load testing

**Day 27-28: Final Testing & Launch**
- ✅ End-to-end testing
- ✅ Bug fixes
- ✅ Documentation
- ✅ Launch! 🚀

---

## 🎯 Success Metrics

### 📊 KPIs to Track

1. **Technical Metrics**
   - Uptime: > 99.5%
   - Response time: < 200ms (p95)
   - Error rate: < 0.1%
   - Database query time: < 50ms (p95)

2. **User Metrics**
   - Daily Active Users (DAU)
   - Monthly Active Users (MAU)
   - User retention rate
   - Average session duration

3. **Business Metrics**
   - Free to Pro conversion rate
   - Average revenue per user (ARPU)
   - Churn rate
   - Customer lifetime value (CLV)

---

## 🔮 Future Enhancements (Phase 2)

### 🚀 Planned Features

1. **Developer API** (Priority: High)
   - RESTful API للمطورين
   - API key management
   - Rate limiting per API key
   - Documentation (Swagger/OpenAPI)

2. **Web Dashboard** (Priority: Medium)
   - File editor في المتصفح
   - Real-time logs viewer
   - Analytics dashboard
   - Bot management UI

3. **AI Integration** (Priority: Medium)
   - Code error detection
   - Auto-fix suggestions
   - Code generation
   - Security scanning

4. **Marketplace** (Priority: Low)
   - Bot templates marketplace
   - User ratings & reviews
   - Payment integration
   - Revenue sharing

5. **Advanced Features** (Priority: Low)
   - Git integration
   - Automated backups
   - Staging environments
   - Custom domains
   - CDN integration

---

## 💡 Key Improvements Over Reference Bot

### ✨ Architecture Improvements

| Aspect | Reference Bot | New Bot |
|--------|---------------|---------|
| **Database** | SQLite | PostgreSQL (scalable) |
| **Bot Framework** | Telethon | python-telegram-bot (better for bots) |
| **Architecture** | Monolithic | Layered (separation of concerns) |
| **Caching** | File-based | Redis (fast & distributed) |
| **Code Structure** | Mixed responsibilities | Clean architecture |
| **Testing** | Minimal | Comprehensive test coverage |
| **Logging** | Basic | Structured logging |
| **Error Handling** | Basic | Robust error handling |
| **Scalability** | Limited | Highly scalable |
| **Deployment** | Docker only | Railway-optimized |

### 🎯 Feature Improvements

1. **Better Quota System**
   - Real-time tracking
   - Cached for performance
   - Accurate calculations
   - Proactive warnings

2. **Improved Security**
   - Better PHP sandboxing
   - Rate limiting
   - Input validation
   - Audit logging

3. **Better UX**
   - Clearer commands
   - Better error messages
   - Progress indicators
   - Inline keyboards

4. **Performance**
   - Faster response times
   - Better caching
   - Optimized queries
   - Async operations

---

## 📚 Dependencies (requirements.txt)

```txt
# Core
python-telegram-bot==21.0
fastapi==0.110.0
uvicorn[standard]==0.27.0

# Database
sqlalchemy==2.0.27
asyncpg==0.29.0
alembic==1.13.1

# Cache & Queue
redis==5.0.1
hiredis==2.3.2

# Async
aiofiles==23.2.1
aiohttp==3.9.3
httpx==0.26.0

# Validation & Config
pydantic==2.6.1
pydantic-settings==2.1.0
python-dotenv==1.0.1

# Logging
structlog==24.1.0
python-json-logger==2.0.7

# Background Tasks
apscheduler==3.10.4

# Security
cryptography==42.0.2
python-multipart==0.0.9

# Utilities
python-dateutil==2.8.2
pytz==2024.1

# Development
pytest==8.0.0
pytest-asyncio==0.23.5
pytest-cov==4.1.0
black==24.2.0
ruff==0.2.2
```

---

## 🎓 Best Practices Applied

### 🏗️ Code Quality

1. **SOLID Principles**
   - Single Responsibility
   - Open/Closed
   - Liskov Substitution
   - Interface Segregation
   - Dependency Inversion

2. **Clean Code**
   - Meaningful names
   - Small functions
   - Clear comments
   - Consistent formatting

3. **Error Handling**
   - Custom exceptions
   - Proper logging
   - User-friendly messages
   - Graceful degradation

4. **Testing**
   - Unit tests
   - Integration tests
   - E2E tests
   - Test coverage > 70%

---

## 📖 Documentation Plan

### 📝 Documentation Structure

```
docs/
├── README.md                    # Project overview
├── SETUP.md                     # Setup instructions
├── DEPLOYMENT.md                # Deployment guide
├── API.md                       # API documentation
├── ARCHITECTURE.md              # This file
├── CONTRIBUTING.md              # Contribution guidelines
└── CHANGELOG.md                 # Version history
```

---

## ✅ Conclusion

هذه الخطة المعمارية توفر:

1. ✅ **معمارية قوية وقابلة للتوسع** - Layered architecture مع separation of concerns
2. ✅ **قاعدة بيانات قوية** - PostgreSQL بدلاً من SQLite
3. ✅ **أداء عالي** - Redis caching + optimized queries
4. ✅ **أمان محسّن** - Multiple security layers
5. ✅ **سهولة الصيانة** - Clean code + comprehensive tests
6. ✅ **جاهز للنشر على Railway** - Optimized for Railway platform
7. ✅ **قابل للتوسع المستقبلي** - Easy to add new features

**الخطوة التالية:** البدء في التنفيذ حسب الـ Roadmap! 🚀

---

**تاريخ الإنشاء:** 28 مايو 2026  
**الإصدار:** 1.0  
**الحالة:** Ready for Implementation ✅


