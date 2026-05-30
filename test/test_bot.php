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

if ($text === '/start') {
    $reply = "أهلاً! أنا بوت اختبار.";
} elseif ($text === '/help') {
    $reply = "الأوامر المتاحة:\n/start - بدء\n/help - مساعدة\n/info - معلومات";
} elseif ($text === '/info') {
    $reply = "User ID: " . $message['from']['id'] . "\nChat ID: " . $chat_id;
} else {
    $reply = "قلت: " . $text;
}

$url = "https://api.telegram.org/bot{$_ENV['BOT_TOKEN']}/sendMessage";
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
