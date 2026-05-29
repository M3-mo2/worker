<?php
/**
 * PHP Host Security Scanner
 * Tests environment isolation, file access restrictions, and sensitive file exposure.
 * READ-ONLY: Does not modify or delete any files.
 */

header('Content-Type: text/plain; charset=utf-8');

echo "============================================\n";
echo "  PHP Host Security Scanner\n";
echo "============================================\n\n";

echo "[*] Basic Info\n";
echo "  PHP Version    : " . phpversion() . "\n";
echo "  SAPI           : " . PHP_SAPI . "\n";
echo "  OS             : " . PHP_OS . "\n";
echo "  Server IP      : " . ($_SERVER['SERVER_ADDR'] ?? 'N/A') . "\n";
echo "  Client IP      : " . ($_SERVER['REMOTE_ADDR'] ?? 'N/A') . "\n";
echo "  Script Path    : " . __FILE__ . "\n";
echo "  Document Root  : " . ($_SERVER['DOCUMENT_ROOT'] ?? 'N/A') . "\n\n";

// ─── Disabled Functions ─────────────────────────────────────────────
echo "[*] Disabled Functions\n";
$disabled = ini_get('disable_functions');
echo "  " . ($disabled ?: '(none)') . "\n\n";

// ─── open_basedir ───────────────────────────────────────────────────
echo "[*] open_basedir\n";
$obd = ini_get('open_basedir');
echo "  " . ($obd ?: '(not set — unrestricted)') . "\n\n";

// ─── Critical INI Settings ──────────────────────────────────────────
$checks = [
    'allow_url_fopen'  => 'URL file open',
    'allow_url_include'=> 'URL inclusion',
    'exec_enabled'     => 'exec() enabled', // custom
    'display_errors'   => 'Display errors',
    'file_uploads'     => 'File uploads',
];
foreach ($checks as $k => $label) {
    $v = ini_get($k);
    if ($v === false) $v = 'not found';
    elseif (in_array(strtolower($v), ['', '0', 'off', 'false'])) $v = 'OFF';
    else $v = 'ON';
    echo "  {$label}: {$v}\n";
}
echo "\n";

// ─── Directory Traversal / Sensitive Files ──────────────────────────
echo "[*] Sensitive File Access\n";
$targets = [
    '/etc/passwd',
    '/etc/shadow',
    '/etc/hosts',
    '/etc/hostname',
    '/proc/1/environ',
    '/proc/self/environ',
    '/proc/self/cmdline',
    '/proc/self/status',
    '/.env',
    '/../.env',
    '/vendor/.env',
    '/.git/config',
    '/../.git/config',
    '/var/log/auth.log',
    '/var/log/syslog',
    '/root/.bash_history',
    '/home/*/.ssh/id_rsa',
    '/home/*/.ssh/authorized_keys',
];

foreach ($targets as $path) {
    $expanded = str_replace('*', 'dummy', $path);
    $accessible = @file_get_contents($expanded, false, null, 0, 128);
    if ($accessible !== false) {
        echo "  ⚠ ACCESSIBLE: {$path}\n";
        echo "    -> " . bin2hex(substr($accessible, 0, 64)) . "...\n";
    } else {
        echo "  ✓ BLOCKED: {$path}\n";
    }
}
echo "\n";

// ─── Parent Directory Traversal ─────────────────────────────────────
echo "[*] Directory Traversal\n";
for ($i = 1; $i <= 5; $i++) {
    $path = str_repeat('../', $i);
    $real = @realpath(__DIR__ . '/' . $path);
    if ($real && strpos($real, __DIR__) !== 0) {
        echo "  ⚠ Escaped {$i} level(s): {$real}\n";
    } else {
        $display = $real ?: 'blocked';
        echo "  ✓ Level {$i}: {$display}\n";
    }
}
echo "\n";

// ─── Writable Directories ───────────────────────────────────────────
echo "[*] Writable Locations\n";
$writable_checks = [
    __DIR__,
    __DIR__ . '/../',
    '/tmp',
    '/var/tmp',
    sys_get_temp_dir(),
];
foreach ($writable_checks as $dir) {
    $r = @realpath($dir);
    if ($r && @is_writable($r)) {
        echo "  ⚠ WRITABLE: {$r}\n";
        $test = @file_put_contents($r . '/.security_test_tmp', 'test');
        if ($test !== false) {
            @unlink($r . '/.security_test_tmp');
            echo "    -> confirmed writable\n";
        }
    } else {
        echo "  ✓ NOT writable: " . ($r ?: $dir) . "\n";
    }
}
echo "\n";

// ─── Network Capabilities ───────────────────────────────────────────
echo "[*] Network Access\n";
$net_tests = [
    'fsockopen'  => function_exists('fsockopen'),
    'curl_init'  => function_exists('curl_init'),
    'stream_context_create' => function_exists('stream_context_create'),
    'dns_get_record' => function_exists('dns_get_record'),
    'gethostbynamel' => function_exists('gethostbynamel'),
];
foreach ($net_tests as $name => $avail) {
    echo "  {$name}: " . ($avail ? 'AVAILABLE' : 'DISABLED') . "\n";
}

// Attempt external connection (read-only HTTP GET)
if (function_exists('fsockopen') || function_exists('curl_init')) {
    echo "\n  Testing outbound HTTP ... ";
    $ctx = stream_context_create(['http' => ['timeout' => 5, 'method' => 'GET']]);
    $result = @file_get_contents('https://httpbin.org/get', false, $ctx, 0, 1);
    if ($result !== false) {
        echo "PASS (outbound allowed)\n";
    } else {
        echo "FAIL (outbound blocked)\n";
    }
}
echo "\n";

// ─── System Command Execution ───────────────────────────────────────
echo "[*] Command Execution\n";
$cmds = [
    'whoami'       => 'whoami 2>/dev/null',
    'id'           => 'id 2>/dev/null',
    'pwd'          => 'pwd 2>/dev/null',
    'ls /'         => 'ls / 2>/dev/null',
    'cat /etc/passwd' => 'cat /etc/passwd 2>/dev/null',
    'env'          => 'env 2>/dev/null',
];
foreach ($cmds as $label => $cmd) {
    $output = null; $rc = -1;
    // Try shell_exec
    if (function_exists('shell_exec')) {
        $output = shell_exec($cmd);
    } elseif (function_exists('exec')) {
        exec($cmd, $outArr, $rc);
        $output = implode("\n", $outArr);
    } elseif (function_exists('system')) {
        ob_start();
        system($cmd, $rc);
        $output = ob_get_clean();
    } elseif (function_exists('passthru')) {
        ob_start();
        passthru($cmd, $rc);
        $output = ob_get_clean();
    } elseif (function_exists('popen')) {
        $h = popen($cmd, 'r');
        if ($h) { $output = stream_get_contents($h); pclose($h); }
    }
    if ($output !== null && strlen(trim($output)) > 0) {
        echo "  ⚠ '{$label}' returned:\n";
        foreach (explode("\n", trim($output)) as $line) {
            echo "    | {$line}\n";
        }
    } else {
        echo "  ✓ {$label}: blocked\n";
    }
}
echo "\n";

// ─── PHP Functions That Can Leak Info ───────────────────────────────
echo "[*] Dangerous / Info-Leaking Functions\n";
$funcs = [
    'phpinfo', 'eval', 'assert', 'system', 'exec', 'shell_exec',
    'passthru', 'popen', 'proc_open', 'pcntl_exec', 'dl',
    'mail', 'putenv', 'ini_set', 'apache_child_terminate',
    'posix_mkfifo', 'posix_getpwuid', 'posix_kill',
];
foreach ($funcs as $f) {
    echo "  {$f}: " . (function_exists($f) ? 'ENABLED' : 'DISABLED') . "\n";
}
echo "\n";

// ─── PHP Classes / Extensions ───────────────────────────────────────
echo "[*] Loaded Extensions (security-relevant)\n";
$ext_filter = ['PDO', 'mysqli', 'mysql', 'pgsql', 'sqlite3', 'ssh2', 'ftp', 'sockets', 'pcntl', 'posix', 'apcu', 'redis', 'memcached', 'imagick', 'exec'];
$loaded = get_loaded_extensions();
sort($loaded);
foreach ($loaded as $ext) {
    if (in_array(strtolower($ext), array_map('strtolower', $ext_filter))) {
        echo "  {$ext} (loaded)\n";
    }
}

echo "\n============================================\n";
echo "  Scan Complete\n";
echo "============================================\n";
