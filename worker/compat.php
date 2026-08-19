<?php
// Compatibility prepend for user bots written for a hosting/framework that
// injects globals/constants (ID, TOKEN, $update, $message, $chatID, ...)
// before running the bot file. Runs before the user's bot (auto_prepend_file).
//
// Opt-out: drop a file named `__nocompat` in the bot folder to disable the
// injection (keeps php://input intact for standard bots that read it).
// Injection is ON by default so existing bots start working as soon as the
// worker is redeployed (their old config.json may lack the "compat" flag).

$__script = $_SERVER['SCRIPT_FILENAME'] ?? '';
$__dir = is_string($__script) ? dirname($__script) : '';

// 1) Pin CWD to the bot's own folder (so relative writes stay confined).
if ($__dir && is_dir($__dir)) {
    @chdir($__dir);
}

// 2) Load config (for TOKEN); inject unless explicitly opted out.
$__cfgPath = $__dir . '/config.json';
$__cfg = is_file($__cfgPath) ? json_decode(@file_get_contents($__cfgPath), true) : [];

if (!is_file($__dir . '/__nocompat')) {
    // 3) Static values (no request body needed).
    if (preg_match('#/user_bots/(\d+)/#', $__script, $__m) && !defined('ID')) {
        define('ID', (int) $__m[1]);
    }
    if (!empty($__cfg['bot_token']) && !defined('TOKEN')) {
        define('TOKEN', $__cfg['bot_token']);
    }
    if (!defined('API')) {
        define('API', 'https://api.telegram.org');
    }
    if (!defined('BOT_API')) {
        define('BOT_API', 'https://api.telegram.org');
    }

    // 4) Per-request values from the webhook body (safe to consume input here,
    //    because compat-on bots rely on these globals instead of reading it).
    $__raw = @file_get_contents('php://input');
    $GLOBALS['RAW_INPUT'] = $__raw;
    $__u = $__raw ? json_decode($__raw, true) : null;
    if (is_array($__u)) {
        $GLOBALS['update'] = $__u;
        $GLOBALS['message'] = $__u['message'] ?? null;
        $m = $GLOBALS['message'];
        if (is_array($m)) {
            $GLOBALS['chatID']   = $m['chat']['id'] ?? null;
            $GLOBALS['chat_id']  = $GLOBALS['chatID'];
            $GLOBALS['text']     = $m['text'] ?? '';
            $GLOBALS['fromID']   = $m['from']['id'] ?? null;
            $GLOBALS['from_id']  = $GLOBALS['fromID'];
            $GLOBALS['userID']   = $GLOBALS['fromID'];
            $GLOBALS['firstName']= $m['from']['first_name'] ?? '';
            $GLOBALS['username'] = $m['from']['username'] ?? '';
        }
        if (!empty($__u['callback_query'])) {
            $GLOBALS['callback_query'] = $__u['callback_query'];
            $GLOBALS['cbdata'] = $__u['callback_query']['data'] ?? '';
        }
        // $z1: framework-specific; extend here once a sample file is provided.
    }
}
