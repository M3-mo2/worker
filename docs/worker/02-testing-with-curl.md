# Worker Service - اختبار بـ curl (A to Z)

## المتطلبات قبل البدء

```
1. الـ Worker شغال على Railway (أو محلي)
2. عندك INTERNAL_SECRET (أنشئته في Railway - شوف الخطوة التالية)
3. عندك bot_token من تيليجرام (من @BotFather)
4. عندك ملف PHP جاهز للاختبار
```

---

## الخطوة 0: إعداد Environment Variables على Railway

قبل ما تختبر، لازم المتغيرات دي تكون موجودة في Railway dashboard:

```
1. افتح مشروعك على Railway
2. اختر الـ Worker service
3. روح على تب "Variables"
4. أضف المتغيرات دي:
```

| المتغير | الشرح | مثال |
|---------|-------|------|
| `INTERNAL_SECRET` | سر تنتجه أنت (مش متغير Railway) | `my_super_secret_key_123` |
| `MAIN_BOT_URL` | عنوان البوت الأساسي | `https://main-bot.up.railway.app` |

**ملاحظة مهمة:** `INTERNAL_SECRET` مش متغير Railway جاهز — ده سر تنتجه أنت وتكتبه في Variables. أي نص معقد ينفع، مثلاً:

```bash
# توليد سر عشوائي (في الـ terminal)
openssl rand -hex 32
# النتيجة مثلاً: a1b2c3d4e5f6...
```

`RAILWAY_PUBLIC_DOMAIN` بيتحدد تلقائياً من Railway — مش محتاج تضيفه.

---

## الخطوة 0.5: تحديد المتغيرات للاختبار المحلي

```bash
# عنوان الـ Worker (غيّره حسب عنوانك)
export WORKER_URL="https://your-worker-url.up.railway.app"

# السر المشترك (نفس القيمة اللي حطيتها في Railway)
export SECRET="26c29f5306ee74dd9517bafee1d1a9560081145df7551af5fa9d2eec9fba0e42"

# رقم المستخدم (أي رقم للاختبار)
export USER_ID="12345"

# توكن البوت من تيليجرام
export BOT_TOKEN="8651434899:AAGpWO75_oqavjPUb3DKBrc6hG2YNcifcLk"
```

---

## الخطوة 1: التأكد إن الـ Worker شغال (Health Check)

```bash
curl -X GET "$WORKER_URL/health"
```

**المتوقع:**
```json
{
  "status": "ok",
  "timestamp": 1717123456.789
}
```

**لو مش شغال:** تأكد إن Railway الـ deployment نجح وإن البورت صح.

---

## الخطوة 2: إنشاء ملف PHP للاختبار

```bash
cat > /tmp/test_bot.php << 'PHP'
<?php
$input = file_get_contents('php://input');
$update = json_decode($input, true);

if (!$update) {
    http_response_code(200);
    echo 'ok';
    exit;
}

$message = $update['message'] ?? null;
if (!$message) {
    http_response_code(200);
    echo 'ok';
    exit;
}

$chat_id = $message['chat']['id'];
$text = $message['text'] ?? '';
$bot_token = 'BOT_TOKEN_HERE';

if ($text === '/start') {
    $reply = "أهلاً! أنا بوت اختبار.";
} elseif ($text === '/help') {
    $reply = "الأوامر المتاحة:\n/start - بدء\n/help - مساعدة\n/info - معلومات";
} elseif ($text === '/info') {
    $reply = "User ID: " . $message['from']['id'] . "\nChat ID: " . $chat_id;
} else {
    $reply = "قلت: " . $text;
}

$url = "https://api.telegram.org/bot{$bot_token}/sendMessage";
$data = json_encode([
    'chat_id' => $chat_id,
    'text' => $reply,
]);

$ch = curl_init($url);
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, $data);
curl_setopt($ch, CURLOPT_HTTPHEADER, ['Content-Type: application/json']);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_exec($ch);
curl_close($ch);

http_response_code(200);
echo 'ok';
```

**ملاحظة:** استبدل `BOT_TOKEN_HERE` بالتوكن الحقيقي، أو سيبه كده لأن الـ Worker مش بيحتاجه (التوكن بيتحفظ عنده).

---

## الخطوة 3: نشر البوت (Deploy)

```bash
curl -X POST "$WORKER_URL/deploy" \
  -H "X-Internal-Secret: $SECRET" \
  -F "user_id=$USER_ID" \
  -F "bot_token=$BOT_TOKEN" \
  -F "file=@/tmp/test_bot.php"
```

** الشرح:**
- `-X POST` → نوع الطلب POST
- `-H "X-Internal-Secret: ..."` → السر المشترك (مطلوب في كل API)
- `-F "user_id=12345"` → رقم المستخدم
- `-F "bot_token=..."` → توكن البوت من تيليجرام
- `-F "file=@/tmp/test_bot.php"` → ملف الـ PHP (@ معناها اقرأ من الملف)

**المتوقع (نجاح):**
```json
{
  "status": "ok",
  "user_id": 12345,
  "message": "Bot deployed successfully"
}
```

**المتوقع (فشل - سر غلط):**
```json
{
  "detail": "Invalid secret"
}
```
الحالة: 403 Forbidden

**الموقع (فشل - ملف مش PHP):**
```json
{
  "detail": "Only .php files are allowed"
}
```
الحالة: 400 Bad Request

**المتوقع (فشل - ملف فاضي):**
```json
{
  "detail": "Empty file"
}
```
الحالة: 400 Bad Request

---

## الخطوة 4: التأكد إن البوت اتسجل

```bash
curl -X GET "$WORKER_URL/status/$USER_ID" \
  -H "X-Internal-Secret: $SECRET"
```

**المتوقع:**
```json
{
  "user_id": 12345,
  "status": "running",
  "created_at": 1717123456.789
}
```

**لو status = "running"** → البوت اتسجل بنجاح على تيليجرام!

---

## الخطوة 5: اختبار البوت على تيليجرام

```
1. افتح تيليجرام
2. دور على البوت بتاعك بالتوكن
3. ابعتله /start
4. المفروض يرد عليك: "أهلاً! أنا بوت اختبار."
```

**لو ماردش:** شوف الخطوة 6 عشان ت debug.

---

## الخطوة 6: Debug لو البوت مش بيرد

### 6.1 تأكد إن الـ webhook اتسجل

```bash
curl -X GET "https://api.telegram.org/bot$BOT_TOKEN/getWebhookInfo"
```

**المتوقع:**
```json
{
  "ok": true,
  "result": {
    "url": "https://your-worker-url.up.railway.app/webhook/12345",
    "has_custom_certificate": false,
    "pending_update_count": 0,
    "last_error_date": 0,
    "last_error_message": "",
    "max_connections": 40
  }
}
```

**لو `url` فاضي** → الـ webhook متسجلش. تأكد إن Deploy نجح.

**لو `last_error_message` فيه حاجة** → فيه مشكلة في الـ Worker. شوف اللوجات.

### 6.2 شوف لوجات الـ Worker على Railway

```
1. افتح Railway dashboard
2. اختر الـ Worker service
3. روح على Deployments
4. اضغط على آخر deployment
5. شوف الـ Logs
```

**أو من الـ CLI:**
```bash
railway logs
```

### 6.3 اختبر الـ webhook يدوياً

```bash
curl -X POST "$WORKER_URL/webhook/$USER_ID" \
  -H "Content-Type: application/json" \
  -H "X-Telegram-Bot-Api-Secret-Token: WEBHOOK_SECRET" \
  -d '{
    "update_id": 1,
    "message": {
      "message_id": 1,
      "from": {"id": 999, "first_name": "Test"},
      "chat": {"id": 999, "type": "private"},
      "date": 1717123456,
      "text": "/start"
    }
  }'
```

**ملاحظة:** `WEBHOOK_SECRET` لازم يكون نفس السر اللي اتولد لما عملت deploy. لو مش عارفه، شوفه في `bots.json` أو في لوجات الـ Worker.

---

## الخطوة 7: إيقاف البوت (Stop)

```bash
curl -X POST "$WORKER_URL/stop" \
  -H "X-Internal-Secret: $SECRET" \
  -H "Content-Type: application/json" \
  -d "{\"user_id\": $USER_ID}"
```

**المتوقع:**
```json
{
  "status": "ok",
  "user_id": 12345,
  "message": "Bot stopped"
}
```

**اللي بيحصل جوه:**
1. الـ webhook بيت حذف من تيليجرام
2. حالة البوت بتتغير لـ "stopped"
3. لو حد بعت رسالة للبوت، الـ Worker مش هيعمل حاجة

---

## الخطوة 8: التأكد إن ال봇 وقف

```bash
curl -X GET "$WORKER_URL/status/$USER_ID" \
  -H "X-Internal-Secret: $SECRET"
```

**المتوقع:**
```json
{
  "user_id": 12345,
  "status": "stopped",
  "created_at": 1717123456.789
}
```

---

## الخطوة 9: إعادة تشغيل البوت

```bash
# Deploy تاني بنفس الملف
curl -X POST "$WORKER_URL/deploy" \
  -H "X-Internal-Secret: $SECRET" \
  -F "user_id=$USER_ID" \
  -F "bot_token=$BOT_TOKEN" \
  -F "file=@/tmp/test_bot.php"
```

---

## اختبارات إضافية

### اختبار رفض الملفات غير PHP

```bash
echo "not a php file" > /tmp/test.txt

curl -X POST "$WORKER_URL/deploy" \
  -H "X-Internal-Secret: $SECRET" \
  -F "user_id=$USER_ID" \
  -F "bot_token=$BOT_TOKEN" \
  -F "file=@/tmp/test.txt"
```

**المتوقع:**
```json
{
  "detail": "Only .php files are allowed"
}
```
الحالة: 400

### اختبار رفض السر الغلط

```bash
curl -X GET "$WORKER_URL/status/$USER_ID" \
  -H "X-Internal-Secret: wrong_secret"
```

**المتوقع:**
```json
{
  "detail": "Invalid secret"
}
```
الحالة: 403

### اختبار حالة بوت مش موجود

```bash
curl -X GET "$WORKER_URL/status/99999" \
  -H "X-Internal-Secret: $SECRET"
```

**المتوقع:**
```json
{
  "user_id": 99999,
  "status": "not_found"
}
```

### اختبار إيقاف بوت مش موجود

```bash
curl -X POST "$WORKER_URL/stop" \
  -H "X-Internal-Secret: $SECRET" \
  -H "Content-Type: application/json" \
  -d '{"user_id": 99999}'
```

**المتوقع:**
```json
{
  "detail": "Bot not found"
}
```
الحالة: 404

### اختبار Payload كبير (أكبر من 1MB)

```bash
# إنشاء ملف كبير
python3 -c "print('<?php echo \"ok\"; ?> ' * 500000)" > /tmp/big_bot.php

curl -X POST "$WORKER_URL/deploy" \
  -H "X-Internal-Secret: $SECRET" \
  -F "user_id=$USER_ID" \
  -F "bot_token=$BOT_TOKEN" \
  -F "file=@/tmp/big_bot.php"
```

**المتوقع:**
```json
{
  "detail": "File too large (max 10MB)"
}
```
الحالة: 413

---

## السكريبت الكامل (نسخ واللصق)

```bash
#!/bin/bash
# === Worker Test Script ===

# المتغيرات (غيّرها حسب وضعك)
WORKER_URL="https://your-worker-url.up.railway.app"
SECRET="your_internal_secret_here"
USER_ID="12345"
BOT_TOKEN="1234567890:ABCdefGHIjklMNOpqrsTUVwxyz"

echo "=== 1. Health Check ==="
curl -s "$WORKER_URL/health" | python3 -m json.tool
echo ""

echo "=== 2. Create Test PHP File ==="
cat > /tmp/test_bot.php << 'PHP'
<?php
$input = file_get_contents('php://input');
$update = json_decode($input, true);
if (!$update) { http_response_code(200); echo 'ok'; exit; }
$message = $update['message'] ?? null;
if (!$message) { http_response_code(200); echo 'ok'; exit; }
$chat_id = $message['chat']['id'];
$text = $message['text'] ?? '';
$bot_token = 'BOT_TOKEN_HERE';
if ($text === '/start') { $reply = "أهلاً! أنا بوت اختبار."; }
else { $reply = "قلت: " . $text; }
$url = "https://api.telegram.org/bot{$bot_token}/sendMessage";
$data = json_encode(['chat_id' => $chat_id, 'text' => $reply]);
$ch = curl_init($url);
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, $data);
curl_setopt($ch, CURLOPT_HTTPHEADER, ['Content-Type: application/json']);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_exec($ch);
curl_close($ch);
http_response_code(200);
echo 'ok';
PHP
echo "File created at /tmp/test_bot.php"
echo ""

echo "=== 3. Deploy Bot ==="
curl -s -X POST "$WORKER_URL/deploy" \
  -H "X-Internal-Secret: $SECRET" \
  -F "user_id=$USER_ID" \
  -F "bot_token=$BOT_TOKEN" \
  -F "file=@/tmp/test_bot.php" | python3 -m json.tool
echo ""

echo "=== 4. Check Status ==="
curl -s -X GET "$WORKER_URL/status/$USER_ID" \
  -H "X-Internal-Secret: $SECRET" | python3 -m json.tool
echo ""

echo "=== 5. Check Webhook Info ==="
curl -s "https://api.telegram.org/bot$BOT_TOKEN/getWebhookInfo" | python3 -m json.tool
echo ""

echo "=== Done! Go test on Telegram ==="
echo "Bot URL: https://t.me/$(echo $BOT_TOKEN | cut -d: -f1)"
echo ""

read -p "Press Enter to stop the bot..."

echo "=== 6. Stop Bot ==="
curl -s -X POST "$WORKER_URL/stop" \
  -H "X-Internal-Secret: $SECRET" \
  -H "Content-Type: application/json" \
  -d "{\"user_id\": $USER_ID}" | python3 -m json.tool
echo ""

echo "=== 7. Verify Stopped ==="
curl -s -X GET "$WORKER_URL/status/$USER_ID" \
  -H "X-Internal-Secret: $SECRET" | python3 -m json.tool
echo ""

echo "=== Test Complete ==="
```

**لتشغيله:**
```bash
chmod +x test_worker.sh
./test_worker.sh
```

---

## الأخطاء الشائعة وحلولها

| الخطأ | السبب | الحل |
|-------|-------|------|
| `Connection refused` | الـ Worker مش شغال | تأكد إن Railway deployment نجح |
| `Invalid secret` | السر غلط | تأكد من `INTERNAL_SECRET` |
| `Only .php files` | الملف مش `.php` | تأكد إن اسم الملف ينتهي بـ `.php` |
| `File too large` | الملف أكبر من 10MB | قلّل حجم الملف |
| `Telegram error: ...` | التوكن غلط | تأكد من `BOT_TOKEN` |
| `Bot not found` | مفيش بوت بالـ user_id ده | اعمل deploy الأول |
| البوت مش بيرد على تيليجرام | الـ webhook متسجلش أو PHP فيها غلط | شوف الخطوة 6 (Debug) |
| 502 Bad Gateway | PHP-FPM مش شغال | شوف لوجات Railway |

---

## ملخص الخطوات

```
1. Health Check      → GET  /health
2. Deploy            → POST /deploy (file + user_id + bot_token)
3. Check Status      → GET  /status/{user_id}
4. Test on Telegram  → ابعت /start للبوت
5. Debug             → GET  /webhookInfo من تيليجرام API
6. Stop              → POST /stop (user_id)
7. Verify            → GET  /status/{user_id} (يكون stopped)
```
