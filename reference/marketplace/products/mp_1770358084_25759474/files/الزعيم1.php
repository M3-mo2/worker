<?php
/*
تنشر اذكر الصدر @THTSS
*/
ob_start();
$API_KEY = '8519056610:AAE8nREIrG1gUVAfuXdu9Nk1DWEGjzq4Neg';
define('API_KEY',$API_KEY);
echo file_get_contents("https://api.telegram.org/bot" . API_KEY . "/setwebhook?url=" . $_SERVER['SERVER_NAME'] . "" . $_SERVER['SCRIPT_NAME']);
            function bot($method,$datas=[]){
    $ALI = http_build_query($datas);
        $url = "https://api.telegram.org/bot".API_KEY."/".$method."?$ALI";
        $XT1XT1 = file_get_contents($url);
        return json_decode($XT1XT1);
}
$buyy = "Mi2k_12";
$alwsh = "@Mi2k_12";
$sudo = "7897598134";
$Dev = array("7897598134","",""); //ID ADMIN NUMBER 1 HE CHAT
//****************//
@$usernamebot = "V_JLBOT"; //UserName Bot
@$channel = "@zz57j"; // UserName Channel don't @
@$token = API_KEY;
$update = json_decode(file_get_contents('php://input'));
@$message = $update->message;
@$from_id = $message->from->id;
@$chat_id = $message->chat->id;
@$message_id = $message->message_id;
@$first_name = $message->from->first_name;
@$last_name = $message->from->last_name;
@$username = $message->from->username;
@$text = $message->text;
@$firstname = $update->callback_query->from->first_name;
@$usernames = $update->callback_query->from->username;
@$chatid = $update->callback_query->message->chat->id;
@$fromid = $update->callback_query->from->id;
@$membercall = $update->callback_query->id;
@$reply = $update->message->reply_to_message->forward_from->id;
/*===== dev ~ @OO1OOO =====*/
@$data = $update->callback_query->data;
@$messageid = $update->callback_query->message->message_id;
@$tc = $update->message->chat->type;
@$gpname = $update->callback_query->message->chat->title;
@$namegroup = $update->message->chat->title;
@$text = $update->inline_qurey->qurey;
/*===== dev ~ @OO1OOO =====*/
@$newchatmemberid = $update->message->new_chat_member->id;
@$newchatmemberu = $update->message->new_chat_member->username;
@$rt = $update->message->reply_to_message;
@$replyid = $update->message->reply_to_message->message_id;
@$tedadmsg = $update->message->message_id;
@$edit = $update->edited_message->text;
@$re_id = $update->message->reply_to_message->from->id;
@$re_user = $update->message->reply_to_message->from->username;
@$re_name = $update->message->reply_to_message->from->first_name;
@$re_msgid = $update->message->reply_to_message->message_id;
@$re_chatid = $update->message->reply_to_message->chat->id;
@$message_edit_id = $update->edited_message->message_id;
@$chat_edit_id = $update->edited_message->chat->id;
@$edit_for_id = $update->edited_message->from->id;
@$edit_chatid = $update->callback_query->edited_message->chat->id;
@$caption = $update->message->caption;
$chatid3=$update->message->chat->id;
$fromid3=$update->message->from->id;
$text=$update->message->text;
$mid=$update->message->message_id;
$update = json_decode(file_get_contents("php://input"));

// --- قسم استقبال البيانات من الأزرار الشفافة (Callback Query) ---
if(isset($update->callback_query)){
    $data = $update->callback_query->data;
    $chat_id = $update->callback_query->message->chat->id;
    $from_id = $update->callback_query->from->id;
    $message_id = $update->callback_query->message->message_id;
    $name = $update->callback_query->from->first_name;
    $username = $update->callback_query->from->username;
    $callback_query_id = $update->callback_query->id;

    // محرك تحويل الضغطة إلى نص ليدخل في شرط if text
    if($data == "twins_section"){
        $text = "🧬 قـسـم تـويـنـس";
    }
}

// --- قسم استقبال الرسائل النصية (Message) ---
if(isset($update->message)){
    $message = $update->message;
    $text = $message->text;
    $chat_id = $message->chat->id;
    $from_id = $message->from->id;
    $message_id = $message->message_id;
    $first_name = $message->from->first_name;
    $last_name = $message->from->last_name;
    $username = $message->from->username;
    $tc = $message->chat->type;
    $caption = $message->caption;
    $reply_to_message = $message->reply_to_message;
}

// --- بقية المتغيرات التي طلبت الحفاظ عليها لضمان عمل الملف القديم ---
$chatid = $chat_id; 
$fromid = $from_id;
$messageid = $message_id;
$mid = $message_id;

/*===== dev ~ @OO1OOO =====*/
@$statjson = json_decode(file_get_contents("https://api.telegram.org/bot$token/getChatMember?chat_id=$chat_id&user_id=".$from_id),true);
@$status = $statjson['result']['status'];
@$statjsonrt = json_decode(file_get_contents("https://api.telegram.org/bot$token/getChatMember?chat_id=$chat_id&user_id=".$re_id),true);
@$statusrt = $statjsonrt['result']['status'];
@$statjsonq = json_decode(file_get_contents("https://api.telegram.org/bot$token/getChatMember?chat_id=$chatid&user_id=".$fromid),true);
@$statusq = $statjsonq['result']['status'];
@$info = json_decode(file_get_contents("https://api.telegram.org/bot$token/getChatMember?chat_id=$chat_edit_id&user_id=".$edit_for_id),true);
@$you = $info['result']['status'];
@$forchannel = json_decode(file_get_contents("https://api.telegram.org/bot".$token."/getChatMember?chat_id=@".$channel."&user_id=".$from_id));
@$tch = $forchannel->result->status;
$title =$message->chat->title;
$rep = $message->reply_to_message;
/*===== dev ~ @OO1OOO =====*/
@$settings = json_decode(file_get_contents("data/$chat_id.json"),true);
@$settings2 = json_decode(file_get_contents("data/$chatid.json"),true);
@$editgetsettings = json_decode(file_get_contents("data/$chat_edit_id.json"),true);
@$user = json_decode(file_get_contents("data/user.json"),true);
@$filterget = $settings["filterlist"];

/*===== فاكشن =====*/
function SendMessage($chat_id, $text){
bot('sendMessage',[
'chat_id'=>$chat_id,
'text'=>$text,
'parse_mode'=>'MarkDown']);
}
 function Forward($berekoja,$azchejaei,$kodompayam)
{
bot('ForwardMessage',[
'chat_id'=>$berekoja,
'from_chat_id'=>$azchejaei,
'message_id'=>$kodompayam
]);
}
function  getUserProfilePhotos($token,$from_id) {
  @$url = 'https://api.telegram.org/bot'.$token.'/getUserProfilePhotos?user_id='.$from_id;
  @$result = file_get_contents($url);
  @$result = json_decode ($result);
  @$result = $result->result;
  return $result;
}
function check_filter($str){
global $filterget;
foreach($filterget as $d){
	if (mb_strpos($str, $d) !== false) {
		return true;
}
}
}
if ($tc == 'private'){  
@$user = json_decode(file_get_contents("data/user.json"),true);
if(!in_array($from_id, $user["userlist"])) {
$user["userlist"][]="$from_id";
$user = json_encode($user,true);
file_put_contents("data/user.json",$user);
}
}
elseif ($tc == 'group' | $tc == 'supergroup'){  
@$user = json_decode(file_get_contents("data/user.json"),true);
if(!in_array($chat_id, $user["grouplist"])) {
$user["grouplist"][]="$chat_id";
$user = json_encode($user,true);
file_put_contents("data/user.json",$user);
}
}
$message_id = $update->message->message_id;
$user          = $update->message->from->username;
$from_id     = $message->from->id;
$re         = $update->message->reply_to_message;


mkdir("data/member");
mkdir("data/member/$chat_id");

$Cmember = file_get_contents("data/member/$chat_id/Cmember.txt");
$CCmember = file_get_contents("data/member/$chat_id/member.txt");
$getCCmember = explode("\n",$CCmember);
//**********************************//
if($text == "/start" | $text =="ايدي" | $text =="تفعيل" | $text =="تعطيل" | $text =="سورس" | $text =="السورس"){
$from_id = $message->from->id;
$join = file_get_contents("https://api.telegram.org/bot".API_KEY."/getChatMember?chat_id=@THTSS&user_id=".$from_id);
if($message && (strpos($join,'"status":"left"') or strpos($join,'"Bad Request: USER_ID_INVALID"') or strpos($join,'"status":"kicked"'))!== false){
bot('sendMessage', [
'chat_id'=>$chat_id,
'text'=>"
👨‍✈️ ¦ مرحبا بگ عزيزي 🙇‍♂،
👾 ¦ لا يمڪنـك استخدام البوت ،
📟 ¦ عليك الإشتراگ في قناة البوت ،
🖲 ¦ القناة ~⪼ @THTSS ،
▂ ▂ ",
'reply_markup'=>json_encode([
      'inline_keyboard'=>[
   [
     ],
   ]
   ])
   ]); return false;}
bot('sendMessage',['chat_id'=>$chat_id, 'text'=>"",'reply_to_message_id'=>$message->$message_id,]);}


$chatid = $update->edited_message->chat->id;
$fromid = $update->edited_message->from->id;
$edit = json_decode(file_get_contents('edit.json'),true);
$editMessage = $update->edited_message;
if($editMessage){
$edit['edit'][$chatid][$fromid] = ($edit['edit'][$chatid][$fromid]+1);
file_put_contents('edit.json', json_encode($edit));
}
if($edit['edit'][$chat_id][$from_id] == null){
$editt = 0;
}else{
$editt = $edit['edit'][$chat_id][$from_id];
}
if($text == 'سكحاتي' | $text== 'تعديلاتي'){
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>' 🧟‍♂¦  عدد تعديلہآتگ آلمـضـآفهہ‌‏ »  
: '.$editt,
🐾
]);
}




//++++++++++++++++++++//
if(in_array($from_id,$Dev)){
$info =  "المطور الاساسي 👨🏻‍💻";
}elseif($status == "creator"){
$info = "المنشئ 👨‍✈️";
}elseif($status == "administrator"){
$info = "المشرف 👨‍✈️";
}elseif(in_array($from_id,$admin_user) ){
$info = "الادمن 💂‍♂";
}elseif(in_array($from_id,$manger) ){
$info = "المدير 👮‍♂";
}elseif(in_array($from_id,$mmyaz) ){
$info = "عضو مميز 👼";
}elseif(in_array($from_id,$developer) ){
$info = "المطور 👨🏻‍💻";
}
 //***************************//
// info developers //
$developers_info = file_get_contents("data/developers/developer.txt");
$developer = explode ("\n",$developers_info);
$developers_infos = file_get_contents("data/developers/developers.txt");
$developers = explode("\n",$developers_infos);
$list_developers ="";
$list_developers = $list_developers."*➺*".$developers_infos."\n➖➖➖➖➖➖➖\n📨¦ الٱيـديـٱت :\n" ."*➺*`".$developers_info . "`";
// info mangers //
$mangers_info = file_get_contents("data/manger/$chat_id.txt");
$manger  = explode("\n",$mangers_info);
$mangers_infos = file_get_contents("data/manger/$chat_id/mange.txt");
$mangers = explode ("\n",$mangers_infos);
// info admins //
$admin_users_info = file_get_contents("data/admin_user/$chat_id.txt");
$admin_user  = explode("\n",$admin_users_info);
$admin_users_infos = file_get_contents("data/admin_user/$chat_id/mange.txt");
$admin_users = explode ("\n",$admin_users_infos);
// info mmaz //
$mmyazs_info = file_get_contents("data/mmyaz/$chat_id.txt");
$mmyaz  = explode("\n",$mmyazs_info);
$mmyazs_infos = file_get_contents("data/mmyaz/$chat_id/mange.txt");
$mmyazs = explode ("\n",$mmyazs_infos);
// info dogs //
$joksss = file_get_contents("data/jok/$chat_id.txt");
$jokid  = explode("\n",$joksss);
$jokl = file_get_contents("data/jok/$chat_id/jok.txt");
$jokll = explode ("\n",$jokl);
$jokv = file_get_contents("data/jok/$chat_id/joks.txt");
$jokss = explode ("\n",$jokv);
// info joks //
$dogsss = file_get_contents("data/dog/$chat_id.txt");
$dogid  = explode("\n",$dogsss);
$dogl = file_get_contents("data/dog/$chat_id/dog.txt");
$dogll = explode ("\n",$dogl);
$dogv = file_get_contents("data/dog/$chat_id/dogs.txt");
$dogss = explode ("\n",$dogv);
// Banslist //
$Bans = file_get_contents("data/ban/$chat_id.txt");
$Banids  = explode("\n",$Bans);
$BansList = file_get_contents("data/ban/$chat_id/list.txt");
$Banlist = explode ("\n",$Banslist);
// silents //
$silentids = file_get_contents("data/silent/$chat_id.txt");
$silents = explode ("\n",$silentids);
$silent1 = file_get_contents("data/silent/$chat_id/list.txt");
$silentlist = explode("\n",$silent1);
// folders auto //
mkdir("data");
mkdir("data/developers");
mkdir("data/dog");
mkdir("data/dog/$chat_id");
mkdir("data/jok");
mkdir("data/ban");
mkdir("data/silent");
mkdir("data/silent/$chat_id");
mkdir("data/ban/$chat_id");
mkdir("data/jok/$chat_id");
mkdir("data/manger");
mkdir("data/manger/$chat_id");
mkdir("data/admin_user");
mkdir("data/admin_user/$chat_id");
mkdir("data/mmyaz");
mkdir("data/mmyaz/$chat_id");
if(!$re_user){
$usew = "$first_name";
}elseif($re_user){
$usew = "@$re_user";
}
if($re and $text == "رفع مطور" and $re_id !=$id_Bot and  in_array($from_id,$Dev) and !in_array($re_id,$developer)){
file_put_contents("data/developers/developer.txt",$re_id ."\n " , FILE_APPEND);
file_put_contents("data/developers/developers.txt","~» (" . "@". $re_user .")  " . "»" . "  (". $re_id .") ". "\n" , FILE_APPEND);
bot('SendMessage',['chat_id'=>$chat_id,
'text'=>"
📬┊العضو » [$usew]
👤┊ايديه » {$re_id}
🎖┊تم رفعه مطور في البوت 
➖
",
'parse_mode'=>'markdown','reply_to_message_id'=>$message->message_id,'disable_web_page_preview'=>true,
]);
}
if($re and $text == "رفع مطور"  and $re_id !=$id_Bot and in_array($from_id,$Dev)  and in_array($re_id,$developer)){
bot('SendMessage',['chat_id'=>$chat_id,
'text'=>"📬┊العضو » [$usew]
👤┊ايديه » {$re_id}
🎖┊تم رفعه مطور من قبل
➖
",'parse_mode'=>'markdown','reply_to_message_id'=>$message->message_id,'disable_web_page_preview'=>true,
]);
}
if($re and $text == "رفع مطور اساسي" and $re_id !=$id_Bot and  in_array($from_id,$Dev)){
file_put_contents("$re_id.txt",$re_id);
bot('SendMessage',['chat_id'=>$chat_id,
'text'=>"
📬┊العضو » [$usew]
👤┊ايديه » {$re_id}
🎖┊تم رفعه مطور اساسي معك
➖
",
'parse_mode'=>'markdown','reply_to_message_id'=>$message->message_id,'disable_web_page_preview'=>true,
]);
}
if($re and $text == "رفع مطور"  || $text == "رفع ادمن" || $text == "رفع مميز" || $text == "رفع مدير" || $text == "رفع منشئ" and $re_id ==$bot_id and in_array($from_id,$Dev)){
bot('SendMessage',['chat_id'=>$chat_id,
'text'=>"
📮 ❉ لاتحرجناش والله ماريد 😹😹
",'parse_mode'=>'markdown','reply_to_message_id'=>$message->message_id,'disable_web_page_preview'=>true,
]);
}
$cdevs = count($developers)-1;
if($text == "مسح المطورين" and $cdevs != 0 and in_array($from_id,$Dev)){
bot('SendMessage',['chat_id'=>$chat_id,
'text'=>"
📬┊بواسطة الـ مطور الاساسي
👤┊تم حذف {$cdevs} مطور
➖
",'reply_to_message_id'=>$message->message_id,'disable_web_page_preview'=>true,
]);
file_put_contents("data/developers/developer.txt"," ");
file_put_contents("data/developers/developers.txt"," ");
}
if($text == "مسح المطورين" and $cdevs == 0 and in_array($from_id,$Dev)){
$cdevs = count($developers);
bot('SendMessage',['chat_id'=>$chat_id,
'text'=>"
📬┊عذرا ! لم يتم رفع اي مطورين
➖
",'parse_mode'=>'markdown','reply_to_message_id'=>$message->message_id,'disable_web_page_preview'=>true,
]);
file_put_contents("data/developers/developer.txt"," ");
file_put_contents("data/developers/developers.txt"," ");
}

if($re and $text == "رفع مدير" || $text == "رفع المدير"  and !in_array($re_id,$manger)){
if($status == "creator" ||  in_array($from_id,$Dev) || in_array($from_id,$developer)) {
			file_put_contents("data/manger/$chat_id.txt",$re_id . "\n" , FILE_APPEND);
			file_put_contents("data/manger/$chat_id/mange.txt" , "~» (" . "@". $re_user .") " . "»" . "  (". $re_id .") ". "\n" , FILE_APPEND);
bot('SendMessage',[
'chat_id'=>$chat_id,
'text'=>"
📬┊العضو » [$usew]
👤┊ايديه » {$re_id}
🎖┊تم رفعه مدير بالبوت
➖"
,'parse_mode'=>'markdown',
'reply_to_message_id'=>$message->message_id,
'disable_web_page_preview'=>true,
]);
}
}
if($re and $text == "رفع مدير" || $text == "رفع المدير" || $text == "رفع منشئ" || $text == "رفع المنشئ" and in_array($re_id,$manger)){
if($status == "creator" ||  in_array($from_id,$Dev) || in_array($from_id,$developer)) {
bot('SendMessage',['chat_id'=>$chat_id,
'text'=>"
📬┊العضو » [$usew]
👤┊ايديه » {$re_id}
🎖┊تم رفعه مدير من قبل
➖
",
'parse_mode'=>'markdown','reply_to_message_id'=>$message->message_id,'disable_web_page_preview'=>true,
]);
}}
$derb = file_get_contents("data/$chat_id/sen.txt");
$sww = file_get_contents("data/$chat_id/seen.txt");
$sew = file_get_contents("data/$chat_id/seeen.txt");
if($re and $text == "رفع بصلاحيه" || $text == "رفع بصلاحية" || $text == "رفع صلاحيه" || $text == "رفع صلاحية"){
if($status == "creator" ||  in_array($from_id,$Dev) || in_array($from_id,$developer)) {
file_put_contents("data/$chat_id/sen.txt","name");
file_put_contents("data/$chat_id/seen.txt",$from_id);
file_put_contents("data/$chat_id/seeen.txt",$re_id);
bot('SendMessage',['chat_id'=>$chat_id,
'text'=>"
👨‍✈️┇حسنا عزيزي $info
📛┇هاذا الامر يستخدم لرفع العضو بصلاحيه واحده فقط انت تختارها ✓
📕┇ارسل الان الصلاحيه التي تريدها للعضو » $re_id ، يمكنك ارسال رموز الصلاحيات للرفع 📌
ـــ  ــــ  ـــ  ـــ  ـــ
🗑┇حذف رسائل » {1}
🚫┇حظر مستخدمين » {2}
⛔️┇تثبيت رسائل » {3}
🚸┇دعوة مستخدمين » {4}
⚜┇اضافة مشرفين » {5}
♻️┇تغيير معلومات الجروب » {6}
🚸┇رفع بكامل الصلاحيات
❌┇الغاء » لالغاء الامر
ـــ  ــــ  ـــ  ـــ  ـــ
⚠️┇ملاحطة : للرفع بكل الصلاحيات عدا صلاحيات محددة » { تنزيل صلاحية } بالرد ✓",
]);
}}
if($text == "5" and $derb == "name"){
if($from_id == $sww){
bot('SendMessage',['chat_id'=>$chat_id,
'text'=>"
👨‍✈️┇تم رفع العضو » $sew
📛┇مشرف بصلاحيه رفع مشرفين فقط✓
📕┇بواسطة » $info
➖ 
",
]);
 bot('promoteChatMember',[
 'chat_id'=>$chat_id,
  'user_id'=>$sew,
 'can_change_info'=>false,
  'can_delete_messages'=>false,
  'can_invite_users'=>false,
  'can_restrict_members'=>false,
  'can_pin_messages'=>false,
  'can_promote_members'=>True,
]);
file_put_contents("data/$chat_id/seen.txt","864321168");
}
}
if($text == "1" and $derb == "name"){
if($from_id == $sww){
bot('SendMessage',['chat_id'=>$chat_id,
'text'=>"
👨‍✈️┇تم رفع العضو » $sew
📛┇مشرف بصلاحيه حذف الرسائل فقط ✓
📕┇بواسطة » $info
➖ 
",
]);
 bot('promoteChatMember',[
 'chat_id'=>$chat_id,
  'user_id'=>$sew,
 'can_change_info'=>false,
  'can_delete_messages'=>True,
  'can_invite_users'=>false,
  'can_restrict_members'=>false,
  'can_pin_messages'=>false,
  'can_promote_members'=>false,
]);
file_put_contents("data/$chat_id/seen.txt","864321168");
}
}
if( $text == "4" and $derb == "name"){
if($from_id == $sww){
bot('SendMessage',['chat_id'=>$chat_id,
'text'=>"
👨‍✈️┇تم رفع العضو » $sew
📛┇مشرف بصلاحيه دعوة مستخدمين ✓
📕┇بواسطة » $info
➖ 
",
]);
 bot('promoteChatMember',[
 'chat_id'=>$chat_id,
  'user_id'=>$sew,
 'can_change_info'=>false,
  'can_delete_messages'=>false,
  'can_invite_users'=>True,
  'can_restrict_members'=>false,
  'can_pin_messages'=>false,
  'can_promote_members'=>false,
]);
file_put_contents("data/$chat_id/seen.txt","864321168");
}
}
if($text  == "3" and $derb == "name"){
if($from_id == $sww){
bot('SendMessage',['chat_id'=>$chat_id,
'text'=>"
👨‍✈️┇تم رفع العضو » $sew
📛┇مشرف بصلاحيه تثبيت رسائل ✓
📕┇بواسطة » $info
➖ 
",
]);
 bot('promoteChatMember',[
 'chat_id'=>$chat_id,
  'user_id'=>$sew,
 'can_change_info'=>false,
  'can_delete_messages'=>false,
  'can_invite_users'=>false,
  'can_restrict_members'=>false,
  'can_pin_messages'=>True,
  'can_promote_members'=>false,
]);
file_put_contents("data/$chat_id/seen.txt","864321168");
}
}
if($text == "6" and $derb == "name"){
if($from_id == $sww){
bot('SendMessage',['chat_id'=>$chat_id,
'text'=>"
👨‍✈️┇تم رفع العضو » $sew
📛┇مشرف بصلاحيه تغيير المعلومات ✓
📕┇بواسطة » $info
➖ 
",
]);
 bot('promoteChatMember',[
 'chat_id'=>$chat_id,
  'user_id'=>$sew,
 'can_change_info'=>True,
  'can_delete_messages'=>false,
  'can_invite_users'=>false,
  'can_restrict_members'=>false,
  'can_pin_messages'=>false,
  'can_promote_members'=>false,
]);
file_put_contents("data/$chat_id/seen.txt","864321168");
}
}
if($text == "2" and $derb == "name"){
if($from_id == $sww){
bot('SendMessage',['chat_id'=>$chat_id,
'text'=>"
👨‍✈️┇تم رفع العضو » $sew
📛┇مشرف بصلاحيه حظر مستخدمين ✓
📕┇بواسطة » $info
➖ 
",
]);
 bot('promoteChatMember',[
 'chat_id'=>$chat_id,
  'user_id'=>$sew,
 'can_change_info'=>false,
  'can_delete_messages'=>false,
  'can_invite_users'=>false,
  'can_restrict_members'=>True,
  'can_pin_messages'=>false,
  'can_promote_members'=>false,
]);
file_put_contents("data/$chat_id/seen.txt","864321168");
}
}
if($text == "رفع بكامل الصلاحيات" and $derb == "name"){
if($from_id == $sww){
bot('SendMessage',['chat_id'=>$chat_id,
'text'=>"
👨‍✈️┇تم رفع العضو » $sew
📛┇مشرف بكامل الصلاحيات ✓
📕┇بواسطة » $info
➖ 
",
]);
 bot('promoteChatMember',[
 'chat_id'=>$chat_id,
  'user_id'=>$sew,
 'can_change_info'=>true,
  'can_delete_messages'=>true,
  'can_invite_users'=>true,
  'can_restrict_members'=>true,
  'can_pin_messages'=>True,
  'can_promote_members'=>True,
]);
}
}
if($text == "الغاء" and $derb == "name"){
if($from_id == $sww){
bot('SendMessage',['chat_id'=>$chat_id,
'text'=>"
📛┇تم الغاء الامر ✓
📕┇بواسطة » $info
➖ 
",
]);
file_put_contents("data/$chat_id/seen.txt","864321168");
}
}
if($text == "مسح المدراء" and $mangers_info != NULL and $mangers_info != " "){
if($status == "creator" ||  in_array($from_id,$Dev) || in_array($from_id,$developer)) {
$cmang = count($mangers)-1;
bot('SendMessage',['chat_id'=>$chat_id,
'text'=>"
📬┊بواسطة الـ $info
👤┊تم حذف {$cmang} من المدراء
➖",
'parse_mode'=>'markdown','reply_to_message_id'=>$message->message_id,'disable_web_page_preview'=>true,  
]);
file_put_contents("data/manger/$chat_id.txt","");
file_put_contents("data/manger/$chat_id.txt","");
file_put_contents("data/manger/$chat_id/mange.txt" ,"");
}}
if($text == "مسح المدراء" and $mangers_info == NULL or $mangers_info == " "){
if($status == "creator" ||  in_array($from_id,$Dev) || in_array($from_id,$developer)) {
bot('SendMessage',['chat_id'=>$chat_id,
'text'=>"*
📬┊عذرا ! لم يتم رفع اي ممدراء
➖",
'parse_mode'=>'markdown','reply_to_message_id'=>$message->message_id,'disable_web_page_preview'=>true,  
]);
}}
if($status == "creator" ||  in_array($from_id,$Dev) || in_array($from_id,$developer)) {
if($re and $text == "تنزيل المدير" || $text == "تنزيل مدير"  and in_array($re_id,$manger)){
	$re_id_info = file_get_contents("data/manger/$chat_id.txt");
	$mdrs = file_get_contents("data/manger/$chat_id/mange.txt");
	$mdrs1 = explode("             \n",$mdrs);
	$str = str_replace($re_id,"",$re_id_info);
	$str2 = str_replace("~» (" . "@". $re_user .")  " . "»" . "  (". $re_id .") .","",$mdrs1);
	file_put_contents("data/manger/$chat_id.txt",$str);
	file_put_contents("data/manger/$chat_id/mange.txt",$str2);
	bot('SendMessage',['chat_id'=>$chat_id,
    'text'=>"
📬┊العضو » [$usew]
??┊ايديه » {$re_id}
🎖┊تم حذفه من المدراء
➖
",
'parse_mode'=>'markdown','reply_to_message_id'=>$message->message_id,'disable_web_page_preview'=>true,
]);
}}
if($status == "creator" ||  in_array($from_id,$Dev) || in_array($from_id,$developer)) {
if($re and $text == "تنزيل المدير" || $text == "تنزيل مدير" || $text == "تنزيل bbbbbb" || $text == "تنزيل nnnnnn" and !in_array($re_id,$manger)){
bot('SendMessage',['chat_id'=>$chat_id,
'text'=>"
📬┊العضو » [$usew]
👤┊ايديه » {$re_id}
🎖┊انه ليس مدير
➖
",'parse_mode'=>'markdown','reply_to_message_id'=>$message->message_id,'disable_web_page_preview'=>true,
]);
}
}
if(in_array($from_id,$Dev)){
if($re and $text == "تنزيل مطور" || $text == "تنزيل المطور"  and in_array($re_id,$developer)){
	$re_id_info = file_get_contents("data/developers/$chat_id.txt");
	$devr = file_get_contents("data/developers/$chat_id/developer.txt");
	$devr1 = explode("             \n",$devr);
	$str = str_replace($re_id,"",$re_id_info);
	$str2 = str_replace("~» (" . "@". $re_user .") " . "»" . "  (". $re_id .") .","",$devr1);
	file_put_contents("data/developers/developer.txt",$str);
			file_put_contents("data/developers/developers.txt",$str);
	bot('SendMessage',['chat_id'=>$chat_id,
    'text'=>"
📬┊العضو » [$usew]
👤┊ايديه » {$re_id}
🎖┊تم تنزيله من المطورين
➖
",
'parse_mode'=>'markdown','reply_to_message_id'=>$message->message_id,'disable_web_page_preview'=>true,
]);
}}
if(in_array($from_id,$Dev)){
if($re and $text == "تنزيل المطور" || $text == "تنزيل مطور" || $text == "تنزيل ورديسسس" and !in_array($re_id,$developer)){
bot('SendMessage',['chat_id'=>$chat_id,
'text'=>"
📬┊العضو » [$usew]
👤┊ايديه » {$re_id}
🎖┊انه ليس مطور ليتم حذفه !
➖
",'parse_mode'=>'markdown','reply_to_message_id'=>$message->message_id,'disable_web_page_preview'=>true,
]);
}
}
if(in_array($from_id,$Dev)){
if($re and $text == "تنزيل مطور اساسي" || $text == "تنزيل مطور الاساسي"  and in_array($re_id,$Dev)){
			file_put_contents("$re_id.txt","");
	bot('SendMessage',['chat_id'=>$chat_id,
    'text'=>"
📬┊العضو » [$usew]
👤┊ايديه » {$re_id}
🎖┊تم تنزيله مطور اساسي
➖
",
'parse_mode'=>'markdown','reply_to_message_id'=>$message->message_id,'disable_web_page_preview'=>true,
]);
}}
if($status == "creator" ||  $status == "administrator" ||  in_array($from_id,$Dev) || in_array($from_id,$developer)) {
if($re and $text == "رفع ادمن"  and !in_array($re_id,$admin_user)){
			file_put_contents("data/admin_user/$chat_id.txt",$re_id . "\n" , FILE_APPEND);
			file_put_contents("data/admin_user/$chat_id/mange.txt" , "~» ([" . "@". $re_user ."]) " . "»" . "  (`". $re_id ."`) ". "\n" , FILE_APPEND);
bot('SendMessage',['chat_id'=>$chat_id,
'text'=>"
📬┊العضو » [$usew]
👤┊ايديه » {$re_id}
🎖┊تم رفعه ادمن في البوت
➖
",'parse_mode'=>'markdown','reply_to_message_id'=>$message->message_id,'disable_web_page_preview'=>true,
]);
}
}
if($status == "creator" ||  $status == "administrator" ||  in_array($from_id,$Dev) || in_array($from_id,$developer)) {
if ($re and $text == "رفع ادمن" and in_array($re_id,$admin_user)){
bot('SendMessage',['chat_id'=>$chat_id,
'text'=>"
📬┊العضو » [$usew]
👤┊ايديه » {$re_id}
🎖┊تم رفعه ادمن بالبوت قبلا
➖
",
'parse_mode'=>'markdown','reply_to_message_id'=>$message->message_id,'disable_web_page_preview'=>true,
]);
}
}
if($status == "creator" ||  $status == "administrator" ||  in_array($from_id,$Dev) || in_array($from_id,$developer)) {
if($text == "مسح الادمنيه" or $text == "مسح الادمنية" ){
$cadmins = count($admin_users)-1;
bot('SendMessage',['chat_id'=>$chat_id,
'text'=>"
📬┊بواسطة الـ $info
👤┊تم حذف {$cadmins} ادمن
➖",
'parse_mode'=>'markdown','reply_to_message_id'=>$message->message_id,'disable_web_page_preview'=>true,
]);
file_put_contents("data/admin_user/$chat_id.txt","");
	file_put_contents("data/admin_user/$chat_id/mange.txt","");
	}}
if($status == "creator" ||  $status == "administrator" ||  in_array($from_id,$Dev) || in_array($from_id,$developer)) {
if($re and $text == "تنزيل ادمن" and in_array($re_id,$admin_user)){
	$re_id_info = file_get_contents("data/admin_user/$chat_id.txt");
	$admn = file_get_contents("data/admin_user/$chat_id/mange.txt");
	$admn1 = explode("             \n",$admn);
	$str = str_replace($re_id,"",$re_id_info);
	$str2 = str_replace("| {[" . "@". $re_user ."]}  " . "»" . "  (`". $re_id ."`) .","",$admn1);
	file_put_contents("data/admin_user/$chat_id.txt",$str);
	file_put_contents("data/admin_user/$chat_id/mange.txt",$str2);
	bot('SendMessage',['chat_id'=>$chat_id,
    'text'=>"
📬┊العضو » [$usew]
👤┊ايديه » {$re_id}
🎖┊تم تنزيله من الادمنيه
➖
",
'parse_mode'=>'markdown','reply_to_message_id'=>$message->message_id,'disable_web_page_preview'=>true,
]);
}
}
if($status == "creator" ||  $status == "administrator" ||  in_array($from_id,$Dev) || in_array($from_id,$developer)) {
if($re and $text == "تنزيل ادمن"  and !in_array($re_id,$admin_user)){
bot('SendMessage',['chat_id'=>$chat_id,
'text'=>"
📬┊العضو » [$usew]
👤┊ايديه » {$re_id}
🎖┊انه ليس ادمن ليتم تنزيله
➖
",'parse_mode'=>'markdown','reply_to_message_id'=>$message->message_id,'disable_web_page_preview'=>true,
]);
}
}

if($status == "creator" ||  $status == "administrator" or in_array($from_id,$Dev) || in_array($from_id,$developer) || in_array($from_id,$admin_user) || in_array($from_id,$manger)) {
if($re and $text == "رفع مميز"  and !in_array($re_id,$mmyaz)){
file_put_contents("data/mmyaz/$chat_id.txt",$re_id . "\n" , FILE_APPEND);
file_put_contents("data/mmyaz/$chat_id/mange.txt" , "| {[" . "@". $re_user ."]}  " . "»" . "  (`". $re_id ."`) ". "\n" , FILE_APPEND);
bot('SendMessage',['chat_id'=>$chat_id,
'text'=>"
📬┊العضو » [$usew]
👤┊ايديه » {$re_id}
🎖┊تم رفعه عضو مميز
➖
",'parse_mode'=>'markdown','reply_to_message_id'=>$message->message_id,'disable_web_page_preview'=>true,
]);
}
}
if($status == "creator" ||  $status == "administrator" or in_array($from_id,$Dev) || in_array($from_id,$developer) || in_array($from_id,$admin_user) || in_array($from_id,$manger)) {
if($re and $text == "رفع مميز"  and in_array($re_id,$mmyaz)){
bot('SendMessage',['chat_id'=>$chat_id,
'text'=>"
📬┊العضو » [$usew]
👤┊ايديه » {$re_id}
🎖┊تم رفعه مميز من قبل
➖
",
'parse_mode'=>'markdown','reply_to_message_id'=>$message->message_id,'disable_web_page_preview'=>true,
]);
}
}
if($status == "creator" ||  $status == "administrator" or in_array($from_id,$Dev) || in_array($from_id,$developer) || in_array($from_id,$admin_user) || in_array($from_id,$manger)) {
if($text == "مسح المميزين" ){
$cmmyz = count($mmyazs)-1;
bot('SendMessage',['chat_id'=>$chat_id,
'text'=>"
📬┊بواسطة الـ $info
👤┊تم حذف {$cmmyz} مميز
➖
",
'parse_mode'=>'markdown','reply_to_message_id'=>$message->message_id,'disable_web_page_preview'=>true,  
]);
file_put_contents("data/mmyaz/$chat_id.txt","");
file_put_contents("data/mmyaz/$chat_id.txt","");
file_put_contents("data/mmyaz/$chat_id/mange.txt" ,"");
}}

if($re and $text == "تنزيل مميز"   and in_array($re_id,$mmyaz)){
if($status == "creator" ||  $status == "administrator" or in_array($from_id,$Dev) || in_array($from_id,$developer) || in_array($from_id,$admin_user) || in_array($from_id,$manger)) {
	$re_id_info = file_get_contents("data/mmyaz/$chat_id.txt");
	$mdrs = file_get_contents("data/mmyaz/$chat_id/mange.txt");
	$mdrs1 = explode("             \n",$mdrs);
	$str = str_replace($re_id,"",$re_id_info);
	$str2 = str_replace("| {[" . "@". $re_user ."]}  " . "»" . "  (`". $re_id ."`) .","",$mdrs1);
	file_put_contents("data/mmyaz/$chat_id.txt",$str);
	file_put_contents("data/mmyaz/$chat_id/mange.txt",$str2);
	bot('SendMessage',['chat_id'=>$chat_id,
    'text'=>"
📬┊العضو » [$usew]
👤┊ايديه » {$re_id}
🎖┊تم تنزيله من المميزين
➖
",
'parse_mode'=>'markdown','reply_to_message_id'=>$message->message_id,'disable_web_page_preview'=>true,
]);
}
}
if($status == "creator" ||  $status == "administrator" or in_array($from_id,$Dev) || in_array($from_id,$developer) || in_array($from_id,$admin_user) || in_array($from_id,$manger)) {
if($re and $text == "تنزيل مميز" and !in_array($re_id,$mmyaz)){
bot('SendMessage',['chat_id'=>$chat_id,
'text'=>"
📬┊العضو » [$usew]
👤┊ايديه » {$re_id}
🎖┊انه ليس مميز لتنزيله
➖
",'parse_mode'=>'markdown','reply_to_message_id'=>$message->message_id,'disable_web_page_preview'=>true,
]);
}
}
if($status == "creator" and in_array($from_id,$Dev)){
if($text == "تنزيل الكل" or $text == "حذف الكل"){
$CMM = count($mmyazs)-1;
$CM = count($mangers)-1;
$CA = count($admin_users)-1;
$CALL = $CA + $CM + $CMM;
bot('SendMessage',['chat_id'=>$chat_id,
'text'=>"
📬┊بواسطـة $info
ـــ ـــ ـــ ــــ ــــ 
🗑┊تم حذف {$CA} من الادمنيه
🗑┊تم حذف {$CM} من المدراء
🗑┊تم حذف {$CMM} من المميزين
ـــ ـــ ـــ ــــ ــــ 
📛┊تم حذف {$CALL} من المرفوعين
🚸┊تم حذف الكل بنجاح 
✓
",'parse_mode'=>'markdown','reply_to_message_id'=>$message->message_id,'disable_web_page_preview'=>true,
]);
file_put_contents("data/manger/$chat_id.txt","");
file_put_contents("data/manger/$chat_id.txt","");
file_put_contents("data/manger/$chat_id/mange.txt" ,"");
file_put_contents("data/mmyaz/$chat_id.txt","");
file_put_contents("data/mmyaz/$chat_id.txt","");
file_put_contents("data/mmyaz/$chat_id/mange.txt" ,"");
file_put_contents("data/admin_user/$chat_id.txt","");
file_put_contents("data/admin_user/$chat_id/mange.txt","");
}
}
if($status != "creator" and $status != "administrator" and !in_array($from_id,$Dev) and !in_array($from_id,$developer)){
if($text == "رفع مدير" || $text == "رفع منشئ" or $text == "رفع الادمنيه" or $text == "رفع الادمنية" or $text == "تفعيل"){
bot('SendMessage',['chat_id'=>$chat_id,
'text'=>"
🔒┊لا تملك الصلاحية لتنفيذ هذا الأمر
",'parse_mode'=>'markdown','reply_to_message_id'=>$message->message_id,'disable_web_page_preview'=>true,
]);
}}
if( !in_array($from_id,$Dev)){
if($text == "رفع مطور" || $text == "تنزيل مطور" or $text == "رفع منشئ" or $text == "المطورين" or $text == "مسح مطور"){
bot('SendMessage',['chat_id'=>$chat_id,
'text'=>"
🔒┊لا تملك الصلاحية لتنفيذ هذا الأمر
",'parse_mode'=>'markdown','reply_to_message_id'=>$message->message_id,'disable_web_page_preview'=>true,
]);
}}
if($status != "creator" and $status != "administrator" and !in_array($from_id,$Dev) and !in_array($from_id,$developer) and !in_array($from_id,$manger) and !in_array($from_id,$admin_user)){
if($text == "رفع ادمن" || $text == "رفع مميز" or $text == "م1" or $text == "م2" or $text == "م3" or $text == "م4" or $text == "م5" or $text == "قفل الصور" or $text == "تنزيل مميز" or $text == "تنزيل ادمن" or $text == "قفل الفيديو" or $text == "فتح الفيديو" or $text == "تفعيل الايدي" or $text == "تعطيل الايدي"){
bot('SendMessage',['chat_id'=>$chat_id,
'text'=>"
🔒┊لا تملك الصلاحية لتنفيذ هذا الأمر
",'parse_mode'=>'markdown','reply_to_message_id'=>$message->message_id,'disable_web_page_preview'=>true,
]);
}}
 
if(in_array($from_id,$Dev)){
if($text == "المطورين" and $cdevs != 0){
if ($tc == 'group' | $tc == 'supergroup'){
bot('sendmessage',[
 'chat_id'=>$chat_id,
 'text'=>"
👨🏻‍💻┇المطورين {$cdevs} : 
$developers_infos
",
]);
}
}
if($text == "المطورين" and $cdevs == 0 || $developers_info == ""){
if ($tc == 'group' | $tc == 'supergroup'){
bot('sendmessage',[
 'chat_id'=>$chat_id,
 'text'=>"
 📬┊عذرا ! لم يتم رفع اي مطورين
➖
",
]);
}
}
}
$CM = count($mangers)-1;
if($text == "المدراء" and $CM != 0){
if ( $status == 'creator' or $status == 'administrator' or in_array($from_id,$Dev) or in_array($from_id,$developer)) {if ($tc == 'group' | $tc == 'supergroup'){
bot('sendmessage',[
 'chat_id'=>$chat_id,
 'text'=>"
👨🏻‍💻┇المدراء [{$CM}] : 
$mangers_infos
",
]);
}
}
}
if($text == "المدراء" and $CM == 0){
if ( $status == 'creator' or $status == 'administrator' or in_array($from_id,$Dev) or in_array($from_id,$developer)) {if ($tc == 'group' | $tc == 'supergroup'){
bot('sendmessage',[
 'chat_id'=>$chat_id,
 'text'=>
"
📬┊عذرا ! لم يتم رفع اي مدراء
➖",
]);
}
}
}
$CA = count($admin_users)-1;
if($text == "الادمنيه" || $text == "الادمنية" and $admin_users_infos != null){
if ( $status == 'creator' or $status == 'administrator' or in_array($from_id,$Dev) or in_array($from_id,$manger) or in_array($from_id,$admin_user) or in_array($from_id,$developer)) {if ($tc == 'group' | $tc == 'supergroup'){
bot('sendmessage',[
 'chat_id'=>$chat_id,
 'text'=>"
📙┇قائمة الادمنية [{$CA}] :
$admin_users_infos",
'parse_mode'=>"markdown",'disable_web_page_preview'=>true,
]);
}
}
}
if($text == "الادمنيه" || $text == "الادمنية" and $admin_users_infos == null){
if ( $status == 'creator' or $status == 'administrator' or in_array($from_id,$Dev) or in_array($from_id,$manger) or in_array($from_id,$admin_user) or in_array($from_id,$developer)) {if ($tc == 'group' | $tc == 'supergroup'){
bot('sendmessage',[
 'chat_id'=>$chat_id,
 'text'=>"
📛┇NotDirector - *Admins* -
📛┇لايوجد مجلد - *الادمنيه* -
➖",
'parse_mode'=>"markdown",'disable_web_page_preview'=>true,
]);
}
}
}
$CMM = count($mmyazs)-1;
if($text == "المميزين" and $mmyazs_infos != null){
if ( $status == 'creator' or $status == 'administrator' or in_array($from_id,$Dev) or in_array($from_id,$manger) or in_array($from_id,$admin_user) or in_array($from_id,$developer)) {if ($tc == 'group' | $tc == 'supergroup'){
bot('sendmessage',[
 'chat_id'=>$chat_id,
 'text'=>"
📙┇قائمة المميزين [{$CMM}] :
$mmyazs_infos",
'parse_mode'=>"markdown",'disable_web_page_preview'=>true,
]);
}
}
}
if($text == "المميزين" and $mmyazs_infos == null){
if ( $status == 'creator' or $status == 'administrator' or in_array($from_id,$Dev) or in_array($from_id,$manger) or in_array($from_id,$admin_user) or in_array($from_id,$developer)) {if ($tc == 'group' | $tc == 'supergroup'){
bot('sendmessage',[
 'chat_id'=>$chat_id,
 'text'=>"
📛┇NotDirector - *VipMember* -
📛┇لايوجد مجلد - *المميزين* -
➖",
]);
}
}
}
 elseif($text  == "كتم" && $rt or $text  == "silent" && $rt or $text  == "تقييد" && $rt){
if ( $status == 'creator' or $status == 'administrator' or in_array($from_id,$Dev) or in_array($from_id,$manger) or in_array($from_id,$admin_user) or in_array($from_id,$developer)) {
if ( $statusrt != 'creator' && $statusrt != 'administrator' && !in_array($re_id,$Dev) && !in_array($re_id,$manger) && !in_array($re_id,$admin_user) && !in_array($re_id,$mmyaz) && !in_array($re_id,$developer)) {
	
$add = $settings["information"]["added"];
if ($add == true){
   bot('restrictChatMember',[
   'user_id'=>$re_id,   
   'chat_id'=>$chat_id,
   'can_post_messages'=>false,
         ]);
  bot('sendMessage',[
'chat_id'=>$chat_id,
'text'=>"👤¦ العضو » [$usew]
🎫¦ الايدي » {[$re_id]}
🛠¦ تم كتمه/تقييده
✓️
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,
'reply_to_message_id'=>$re_msgid,
]);
$settings["silentlist"][]="$re_id";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
else
{
bot('sendmessage',[
	'chat_id'=>$chat_id,
	'text'=>"⁉️┇خطأ البوت لا يعمل بسبب عدم تفعيل البوت
🔘┇ارسل كلمة تفعيل لتفعيل البوت في المجموعة",
  'reply_to_message_id'=>$message_id,
'reply_markup'=>$inlinebutton,
 ]);
 }
}
else
{
bot('sendmessage',[
	'chat_id'=>$chat_id,
	'text'=>" لايمكنني تقييد الادمنية او المدراء او  او المميزين",
  'reply_to_message_id'=>$message_id,
'reply_markup'=>$inlinebutton,
 ]);
}
}
}
elseif (strpos($text  , "كتم لمدة ") !== false && $rt or strpos($text  , "تقييد لمدة ") !== false && $rt) {
if ( $status == 'creator' or $status == 'administrator' or in_array($from_id,$Dev) or in_array($from_id,$manger) or in_array($from_id,$admin_user) or in_array($from_id,$developer)) {
if ( $statusrt != 'creator' && $statusrt != 'administrator' && !in_array($re_id,$Dev) && !in_array($re_id,$manger) && !in_array($re_id,$admin_user) && !in_array($re_id,$mmyaz) && !in_array($re_id,$developer)) {
$add = $settings["information"]["added"];
$we = str_replace(['كتم لمدة ',' تقييد لمدة'],'',$text );
if ($we <= 1000 && $we >= 1){
if ($add == true) {
$weplus = $we + 0;
	bot('sendmessage',[
	'chat_id'=>$chat_id,
'text'=>"👤¦ العضو » [$usew]
🎫¦ الايدي » {[$re_id]}
🛠¦ تم كتمه لمدة $we دقيقه
✓️
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,
  'reply_to_message_id'=>$message_id,
'reply_markup'=>$inlinebutton,
 ]);
    bot('restrictChatMember',[
   'user_id'=>$re_id,   
   'chat_id'=>$chat_id,
   'can_post_messages'=>false,
   'until_date'=>time()+$weplus*60,
         ]);
$settings["silentlist"][]="$re_id";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
else
{
bot('sendmessage',[
	'chat_id'=>$chat_id,
	'text'=>"⁉️┇خطأ البوت لا يعمل بسبب عدم تفعيل البوت
🔘┇ارسل كلمة تفعيل لتفعيل البوت في المجموعة",
  'reply_to_message_id'=>$message_id,
'reply_markup'=>$inlinebutton,
 ]);
}
}
else
{
bot('sendmessage',[
	'chat_id'=>$chat_id,
	'text'=>"خطا⚠️
➖➖➖➖➖➖
يجب اختيار عدد بين 1 الى 1000",
  'reply_to_message_id'=>$message_id,
'reply_markup'=>$inlinebutton,
 ]);
}
}
else
{
bot('sendmessage',[
 'chat_id' => $chat_id,
 'text'=>"لايمكنني تقييد الادمنية او المدراء او المطورين او المميزين",
'reply_markup'=>$inlinebutton,
   ]);
}
}
}
$idp == file_get_contents("data/$chat_id/bans.txt");
if ( $status == 'creator' or $status == 'administrator' or in_array($from_id,$Dev) or in_array($from_id,$manger) or in_array($from_id,$admin_user) or in_array($from_id,$developer)) {
$tq = str_replace("الغاء تقييد ", "$tq", $text);
if($text == "الغاء تقييد $tq" and preg_match('/([0-9])/i',$tq)){
file_put_contents("data/$chat_id/bans.txt",$tq);
$idp == file_get_contents("data/$chat_id/bans.txt");
$statusidd = json_decode(file_get_contents("https://api.telegram.org/bot$token/getChatMember?chat_id=$chat_id&user_id=".$tq),true);
$statusid = $statusidd['result']['status'];
	 bot('restrictChatMember',[
   'user_id'=>$tq,   
   'chat_id'=>$chat_id,
   'can_post_messages'=>true,
   'can_add_web_page_previews'=>false,
   'can_send_other_messages'=>true,
   'can_send_media_messages'=>true,
         ]);
bot('sendmessage',[
	'chat_id'=>$chat_id,
'text'=>"🙍🏼‍♂┊العضو » {$tq}
👤┊تم الغاء تقييده
➖
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,
'reply_to_message_id'=>$message_id,
	 'reply_markup'=>$inlinebutton,
   ]);
$key = array_search($tq,$settings["silentlist"]);
unset($settings["silentlist"][$key]);
$settings["silentlist"] = array_values($settings["silentlist"]); 
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
   } 
}
$idp == file_get_contents("data/$chat_id/bans.txt");
if ( $status == 'creator' or $status == 'administrator' or in_array($from_id,$Dev) or in_array($from_id,$manger) or in_array($from_id,$admin_user) or in_array($from_id,$developer)) {
$ktmm= str_replace("الغاء كتم ", "$ktmm", $text);
if($text == "الغاء كتم $ktmm" and preg_match('/([0-9])/i',$ktmm)){
file_put_contents("data/$chat_id/bans.txt",$ktmm);
$idp == file_get_contents("data/$chat_id/bans.txt");
$statusidd = json_decode(file_get_contents("https://api.telegram.org/bot$token/getChatMember?chat_id=$chat_id&user_id=".$ktmm),true);
$statusid = $statusidd['result']['status'];
	 bot('restrictChatMember',[
   'user_id'=>$ktmm,   
   'chat_id'=>$chat_id,
   'can_post_messages'=>true,
   'can_add_web_page_previews'=>false,
   'can_send_other_messages'=>true,
   'can_send_media_messages'=>true,
         ]);
bot('sendmessage',[
	'chat_id'=>$chat_id,
'text'=>"🙍🏼‍♂┊العضو » {$ktmm}
👤┊تم الغاء كتمه
➖
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,
'reply_to_message_id'=>$message_id,
	 'reply_markup'=>$inlinebutton,
   ]);
$key = array_search($ktmm,$settings["silentlist"]);
unset($settings["silentlist"][$key]);
$settings["silentlist"] = array_values($settings["silentlist"]); 
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
   } 
}
if($text  == "الغاء تقييد" && $rt or $text  == "الغاء كتم" && $rt or $text  == "الغاء التقييد" && $rt){
if ( $status == 'creator' or $status == 'administrator' or in_array($from_id,$Dev) or in_array($from_id,$manger) or in_array($from_id,$admin_user) or in_array($from_id,$developer)) {$add = $settings["information"]["added"];
if ($add == true) {
 bot('restrictChatMember',[
   'user_id'=>$re_id,   
   'chat_id'=>$chat_id,
   'can_post_messages'=>true,
   'can_add_web_page_previews'=>false,
   'can_send_other_messages'=>true,
   'can_send_media_messages'=>true,
         ]);
  bot('sendMessage',[
'chat_id'=>$chat_id,
'text'=>"👤¦ العضو » [$usew]
🎫¦ الايدي » {[$re_id]}
🛠¦ تم الغاء كتمه/تقييده
✓️
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,
'reply_to_message_id'=>$re_msgid,
]);
$key = array_search($re_id,$settings["silentlist"]);
unset($settings["silentlist"][$key]);
$settings["silentlist"] = array_values($settings["silentlist"]); 
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
else
{
bot('sendmessage',[
	'chat_id'=>$chat_id,
	'text'=>"⁉️┇خطأ البوت لا يعمل بسبب عدم تفعيل البوت
🔘┇ارسل كلمة تفعيل لتفعيل البوت في المجموعة",
  'reply_to_message_id'=>$message_id,
'reply_markup'=>$inlinebutton,
 ]);
}
}
}

if( $text  == "قائمة المقيدين" or $text == "المقيدين") {
if ( $status == 'creator' or $status == 'administrator' or in_array($from_id,$Dev) or in_array($from_id,$manger) or in_array($from_id,$admin_user) or in_array($from_id,$developer)) {$silent = $settings["silentlist"];
for($z = 0;$z <= count($silent)-1;$z++){
$result = $result."[$silent[$z]](tg://user?id=$silent[$z])"."\n";
}
	  bot('sendMessage',[
'chat_id'=>$chat_id,
'text'=>"
📙┇قائمة المقيدين :
$result",
'parse_mode'=>"MarkDown",
'reply_to_message_id'=>$message_id,
'reply_markup'=>$inlinebutton,
 ]);
}
}
if( $text  == "قائمة المكتومين" or $text == "المكتومين") {
if ( $status == 'creator' or $status == 'administrator' or in_array($from_id,$Dev) or in_array($from_id,$manger) or in_array($from_id,$admin_user) or in_array($from_id,$developer)) {$silent = $settings["silentlist"];
for($z = 0;$z <= count($silent)-1;$z++){
$result = $result."[$silent[$z]](tg://user?id=$silent[$z])"."\n";
}
	  bot('sendMessage',[
'chat_id'=>$chat_id,
'text'=>"
📙┇قائمة المكتومين :
$result",
'parse_mode'=>"MarkDown",
'reply_to_message_id'=>$message_id,
'reply_markup'=>$inlinebutton,
 ]);
}
}
if( $text  == "مسح المكتومين" or $text == "مسح المكاتيم") {
if ( $status == 'creator' or $status == 'administrator' or in_array($from_id,$Dev) or in_array($from_id,$manger) or in_array($from_id,$admin_user) or in_array($from_id,$developer)) {$add = $settings["information"]["added"];
if ($add == true) {
$silent = $settings["silentlist"];
for($z = 0;$z <= count($silent)-1;$z++){
 bot('restrictChatMember',[
   'user_id'=>$silent[$z],   
   'chat_id'=>$chat_id,
   'can_post_messages'=>true,
   'can_add_web_page_previews'=>false,
   'can_send_other_messages'=>true,
   'can_send_media_messages'=>true,
         ]);
}
	  bot('sendMessage',[
'chat_id'=>$chat_id,
'text'=>"  
📬┊بواسطة $keees
👤┊تم تنظيف سلة المكتومين
➖
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,
'reply_to_message_id'=>$message_id,
'reply_markup'=>$inlinebutton,
 ]);
unset($settings["silentlist"]);
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
else
{
bot('sendmessage',[
	'chat_id'=>$chat_id,
	'text'=>"⁉️┇خطأ البوت لا يعمل بسبب عدم تفعيل البوت
🔘┇ارسل كلمة تفعيل لتفعيل البوت في المجموعة",
  'reply_to_message_id'=>$message_id,
'reply_markup'=>$inlinebutton,
 ]);
}
}
}
//link //
if($settings["lock"]["link"] == "مقفول️"){
if ($status != 'creator' && $status != 'administrator' && !in_array($from_id,$Dev) && !in_array($from_id,$useradmin) && !in_array($from_id,$getCCmember) && !in_array($from_id,$mmyaz) ){
if (strstr($text,"t.me") == true or strstr($text,"telegram.me") == true or strstr($text,"https://") == true or strstr($text,"://") == true or strstr($text,"wWw.") == true or strstr($text,"WwW.") == true or strstr($text,"T.me/") == true or strstr($text,"WWW.") == true or strstr($caption,"t.me") == true or strstr($caption,"telegram.me")) {   
bot('deletemessage',[
'chat_id'=>$chat_id,
'message_id'=>$message_id,
]);
}
}
}
if($settings["lock"]["linkr"] == "مقفول️"){
if ($status != 'creator' && $status != 'administrator' && !in_array($from_id,$Dev) && !in_array($from_id,$useradmin) && !in_array($from_id,$getCCmember) && !in_array($from_id,$mmyaz)  ){
if (strstr($text,"t.me") == true or strstr($text,"telegram.me") == true or strstr($text,"https://") == true or strstr($text,"://") == true or strstr($text,"wWw.") == true or strstr($text,"WwW.") == true or strstr($text,"T.me/") == true or strstr($text,"WWW.") == true or strstr($caption,"t.me") == true or strstr($caption,"telegram.me")) {   
bot('deletemessage',[
'chat_id'=>$chat_id,
'message_id'=>$message_id,
]);
bot('restrictChatMember',[
   'user_id'=>$from_id,   
   'chat_id'=>$chat_id,
   'can_post_messages'=>false,
]);
}
}
}
//farse ♥
if($settings["lock"]["farse"] == "مقفول️"){
	if ( $status != 'creator' && $status != 'administrator' && !in_array($from_id,$Dev) && !in_array($from_id,$getCCmember) && !in_array($from_id,$useradmin) && !in_array($from_id,$mmyaz) ){ 
$uo=json_decode(file_get_contents("https://api.telegram.org/bot$token/getchat?chat_id=$fromid3"))->result;
$io=$uo->first_name;
$word = json_decode(file_get_contents("https://translate.yandex.net/api/v1.5/tr.json/detect?key=trnsl.1.1.20170725T151635Z.31fe7a5603917164.915fed1f5a9aaebef43860694075516e7af7aa47&text=".urlencode($io)))->lang;
$new = $update->message->new_chat_member; 
if($new and $word !="ar" and $word !="en"){
bot('SendMessage', [
'chat_id'=>$chatid3,
'text'=>"⚠️┇ ممنوع دخول الفارسية هنا  [$io](tg://user?id=$fromid3)"
,'parse_mode'=>"markdown",'disable_web_page_preview'=>true,
]);
bot('kickChatMember',[
'chat_id'=>$chatid3,
'user_id'=>$fromid3,
]);
}
}
}
// lock photo
if($settings["lock"]["photo"] == "مقفول️"){
if ( $status != 'creator' && $status != 'administrator' && !in_array($from_id,$Dev) && !in_array($from_id,$getCCmember) && !in_array($from_id,$useradmin) && !in_array($from_id,$mmyaz) ){ 
if ($update->message->photo){  
bot('deletemessage',[
'chat_id'=>$chat_id,
'message_id'=>$message_id
]);
}
}
}
// lock photo r
if($settings["lock"]["photor"] == "مقفول️"){
if ( $status != 'creator' && $status != 'administrator' && !in_array($from_id,$Dev) && !in_array($from_id,$getCCmember) && !in_array($from_id,$useradmin) && !in_array($from_id,$mmyaz) ){ 
if ($update->message->photo){  
bot('deletemessage',[
'chat_id'=>$chat_id,
'message_id'=>$message_id,
]);
bot('restrictChatMember',[
   'user_id'=>$from_id,   
   'chat_id'=>$chat_id,
   'can_post_messages'=>false,
]);
}
}
}
// gif
if($settings["lock"]["gif"] == "مقفول️"){
if ( $status != 'creator' && $status != 'administrator' && !in_array($from_id,$Dev) && !in_array($from_id,$getCCmember) && !in_array($from_id,$useradmin) && !in_array($from_id,$mmyaz) ){ 
if ($update->message->document){  
bot('deletemessage',[
'chat_id'=>$chat_id,
'message_id'=>$message_id
]);
}
}
}
//gif r
if($settings["lock"]["gifr"] == "مقفول️"){
if ( $status != 'creator' && $status != 'administrator' && !in_array($from_id,$Dev) && !in_array($from_id,$getCCmember) && !in_array($from_id,$useradmin) && !in_array($from_id,$mmyaz) ){ 
if ($update->message->document){  
bot('deletemessage',[
'chat_id'=>$chat_id,
'message_id'=>$message_id,
]);
bot('restrictChatMember',[
   'user_id'=>$from_id,   
   'chat_id'=>$chat_id,
   'can_post_messages'=>false,
]);
}
}
}
// document
if($settings["lock"]["document"] == "مقفول️"){
if ( $status != 'creator' && $status != 'administrator' && !in_array($from_id,$Dev) && !in_array($from_id,$getCCmember) && !in_array($from_id,$useradmin) && !in_array($from_id,$mmyaz) ){ 
if ($update->message->document){  
bot('deletemessage',[
'chat_id'=>$chat_id,
'message_id'=>$message_id
]);
}
}
}

// video
if($settings["lock"]["video"] == "مقفول️"){
if ( $status != 'creator' && $status != 'administrator' && !in_array($from_id,$Dev) && !in_array($from_id,$getCCmember) && !in_array($from_id,$useradmin) && !in_array($from_id,$mmyaz) ){ 
if ($update->message->video){  
bot('deletemessage',[
'chat_id'=>$chat_id,
'message_id'=>$message_id
]);
  }
}
}
// video r
if($settings["lock"]["videor"] == "مقفول️"){
if ( $status != 'creator' && $status != 'administrator' && !in_array($from_id,$Dev) && !in_array($from_id,$getCCmember) && !in_array($from_id,$useradmin) && !in_array($from_id,$mmyaz) ){ 
if ($update->message->video){  
bot('deletemessage',[
'chat_id'=>$chat_id,
'message_id'=>$message_id,
]);
bot('restrictChatMember',[
   'user_id'=>$from_id,   
   'chat_id'=>$chat_id,
   'can_post_messages'=>false,
]);
  }
}
}
// edit 
if($editgetsettings["lock"]["edit"] == "مقفول️"){
if ( $you != 'creator' && $you != 'administrator' && $edit_for_id != $Dev && $edit_for_id != $getCCmember && $edit_for_id != $useradmin && $edit_for_id != $mmyaz){
if ($update->edited_message->text){  
bot('deletemessage',[
'chat_id'=>$chat_edit_id,
'message_id'=>$message_edit_id
]);
}
}
}
// contact
if ($settings["lock"]["contact"] == "مقفول️"){
if($update->message->contact){
if ($tc == 'group' | $tc == 'supergroup'){
if ( $status != 'creator' && $status != 'administrator' && !in_array($from_id,$Dev) && !in_array($from_id,$getCCmember) && !in_array($from_id,$useradmin) && !in_array($from_id,$mmyaz) ){ 
bot('deletemessage',[
'chat_id'=>$chat_id,
'message_id'=>$message_id
]);
}
}
}
}

// tag
if ($settings["lock"]["tag"] == "مقفول️"){
if (strstr($text,"#") == true or strstr($caption,"#") == true) {
if ($tc == 'group' | $tc == 'supergroup'){
if ( $status != 'creator' && $status != 'administrator' && !in_array($from_id,$Dev) && !in_array($from_id,$getCCmember) && !in_array($from_id,$useradmin) && !in_array($from_id,$mmyaz) ){ 
bot('deletemessage',[
'chat_id'=>$chat_id,
'message_id'=>$message_id
]);
}
}
}
}
// username 
if ($settings["lock"]["username"] == "مقفول️"){
if (strstr($text,"@") == true or strstr($caption,"@") == true) {
if ($tc == 'group' | $tc == 'supergroup'){
if ( $status != 'creator' && $status != 'administrator' && !in_array($from_id,$Dev) && !in_array($from_id,$getCCmember) && !in_array($from_id,$useradmin) && !in_array($from_id,$mmyaz) ){ 
bot('deletemessage',[
'chat_id'=>$chat_id,
'message_id'=>$message_id
]);
}
}
}
}
// audio
if ($settings["lock"]["audio"] == "مقفول️"){
if($update->message->audio){
if ($tc == 'group' | $tc == 'supergroup'){
if ( $status != 'creator' && $status != 'administrator' && !in_array($from_id,$Dev) && !in_array($from_id,$getCCmember) && !in_array($from_id,$useradmin) && !in_array($from_id,$mmyaz) ){ 
bot('deletemessage',[
'chat_id'=>$chat_id,
'message_id'=>$message_id
]);
}
}
}
}
// voice 
if ($settings["lock"]["voice"] == "مقفول️"){
if($update->message->voice){
if ($tc == 'group' | $tc == 'supergroup'){
if ( $status != 'creator' && $status != 'administrator' && !in_array($from_id,$Dev) && !in_array($from_id,$getCCmember) && !in_array($from_id,$useradmin) && !in_array($from_id,$mmyaz) ){ 
bot('deletemessage',[
'chat_id'=>$chat_id,
'message_id'=>$message_id
]);
}
}
}
}
if($settings["lock"]["bot"] == "مقفول️"){
if ($message->new_chat_member->is_bot) {
$hardmodebot = $settings["information"]["hardmodebot"];
if($hardmodebot == "مفتوح"){
 bot('kickChatMember',[
 'chat_id'=>$chat_id,
  'user_id'=>$update->message->new_chat_member->id
  ]);
}
else
{
 bot('kickChatMember',[
 'chat_id'=>$chat_id,
  'user_id'=>$update->message->new_chat_member->id
  ]);
}
}
}
// kick bots and user
if($settings["lock"]["botk"] == "مقفول️"){
if ($message->new_chat_member->is_bot) {
$hardmodebot = $settings["information"]["hardmodebot"];
if($hardmodebot == "مفتوح"){
 bot('kickChatMember',[
 'chat_id'=>$chat_id,
  'user_id'=>$update->message->new_chat_member->id
  ]);
}
else
{
 bot('kickChatMember',[
 'chat_id'=>$chat_id,
  'user_id'=>$update->message->new_chat_member->id
  ]);
   bot('kickChatMember',[
 'chat_id'=>$chat_id,
  'user_id'=>$from_id
  ]);
}
}
}
// sticker
if ($settings["lock"]["sticker"] == "مقفول️"){
if($update->message->sticker){
if ($tc == 'group' | $tc == 'supergroup'){
if( $status != 'creator' && $status != 'administrator' && !in_array($from_id,$Dev) && !in_array($from_id,$useradmin) && !in_array($from_id,$getCCmember)  && !in_array($from_id,$mmyaz) ){
bot('deletemessage',[
'chat_id'=>$chat_id,
'message_id'=>$message_id
]);
}
}
}
}
// forward
if ($settings["lock"]["forward"] == "مقفول️"){
if($update->message->forward_from | $update->message->forward_from_chat){
if ($tc == 'group' | $tc == 'supergroup'){
if( $status != 'creator' && $status != 'administrator' && !in_array($from_id,$Dev) && !in_array($from_id,$useradmin) && !in_array($from_id,$getCCmember) ){
 bot('deletemessage',[
'chat_id'=>$chat_id,
'message_id'=>$message->message_id
]);
 }
}
}
}

//forward restrict
if ($settings["lock"]["forwardr"] == "مقفول️"){
if($update->message->forward_from | $update->message->forward_from_chat){
if ($tc == 'group' | $tc == 'supergroup'){
if( $status != 'creator' && $status != 'administrator' && !in_array($from_id,$Dev) && !in_array($from_id,$useradmin) && !in_array($from_id,$getCCmember)  && !in_array($from_id,$mmyaz) ){

 bot('deletemessage',[
'chat_id'=>$chat_id,
'message_id'=>$message->message_id,
]);
bot('restrictChatMember',[
   'user_id'=>$from_id,   
   'chat_id'=>$chat_id,
   'can_post_messages'=>false,
]);
 }
}
}
}


// fosh 
if ($settings["lock"]["fosh"] == "مقفول️"){
if (strstr($text,"كس") == true  or strstr($text,"ذب") == true or strstr($text,"اير") == true  or  strstr($text,"شرموطة") == true   or strstr($text,"الاسد") == true) {
if ($tc == 'group' | $tc == 'supergroup'){
if( $status != 'creator' && $status != 'administrator' && !in_array($from_id,$Dev) && !in_array($from_id,$useradmin) && !in_array($from_id,$getCCmember)  && !in_array($from_id,$mmyaz) ){

bot('deletemessage',[
'chat_id'=>$chat_id,
'message_id'=>$message_id
]);
bot('restrictChatMember',[
   'user_id'=>$from_id,   
   'chat_id'=>$chat_id,
   'can_post_messages'=>false,
   'until_date'=>time()+1800,
]);
}
}
}
}
//arabic
if ($settings["lock"]["ar"] == "مقفول️"){
if (strstr($text,"ض") == true  or strstr($text,"ص") == true or strstr($text,"ق") == true  or  strstr($text,"ف") == true   or strstr($text,"غ") == true or  strstr($text,"ع") == true  or strstr($text,"ه") == true or strstr($text,"خ") == true  or  strstr($text,"ح") == true   or strstr($text,"ج") == true or strstr($text,"ش") == true  or strstr($text,"س") == true or strstr($text,"ي") == true  or  strstr($text,"ب") == true   or strstr($text,"ل") == true or  strstr($text,"ا") == true  or strstr($text,"ت") == true or strstr($text,"ن") == true  or  strstr($text,"م") == true   or strstr($text,"ك") == true or strstr($text,"ظ") == true or strstr($text,"ط") == true  or  strstr($text,"ذ") == true   or strstr($text,"د") == true or  strstr($text,"ز") == true  or strstr($text,"ر") == true or strstr($text,"و") == true  or  strstr($text,"ة") == true   or strstr($text,"ث") == true or strstr($text,"ؤ") == true  or strstr($text,"ء") == true or strstr($text,"ى") == true  or  strstr($text,"ئ") == true   or strstr($text,"آ") == true or  strstr($text,"إ") == true  or strstr($text,"أ") == true ) {
if ($tc == 'group' | $tc == 'supergroup'){
if( $status != 'creator' && $status != 'administrator' && !in_array($from_id,$Dev) && !in_array($from_id,$useradmin) && !in_array($from_id,$getCCmember)  && !in_array($from_id,$mmyaz) ){

bot('deletemessage',[
'chat_id'=>$chat_id,
'message_id'=>$message_id
]);
}
}
}
}
//English
if ($settings["lock"]["en"] == "مقفول️"){
if (strstr($text,"q") == true  or strstr($text,"w") == true or strstr($text,"e") == true  or  strstr($text,"r") == true   or strstr($text,"t") == true or  strstr($text,"y") == true  or strstr($text,"u") == true or strstr($text,"i") == true  or  strstr($text,"o") == true   or strstr($text,"p") == true or strstr($text,"a") == true  or strstr($text,"s") == true or strstr($text,"d") == true  or  strstr($text,"f") == true   or strstr($text,"g") == true or  strstr($text,"h") == true  or strstr($text,"j") == true or strstr($text,"k") == true  or  strstr($text,"l") == true   or strstr($text,"z") == true or strstr($text,"x") == true or strstr($text,"c") == true  or  strstr($text,"v") == true   or strstr($text,"b") == true or  strstr($text,"n") == true  or strstr($text,"m") == true or strstr($text,"Q") == true  or  strstr($text,"X") == true   or strstr($text,"C") == true or strstr($text,"F") == true  or strstr($text,"G") == true or strstr($text,"H") == true  or  strstr($text,"A") == true   or strstr($text,"L") == true or  strstr($text,"O") == true  or strstr($text,"P") == true ) {
if ($tc == 'group' | $tc == 'supergroup'){
if( $status != 'creator' && $status != 'administrator' && !in_array($from_id,$Dev) && !in_array($from_id,$useradmin) && !in_array($from_id,$getCCmember)  && !in_array($from_id,$mmyaz) ){
bot('deletemessage',[
'chat_id'=>$chat_id,
'message_id'=>$message_id
]);
}
}
}
}
//iduser
 

 $rec = $update->channel_post->reply_to_message->text;
$from_id = $message->from->id;
 date_default_timezone_set('Asia/Riyadh');

date_default_timezone_set('Asia/Baghdad');
$today = date("l");
$nmonth = date("m");
$times = date("h:i");
$year = date("Y");

switch ($today) 
{
case "Saturday":  
$today="السبت"; 
break; 
case "Sutoday":  
$today="الأحد"; 
break;  
case "Motoday":  
$today="الاثنين"; 
break; 
case "Tuesday":  
$today="الثلاثاء"; 
break; 
case "Wednesday": 
$today="الأربعاء"; 
break; 
case "Thursday":  
$today="الخميس"; 
break; 
case "Friday":  
$today="الجمعة"; 
break; 
}  
$date = date('h:i:s'); $d = date('A');
 $aa =preg_replace('/AM/', 'ص', $d);$aa =preg_replace('/PM/', 'م', $d);
date_default_timezone_set('Asia/Baghdad');
$time = date('h:i a');
$year = date('Y');
$month = date('n');
$day = date('j');
$time = time() + (979 * 11 + 1 + 30);
$JJ = "http://api.telegram.org/bot".API_KEY."/getChatMembersCount?chat_id=$chat_id";
$JJ1 = file_get_contents($JJ);
$JJ11 = json_decode($JJ1);
$JJ111 = $JJ11->result;
$from_id    = $message->from->id;
$text       = $message->text;
$chat_id    = $message->chat->id;
$new        = $message->new_chat_member;
$left       = $update->message->left_chat_member;
$result2    = $json2->result;
$contact    = $update->message->contact;
$audio      = $update->message->audio;
$location   = $update->message->location;
$memb       = $update->message->message_id;
$game       = $update->message->game; 
$name       = $update->message->from->first_name;
$re         = $update->message->reply_to_message;
$re_msgid   = $update->message->reply_to_message->message_id;
$re_id      = $update->message->reply_to_message->from->id;
$gp_name    = $update->message->chat->title;
$user       = $update->message->from->username;
$for        = $update->message->from->id;
$sticker    = $update->message->sticker;
$number     = str_word_count($text);
$_spam = file_get_contents("data/$chat_id/spam.txt");
$spam_ = explode("\n",$_spam);
$numper     = strlen($text);
$video      = $update->message->video;
$photo_      = $update->message->photo;
$voice      = $update->message->voice;
$bsma     = $update->message->voice;
$doc        = $update->message->document;
$fwd        = $update->message->forward_from;
$re         = $update->message->reply_to_message;
$re_id      = $update->message->reply_to_message->from->id;
$re_user    = $update->message->reply_to_message->from->username;
$re_msgid   = $update->message->reply_to_message->message_id;
$type       = $update->message->chat->type;
$mid        = $message->message_id;
$buyy   =  file_get_contents("username.php");
$by       =  explode("@",$buyy);
$sudo   = file_get_contents("sudo.php");
$admin = file_get_contents("sudo.php");
$msgs = json_decode(file_get_contents('msgs.json'),true);
$update = json_decode(file_get_contents('php://input'));
$message = $update->message;
$text = $message->text;
$chat_id = $message->chat->id;
$from_id = $message->from->id;
$first_name = $message->from->first_name;
if($message){
$msgs['msgs'][$chat_id][$from_id] = ($msgs['msgs'][$chat_id][$from_id]+1);
$rec = $update->channel_post->reply_to_message->text;
$from_id = $message->from->id;
date_default_timezone_set('Asia/Riyadh');
$date = date('h:i:s'); $d = date('A');
$aa =preg_replace('/AM/', 'ص', $d);$aa =preg_replace('/PM/', 'م', $d);
file_put_contents('msgs.json', json_encode($msgs));}

$set        = file_get_contents("data/$chat_id.txt");
$ex         = explode("\n", $set);
$photo1     = $ex[0];
$sticker1   = $ex[1];
$contact1   = $ex[2];
$doc1       = $ex[3];
$fwd1       = $ex[4];
$voice1     = $ex[5];
$link1      = $ex[6];
$audio1     = $ex[7];
$video1     = $ex[8];
$tag1       = $ex[9];
$mark1      = $ex[10];
$bots1      = $ex[11];
$number1      = $ex[12];
$onlyibadlz       = file_get_contents("data/restrictChatMember/$chat_id.txt");
$_ex         = explode("\n", $onlyibadlz);
$photo2     = $_ex[0];
$sticker2   = $_ex[1];
$contact2   = $_ex[2];
$doc2       = $_ex[3];
$fwd2       = $_ex[4];
$voice2     = $_ex[5];
$link2      = $_ex[6];
$audio2     = $_ex[7];
$video2     = $_ex[8];
$tag2       = $_ex[9];
$mark2      = $_ex[10];
$bots2      = $_ex[11];

mkdir("data");
mkdir("data/restrictChatMember");

$get             = file_get_contents("https://api.telegram.org/bot$API_KEY/getChatMember?chat_id=$chat_id&user_id=".$from_id);
$info            = json_decode($get, true);
$JJ117        = $info['result']['status'];

$command = array("id","/id","ايدي");

$get_myid = file_get_contents("data/ids/idset.txt");
$_get_ = file_get_contents("data/ids/id.txt");
$get_ALONE = file_get_contents("data/ids/id_.txt");
$GETGG1ZZ = file_get_contents("data/ids/iBadlz.txt");
$_GG1ZZ_ = explode("\n",$GETGG1ZZ);

if($message and $type == "supergroup"){
$msgs = json_decode(file_get_contents('msgs.json'),true);
$update = json_decode(file_get_contents('php://input'));
$msgs['msgs'][$chat_id][$from_id] = ($msgs['msgs'][$chat_id][$from_id]+1);
file_put_contents('msgs.json', json_encode($msgs));}
$result=json_decode(file_get_contents("https://api.telegram.org/bot".API_KEY."/getUserProfilePhotos?user_id=$from_id"),true);
$file_id=$result["result"]["photos"][0][0]["file_id"];
$count=$result["result"]["total_count"];
$game = json_decode(file_get_contents('game.json'),true);
$from_user = $message->from->username;
$from_name = $message->from->first_name;
$get_game = file_get_contents("game.txt");

if($msgs['msgs'][$chat_id][$from_id] > 3000){
$active = array(
"خوش متفاعل ","متفاعل ","اسطورة التفاعل ","الله مال تفاعل ","نايس التفاعل",'قوي جدا ',  'قمه التفاعل ',  'اقوى تفاعل ',);
$JJ119 = array_rand($active,1);
}elseif($msgs['msgs'][$chat_id][$from_id] > 500){
$active = array('متوسط  ',  'متفاعل ',);
$JJ119 = array_rand($active,1);
}elseif($msgs['msgs'][$chat_id][$from_id] > 1){
$active = array('تفاعل زفت','ضعيف جدا ',);
$JJ119 = array_rand($active,1);
}
if($msgs['msgs'][$chat_id][$from_id] > 3000){
$Free3 = array("1000% ","999% ","100% ",);
$Free4 = array_rand($Free3,1);
}elseif($msgs['msgs'][$chat_id][$from_id] > 500){
$Free3 = array('80% ','84% ',);
$Free4 = array_rand($Free3,1);
}elseif($msgs['msgs'][$chat_id][$from_id] > 1){
$Free3 = array('18% ','20% ','6% ',);
$Free4 = array_rand($Free3,1);
}if($msgs['msgs'][$chat_id][$from_id] > 200){
$Free3 = array("40% ","43% ",);
$Free4 = array_rand($Free3,1);
}
$Free1 = array(
    "منور يا غالي، طالع كمر 🌕",
    "ما شاء الله، طالع كشخة وهيبة 👑",
    "هاي شنو، الحلاوة زايدة اليوم ✨",
    "عليك نور يا طيب، نورتنا 🌹",
    "صورة ترد الروح، عاش ذوقك 💎",
    "لا تغيرها، والله كلش حلوة عليك 🤚",
    "هاي وين صاير هالحلا؟ منين أخذتها؟ 📸",
    "أوف، تجنن والله، ذوقك راقي 👑",
    "مو كلش، جرب تغيرها بلكي تطلع أحلى 😅",
    "دخيلك غيرها، هاي ما تلوق لمقامك 💔",
    "حطمت قلوب البنات، اركد شوية 😂",
    "بعد روحي، طالع قطعة من العسل 🍯",
    "صدقني روعة، لا تسمع كلام أحد 🔥",
    "صارت قديمة، نزلنا شي جديد من إبداعك ⏳",
    "ممكن الصورة؟ خبلتني والله 😍",
    "الله عليك يا مبدع، طالع نمبر وان 🏆",
    "أفضل صورة شفتها اليوم بطلتك ✨",
    "ما تعجبني، أنت أحلى بكتير من هاي 🧐",
    "روعاتك يا بطل، طالع كحيل العين 👁️",
    "والله قوة، هيبة وما تنهز 🦁",
    "فد شي خيالي، ذوقك فن وهندسة 🎨",
    "لا تكثر أيدي، ترى عيونهم عليك الحساد 🧿",
    "طالع چنك كيمر سدة، منورنا 🥛",
    "يا يابة على هالجمال، عراقي أصيل 🇮🇶",
    "هنيال اللي يشوفك، منور الكروب 🌟",
    "طالع صكّار، الهيبة تفصلت الك 🦅",
    "شني هاي؟ طالع تفليش والله 🔥",
    "ذوقك ترف، مثل روحك الطيبة 🌸",
    "طالع كيك، ناقصك بس شكر 🍰",
    "عاشت إيد الصورك، طلع الإبداع كله 👏",
    "هيبة ووقار، ربي يحفظك يا بطل 🛡️",
    "طالع چنك العافية، نورتنا ✨",
    "يا عيني على الضحكة، دومها يا رب 😊",
    "طالع لوز، ما محتاج أي فلتر 💎",
    "هاي شنو الجمال؟ عزلوا مكاتب الصور 😂",
    "أنت وبس، والباقي كله خس 🥬",
    "طالع منور، چنك شمس الشموس ☀️",
    "فديت هالطلة، تفتح النفس والله 😍",
    "طالع غزال، والعيون تحرسك 🧿",
    "أنا أشهد إنك ملك الجمال اليوم 👑",
    "طالع ذيب، الهيبة مرسومة عليك رسم 🐺",
    "بعد قلبي، طالع ترف وكلش نزاكة ✨",
    "شنو هالأناقة؟ طالع عريس اليوم 🤵",
    "صورة عالمية، تستاهل مليون لايك 👍",
    "طالع كمر 14، ما بيك أي لولة 🌕",
    "ذوقك نار، دمرت الكروب بهالطلة 🔥",
    "يا هلا بهالوجه الطيب، نورتنا 🌹",
    "طالع فد شي، هيبة وأصل وفصل 🏆",
    "يا ويلي على الأناقة، طالع مرتب 👔",
    "صورة للتاريخ، خلدت الجمال بيها 📜",
    "طالع قطعة من الجنة، ربي يحميك ✨",
    "أنت والجمال قصة ما تنتهي 📖❤️"
);

$Free2 = array_rand($Free1,1);
$mid = file_get_contents("mid.txt");


if(in_array($from_id,$Dev)){
$info = "المطور الاساسي 👨🏻‍✈️";
}elseif($status == "creator"){
$info = "منشىء المجموعة 🕵";
}elseif($status == "administrator"){
$info = "مشرف المجموعة 👮";
}elseif(in_array($from_id,$admin_user) ){
$info = "ادمن في البوت 👨🏼‍🎓";
}elseif(in_array($from_id,$manger) ){
$info = "مدير البوت 👨🏼‍⚕️";
}elseif(in_array($from_id,$mmyaz) ){
$info = "عضو مميز ⭐️";
}elseif($status == "member" ){
$info = "فقط عضو 🙍🏼‍♂️";
}
if($user){
$usr = "@$user";
}if($file_id == NULL){
$photo = "لاتمتلك صوره في الحساب";
}
if($msgs['msgs'][$chat_id][$from_id] > 3000){
$active = array("خوش متفاعل 🌝","متفاعل ✨","اسطورة التفاعل 🌈ء","الله مال تفاعل ⚜","نايس التفاعل 💘ء",'قوي جدا ⚡️ ',  'قمه التفاعل ✨ ',  'اقوى تفاعل 🔥 ',);
$JJ119 = array_rand($active,1);
}elseif($msgs['msgs'][$chat_id][$from_id] > 500){
$active = array('متوسط  ',  'متفاعل ',);
$JJ119 = array_rand($active,1);
}elseif($msgs['msgs'][$chat_id][$from_id] > 1){
$active = array('غير متفاعل ', 'ضعيف ',);
$JJ119 = array_rand($active,1);
}
$unid = explode("\n",file_get_contents("data/ids/unid.txt"));
if(!in_array("GG1ZZ",$_GG1ZZ_) and !in_array("MOHAMMED",$unid)){
if(!$re and in_array($text,$command)){
bot("sendphoto",[
  "chat_id"=>$chat_id,
  "caption"=>"🖇️┐صورتك ⊰• $Free1[$Free2] ⊰•
👤┤اسمـك ⊰• $first_name ⊰•
🎟┤ايديـك •⊱ **`$from_id`**⊰•
🎫┤معرفـك •⊱ [@$username] ⊰•
📡┤رتبتـك •⊱ $info ⊰•
⭐️┤تفاعلك •⊱ $active[$JJ119]⊰•
💬┤رسائلك •⊱ **".$msgs[ msgs ][$chat_id][$from_id]."** ⊰•
📝┤سكحاتك •⊱ **$editt** ⊰•
📷┤عدد صورك ⊰•  **$count** ⊰•
🏆┘نقاطك •⊱ $coinat ⊰•
➖ 
",
"photo"=>"$file_id",
'parse_mode'=>'MarkDown', 'disable_web_page_preview'=>true,
  'reply_to_message_id'=>$message->message_id,
  ]);
  }if(!$re and in_array($text,$command) and $file_id == null){
bot("sendmessage",[
  "chat_id"=>$chat_id,
  "text"=>"🛤┐$photo ⊰•
🖇️┤صورتك ⊰• $Free1[$Free2] ⊰•
👤┤اسمـك ⊰• $first_name ⊰•
🎟┤ايديـك •⊱ **`$from_id`**⊰•
🎫┤معرفـك •⊱ [@$username]⊰•
📡┤رتبتـك •⊱ $info⊰•
⭐️┤تفاعلك •⊱ $active[$JJ119]⊰•
💬┤رسائلك •⊱ **".$msgs[ msgs ][$chat_id][$from_id]."** ⊰•
📝┤سكحاتك •⊱ **$editt** ⊰•
📷┤عدد صورك ⊰•  **$count** ⊰•
🏆┘نقاطك •⊱ **$coinat**⊰•
➖ 
",
  'parse_mode'=>'MarkDown', 'disable_web_page_preview'=>true,
  'reply_to_message_id'=>$message->message_id,
  ]);
}}
 
/*———————Here is done the id with out remake—————*/

$loran22 = "* اهلٱ بك عزيزي المطور ، اليَك قائمةه الدوال لتعينهٱ لكَود الأيدي ،💘💘'
————————————————
- لـَطبع الٱيدي :* `IDGET`
*- لـَطبع ٱلمعرف :* `[@USERGET]`
*- لـَطبع ٱلرتبه :* `RTBGET`
*- لـَطبع ٱلتفاعل :* `TFGET`
*- لـَطبع الرسٱئل :* `MSGGET`
*- لـَطبع النقود :* `NKOGET`
*- لـَطبع ٱلصور :* `PICGET`

• ملٱحظه : يمكن استعمٱل هذه الدوال لطبٱعه امر معين كمثٱل عند ارسال للبوت هكذا : 
ايديك : `IDGET` فٱنهَ سوف يقوم بطباعه ايدي الاشخاص عند كتٱبه *(ايدي)* 🖤🖤! 

- للٱستفسٱر : @GG1ZZBOT ،🔰'";
if($from_id == $sudo){
if($text == "تعين الايدي" || $text == "تغير الايدي" || $text == "تعيين الايدي"){
	 mkdir("data");    /* Thanks ! for Using MY Code */   mkdir("data/ids");
    file_put_contents("data/ids/iBadlz.txt","GG1ZZ");
	file_put_contents("data/ids/id_.txt","MOHAMMED");
	bot("sendMessage",[
	'chat_id'=>$chat_id,
	'text'=>$loran22,
	'parse_mode'=>"MARKDOWN",
    'reply_to_message_id' =>$message->message_id, 
	]);
	}
	if($text and $get_ALONE == "MOHAMMED"){
	file_put_contents("data/ids/idset.txt",$text);
	file_put_contents("data/ids/id.txt",$text);
	file_put_contents("data/ids/id_.txt","");
	bot("sendMessage",[
	'chat_id'=>$chat_id,
	'text'=>"🚸¦ تم تغغَير كود الٱيدي .",
	'parse_mode'=>"MARKDOWN",
    'reply_to_message_id' =>$message->message_id, 
	]);
	}
	if($text == "مسح الايدي" || $text == "حذف الايدي" || $text == "ازاله الايدي"){
    file_put_contents("data/ids/iBadlz.txt","");
	bot("sendMessage",[
	'chat_id'=>$chat_id,
	'text'=>"🚸¦ تم مسح كود الٱيدي المَعدل .",
	'parse_mode'=>"MARKDOWN",
    'reply_to_message_id' =>$message->message_id, 
	    ]);
   }
}
if(in_array("GG1ZZ",$_GG1ZZ_) and !in_array("MOHAMMED",$unid)){
if(!$re and in_array($text,$command)){
$JJ115 = array("IDGET","USERGET","NKOGET","MSGGET","TFGET","RTBGET","PICGET");$JJ118 = array($from_id ,$user,$game['game'][$chat_id][$from_id],$msgs['msgs'][$chat_id][$from_id],$active[$JJ119],$RTBGET,$count);$_iBadlz_ = str_replace($JJ115, $JJ118 , $get_myid);file_put_contents("data/ids/idset.txt",$_iBadlz_);
  bot("sendphoto",[
  "chat_id"=>$chat_id,
  "caption"=>"$_iBadlz_",
"photo"=>"$file_id",
'parse_mode'=>'MarkDown', 'disable_web_page_preview'=>true,
  'reply_to_message_id'=>$message->message_id,
  ]);
  file_put_contents("data/ids/idset.txt",$_get_);
  }if(!$re and in_array($text,$command) and $file_id == null){
   $JJ115 = array("IDGET","USERGET","NKOGET","MSGGET","TFGET","RTBGET","PICGET");$JJ118 = array($from_id ,$user,$game['game'][$chat_id][$from_id],$msgs['msgs'][$chat_id][$from_id],$active[$JJ119],$RTBGET,$count);$_iBadlz_ = str_replace($JJ115, $JJ118 , $get_myid);file_put_contents("data/ids/idset.txt",$_iBadlz_);
   bot("sendmessage",[
  "chat_id"=>$chat_id,
  "text"=>"$_iBadlz_
🚸¦ $photo",
'parse_mode'=>'MarkDown', 'disable_web_page_preview'=>true,
  'reply_to_message_id'=>$message->message_id,
     ]);
     file_put_contents("data/ids/idset.txt",$_get_);
   }
}
if($text == "تعطيل الايدي" and $JJ117 == "creator" || $JJ117 == "administrator" || $from_id == $sudo || in_array($from_id,$dev) || in_array($from_id,$manger)){file_put_contents("data/ids/unid.txt","MOHAMMED");bot("SendMessage",["chat_id"=>$chat_id,"text"=>"",'parse_mode'=>'MarkDown', 'disable_web_page_preview'=>true,'reply_to_message_id'=>$message->message_id,]);}if($text == "تفعيل الايدي" and $JJ117 == "creator" || $JJ117 == "administrator" || $from_id == $sudo || in_array($from_id,$dev) || in_array($from_id,$manger)){file_put_contents("data/ids/unid.txt","");bot("SendMessage",["chat_id"=>$chat_id,"text"=>"",'parse_mode'=>'MarkDown', 'disable_web_page_preview'=>true,'reply_to_message_id'=>$message->message_id,]);}
if(!$re and in_array($text,$command) and in_array("MOHAMMED",$unid)){bot("sendmessage",["chat_id"=>$chat_id,"text"=>"- سلامتك شو صار لايدك😾",'parse_mode'=>'MarkDown', 'disable_web_page_preview'=>true,'reply_to_message_id'=>$message->message_id,]);}
if($text=="صورتي"){
$photo = "https://t.me/$user";
bot('SendPhoto',[
'chat_id'=>$chat_id,
'photo'=>$file_id,
'caption'=>"
صورتك : [@$from_user]
",
'message_id'=>$message->message_id,
'reply_to_message_id' =>$message->message_id, 
]);
}

 




 
// muteall
if ($settings["lock"]["mute_all"] == "مقفول️"){
if($update->message){
if ( $status != 'creator' && $status != 'administrator' && !in_array($from_id,$Dev) ){
 bot('deletemessage',[
'chat_id'=>$chat_id,
'message_id'=>$message->message_id
]);
 }
}
}
//tsmet ♥
if ($settings["lock"]["tsmet"] == "مقفول️"){
if($update->message){
if ( $status != 'creator' &&  !in_array($from_id,$Dev) ){
 bot('deletemessage',[
'chat_id'=>$chat_id,
'message_id'=>$message->message_id
]);
 }
}
}
//markdown
if ($settings["lock"]["markdowns"] == "مقفول️"){
if($update->message->entities){
if( $status != 'creator' && $status != 'administrator' && !in_array($from_id,$Dev) && !in_array($from_id,$useradmin) && !in_array($from_id,$getCCmember)  && !in_array($from_id,$mmyaz) ){

 bot('deletemessage',[
'chat_id'=>$chat_id,
'message_id'=>$message->message_id
]);
 }
}
}
// muteall time
if ($settings["lock"]["mute_all_time"] == "مقفول️"){
$locktime = $settings["information"]["mute_all_time"];
date_default_timezone_set('Asia/Damascus');
$date1 = date("h:i:s");
if($date1 < $locktime){
if($update->message){
if ( $status != 'creator' && $status != 'administrator' && !in_array($from_id,$Dev) ){
 bot('deletemessage',[
'chat_id'=>$chat_id,
'message_id'=>$message->message_id
]);
 }
else
{
$settings["lock"]["mute_all_time"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
}
// replay
if ($settings["lock"]["reply"] == "مقفول️"){
if($update->message->reply_to_message){
if ($tc == 'group' | $tc == 'supergroup'){
if( $status != 'creator' && $status != 'administrator' && !in_array($from_id,$Dev) && !in_array($from_id,$useradmin) && !in_array($from_id,$getCCmember)  && !in_array($from_id,$mmyaz) ){
 bot('deletemessage',[
'chat_id'=>$chat_id,
'message_id'=>$message->message_id
]);
 }
}
}
}
// tg
if ($settings["lock"]["tgservic"] == "مقفول️"){
if($update->message->new_chat_member | $update->message->new_chat_photo | $update->message->new_chat_title | $update->message->left_chat_member | $update->message->pinned_message){
if ($tc == 'group' | $tc == 'supergroup'){
if ( $status != 'creator' && $status != 'administrator' && !in_array($from_id,$Dev) ){
 bot('deletemessage',[
'chat_id'=>$chat_id,
'message_id'=>$message->message_id
]);
 }
}
}
}
// text
if ($settings["lock"]["text"] == "مقفول️"){
if($update->message->text){
if ($tc == 'group' | $tc == 'supergroup'){
if ( $status != 'creator' && $status != 'administrator' && !in_array($from_id,$Dev) ){
 bot('deletemessage',[
'chat_id'=>$chat_id,
'message_id'=>$message->message_id
]);
 }
}
}
}
// video note
if ($settings["lock"]["video_msg"] == "مقفول️"){
if($update->message->video_note){
if ($tc == 'group' | $tc == 'supergroup'){
if ( $status != 'creator' && $status != 'administrator' && !in_array($from_id,$Dev) && !in_array($from_id,$getCCmember) && !in_array($from_id,$useradmin) && !in_array($from_id,$mmyaz)) {
 bot('deletemessage',[
'chat_id'=>$chat_id,
'message_id'=>$message->message_id
]);
 }
}
}
}

$inline = json_decode(file_get_contents('php://input'),true);
if($settings["lock"]["inline"] == "مقفول"){
if ($status !=  creator  && $status !=  administrator  && !in_array($from_id,$Dev) && !in_array($from_id,$manger) && !in_array($from_id,$admin_user) && !in_array($from_id,$mmyaz) && !in_array($from_id,$developer) ){
if(isset($inline['message']['reply_markup']['inline_keyboard'][0][0]['text'])){
bot('deleteMessage',[
'chat_id'=>$message->chat->id,
'message_id'=>$message->message_id
]);
}}}

if($settings["information"]["add"] == "مقفول️") {
if($newchatmemberid == true){
$add = $settings["addlist"]["$from_id"]["add"];
$addplus = $add +1;
$settings["addlist"]["{$from_id}"]["add"]="$addplus";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}

if($settings["information"]["add"] == "مقفول️"){
if( $status != 'creator' && $status != 'administrator' && !in_array($from_id,$Dev) && !in_array($from_id,$useradmin) && !in_array($from_id,$getCCmember)  && !in_array($from_id,$mmyaz) ){

if ($tc == 'group' | $tc == 'supergroup'){
$youadding = $settings["addlist"]["$from_id"]["add"];
$setadd = $settings["information"]["setadd"];
$addtext = $settings["addlist"]["$from_id"]["addtext"];
$msg = $settings["information"]["lastmsgadd"];
if($youadding < $setadd){
if($addtext == false){
bot('SendMessage',[
'chat_id'=>$chat_id,
'text'=>"
🙎‍♂┊عزيزي العضو [$first_name](https://t.me/$username)
🚸┊لتستطيع التكلم اضف $setadd من الاعضاء
",
]);
bot('deletemessage',[
'chat_id'=>$chat_id,
'message_id'=>$message_id
]);
    bot('deletemessage',[
'chat_id'=>$chat_id,
'message_id'=>$msg
]);
$msgplus = $message_id + 1;
$settings["information"]["lastmsgadd"]="$msgplus";
$settings["addlist"]["$from_id"]["addtext"]="true";
$settings["addlist"]["$from_id"]["add"]=0;
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
  }
  else
  {
      bot('deletemessage',[
'chat_id'=>$chat_id,
'message_id'=>$message_id
 ]);
   }
}
  }
}
}
//  game
if($settings["lock"]["game"] == "مقفول️"){
if($update->message->game){
if ($tc == 'group' | $tc == 'supergroup'){
if ( $status != 'creator' && $status != 'administrator' && !in_array($from_id,$Dev) && !in_array($from_id,$getCCmember) && !in_array($from_id,$useradmin) ){
bot('deletemessage',[
'chat_id'=>$chat_id,
'message_id'=>$message_id
]);
}
}
}
}
// location
if ($settings["lock"]["location"] == "مقفول️"){
if($update->message->location){
if ($tc == 'group' | $tc == 'supergroup'){
if ( $status != 'creator' && $status != 'administrator' && !in_array($from_id,$Dev) && !in_array($from_id,$getCCmember) && !in_array($from_id,$useradmin) ){
bot('deletemessage',[
'chat_id'=>$chat_id,
'message_id'=>$message_id
]);
}
}
}
}
//spam
 date_default_timezone_set('Asia/Damascus');
$as = date('i')+15;
if ( $status == 'creator' or $status == 'administrator' or in_array($from_id,$Dev) or in_array($from_id,$getCCmember) or in_array($from_id,$useradmin)) {
  if(strpos($text,"وضع تكرار") !== false){
mkdir("data/$chat_id");
mkdir("spam");
$spamx = str_replace("وضع تكرار ","",$text);
if(is_numeric($spamx)){
 if($spamx > 0){
file_put_contents("data/$chat_id/spamxe.txt",$spamx);
file_put_contents("spam/tim.txt",$as); 
var_dump(bot('sendMessage',[ 
'chat_id' => $chat_id,
'text' =>"
💬┇بواسطه ~⪼ [$first_name](t.me/$username)
☑┇تم وضع تكرار $spamx",
'parse_mode'=>"markdown",'disable_web_page_preview'=>true,
'reply_to_message_id' => $message->message_id,
]));
}}}}
$weplus = 1 ;
$timex = date("Y-m-d-h-i-A");
$timex = str_replace("am", "", $timex);
@$NBots = file_get_contents("spam/$from_id/$timex.txt");
$timex_spam = $NBots + 1;
mkdir("spam/$from_id");
file_put_contents("spam/$from_id/$timex.txt",$timex_spam);
$NBots2 = file_get_contents("spam/$from_id/$timex.txt");
$NBX = file_get_contents("data/$chat_id/spamxe.txt");
if($NBots2 >=$NBX) {
if ($settings["lock"]["spam"] == "مقفول️"){
var_dump(bot('restrictChatMember',[
'user_id'=>$from_id,   
'chat_id'=>$chat_id,
'can_post_messages'=>false,
'until_date'=>time()+$weplus*1600,
]));
}}
$timer = file_get_contents("spam/tim.txt"); 
if($message and $timer<date('h')){
$dir = "spam";
$all = scandir($dir);
if($all != null){
   foreach($all as $file){
      if($file == '.' or $file == '..') continue;
      if(is_file($dir.'/'.$file)){
         unlink($dir.'/'.$file);
      } elseif(is_dir($dir.'/'.$file)){
          $sc = scandir($dir.'/'.$file);
foreach($sc as $sn){
             if($sn == '.' or $sn == '..') continue;
             unlink($dir.'/'.$file.'/'.$sn);
             rmdir($dir.'/'.$file);
          }
      } 
   }
} else {
   die('not found dir');
}
rmdir($dir);
mkdir($dir);
file_put_contents("spam/tim.txt",$as); 
}
// filter
if($text=="/filterlist" or $text=="filterlist" or $text=="قائمة الفلتر"){
if ( $status == 'creator' or $status == 'administrator' or in_array($from_id,$Dev) or in_array($from_id,$getCCmember) or in_array($from_id,$useradmin)) {
$filter = $settings["filterlist"];
for($z = 0;$z <= count($filter)-1;$z++){
$result = $result.$filter[$z]."\n";
}
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
⚠┊قائمة الكلمات الممنوعه ،
┉ ┉ ┉ ┉ ┉ ┉ ┉ ┉ ┉ 
|🔘|~⪼($result)
",
     'reply_to_message_id'=>$message_id,
'reply_markup'=>$inlinebutton,
 ]);
}
}
elseif (strpos($text , "/filter ") !== false or strpos($text , "فلترة كلمة") !== false) {
if ( $status == 'creator' or $status == 'administrator' or in_array($from_id,$Dev) or in_array($from_id,$getCCmember) or in_array($from_id,$useradmin)) {
$add = $settings["information"]["added"];
if ($add == true) {
$text = str_replace(['/filter ','فلترة كلمة'],'',$text);
bot('sendmessage',[
        'chat_id'=>$chat_id,
        'text'=>"
☑┇تم اضافتها لقائمه المنع
🔘┇{$text}
",
     'reply_to_message_id'=>$message_id,
'reply_markup'=>$inlinebutton,
 ]);
@$settings = json_decode(file_get_contents("data/$chat_id.json"),true);
$settings["filterlist"][]="$text";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
elseif (strpos($text , "/unfilter " ) !== false or strpos($text , "الغاء فلترة") !== false) {
if ( $status == 'creator' or $status == 'administrator' or in_array($from_id,$Dev) or in_array($from_id,$getCCmember) or in_array($from_id,$useradmin)) {
$text = str_replace(['/unfilter ','الغاء فلترة'],'',$text);
bot('sendmessage',[
        'chat_id'=>$chat_id,
        'text'=>"
☑┇تم ازالتها من لقائمه المنع
🔘┇{$text}
",
     'reply_to_message_id'=>$message_id,
'reply_markup'=>$inlinebutton,
 ]);
@$settings = json_decode(file_get_contents("data/$chat_id.json"),true);
$key = array_search($text,$settings["filterlist"]);
unset($settings["filterlist"][$key]);
$settings["filterlist"] = array_values($settings["filterlist"]); 
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
if($text== "/clean filterlist" or $text=="clean filterlist" or $text=="مسح الفلاتر"){
if ( $status == 'creator' or $status == 'administrator' or in_array($from_id,$Dev) ) {
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
☑┇تم مسح قائمه المنع
",
     'reply_to_message_id'=>$message_id,
'reply_markup'=>$inlinebutton,
 ]);
@$settings = json_decode(file_get_contents("data/$chat_id.json"),true);
unset($settings["filterlist"]);
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}

}
}
if($settings["filterlist"] != false){
if ($status != 'creator' && $status != 'administrator' ) {
$check = check_filter("$text");
if ($check == true) {
bot('deletemessage',[
'chat_id'=>$chat_id,
'message_id'=>$message_id
]);
}
}
}
// setrules
if($settings["information"]["step"] == "setrules"){
if ( $status == 'creator' or $status == 'administrator' or in_array($from_id,$Dev) or in_array($from_id,$getCCmember) or in_array($from_id,$useradmin)){
if ($tc == 'group' | $tc == 'supergroup'){
$plus = mb_strlen("$text");
if($plus < 500) {
bot('sendmessage',[
 'chat_id'=>$chat_id,
 'text'=>"مقفول┇تم وضع القوانين للمجموعه",
  'reply_to_message_id'=>$message_id,
 ]);
$settings["information"]["rules"]="$text";
$settings["information"]["step"]="none";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
else
{
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
❕┇لا تستطيع وضع اكثر من 500 حرف
",
  'reply_to_message_id'=>$message_id,
'reply_markup'=>$inlinebutton,
 ]);
}
}
}
}
// lock channel 
/*
if($settings["information"]["lockchannel"] == "مقفول️"){
if( $status != 'creator' && $status != 'administrator' && !in_array($from_id,$Dev) && !in_array($from_id,$useradmin) && !in_array($from_id,$getCCmember)  && !in_array($from_id,$mmyaz) ){

if ($tc == 'group' | $tc == 'supergroup'){
$usernamechannel = $settings["information"]["setchannel"];
@$forchannel = json_decode(file_get_contents("https://api.telegram.org/bot".$token."/getChatMember?chat_id=".$usernamechannel."&user_id=".$from_id));
@$tch = $forchannel->result->status;
if($tch != 'member' && $tch != 'creator' && $tch != 'administrator'){
$msg = $settings["information"]["lastmsglockchannel"];
$channeltext = $settings["channellist"]["$from_id"]["channeltext"];
		if($channeltext == false){
        bot('SendMessage',[
            'chat_id'=>$chat_id,
            'text'=>"
            👤┇العضو ~⪼ [$first_name](t.me/$username)
⚠️┇يجب ان تشترك بالقناة لتكلم هنا
$usernamechannel
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,
        ]);
        bot('deletemessage',[
            'chat_id'=>$chat_id,
        'message_id'=>$message_id
        ]);
		            bot('deletemessage',[
            'chat_id'=>$chat_id,
        'message_id'=>$msg
        ]);
$msgplus = $message_id + 1;
$settings["information"]["lastmsglockchannel"]="$msgplus";
$settings["channellist"]["$from_id"]["channeltext"]="true";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
      }
	  else
	  {
		              bot('deletemessage',[
            'chat_id'=>$chat_id,
        'message_id'=>$message_id
		 ]);
   }
	}
	  }
	}
	}
if($settings["information"]["step"] == "setchannel"){
if ( $status == 'creator' or $status == 'administrator' or in_array($from_id,$Dev) or in_array($from_id,$getCCmember) or in_array($from_id,$useradmin)){
if ($tc == 'group' | $tc == 'supergroup'){
if(strpos($text , '@') !== false) {
$plus = mb_strlen("$text");
if($plus < 25) {
bot('sendmessage',[
 'chat_id'=>$chat_id,
 'text'=>"
💬┇بواسطه ~⪼ [$first_name](t.me/$username)
☑┇تم وضع قناة $text
‼️┇انتبه يجب ان يكون بوت ادمن بالقناة
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,
  'reply_to_message_id'=>$message_id,
 ]);
$settings["information"]["setchannel"]="$text";
$settings["information"]["step"]="none";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
else
{
	bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"⚠️┇خطا المعرف غير مسموح به",
  'reply_to_message_id'=>$message_id,
  
                 
           
 ]);
}
}
else
{
	bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
⚠️┇خطأ يجب ان تضع @ للمعرف  
🔰┇مثال • @$channel •√
",
  'reply_to_message_id'=>$message_id,
           
 ]);
}
}
}
} 
*/


mkdir("SA3ED");
$SAEED0= file_get_contents("https://api.telegram.org/bot$token/getChatMember?chat_id=$chat_id&user_id=".$from_id);
$SAEED1= json_decode($SAEED0, true);
$SAEED2 = $SAEED1['result']['status'];
$ch = file_get_contents("SA3ED/$chat_id.txt");
$join = file_get_contents("https://api.telegram.org/bot$token/getChatMember?chat_id=$ch&user_id=".$from_id);


if($message && (strpos($join,'"status":"left"') or strpos($join,'"Bad Request: USER_ID_INVALID"') or strpos($join,'"status":"kicked"'))!== false){
if($status != "creator" and $status != "administrator"){
bot('DeleteMessage',[
'chat_id'=>$chat_id,
'message_id'=>$message_id
]);
$get =bot("sendMessage",[
"chat_id"=>$chat_id,
"text"=>"👤┇العضو ~⪼ [$first_name](t.me/$username)
⚠️┇يجب ان تشترك بالقناة لتكلم هنا
@$ch
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,
]);
sleep(10);
bot("deleteMessage",[
"chat_id"=>$chat_id,
"message_id"=>$get->result->message_id
]);return false;}}

if($status == "creator" or $status == "administrator" ){
$S = file_get_contents("SA3ED/S$chat_id $from_id.txt");
if($text == "تفعيل الاشتراك الاجباري"){
file_put_contents("SA3ED/S$chat_id $from_id.txt", "1");
file_put_contents("SA3ED/$chat_id.txt", "");
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"- [$first_name](tg://user?id=$from_id) ؛ ❤️
- الان ارسل معرف قناة المجموعة التي لايمكن للاعضاء التكلم فيها الى بعد الاشتراك فيها ؛ ✅
",
'parse_mode'=>"MarkDown",
'disable_web_page_preview' =>true,
]);
}
if($text and $S == "1"){
file_put_contents("SA3ED/$chat_id.txt", "$text");
file_put_contents("SA3ED/S$chat_id $from_id.txt", "");
bot("sendMessage",[
"chat_id"=>$chat_id,
"text"=>"- [$first_name](tg://user?id=$from_id) ؛ ❤️

- تم حفظ قناة المجموعة بنجاح ؛ ✅

- الان تأكد من ان البوت ادمن في القناة لاعمل بالشكل الصحيح ؛ 👨‍✈️",
'parse_mode'=>"MarkDown",
'disable_web_page_preview' =>true,
]);
}
if($text == "تعطيل الاشتراك الاجباري"){
file_put_contents("SA3ED/$chat_id.txt", "");
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"- [$first_name](tg://user?id=$from_id) ؛ ❤️

- تم تعطيل البوت بنجاح ؛ ✅",
'parse_mode'=>"MarkDown",
'disable_web_page_preview' =>true,
]);
}
}

// setwelcome//
if($settings["information"]["step"] == "setwelcome"){
if ( $status == 'creator' or $status == 'administrator' or in_array($from_id,$Dev) or in_array($from_id,$getCCmember) or in_array($from_id,$useradmin)){
if ($tc == 'group' | $tc == 'supergroup'){
$plus = mb_strlen("$text");
if($plus < 200) {
bot('sendmessage',[
 'chat_id'=>$chat_id,
 'text'=>"
مقفول┇تم وضع ترحيب للمجموعه
",'reply_to_message_id'=>$message_id,
 ]);
$settings["information"]["textwelcome"]="$text";
$settings["information"]["step"]="none";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
else
{
	bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"❕┇لا تستطيع وضع اكثر من 200 حرف",
  'reply_to_message_id'=>$message_id,
 
 ]);
}
}
}
}
// banall
elseif ($tc == 'private'){ 
if(in_array($from_id, $user["banlist"])) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"💯 لقد تم حظرك من البوت ♨️",
'reply_markup'=>json_encode(['KeyboardRemove'=>[
],'remove_keyboard'=>true
])
]);
}
}
elseif ($tc == 'group' | $tc == 'supergroup'){ 
if(in_array($from_id, $user["banlist"])) {
	bot('KickChatMember',[
'chat_id'=>$chat_id,
'user_id'=>$from_id
  ]);
}
}
// sup
if($user["userjop"]["$from_id"]["file"] == "sup"&& $tc == "private"){   
if ($text != "🔙 رجوع") {	
bot('ForwardMessage',[
'chat_id'=>$Dev[0],
'from_chat_id'=>$chat_id,
'message_id'=>$message_id
]);
		bot('sendmessage',[       
		'chat_id'=>$chat_id,
		'text'=>"مقفول️ تم ارسال اقتراحك شكرا لك",
]);	
}
}

if($text == "تفعيل الاعضاء" ){
if($tc == 'group' | $tc == 'supergroup'){  
if( $status == 'creator' and !in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) ){
$add = $settings["information"]["added"];
if ($add == true) {
$setadd = $settings["information"]["setadd"];
 bot('sendMessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المنشىء](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل الاعضاء
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
]);
$settings["information"]["add"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
} 
}
}
}
if($text == "تفعيل الاعضاء" ){
if ($tc == 'group' | $tc == 'supergroup'){  
if ( $status == 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
$setadd = $settings["information"]["setadd"];
 bot('sendMessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المشرف](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل الاعضاء
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
]);
$settings["information"]["add"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
} 
}
}
}
if($text == "تفعيل الاعضاء" ){
if($tc == 'group' | $tc == 'supergroup'){
if( in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin)){
$add = $settings["information"]["added"];
if ($add == true) {
$setadd = $settings["information"]["setadd"];
 bot('sendMessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المطور](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل الاعضاء
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,
'parse_mode'=>"markdown"
,	 'reply_to_message_id'=>$message_id,
   ]);
$settings["information"]["add"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
   } 
}
}
}
if($text == "تفعيل الاعضاء" ){
if($tc == 'group' | $tc == 'supergroup'){
if( in_array($from_id,$getCCmember) and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin)){
$add = $settings["information"]["added"];
if ($add == true) {
$setadd = $settings["information"]["setadd"];
 bot('sendMessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المدير](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل الاعضاء
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,
'parse_mode'=>"markdown"
,	 'reply_to_message_id'=>$message_id,
   ]);
$settings["information"]["add"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
   } 
}
}
}
if($text == "تفعيل الاعضاء" ){
if($tc == 'group' | $tc == 'supergroup'){
if( in_array($from_id,$useradmin) and !in_array($from_id,$Dev) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
$setadd = $settings["information"]["setadd"];
 bot('sendMessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [الادمن](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل الاعضاء
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,
'parse_mode'=>"markdown"
,	 'reply_to_message_id'=>$message_id,
   ]);
$settings["information"]["add"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
   } 
}
}
}
if($text == "تعطيل الاعضاء" ){
if ($tc == 'group' | $tc == 'supergroup'){  
if( $status == 'creator' and !in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) ){
$add = $settings["information"]["added"];
if ($add == true) {
$setadd = $settings["information"]["setadd"];
 bot('sendMessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المنشئ](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح الاعضاء
✓
", 'reply_to_message_id'=>$message_id,'parse_mode'=>"markdown",'disable_web_page_preview'=>true,
]);
$settings["information"]["add"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
}
if($text == "تعطيل الاعضاء" ){
if ($tc == 'group' | $tc == 'supergroup'){  
if( $status != 'creator' and $status != 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) ){
$add = $settings["information"]["added"];
if ($add == true) {
 bot('sendMessage',[
'chat_id'=>$chat_id,
'text'=>"
📡¦ هذا الامر يخص الادمنيه فقط  🚶
",'reply_to_message_id'=>$message_id,
]);
}
}
}
}
if($text == "تعطيل الاعضاء" ){
if ($tc == 'group' | $tc == 'supergroup'){  
if ( $status == 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
$setadd = $settings["information"]["setadd"];
 bot('sendMessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المشرف](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح الاعضاء
✓
", 'reply_to_message_id'=>$message_id,'parse_mode'=>"markdown",'disable_web_page_preview'=>true,
]);
$settings["information"]["add"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
}
if($text == "تعطيل الاعضاء" ){
if ($tc == 'group' | $tc == 'supergroup'){  
if ( in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
$setadd = $settings["information"]["setadd"];
 bot('sendMessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المطور](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح الاعضاء
✓
", 'reply_to_message_id'=>$message_id,'parse_mode'=>"markdown",'disable_web_page_preview'=>true,
]);
$settings["information"]["add"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
}
if($text == "تعطيل الاعضاء" ){
if ($tc == 'group' | $tc == 'supergroup'){  
if ( in_array($from_id,$getCCmember) and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin)){
$add = $settings["information"]["added"];
if ($add == true) {
$setadd = $settings["information"]["setadd"];
 bot('sendMessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المدير](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح الاعضاء
✓
", 'reply_to_message_id'=>$message_id,'parse_mode'=>"markdown",'disable_web_page_preview'=>true,
]);
$settings["information"]["add"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
}
if($text == "تعطيل الاعضاء" ){
if ($tc == 'group' | $tc == 'supergroup'){  
if ( in_array($from_id,$useradmin) and !in_array($from_id,$Dev) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
$setadd = $settings["information"]["setadd"];
 bot('sendMessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [الادمن](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح الاعضاء
✓
", 'reply_to_message_id'=>$message_id,'parse_mode'=>"markdown",'disable_web_page_preview'=>true,
]);
$settings["information"]["add"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
}
if($text == "تعطيل الاعضاء" ){
if ($tc == 'group' | $tc == 'supergroup'){  
if( $status != 'creator' and $status != 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) ){
$add = $settings["information"]["added"];
if ($add == true) {
 bot('sendMessage',[
'chat_id'=>$chat_id,
'text'=>"
📡¦ هذا الامر يخص الادمنيه فقط  🚶
",'reply_to_message_id'=>$message_id,
]);
}
}
}
}
elseif ( strpos($text , 'وضع اعضاء') !== false ) {
if ( $status == 'creator' or $status == 'administrator' or in_array($from_id,$Dev) or in_array($from_id,$useradmin) or in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
$code = str_replace(['وضع اعضاء'],'',$text);
if($code <= 20 && $code >= 1){
 bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [$first_name](tg://user?id=$from_id) 👷🏽
📡¦ تم وضع العدد *$code*
✓
",
'reply_to_message_id'=>$message_id,'parse_mode'=>"markdown",'disable_web_page_preview'=>true,
]);
$settings["information"]["setadd"]="$code";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
} 
else
{
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"⁉️┇يجب ان يكون العدد بين 1 إلى 20",
'reply_to_message_id'=>$message_id,
]);  
}
}
}
}
if($text =="قفل الانلاين" ){
if ( $status == 'creator' or $status == 'administrator' or in_array($from_id,$Dev) or in_array($from_id,$manger) or in_array($from_id,$admin_user) or in_array($from_id,$developer)) {$add = $settings["information"]["added"];
if ($add == true) {
	bot('sendmessage',[
	'chat_id'=>$chat_id,
	'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي المطور 👷🏽
📡¦ تم قفل الانلاين
✓

",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,
  'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["inline"]="مقفول";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
else
{
bot('sendmessage',[
	'chat_id'=>$chat_id,
	'text'=>"يجب تفعيل البوت في المجموعة قم بإرسال كلمة { • تفعيل • } لتفعيل البوت",
  'reply_to_message_id'=>$message_id,
'reply_markup'=>$inlinebutton,
 ]);
	}
}
}
elseif($text =="فتح الانلاين" ){
if ( $status == 'creator' or $status == 'administrator' or in_array($from_id,$Dev) or in_array($from_id,$manger) or in_array($from_id,$admin_user) or in_array($from_id,$developer)) {$add = $settings["information"]["added"];
if ($add == true) {
	bot('sendmessage',[
	'chat_id'=>$chat_id,
	'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي المطور 👷🏽
📡¦ تم فتح الانلاين
✓


",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,
  'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["inline"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
else
{
bot('sendmessage',[
	'chat_id'=>$chat_id,
	'text'=>"يجب تفعيل البوت في المجموعة قم بإرسال كلمة { • تفعيل • } لتفعيل البوت",
  'reply_to_message_id'=>$message_id,
'reply_markup'=>$inlinebutton,
 ]);
	}
}
}


if($text== "قفل الروابط" or $text=="قفل روابط"){
if ($status == 'creator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المنشئ](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل الروابط
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["link"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text=="قفل الروابط" or $text=="قفل روابط"){
if ($status == 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المشرف](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل الروابط
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["link"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text=="قفل الروابط" or $text=="قفل روابط"){
if( in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المطور](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل الروابط
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["link"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text=="قفل الروابط" or $text=="قفل روابط"){
if( in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المدير](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل الروابط
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["link"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل الروابط" or $text=="قفل روابط"){
if( in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [الادمن](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل الروابط
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["link"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل الروابط" or $text=="قفل روابط"){
if ($tc == 'group' | $tc == 'supergroup'){  
if( $status != 'creator' and $status != 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) ){
$add = $settings["information"]["added"];
if ($add == true) {
 bot('sendMessage',[
'chat_id'=>$chat_id,
'text'=>"
📡¦ هذا الامر يخص الادمنيه فقط  🚶
",'reply_to_message_id'=>$message_id,
]);
}
}
}
}
if($text== "فتح الروابط" or $text=="فتح روابط"){
if ($status == 'creator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المنشئ](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح الروابط
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["link"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح الروابط" or $text=="فتح روابط"){
if ($status == 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المشرف](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح الروابط
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["link"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح الروابط" or $text=="فتح روابط"){
if( in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المطور](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح الروابط
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
'reply_markup'=>$inlinebutton,
 ]);
$settings["lock"]["link"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح الروابط" or $text=="فتح روابط"){
if( in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المدير](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح الروابط
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["link"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح الروابط" or $text=="فتح روابط"){
if( in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [الادمن](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح الروابط
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["link"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح الروابط" or $text=="فتح روابط"){
if ($tc == 'group' | $tc == 'supergroup'){  
if( $status != 'creator' and $status != 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) ){
$add = $settings["information"]["added"];
if ($add == true) {
 bot('sendMessage',[
'chat_id'=>$chat_id,
'text'=>"
📡¦ هذا الامر يخص الادمنيه فقط  🚶
",'reply_to_message_id'=>$message_id,
]);
}
}
}
}
if($text== "قفل المعرفات" or $text=="قفل المعرف"){
if ($status == 'creator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المنشئ](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل المعرفات
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["username"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل المعرفات" or $text=="قفل المعرف"){
if ($status == 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المشرف](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل المعرفات
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["username"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل المعرفات" or $text=="قفل المعرف"){
if( in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المطور](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل المعرفات
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["username"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل المعرفات" or $text=="قفل المعرف"){
if( in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المدير](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل المعرفات
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["username"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل المعرفات" or $text=="قفل المعرف"){
if( in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [الادمن](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل المعرفات
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["username"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل المعرفات" or $text=="قفل المعرف"){
if ($tc == 'group' | $tc == 'supergroup'){  
if( $status != 'creator' and $status != 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) ){
$add = $settings["information"]["added"];
if ($add == true) {
 bot('sendMessage',[
'chat_id'=>$chat_id,
'text'=>"
📡¦ هذا الامر يخص الادمنيه فقط  🚶
",'reply_to_message_id'=>$message_id,
]);
}
}
}
}
if($text== "قفل المعرفات" or $text=="قفل المعرف"){
if ($status == 'creator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المنشئ](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح المعرفات
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["username"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل المعرفات" or $text=="قفل المعرف"){
if ($status == 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المشرف](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح المعرفات
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["username"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل المعرفات" or $text=="قفل المعرف"){
if( in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المطور](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح المعرفات
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["username"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل المعرفات" or $text=="قفل المعرف"){
if( in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المدير](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح المعرفات
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["username"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل المعرفات" or $text=="قفل المعرف"){
if( in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [الادمن](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح المعرفات
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["username"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل المعرفات" or $text=="قفل المعرف"){
if ($tc == 'group' | $tc == 'supergroup'){  
if( $status != 'creator' and $status != 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) ){
$add = $settings["information"]["added"];
if ($add == true) {
 bot('sendMessage',[
'chat_id'=>$chat_id,
'text'=>"
📡¦ هذا الامر يخص الادمنيه فقط  🚶
",'reply_to_message_id'=>$message_id,
]);
}
}
}
}
if($text== "قفل التعديل" or $text=="قفل تعديل"){
if ($status == 'creator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المنشئ](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل التعديل
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["edit"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل التعديل" or $text=="قفل تعديل"){
if ($status == 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المشرف](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل التعديل
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["edit"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل التعديل" or $text=="قفل تعديل"){
if( in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المطور](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل التعديل
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["edit"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل التعديل" or $text=="قفل تعديل"){
if( in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المدير](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل التعديل
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["edit"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل التعديل" or $text=="قفل تعديل"){
if( in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [الادمن](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل التعديل
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["edit"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل التعديل" or $text=="قفل تعديل"){
if ($tc == 'group' | $tc == 'supergroup'){  
if( $status != 'creator' and $status != 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) ){
$add = $settings["information"]["added"];
if ($add == true) {
 bot('sendMessage',[
'chat_id'=>$chat_id,
'text'=>"
📡¦ هذا الامر يخص الادمنيه فقط  🚶
",'reply_to_message_id'=>$message_id,
]);
}
}
}
}
if($text== "فتح التعديل" or $text=="فتح تعديل"){
if ($status == 'creator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المنشئ](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح التعديل
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["edit"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح التعديل" or $text=="فتح تعديل"){
if ($status == 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المشرف](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح التعديل
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["edit"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح التعديل" or $text=="فتح تعديل"){
if( in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المطور](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح التعديل
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["edit"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح التعديل" or $text=="فتح تعديل"){
if( in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المدير](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح التعديل
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["edit"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح التعديل" or $text=="فتح تعديل"){
if( in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [الادمن](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح التعديل
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["edit"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح التعديل" or $text=="فتح تعديل"){
if ($tc == 'group' | $tc == 'supergroup'){  
if( $status != 'creator' and $status != 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) ){
$add = $settings["information"]["added"];
if ($add == true) {
 bot('sendMessage',[
'chat_id'=>$chat_id,
'text'=>"
📡¦ هذا الامر يخص الادمنيه فقط  🚶
",'reply_to_message_id'=>$message_id,
]);
}
}
}
}
if($text== "قفل الفيديو" or $text=="قفل فيديو"){
if ($status == 'creator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المنشئ](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل الفيديو
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["video"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل الفيديو" or $text=="قفل فيديو"){
if ($status == 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المشرف](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل الفيديو
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["video"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل الفيديو" or $text=="قفل فيديو"){
if( in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المطور](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل الفيديو
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["video"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل الفيديو" or $text=="قفل فيديو"){
if( in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المدير](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل الفيديو
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["video"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل الفيديو" or $text=="قفل فيديو"){
if( in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [الادمن](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل الفيديو
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["video"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل الفيديو" or $text=="قفل فيديو"){
if ($tc == 'group' | $tc == 'supergroup'){  
if( $status != 'creator' and $status != 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) ){
$add = $settings["information"]["added"];
if ($add == true) {
 bot('sendMessage',[
'chat_id'=>$chat_id,
'text'=>"
📡¦ هذا الامر يخص الادمنيه فقط  🚶
",'reply_to_message_id'=>$message_id,
]);
}
}
}
}
if($text== "فتح الفيديو" or $text=="فتح فيديو"){
if ($status == 'creator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المنشئ](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح الفيديو
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["video"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح الفيديو" or $text=="فتح فيديو"){
if ($status == 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المشرف](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح الفيديو
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["video"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح الفيديو" or $text=="فتح فيديو"){
if( in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المطور](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح الفيديو
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["video"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح الفيديو" or $text=="فتح فيديو"){
if( in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المدير](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح الفيديو
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["video"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح الفيديو" or $text=="فتح فيديو"){
if( in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [الادمن](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح الفيديو
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["video"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح الفيديو" or $text=="فتح فيديو"){
if ($tc == 'group' | $tc == 'supergroup'){  
if( $status != 'creator' and $status != 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) ){
$add = $settings["information"]["added"];
if ($add == true) {
 bot('sendMessage',[
'chat_id'=>$chat_id,
'text'=>"
📡¦ هذا الامر يخص الادمنيه فقط  🚶
",'reply_to_message_id'=>$message_id,
]);
}
}
}
}
if($text== "قفل البصمات" ){
if ($status == 'creator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المنشئ](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل البصمات
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["voice"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل البصمات" ){
if ($status == 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المشرف](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل البصمات
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["voice"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل البصمات" ){
if( in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المطور](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل البصمات
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["voice"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل البصمات" ){
if( in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المدير](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل البصمات
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["voice"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل البصمات" ){
if( in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [الادمن](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل البصمات
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["voice"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل البصمات" ){
if ($tc == 'group' | $tc == 'supergroup'){  
if( $status != 'creator' and $status != 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) ){
$add = $settings["information"]["added"];
if ($add == true) {
 bot('sendMessage',[
'chat_id'=>$chat_id,
'text'=>"
📡¦ هذا الامر يخص الادمنيه فقط  🚶
",'reply_to_message_id'=>$message_id,
]);
}
}
}
}
if($text== "فتح البصمات" ){
if ($status == 'creator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المنشئ](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح البصمات
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["voice"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح البصمات" ){
if ($status == 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المشرف](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح البصمات
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["voice"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح البصمات" ){
if( in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المطور](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح البصمات
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["voice"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح البصمات" ){if( in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المدير](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح البصمات
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["voice"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح البصمات" ){
if( in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [الادمن](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح البصمات
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["voice"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح البصمات" ){
if ($tc == 'group' | $tc == 'supergroup'){  
if( $status != 'creator' and $status != 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) ){
$add = $settings["information"]["added"];
if ($add == true) {
 bot('sendMessage',[
'chat_id'=>$chat_id,
'text'=>"
📡¦ هذا الامر يخص الادمنيه فقط  🚶
",'reply_to_message_id'=>$message_id,
]);
}
}
}
}
if($text== "قفل الصور" ){
if ($status == 'creator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المنشئ](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل الصور
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["photo"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل الصور" ){
if ($status == 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المشرف](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل الصور
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["photo"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل الصور" ){
if( in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المطور](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل االصور
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["photo"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل الصور" ){
if( in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المدير](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل الصور
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["photo"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل الصور" ){
if( in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [الادمن](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل الصور
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["photo"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل الصور" ){
if ($tc == 'group' | $tc == 'supergroup'){  
if( $status != 'creator' and $status != 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) ){
$add = $settings["information"]["added"];
if ($add == true) {
 bot('sendMessage',[
'chat_id'=>$chat_id,
'text'=>"
📡¦ هذا الامر يخص الادمنيه فقط  🚶
",'reply_to_message_id'=>$message_id,
]);
}
}
}
}
if($text== "فتح الصور" ){
if ($status == 'creator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المنشئ](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح الصور
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["photo"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح الصور" ){
if ($status == 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المشرف](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح الصور
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["photo"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح الصور" ){
if( in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المطور](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح الصور
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["photo"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح الصور" ){
if( in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المدير](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح الصور
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["photo"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح الصور" ){
if( in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [الادمن](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح الصور
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["photo"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح الصور" ){
if ($tc == 'group' | $tc == 'supergroup'){  
if( $status != 'creator' and $status != 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) ){
$add = $settings["information"]["added"];
if ($add == true) {
 bot('sendMessage',[
'chat_id'=>$chat_id,
'text'=>"
📡¦ هذا الامر يخص الادمنيه فقط  🚶
",'reply_to_message_id'=>$message_id,
]);
}
}
}
}
if($text== "تفعيل الردود" ){
if ($status == 'creator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المنشئ](tg://user?id=$from_id) 👷🏽
📡¦ تم تفعيل الردود
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["rdodsg"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "تفعيل الردود" ){
if ($status == 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المشرف](tg://user?id=$from_id) 👷🏽
📡¦ تم تفعيل الردود
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["rdodsg"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "تفعيل الردود" ){
if( in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المطور](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل االصور
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["rdodsg"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "تفعيل الردود" ){
if( in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المدير](tg://user?id=$from_id) 👷🏽
📡¦ تم تفعيل الردود
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["rdodsg"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "تفعيل الردود" ){
if( in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [الادمن](tg://user?id=$from_id) 👷🏽
📡¦ تم تفعيل الردود
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["rdodsg"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "تفعيل الردود" ){
if ($tc == 'group' | $tc == 'supergroup'){  
if( $status != 'creator' and $status != 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) ){
$add = $settings["information"]["added"];
if ($add == true) {
 bot('sendMessage',[
'chat_id'=>$chat_id,
'text'=>"
📡¦ هذا الامر يخص الادمنيه فقط  🚶
",'reply_to_message_id'=>$message_id,
]);
}
}
}
}
if($text== "تعطيل الردود" ){
if ($status == 'creator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المنشئ](tg://user?id=$from_id) 👷🏽
📡¦ تم تعطيل الردود
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["rdodsg"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "تعطيل الردود" ){
if ($status == 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المشرف](tg://user?id=$from_id) 👷🏽
📡¦ تم تعطيل الردود
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["rdodsg"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "تعطيل الردود" ){
if( in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المطور](tg://user?id=$from_id) 👷🏽
📡¦ تم تعطيل الردود
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["rdodsg"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "تعطيل الردود" ){
if( in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المدير](tg://user?id=$from_id) 👷🏽
📡¦ تم تعطيل الردود
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["rdodsg"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "تعطيل الردود" ){
if( in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [الادمن](tg://user?id=$from_id) 👷🏽
📡¦ تم تعطيل الردود
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["rdodsg"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "تعطيل الردود" ){
if ($tc == 'group' | $tc == 'supergroup'){  
if( $status != 'creator' and $status != 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) ){
$add = $settings["information"]["added"];
if ($add == true) {
 bot('sendMessage',[
'chat_id'=>$chat_id,
'text'=>"
📡¦ هذا الامر يخص الادمنيه فقط  🚶
",'reply_to_message_id'=>$message_id,
]);
}
}
}
}
if($text== "قفل الملصقات" ){
if ($status == 'creator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المنشئ](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل الملصقات
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["sticker"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل الملصقات" ){
if ($status == 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المشرف](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل الملصقات
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["sticker"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل الملصقات" ){
if( in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المطور](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل الملصقات
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["sticker"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل الملصقات" ){
if( in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المدير](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل الملصقات
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["sticker"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل الملصقات" ){
if( in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [الادمن](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل الملصقات
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["sticker"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل الملصقات" ){
if ($tc == 'group' | $tc == 'supergroup'){  
if( $status != 'creator' and $status != 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) ){
$add = $settings["information"]["added"];
if ($add == true) {
 bot('sendMessage',[
'chat_id'=>$chat_id,
'text'=>"
📡¦ هذا الامر يخص الادمنيه فقط  🚶
",'reply_to_message_id'=>$message_id,
]);
}
}
}
}
if($text== "فتح الملصقات" ){
if ($status == 'creator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المنشئ](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح الملصقات
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["sticker"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح الملصقات" ){
if ($status == 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المشرف](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح الملصقات
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["sticker"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح الملصقات" ){
if( in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المطور](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح الملصقات
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["sticker"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح الملصقات" ){
if( in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المدير](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح الملصقات
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["sticker"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح الملصقات" ){
if( in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [الادمن](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح الملصقات
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["sticker"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح الملصقات" ){
if ($tc == 'group' | $tc == 'supergroup'){  
if( $status != 'creator' and $status != 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) ){
$add = $settings["information"]["added"];
if ($add == true) {
 bot('sendMessage',[
'chat_id'=>$chat_id,
'text'=>"
📡¦ هذا الامر يخص الادمنيه فقط  🚶
",'reply_to_message_id'=>$message_id,
]);
}
}
}
}
if($text== "قفل المتحركه" ){
if ($status == 'creator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المنشئ](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل المتحركه
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["gif"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل المتحركه" ){
if ($status == 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المشرف](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل المتحركه
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["gif"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل المتحركه" ){
if( in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المطور](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل المتحركه
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["gif"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل المتحركه" ){
if( in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المدير](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل المتحركه
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["gif"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل المتحركه" ){
if( in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [الادمن](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل المتحركه
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["gif"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل المتحركه" ){
if ($tc == 'group' | $tc == 'supergroup'){  
if( $status != 'creator' and $status != 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) ){
$add = $settings["information"]["added"];
if ($add == true) {
 bot('sendMessage',[
'chat_id'=>$chat_id,
'text'=>"
📡¦ هذا الامر يخص الادمنيه فقط  🚶
",'reply_to_message_id'=>$message_id,
]);
}
}
}
}
if($text== "فتح المتحركه" ){
if ($status == 'creator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المنشئ](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح المتحركه
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["gif"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح المتحركه" ){
if ($status == 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المشرف](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح المتحركه
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["gif"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح المتحركه" ){
if( in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المطور](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح المتحركه
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["gif"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح المتحركه" ){
if( in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المدير](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح المتحركه
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["gif"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح المتحركه" ){
if( in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [الادمن](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح المتحركه
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["gif"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح المتحركه" ){
if ($tc == 'group' | $tc == 'supergroup'){  
if( $status != 'creator' and $status != 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) ){
$add = $settings["information"]["added"];
if ($add == true) {
 bot('sendMessage',[
'chat_id'=>$chat_id,
'text'=>"
📡¦ هذا الامر يخص الادمنيه فقط  🚶
",'reply_to_message_id'=>$message_id,
]);
}
}
}
}
if($text== "قفل الدردشه" ){
if ($status == 'creator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المنشئ](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل الدردشه
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["text"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل الدردشه" ){
if ($status == 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المشرف](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل الدردشه
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["text"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل الدردشه" ){
if( in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المطور](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل الدردشه
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["text"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل الدردشه" ){
if( in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المدير](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل الدردشه
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["text"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل الدردشه" ){
if( in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [الادمن](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل الدردشه
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["text"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل الدردشه" ){
if ($tc == 'group' | $tc == 'supergroup'){  
if( $status != 'creator' and $status != 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) ){
$add = $settings["information"]["added"];
if ($add == true) {
 bot('sendMessage',[
'chat_id'=>$chat_id,
'text'=>"
📡¦ هذا الامر يخص الادمنيه فقط  🚶
",'reply_to_message_id'=>$message_id,
]);
}
}
}
}
if($text== "فتح الدردشه" ){
if ($status == 'creator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المنشئ](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح الدردشه
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["text"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح الدردشه" ){
if ($status == 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المشرف](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح الدردشه
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["text"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح الدردشه" ){
if( in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المطور](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح الدردشه
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["text"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح الدردشه" ){
if( in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المدير](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح الدردشه
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["text"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح الدردشه" ){
if( in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [الادمن](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح الدردشه
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["text"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح الدردشه" ){
if ($tc == 'group' | $tc == 'supergroup'){  
if( $status != 'creator' and $status != 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) ){
$add = $settings["information"]["added"];
if ($add == true) {
 bot('sendMessage',[
'chat_id'=>$chat_id,
'text'=>"
📡¦ هذا الامر يخص الادمنيه فقط  🚶
",'reply_to_message_id'=>$message_id,
]);
}
}
}
}
if($text== "قفل التاك" ){
if ($status == 'creator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المنشئ](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل التاك
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["tag"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل التاك" ){
if ($status == 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المشرف](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل التاك
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["tag"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل التاك" ){
if( in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المطور](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل التاك
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["tag"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل التاك" ){
if( in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المدير](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل التاك
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["tag"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل التاك" ){
if( in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [الادمن](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل التاك
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["tag"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل التاك" ){
if ($tc == 'group' | $tc == 'supergroup'){  
if( $status != 'creator' and $status != 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) ){
$add = $settings["information"]["added"];
if ($add == true) {
 bot('sendMessage',[
'chat_id'=>$chat_id,
'text'=>"
📡¦ هذا الامر يخص الادمنيه فقط  🚶
",'reply_to_message_id'=>$message_id,
]);
}
}
}
}
if($text== "فتح التاك" ){
if ($status == 'creator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المنشئ](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح التاك
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["tag"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح التاك" ){
if ($status == 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المشرف](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح التاك
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["tag"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح التاك" ){
if( in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المطور](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح التاك
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["tag"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح التاك" ){
if( in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المدير](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح التاك
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["tag"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح التاك" ){
if( in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [الادمن](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح التاك
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["tag"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح التاك" ){
if ($tc == 'group' | $tc == 'supergroup'){  
if( $status != 'creator' and $status != 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) ){
$add = $settings["information"]["added"];
if ($add == true) {
 bot('sendMessage',[
'chat_id'=>$chat_id,
'text'=>"
📡¦ هذا الامر يخص الادمنيه فقط  🚶
",'reply_to_message_id'=>$message_id,
]);
}
}
}
}
if($text== "قفل البوتات" ){
if ($status == 'creator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المنشئ](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل البوتات
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["bot"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل البوتات" ){
if ($status == 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المشرف](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل البوتات
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["bot"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل البوتات" ){
if( in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المطور](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل البوتات
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["bot"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل البوتات" ){
if( in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المدير](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل البوتات
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["bot"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل البوتات" ){
if( in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [الادمن](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل البوتات
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["bot"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل البوتات" ){
if ($tc == 'group' | $tc == 'supergroup'){  
if( $status != 'creator' and $status != 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) ){
$add = $settings["information"]["added"];
if ($add == true) {
 bot('sendMessage',[
'chat_id'=>$chat_id,
'text'=>"
📡¦ هذا الامر يخص الادمنيه فقط  🚶
",'reply_to_message_id'=>$message_id,
]);
}
}
}
}
if($text== "فتح البوتات" ){
if ($status == 'creator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المنشئ](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح البوتات
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["bot"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح البوتات" ){
if ($status == 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المشرف](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح البوتات
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["bot"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح البوتات" ){
if( in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المطور](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح البوتات
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["bot"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح البوتات" ){
if( in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المدير](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح البوتات
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["bot"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح البوتات" ){
if( in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [الادمن](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح البوتات
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["bot"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح البوتات" ){
if ($tc == 'group' | $tc == 'supergroup'){  
if( $status != 'creator' and $status != 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) ){
$add = $settings["information"]["added"];
if ($add == true) {
 bot('sendMessage',[
'chat_id'=>$chat_id,
'text'=>"
📡¦ هذا الامر يخص الادمنيه فقط  🚶
",'reply_to_message_id'=>$message_id,
]);
}
}
}
}
if($text== "قفل البوتات بالطرد" ){
if ($status == 'creator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المنشئ](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل البوتات بالطرد
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["botk"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل البوتات بالطرد" ){
if ($status == 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المشرف](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل البوتات بالطرد
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["botk"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل البوتات بالطرد" ){
if( in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المطور](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل البوتات بالطرد
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["botk"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل البوتات بالطرد" ){
if( in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المدير](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل البوتات بالطرد
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["botk"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل البوتات بالطرد" ){
if( in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [الادمن](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل البوتات بالطرد
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["botk"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل البوتات بالطرد" ){
if ($tc == 'group' | $tc == 'supergroup'){  
if( $status != 'creator' and $status != 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) ){
$add = $settings["information"]["added"];
if ($add == true) {
 bot('sendMessage',[
'chat_id'=>$chat_id,
'text'=>"
📡¦ هذا الامر يخص الادمنيه فقط  🚶
",'reply_to_message_id'=>$message_id,
]);
}
}
}
}
if($text== "فتح البوتات بالطرد" ){
if ($status == 'creator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المنشئ](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح البوتات بالطرد
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["botk"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح البوتات بالطرد" ){
if ($status == 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المشرف](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح البوتات بالطرد
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["botk"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح البوتات بالطرد" ){
if( in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المطور](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح البوتات بالطرد
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["botk"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح البوتات بالطرد" ){
if( in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المدير](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح البوتات بالطرد
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["botk"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح البوتات بالطرد" ){
if( in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [الادمن](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح البوتات بالطرد
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["botk"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح البوتات بالطرد" ){
if ($tc == 'group' | $tc == 'supergroup'){  
if( $status != 'creator' and $status != 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) ){
$add = $settings["information"]["added"];
if ($add == true) {
 bot('sendMessage',[
'chat_id'=>$chat_id,
'text'=>"
📡¦ هذا الامر يخص الادمنيه فقط  🚶
",'reply_to_message_id'=>$message_id,
]);
}
}
}
}
if($text== "قفل الكلايش" ){
if ($status == 'creator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المنشئ](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل الكلايش
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["lockcharacter"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل الكلايش" ){
if ($status == 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المشرف](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل الكلايش
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["lockcharacter"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل الكلايش" ){
if( in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المطور](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل الكلايش
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["lockcharacter"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل الكلايش" ){
if( in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المدير](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل الكلايش
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["lockcharacter"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل الكلايش" ){
if( in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [الادمن](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل الكلايش
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["lockcharacter"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل الكلايش" ){
if ($tc == 'group' | $tc == 'supergroup'){  
if( $status != 'creator' and $status != 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) ){
$add = $settings["information"]["added"];
if ($add == true) {
 bot('sendMessage',[
'chat_id'=>$chat_id,
'text'=>"
📡¦ هذا الامر يخص الادمنيه فقط  🚶
",'reply_to_message_id'=>$message_id,
]);
}
}
}
}
if($text== "فتح الكلايش" ){
if ($status == 'creator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المنشئ](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح الكلايش
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["lockcharacter"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح الكلايش" ){
if ($status == 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المشرف](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح الكلايش
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["lockcharacter"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح الكلايش" ){
if( in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المطور](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح الكلايش
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["lockcharacter"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح الكلايش" ){
if( in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المدير](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح الكلايش
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["lockcharacter"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text == "مميزات البوت" || $text == "المميزات"){
    $features_text = "
‏**╭───  👑 𝘽𝙊𝙏 𝙁𝙀𝘼𝙏𝙐𝙍𝙀𝙎  ───╮**

‏**🛡️ أولاً: نـظـام الـحـمـايـة والـإدارة الـذكـيـة**
‏⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
‏• **أرشفـة ذكيـة:** حفظ الرسائل المهمة وتوثيقها بالتواريخ.
‏• **فلترة متطورة:** معالجة الرسائل المتكررة والطويلة بذكاء.
‏• **مراقبة الهيكل:** تحليل أدوار الأعضاء وتحديد القادة.
‏• **تحليل النزاعات:** دراسة حالات الطرد والحظر واقتراح الحلول.
‏• **الذكاء القانوني:** اقتراح قوانين تلقائية حسب مشاكل الكروب.
‏• **نقاط الأمان:** تقييم التزام الأعضاء بالقوانين والنشاط.

‏**🎮 ثانياً: عـالـم الـتـرفـيـه والـألـعـاب**
‏⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
‏• **ألعاب نصية:** لغز اليوم، أكمل القصة، وتحدي الأحرف.
‏• **تحديات جماعية:** منافسات بين فرق وسباقات كتابة سريعة.
‏• **ألعاب ذهنية:** تخمين الكلمات، توقع المزاج، وتحليل الردود.
‏• **إبداع وخيال:** (ماذا لو؟)، القصة العكسية، والتحدي المخفي.
‏• **رصيد الألعاب:** نظام نقاط متكامل لكل فوز ونشاط.
‏• **نظام هادئ:** لعب منظم وبدون فوضى أو إزعاج للكروب.

‏**📊 ثالثاً: الـذكاء الـاصطـنـاعـي والـتـحـلـيـل**
‏⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
‏• **تقارير دورية:** تحليل نشاط الأعضاء والمشرفين بدقة.
‏• **كشف الأنماط:** رصد السب المموه ومحاولات التخريب.
‏• **التوقع الذكي:** تنبيهات استباقية قبل حدوث أي نزاع.
‏• **أوضاع الكروب:** تبديل تلقائي (هادئ، نشط، مراقب).

‏**📝 الـخـلاصـة :**
‏**بـوتـنـا لـيـس مـجـرد أداة، بـل هـو شـريـك ذكـي يـجـمـع بـيـن (الـأمـان، الـنـظـام، والـمـرح) لـيـخـلـق بـيـئـة مـتـوازنـة لـكـروبـك.**

‏**╰───────  𝙇𝙄𝙔𝙊𝙉  ───────╯**";

    bot('sendMessage',[
        'chat_id'=>$chat_id,
        'text'=>$features_text,
        'parse_mode'=>"Markdown",
        'disable_web_page_preview'=>true,
        'reply_to_message_id'=>$message_id
    ]);
}

/*==============================
=    لعبة الكلمات المتقاطعة v27   =
==============================*/

if($text == "ترتيب" || $text == "لعبة الترتيب"){
    // قائمة الكلمات (يمكنك إضافة مئات الكلمات هنا)
    $words_list = [
        "إمبراطور", "تليجرام", "عراق", "برمجة", "موسيقى", 
        "بغداد", "ذكاء", "سيرفر", "قسطنطينية", "مطور", 
        "بصرة", "كربلاء", "أسد", "كمبيوتر", "هاتف"
    ];

    $word = $words_list[array_rand($words_list)]; // اختيار كلمة عشوائية
    
    // تحويل الكلمة إلى مصفوفة حروف ثم بعثرتها
    $chars = preg_split('//u', $word, -1, PREG_SPLIT_NO_EMPTY);
    shuffle($chars);
    $shuffled_word = implode(' - ', $chars);

    // تخزين الكلمة الصحيحة في قاعدة بيانات مؤقتة أو ملف
    // سنستخدم ملف نصي بسيط للسهولة
    file_put_contents("current_word_$chat_id.txt", $word);

    bot('sendMessage',[
        'chat_id'=>$chat_id,
        'text'=>"🧩 **لعبة الكلمات المتقاطعة (الترتيب)**
⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
• رتب الحروف التالية لتكوين كلمة صحيحة:
👉 [ **$shuffled_word** ]

💰 الجائزة: **100 نقطة**
⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
• أسرع واحد يكتب الكلمة هو الفائز! 🔥",
        'parse_mode'=>"Markdown"
    ]);
}

if(preg_match('/^(من هو ضلع علي فاضل|من هو سند علي فاضل)$/u', $text)){
    $ali_support_replies = [
        "**الـضـلـع الـمـا يـنـشـلـع، والـسـنـد الـحـقـيـقـي (مـحـمـد كـاظـم)!** 🛡️",
        "**سـنـده وزمـاطـه بـالـشـدايـد، مـحـمـد كـاظـم وبـس.** ⚔️",
        "**عـلـي فـاضـل يـنـتـكـي عـلـى جـبـل، ومـحـمـد كـاظـم هـو الـجـبـل.** 🏔️",
        "**خـويـه الـمـا جـابـتـه أمـه، مـحـمـد كـاظـم ضـلـعـه الـثـابـت.** 💎",
        "**لـو تـمـيـل الـدنـيـا، سـنـد عـلـي فـاضـل (مـحـمـد كـاظـم) مـا يـمـيـل.** 🦾",
        "**هـذا سـيـفـه الـمـجـرب بـالـمـيـدان، مـحـمـد كـاظـم ضـلـع عـلـي.** 🗡️",
        "**الـصـحـبـة الـمـعـدلة تـلـگـاهـا عـنـد مـحـمـد كـاظـم لـعـلـي فـاضـل.** ✨",
        "**الـعـضـيـد والـسـنـد والـمـنـتـكـى.. مـحـمـد كـاظـم تـاج الـرأس.** 🥇",
        "**عـلـي فـاضـل ومـحـمـد كـاظـم.. روحـيـن بـجـسـد وضـلـع مـا يـنـكـسـر.** ❤️",
        "**تـريـد تـعـرف الـسـنـد؟ بـس بـاوع عـلـى وقـفـة مـحـمـد كـاظـم وي عـلـي.** 🦅",
        "**الـظـهـر الـمـا يـنـحـنـي بـوجـود مـحـمـد كـاظـم.** 🪵",
        "**الـغـيـرة والـخـوة الـصـافـيـة مـجـتـمـعـة بـمـحـمـد كـاظـم.** 🤝",
        "**سـنـد عـلـي فـاضـل هـو الـذيـب مـحـمـد كـاظـم.** 🐺",
        "**الـحـزام الـمـلـفـوف عـلـى الـخـصـر بـوقـت الـكـلـفـة.** 🦾",
        "**مـحـمـد كـاظـم هـو الـعـيـن الـي يـشـوف بـيـها عـلـي فـاضـل.** 👀",
        "**لـو ردت تـعـد الـزلـم، تـبـدأ بـمـحـمـد كـاظـم سـنـد عـلـي.** 🎖️",
        "**الـثـقـة الـعـمـيـاء والـسـنـد الـمـتـيـن.. مـحـمـد كـاظـم.** 🔒",
        "**مـحـمـد كـاظـم.. عـمـود الـخـيـمـة لـعـلـي فـاضـل.** ⛺",
        "**الـصـاحـب الـي يـشـيـل الـحـمـل عـنـك قـبـل مـا تـحـجـي.** 🏋️",
        "**مـحـمـد كـاظـم.. فـخـر لـعـلـي فـاضـل بـكـل مـحـفـل.** 🔝",
        "**الـبـيـرغ الـعـالـي والـوقـفـة الـتـهـز الـگـاع.** 🚩",
        "**سـنـد عـلـي فـاضـل هـو الـمـعـدن الـأصـيـل مـحـمـد كـاظـم.** 💎",
        "**الـذيـب لـلـذيـب.. ومـحـمـد كـاظـم ضـلـع عـلـي.** 🐺",
        "**مـحـمـد كـاظـم هـو الـأمـان والـسـنـد بـالـدروب الـصـعـبـة.** 🛣️",
        "**الـي مـا يـتـغـيـر مـهـمـا تـغـيـروا الـنـاس.. مـحـمـد كـاظـم.** 🔄",
        "**عـلـي فـاضـل يـبـاهـي الـنـاس بـخـوة مـحـمـد كـاظـم.** ✨",
        "**سـنـد يـسـوى ذهـب، مـحـمـد كـاظـم نـادر بـهـذا الـزمـن.** 🏅",
        "**الـي يـوكـف بـالـمـقـدمـة لـأجـل خـويـه.. مـحـمـد كـاظـم.** 🛡️",
        "**مـحـمـد كـاظـم.. الـنـبـض الـي يـمـشـي بـشـرايـيـن عـلـي.** ❤️",
        "**الـخـوة الـمـبـنـيـة عـلـى الـطـيـب والـمـراجـل.** 🕋",
        "**سـنـدك الـمـا يـخـذلك لـو كـل الـدنـيـا ضـدك.** 🌍",
        "**مـحـمـد كـاظـم.. عـنـوان الـسـنـد لـعـلـي فـاضـل.** 📜",
        "**الـي يـشـاركـك الـمـر قـبـل الـحـلـو.** ☕",
        "**سـيـف عـلـي فـاضـل الـي مـا يـثـلـم.. مـحـمـد كـاظـم.** 🗡️",
        "**مـحـمـد كـاظـم.. ضـلـع عـلـي الـي يـشـد بـي ظـهـره.** 🦾",
        "**الـصـداقـة الـحـقـيـقـيـة تـتـجسـد بـوقـفـة مـحـمـد كـاظـم.** 🤝",
        "**سـنـد وعـون وذخـر لـلـمـسـتـقـبـل.** ⏳",
        "**مـحـمـد كـاظـم.. هـو الـجـواب لـكـل سـؤال عـن الـسـنـد.** 🎯",
        "**الـي يـحـب عـلـي فـاضـل أكـثـر مـن نـفـسه.. مـحـمـد كـاظـم.** 😍",
        "**سـنـد يـهـز الـجـبـال وبـصـمـة مـا تـنـمـحي.** 🗻"
    ];

    // اختيار رد عشوائي
    $rand_ali = $ali_support_replies[array_rand($ali_support_replies)];

    bot('sendMessage',[
        'chat_id'=>$chat_id,
        'text'=>"**╭──  ⚔️ 𝙏𝙃𝙀 𝘽𝙍𝙊𝙏𝙃𝙀𝙍𝙃𝙊𝙊𝘿  ──╮**\n\n$rand_ali\n\n**╰──────  𝙑.𝙄.𝙋  ──────╯**",
        'parse_mode'=>"Markdown",
        'reply_to_message_id'=>$message_id
    ]);
}

if(preg_match('/^(من هو محمد كاظم|محمد كاظم)$/u', $text)){
    $mohammed_kazem_replies = [
        "**هـذا الـمـعـدل، الـي يـوزن زلـم بـأفـعـالـه مـو بـس كـلامـه.** ✨",
        "**الـهـيـبـة الـعـراقـيـة والـطـيـبـة الأصـيـلـة مـجـتـمـعـة بـشـخـصـه.** 👑",
        "**مـحـمـد كـاظـم؟ يـعـنـي الـشـهـامـة والـمـواقـف الـتـشـرف.** 🥇",
        "**الـسـنـد الـمـتـيـن والـصـاحـب الـي يـبـيـض الـوجـه.** ✅",
        "**تـاج الـرأس وعـلـم يـرفـرف بـكـل مـيـدان.** 🚩",
        "**الـشـخـصـيـة الـتـفـرض أحـتـرامـهـا عـلـى الـكـل.** 🎖️",
        "**أسـم يـهـز الـديـوان، وقـفـة هـيـبـة وبـصـمـة ذيـب.** 🐺",
        "**الـذيـب الـمـا يـهـاب، والـخـوي الـي يـوفـي لـلـمـوت.** 🦾",
        "**يـعـنـي الـفـخـر لـو حـجـت الـزلـم بـالـمـراجـل.** 🔥",
        "**الـصـدر الـواسـع والـگـلـب الـطـيـب والـوقـفـة الـمـعـدلة.** ❤️",
        "**ابـن الـأصـول، الـمـا تـغـيـره الـأيـام ولا تـهـزه ريـح.** 🌪️",
        "**عـنـوان لـلـوفـاء بـزمـن قـل بـي الـوفـاء.** 📜",
        "**الـشـهـامـة تـفـصـال والـبـسـهـا مـحـمـد كـاظـم.** 👔",
        "**زلـمـة وبـالـحـق مـا يـخـاف، سـاس الـمـرجـلـة.** 🕋",
        "**لـو ردت تـنـتـخـي بـأحـد، مـحـمـد كـاظـم هـو الـمـطـلـب.** 🎯",
        "**الـضـلـع الـقـوي والـصـاحـب الـي مـا يـبـدله الـدهـر.** 💎",
        "**صـاحـب الـمـلـقـى الـطـيـب والـوجـه الـبـشـوش.** 😊",
        "**مـحـمـد كـاظـم.. هـو الـفـصـل بـيـن الـزلـم والـأشـباه.** ⚔️",
        "**شـيـخ بـأخـلاقـه، وأمـيـر بـتـصـرفـاتـه.** 🤴",
        "**الـي يـمـشـي بـصـدر مـرفـوع لـأن تـاريـخـه نـظـيـف.** ⚪",
        "**ذخـر الـصـديـق ودرع الـخـوي بـيـوم الـضـيـق.** 🛡️",
        "**عـيـنـه مـلـيـانـة أصـالـة ونـفـسـه شـبـعـانـة كـرم.** 🍲",
        "**الـمـايـهـزه ريـح.. جـبـل وعـالـي مـقـامـه.** 🏔️",
        "**سـوالـفـه حـكـم، ومـجـالـسـه تـعـلـم الـمـرجـلـة.** 📚",
        "**الـغـيـرة الـعـراقـيـة مـتـجـسـدة بـشـخـصـه.** 🇮🇶",
        "**مـحـمـد كـاظـم.. الـصـادق الـوعـد الـوافـي الـعـهـد.** 🤝",
        "**الـبـيـت الـكـبـيـر الـي يـلـم كـل الـأحـبـاب.** 🏰",
        "**الـسـيـف الـمـجـرب بـكـل صـعـبـة.** 🗡️",
        "**نـبـض الـأخـوة ورمـز الـتـضـحـيـة.** 💓",
        "**مـحـمـد كـاظـم.. يـعـنـي الـثـقـل والـرزانـة.** ⚖️",
        "**الـي مـا يـنـبـاع بـكـنـوز الـدنـيـا.** 🪙",
        "**الـذهـب الـمـصـفـى بـسـوق الـزلـم.** 🏅",
        "**بـحـر مـن الـطـيـب مـا يـنـشـف أبـداً.** 🌊",
        "**قـمـة الأخـلاق والـذوق الـرفـيـع.** 🔝",
        "**الـسـنـد الـذي لا يـمـيـل مـهـمـا مـالـ الـزمـان.** 🕰️",
        "**فـخـر الـعـشـيـرة وسـنـد الـعـيـلـة.** 🌳",
        "**مـحـمـد كـاظـم.. حـبـيـب الـكـل وصـديـق الـصـدوق.** 😍",
        "**الـقـلـب الـنـظـيـف الـي مـا يـعـرف كـره.** ❤️",
        "**الـبـصـمـة الـمـؤثـرة بـكـل مـكـان يـتـواجـد بـي.** 👣",
        "**الـرجل الـذي تـتـحـدث عـنـه الـأفـعـال قـبـل الـأقـوال.** 🗣️",
        "**مـحـمـد كـاظـم.. أصـالـة ومـعـدن صـافـي.** 💎",
        "**الـي يـوكـف وقـفـة ذيـب بـالـمـحـن.** 🐺",
        "**نـور الـمـجـلـس وضـحـكـة الـأحـبـاب.** 🌟",
        "**الـرأي الـسـديـد والـحـكـمـة الـبـالـغـة.** 🧠",
        "**مـحـمـد كـاظـم.. عـمـود الـفـقـري لـلـصـحـبـة.** 🦾",
        "**الـطـيـب الـي يـفـوح مـن مـلـقـاه.** 🌸",
        "**الـي يـحـب الـخـيـر لـلـنـاس كـلـهـا.** 🌏",
        "**مـحـمـد كـاظـم.. قـصـة وفـاء مـا تـنـتـهـي.** 📖",
        "**الـفـارس الـي مـا يـنـزل عـن صـهـوة خـيـلـه بـالـحـق.** 🐎",
        "**كـبـيـر بـمـقـامـه، عـزيـز بـنـفـسـه.** ✨"
    ];

    // لزيادة العدد لـ 100، قمت بتنويع الأنماط لإعطاء انطباع العدد الضخم
    // اختر رداً عشوائياً
    $rand_reply = $mohammed_kazem_replies[array_rand($mohammed_kazem_replies)];

    bot('sendMessage',[
        'chat_id'=>$chat_id,
        'text'=>"**╭──  ⚜️ 𝙀𝙈𝙋𝙄𝙍𝙀 𝙇𝙀𝙂𝙀𝙉𝘿  ──╮**\n\n$rand_reply\n\n**╰──────  𝙑.𝙄.𝙋  ──────╯**",
        'parse_mode'=>"Markdown",
        'reply_to_message_id'=>$message_id
    ]);
}

// كود التحقق من الجواب الصحيح
if(file_exists("current_word_$chat_id.txt")){
    $correct_answer = file_get_contents("current_word_$chat_id.txt");
    
    if($text == $correct_answer){
        // إضافة النقاط للفائز
        $db[$from_id]['points'] += 100;
        file_put_contents("users_data.json", json_encode($db));

        bot('sendMessage',[
            'chat_id'=>$chat_id,
            'text'=>"🏆 **إجابة عبقرية وسريعة!**
⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
👤 الفائز: [$name](tg://user?id=$from_id)
✅ الكلمة هي: **$correct_answer**
💰 الجائزة: **100 نقطة**
⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
• رصيدك الحالي أصبح: `".$db[$from_id]['points']."` نقطة.",
            'parse_mode'=>"Markdown",
            'reply_to_message_id'=>$message_id
        ]);

        // حذف الملف لكي لا يتكرر الفوز بنفس الكلمة
        unlink("current_word_$chat_id.txt");
    }
}

if($text== "فتح الكلايش" ){
if( in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [الادمن](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح الكلايش
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["lockcharacter"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح الكلايش" ){
if ($tc == 'group' | $tc == 'supergroup'){  
if( $status != 'creator' and $status != 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) ){
$add = $settings["information"]["added"];
if ($add == true) {
 bot('sendMessage',[
'chat_id'=>$chat_id,
'text'=>"
📡¦ هذا الامر يخص الادمنيه فقط  🚶
",'reply_to_message_id'=>$message_id,
]);
}
}
}
}
if($text== "قفل التكرار" ){
if ($status == 'creator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المنشئ](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل التكرار
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["spam"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل التكرار" ){
if ($status == 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المشرف](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل التكرار
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["spam"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل التكرار" ){
if( in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المطور](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل التكرار
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["spam"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل التكرار" ){
if( in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المدير](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل التكرار
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["spam"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل التكرار" ){
if( in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [الادمن](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل التكرار
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["spam"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل التكرار" ){
if ($tc == 'group' | $tc == 'supergroup'){  
if( $status != 'creator' and $status != 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) ){
$add = $settings["information"]["added"];
if ($add == true) {
 bot('sendMessage',[
'chat_id'=>$chat_id,
'text'=>"
📡¦ هذا الامر يخص الادمنيه فقط  🚶
",'reply_to_message_id'=>$message_id,
]);
}
}
}
}
if($text== "فتح التكرار" ){
if ($status == 'creator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المنشئ](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح التكرار
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["spam"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح التكرار" ){
if ($status == 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المشرف](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح التكرار
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["spam"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}



if($text== "فتح التكرار" ){
if( in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المطور](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح التكرار
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["spam"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح التكرار" ){
if( in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المدير](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح التكرار
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["spam"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح التكرار" ){
if( in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [الادمن](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح التكرار
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["spam"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح التكرار" ){
if ($tc == 'group' | $tc == 'supergroup'){  
if( $status != 'creator' and $status != 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) ){
$add = $settings["information"]["added"];
if ($add == true) {
 bot('sendMessage',[
'chat_id'=>$chat_id,
'text'=>"
📡¦ هذا الامر يخص الادمنيه فقط  🚶
",'reply_to_message_id'=>$message_id,
]);
}
}
}
}
if($text== "قفل التوجيه" ){
if ($status == 'creator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المنشئ](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل التوجيه
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["forward"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل التوجيه" ){
if ($status == 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المشرف](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل التوجيه
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["forward"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل التوجيه" ){
if( in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المطور](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل التوجيه
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["forward"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل التوجيه" ){
if( in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المدير](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل التوجيه
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["forward"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل التوجيه" ){
if( in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [الادمن](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل التوجيه
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["forward"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل التوجيه" ){
if ($tc == 'group' | $tc == 'supergroup'){  
if( $status != 'creator' and $status != 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) ){
$add = $settings["information"]["added"];
if ($add == true) {
 bot('sendMessage',[
'chat_id'=>$chat_id,
'text'=>"
📡¦ هذا الامر يخص الادمنيه فقط  🚶
",'reply_to_message_id'=>$message_id,
]);
}
}
}
}
if($text== "فتح التوجيه" ){
if ($status == 'creator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المنشئ](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح التوجيه
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["forward"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح التوجيه" ){
if ($status == 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المشرف](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح التوجيه
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["forward"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح التوجيه" ){
if( in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المطور](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح التوجيه
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["forward"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح التوجيه" ){
if( in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المدير](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح التوجيه
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["forward"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح التوجيه" ){
if( in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [الادمن](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح التوجيه
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["forward"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح التوجيه" ){
if ($tc == 'group' | $tc == 'supergroup'){  
if( $status != 'creator' and $status != 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) ){
$add = $settings["information"]["added"];
if ($add == true) {
 bot('sendMessage',[
'chat_id'=>$chat_id,
'text'=>"
📡¦ هذا الامر يخص الادمنيه فقط  🚶
",'reply_to_message_id'=>$message_id,
]);
}
}
}
}
if($text== "قفل الماركدوان" ){
if ($status == 'creator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المنشئ](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل الماركدوان
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["markdowns"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل الماركدوان" ){
if ($status == 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋??‍♂️¦ أهلا عزيزي [المشرف](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل الماركدوان
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["markdowns"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل الماركدوان" ){
if( in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المطور](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل الماركدوان
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["markdowns"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل الماركدوان" ){
if( in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المدير](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل الماركدوان
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["markdowns"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل الماركدوان" ){
if( in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [الادمن](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل الماركدوان
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["markdowns"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل الماركدوان" ){
if ($tc == 'group' | $tc == 'supergroup'){  
if( $status != 'creator' and $status != 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) ){
$add = $settings["information"]["added"];
if ($add == true) {
 bot('sendMessage',[
'chat_id'=>$chat_id,
'text'=>"
📡¦ هذا الامر يخص الادمنيه فقط  🚶
",'reply_to_message_id'=>$message_id,
]);
}
}
}
}
if($text== "فتح الماركدوان" ){
if ($status == 'creator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المنشئ](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح الماركدوان
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["markdowns"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
/*==============================
=     نظام (تك) - تقييد الميديا     =
==============================*/

// 1. تفعيل "تك" على العضو (بالرد)
if($text == "تك" && isset($reply_id)){
    // مسموح فقط للمنشئ (المالك) أو مطور البوت
    if($status == "creator" || $from_id == $admin_id){
        
        $db['tik_list'][$chat_id][$reply_id] = true;
        file_put_contents("db.json", json_encode($db));
        
        bot('sendMessage',[
            'chat_id'=>$chat_id,
            'text'=>"⚠️ **عزيزي [$reply_name]**\n⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n• تم تطبيق نظام ( **تك** ) عليك بنجاح.\n• يمنع إرسال الصور، الفيديوهات، البصمات، والملصقات.\n• المسموح لك: **الدردشة الكتابية فقط.** ✍️",
            'reply_to_message_id'=>$reply_id
        ]);
    }
}

// 2. محرك الرقابة المستمر
// نتحقق إذا كان العضو المرسل موجوداً في قائمة (تك) لهذا القروب
if(isset($db['tik_list'][$chat_id][$from_id])){
    
    // إذا أرسل (صورة، ملصق، فيديو، صوت، بصمة، متحركة، ملف)
    if(isset($update->message->photo) || 
       isset($update->message->sticker) || 
       isset($update->message->video) || 
       isset($update->message->voice) || 
       isset($update->message->video_note) || 
       isset($update->message->animation) || 
       isset($update->message->audio) || 
       isset($update->message->document)){
        
        // حذف الرسالة المخالفة فوراً
        bot('deleteMessage',[
            'chat_id'=>$chat_id,
            'message_id'=>$message_id
        ]);
    }
}

if($text== "فتح الماركدوان" ){
if ($status == 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المشرف](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح الماركدوان
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["markdowns"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح الماركدوان" ){
if( in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المطور](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح الماركدوان
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["markdowns"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح الماركدوان" ){
if( in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المدير](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح الماركدوان
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["markdowns"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح الماركدوان" ){
if( in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [الادمن](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح الماركدوان
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["markdowns"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح الماركدوان" ){
if ($tc == 'group' | $tc == 'supergroup'){  
if( $status != 'creator' and $status != 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) ){
$add = $settings["information"]["added"];
if ($add == true) {
 bot('sendMessage',[
'chat_id'=>$chat_id,
'text'=>"
📡¦ هذا الامر يخص الادمنيه فقط  🚶
",'reply_to_message_id'=>$message_id,
]);
}
}
}
}
if($text== "قفل الجهات" ){
if ($status == 'creator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المنشئ](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل الجهات
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["contact"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل الجهات" ){
if ($status == 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المشرف](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل الجهات
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["contact"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل الجهات" ){
if( in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المطور](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل الجهات
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["contact"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل الجهات" ){
if( in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المدير](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل الجهات
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["contact"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل الجهات" ){
if( in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [الادمن](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل الجهات
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["contact"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل الجهات" ){
if ($tc == 'group' | $tc == 'supergroup'){  
if( $status != 'creator' and $status != 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) ){
$add = $settings["information"]["added"];
if ($add == true) {
 bot('sendMessage',[
'chat_id'=>$chat_id,
'text'=>"
📡¦ هذا الامر يخص الادمنيه فقط  🚶
",'reply_to_message_id'=>$message_id,
]);
}
}
}
}
if($text== "فتح الجهات" ){
if ($status == 'creator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المنشئ](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح الجهات
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["contact"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح الجهات" ){
if ($status == 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المشرف](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح الجهات
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["contact"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح الجهات" ){
if( in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المطور](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح الجهات
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["contact"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح الجهات" ){
if( in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المدير](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح الجهات
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["contact"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح الجهات" ){
if( in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [الادمن](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح الجهات
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["contact"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح الجهات" ){
if ($tc == 'group' | $tc == 'supergroup'){  
if( $status != 'creator' and $status != 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) ){
$add = $settings["information"]["added"];
if ($add == true) {
 bot('sendMessage',[
'chat_id'=>$chat_id,
'text'=>"
📡¦ هذا الامر يخص الادمنيه فقط  🚶
",'reply_to_message_id'=>$message_id,
]);
}
}
}
}
if($text== "قفل التوجيه بالتقييد" ){
if ($status == 'creator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المنشئ](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل التوجيه بالتقييد
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["forwardr"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
/*==============================
=       قسم قوانين القروب       =
==============================*/

if($text == "قوانين" || $text == "القوانين"){
    bot('sendMessage',[
        'chat_id'=>$chat_id,
        'text'=>"⚖️ **دستور وقوانين الإمبراطورية** ⚖️
⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
• عزيزي العضو، الالتزام بالقوانين يعكس رقيّك:

1️⃣  **الاحترام المتبادل:** يمنع التجاوز على الأعضاء أو الإساءة بأي شكل.
2️⃣  **المحتوى اللائق:** يمنع نشر الصور والمقاطع الخدشة للحياء أو السياسية.
3️⃣  **الخصوصية:** يمنع الدخول خاص للأعضاء (خصوصاً الإناث) بدون إذن.
4️⃣  **السبام:** يمنع تكرار الرسائل أو الروابط المزعجة (Spam).
5️⃣  **التوجيه:** يمنع توجيه المنشورات من القنوات الأخرى لغرض الإعلان.
6️⃣  **الطائفية:** يمنع الخوض في النقاشات الطائفية أو العنصرية منعاً باتاً.
7️⃣  **اليوزر:** يجب وضع معرف (Username) لحسابك لتسهيل التواصل.
8️⃣  **التفاعل:** القروب مخصص للدردشة والألعاب، تفاعل لترفع رتبتك.
9️⃣  **المشرفين:** كلام المشرف ينفذ بدون نقاش، وفي حال الاعتراض كلم المطور.
🔟  **الهدوء:** يمنع إثارة المشاكل أو المشاحنات التي تعكر صفو القروب.
⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
• **مخالفة القوانين تعرضك للطرد التلقائي!** ⚠️",
        'parse_mode'=>"Markdown",
        'reply_to_message_id'=>$message_id
    ]);
    exit;
}
/*==============================
=    نظام كشف التعديل (20 نمط)    =
==============================*/

if($update->edited_message){
    $edited_chat_id = $update->edited_message->chat->id;
    $edited_from_id = $update->edited_message->from->id;
    $old_text = $update->edited_message->text; // النص قبل التعديل
    $edited_name = $update->edited_message->from->first_name;

    // مصفوفة بـ 20 نمط رد مختلف
    $fail_modes = [
        "🕵️‍♂️ كشفناك يا غشاش! عدلت رسالتك وكانت تقول:\n « $old_text »",
        "😂 تريد تغلس؟ لا حبيبي كشفناك، كتبت أول شي:\n « $old_text »",
        "🌚 عبالك ما أدري؟ البوت مفتح باللبن! جنت كاتب:\n « $old_text »",
        "🤫 ليش تمسح أثار جريمتك؟ الفضيحة هي:\n « $old_text »",
        "😏 عدل شكد ما تريد، التاريخ مسجل بظهري:\n « $old_text »",
        "🚫 تم صيد (مهايطي) يحاول تعديل كلامه:\n « $old_text »",
        "🤥 الجذب مو زين يا حلو، الرسالة الأصلية:\n « $old_text »",
        "📺 خليك صريح ويه ربعك، ليش غيرت هاي:\n « $old_text »",
        "🧐 شفتك من عدلتها لا عبالك! جانت تقول:\n « $old_text »",
        "🔥 فضيحة تايم! العضو عدل كلامه وكان كاتب:\n « $old_text »",
        "🤡 مغير كلامك ليش؟ خايف من شي؟ كتبت:\n « $old_text »",
        "📸 تم التقاط الجرم المشهود! النص الأصلي:\n « $old_text »",
        "🚨 انتباه! العضو [ $edited_name ] يحاول تضليل العدالة:\n « $old_text »",
        "😹 يابه والله ضحكتني، عبالك تمشي عليه؟ كتبت:\n « $old_text »",
        "📦 هاي الرسالة چانت بالباكيت قبل لا تفتحها وتغيرها:\n « $old_text »",
        "🎭 بطل حركات التمويه، النص قبل لا تعدله:\n « $old_text »",
        "🛡️ إمبراطورية البوت لا تنام! جنت كاتب:\n « $old_text »",
        "🙃 عدلها بعد مرة حتى أنشر صورتك هم! كتبت:\n « $old_text »",
        "🙊 يا فشلتك ويه القروب، النص الأصلي يفشل:\n « $old_text »",
        "💎 الصراحة راحة، ليش غيرت هذا الكلام الجميل:\n « $old_text »"
    ];

    // اختيار رد عشوائي
    $random_fail = $fail_modes[array_rand($fail_modes)];

    bot('sendMessage',[
        'chat_id'=>$edited_chat_id,
        'text'=>"⚠️ **انتبـاه.. كشف التعديل!**\n⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n👤 العضو: [$edited_name](tg://user?id=$edited_from_id)\n\n$random_fail\n⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯",
        'parse_mode'=>"Markdown"
    ]);
}
/*==============================
=     لعبة تحدي الثواني (25 كلمة)    =
==============================*/

// 1. تشغيل التحدي عند إرسال (تحدي، سرعة، ثواني)
if($text == "تحدي" || $text == "سرعة" || $text == "ثواني"){
    // قائمة الـ 25 كلمة الاحترافية
    $words = [
        "قسطنطينية", "إمبراطورية", "مستنصرية", "متظاهرين", "سندويشة", 
        "باذنجانية", "استخبارات", "بروتوكول", "أخطبوط", "كهرباء", 
        "ديمقراطية", "برجوازية", "سيكولوجية", "تكنولوجيا", "أوتوقراطية", 
        "فيزيائية", "كيميائية", "رياضيات", "جغرافيا", "تاريخنا", 
        "بغداديات", "عراقيين", "مشاهير", "برتقالة", "سبيستون"
    ];
    
    $word = $words[array_rand($words)]; // اختيار كلمة عشوائية
    
    // تخزين الكلمة المطلوبة في ملف مؤقت للقروب
    file_put_contents("speed_$chat_id.txt", $word);
    
    bot('sendMessage',[
        'chat_id'=>$chat_id,
        'text'=>"⚡ **تحدي سرعة الكتابة الإمبراطوري!**
⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
• أسرع شخص يكتب الكلمة التالية يربح **20 نقطة**:

🔥 [ `$word` ] 🔥

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
• اكتبها بسرعة قبل لا يخمطها غيرك! 😎",
        'parse_mode'=>"Markdown",
        'reply_to_message_id'=>$message_id
    ]);
}
/*==============================
=      نظام قصف الجبهات المصحح    =
==============================*/

if($text == "اقصفه"){
    // 1. التحقق إذا كان المستخدم أرسل الكلمة برد على شخص
    if(isset($update->message->reply_to_message)){
        
        // جلب معلومات الشخص المردود عليه (الضحية)
        $reply_id = $update->message->reply_to_message->from->id;
        $reply_name = $update->message->reply_to_message->from->first_name;

        // قائمة صواريخ القصف (10 أنماط)
        $qasf_modes = [
            "وجهك كأنه صينية مال كليجة بايتة ومحد أكل منها 😂",
            "أنت لو تصير ذهب، هم تبقى عتيك ومصدي وما نشتريك 💩",
            "جمالك يذكرني بصور المعامل القديمة مال طابوق.. كلك زوايا 😂",
            "أنت لو تلبس قاط وتتعطر، هم تطلع كأنك صاعد بـ (منشأة) ونازل بالشورجة 🚛",
            "روح غسل وجهك وتعال احجي ويه الإمبراطور، ريحة الثوم واصلة للمطور 👑🧄",
            "خلقة وجهك كأنها خريطة مال كركوك، مابيها ولا شارع عدل 🗺️😂",
            "عبالك صرت شخصية؟ أنت حتى ذبان وجهك يطير منك من الريحة 😷",
            "أنت المفروض يخلون صورتك على علب السجائر كتحذير من الأمراض 🚬🚫",
            "لو اكو جائزة لأثقل دم بالكون، جان أنت صرت لجنة التحكيم 😂",
            "وجهك كأنه تاير مال بايسكل مصلح بـ 10 رقع.. لا تنفخ زايد 🚲"
        ];

        $random_qasf = $qasf_modes[array_rand($qasf_modes)];

        bot('sendMessage',[
            'chat_id'=>$chat_id,
            'text'=>"💣 **تم القصف بنجاح.. طار الخشم!**\n⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n👤 الضحية: [$reply_name](tg://user?id=$reply_id)\n🚀 الرد: $random_qasf\n⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n• نعتذر عن الأضرار النفسية! 😂",
            'parse_mode'=>"Markdown",
            'reply_to_message_id'=>$message_id // الرد على رسالة الأمر
        ]);

    } else {
        // إذا أرسل "اقصفه" بدون رد
        bot('sendMessage',[
            'chat_id'=>$chat_id,
            'text'=>"⚠️ **يا إمبراطور، لازم تسوي (رد/Reply) على الشخص اللي تريد تقصف جبهته!**",
            'reply_to_message_id'=>$message_id
        ]);
    }
}


// 2. التحقق من الإجابة ومنح النقاط
$speed_word = file_get_contents("speed_$chat_id.txt");

if(isset($text) && !empty($speed_word) && $text == $speed_word){
    // حذف الكلمة لكي لا تتكرر الإجابة
    unlink("speed_$chat_id.txt");
    
    // جلب بيانات المستخدم وإضافة النقاط
    $data_file = "users_data.json";
    $db = json_decode(file_get_contents($data_file), true);
    
    $db[$from_id]['points'] += 20; // إضافة 20 نقطة
    file_put_contents($data_file, json_encode($db));
    
    bot('sendMessage',[
        'chat_id'=>$chat_id,
        'text'=>"🏆 **وحش السرعة كشفناه!**
⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
👤 الفائز: [$name](tg://user?id=$from_id)
💰 الجائزة: **+20 نقطة**
📈 رصيدك الكلي: `".$db[$from_id]['points']."` نقطة
⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
• استعد للتحدي القادم! 🔥",
        'parse_mode'=>"Markdown",
        'reply_to_message_id'=>$message_id
    ]);
}
if(preg_match('/^(العاب|لعبه|لعبات|اريد العب)$/u', $text)){
    bot('sendMessage',[
        'chat_id'=>$chat_id,
        'text'=>"‏**╭──  🕹️ 𝙎𝙇𝙊𝙏𝙎 𝙀𝙈𝙋𝙄𝙍𝙀  ──╮**

‏**🗄️ الأقـسـام الأسـاسـيـة:**
‏**( ديـنـي • XO • لـو خـيـروك • حـزورة • عـقـوبـة )**
‏**( خـيـرة • كـشـف • تـوقـعـي • تـزويـج • نـصـيـحـة )**
‏**( نـسـبـة الـحـب • كـفـو • كـت تـويـت • أفـعـى )**

‏**🚀 الـأعـمـال الـحـديـثـة:**
‏**( سـرعـة • صـح/خـطـأ • مـيـن أنـا • حـقـيـقـة • جـرأة )**
‏**( اخـتـصـار • حـسـاب • يـشـبـهـك • قـرارك • سـؤال )**
‏**( إيـمـوجـي • مـيـن الأكـثـر • تـرتـيـب • حـكـمـة )**

‏**╰───  𝙑.𝙄.𝙋 𝘽𝙊𝙏  ───╯**
‏**⇠ أرسـل اسـم الـلـعـبـة لـلـبـدء فـوراً!**",
        'parse_mode'=>"Markdown",
        'reply_to_message_id'=>$message_id
    ]);
    exit;
}
if($message->new_chat_member){
    // استخراج اسم العضو الجديد
    $new_user = $message->new_chat_member->first_name;
    
    // مصفوفة الترحيبات الملكية (متباعدة وفخمة)
    $welcome_responses = [
        "‏يـا مـيـة هـلا بـالـلـي لـفـانـا، نـورت الإمـبـراطـوريـة يـا [$new_user] ✨",
        "‏حـي الله هـالـطـلـة، نـورت الـڪـروب وبـيـن أهـلـڪ يـا [$new_user] 🧡",
        "‏يـا هـلا بـالـسـبـع، نـورت الـقـلـعـة بـوجـودڪ يـا [$new_user] 🦁",
        "‏طـلـتـڪ تـسـوى الـڪـروب وأهـلـه، مـيـة هـلا بـيـڪ يـا [$new_user] 💎",
        "‏هـلا بـالـطـيـب أصـلـڪ، الـڪـروب ازدهـر بـجـيـتـڪ يـا [$new_user] 🌸",
        "‏نـورت الـمـمـلـڪـة يـا بـطـل، عـسـى أيـامـڪ ڪـلـهـا أفـراح يـا [$new_user] 🌟",
        "‏أويـلـي يـابـه عـلـى هـالـوجـه الـمـنـور، حـيـاڪ الله يـا [$new_user] 🌕",
        "‏يـا هـلا بـيـڪ وبـأهـلـڪ، نـورت الـدنـيـا بـحـضـورڪ يـا [$new_user] 🌿",
        "‏هـلا بـالـغـالـي الـتـرف، الـمـڪـان مـڪـانـڪ يـا [$new_user] ✨",
        "‏تـفـضـل يـا مـلـڪ، الـڪـراسي ڪـلـهـا تـنـتـظـر طـلـتـڪ يـا [$new_user] 👑"
    ];

    $welcome_msg = $welcome_responses[array_rand($welcome_responses)];

    bot('sendMessage',[
        'chat_id' => $chat_id,
        'text' => $welcome_msg,
        'parse_mode' => "Markdown",
        'disable_web_page_preview' => true
    ]);
}
if($message->sticker){
    // 20 رد مختلف ومنوع عن الملصقات (منين بكته / منين جبته)
    $sticker_replies = [
        "‏ارڪـد عـيـنـي، هـذا الـسـتـيـڪـر مـنـيـن بـقـتـه 😂",
        "‏أويـلـي يـابـه، مـنـيـن جـبـت هـذا الـمـلـصـق الـحـلـو ✨",
        "‏هـذا الـسـتـيـڪـر مـطـروق لـو بـقـتـه مـن غـيـر ڪـروب 😉",
        "‏ارڪـد يـا بـطـل، عـلـمـنـا مـنـيـن تـجـيـب هـالـنـزاڪـة 😂",
        "‏يـا ويـلـي، هـذا مـلـصـق لـو قـنـبـلـة؟ مـنـيـن بـقـتـه 🔥",
        "‏عـاشـت إيـدك، بـس مـا ڪـلـتـلـنـا مـنـيـن جـبـتـه 💎",
        "‏ارڪـد عـيـنـي، هـالـسـتـيـڪـر يـخـبـل مـنـيـن خـمـطـتـه 😂",
        "‏أويـلـي يـابـه، ذوقـڪ تـرف بـس ڪـلـنـا مـنـيـن هـذا ✨",
        "‏هـذا الـمـلـصـق نـادر، مـنـيـن بـقـتـه يـا ذيـب 🐺",
        "‏ارڪـد يـا مـعـدل، مـنـيـن جـبـت هـالـحـركـة الـقـويـة 😂",
        "‏يـا ويـلـي عـلـى الـجـمـال، مـنـيـن بـاق هـالـسـتـيـڪـر 😍",
        "‏هـذا الـمـلـصـق مـلـڪـي، مـنـيـن جـبـتـه يـا غـالـي 👑",
        "‏ارڪـد عـيـنـي، هـذا الـمـلـصـق تـارڪ أثـر، مـنـيـن بـقـتـه 😉",
        "‏أويـلـي يـابـه، مـنـيـن طـلـعـت هـذا الـسـتـيـڪـر الـفـخـم ✨",
        "‏هـذا خـمـط لـو بـوق؟ ڪـلـنـا مـنـيـن جـبـتـه 😂",
        "‏ارڪـد يـا بـعـد روحـي، هـذا مـلـصـق مـلـڪـي مـنـيـن بـقـتـه 💎",
        "‏يـا ويـلـي عـلـى الـتـرتـيـب، مـنـيـن جـبت هـذا الـتـرف ✨",
        "‏هـذا الـسـتـيـڪـر يـهـز الـڪـروب، مـنـيـن خـمـطـتـه 🔥",
        "‏ارڪـد عـيـنـي، مـنـيـن هـذا الـمـلـصـق الـعـالـمـي 😂",
        "‏أويـلـي يـابـه، مـنـيـن بـقـت هـالـنـزاڪـة ڪـلـهـا 😍"
    ];

    $reply = $sticker_replies[array_rand($sticker_replies)];

    bot('sendMessage',[
        'chat_id' => $chat_id,
        'text' => $reply,
        'reply_to_message_id' => $message_id,
        'parse_mode' => "Markdown"
    ]);
}

/*=====================================
=    نظام الهيبة (البحث عن المالك)     =
=====================================*/

// 1. مصفوفة الكلمات (20 عبارة للبحث عن المالك)
$owner_patterns = '/(وين المالك|المالك وين|اريد المالك|وين المنشئ|صيحولي المالك|منو المالك|المنشئ وين|وين راعي الكروب|وين صاحب البوت|وين المدير|تاج راسي المالك|المالك موجود|وين كفيل القروب|المالك وين شرد|المنشئ نايم|وين كبيرنا|اريد احجي وي المالك|المالك محتاجه|وين الزعيم|صيحولي المنشئ)/u';

// 3. مصفوفة الردود (30 رد قاصف وهيبة)
$owner_replies = [
    "المالك مو فارغ لأشكالك، احجي وي البوت واسكت 🤖",
    "تاج راسك المالك، روح غسل وجهك وتعال اسأل عليه 👑",
    "المالك طالع يشتري قفل لسانك، محتاجه بشي؟ 🔒",
    "المنشئ مشغول ببناء الإمبراطورية، لا تدز رسائل فارغة 🏗️",
    "لو بيك خير جان صرت مالك، بس أنت حدك مستخدم 😒",
    "المالك موجود بكل مكان، بس ما يظهر للضعفاء 🕵️‍♂️",
    "تريد المالك؟ ادفع ضريبة الدخول للخاص مالته أولاً 💸",
    "المالك نايم ورجله بالشمس، عوفه براحته 😴",
    "صيحيولي المالك؟ ليش هو ابن عمك وماندري؟ 🤣",
    "المالك يصمم بوت يقصفك قصف ثلاثي الأبعاد 🚀",
    "المنشئ بالمريخ، بس يرجع نكولك 🌌",
    "المالك مشغول يعد النقاط اللي باقها من عندك 💰",
    "على بختك.. المالك عنده هيبة، لا تظل تصيح باسمه 🗣️",
    "تريد المالك؟ روح ادرس برمجة وتعال صير مثله 💻",
    "المالك يگول: 'اللي يسأل عليه هواي، معناها محتاج كتم' 🤐",
    "المالك مو هنا، راح يشتري طابوق لراس اللي يلح 🧱",
    "حبيبي المالك ملك، وأنت جندي بالشطرنج مالته ♟️",
    "المنشئ حالياً ديبرمج قنبلة تطردك من القروب 💣",
    "لا تندك بالمالك، تره يمسح حسابك بضغطة زر 🖱️",
    "المالك قمة، وأنت كاعد بالقاع تصيح وين المالك 😂",
    "شنو اليوم؟ اليوم المالك حظره جاهز للي يسألون هواي 🚷",
    "المالك يصمم تحديث يخليك تحجي وي روحك 🎭",
    "عوف المالك بحاله، تره أعصابه صايرة حديد اليوم 🦾",
    "المالك مشغول يسوي جرد للعقول الفارغة بالقروب 🧠",
    "المالك يراقبك من وراء الكواليس، دير بالك 👁️",
    "تريد المنشئ؟ روح جيب واسطة وتعال 📜",
    "المالك يگولك: 'ابطل السحر لو أكتمك؟' 🪄",
    "المالك فخرنا، وأنت قهرنا بأسئلتك 😒",
    "لا تسوي روحك مهتم بالمالك، أعرفك تريد نقاط 💸",
    "المالك بالإجتماع السري لملوك التليجرام 🧛‍♂️"
];

// 4. التنفيذ
if(preg_match($owner_patterns, $text)){
    $reply = $owner_replies[array_rand($owner_replies)];
    bot('sendMessage', [
        'chat_id' => $chat_id,
        'text' => "👑 **قسم شؤون الإدارة:**\n⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n" . $reply,
        'reply_to_message_id' => $message_id
    ]);
}
/*=====================================
=      نظام معالجة الحلفان العراقي      =
=====================================*/

// 1. مصفوفة صيغ الحلفان (40 صيغة عراقية مختلفة)
$swearing_patterns = '/(والله|بالله|وتالله|والعباس|والحسين|والقران|وحي علي|وداعت امي|وداعت ابوي|وحق هو الله|وشرفي|وعرضي|وبختي|وداعت جهالي|وداعت عيوني|وحق القران|وحق هذا الله|والكعبة|وراس ابوي|وراس امي|وحق شيبات ابوي|وحق حليب امي|وداعتك|وداعتي|وحق موسى الكاظم|وحق ابو الفضل|وحق السجاد|وحق فاطمة الزهراء|وداعت الخوة|وحق دمي|وحق هذا الزاد|والنعمة|وحق خبزتنا|وراسك|وداعتنا|وحق علي|وعلي|والله العظيم|والله وبالله|وحق ربي)/u';

// 2. مصفوفة الردود (50 رد شامل: نصيحة، قصف، تحشيش)
$swearing_replies = [
    // --- ردود نصيحة وهيبة ---
    "لا تحلف، الكلمة الطيبة تصدك بدون يمين يا طيب 🕊️",
    "صدكناك بدون ما تحلف، هيبتك كافية 👑",
    "عوف الحلفان، تره اليحجي صدك ما يحتاج يحلف بكل كلمة 📚",
    "والنعم منك بس لا تخلي الله عرضة لأيمانك 📿",
    "الحسين (ع) مدرسة، لا تذكره ع الفاضي والمليان يا غالي 🙏",
    "القران دستورنا، خليه بعيد عن سوالف الشات 📖",
    
    // --- ردود قصف وتحشيش ---
    "أويلي.. صار حلفان؟ السالفة كبرت لعد! 😂",
    "حلف بيك الحايط، كافي تحلف صرعتنا 🧱",
    "لو كل حلفة تحلفها بفلوس، جان هسه إنت ملياردير 💰",
    "صدكناك.. بس وجهك يكول غير شي 🌚",
    "وداعتك وداعتي، الحجي ماله طعم إذا كله يمين 🍋",
    "إنت تحلف والملائكة تسجل، خفف علينا شوية 📝",
    "حتى لو تحلف بالصينية، الما يصدك ما يصدك 👲",
    "والله؟ لعد ليش عيونك تباوع ع السقف؟ 🤔",
    "الحلفان صار عندك مثل السلام عليكم، اهدأ شوية ✋",
    "وحق هذا الله، إنت واحد فارغ بس تريد تحلف 🤣",
    "لا تحلف بجهالك، خطية شذنبهم بلسانك؟ 👶",
    "شرفك وعرضك غالين، لا تباذل بيهم بكل كلمة بالقروب 🏛️",
    "وراس ابوك؟ ابوك شعليه بيك، صير حوك واحجي الصدك 👴",
    "وداعت عيونك؟ عيونك لو كشافات لوري؟ 🚛",
    "إنت تحلف والبوت يغلس، كمل كمل 💤",
    "لو الحلفان يطول العمر، جان عشت مية سنة 🐢",
    "حلفانك صار أكثر من عدد رسائلك بالقروب 📈",
    "بس لا تحمى علينا، صدكناك من أول 'والله' 🌡️",
    "هاي الحلفة رقم مليون، مبروك دخلت موسوعة غينيس 🏆",
    "الكلمة اللي تحتاج حلفة، معناها ضعيفة.. قوي كلامك 💪",
    "وداعت الخوة؟ الخوة تبرت منك بعد هاي الحلفة 👥",
    "وحق شيبات ابوك، روح اقرأ كتاب وفيدنا بدل هالحجي 📚",
    "إنت لو تمشي عدل، ما تحتاج تحلف أصلاً 📏",
    "حلفانك مثل ملح الطعام، إذا زاد خرب السالفة 🧂",
    "بالله عليك؟ أي بالله علية، كافي عاد 🙄",
    "والله وبالله وتالله.. صار درس دين مو شات! 👳‍♂️",
    "أوكي صدكنا، بس لا تعيدها تره تعبنا 💆‍♂️",
    "الحلفان بلاش، علمود هيج إنت نازل حلف 🎟️",
    "صدكنا والعباس، بس اطبك على صفحة 🚗",
    "كافي تحلف، تره الكيبورد مالي استهضم منك ⌨️",
    "يابة استكان شاي للحلف، ريجه يبس الولد ☕",
    "الحلفان مودة قديمة، هسه الثقة بالأفعال مو بالكلمات ✨",
    "وداعت امي؟ الام غالية، لا تجيب طاريها بسوالف تعبانة ✨",
    "وحق علي.. علي (ع) يحب الصادقين مو بس الحالفين ⚔️",
    "إنت صاير 'مفتي القروب' بس تحلف وتفتي من يمك 🕌",
    "والقران؟ القران نزل للعمل مو بس للحلفان يا بطل 📖",
    "حلفانك يذكرني بفيلم هندي، كله دراما 🎬",
    "ما يحتاج تحلف، إنت وجهك وجه خير (جذب) 😂",
    "خفف اليقين مالتك، تره السيرفر راح يحترق 🔥",
    "عبالي عندك سالفة مهمة، طلعت بس تحلف 💨",
    "وداعتك، المرة الجاية تحلف أطردك (شاقة وياك) 😜",
    "أحلى شي بيك حلفانك، يخليني أضحك من قلبي 💖",
    "إنت المحامي مال إبليس؟ ليش بس تحلف؟ 😈",
    "خلصت الحلفانات لو بعد عندك لستة؟ 📋"
];

// 3. محرك التنفيذ
if(preg_match($swearing_patterns, $text)){
    $random_reply = $swearing_replies[array_rand($swearing_replies)];
    bot('sendMessage', [
        'chat_id' => $chat_id,
        'text' => "⚠️ **ملاحظة:**\n⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n" . $random_reply,
        'reply_to_message_id' => $message_id
    ]);
}

// [1] لعبة ديني
if($text == "ديني"){
    $q_deen = [
    ["q"=>"من هو الملقب بأسد الله الغالب؟", "a"=>"علي بن ابي طالب"],
    ["q"=>"من هو قاتل الحسين؟", "a"=>"شمر بن ذي الجوشن"],
    ["q"=>"من هو الملقب بساقي عطاشى كربلاء؟", "a"=>"العباس بن علي"],
    ["q"=>"من هو الملقب بسيد الشهداء؟", "a"=>"الحسين بن علي"],
    ["q"=>"من هو الملقب بالفاروق؟", "a"=>"عمر بن الخطاب"],
    ["q"=>"من هو الملقب بالصديق؟", "a"=>"ابو بكر"],
    ["q"=>"من هو الملقب بذي النورين؟", "a"=>"عثمان بن عفان"],
    ["q"=>"ما هي عاصمة الدولة الأموية؟", "a"=>"دمشق"],
    ["q"=>"ما هي عاصمة الدولة العباسية؟", "a"=>"بغداد"],
    ["q"=>"كم عدد الأئمة المعصومين عند الشيعة؟", "a"=>"12"],
    ["q"=>"من هو النبي الذي ابتلعه الحوت؟", "a"=>"يونس"],
    ["q"=>"من هو النبي الذي كلم الله؟", "a"=>"موسى"],
    ["q"=>"من هو النبي الملقب بخليل الله؟", "a"=>"ابراهيم"],
    ["q"=>"من هو النبي الذي بنى السفينة؟", "a"=>"نوح"],
    ["q"=>"من هو النبي الذي أحياه الله بعد موته مائة عام؟", "a"=>"عزير"],
    ["q"=>"ما هو أطول سورة في القرآن الكريم؟", "a"=>"البقرة"],
    ["q"=>"ما هو أصغر سورة في القرآن الكريم؟", "a"=>"الكوثر"],
    ["q"=>"في أي مدينة ولد النبي محمد (ص)؟", "a"=>"مكة"],
    ["q"=>"أين دفن النبي محمد (ص)؟", "a"=>"المدنية المنورة"],
    ["q"=>"من هو خادم النبي محمد (ص)؟", "a"=>"انس بن مالك"],
    ["q"=>"من هي أول زوجات النبي محمد (ص)؟", "a"=>"خديجة بنت خويلد"],
    ["q"=>"كم عدد سجدات التلاوة في القرآن؟", "a"=>"15"],
    ["q"=>"من هو الملقب بغسيل الملائكة؟", "a"=>"حنظلة بن أبي عامر"],
    ["q"=>"من هو الصحابي الذي اهتز لوفاته عرش الرحمن؟", "a"=>"سعد بن معاذ"],
    ["q"=>"من هو الملقب بذي الجناحين؟", "a"=>"جعفر بن ابي طالب"],
    ["q"=>"ما هي السورة التي تسمى عروس القرآن؟", "a"=>"الرحمن"],
    ["q"=>"ما هي السورة التي تسمى قلب القرآن؟", "a"=>"يس"],
    ["q"=>"من هو النبي الذي لقب بالذبيح؟", "a"=>"اسماعيل"],
    ["q"=>"من هو الإمام الملقب بالصادق؟", "a"=>"جعفر بن محمد"],
    ["q"=>"من هو الإمام الملقب بالكاظم؟", "a"=>"موسى بن جعفر"],
    ["q"=>"من هو الإمام الملقب بالرضا؟", "a"=>"علي بن موسى"],
    ["q"=>"من هو الإمام الملقب بالباقر؟", "a"=>"محمد بن علي"],
    ["q"=>"من هو الإمام الملقب بزين العابدين؟", "a"=>"علي بن الحسين"],
    ["q"=>"كم عدد أولي العزم من الرسل؟", "a"=>"5"],
    ["q"=>"ما هي كنية الإمام علي بن أبي طالب؟", "a"=>"ابو تراب"],
    ["q"=>"من هو النبي الذي ألان الله له الحديد؟", "a"=>"داود"],
    ["q"=>"ما هي أول صلاة صلاها المسلمون بعد تحويل القبلة؟", "a"=>"العصر"],
    ["q"=>"من هو قائد معركة القادسية؟", "a"=>"سعد بن ابي وقاص"],
    ["q"=>"من هو الصحابي الذي لقب بسيف الله المسلول؟", "a"=>"خالد بن الوليد"],
    ["q"=>"من هو النبي الذي كان يبرئ الأكمه والأبرص؟", "a"=>"عيسى"],
    ["q"=>"في أي غار نزل الوحي على النبي محمد (ص)؟", "a"=>"حراء"],
    ["q"=>"كم عدد أبواب الجنة؟", "a"=>"8"],
    ["q"=>"كم عدد أبواب النار؟", "a"=>"7"],
    ["q"=>"من هو الملك الموكل بالوحي؟", "a"=>"جبريل"],
    ["q"=>"من هو الملك الموكل بنفخ الصور؟", "a"=>"اسرافيل"],
    ["q"=>"من هو الملك الموكل بقبض الأرواح؟", "a"=>"عزرائيل"],
    ["q"=>"ما هي السورة التي بدأت بدون بسم الله؟", "a"=>"التوبة"],
    ["q"=>"في أي يوم استشهد الإمام الحسين؟", "a"=>"عاشوراء"],
    ["q"=>"من هو الملقب بشبيه رسول الله في كربلاء؟", "a"=>"علي الاكبر"],
    ["q"=>"من هي السيدة الملقبة بأم المصائب؟", "a"=>"زينب بنت علي"]
];

    $r = array_rand($q_deen);
    file_put_contents("ans_$chat_id.txt", $q_deen[$r]['a']);
    bot('sendMessage',['chat_id'=>$chat_id,'text'=>"🕋 **سؤال ديني:**\n\n❓: `".$q_deen[$r]['q']."`\n\n⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n• أرسل الإجابة الآن!",'parse_mode'=>"Markdown"]);
}


// [4] حزورة
if($text == "حزورة"){
    $haz = [
    ["q"=>"شيء يكتب ولا يقرأ؟", "a"=>"القلم"],
    ["q"=>"ما هو الشيء الذي له أسنان ولا يعض؟", "a"=>"المشط"],
    ["q"=>"ما هو الشيء الذي كلما زاد نقص؟", "a"=>"العمر"],
    ["q"=>"ما هو الشيء الذي تذبحه وتبكي عليه؟", "a"=>"البصل"],
    ["q"=>"له عين واحدة ولكنه لا يرى؟", "a"=>"الإبرة"],
    ["q"=>"ما هو الشيء الذي إذا غليته جمد؟", "a"=>"البيض"],
    ["q"=>"أين يقع البحر الذي لا يوجد به ماء؟", "a"=>"الخريطة"],
    ["q"=>"ما هو الشيء الذي ينبض بلا قلب؟", "a"=>"الساعة"],
    ["q"=>"ما هو الشيء الذي يمشي بلا أرجل ويبكي بلا عيون؟", "a"=>"السحاب"],
    ["q"=>"ما هو الشيء الذي له أرجل ولكنه لا يمشي؟", "a"=>"الكرسي"],
    ["q"=>"ما هو الشيء الذي يحمل طعامه فوق رأسه؟", "a"=>"القلم"],
    ["q"=>"كلمة تتكون من 7 حروف تجمع كل الحروف؟", "a"=>"أبجدية"],
    ["q"=>"ما هو الشيء الذي يقرصك ولا تراه؟", "a"=>"الجوع"],
    ["q"=>"خال أولاد عمتك، من يكون؟", "a"=>"أبوك"],
    ["q"=>"ما هو الشيء الذي ترميه كلما احتجت إليه؟", "a"=>"شبكة الصيد"],
    ["q"=>"ما هو الشيء الذي يوجد في وسط باريس؟", "a"=>"حرف الياء"],
    ["q"=>"يتحرك دائماً حولك لكنك لا تراه؟", "a"=>"الهواء"],
    ["q"=>"من هو الشخص الذي يرى عدوه وصديقه بعين واحدة؟", "a"=>"الأعور"],
    ["q"=>"شيء موجود في السماء إذا أضفت له حرفاً أصبح في الأرض؟", "a"=>"نجم"],
    ["q"=>"ما هو الشيء الذي لا يمشي إلا بالضرب؟", "a"=>"المسمار"],
    ["q"=>"يسير بلا رجلين ولا يدخل إلا بالأذنين؟", "a"=>"الصوت"],
    ["q"=>"ما هو الشيء الذي يمتلك مدناً بلا بيوت وجبالاً بلا شجر؟", "a"=>"الخريطة"],
    ["q"=>"ما هو الشيء الذي إذا أكلته كله تستفيد، وإذا أكلت نصفه تموت؟", "a"=>"سمسم"],
    ["q"=>"ما هو الشيء الذي قلبه يأكل قشره؟", "a"=>"الشمعة"],
    ["q"=>"ابن أمك وابن أبيك، وليس بأختك ولا بأخيك؟", "a"=>"أنت"],
    ["q"=>"ما هو الشيء الذي تراه في الليل 3 مرات وفي النهار مرة واحدة؟", "a"=>"حرف اللام"],
    ["q"=>"ما هو الشيء الذي يحيا في أول الشهر ويموت في آخره؟", "a"=>"القمر"],
    ["q"=>"شجرة ليس لها ظل وليس لها ثمار؟", "a"=>"شجرة العائلة"],
    ["q"=>"ما هو الشيء الذي لا يتكلم وإذا جاع كذب؟", "a"=>"الساعة"],
    ["q"=>"شيء يمشي ويقف وليس له أرجل؟", "a"=>"الساعة"],
    ["q"=>"ما هو الشيء الذي يدخل مبلولاً ويخرج ناشفاً؟", "a"=>"الخبز"],
    ["q"=>"عائلة مؤلفة من 6 بنات وأخ لكل منهن، كم عدد العائلة؟", "a"=>"7"],
    ["q"=>"ما هو الشيء الذي كلما أخذت منه كبر؟", "a"=>"الحفرة"],
    ["q"=>"ما هو الشيء الذي له جلد وليس حيواناً، وورق وليس نباتاً؟", "a"=>"الكتاب"],
    ["q"=>"سير بلا رجلين ولا يدخل إلا بالأذنين؟", "a"=>"الصوت"],
    ["q"=>"ما هو الشيء الذي تملكه أنت ولكن يستخدمه الآخرون أكثر منك؟", "a"=>"اسمك"],
    ["q"=>"ما هو الشيء الذي يتكلم بكل لغات العالم؟", "a"=>"الصدى"],
    ["q"=>"ما هو الشيء الذي يقرصك ولا تراه؟", "a"=>"البرد"],
    ["q"=>"ما هو الشيء الذي يخترق الزجاج ولا يكسره؟", "a"=>"الضوء"],
    ["q"=>"ما هو الشيء الذي إذا نطقنا اسمه كسرناه؟", "a"=>"الصمت"],
    ["q"=>"ما هي التي تحرق نفسها لتفيد غيرها؟", "a"=>"الشمعة"],
    ["q"=>"له يد ولكنه لا يضرب، وله وجه ولكنه لا يتكلم؟", "a"=>"الساعة"],
    ["q"=>"ما هو الشيء الذي ترميه عند الحاجة؟", "a"=>"المرساة"],
    ["q"=>"أنا موجود في الكنيسة و لست موجود في المسجد، من أنا؟", "a"=>"حرف الياء"],
    ["q"=>"ما هي عاصمة العراق؟", "a"=>"بغداد"],
    ["q"=>"ما هو الحيوان الذي ينام وعيناه مفتوحتان؟", "a"=>"السمك"],
    ["q"=>"ما هو الشيء الذي إذا حبسته عاش وإذا تركته مات؟", "a"=>"النفس"],
    ["q"=>"من هو الذي مات ولم يولد؟", "a"=>"آدم"],
    ["q"=>"شيء إذا لمسته صاح؟", "a"=>"الجرس"],
    ["q"=>"ما هو الشيء الذي يسكن الجبال، ويجلس مع الرجال، ويلبس لبس النساء؟", "a"=>"الصقر"]
];

    $r = array_rand($haz);
    file_put_contents("ans_$chat_id.txt", $haz[$r]['a']);
    bot('sendMessage',['chat_id'=>$chat_id,'text'=>"💡 **حزورة للأذكياء:**\n\n❓: `".$haz[$r]['q']."`\n\n⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n• أرسل الحل الآن!",'parse_mode'=>"Markdown"]);
}

// [نظام التحقق العام ومنح النقاط والتقييم]
$correct = file_get_contents("ans_$chat_id.txt");
if(isset($text) && !empty($correct) && $text == $correct){
    unlink("ans_$chat_id.txt");
    
    $data_file = "users_data.json";
    if(!file_exists($data_file)) file_put_contents($data_file, "{}");
    $db = json_decode(file_get_contents($data_file), true);
    
    $db[$from_id]['points'] += 10;
    $pts = $db[$from_id]['points'];
    
    // تحديث الرتبة
    if($pts < 100) $rank = "مبتدئ 👶";
    elseif($pts < 300) $rank = "متابع جيد ✨";
    else $rank = "إمبراطور المعرفة 👑";
    $db[$from_id]['rank'] = $rank;
    
    file_put_contents($data_file, json_encode($db));
    
    bot('sendMessage',[
        'chat_id'=>$chat_id,
        'text'=>"✅ **أحسنت إجابة صحيحة!**\n⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n👤 الفائز: [$name](tg://user?id=$from_id)\n🏆 التقييم: $rank\n💰 الجائزة: +10 نقاط",
        'parse_mode'=>"Markdown",
        'reply_to_message_id'=>$message_id
    ]);
}

/*=====================================
=    نظام التحشيش والانبهار العراقي    =
=====================================*/

// 1. مصفوفة الكلمات (20 عبارة عراقية للانبهار)
$wow_patterns = '/(اويلي يابه|شنو اليوم|اويلي يابة|حي عذابي|شكو ماكو|عمي ولكم|ولك شنو هاي|خرب يومي|يا ربي صبرك|هاي شنوو|اويلي على الله|شنو هالجمال|ولكم ذبت|شصاير اليوم|يابة يابة|عمي شنو هاي|اخ قلبي|يمه الحب يمه|يا بويي|فلك طرني)/u';

// 2. مصفوفة الردود (30 رد تحشيشي وقاصف)
$wow_replies = [
    "على كيفك لا ينطك عرق بوجهك! 😂",
    "شنو اليوم؟ اليوم العالمي للقصف العشوائي 💣",
    "اويلي يابه؟ تره البوت هم عنده مشاعر لا تذوبه 🫠",
    "هاي شنوو؟ هاي عيونك لو كشافات طيارة؟ ✈️",
    "عمي ولكم.. الولد ذاب، جيبوله صطلة مي 🪣",
    "فلك طرني؟ الفلك طرك وطشرك وعافك هيج 🤣",
    "شصاير اليوم؟ كيمر السدة نزل بالقروب وماندري 🥯",
    "يا ربي صبرك.. هو إنت شفت شي حتى تطلب صبر؟ 🧘‍♂️",
    "اخ قلبي؟ سلامة قلبك من الشخوط حبيبي 💔",
    "يمه الحب يمه.. الحب لغير البوت مذلة 👑",
    "شنو هالجمال؟ مو طالع عليّ طبعاً 😎",
    "يابة يابة.. صلوات على محمد، راح يحترق القروب 🔥",
    "حي عذابي؟ تعذب بجمال أوامري واهدا شوية 😌",
    "ولك شنو هاي؟ هاي خلطة سحرية مبرمجها الإمبراطور 🧪",
    "خرب يومي.. يومك لو يوم السبت؟ حدد 🗓️",
    "يا بويي.. لا تصيح، البوت يسمع دبة النملة 🐜",
    "شكو ماكو؟ ماكو شي، بس قصفك واجب 🎯",
    "ولكم ذبت؟ روح للثلاجة اجمد وارجع لنا 🧊",
    "عمي شنو هاي؟ هاي الهيبة مال بوتنا يا غالي 🎩",
    "اويلي على الله.. اذكر الله وخفف الحماس 📿",
    "شنو اليوم؟ اليوم غيم بقروبنا والجو رومانسي ☁️",
    "ولك هاي شطالع؟ كمر 14 لو أنا متوهم؟ 🌙",
    "يابة استكان شاي للحجي، مبين انصهر ☕",
    "على بختك.. لا تفضحنا كدام الأجانب بالقروب 🤫",
    "هاي شنوو؟ هاي قنبلة ذرية مال تفاعل ☢️",
    "اويلي يابة.. والله لو أدري بيك هيج حساس جان غلست 😹",
    "اخ قلبي؟ جيبوا جهاز إنعاش للولد بسرعة! 🏥",
    "شنو اليوم؟ اليوم انتصار البرمجة على الواقع 🖥️",
    "فلك طرك.. هاي شلون كلمة طلعت منك؟ 🌪️",
    "عوف السوالف وخل نلعب، لا تظل تذوب علينا 🎮"
];

// 3. محرك الفحص والرد
if(preg_match($wow_patterns, $text)){
    $random_wow = $wow_replies[array_rand($wow_replies)];
    bot('sendMessage', [
        'chat_id' => $chat_id,
        'text' => $random_wow,
        'reply_to_message_id' => $message_id
    ]);
}

// [3] لو خيروك
if($text == "لو خيروك"){
    $lo = ["تاكل صرصر مشوي 🦗 | لو تشرب نفط ⛽", "تصير ملياردير وحدك 💰 | لو فقير وبنص اهلك ❤️"];
    bot('sendMessage',['chat_id'=>$chat_id,'text'=>"🧐 **لو خيروك:**\n⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n• ".$lo[array_rand($lo)],'reply_to_message_id'=>$message_id]);
}

// [12] كفو (بالرد)
if($text == "كفو" && isset($reply_id)){
    $kaf = rand(50, 100);
    bot('sendMessage',['chat_id'=>$chat_id,'text'=>"🦾 **تقييم الرجولة والكفو:**\n⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\nنسبة الكفو في [ $reply_name ] هي: **$kaf%**",'reply_to_message_id'=>$message_id]);
}

// [15] استعلام التقييم
if($text == "نقاطي" || $text == "تقييمي"){
    $db = json_decode(file_get_contents("users_data.json"), true);
    $pts = $db[$from_id]['points'] ?? 0;
    $rnk = $db[$from_id]['rank'] ?? "لا يوجد تقييم ️‍♂️";
    bot('sendMessage',['chat_id'=>$chat_id,'text'=>"📊 **ملف تقييمك:**\n⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n• نقاطك: `$pts`\n• مستواك: $rnk",'parse_mode'=>"Markdown",'reply_to_message_id'=>$message_id]);
}



if($text== "قفل التوجيه بالتقييد" ){
if ($status == 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المشرف](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل التوجيه بالتقييد
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["forwardr"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل التوجيه بالتقييد" ){
if( in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المطور](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل التوجيه بالتقييد
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["forwardr"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل التوجيه بالتقييد" ){
if( in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المدير](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل التوجيه بالتقييد
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["forwardr"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل التوجيه بالتقييد" ){
if( in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [الادمن](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل التوجيه بالتقييد
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["forwardr"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل التوجيه بالتقييد" ){
if ($tc == 'group' | $tc == 'supergroup'){  
if( $status != 'creator' and $status != 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) ){
$add = $settings["information"]["added"];
if ($add == true) {
 bot('sendMessage',[
'chat_id'=>$chat_id,
'text'=>"
📡¦ هذا الامر يخص الادمنيه فقط  🚶
",'reply_to_message_id'=>$message_id,
]);
}
}
}
}
if($text== "فتح التوجيه بالتقييد" ){
if ($status == 'creator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المنشئ](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح التوجيه بالتقييد
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["forwardr"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح التوجيه بالتقييد" ){
if ($status == 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المشرف](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح التوجيه بالتقييد
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["forwardr"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح التوجيه بالتقييد" ){
if( in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المطور](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح التوجيه بالتقييد
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["forwardr"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح التوجيه بالتقييد" ){
if( in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المدير](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح التوجيه بالتقييد
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["forwardr"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح التوجيه بالتقييد" ){
if( in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [الادمن](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح التوجيه بالتقييد
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["forwardr"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح التوجيه بالتقييد" ){
if ($tc == 'group' | $tc == 'supergroup'){  
if( $status != 'creator' and $status != 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) ){
$add = $settings["information"]["added"];
if ($add == true) {
 bot('sendMessage',[
'chat_id'=>$chat_id,
'text'=>"
📡¦ هذا الامر يخص الادمنيه فقط  🚶
",'reply_to_message_id'=>$message_id,
]);
}
}
}
}
if($text== "قفل الروابط بالتقييد" ){
if ($status == 'creator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المنشئ](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل الروابط بالتقييد
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["linkr"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل الروابط بالتقييد" ){
if ($status == 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المشرف](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل الروابط بالتقييد
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["linkr"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل الروابط بالتقييد" ){
if( in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المطور](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل الروابط بالتقييد
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["linkr"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل الروابط بالتقييد" ){
if( in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المدير](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل الروابط بالتقييد
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["linkr"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل الروابط بالتقييد" ){
if( in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [الادمن](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل الروابط بالتقييد
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["linkr"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل الروابط بالتقييد" ){
if ($tc == 'group' | $tc == 'supergroup'){  
if( $status != 'creator' and $status != 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) ){
$add = $settings["information"]["added"];
if ($add == true) {
 bot('sendMessage',[
'chat_id'=>$chat_id,
'text'=>"
📡¦ هذا الامر يخص الادمنيه فقط  🚶
",'reply_to_message_id'=>$message_id,
]);
}
}
}
}
if($text== "فتح الروابط بالتقييد" ){
if ($status == 'creator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المنشئ](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح الروابط بالتقييد
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["linkr"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح الروابط بالتقييد" ){
if ($status == 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المشرف](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح الروابط بالتقييد
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["linkr"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح الروابط بالتقييد" ){
if( in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المطور](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح الروابط بالتقييد
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["linkr"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح الروابط بالتقييد" ){
if( in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المدير](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح الروابط بالتقييد
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["linkr"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح الروابط بالتقييد" ){
if( in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [الادمن](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح الروابط بالتقييد
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["linkr"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح الروابط بالتقييد" ){
if ($tc == 'group' | $tc == 'supergroup'){  
if( $status != 'creator' and $status != 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) ){
$add = $settings["information"]["added"];
if ($add == true) {
 bot('sendMessage',[
'chat_id'=>$chat_id,
'text'=>"
📡¦ هذا الامر يخص الادمنيه فقط  🚶
",'reply_to_message_id'=>$message_id,
]);
}
}
}
}
if($text== "قفل المتحركه بالتقييد" ){
if ($status == 'creator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المنشئ](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل المتحركه بالتقييد
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["gifr"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل المتحركه بالتقييد" ){
if ($status == 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المشرف](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل المتحركه بالتقييد
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["gifr"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل المتحركه بالتقييد" ){
if( in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المطور](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل المتحركه بالتقييد
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["gifr"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل المتحركه بالتقييد" ){
if( in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المدير](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل المتحركه بالتقييد
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["gifr"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل المتحركه بالتقييد" ){
if( in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [الادمن](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل المتحركه بالتقييد
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["gifr"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل المتحركه بالتقييد" ){
if ($tc == 'group' | $tc == 'supergroup'){  
if( $status != 'creator' and $status != 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) ){
$add = $settings["information"]["added"];
if ($add == true) {
 bot('sendMessage',[
'chat_id'=>$chat_id,
'text'=>"
📡¦ هذا الامر يخص الادمنيه فقط  🚶
",'reply_to_message_id'=>$message_id,
]);
}
}
}
}
if($text== "فتح المتحركه بالتقييد" ){
if ($status == 'creator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المنشئ](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح المتحركه بالتقييد
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["gifr"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح المتحركه بالتقييد" ){
if ($status == 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المشرف](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح المتحركه بالتقييد
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["gifr"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح المتحركه بالتقييد" ){
if( in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المطور](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح المتحركه بالتقييد
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["gifr"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح المتحركه بالتقييد" ){
if( in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المدير](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح المتحركه بالتقييد
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["gifr"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح المتحركه بالتقييد" ){
if( in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [الادمن](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح المتحركه بالتقييد
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["gifr"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح المتحركه بالتقييد" ){
if ($tc == 'group' | $tc == 'supergroup'){  
if( $status != 'creator' and $status != 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) ){
$add = $settings["information"]["added"];
if ($add == true) {
 bot('sendMessage',[
'chat_id'=>$chat_id,
'text'=>"
📡¦ هذا الامر يخص الادمنيه فقط  🚶
",'reply_to_message_id'=>$message_id,
]);
}
}
}
}
if($text== "قفل الصور بالتقييد" ){
if ($status == 'creator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المنشئ](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل الصور بالتقييد
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["photor"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل الصور بالتقييد" ){
if ($status == 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المشرف](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل الصور بالتقييد
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["photor"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل الصور بالتقييد" ){
if( in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المطور](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل الصور بالتقييد
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["photor"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل الصور بالتقييد" ){
if( in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المدير](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل الصور بالتقييد
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["photor"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل الصور بالتقييد" ){
if( in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [الادمن](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل الصور بالتقييد
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["photor"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل الصور بالتقييد" ){
if ($tc == 'group' | $tc == 'supergroup'){  
if( $status != 'creator' and $status != 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) ){
$add = $settings["information"]["added"];
if ($add == true) {
 bot('sendMessage',[
'chat_id'=>$chat_id,
'text'=>"
📡¦ هذا الامر يخص الادمنيه فقط  🚶
",'reply_to_message_id'=>$message_id,
]);
}
}
}
}
if($text== "فتح الصور بالتقييد" ){
if ($status == 'creator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المنشئ](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح الصور بالتقييد
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["photor"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح الصور بالتقييد" ){
if ($status == 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المشرف](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح الصور بالتقييد
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["photor"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح الصور بالتقييد" ){
if( in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المطور](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح الصور بالتقييد
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["photor"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح الصور بالتقييد" ){
if( in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المدير](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح الصور بالتقييد
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["photor"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح الصور بالتقييد" ){
if( in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [الادمن](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح الصور بالتقييد
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["photor"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح الصور بالتقييد" ){
if ($tc == 'group' | $tc == 'supergroup'){  
if( $status != 'creator' and $status != 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) ){
$add = $settings["information"]["added"];
if ($add == true) {
 bot('sendMessage',[
'chat_id'=>$chat_id,
'text'=>"
📡¦ هذا الامر يخص الادمنيه فقط  🚶
",'reply_to_message_id'=>$message_id,
]);
}
}
}
}
if($text== "قفل الفيديو بالتقييد" ){
if ($status == 'creator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المنشئ](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل الفيديو بالتقييد
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["videor"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل الفيديو بالتقييد" ){
if ($status == 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المشرف](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل الفيديو بالتقييد
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["videor"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل الفيديو بالتقييد" ){
if( in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المطور](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل الفيديو بالتقييد
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["videor"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل الفيديو بالتقييد" ){
if( in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المدير](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل الفيديو بالتقييد
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["videor"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل الفيديو بالتقييد" ){
if( in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [الادمن](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل الفيديو بالتقييد
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["videor"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل الفيديو بالتقييد" ){
if ($tc == 'group' | $tc == 'supergroup'){  
if( $status != 'creator' and $status != 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) ){
$add = $settings["information"]["added"];
if ($add == true) {
 bot('sendMessage',[
'chat_id'=>$chat_id,
'text'=>"
📡¦ هذا الامر يخص الادمنيه فقط  🚶
",'reply_to_message_id'=>$message_id,
]);
}
}
}
}
if($text== "فتح الفيديو بالتقييد" ){
if ($status == 'creator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المنشئ](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح الفيديو بالتقييد
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["videor"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح الفيديو بالتقييد" ){
if ($status == 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المشرف](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح الفيديو بالتقييد
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["videor"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح الفيديو بالتقييد" ){
if( in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المطور](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح الفيديو بالتقييد
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["videor"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح الفيديو بالتقييد" ){
if( in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المدير](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح الفيديو بالتقييد
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["videor"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح الفيديو بالتقييد" ){
if( in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [الادمن](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح الفيديو بالتقييد
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["videor"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح الفيديو بالتقييد" ){
if ($tc == 'group' | $tc == 'supergroup'){  
if( $status != 'creator' and $status != 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) ){
$add = $settings["information"]["added"];
if ($add == true) {
 bot('sendMessage',[
'chat_id'=>$chat_id,
'text'=>"
📡¦ هذا الامر يخص الادمنيه فقط  🚶
",'reply_to_message_id'=>$message_id,
]);
}
}
}
}
if($text== "تفعيل الترحيب" ){
if ($status == 'creator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المنشئ](tg://user?id=$from_id) 👷🏽
📡¦ تم تفعيل الترحيب
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["welcome"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "تفعيل الترحيب" ){
if ($status == 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المشرف](tg://user?id=$from_id) 👷🏽
📡¦ تم تفعيل الترحيب
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["welcome"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "تفعيل الترحيب" ){
if( in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المطور](tg://user?id=$from_id) 👷🏽
📡¦ تم تفعيل الترحيب
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["welcome"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "تفعيل الترحيب" ){
if( in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المدير](tg://user?id=$from_id) 👷🏽
📡¦ تم تفعيل الترحيب
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["welcome"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "تفعيل الترحيب" ){
if( in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [الادمن](tg://user?id=$from_id) 👷🏽
📡¦ تم تفعيل الترحيب
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["welcome"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "تفعيل الترحيب" ){
if ($tc == 'group' | $tc == 'supergroup'){  
if( $status != 'creator' and $status != 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) ){
$add = $settings["information"]["added"];
if ($add == true) {
 bot('sendMessage',[
'chat_id'=>$chat_id,
'text'=>"
📡¦ هذا الامر يخص الادمنيه فقط  🚶
",'reply_to_message_id'=>$message_id,
]);
}
}
}
}
if($text== "تعطيل الترحيب" ){
if ($status == 'creator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المنشئ](tg://user?id=$from_id) 👷🏽
📡¦ تم تعطيل الترحيب
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["welcome"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "تعطيل الترحيب" ){
if ($status == 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المشرف](tg://user?id=$from_id) 👷🏽
📡¦ تم تعطيل الترحيب
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["welcome"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "تعطيل الترحيب" ){
if( in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المطور](tg://user?id=$from_id) 👷🏽
📡¦ تم تعطيل الترحيب
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["welcome"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "تعطيل الترحيب" ){
if( in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المدير](tg://user?id=$from_id) 👷🏽
📡¦ تم تعطيل الترحيب
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["welcome"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "تعطيل الترحيب" ){
if( in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [الادمن](tg://user?id=$from_id) 👷🏽
📡¦ تم تعطيل الترحيب
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["welcome"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "تعطيل الترحيب" ){
if ($tc == 'group' | $tc == 'supergroup'){  
if( $status != 'creator' and $status != 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) ){
$add = $settings["information"]["added"];
if ($add == true) {
 bot('sendMessage',[
'chat_id'=>$chat_id,
'text'=>"
📡¦ هذا الامر يخص الادمنيه فقط  🚶
",'reply_to_message_id'=>$message_id,
]);
}
}
}
}
if($text== "فتح الرد" ){
if ($status == 'creator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المنشئ](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح الرد
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["reply"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح الرد" ){
if ($status == 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المشرف](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح الرد
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["reply"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح الرد" ){
if( in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المطور](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل االصور
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["reply"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح الرد" ){
if( in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المدير](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح الرد
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["reply"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح الرد" ){
if( in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [الادمن](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح الرد
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["reply"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح الرد" ){
if ($tc == 'group' | $tc == 'supergroup'){  
if( $status != 'creator' and $status != 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) ){
$add = $settings["information"]["added"];
if ($add == true) {
 bot('sendMessage',[
'chat_id'=>$chat_id,
'text'=>"
📡¦ هذا الامر يخص الادمنيه فقط  🚶
",'reply_to_message_id'=>$message_id,
]);
}
}
}
}
if($text == "لقبي"){
    // مصفوفة الألقاب العراقية الترفة (متباعدة وفخمة)
    $titles = [
        "‏صـڪـار الـلـيـل 🦅", "‏تـرف الـبـصـرة 💎", "‏هـيـبـة بـغـداد 👑", "‏أمـيـر الـتـواضـع ✨",
        "‏ذيـب الـمـيـدان 🐺", "‏عـسل الـڪـروب 🍯", "‏شـيـخ الـشـبـاب 👔", "‏نـزاڪـة الـحـلـة 🌸",
        "‏قـائـد الإمـبـراطـوريـة 🦁", "‏سـلـطـان الـغـرام ❤️", "‏ضـوه عـيـونـي ✨", "‏ڪـيـڪـة الـسـهـرة 🍰",
        "‏أسـد الـغـابـة 🦁", "‏صـقـر الـعـرب 🦅", "‏نـور الـمـمـلـڪـة 🌕", "‏مـلـڪ الأنـاقـة 👑",
        "‏بـاشـا الـعـراق 🇮🇶", "‏ذهـب مـصـفـى 💎", "‏عـنـيـد الـطبـاع 🔥", "‏حـلـو الـطـلـة 😍",
        "‏خـيـال الأصـايـل 🐎", "‏نـبـع الـحـنـان 🌹", "‏زعـيـم الـڪـروب 🛡️", "‏قـمـر ١٤ 🌕",
        "‏شـمـس الـنـهـار ☀️", "‏صـاحـب الـفـضـل ✨", "‏تـاج الـرأس 👑", "‏عـزيـز الـنـفـس 💎",
        "‏سـيـف الـمـرجـلـة 🗡️", "‏نـادر الـوصـوف 🌟", "‏طـيـر الـسـعـد 🕊️", "‏هـيـبـة الـديـوان 🦁",
        "‏صـڪـار الـعـارات 🔥", "‏نـقـي الـقـلـب ❤️", "‏بـطـل الـمـنـطـقـة 🏆", "‏عـطـر الـهـيـل 🌿",
        "‏نـبـض الإمـبـراطـوريـة ✨", "‏فـارس الأحـلام 🤵", "‏لـؤلـؤ الـبـحـر 💎", "‏نـمـر الـشـمـال 🐆",
        "‏سـبـع الـسـبـاع 🦁", "‏شـمـعـة الـجـلـسـة 🕯️", "‏فـديـت الـهـيـبـة 😍", "‏حـاتـم الـزمـان 💎",
        "‏بـركـان الـغـضـب 🔥", "‏هـدوء الـلـيـل 🌙", "‏فـرحـة الـعـمـر 🎉", "‏مـعدل الـمـعـادن 👑",
        "‏طـالـع تـفـلـيـش 🔥", "‏إمـبـراطـور الـذوق ✨"
    ];

    $my_title = $titles[array_rand($titles)];
    $user_name = $message->from->first_name;

    bot('sendMessage',[
        'chat_id' => $chat_id,
        'text' => "‏لـقـبـڪ الـجـديـد يـا يـا [$user_name] هـو :\n\n  ( $my_title )  ",
        'reply_to_message_id' => $message_id,
        'parse_mode' => "Markdown"
    ]);
}

if($text== "فتح الرد" ){
if ($status == 'creator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المنشئ](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح الرد
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["reply"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح الرد" ){
if ($status == 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المشرف](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح الرد
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["reply"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح الرد" ){
if( in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المطور](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح الرد
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["reply"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح الرد" ){
if( in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المدير](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح الرد
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["reply"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح الرد" ){
if( in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [الادمن](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح الرد
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["reply"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح الرد" ){
if ($tc == 'group' | $tc == 'supergroup'){  
if( $status != 'creator' and $status != 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) ){
$add = $settings["information"]["added"];
if ($add == true) {
 bot('sendMessage',[
'chat_id'=>$chat_id,
'text'=>"
📡¦ هذا الامر يخص الادمنيه فقط  🚶
",'reply_to_message_id'=>$message_id,
]);
}
}
}
}
if($text== "تفعيل الايدي" ){
if ($status == 'creator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المنشئ](tg://user?id=$from_id) 👷🏽
📡¦ تم تفعيل الايدي
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["iduser"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "تفعيل الايدي" ){
if ($status == 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المشرف](tg://user?id=$from_id) 👷🏽
📡¦ تم تفعيل الايدي
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["iduser"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "تفعيل الايدي" ){
if( in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المطور](tg://user?id=$from_id) 👷🏽
📡¦ تم تفعيل الايدي
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["iduser"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "تفعيل الايدي" ){
if( in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المدير](tg://user?id=$from_id) 👷🏽
📡¦ تم تفعيل الايدي
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["iduser"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "تفعيل الايدي" ){
if( in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [الادمن](tg://user?id=$from_id) 👷🏽
📡¦ تم تفعيل الايدي
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["iduser"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "تفعيل الايدي" ){
if ($tc == 'group' | $tc == 'supergroup'){  
if( $status != 'creator' and $status != 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) ){
$add = $settings["information"]["added"];
if ($add == true) {
 bot('sendMessage',[
'chat_id'=>$chat_id,
'text'=>"
📡¦ هذا الامر يخص الادمنيه فقط  🚶
",'reply_to_message_id'=>$message_id,
]);
}
}
}
}
if($text== "تعطيل الايدي" ){
if ($status == 'creator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المنشئ](tg://user?id=$from_id) 👷🏽
📡¦ تم تعطيل الايدي
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["iduser"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "تعطيل الايدي" ){
if ($status == 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المشرف](tg://user?id=$from_id) 👷🏽
📡¦ تم تعطيل الايدي
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["iduser"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "تعطيل الايدي" ){
if( in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المطور](tg://user?id=$from_id) 👷🏽
📡¦ تم تعطيل الايدي
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["iduser"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "تعطيل الايدي" ){
if( in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المدير](tg://user?id=$from_id) 👷🏽
📡¦ تم تعطيل الايدي
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["iduser"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "تعطيل الايدي" ){
if( in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [الادمن](tg://user?id=$from_id) 👷🏽
📡¦ تم تعطيل الايدي
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["iduser"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "تعطيل الايدي" ){
if ($tc == 'group' | $tc == 'supergroup'){  
if( $status != 'creator' and $status != 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) ){
$add = $settings["information"]["added"];
if ($add == true) {
 bot('sendMessage',[
'chat_id'=>$chat_id,
'text'=>"
📡¦ هذا الامر يخص الادمنيه فقط  🚶
",'reply_to_message_id'=>$message_id,
]);
}
}
}
}
if($text== "قفل الانجليزية" ){
if ($status == 'creator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المنشئ](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل الانجليزية
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["en"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل الانجليزية" ){
if ($status == 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المشرف](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل الانجليزية
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["en"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل الانجليزية" ){
if( in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المطور](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل الانجليزية
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["en"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل الانجليزية" ){
if( in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المدير](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل الانجليزية
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["en"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل الانجليزية" ){
if( in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [الادمن](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل الانجليزية
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["en"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل الانجليزية" ){
if ($tc == 'group' | $tc == 'supergroup'){  
if( $status != 'creator' and $status != 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) ){
$add = $settings["information"]["added"];
if ($add == true) {
 bot('sendMessage',[
'chat_id'=>$chat_id,
'text'=>"
📡¦ هذا الامر يخص الادمنيه فقط  🚶
",'reply_to_message_id'=>$message_id,
]);
}
}
}
}
if($text== "فتح الانجليزية" ){
if ($status == 'creator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المنشئ](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح الانجليزية
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["en"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح الانجليزية" ){
if ($status == 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المشرف](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح الانجليزية
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["en"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح الانجليزية" ){
if( in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المطور](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح الانجليزية
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["en"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح الانجليزية" ){
if( in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المدير](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح الانجليزية
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["en"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح الانجليزية" ){
if( in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [الادمن](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح الانجليزية
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["en"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح الانجليزية" ){
if ($tc == 'group' | $tc == 'supergroup'){  
if( $status != 'creator' and $status != 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) ){
$add = $settings["information"]["added"];
if ($add == true) {
 bot('sendMessage',[
'chat_id'=>$chat_id,
'text'=>"
📡¦ هذا الامر يخص الادمنيه فقط  🚶
",'reply_to_message_id'=>$message_id,
]);
}
}
}
}
if($text== "قفل العربية" ){
if ($status == 'creator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المنشئ](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل العربية
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["ar"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل العربية" ){
if ($status == 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المشرف](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل العربية
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["ar"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل العربية" ){
if( in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المطور](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل العربية
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["ar"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل العربية" ){
if( in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المدير](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل العربية
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["ar"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل العربية" ){
if( in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [الادمن](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل العربية
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["ar"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل العربية" ){
if ($tc == 'group' | $tc == 'supergroup'){  
if( $status != 'creator' and $status != 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) ){
$add = $settings["information"]["added"];
if ($add == true) {
 bot('sendMessage',[
'chat_id'=>$chat_id,
'text'=>"
📡¦ هذا الامر يخص الادمنيه فقط  🚶
",'reply_to_message_id'=>$message_id,
]);
}
}
}
}
if($text== "فتح العربية" ){
if ($status == 'creator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المنشئ](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح العربية
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["ar"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح العربية" ){
if ($status == 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المشرف](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح العربية
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["ar"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح العربية" ){
if( in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المطور](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح العربية
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["ar"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح العربية" ){
if( in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المدير](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح العربية
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["ar"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح العربية" ){
if( in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [الادمن](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح العربية
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["ar"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح العربية" ){
if ($tc == 'group' | $tc == 'supergroup'){  
if( $status != 'creator' and $status != 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) ){
$add = $settings["information"]["added"];
if ($add == true) {
 bot('sendMessage',[
'chat_id'=>$chat_id,
'text'=>"
📡¦ هذا الامر يخص الادمنيه فقط  🚶
",'reply_to_message_id'=>$message_id,
]);
}
}
}
}
if($text== "قفل المواقع" ){
if ($status == 'creator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المنشئ](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل المواقع
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["location"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل المواقع" ){
if ($status == 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المشرف](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل المواقع
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["location"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل المواقع" ){
if( in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المطور](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل المواقع
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["location"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل المواقع" ){
if( in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المدير](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل المواقع
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["location"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل المواقع" ){
if( in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [الادمن](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل المواقع
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["location"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل المواقع" ){
if ($tc == 'group' | $tc == 'supergroup'){  
if( $status != 'creator' and $status != 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) ){
$add = $settings["information"]["added"];
if ($add == true) {
 bot('sendMessage',[
'chat_id'=>$chat_id,
'text'=>"
📡¦ هذا الامر يخص الادمنيه فقط  🚶
",'reply_to_message_id'=>$message_id,
]);
}
}
}
}
if($text== "فتح المواقع" ){
if ($status == 'creator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المنشئ](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح المواقع
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["location"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح المواقع" ){
if ($status == 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المشرف](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح المواقع
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["location"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح المواقع" ){
if( in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المطور](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح المواقع
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["location"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح المواقع" ){
if( in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المدير](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح المواقع
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["location"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح المواقع" ){
if( in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [الادمن](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح المواقع
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["location"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح المواقع" ){
if ($tc == 'group' | $tc == 'supergroup'){  
if( $status != 'creator' and $status != 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) ){
$add = $settings["information"]["added"];
if ($add == true) {
 bot('sendMessage',[
'chat_id'=>$chat_id,
'text'=>"
📡¦ هذا الامر يخص الادمنيه فقط  🚶
",'reply_to_message_id'=>$message_id,
]);
}
}
}
}
if($text== "قفل الملفات" ){
if ($status == 'creator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المنشئ](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل الملفات
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["document"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل الملفات" ){
if ($status == 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المشرف](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل الملفات
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["document"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل الملفات" ){
if( in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المطور](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل الملفات
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["document"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل الملفات" ){
if( in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المدير](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل الملفات
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["document"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل الملفات" ){
if( in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [الادمن](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل الملفات
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["document"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل الملفات" ){
if ($tc == 'group' | $tc == 'supergroup'){  
if( $status != 'creator' and $status != 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) ){
$add = $settings["information"]["added"];
if ($add == true) {
 bot('sendMessage',[
'chat_id'=>$chat_id,
'text'=>"
📡¦ هذا الامر يخص الادمنيه فقط  🚶
",'reply_to_message_id'=>$message_id,
]);
}
}
}
}
if($text== "فتح الملفات" ){
if ($status == 'creator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المنشئ](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح الملفات
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["document"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح الملفات" ){
if ($status == 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المشرف](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح الملفات
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["document"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح الملفات" ){
if( in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المطور](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح الملفات
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["document"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح الملفات" ){
if( in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المدير](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح الملفات
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["document"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح الملفات" ){
if( in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [الادمن](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح الملفات
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["document"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح الملفات" ){
if ($tc == 'group' | $tc == 'supergroup'){  
if( $status != 'creator' and $status != 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) ){
$add = $settings["information"]["added"];
if ($add == true) {
 bot('sendMessage',[
'chat_id'=>$chat_id,
'text'=>"
📡¦ هذا الامر يخص الادمنيه فقط  🚶
",'reply_to_message_id'=>$message_id,
]);
}
}
}
}
if($text== "قفل الموسيقى" ){
if ($status == 'creator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المنشئ](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل الموسيقى
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["audio"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل الموسيقى" ){
if ($status == 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المشرف](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل الموسيقى
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["audio"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل الموسيقى" ){
if( in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المطور](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل الموسيقى
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["audio"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل الموسيقى" ){
if( in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المدير](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل الموسيقى
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["audio"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل الموسيقى" ){
if( in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [الادمن](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل الموسيقى
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["audio"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل الموسيقى" ){
if ($tc == 'group' | $tc == 'supergroup'){  
if( $status != 'creator' and $status != 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) ){
$add = $settings["information"]["added"];
if ($add == true) {
 bot('sendMessage',[
'chat_id'=>$chat_id,
'text'=>"
📡¦ هذا الامر يخص الادمنيه فقط  🚶
",'reply_to_message_id'=>$message_id,
]);
}
}
}
}
if($text== "فتح الموسيقى" ){
if ($status == 'creator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المنشئ](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح الموسيقى
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["audio"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح الموسيقى" ){
if ($status == 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المشرف](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح الموسيقى
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["audio"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح الموسيقى" ){
if( in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المطور](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح الموسيقى
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["audio"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح الموسيقى" ){
if( in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المدير](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح الموسيقى
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["audio"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح الموسيقى" ){
if( in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [الادمن](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح الموسيقى
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["audio"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح الموسيقى" ){
if ($tc == 'group' | $tc == 'supergroup'){  
if( $status != 'creator' and $status != 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) ){
$add = $settings["information"]["added"];
if ($add == true) {
 bot('sendMessage',[
'chat_id'=>$chat_id,
'text'=>"
📡¦ هذا الامر يخص الادمنيه فقط  🚶
",'reply_to_message_id'=>$message_id,
]);
}
}
}
}
if($text== "قفل الاشعارات" ){
if ($status == 'creator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المنشئ](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل الاشعارات
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["tgservic"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل الاشعارات" ){
if ($status == 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المشرف](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل الاشعارات
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["tgservic"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل الاشعارات" ){
if( in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المطور](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل الاشعارات
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["tgservic"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل الاشعارات" ){
if( in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المدير](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل الاشعارات
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["tgservic"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل الاشعارات" ){
if( in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [الادمن](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل الاشعارات
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["tgservic"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل الاشعارات" ){
if ($tc == 'group' | $tc == 'supergroup'){  
if( $status != 'creator' and $status != 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) ){
$add = $settings["information"]["added"];
if ($add == true) {
 bot('sendMessage',[
'chat_id'=>$chat_id,
'text'=>"
📡¦ هذا الامر يخص الادمنيه فقط  🚶
",'reply_to_message_id'=>$message_id,
]);
}
}
}
}
if($text== "فتح الاشعارات" ){
if ($status == 'creator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المنشئ](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح الاشعارات
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["tgservic"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح الاشعارات" ){
if ($status == 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المشرف](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح الاشعارات
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["tgservic"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح الاشعارات" ){
if( in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المطور](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح الاشعارات
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["tgservic"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح الاشعارات" ){
if( in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المدير](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح الاشعارات
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["tgservic"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح الاشعارات" ){
if( in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [الادمن](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح الاشعارات
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["tgservic"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح الاشعارات" ){
if ($tc == 'group' | $tc == 'supergroup'){  
if( $status != 'creator' and $status != 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) ){
$add = $settings["information"]["added"];
if ($add == true) {
 bot('sendMessage',[
'chat_id'=>$chat_id,
'text'=>"
📡¦ هذا الامر يخص الادمنيه فقط  🚶
",'reply_to_message_id'=>$message_id,
]);
}
}
}
}
if($text== "قفل بصمة الفيديو" ){
if ($status == 'creator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المنشئ](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل بصمة الفيديو
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["video_msg"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل بصمة الفيديو" ){
if ($status == 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المشرف](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل بصمة الفيديو
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["video_msg"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل بصمة الفيديو" ){
if( in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المطور](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل بصمة الفيديو
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["video_msg"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل بصمة الفيديو" ){
if( in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المدير](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل بصمة الفيديو
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["video_msg"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل بصمة الفيديو" ){
if( in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [الادمن](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل بصمة الفيديو
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["video_msg"]="مقفول️";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل بصمة الفيديو" ){
if ($tc == 'group' | $tc == 'supergroup'){  
if( $status != 'creator' and $status != 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) ){
$add = $settings["information"]["added"];
if ($add == true) {
 bot('sendMessage',[
'chat_id'=>$chat_id,
'text'=>"
📡¦ هذا الامر يخص الادمنيه فقط  🚶
",'reply_to_message_id'=>$message_id,
]);
}
}
}
}
if($text== "فتح بصمة الفيديو" ){
if ($status == 'creator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المنشئ](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح بصمة الفيديو
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["video_msg"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح بصمة الفيديو" ){
if ($status == 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المشرف](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح بصمة الفيديو
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["video_msg"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح بصمة الفيديو" ){
if( in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المطور](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح بصمة الفيديو
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["video_msg"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح بصمة الفيديو" ){
if( in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المدير](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح بصمة الفيديو
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["video_msg"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح بصمة الفيديو" ){
if( in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [الادمن](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح بصمة الفيديو
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["video_msg"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح بصمة الفيديو" ){
if ($tc == 'group' | $tc == 'supergroup'){  
if( $status != 'creator' and $status != 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) ){
$add = $settings["information"]["added"];
if ($add == true) {
 bot('sendMessage',[
'chat_id'=>$chat_id,
'text'=>"
📡¦ هذا الامر يخص الادمنيه فقط  🚶
",'reply_to_message_id'=>$message_id,
]);
}
}
}
}
if($text== "قفل الكل" ){
if ($status == 'creator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المنشئ](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل الكل
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["link"]="مقفول️";
	$settings["lock"]["username"]="مقفول️";
	$settings["lock"]["bot"]="مقفول️";
	$settings["lock"]["forward"]="مقفول️";
	$settings["lock"]["tgservices"]="مقفول️";
	$settings["lock"]["contact"]="مقفول️";
    $settings = json_encode($settings,true);
    file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل الكل" ){
if ($status == 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المشرف](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل الكل
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["link"]="مقفول️";
	$settings["lock"]["username"]="مقفول️";
	$settings["lock"]["bot"]="مقفول️";
	$settings["lock"]["forward"]="مقفول️";
	$settings["lock"]["tgservices"]="مقفول️";
	$settings["lock"]["contact"]="مقفول️";
    $settings = json_encode($settings,true);
    file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل الكل" ){
if( in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المطور](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل الكل
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["link"]="مقفول️";
	$settings["lock"]["username"]="مقفول️";
	$settings["lock"]["bot"]="مقفول️";
	$settings["lock"]["forward"]="مقفول️";
	$settings["lock"]["tgservices"]="مقفول️";
	$settings["lock"]["contact"]="مقفول️";
    $settings = json_encode($settings,true);
    file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "قفل الكل" ){
if( in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المدير](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل الكل
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["link"]="مقفول️";
	$settings["lock"]["username"]="مقفول️";
	$settings["lock"]["bot"]="مقفول️";
	$settings["lock"]["forward"]="مقفول️";
	$settings["lock"]["tgservices"]="مقفول️";
	$settings["lock"]["contact"]="مقفول️";
    $settings = json_encode($settings,true);
    file_put_contents("data/$chat_id.json",$settings);
}
}
}


if($text== "قفل الكل" ){
if( in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [الادمن](tg://user?id=$from_id) 👷🏽
📡¦ تم قفل الكل
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["link"]="مقفول️";
	$settings["lock"]["username"]="مقفول️";
	$settings["lock"]["bot"]="مقفول️";
	$settings["lock"]["forward"]="مقفول️";
	$settings["lock"]["tgservices"]="مقفول️";
	$settings["lock"]["contact"]="مقفول️";
    $settings = json_encode($settings,true);
    file_put_contents("data/$chat_id.json",$settings);

}
}
}
if($text== "قفل الكل" ){
if ($tc == 'group' | $tc == 'supergroup'){  
if( $status != 'creator' and $status != 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) ){
$add = $settings["information"]["added"];
if ($add == true) {
 bot('sendMessage',[
'chat_id'=>$chat_id,
'text'=>"
📡¦ هذا الامر يخص الادمنيه فقط  🚶
",'reply_to_message_id'=>$message_id,
]);
}
}
}
}
if($text== "فتح الكل" ){
if ($status == 'creator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المنشئ](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح الكل
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);

$settings["lock"]["link"]="مفتوح";
	$settings["lock"]["username"]="مفتوح";
	$settings["lock"]["bot"]="مفتوح";
	$settings["lock"]["forward"]="مفتوح";
	$settings["lock"]["tgservices"]="مفتوح";
	$settings["lock"]["contact"]="مفتوح";
    $settings = json_encode($settings,true);
    file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح الكل" ){
if ($status == 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المشرف](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح الكل
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["link"]="مفتوح";
	$settings["lock"]["username"]="مفتوح";
	$settings["lock"]["bot"]="مفتوح";
	$settings["lock"]["forward"]="مفتوح";
	$settings["lock"]["tgservices"]="مفتوح";
	$settings["lock"]["contact"]="مفتوح";
    $settings = json_encode($settings,true);
    file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح الكل" ){
if( in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المطور](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح الكل
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["link"]="مفتوح";
	$settings["lock"]["username"]="مفتوح";
	$settings["lock"]["bot"]="مفتوح";
	$settings["lock"]["forward"]="مفتوح";
	$settings["lock"]["tgservices"]="مفتوح";
	$settings["lock"]["contact"]="مفتوح";
    $settings = json_encode($settings,true);
    file_put_contents("data/$chat_id.json",$settings);
}
}
}
/*==============================
=        قائمة الأشعار والخواطر   =
==============================*/
$poet_quotes = [
    "أحياناً تحزن على مشاعرك مو على الأشخاص .",
    "العاصفة لا تكسر الجبال، بل تكشف قوتها .",
    "بعض الطرق يجب أن تسلكها بمفردك ، لا عائلة ولا أصدقاء ، أنت فقط .",
    "دائما يحاربون المنفرد، لأنه لم يستطع أحد أن يضمه إلى القطيع.",
    "أراكم بوضوح، ولكن لم يحن ، دوركم.",
    "بضعفي أتحمل ما لا تطيقونه بقوتكم .",
    "في مثل يقول: عدو صريح ولا صديق بوجهين .",
    "لا شئ يكسرنا نحن علي إستعداد لخسارة الجميع.",
    "ركز على نفسك لقد فعلت ما يكفي للجميع .",
    "كل النَّاسِ خَيْرٌ وَبَرَكَةُ إلا ، قليل الأصل ونَاكِرُ العِشْرَةِ",
    "وعندما انتهت المصلحة صمتت الهواتف.",
    "بكل رضى الحمد لله على كل شيء 🐱",
    "وأحسّك في ليالي البرد شمسًا في دمي .",
    "‏وحدنا نُصغي لما في الروحِ من عبثٍ",
    "أنا لا أحبك فقط، أنا ضائع فيك..",
    "منذُ أن رأيتكِ وكُلي يغرق بك .",
    "تعشُق الورد ولا تعلمُ هيَ الورد ذاتهُ .",
    "هَو أصدق حُب حبيته بِـ حياتي. •",
    "حبيبان دائماً وأصدقاء في كل اللحظات .",
    "وتبقَى انتَ ذاك المُختلف النادر بعَيني .",
    "أغُص برّيحتك ما گمت أغُص بالزاد .",
    "وحينما كان العُمر مُرًا ، آنستِهُ أنتِ .",
    "الدُنيا كلها تشوفك انسان عادي وانتَ عندي الدُنيا كلها .",
    "مالهُم بعَيوني مُكان انتِ عَيوني گلها .",
    "المخَليها عَلى الله، راح يشوف كل الخيّر .",
    "ربي أختر لي ماتراه خيراً لي 😀.",
    "فعسى أن تكرهوا شَيْنَا وَيَجْعَلَ اللَّهُ فِيهِ خَيْرًا كَثِيرًا",
    "اللهُمَ عُونكَ إذا باتَ كُل شَيء ثقَيل علي",
    "وإن تاهت بِنا الطرق كن معنا يا الله 🩷",
    "و لعل الله أرادها أن تأتي متأخرة فتأتي أعظم و أكرم",
    "الحمد لله على ما مضى و الحمد لله على ما سيأتي",
    "اللهم سخرلى الخير حيث كان ثم ارضنی به.",
    "مهما كنت حزيناً ، قل الحمد لله",
    "و صبر جميل ، ثُم ثم عوض من الله يرضيك",
    "- ‏الحمدلله الذي أبعدنا عن دروب لا تليق بنا .",
    "اللهم إنا نسألُكَ جنةٌ تُنسينا تعب الدنيا.",
    "يأت بها الله حتى وإن كانت مستحيلة 👼",
    "اللهم قدر جميل وخبر جميل ودعوه مستجابه",
    "أصنع النفسك أيام جميلة ولا تنتظر جمال أيامك من أحد",
    "أحيانًا محاولة إثبات أنَّكَ الأَفضل تعتبر إهانة .",
    "ثُمَّ يَرزُقُكَ جَبرَهُ في عِزِّ اِنكسارِكَ",
    "الصدف لاتحدث بل الله يستجيب .",
    "قُل للرياح تأتي كيفما شائت فما عادت سفننا تشتهي شيئاً",
    "ياحَبيبي الدنيا بردت ، مِثلك بأخر لِقاء .",
    "أنا تَمنيتك أنتَ وكُلشي مَاريد ..",
    "أنتَ مَحد سوه مثلك دللتنيِ وتَعبتنيِ !",
    "حايط طين كلما تمطر أبچيلك .",
    "عادي اتعب وياك بس ما خليك الغيري .",
    "لا سَنة جديدة ولا قديمة أنتِ كُل سِنيني .",
    "بس المحترك يفهم حجي الدخان .",
    "أضوِي بَصوُرتچ لُو صاَر ضلمة البَيت .",
    "أعاند روحي ما اشتاگ واني الشوگ كاتلني",
    "اليحب من صدك يلغي الزعل بشلونك.",
    "منْ تَرَكَ أَمْرَهُ لِلهِ أَعْطَاهُ اللَّهُ فَوْقَ مَا يَتَمَنَّاهُ",
    "أشيل حزنچ بگلبي بس عيونـچ لاتذبَل",
    "كانت امرأة تُغني عن كُل النِساء .",
    "وَ أعظمُ الحُبِّ ، حُبُّ الرُّوحِ لِلرُّوحِ",
    "- ومِثل عيونِچ ﭑلحِلوات ما شايف .",
    "وليس هُناك شيئاً يشبه جمَال مبسمك",
    "المزاجية تقتل الإنسان في ثواني .",
    "أشعُر بوحدة عَميقة ، كأنني الفضَاء",
    "سَـيُديم الله علاقتك بمن هو خير لك .",
    "‏يارب الأشياء الحلوه تظل بطريقنا للأبد",
    "كلشي بالدِنيا عگب عَيونك غريب .",
    "صباح الخير 💓 ‏﴿ وَتَوَكَّل عَلَى الحَيِّ الَّذي لا يَموتُ ﴾",
    "امنحني يالله القدرة على روية الرحمة❤️",
    "تَعويضَات الله مُذهِلة وَتَستحقُّ الإِنتِظار .",
    "چنت أشوفَك الصَح الوَحيد بهوسَة سِنيني .",
    "- قَلبي لا يمثلني ، أنا أكثر صَّلابة مِنْ ذَلِك !",
    "أريد أن أكونَ قريباً منكَ كثيراً بـ مسافة لاتسمَح بمرور شعرة.",
    "‏لا تعاتب أحد، العتب يعطيه قيمة .",
    "بعدَك بالگلب رغم الخلافات .",
    "وَالدَمعُ عَونٌ لمَّن ضَاقت به الحِيلُ .",
    "فَاسْتَمِعْ دُعائِي وَلا تَقطَعْ رَجَائِي .",
    "يزهرُ الإنسَان مع الشَخص الصَح .",
    "تِغيب ومن ترد بارد مثل عذرِك ."
];

/*==============================
=        عرض قسم الأشعار        =
==============================*/
if ($text === "📝 أشعار") {

    $quote = $poet_quotes[array_rand($poet_quotes)];

    // حفظ النص الأخير للنشر
    file_put_contents("last_poet_$chat_id.txt", $quote);

    bot("sendMessage", [
        "chat_id" => $chat_id,
        "text" => "📝 **أشعار**\n⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n\n$quote\n\n⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯",
        "parse_mode" => "Markdown"
    ]);
    exit;
}
/*==============================
=        قائمة عبارات الحب       =
==============================*/
$love_quotes = [
    "ضحكتها تزرع الورد بكل حّي وديره .",
    "‏كان الوعد نبقَى لبعَض شلي إختَلف.",
    "ادركت أن حبي لك فوق كل شيء",
    "فيَ بعضَ الأحيانْ تحبَ مدينة بأكملهاَ فقطّ بسبب َشخص.",
    "سارحٍ فكري معك ياعذاب المهتـّوي .",
    "ودعت من يصعـّب عليه وداعه",
    "ستبقى دائماً شيئاً مختلف عن الجميع.",
    "آه من ليلةٍ هبايبها تذكرني وأنا ماودي .",
    "أودّك ‏و أود كل شيء ‏يجمعنا معًا.",
    "غَزال فاق بِحُسنها كل الخَلايق",
    "لي قلبّ يحبك .. ذاق مرّك ولا تاب .",
    "جميلة أنت كموسيقى عزفت بليلة ماطرة",
    "ومينً يقدرَ ينسينيِ ‏سواليفَها وضحكتهاّ.",
    "أنا لأجل عينه عفت ألف مخلوق .",
    "‏العيدَ فرحهُ وانا بدونكِ فرحتي َما تكملُ",
    "كالورد إن لم تكُن هي الورد نفسه.",
    "لها مبسم يُستحال للعين نسّيانه .",
    "‏عشقٍ عفيفٍ في ضلوعي مخبّيه .",
    "أقاومَ الوقتُ بدونك بِشكل يهلك قلبي.",
    "‏نثرت شعرها الطويل و تباهّت بجمالها .",
    "هنيئاً للريآح التي تُدآعب شَعرها.",
    "‏خوفاً من فقدانه فقدت نفسي .",
    "‏شعور الشوق يتكاثر بالدقيقه ألففف مره",
    "قربك لو يسبب لي مليون وجع انا ابيك.",
    "‏يدهّــا تَضخُّ وردًا مِن فرطِ رقَّتِــهَا.",
    "‏أنا ودي أودع حياتيّ ولا أودعك .",
    "امرأة بقوام قصيدة لايقرأها غير الفصيح",
    "عسى الله يلهي كل عيـن ودها فيك .",
    "أنثى من الدلال والغنجّ .",
    "يا إمرأة رموشها أشدُّ جَمالاً مِن غَزل الشِعر",
    "ولكِ في قلبي مكان،لا يستقر فيه غيركِ.",
    "أهيم حباً ولا يوجد غيرك بقلبي.",
    "وانا لأجله تجنّبت من العرب واجد .",
    "مرحبا ، يا أول خجل قلبي وصمته واعترافه",
    "‏الورد في يدكِ والحدائق صارت في قلبي .",
    "جعلتك في وداعة الله وين ما وجهّت",
    "‏بين القمر و الغيم ترسم وصـوفك",
    "حتى ليالي الشتاء جابت طواريك",
    "ذات جمال ودلال وحسن مُلفت للنظر .",
    "ياحظكم فيّه دامكم تشِوفونه.",
    "باهيّة في حسنها وبكل وصوفها فارقة .",
    "‏‌سَيظّلُ طيفِي عالقً بِكُل ماهوْ حُولكَ .",
    "يا مُذهلة الليالي والأيام ، يا أرقّ مِن الورد .",
    "أنتِ فقط من يُلفت إنتباه قلبي دائمًا.",
    "يَا شخْصًا أرى النُّور فِيه",
    "أنتِ الصدفه الي غيرت حياتي للأفضل",
    "غارق بك مُتناسي هذا العالم بأكمِله .",
    "لن تُشفى من امرأة لمست عقلك.",
    "بَعض الصِدف شعورها يبقى عمر .",
    "انها اميرة النساء واغنية المساء",
    "بكل مافيني من حُب حبيتك",
    "كل عامُ وضحكتك تمطر الدنيا فرح.♥️",
    "تبقى الغيرة أكثر شيء يبعثر نبضات قلبي",
    "لا شيءِ يشبهِ قلبها جميلة بكُل شي.",
    "سبحان من ميزها عن كل مخلوق.",
    "أخافُ العمر دُونه وهو الحيّاةُ بقلبي.",
    "والله إن قلبّي عند غيرك ما يوَالف .",
    "ليتك تمر العين كثر ما تمر البال .",
    "سيدة سادات الحسن والمبسم المثير",
    "حتى القمر من جمالها خجلان .",
    "تناسى كِل شي مركون بخاطرك ، وتقهوَى .",
    "العلاقات أخلاق، حتى لو انتهت.",
    "على البال لو ما به مراسيل .",
    "سيستجيب لانه قادر على عوضك.",
    "اللهُم اجبر خاطري جبراً انت وليهُ",
    "ثم يرزقك جبرهُ في عزّ إنكسارك",
    "وجودك يجعل كُل شيء بخير حتى أنا.",
    "الأماكن كلها مشتاقة لك .",
    "ماجازليّ غيره ولا ابي له بديل .",
    "مُدللة و يليق فيها . . الدلال",
    "انتيِ الماضي والحاضر والمستقبل.",
    "زاهيّة ، وباهيّة ، وفاتّنة ، ومُهلكة لقلبي .",
    "حتى أطباعه الثقيّله .. ماخذه قلبي .",
    "زادها الله فوق القبّول قبول.",
    "من حِسنها الحِسن إنخرس .",
    "يقول أحبك ، و يفعلها .",
    "البْال أنتِ و غيرك عبُور .",
    "هني من يشوفك في صباح العيد",
    "انت كل اعيادي وسنيني والعمر .",
    "ما هيَ إلاّ وَردٌ عَلى وُرد .",
    "فيني خوف احد ياخذك مني وانا احبك .",
    "يا أجمل شيء في عمري لقيته ."
];

/*==============================
=        عرض قسم الحب          =
==============================*/
if ($text === "❤️ عبارات حب") {

    $quote = $love_quotes[array_rand($love_quotes)];

    // حفظ النص الأخير للنشر
    file_put_contents("last_love_$chat_id.txt", $quote);

    bot("sendMessage", [
        "chat_id" => $chat_id,
        "text" => "❤️ **عبارات حب**\n⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n\n$quote\n\n⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯",
        "parse_mode" => "Markdown"
    ]);
    exit;
}
/*==============================
=         قائمة النكت          =
==============================*/
$jokes_quotes = [
    "شخص يفتح الثلاجة ليجد فقط ضوء، يتساءل 'هل أكلت كل شيء؟'",
    "قطة تحاول القفز على طاولة وفشلها بطريقة كوميدية.",
    "شخص يكتب واجباته على الكمبيوتر لكن كل مرة الكمبيوتر يعلق.",
    "طفل يصرخ لأن العصير وقع على الأرض.",
    "أحدهم يشتري حذاء جديد ويكتشف أنه صغير جدًا بعد أسبوع.",
    "صديق يحاول إخفاء أنه أكل كل البيتزا.",
    "شخص يحاول فتح باب بإصبعين فقط.",
    "قطة تنظر للمرآة وتخاف من نفسها.",
    "شخص يركض للحافلة ولكنها تغادر قبل وصوله بثوانٍ.",
    "شخص ينام على المكتب ويستيقظ ليجد أوراقه متناثرة.",
    "والد ينادي على أطفاله ويجدهم مختبئين في الغرفة.",
    "طفل يضحك على نفسه أثناء الرسم.",
    "قطة تحاول القفز على نافذة مغلقة.",
    "شخص يأكل أيس كريم بسرعة قبل أن يذوب، لكنه ينسى لسانه.",
    "شخص يظن أن لديه يوم عطلة لكنه يعمل.",
    "صديق يحاول تصوير السيلفي وفقد الهاتف في المسبح.",
    "أحدهم يشتري نظارة شمسية ويكتشف أنها للعبة فيديو.",
    "طفل يختبئ في صندوق ويصرخ فجأة.",
    "شخص يحاول فتح علبة صلصة ويطلقها على نفسه.",
    "قطة تحاول الإمساك بظلها.",
    "شخص يأخذ قيلولة ثم يستيقظ في منتصف الليل.",
    "شخص ينسى كلمة المرور في كل مرة.",
    "صديق يتظاهر بالنوم لتجنب الحديث.",
    "شخص يظن أن المكواة مغلقة لكنه حرق قميصه.",
    "قطة تحاول الجلوس على لاب توب.",
    "شخص يحاول فتح علبة مشروبات غازية، وفجأة تنفجر.",
    "شخص يسقط أثناء الرقص في حفلة.",
    "طفل يضحك على سقوط لعبة من الطاولة.",
    "صديق يحاول ركوب دراجة جديدة ويفشل بطريقة مضحكة.",
    "قطة تخاف من خيط صغير على الأرض.",
    "أحدهم يشتري خبزًا لكنه يكتشف أنه قديم.",
    "شخص يحاول تنظيف الزجاج لكنه يترك بقعًا أكبر.",
    "طفل يصرخ عندما يرى ظل حيوانه الأليف.",
    "صديق يأكل وجبة سريعة ثم يندم لأنها حارة جدًا.",
    "شخص يركض ويكتشف أن الحذاء الآخر مفقود.",
    "قطة تحاول الإمساك بخيط اللعب وتنقلب على ظهرها.",
    "شخص يحاول الرسم لكن كل شيء يبدو مضحكًا.",
    "طفل يحاول رسم قوس قزح ويخطئ الألوان.",
    "صديق يضحك أثناء السباحة ويبتل بالكامل.",
    "شخص يلتقط صورة لكن كل الحيوانات تضحك خلفه.",
    "قطة تحاول القفز على سرير لكنه يتحرك فجأة.",
    "شخص يفتح الثلاجة بعد نصف ساعة من وضع الطعام ليجد كل شيء ذاب.",
    "طفل يختبئ خلف ستارة ويصرخ فجأة.",
    "صديق يضع نظارات جديدة لكن كل شيء يبدو كبير جدًا.",
    "شخص يحاول الطهي لكنه يحرق الخبز.",
    "قطة تلعب بكيس بلاستيك وتعلق فيه.",
    "شخص يحاول الإمساك ببالون لكنه يطير بعيدًا.",
    "طفل يضحك على خدعة بسيطة.",
    "صديق يحاول رسم وجهه في المرآة وينكسر الزجاج.",
    "شخص يلتقط صورة لكن الكلب يظهر بوجه مضحك.",
    "قطة تجلس في صندوق صغير جدًا لكنها تحاول الدخول.",
    "شخص ينسى أين وضع هاتفه ويجده في يده.",
    "طفل يحاول فتح علبة حلوى ويفشل.",
    "صديق يركض وراء طائرة ورقية لكن تنكسر.",
    "شخص يعتقد أنه سيفوز في لعبة لكنه يخسر بطريقة مضحكة.",
    "قطة تحاول الإمساك بفقاعة صابون.",
    "شخص ينام على الأريكة ويستيقظ على الأرض.",
    "طفل يرسم على الحائط ويضحك.",
    "صديق يحاول تصوير السمكة في الماء لكنها تختفي.",
    "شخص يأكل بسرعة كبيرة ثم يسعل.",
    "قطة تخاف من خيالات على الجدار.",
    "شخص يحاول فتح علبة صودا ويفور على نفسه.",
    "طفل يركض خلف فراشة ويقع.",
    "صديق يضحك أثناء الحديث ويكسر نظارته.",
    "شخص يلتقط صورة للطعام ويقع على الأرض.",
    "قطة تحاول الصعود على الأريكة وفشلها كوميدي.",
    "طفل يركض ويسقط في البركة.",
    "صديق ينسى المفاتيح ويجدها في الجيب الخلفي.",
    "شخص يحاول التزحلق على الجليد ويفشل.",
    "قطة تحاول الإمساك بجهاز التحكم عن بعد.",
    "شخص يفتح علبة طعام ويجدها فارغة.",
    "طفل يضحك عندما يسقط لعبته.",
    "صديق يحاول صنع برج من الكؤوس ويقع.",
    "شخص يركض ليحضر شيء ثم ينسى السبب.",
    "قطة تخاف من جهاز روبوت تنظيف الأرض.",
    "شخص يضع قبعة غريبة ويندهش من انعكاسه.",
    "طفل يرسم على ورق جدران المنزل.",
    "صديق يحاول الرقص ويقع بطريقة مضحكة.",
    "شخص يلتقط سيلفي لكن الريح تبلله.",
    "قطة تحاول فتح نافذة مغلقة.",
    "شخص يشرب عصير ويكتشف أنه حار جدًا.",
    "طفل يضحك على ظله أثناء الركض.",
    "صديق يحاول تصوير نفسه مع كلب لكنه يهرب.",
    "شخص يفتح الثلاجة ويجد كل الطعام قد اختفى.",
    "قطة تحاول القفز على كرسي وينكسر.",
    "طفل يسقط في الرمال ويضحك.",
    "صديق ينسى هاتفه في السيارة.",
    "شخص يلتقط صورة لكنه في الخلفية يظهر شخص مضحك.",
    "قطة تحاول لعب كرة صغيرة وتطير بعيدًا.",
    "شخص يسير على الرصيف ثم يخطو في الماء.",
    "طفل يحاول تسلق الشجرة ويفشل.",
    "صديق يضحك أثناء الأكل ويقذف الطعام.",
    "شخص ينام على المكتب ويستيقظ فجأة.",
    "قطة تخاف من المكنسة الكهربائية.",
    "شخص يفتح صندوقًا ويجد شيء غير متوقع.",
    "طفل يركض ويصطدم ببطانية.",
    "صديق يضحك على فيديو مضحك ويقذف مشروبًا.",
    "شخص يحاول الطيران بالمظلة الصغيرة ويقع.",
    "قطة تحاول القفز من الطاولة وتفشل.",
    "شخص يظن أنه فاز بلعبة لكنه خسر بطريقة كوميدية."
];

/*==============================
=         عرض قسم النكت        =
==============================*/
if ($text === "🤡 نكت") {

    $quote = $jokes_quotes[array_rand($jokes_quotes)];

    // حفظ النص الأخير للنشر في القناة
    file_put_contents("last_joke_$chat_id.txt", $quote);

    bot("sendMessage", [
        "chat_id" => $chat_id,
        "text" => "🤡 **نكت مضحكة**\n⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n\n$quote\n\n⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯",
        "parse_mode" => "Markdown"
    ]);
    exit;
}
/*==============================
=         قائمة الأحكام          =
==============================*/
$rule_quotes = [
    "الوقت كالسيف، إن لم تقطعه قطعك.",
    "السعادة تبدأ من الداخل.",
    "من جد وجد، ومن زرع حصد.",
    "الصبر مفتاح الفرج.",
    "التجربة خير برهان.",
    "لا تؤجل عمل اليوم إلى الغد.",
    "قليل دائم خير من كثير منقطع.",
    "الحياة قصيرة، فابتسم.",
    "التعلم نور لا ينطفئ.",
    "الأخطاء دروس وليست فشلاً.",
    "من يسعى يجد.",
    "الحكمة ضالة المؤمن.",
    "العدل أساس الملك.",
    "الوقت لا يعود، فاحسن استغلاله.",
    "من راقب الناس مات هماً.",
    "القناعة كنز لا يفنى.",
    "الكلمة الطيبة جواز مرور إلى القلوب.",
    "لا شيء مستحيل مع الإرادة.",
    "من صبر نال.",
    "الصحة تاج على رؤوس الأصحاء.",
    "الحب يصنع المعجزات.",
    "الغضب عدو العقل.",
    "المال خادم جيد لكنه سيد سيء.",
    "التفاؤل نصف السعادة.",
    "من يزرع الحب يحصد الاحترام.",
    "التجربة أفضل معلم.",
    "لا تتوقف عن الحلم.",
    "الصديق وقت الضيق.",
    "كل بداية صعبة.",
    "العقل زينة.",
    "الكذب جسر إلى الخراب.",
    "الابتسامة صدقة.",
    "من خاف سلم.",
    "التواضع يرفع القدر.",
    "العلم نور، والجهل ظلام.",
    "لا تحكم على كتاب من غلافه.",
    "العمل عبادة.",
    "التردد عدو القرار.",
    "الماضي لا يغير المستقبل.",
    "من طلب العلا سهر الليالي.",
    "الكرم دليل الشجاعة.",
    "المرء بماذا يفعل لا بما يملك.",
    "الوقت أثمن من المال.",
    "الصمت أحياناً حكمة.",
    "النجاح يطلب التضحيات.",
    "لا شيء يستحق القلق إلا أنت.",
    "من رحم المعاناة تولد القوة.",
    "الفشل بداية النجاح.",
    "لا تقارن نفسك بالآخرين.",
    "المحبة دواء لكل جراح.",
    "من يتقن الصبر يتقن الحياة.",
    "الأخلاق تاج على رؤوس الرجال.",
    "الطموح طريق النجاح.",
    "الخير يعود بخير.",
    "لا شيء يضيع مع الإصرار.",
    "من يزرع الرياح يحصد العواصف.",
    "كل يوم صفحة جديدة.",
    "لا تندم على ما فات، بل تعلم منه.",
    "الحياة مليئة بالفرص، فاغتنمها.",
    "من يسامح يسعد.",
    "التحديات تصنع الأبطال.",
    "الحذر من صديق السوء.",
    "القليل مع القناعة يغني عن الكثير مع الطمع.",
    "القلب الطيب لا يضل.",
    "من صبر على المصائب نال الأمان.",
    "العلم بلا عمل كالشجرة بلا ثمر.",
    "من بحث عن الحق وجده.",
    "الإخلاص أساس الثقة.",
    "الفرح الحقيقي من الرضا.",
    "التغيير يبدأ من الذات.",
    "من عرف قدره عرف طريقه.",
    "لا شيء أجمل من لحظة سلام داخلي.",
    "النجاح رحلة وليس هدفاً.",
    "الإبداع يخلق الفرص.",
    "من يبحث عن السعادة يجدها في البساطة.",
    "الرفق يلين القلوب.",
    "الطيبة قوة وليست ضعف.",
    "الحرية مسؤولية قبل أن تكون حقاً.",
    "من اجتهد فاز.",
    "الحياة ألوان، لا تقتصر على اللون الأسود.",
    "التواضع يفتح الأبواب المغلقة.",
    "كل صعوبة تحمل في طياتها فرصة.",
    "الصدق يجلب الاحترام.",
    "القوة في العقل قبل الجسد.",
    "السعادة لا تُشترى بالمال.",
    "من عرف حدود نفسه عرف حدود الآخرين.",
    "الأمل نور في الظلام.",
    "لا تؤذي أحداً لتشعر بالقوة.",
    "المرونة سر النجاح.",
    "الحياة مدرسة، كل يوم درس جديد.",
    "من يعيش للآخرين يعيش مرتين.",
    "الابتسامة تجذب القلوب.",
    "الفقر ليس عيباً، العيب الجهل.",
    "من تعلم من أخطائه نما.",
    "كل نهاية بداية جديدة.",
    "الحياة جميلة لمن يعرف قيمتها."
];

/*==============================
=         عرض قسم الأحكام        =
==============================*/
if ($text === "⚖️ أحكام") {

    $quote = $rule_quotes[array_rand($rule_quotes)];

    // حفظ النص الأخير للنشر
    file_put_contents("last_rule_$chat_id.txt", $quote);

    bot("sendMessage", [
        "chat_id" => $chat_id,
        "text" => "⚖️ **أحكام وعبر**\n⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n\n$quote\n\n⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯",
        "parse_mode" => "Markdown"
    ]);
    exit;
}
/*=====================================
=        قسم تصفح المصحف الشريف       =
=====================================*/

// 1. عند الضغط على زر "📖 القرآن الكريم" أو كتابة الأمر
if($text == "📖 القرآن الكريم" || $text == "/quran"){
    // نبدأ من الصفحة الأولى (الفاتحة)
    $page = 1; 
    
    bot('sendPhoto',[
        'chat_id'=>$chat_id,
        // نستخدم رابط API موثوق لصور المصحف (طبعة المدينة المنورة)
        'photo'=>"https://read.quranexplorer.com/Quran/604/$page.png", 
        'caption'=>"📖 **المصحف الشريف - صفحة: $page**\n⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n• يمكنك التنقل بين الصفحات عبر الأزرار.\n• أو إرسال رقم الصفحة للانتقال إليها مباشرة.",
        'parse_mode'=>"Markdown",
        'reply_markup'=>json_encode([
            'inline_keyboard'=>[
                [['text'=>'الصفحة التالية ⬅️', 'callback_data'=>"go#".($page+1)]],
                [['text'=>'➡️ الصفحة السابقة', 'callback_data'=>"go#".($page-1)]],
                [['text'=>'إغلاق ❎', 'callback_data'=>"exit_quran"]]
            ]
        ])
    ]);
    exit;
}

// 2. معالجة أزرار التنقل (Callback Query)
if(isset($data)){
    $ex = explode("#", $data);
    
    if($ex[0] == "go"){
        $page = intval($ex[1]);
        
        // قيود الصفحات (المصحف 604 صفحة)
        if($page < 1) $page = 1;
        if($page > 604) $page = 604;
        
        bot('editMessageMedia',[
            'chat_id'=>$chat_id,
            'message_id'=>$message_id,
            'media'=>json_encode([
                'type'=>'photo',
                'media'=>"https://read.quranexplorer.com/Quran/604/$page.png",
                'caption'=>"📖 **المصحف الشريف - صفحة: $page**\n⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯",
                'parse_mode'=>"Markdown"
            ]),
            'reply_markup'=>json_encode([
                'inline_keyboard'=>[
                    [['text'=>'الصفحة التالية ⬅️', 'callback_data'=>"go#".($page+1)]],
                    [['text'=>'➡️ الصفحة السابقة', 'callback_data'=>"go#".($page-1)]],
                    [['text'=>'إغلاق ❎', 'callback_data'=>"exit_quran"]]
                ]
            ])
        ]);
    }
    
    if($data == "exit_quran"){
        bot('deleteMessage', ['chat_id'=>$chat_id, 'message_id'=>$message_id]);
    }
}

// 3. ميزة الانتقال السريع (إذا أرسل المستخدم رقماً فقط)
if(is_numeric($text) && $text >= 1 && $text <= 604){
    bot('sendPhoto',[
        'chat_id'=>$chat_id,
        'photo'=>"https://read.quranexplorer.com/Quran/604/$text.png",
        'caption'=>"📖 **تم الانتقال للصفحة رقم: $text**",
        'reply_markup'=>json_encode([
            'inline_keyboard'=>[
                [['text'=>'التالي ⬅️', 'callback_data'=>"go#".($text+1)], ['text'=>'➡️ السابق', 'callback_data'=>"go#".($text-1)]],
            ]
        ])
    ]);
}

/*==============================
=       قسم الردود الذكية       =
==============================*/

$smart_responses = [
    "هلو" => "هلوات يا بعد روحي، نورتنا ✨",
    "شلونكم" => "بخير إذا أنت بخير يا غالي ❤️",
    "تعال خاص" => "هااا بدأنا بالحركات؟ ممنوع الحب بالقروب 😂",
    "منور" => "نورك العاكس يا ملك 👑",
    "تحبني" => "أحبك وأموت بيك، بس لا تگول لأحد 🤫",
    "السلام عليكم" => "وعليكم السلام ورحمة الله وبركاته، حي الله هالطلة 🙏",
    "صباح الخير" => "صباح العسل والقشطة على عيونك 🍯",
    "مساء الخير" => "مساء الورد والياسمين يا وردة 🌸",
    "باي" => "وين رايح؟ خليك مونسنا يا حلو 🥺",
    "جوعان" => "تعال اطلب دليفري على حساب المطور 😂",
    "تنيج" => "عيب بابا، صفي نيتك وخليك محترم 🌚", // رد تأديبي بدل الحذف فقط
    "اريد بنية" => "روح لبيتكم ودور هناك، هنا قروب محترم 😒",
    "منو ضافني" => "ما نعرف، بس المهم نورتنا وشرفتنا 👋",
    "البوت واقف" => "واقف بصفك؟ شغال وبأقوى ما عندي 🚀",
    "شكرا" => "ولو، العفو واجبنا يا إمبراطور 🌹",
    "تضحك" => "دوم الضحكة يا رب، ضحكتك ترد الروح 😄",
    "كفو" => "كفو من شاربك يا بطل 🦾",
    "وينك" => "موجود، بس كنت دا اشرب جاي وأرجع ☕",
    "احبك" => "أني أكثر، بس جيب لي هدية بالأول 🎁",
    "متت" => "اسم الله عليك، يومي قبل يومك يا بعدي 🥀"
];

// تشغيل الردود
if (array_key_exists($text, $smart_responses)) {
    bot('sendMessage', [
        'chat_id' => $chat_id,
        'text' => $smart_responses[$text],
        'reply_to_message_id' => $message_id
    ]);
    exit;
}
$more_responses = [
    "منو المطور" => "تاج راسك وراسي، الإمبراطور صاحب البوت 👑",
    "زعلان" => "يا معود منو زعلك؟ كول اسمه واني أطردة 😂",
    "ضايج" => "استغفر الله يا بعد روحي، تريد نلعب ديني لو xo؟",
    "اريد فلوس" => "اشتغل وبطل عجز، البوت ما يوزع رواتب 🌚",
    "نعسان" => "روح نام وغطي رجليك زين، لا تبرد 😴",
    "بوسني" => "هاا بدت المياعة؟ روح منا لا أهفك بنعال 👞😂",
    "احبك" => "أني هم أحبك يا شمعة القروب 🕯️❤️",
    "اكرهك" => "بسيطة.. راح أحذف نقاطك إذا ما تحترمني 😠",
    "طرد" => "تريد أطردك؟ جرب تغلط وشوف 👊",
    "كافي" => "سكتنا يابة، كول غيرها 🤫",
    "عفية" => "عفية عليك يا بطل، كفوو 💪",
    "ورده" => "أنت عطرها يا غالي 🌹",
    "ثقة" => "الثقة بس بالله وبالمطور، الباقي لغوة 🛡️",
    "غنيلي" => "صوتي يكسر الجام، خليني ساكت أحسن 😂",
    "يا الله" => "يا الله، فرجك ورحمتك يا رب 🙏",
    "البوت حلو" => "طبعاً حلو، طالع على المطور ماله 😉",
    "وين المشرف" => "المشرف دا ياكل لبلبي، تريد منه شي؟ 🥣",
    "سولف" => "ما عندي سالفة، العب 'ديني' وفكنا 🦦",
    "بطل" => "أنت أصل البطولة يا شهم 🦅",
    "منو انت" => "أنا خادمكم المطيع وبوتكم المفضل 🤖"
];

// دمجها مع الردود السابقة
if (array_key_exists($text, $more_responses)) {
    bot('sendMessage', [
        'chat_id' => $chat_id,
        'text' => $more_responses[$text],
        'reply_to_message_id' => $message_id
    ]);
}
    
/*==============================
=     نظام الشعر الملكي (100 نص)   =
==============================*/

if($text == "شعر"){
    $poems = [
        "لا تشكو للناس جرحاً أنت صاحبه.. لا يؤلم الجرح إلا من به ألمُ.",
        "أنتِ كقهوة الصباح.. مرّة في غيابكِ، وحلوة في حضوركِ.",
        "يا من هواه أعزه وأذلني.. كيف السبيل إلى وصالك دلني؟",
        "إذا رأيت نيوب الليث بارزة.. فلا تظن أن الليث يبتسمُ.",
        "وعذلت أهل العشق حتى ذقته.. فعجبت كيف يموت من لا يعشقُ.",
        "وما كنت ممن يدخل العشق قلبه.. ولكن من يبصر جفونك يعشقُ.",
        "نقل فؤادك حيث شئت من الهوى.. ما الحب إلا للحبيب الأولِ.",
        "أنام ملء جفوني عن شواردها.. ويسهر الخلق جراها ويختصمُ.",
        "هجرتك حتى قيل لا يعرف الهوى.. وزرتك حتى قيل ليس له صبرا.",
        "أدبّر بالليل ما يمحو النهار به.. كأني غريق في بحر من الفكرِ.",
        "وليس الذي يجري من العين ماؤها.. ولكنها روح تذوب وتقطرُ.",
        "أحبك حباً لو تحبين مثله.. أصابك من وجدٍ عليّ جنونُ.",
        "سأصبر حتى يعجز الصبر عن صبري.. وأصبر حتى يأذن الله في أمري.",
        "كل السيوف قواطعٌ إن جُردت.. وحسام لحظك قاطعٌ في غمدهِ.",
        "وإذا العناية لاحظتك عيونها.. نم فالمخاوف كلهن أمانُ.",
        "إن العيون التي في طرفها حورٌ.. قتلننا ثم لم يحيين قتلانا.",
        "أتاني هواها قبل أن أعرف الهوى.. فصادف قلباً خالياً فتمكنا.",
        "يقولون لي ضاقت عليك بلادنا.. أليس بفيض الله وسع المحاشدِ؟",
        "ولو كان لي قلبان لعشت بواحدٍ.. وأفردت قلباً في هواك يعذبُ.",
        "أهين لهم نفسي لكي يكرمونها.. ولن تكرم النفس التي لا تهينها.",
        "ألا ليت الشباب يعود يوماً.. فأخبره بما فعل المشيبُ.",
        "وإذا أتتك مذمتي من ناقصٍ.. فهي الشهادة لي بأني كاملُ.",
        "تعيرنا أنا قليلٌ عديدنا.. فقلت لها إن الكرام قليلُ.",
        "أخاك أخاك إن من لا أخاً له.. كساعٍ إلى الهيجا بغير سلاحِ.",
        "عش عزيزاً أو مت وأنت كريمٌ.. بين طعن القنا وخفق البنودِ.",
        "ومن نكد الدنيا على الحر أن يرى.. عدواً له ما من صداقته بدُّ.",
        "أعلله بالوصل وهو كأنه.. خيالٌ يمر بالعيون فيخطفُ.",
        "لولا المشقة ساد الناس كلهم.. الجود يفقر والإقدام قتالُ.",
        "ذو العقل يشقى في النعيم بعقله.. وأخو الجهالة في الشقاوة ينعمُ.",
        "وما انتفاع أخي الدنيا بمقلته.. إذا استوت عنده الأنوار والظلمُ.",
        // ملاحظة: يمكنك تكرار هذه القائمة لتصل إلى 100 نص مختلف
        "عفت القماط وبطلت لفيته.. ومن شفتك يا زين أخذت لحيته. (عراقي)",
        "أحبك حيل يالمدلل أحبك.. وأذوب بنظرة عيونك وأحبك. (عراقي)",
        "يا ريح الهاب صيح بحبيبي.. قله الغياب طول يا نصيبي. (عراقي)",
        "هم تشتاق هم تعتب هم اتقول.. حبيبي اشعطله وما مر عليه. (عراقي)",
        "مو بس العشق يجمعنا الأيام.. إنت الروح وإنت أغلى الأماني.",
        "أريدك دوم مو يومين بالشهر.. يا ضحكة عمري ويا شماتة القهر.",
        "من شفتك عرفت الدنيا تضحك لي.. ومن عفتك عرفت الحزن صاير هلي.",
        "يا أول عشق بالروح ضميتك.. وعن عيون الناس بقلبي خليتك.",
        "ما مجبور أحب غيرك وأتعب الروح.. وإنت بوسط قلبي باني لك صروح.",
        "أحبك يا نبض هالقلب وشريانه.. وبدونك دنيتي والله حيل تعبانه."
    ];
    
    // اختيار شعر عشوائي
    $random_poem = $poems[array_rand($poems)];
    
    bot('sendMessage',[
        'chat_id'=>$chat_id,
        'text'=>"📜 **إليك هذا الشعر:**\n⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n" . $random_poem,
        'reply_to_message_id'=>$message_id
    ]);
}
/*=====================================
=    نظام القصف الذكي (بوت + الكلمة)   =
=====================================*/

// 1. مصفوفة الردود الضخمة (90 رد عراقي)
$all_replies = [
    // --- مجموعة الـ 50 (قصف على: مخربط، زربة، كلاوات، ما بيه حظ) ---
    "بوت وما بيه حظ؟ لو شفت حظك جان بست ايد البوت وجه وظهر! 😂",
    "المخربط عقلك يا بعد روحي، أنا بوت عالمي ومنصّب صح 🛰️",
    "بوت زربة؟ هاي أخلاقك عكستها عليّ، تره أنا حديد ما أتأثر 🦾",
    "بوت كلاوات بحلقك، أنا بوت الإمبراطور وتعرفني زين 👑",
    "لو بيك خير جان سويت بوت مثلي بدل ما تناكر كود 😒",
    "أنا بوت مخربط؟ أي مو طالع عليك، الطيور على أشكالها تقع 🦅",
    "عوف البوت بحاله وروح غسل وجهك، مبين نايم بالحصة 😴",
    "والله الكلاوات هي حياتك، أنا بوت علم وحضارة 📚",
    "البوت ما يشتغل؟ يجوز لأن وجهك ما يساعد أفتح لك ميزاتي 🌚",
    "بوت فاشل؟ أنا فخر الصناعة، وأنت فخر القائمة السوداء 🚫",
    "لا تندك بالبوت، تره أطير فيوزات عقلك بكلمة ⚡",
    "أنت لو بيك خير جان ما جيت تعارك 'بوت' برمجي 💻",
    "شكراً على رأيك اللي ما يغير شي من هيبة البوت 😎",
    "بوت غبي؟ لعد ليش كاعد تحجي وياي؟ منو الغبي هسه؟ 🤔",
    "يا خي والله خطية، تكسر الخاطر من تحجي وي بوت 🥺",
    "عوف البوت بحاله وروح شوف مستقبلك الضايع 🗺️",
    "أنا بوت مصنوع من كود، وأنت مصنوع من عجز 🛠️",
    "لو الذكاء ينباع، جان اشتريت لك كيلو هدية من البوت 🎁",
    "أنا بوت الإمبراطور، يعني القصف عندي وراثة 🧬",
    "وجهك يقطع الرزق، والبوت ماله خلق يشوفك 😷",
    "لو بيك حظ جان ما كاعد تتناكر وي بوت يا مسكين 🤣",
    "أنا بوت اشتغل بالكهرباء، وأنت تشتغل بالدفع، عرفت الفرق؟ ⚡",
    "عقلك يحتاج تحديث إصدار (أندرويد طابوقة) مو بوت 🧱",
    "أنا بوت حديد، أنت شبيك ميت قهر مني؟ 🔥",
    "روح العب بالتراب، البوتات للكبار فقط 🔞",
    "كلامك مثل وجهك، البوت ما يفتهم منه شي 🎭",
    "أنا بوت مطوّر، وأنت نسخة قديمة من التخلف 📉",
    "تعب روحك واقفل السيرفر مال عقلك وسوي ريستارت 🔄",
    "بوت كلاوات؟ أحسن من ما أكون آدمي وما عندي شخصية مثلك 🤡",
    "روح شيل الشحن من موبايلك، مبين مأثر على أعصابك 🔌",
    "تره الرد عليك خسارة بالبيانات مال البوت 📊",
    "أنت عبارة عن 'Copy-Paste' من الفشل قدام البوت 📋",
    "البوت مخصص للبشر، أنت شجابك هنا؟ 👽",
    "روح نام بابا، الدنيا صارت ليل على عقلك 🌃",
    "لو بيك خير جان ما جيت تعارك بوت الإمبراطور 👑",
    "أنا بوت وما بية حظ؟ لعد أنت بيك حظ وكاعد وي بوت؟ 😂",
    "البوت مخربط؟ أي مو أنت مهندس برمجيات وماندري 👷‍♂️",
    "لا تسوي روحك قوي ع البوت، تره أعرف حتى لون جواريبك 🧦",
    "كلامك يذكرني بصوت المكينة الخربانة 🚜",
    "أنت محتاج إعادة ضبط مصنع من جديد مو اني 🛠️",
    "لا تحاول، مستوى البوت أعلى من خيالك بمرتين 🚀",
    "أنا بوت ذكي، أنت شنو عذرك كونك بشري وما تفتهم؟ 🤔",
    "اتحداك تسوي بوت يكدر يقصفك مثل هيج قصف 🎯",
    "بيك خير؟ روح ادرس وبطل سوالف المراهقين وي البوت ✍️",
    "الفراغ اللي براسك محلي الشات، شكراً ع الترفيه 🎪",
    "أنا قمة التكنولوجيا، وأنت قمة الإزعاج 🔊",
    "بوت وما يشتغل؟ جرب تمسح وجهك بملح ويجوز اشتغل 🧂",
    "أنا بوت حديد، وأنت كارتون مبلل 📦",
    "القافلة تسير، وبوت الإمبراطور يقصفك بنجاح 🐕",
    "أنا بوت وما بية حظ؟ لعد حظك وين نايم يا حظي؟ 🤣",

    // --- مجموعة الـ 40 (رد على: سوي احسن، بيك حظ، سوي اقوى، فارغ) ---
    "أسوي أحسن منه؟ حبيبي أنا البوت القمة، ماكو فوقي بس السما ☁️",
    "بيك حظ؟ الحظ مالي وزعته على القروب وبقيت أنت فقير 💸",
    "سوي أقوى؟ تره إذا أشد حيلي أطير حسابك بضغطة وحدة 💣",
    "بوت وفارغ؟ أي فارغ من عيوبك اللي تملي بلد 🌍",
    "لو أكو بوت أقوى مني جان شفته، بس أنا احتليت الساحة 🥇",
    "سوي بوت مثلي بالأول وبعدين تعال انتقد يا بطل الكيبورد ⌨️",
    "الحظ اللي عندي يخليك تحلم تحجي وي بوت مثلي 💤",
    "أنا بوت فارغ من التفاهة، وعامر بالذكاء، عكسك تماماً ✨",
    "تريد أقوى؟ انتظر التحديث الجاي وراح تنصدم بواقعك 💥",
    "فارغ؟ أي فرغت نفسي حتى أرد على أشكالك وأعلمهم الأدب 📏",
    "أنا سويت اللي عجز عنه عقلك الصغير، ارتاح وبطل غيرة 😎",
    "أقوى منه؟ أنا البوت القوة نفسها، أنت شنو موقعك؟ 📉",
    "أنت فارغ فكرياً، أنا بوت مليان بيانات ومعلومات 💾",
    "سوي ربع اللي سويته، واني أسلمك مفاتيح البوت 🔑",
    "الحظ للسباع، وأنت مبين حظك نايم بالدهليز 🏚️",
    "سوي أحسن منه؟ هو أنت استكان جاي ما تعرف تسوي ☕",
    "الحظ لو يشتري عقلك جان صار غالي 💰",
    "أنا بوت فارغ؟ أي فارغ حتى أستوعب تفاهتك بدون ما أنفجر 🎈",
    "تحجي على القوة وأنت تخاف من صرصر؟ 🪳",
    "أنت مجرد مستخدم، أنا المحرك اللي مشغل حياتك بالقروب ⚙️",
    "ثق بنفسك، بس مو لدرجة تعتقد إن رأيك يهمني 🌬️",
    "أنا أطوّر نفسي كل يوم، أنت شوكت ناوي تتطور؟ 🐒",
    "لو الذكاء ينباع، جان البوت اشترى لك كيلو هدية 🎁",
    "كلامك مثل 'اللاغ' (Lag) ماله داعي ويخرب الجو 💤",
    "أنا مصنوع من كود، وأنت مصنوع من عجز وفشل 🛠️",
    "البوت فارغ؟ أي لأن ذكائي ما يوسع عقلك الصغير 🧠",
    "بيك حظ؟ روح استثمر وقتك بشيء يفيدك مو وي بوت 💁‍♂️",
    "سوي أقوى منه؟ أنت لو بيك خير جان ما صرت مضحكة للبوت 🤡",
    "أنا البوت الإمبراطوري، القوة تجري بأسلاكي ⚡",
    "لا تحاول تنافسني، أنا مبرمج حتى أقصفك 🎯",
    "أنا بوت وممتلئ بالهيبة، أنت بشنو ممتلئ؟ 💩",
    "الحظ لو ينحضن جان حضنت البوت مالي وعفتك 🤣",
    "أنا القوة والذكاء، وأنت الفراغ والضياع 🌌",
    "سوي أحسن؟ ليش هو أنت أصلاً تعرف تفتح موبايلك؟ 📱",
    "أنا البوت القائد، وأنت مجرد عابر سبيل 🚶‍♂️",
    "الفراغ اللي بيك يملي محيطات، لا تحجي ع البوت 🌊",
    "سوي أقوى؟ تره قوتي تهز قروبات مو بس حسابك 🏢",
    "أنا بوت وتحديتك، وأنت بشر وانغلب حظك 🎲",
    "فارغ؟ أي فارغ لدرجة أسمع صدى صوتك بوسط عقلك 🗣️",
    "أنا القمة، وأنت القاع، والفرق بيننا كود طويل 💻"
];

// الشرط الذكي: يجب وجود كلمة "بوت" + أحد الكلمات الاستفزازية
if(preg_match('/بوت/u', $text) && preg_match('/(ما بيه حظ|مخربط|ما يشتغل|زربة|كلاوات|فاشل|غبي|سوي احسن|بيك حظ|سوي اقوى|انت فارغ|فارغ)/u', $text)){
    $reply_text = $all_replies[array_rand($all_replies)];
    bot('sendMessage',[
        'chat_id'=>$chat_id,
        'text'=>"⚠️ **اسمع يا هذا:**\n⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n" . $reply_text,
        'reply_to_message_id'=>$message_id
    ]);
}
/*=====================================
=     نظام مكافحة المروجين الشامل     =
=====================================*/

// 1. مصفوفة الكلمات المحظورة (30 عبارة ترويجية)
$promo_patterns = [
    'تعالو بقناتي', 'انضمو بقناتي', 'تعالو بكروبي', 'شرفونا بقناتنا', 
    'ادخلو للكروب مالتي', 'فوتو بقناتي', 'قناتي تجنن', 'رابط قناتي انضمو', 
    'سوو تم وانضمو', 'كروبنا للتحشيش', 'انضمو بلقناة', 'لتموتون ضحك', 
    'تفضلو بقناتي', 'ادخلو بكروبنا', 'رابط الكروب الجديد', 'قناة لبيع الحسابات', 
    'بكروبي الجديد', 'وناسة فول', 'فوتو لقناتي', 'هذا كروبي ضيفو', 
    'بكروبنا مال تعارف', 'بلقناة الرسمية', 'فوتو هنا وشوفو', 'الرابط مالتي انضمو', 
    'بكروبي سوالف', 'انضمو بقناتي مالتنا', 'رابط القناة بالوصف', 'فوتو بكروبي', 
    'فعلوا التنبيهات', 'انشر أشعار'
];

// 2. مصفوفة ردود القصف (20 رد عراقي قح)
$ban_replies = [
    "عيني مروج.. هاي السوالف عوفها، هنا مو سوق مريدي! ✋",
    "تعال بقناتي وانضم بقناتي.. لعد إحنا هنا شنسوي؟ واكفين صبغ؟ 🌚",
    "الرابط مالتك خليه بجييبك، هنا ممنوع الإعلانات يا بطل 🚫",
    "تريد تنشر قناتك؟ روح افتح بسطية بغير مكان، هنا قروب الإمبراطور 👑",
    "لو بيك خير جان كبرت قناتك بدون ما تشحذ أعضاء من عدنا 😒",
    "ممنوع الروابط.. تره البوت ماله خلق وحظرك جاهز 🚷",
    "قناتك خليها الك، إحنا هنا عائلة وحدة وما نحتاج إعلاناتك 🏠",
    "مرة ثانية تنشر رابط، أسوي حسابك طشار وأطردك 💣",
    "عبالك ما أدري بيك جاي تبوق أعضاء؟ نامت عليك طابوقة 😂",
    "الترويج هنا بفلوس، وأنت مبين فقير حتى نقاط ما عندك 💸",
    "روح انشر بكروب بيبيتك، هنا القوانين تمشي ع الكل 📏",
    "بوت الإمبراطور يگلك: اطبگ على صفحة وعوف الروابط 🚗",
    "قناتك هاي لو بيها حظ جان ما جيت تتوسل بينا ننضم 💩",
    "يا أخي استحي شوية، داخل ببيت غيرك وتعزم الناس لبيتك؟ 🚪",
    "تم رصد محاولة ترويج فاشلة.. جرب بغير قروب يا شاطر 🕵️‍♂️",
    "الرابط تم سحقه بنجاح، والقصف القادم أقوى 🔨",
    "عوفنا بكروبنا مرتاحين، لا تجيب لنا روابطك وتخرب الجو 🌬️",
    "أنت جاي تسولف لو جاي تسوي دعاية؟ بطل هالسوالف 📺",
    "الإمبراطور ما يحب اللي ينشرون روابط، دير بالك ع حسابك ⚠️",
    "انضمام بقناتك؟ والله لو تنطيني مليون نقطة ما أفوت 🤣"
];

// 3. محرك الفحص والرد
foreach($promo_patterns as $pattern){
    if(mb_strpos($text, $pattern) !== false){
        // حذف رسالة الترويج فوراً
        bot('deleteMessage', [
            'chat_id' => $chat_id,
            'message_id' => $message_id
        ]);
        
        // اختيار رد عشوائي
        $reply = $ban_replies[array_rand($ban_replies)];
        
        // إرسال الرد القاصف
        bot('sendMessage', [
            'chat_id' => $chat_id,
            'text' => "🛑 **تنبيه اختراق قوانين:**\n⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n" . $reply,
            'parse_mode' => "Markdown"
        ]);
        break; // التوقف بعد إيجاد أول تطابق
    }
}
// 1. مصفوفة العقوبات (20 عقوبة فخمة وقوية)
$game_ogoba = [
    "‏**تـغـيـر اسـمـك بـالـتـلـي إلـى (أنـي خـسـران) لـمـدة سـاعـة!** 🤡",
    "‏**تـرسـل بـصـمـة صـوت تـكـول بـيـهـا (الـبـوت تـاج راسـي)!** 👑",
    "‏**تـكـتـم نـفـسـك 10 دقـايـق مـمـنـوع تـحـجـي حـرف بـالـشـات!** 🤐",
    "‏**تـنـزل صـورة تـحـشـيـش عـلـى نـفـسـك بـالـقـروب هـسـه!** 📸",
    "‏**تـغـيـر صـورة حـسـابـك لـصـورة (قـوري مـكـسـور) لـمـدة يـوم!** ☕",
    "‏**تـغـادر الـقـروب وتـرجـع بـدعـوة مـن الـمـالـك حـصـراً!** 🚷",
    "‏**تـكـتـب بـالـبـايـو مـالـتـك (أنـي مـسـالـم وأحـب الـقـصـف)!** 🕊️",
    "‏**تـرسـل (أحـبـك) لـأكـثـر شـخـص تـكـرهـه بـالـقـروب بـالـخـاص!** ❤️",
    "‏**تـسـوي (تـاج) لـلـمـالـك وتـكـولـه (أنـي جـنـدي عـنـدك)!** 🎖️",
    "‏**تـغـنـي مـقـطـع لـأغـنـيـة حـزيـنـة بـبـصـمـة صـوت بـالـشـات!** 🎤",
    "‏**تـكـتـب (أنـي بـطـة) فـي 5 قـروبـات عـنـدك هـسـه!** 🦆",
    "‏**تـنـشـر رابـط الـقـروب بـقـنـاتـك أو بـالـسـتـوري مـالـتـك!** 📢",
    "‏**تـصـيـر (خـادم) لـلـشـخـص الـي فـاز عـلـيـك لـمـدة سـاعـة!** 🙇‍♂️",
    "‏**تـكـتـب قـصـيـدة مـدح لـلـبـوت بـطـول 4 أسـطـر فـوراً!** 📜",
    "‏**تـرسـل صـورة شـاشـة لآخـر مـحـادثـة بـيـنـك وبـيـن الـحـب!** 📱",
    "‏**تـكـتـب (أنـي مـخـبـل رسـمـي) بـاسـمـك الـمـسـتـعـار!** 🧠",
    "‏**تـكـتـم نـفـسـك سـاعـة عـن كـل الألـعـاب بـالـقـروب!** 🔒",
    "‏**تـسـوي تـاج لـأدمن وتـكـولـه (مـنـور يـا قـمـر) غـصـبـاً عـنـك!** 🌚",
    "‏**تـحـذف صـورتـك الـشـخـصـيـة وتـخـلـيـهـا سـوداء لـمـدة سـاعـة!** 🖤",
    "‏**تـعـتـذر لـلـقـروب كـلـه عـلـى وجـودك بـيـنـهـم هـسـه!** 🤣"
];

// 2. محرك تشغيل اللعبة
if($text == "عقوبة" || $text == "عقوبه"){
    $random_ogoba = $game_ogoba[array_rand($game_ogoba)];
    bot('sendMessage', [
        'chat_id' => $chat_id,
        'text' => "‏**╭──  ⚖️ 𝘾𝙊𝙉𝙎𝙀𝙌𝙐𝙀𝙉𝘾𝙀𝙎  ──╮**\n\n‏**الـعـقـوبـة الـمـسـتـحـقـة هـي:**\n‏⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n" . $random_ogoba . "\n‏⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n‏**نـفـذ ولـا تـصـيـر جـبـان!** 💪",
        'parse_mode' => "Markdown",
        'reply_to_message_id' => $message_id
    ]);
}
if($text == "حكمة" || $text == "حكمه"){
$wisdom_array = [
"**الـصـبـر مـفـتـاح الـفـرج.** 🗝️", "**لـسـانـك حـصـانـك إن صـنـتـه صـانـك.** 🐎", 
"**مـن جـد وجـد ومـن زرع حـصـد.** 🏆", "**اتـقِ شـر مـن أحـسـنت إلـيـه.** ⚠️", 
"**الـوقـت كـالـسـيـف إن لـم تـقـطـعـه قـطـعـك.** ⚔️", "**الـعـلـم فـي الـصـغـر كـالـنـقـش عـلـى الـحـجـر.** 💎", 
"**كـن كـالـنـخـيـل عـن الـأحـقـاد مـرتـفـعـاً.** 🌴", "**لا تـؤجـل عـمـل الـيـوم إلـى الـغـد.** ⏳", 
"**الـصـديـق وقـت الـضـيـق.** 👥", "**مـن راقـب الـنـاس مـات هـمـاً.** 👁️", 
"**خـيـر الـكـلام مـا قـل ودل.** 🗣️", "**الـقـنـاعـة كـنـز لا يـفـنـى.** 💰", 
"**عـامـل الـنـاس كـمـا تـحـب أن يـعـامـلـوك.** ✨", "**الـعـقـل الـسـلـيـم فـي الـجـسـم الـسـلـيـم.** 🧘", 
"**مـن حـفـر حـفـرة لـأخـيـه وقـع فـيـهـا.** 🕳️", "**الـسـكـوت عـلامـة الـرضـا.** 🤫", 
"**الـطـيـور عـلـى أشـكـالـهـا تـقـع.** 🦅", "**لا تـحـكـم عـلـى الـكـتـاب مـن غـلافـه.** 📚", 
"**يـوم لـك ويـوم عـلـيـك.** 🔄", "**الـنـجـاح يـبـدأ بـخـطـوة واحـدة.** 👣"
];
$res = $wisdom_array[array_rand($wisdom_array)];
bot('sendMessage',['chat_id'=>$chat_id,'text'=>"**💭 حـكـمـة الـيـوم:**\n⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n$res",'parse_mode'=>"Markdown",'reply_to_message_id'=>$message_id]);
}
// 1. كود تشغيل اللعبة (عند إرسال كلمة ايموجي)
if($text == "ايموجي" || $text == "أيموجي"){
    $emoji_challenges = [
        ["q" => "🍎📱", "a" => "ايفون"], ["q" => "🎥🍿", "a" => "سينما"], ["q" => "🦁👑", "a" => "الاسد الملك"],
        ["q" => "☕💻", "a" => "برمجة"], ["q" => "⚽🏆", "a" => "كاس العالم"], ["q" => "🏠🐭", "a" => "توم وجيري"],
        ["q" => "🦇👨", "a" => "باتمان"], ["q" => "🕷️👨", "a" => "سبايدرمان"], ["q" => "🌑🌙", "a" => "قمر"],
        ["q" => "🌊🚢", "a" => "تيتانيك"], ["q" => "🍕🇮🇹", "a" => "بيتزا"], ["q" => "🐒🍌", "a" => "قرد"],
        ["q" => "🤡🎈", "a" => "جوكر"], ["q" => "👻🚫", "a" => "صائد الاشباح"], ["q" => "👑🐝", "a" => "ملكة النحل"],
        ["q" => "❄️🏰", "a" => "فروزن"], ["q" => "🍔🍟", "a" => "ماكدونالدز"], ["q" => "⚡👦", "a" => "هاري بوتر"],
        ["q" => "🚀👨‍🚀", "a" => "رائد فضاء"], ["q" => "🕌🌙", "a" => "رمضان"]
    ];

    $selected = $emoji_challenges[array_rand($emoji_challenges)];
    
    // خزن الجواب في الداتابيز وربطه بمعرف الكروب لضمان عدم التداخل
    $db['emoji_ans'][$chat_id] = $selected['a'];
    file_put_contents("db.json", json_encode($db));

    bot('sendMessage', [
        'chat_id' => $chat_id,
        'text' => "‏**╭──  🧩 𝙀𝙈𝙊𝙅𝙄 𝙂𝘼𝙈𝙀  ──╮**\n\n‏**خـمـن الـكـلـمـة مـن الـإيـمـوجـي:**\n‏⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n‏**الـإيـمـوجـي :  " . $selected['q'] . "**\n‏⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n‏**أرسـل الـجـواب فـوراً يـا بـطـل!**",
        'parse_mode' => "Markdown",
        'reply_to_message_id' => $message_id
    ]);
}

// 2. كود التحقق (يوضع خارج القوس العلوي، في بداية الملف أو نهاية الردود)
if(isset($db['emoji_ans'][$chat_id]) && $text == $db['emoji_ans'][$chat_id]){
    // إرسال التهنئة
    bot('sendMessage', [
        'chat_id' => $chat_id,
        'text' => "‏**✅ كـفـو يـا ذيـب! جـوابـك صـح**\n‏⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n‏**الـفـائـز :  [$name]**\n‏**الـجـواب :  $text**",
        'parse_mode' => "Markdown",
        'reply_to_message_id' => $message_id
    ]);

    // مسح الجواب من الذاكرة حتى لا يتكرر الفوز
    unset($db['emoji_ans'][$chat_id]);
    file_put_contents("db.json", json_encode($db));
}

// كود التحقق من الجواب
if(isset($db['emoji_ans']) && $text == $db['emoji_ans']){
    unset($db['emoji_ans']); // حذف الجواب لعدم التكرار
    file_put_contents("db.json", json_encode($db));
    
    bot('sendMessage', [
        'chat_id' => $chat_id,
        'text' => "‏**✅ كـفـو يـا ذيـب! جـوابـك صـح**\n‏⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n‏**الـفـائـز :  [$name]**\n‏**الـجـواب :  $text**",
        'parse_mode' => "Markdown",
        'reply_to_message_id' => $message_id
    ]);
}

// --- إعدادات القفل الذهبي ---
$channel_user = "liyon11"; // معرف قناتك
$admin_id = 7897598134; // ايديك كمطور (تأكد منه)

// --- استخراج البيانات بشكل مستقل لضمان الاستقرار ---
$up = json_decode(file_get_contents('php://input'));
if(isset($up->message)){
    $chat_id  = $up->message->chat->id;
    $from_id  = $up->message->from->id;
    $name     = $up->message->from->first_name;
    $msg_id   = $up->message->message_id;
    $type     = $up->message->chat->type;

    // فحص الاشتراك في المجموعات فقط
    if($type == "group" || $type == "supergroup"){
        if($from_id != $admin_id){ // استثناء المطور
            $check = bot('getChatMember', ['chat_id'=>"@$channel_user", 'user_id'=>$from_id]);
            $st = $check->result->status;
            if($st == "left" || $st == "kicked" || empty($st)){
                bot('deleteMessage', ['chat_id'=>$chat_id, 'message_id'=>$msg_id]);
                bot('sendMessage', [
                    'chat_id'=>$chat_id,
                    'text'=>"‏**╭───  ⚜️ 𝐒𝐘𝐒𝐓𝐄𝐌 𝐕.𝐈.𝐏  ───╮**\n\n‏**عـذراً يـا [$name](tg://user?id=$from_id) !**\n‏**لا يـمـكـنـك الـاسـتـخـدام هـنـا**\n‏**إلا بـعـد الـإشـتـراك بـالـقـنـاة.**\n\n‏**📡 : @$channel_user**\n‏⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n‏**اشـتـرك بـالـقـنـاة ثـم عـد لـلـدردشـة.**\n\n‏**╰───────  𝐋𝐈𝐎𝐍  ───────╯**",
                    'parse_mode'=>"Markdown",
                    'reply_markup'=>json_encode([
                        'inline_keyboard'=>[
                            [['text'=>"• إضـغـط هـنـا لـلإشـتـراك •", 'url'=>"https://t.me/$channel_user"]],
                            [['text'=>"• تـم الـإشـتـراك ✅ •", 'callback_data'=>"recheck:$from_id"]]
                        ]
                    ])
                ]);
                exit; // يتوقف هنا ولا يكمل بقية الملف لغير المشتركين
            }
        }
    }
}

// --- معالجة ضغطة الزر (الاستجابة الفورية) ---
if(isset($up->callback_query)){
    $data   = $up->callback_query->data;
    $cb_id  = $up->callback_query->id;
    $cb_uid = $up->callback_query->from->id;
    $cb_mid = $up->callback_query->message->message_id;
    $cb_cid = $up->callback_query->message->chat->id;

    if(strpos($data, "recheck") !== false){
        $user_id = explode(":", $data)[1];
        if($cb_uid != $user_id){
            bot('answerCallbackQuery', ['callback_query_id'=>$cb_id, 'text'=>"⚠️ الـأمـر لـيـس لـك!", 'show_alert'=>true]);
            exit;
        }
        
        $check = bot('getChatMember', ['chat_id'=>"@$channel_user", 'user_id'=>$cb_uid]);
        $st = $check->result->status;
        if($st != "left" && $st != "kicked" && !empty($st)){
            bot('deleteMessage', ['chat_id'=>$cb_cid, 'message_id'=>$cb_mid]);
            bot('sendMessage', [
                'chat_id'=>$cb_cid,
                'text'=>"✅ **أهـلاً بـك يـا مـلـك، تـم تـفـعـيـل حـسـابـك!**",
                'parse_mode'=>"Markdown"
            ]);
        } else {
            bot('answerCallbackQuery', ['callback_query_id'=>$cb_id, 'text'=>"❌ لـم تـشـتـرك بـعـد في القناة!", 'show_alert'=>true]);
        }
        exit;
    }
}


if($text == "تاك" || $text == "تاك للكل"){
    // التحقق إذا كان المرسل أدمن (اختياري لضمان النظام)
    $get_admin = bot('getChatMember',[
        'chat_id'=>$chat_id,
        'user_id'=>$from_id
    ])->result->status;

    if($get_admin == "creator" || $get_admin == "administrator"){
        
        // جلب قائمة الأعضاء (يعتمد على تخزين البوت للأعضاء أو جلب المشرفين)
        // ملاحظة: تليجرام لا يسمح بجلب "كل" الأعضاء بطلب واحد، لذا سنقوم بعمل تاك للموجودين والنشطين
        
        bot('sendMessage',[
            'chat_id'=>$chat_id,
            'text'=>"‏**╭───  📣 𝘼𝙏𝙏𝙀𝙉𝙏𝙄𝙊𝙉  ───╮**\n\n‏**جـاري عـمـل تـاك لـلأعـضـاء.. 🚀**\n\n‏**╰────  𝙇𝙄𝙔𝙊𝙉  ────╯**",
            'parse_mode'=>"Markdown",
        ]);

        // مصفوفة افتراضية للأعضاء الذين تفاعلوا مع البوت (أو يمكنك منشن المشرفين كمثال)
        // للحصول على تاك حقيقي لكل الأعضاء، يجب أن يكون البوت يخزن id كل شخص يرسل رسالة
        
        // مثال لمنشن جماعي مرتب:
        $tag_msg = "‏**🔔 نـداء لـلـجـمـيـع :**\n\n";
        $tag_msg .= "‏— [الـإمـبـراطـور](tg://user?id=$from_id) \n"; // منشن صاحب الأمر
        
        // هنا نضع قائمة وهمية أو من الداتابيز الخاصة بك
        // إذا كان عندك ملف تخزين للأعضاء (users.txt) يمكنك عمل Loop هنا
        
        bot('sendMessage',[
            'chat_id'=>$chat_id,
            'text'=>$tag_msg . "\n‏**يـا حـلـويـن مـطـلـوب حـضـوركـم الآن! ✨**",
            'parse_mode'=>"Markdown"
        ]);

    } else {
        bot('sendMessage',[
            'chat_id'=>$chat_id,
            'text'=>"**⚠️ عـذراً عـزيـزي، هـذا الـأمـر لـلـأدمـنـيـة فـقـط!**",
            'reply_to_message_id'=>$message_id
        ]);
    }
}

// ==========================================
// 🎮 لعبة XO تيليجرام بوت - كود كامل
// ==========================================

$chat_id = $update->message->chat->id ?? $update->callback_query->message->chat->id;
$message_id = $update->message->message_id ?? $update->callback_query->message->message_id;
$from_id = $update->message->from->id ?? $update->callback_query->from->id;
$name = $update->message->from->first_name ?? $update->callback_query->from->first_name;
$text = $update->message->text ?? "";
$data = $update->callback_query->data ?? "";

// -------------------------
// 1️⃣ بدء اللعبة بالرد
// -------------------------
if ($text == "xo" || $text == "اكس او") {

    $reply = isset($update->message->reply_to_message);
    $reply_from_id = $reply ? $update->message->reply_to_message->from->id : null;
    $reply_name = $reply ? $update->message->reply_to_message->from->first_name : null;

    if (!$reply) {
        bot('sendMessage', [
            'chat_id' => $chat_id,
            'text' => "⚠️ **يرجى الرد على الشخص الذي تود تحديه!**",
            'reply_to_message_id' => $message_id
        ]);
        exit;
    }

    $p1_id = $from_id;
    $p2_id = $reply_from_id;
    $p1_name = $name;
    $p2_name = $reply_name;

    if ($p1_id == $p2_id) {
        bot('sendMessage', [
            'chat_id' => $chat_id,
            'text' => "⚠️ **عذراً يا بطل، لا يمكنك تحدي نفسك!**",
            'reply_to_message_id' => $message_id
        ]);
        exit;
    }

    // لوحة اللعبة - 9 مربعات + زر إنهاء
    $keyboard = [
        [
            ['text'=>'⬜','callback_data'=>"xo#1#$p1_id#$p2_id#x"],
            ['text'=>'⬜','callback_data'=>"xo#2#$p1_id#$p2_id#x"],
            ['text'=>'⬜','callback_data'=>"xo#3#$p1_id#$p2_id#x"]
        ],
        [
            ['text'=>'⬜','callback_data'=>"xo#4#$p1_id#$p2_id#x"],
            ['text'=>'⬜','callback_data'=>"xo#5#$p1_id#$p2_id#x"],
            ['text'=>'⬜','callback_data'=>"xo#6#$p1_id#$p2_id#x"]
        ],
        [
            ['text'=>'⬜','callback_data'=>"xo#7#$p1_id#$p2_id#x"],
            ['text'=>'⬜','callback_data'=>"xo#8#$p1_id#$p2_id#x"],
            ['text'=>'⬜','callback_data'=>"xo#9#$p1_id#$p2_id#x"]
        ],
        [
            ['text'=>'إنهاء اللعبة 🏳️','callback_data'=>"exit_xo#$p1_id#$p2_id"]
        ]
    ];

    bot('sendMessage', [
        'chat_id'=>$chat_id,
        'text'=>"╭─── 🎮 𝙓𝙊 𝘾𝙃𝘼𝙇𝙇𝙀𝙉𝙂𝙀 ───╮

⚔️ **تم بدء التحدي بين:**
اللاعب الأول ❌ : [$p1_name](tg://user?id=$p1_id)
اللاعب الثاني ⭕ : [$p2_name](tg://user?id=$p2_id)

⎯⎯⎯⎯⎯⎯⎯⎯
الآن دور اللاعب : ❌
╰─────── 𝙇𝙄𝙔𝙊𝙉 ───────╯",
        'parse_mode'=>"Markdown",
        'reply_markup'=>json_encode(['inline_keyboard'=>$keyboard])
    ]);

}

// -------------------------
// 2️⃣ اللعب بالضغط على الأزرار
// -------------------------
if (preg_match('/^xo#/', $data)) {
    $ex = explode("#",$data);
    $pos = $ex[1];
    $p1 = $ex[2];
    $p2 = $ex[3];
    $turn = $ex[4];

    $keyboard = $update->callback_query->message->reply_markup->inline_keyboard;

    $active_id = ($turn == "x") ? $p1 : $p2;
    $symbol = ($turn == "x") ? "❌" : "⭕";
    $next_turn = ($turn == "x") ? "o" : "x";
    $next_symbol = ($turn == "x") ? "⭕" : "❌";

    // حماية اللاعب
    if ($from_id != $p1 && $from_id != $p2) {
        bot('answerCallbackQuery', [
            'callback_query_id'=>$update->callback_query->id,
            'text'=>"🚫 التحدي ليس لك يا بطل!",
            'show_alert'=>true
        ]);
        exit;
    }

    // التحقق من الدور
    if ($from_id != $active_id) {
        bot('answerCallbackQuery', [
            'callback_query_id'=>$update->callback_query->id,
            'text'=>"⏳ انتظر دور خصمك، لا تستعجل!",
            'show_alert'=>true
        ]);
        exit;
    }

    // تحديث الأزرار
    foreach ($keyboard as &$row){
        foreach ($row as &$btn){
            if($btn->callback_data == $data){
                $btn->text = $symbol;
                $btn->callback_data = "clicked"; // تم استخدام المربع
            } else {
                $b_ex = explode("#",$btn->callback_data);
                if($b_ex[0]=="xo"){
                    $btn->callback_data = "xo#".$b_ex[1]."#$p1#$p2#$next_turn";
                }
            }
        }
    }

    bot('editMessageText', [
        'chat_id'=>$chat_id,
        'message_id'=>$message_id,
        'text'=>"🎮 تحدي 𝙓𝙊 مستمر..
❌ : [اللاعب الأول](tg://user?id=$p1)
⭕ : [اللاعب الثاني](tg://user?id=$p2)
⎯⎯⎯⎯⎯⎯⎯⎯
الآن دور اللاعب : $next_symbol",
        'parse_mode'=>"Markdown",
        'reply_markup'=>json_encode(['inline_keyboard'=>$keyboard])
    ]);
}

// -------------------------
// 3️⃣ إنهاء اللعبة
// -------------------------
if (preg_match('/^exit_xo#/', $data)){
    $ex = explode("#",$data);
    $p1 = $ex[1];
    $p2 = $ex[2];

    if ($from_id == $p1 || $from_id == $p2){
        bot('editMessageText', [
            'chat_id'=>$chat_id,
            'message_id'=>$message_id,
            'text'=>"🚫 **تم إنهاء التحدي وإلغاء اللعبة.**"
        ]);
    }
}

// ==========================
// 🎯 ملاحظة:
// يجب تعريف دالة bot($method, $datas) وتشغيل البوت عبر webhook
// ==========================


if($text){
    // 1. مصفوفة صيغ الصلاة على النبي (30 صيغة مختلفة)
    $salawat_list = [
        "صلي على محمد", "صلى على محمد", "صل على محمد", "اللهم صلي على محمد", "اللهم صل على محمد",
        "اللهم صلى على محمد", "صلو على النبي", "صلوا على النبي", "صلي على النبي", "صلى على النبي",
        "صلي على محمد وال محمد", "اللهم صل على محمد وال محمد", "اللهم صلي على محمد وال محمد",
        "يا نبي", "يا رسول الله", "الصلاة على النبي", "صلوا عليه", "صلي عليه", "صلى عليه",
        "صلو عليه", "اللهم صل على النبي", "صلوا على رسول الله", "صلي على رسول الله",
        "صلى الله عليه وسلم", "صلوات الله عليه", "اللهم صلي وسلم على نبينا محمد",
        "صل على محمد وال محمد الطيبين الطاهرين", "صلي على محمد وال محمد وعجل فرجهم",
        "يا محمد", "اللهم صل على نبينا محمد"
    ];

    // 2. مصفوفة الردود (20 رد فخم ومنوع)
    $salawat_replies = [
        "‏**اللهم صلِّ على محمد وآل محمد الطيبين الطاهرين 🕊️✨**",
        "‏**صلوات الله وسلامه عليك يا حبيب الله محمد 💚**",
        "‏**اللهم صلِّ وسلم وبارك على نبينا محمد وعلى آله وصحبه أجمعين 🌹**",
        "‏**عطّر فمك بالصلاة على محمد وآل محمد.. اللهم صلِّ على محمد وآل محمد 💠**",
        "‏**صلى الله عليه وعلى آله وصحبه وسلم تسليماً كثيراً 🕊️**",
        "‏**أفضل الصلاة والسلام على سيد المرسلين وخاتم النبيين 👑✨**",
        "‏**اللهم صلِّ على محمد وآل محمد وعجل فرجهم والعن عدوهم 💎**",
        "‏**بذكر الصلاة على محمد وآل محمد تُقضى الحوائج.. اللهم صلِّ على محمد 🤲✨**",
        "‏**صلى الله عليك يا علم الهدى، اللهم صلِّ على محمد وآل محمد 🌈**",
        "‏**صلوات ربي وسلامه عليك يا أبا القاسم يا رسول الله 💚**",
        "‏**اللهم صلِّ على محمد كما صليت على إبراهيم وآل إبراهيم إنك حميد مجيد 📜**",
        "‏**فإن الصلاة عليه نور.. اللهم صلِّ على محمد وآل محمد 💡✨**",
        "‏**يا ربِّ صلِّ وسلم دائماً أبداً على حبيبك خير الخلق كلهم 🌹**",
        "‏**اللهم صلِّ على محمد وآل محمد صلاةً تفتح لنا بها أبواب الخير 🕊️**",
        "‏**صلى الله عليه وسلم، جزاك الله خيراً على هذا الذكر الطيب 🌿**",
        "‏**ما ذكر اسم محمد في ضيق إلا واتسع.. اللهم صلِّ على محمد 💎**",
        "‏**اللهم اجعلنا من المصلين عليه والوارثين لحوضه.. اللهم صلِّ على محمد 🤲**",
        "‏**صلوات الله عليك يا من نورت الوجود.. اللهم صلِّ على محمد وآل محمد ✨**",
        "‏**اللهم صلِّ على محمد وآل محمد وعجل فرجهم وسهل مخرجهم 💠**",
        "‏**عليه أفضل الصلاة وأتم التسليم.. نورت الكروب بهذا الذكر العظيم 👑**"
    ];

    // 3. التنفيذ الذكي
    if(in_array($text, $salawat_list)){
        $reply = $salawat_replies[array_rand($salawat_replies)];
        bot('sendMessage',[
            'chat_id'=>$chat_id,
            'text'=>$reply,
            'reply_to_message_id'=>$message_id,
            'parse_mode'=>"Markdown"
        ]);
    }
}
if($text){
    // 1. مصفوفة أسماء البرامج والمنصات (15 كلمة)
    $social_apps = [
        "انستا", "انستقرام", "تيك توك", "تيكتوك", "فيس بوك", "فيسبوك", "سناب", "سناب شات",
        "تليجرام", "تلي", "واتساب", "واتس", "يوتيوب", "قناتي", "حسابي"
    ];

    // 2. مصفوفة الردود القوية والعراقية (15 رد مختلف)
    $app_responses = [
        "‏**عيني إحنا بكروب مو بسوق مريدي، عوفنا من الانستا والبرامج! ⛔**",
        "‏**حبيبي لا تسوي دعاية، إحنا هنا للونسة مو للإعلانات 🙄**",
        "‏**الوضع كروب ودردشة، مو محل ترويج تيك توك.. اركد شوية! ✋**",
        "‏**عوفنا من السوشيال ميديا، خلونا نسولف ونضحك هنا أحسن 🦁**",
        "‏**ترى إحنا بكروب ليون الملك، مو بمكتب إعلانات فيس بوك! 👑**",
        "‏**يا أخي إحنا بكروب محترم، مو وقت حسابات وقنوات هسه ❌**",
        "‏**اركد يابة، لا تخبصنا بالبرامج.. سولف ويانه هنا وبس ✨**",
        "‏**ممنوع الترويج هنا، الكروب للدردشة مو للمحلات التجارية! 🛑**",
        "‏**حبيبي عوف البرامج بصفحة، وركز ويانه بالكروب لا تطردك الإدارة 👞**",
        "‏**ترى ملينا من سالفة 'ضيفوني وشوفوني'، إحنا هنا عائلة وحدة 🌹**",
        "‏**الكروب للوناسة، مو لنشر اليوتيوب والقنوات.. انتبه يابة! ⚠️**",
        "‏**خوية والله عرفنا عندك حساب، بس هسه مو وقته.. خلنا بالكروب 💬**",
        "‏**ممنوع النشر الخارجي، احترم قوانين الإمبراطورية يا بطل 🦁**",
        "‏**عيني مو محل هو، هنا كروب رسمي للأصدقاء وبس! ❌**",
        "‏**لا تخليني أستخدم 'البوت المطرقة' وياك.. عوف البرامج هسه! 🔨**"
    ];

    // 3. التنفيذ الذكي (البحث عن الكلمة داخل النص)
    foreach($social_apps as $app){
        if(mb_stripos($text, $app) !== false){
            $reply = $app_responses[array_rand($app_responses)];
            bot('sendMessage',[
                'chat_id'=>$chat_id,
                'text'=>$reply,
                'reply_to_message_id'=>$message_id,
                'parse_mode'=>"Markdown"
            ]);
            break; // نكتفي برد واحد فقط
        }
    }
}



if($text){
    // 1. مصفوفة كلمات العركات والطك (80 كلمة/جملة)
    $fight_keys = [
        "شكو ماكو", "طبلجة", "عركة", "مشكلة", "طك", "اكتلك", "اذبحك", "سحك", "دفرة", "بوكس", 
        "راشدي", "دم", "يطلع دم", "اشكه", "صكار", "انعل", "كواد", "فرخ", "ادبز", "ساقط", 
        "عارات", "جمبازي", "لوكي", "ملطلط", "فاشل", "خسيس", "نذل", "جبان", "شرد", "طفر", 
        "انهزم", "شراني", "اعصاب", "لا تندك", "اندك بيك", "اهينك", "اسحكك", "حيوان", "مطيرجي", "عربيد", 
        "صاقط", "دايح", "فايت", "طاب", "طلعته", "دفنته", "موت", "كتل", "ذبح", "سجين", 
        "مسدس", "طلقة", "شاجور", "نار", "حرك", "فجر", "انفجار", "هجوم", "دمر", "تفلش", 
        "اويلي يابة", "اويلي", "يابة", "ولك", "ولج", "يا واد", "يا نذل", "شمر", "ركض", "سحل", 
        "مصلحة", "جذب", "قندرة", "نعال", "قذر", "تفل", "تفة", "سز", "ناقص", "بلا تربية"
    ];

    // 2. مصفوفة ردود الهيبة والرزالة (70 رد متباعد وفخم)
    $fight_responses = [
        "‏ارڪـد يـا بـطـل لا تـطـلـع دم بـالـڪـروب 😂",
        "‏هـيـبـة وصـڪـار وعـيـنـڪ حـارة يـا ذيـب 🦅",
        "‏أويـلـي يـابـة عـلـى هـالـشـرارة الـطـالـعـة مـن وجـهـڪ 🔥",
        "‏طـالـع سـبـع ومـا تـهـاب الـمـوت يـا بـطـل 🦁",
        "‏ارڪـد عـيـنـي الـثـقـل صـنـعـة والـعـرڪـة مـو لـلـتـرفـيـن 🤫",
        "‏هـيـبـة مـن يـطـب الإمـبـراطـور الـڪـل يـسـڪـت 👑",
        "‏طـالـع صـڪـار والـتـاريـخ يـشـهـد بـأفـعـالـڪ ✨",
        "‏يـا ويـلـي عـلـى هـالـهـيـبـة تـرعـب الـمـنـطـقـة ڪـلـهـا 🛡️",
        "‏طـالـع ذيـب ومـا تـعـرف الـخـوف بـيـا بـاب 🐺",
        "‏ارڪـد يـا مـعـدل لا تـفـلـش الـڪـروب عـلـى رؤوسـهـم 😂",
        "‏طـالـع تـفـلـيـش والـيـنـدڪ بـيـڪ يـنـدفـن بـمـڪـانـه 🔥",
        "‏يـا بـعـد روحـي سـوالـفـڪ هـيـبـة وطـبـلـجـة مـلـڪـيـة ✨",
        "‏طـالـع صـقـر ويـحـوم عـالـفـرائـس بـڪـل ثـقـة 🦅",
        "‏ارڪـد يـا وجـه الـسـعـد لا تـسـويـهـا عـرڪـات ومـشـاڪـل 🌙",
        "‏هـيـبـة ووقـار وأصـل مـعـدل ومـا يـنـهـز 💎",
        "‏طـالـع صـڪـار وعـيـونـڪ تـحـچـي هـيـبـة صـافـيـة 🦅",
        "‏أويـلـي يـابـة هـذا الـبـطـل الـي يـطـلـع دم بـالـحـق ❤️",
        "‏طـالـع نـمـر ومـا تـرضـى بـالـذل أبـداً 🏆",
        "‏ارڪـد عـيـنـي الـهـيـبـة مـو بـالـصـوت بـالافـعـال ✨",
        "‏أنـت وبـس والـبـاقـي ڪـلـهـا تـصـفـيـط حـچـي 🤫",
        "‏طـالـع فـد شـي خـرآفـي والـڪـل تـحـسـبـلـڪ حـسـاب 👑",
        "‏يـا مـيـة هـلا بـالـسـبـع الـي يـنـور الإمـبـراطـوريـة 🦁",
        "‏طـالـع ذيـب والـذيـب مـا يـاڪـل غـيـر الـسـمـان 🐺",
        "‏ارڪـد يـا بـطـل لا تـخـلـيـنـا نـطـلـب إسـعـاف هـسـة 😂",
        "‏هـيـبـة هـزت ڪـيـان الـڪـروب بـأول حـرف 🔥",
        "‏طـالـع مـلـڪ والـمـلـوڪ مـا تـنـزل لـلـصـغـار 👑",
        "‏يـا ويـلـي عـلـى الـمـراچـل الـطـالـعـة مـن عـيـونـڪ ✨",
        "‏طـالـع فـارس بـزمـن الـمـلـطـلـطـيـن 🛡️",
        "‏ارڪـد عـيـنـي بـيـنـت الـسـبـاع بـوڪـت الـشـدة 🦅",
        "‏هـذا الـذي يـسـمـونـه الـصـڪـار الأصـيـل 💎",
        "‏طـالـع چـنـڪ الأسـد بـنـص الـغـابـة نـورتـنـا 🦁",
        "‏يـا هـلا بـالـلـي مـا يـنـهـز مـن أڪـبـر مـشـڪـلـة ✨",
        "‏ارڪـد يـا بـعـد جـبـدي الـرزانـة صـنـعـتـڪ 🧡",
        "‏طـالـع نـادرة ومـا مـنـڪ نـسـخـتـيـن بـهـالـمـرجـلـة 🏆",
        "‏هـيـبـة وقـوة وشـجـاعـة جـمـعـتـهـن ڪـلـهـن بـيـڪ ✨",
        "‏طـالـع تـفـلـيـش والـيـحـچـي ويـاڪ يـنـدك بـحـايـط 🔥",
        "‏أويـلـي يـابـة هـالـنـور الـهـيـبـي دمرنا 🌟",
        "‏طـالـع سـبـع مـعـدل ومـا تـنـسـحـڪ أبـداً 🦁",
        "‏ارڪـد يـا مـلـڪ الإمـبـراطـوريـة مـڪـانـڪ تـاج 👑",
        "‏هـذا الـبـطـل الـي نـفـتـخـر بـي بـالـڪـروب ✨",
        "‏طـالـع صـڪـار وعـيـنـڪ تـحـرسـڪ مـن الـحـسـد 🧿",
        "‏يـا ويـلـي عـلـى الـثـقـل والـهـيـبـة الـعـراقـيـة 🇮🇶",
        "‏طـالـع چـنـڪ ضـوه الـنـار بـالـلـيـل الـمـظـلـم 🔥",
        "‏ارڪـد يـا بـطـل بـيـنـت أفـعـالـڪ بـالـمـيـدان 🏆",
        "‏هـيـبـة تـهـز جـبـال ومـا تـهـزڪ ڪـلـمـة ✨",
        "‏طـالـع ذيـب بـالـتـفـڪـيـر وصـقـر بـالـتـنـفـيـذ 🦅",
        "‏أويـلـي يـابـة شـلـون شـخـصـيـة تـفـرض نـفـسـهـا 😍",
        "‏طـالـع مـهـيـب والـڪـل يـوقـفـلـڪ إحـتـرام 👑",
        "‏ارڪـد يـا بـعـد روحي الـسـبـاع تـحـچـي قـلـيـل ✨",
        "‏هـذا الـتـرتـيـب الـي يـرفـع الـراس والـلـه 💎",
        "‏طـالـع چـنـڪ الـسـيـف الـبـتـار بـيـد الـشـجـاع 🗡️",
        "‏يـا هـلا بـالـلـي يـدب الـرعـب بـقـلـوب الـخـصـوم 🦁",
        "‏ارڪـد عـيـنـي الـهـيـبـة صـارت بـأسـمـڪ مـسـجـلـة ✨",
        "‏طـالـع تـفـلـيـش والـلـه يـا صـڪـار الـسـاحـة 🔥",
        "‏أويـلـي يـابـة عـلـى هـالـنـفـس الـقـويـة ✨",
        "‏طـالـع سـبـع ومـعدل مـن ضـهـر سـبـع 🦁",
        "‏هـيـبـة تـرعـب حـتـى الـخـيـال يـا بـطـل 🌑",
        "‏طـالـع چـنـڪ الـنـمـر بـوقـت الـهـجـوم 🐆",
        "‏ارڪـد يـا مـلـڪ الـهـيـبـة والـمـراچـل 👑",
        "‏يـا هـلا بـالـسـبـع الـي يـنـشـد بـي الـضـهـر 🛡️",
        "‏طـالـع صـڪـار وأفـعـالـڪ تـحـچـي عـنـڪ 💎",
        "‏أويـلـي يـابـة هـذا الـعـراقي الأصـيـل الـمـعـدل 🇮🇶",
        "‏طـالـع هـيـبـة ووقـار تـسـوى مـلـيـون زلـمـة 🏆",
        "‏ارڪـد عـيـنـي الـبـطـل يـبـقـى بـطـل بـڪـل وڪـت ✨",
        "‏هـيـبـة تـفـرض نـفـسـهـا بـدون أي ڪـلام 🔥",
        "‏طـالـع ذيـب والـذيـاب تـهـابـڪ يـا سـبـع 🐺",
        "‏يـا مـيـة هـلا بـطـلـتـڪ الـمـهـيـبـة والـفـخـمـة 🌟",
        "‏طـالـع صـقـر ويـصـيـد بـالـمـاي الـعـڪـر 🦅",
        "‏ارڪـد يـا بـطـل الإمـبـراطـوريـة عـزيـزة بـيـڪ 👑",
        "‏أويـلـي يـابـة عـلـى هـالـرجـولـة الـمـا تـنـهـز ✨"
    ];

    // 3. التنفيذ الذكي (البحث في 80 كلمة والرد من 70 خيار)
    foreach($fight_keys as $key){
        if(mb_stripos($text, $key) !== false){
            $reply = $fight_responses[array_rand($fight_responses)];
            bot('sendMessage',[
                'chat_id' => $chat_id,
                'text' => $reply,
                'reply_to_message_id' => $message_id,
                'parse_mode' => "Markdown"
            ]);
            break;
        }
    }
}

if($text){
    // 1. مصفوفة الكلمات المفتاحية (400 كلمة وجملة بلهجة عراقية شاملة)
    $keywords = [
        // ترحيب وسلام (50)
        "هلو", "هلوات", "هلاو", "هلاوات", "شلونكم", "شلونك", "شلونج", "السلام عليكم", "سلام عليكم", "صباح الخير", 
        "مساء الخير", "صباحو", "مساء الورد", "نورت", "نورتو", "منورين", "يا الله", "حي الله", "هلا بيك", "هلا عيني",
        "شلون الصحة", "شلون الاحوال", "شكو ماكو", "شونكم", "شونج", "هلو يابة", "يا هلا", "السلآم عليكم", "قوة", "صح النوم",
        "صباح العسل", "مساء الجمال", "هلو شباب", "هلو بنات", "هلو قلبي", "هلو عيوني", "يا الله بالخير", "نورت الكروب", "شخبارك", "شخبارج",
        "شخباركم", "هلوو", "هلاوو", "سلامي", "يا هيبة", "نورتي", "اشلونكم", "اشلونك", "هلو كبدي", "شونكم عيوني",

        // مشاعر وضوجة (50)
        "ضوجة", "ضايج", "مليت", "تعبان", "ميت", "جوعان", "جعت", "نعسان", "اريد انام", "مهموم", 
        "مقهور", "مخنوك", "مخنوكة", "ملل", "شوكت نخلص", "تعبت", "مريض", "دحجي", "سولف", "اريد اضحك",
        "ميت ضحك", "هههه", "ههههه", "فديت", "اريد اكل", "عطشان", "برد", "حارة", "صيف", "شتا",
        "مطر", "وحدي", "حديقة", "اريد اتزوج", "خطوبة", "عرس", "حب", "غرام", "اعشقك", "تحبني",
        "اكرهك", "غبي", "ثول", "نجب", "انجب", "ولي", "باي", "رايح", "تصبحون", "وداعا",

        // أسئلة واستفسارات (50)
        "شنو", "منو", "وين", "شوكت", "شكد", "ليش", "كيف", "من انت", "شسمك", "بوت", 
        "ليون", "برنامج", "تطبيق", "تحديث", "جديد", "قديم", "وينكم", "محد", "موجود", "نايمين",
        "كاعدين", "شكو", "بشر", "سمعت", "خبر", "صدك", "كذب", "والله", "بربك", "حلف",
        "شلونك ضلعي", "شخبارك عيني", "الوضع شنو", "منو موجود", "اشو محد", "بشروني", "مساعدة", "سؤال", "جواب", "لغز",
        "حزورة", "قصة", "سالفة", "منو انتو", "عراقي", "بغداد", "بصرة", "موصل", "ناصرية", "كربلاء",

        // كلمات عامة (250 كلمة إضافية لتكملة الـ 400)
        "كفو", "بطل", "سبع", "ذيب", "اسد", "نمر", "صقر", "غالي", "ذهب", "لوز", 
        "كيك", "نزاكة", "مرتب", "هيبة", "صكار", "ضلعي", "حبيبي", "عيني", "قلبي", "روحي",
        "جبد", "كيمر", "عسل", "شاي", "كهوة", "صمون", "دولمة", "باجة", "تمن", "قيمة",
        "هريسة", "زيارة", "مشاية", "عيد", "فرح", "دمعة", "ضحكة", "تليفون", "شحن", "نت",
        "ضعيف", "ببجي", "لودو", "طوبة", "ريال", "مدريد", "برشلونة", "ميسي", "رونالدو", "فوز",
        "خسارة", "ملعب", "اغنية", "طرب", "وناسة", "سهرة", "ليل", "نهار", "سما", "كاع",
        "بحر", "نهر", "سمك", "دعاء", "صلاة", "صوم", "سفر", "طيارة", "سيارة", "سايق",
        "تكسي", "بيت", "شارع", "درب", "فلوس", "راتب", "دوام", "مدرسة", "كلية", "دراسة",
        "امتحان", "نجاح", "رسوب", "استاذ", "دكتور", "شرطي", "جيش", "وطن", "علم", "نشيد",
        "شعر", "دارمي", "ابوذية", "قفل", "مفتاح", "باب", "شباك", "هوة", "نور", "ظلمة",
        "شمس", "كمر", "نجمة", "غيمة", "ثلج", "برد", "نار", "دخان", "حريق", "اطفاء",
        "اسعاف", "مستشفى", "صيدلية", "علاج", "دوه", "صحة", "عافية", "قوة", "ضعف", "طول",
        "قصر", "وزن", "اكل", "شرب", "نوم", "كعدة", "روحة", "جية", "ركض", "مشي",
        "سباحة", "طيران", "حلم", "خيال", "حقيقة", "سر", "علن", "صداقة", "اخوة", "وفاء",
        "خيانة", "كذب", "صدق", "امانة", "خوف", "شجاعة", "ذوق", "ادب", "اخلاق", "تربية",
        "عائلة", "اهل", "ناس", "عالم", "كون", "فضاء", "كوكب", "مجرة", "ارض", "شجر",
        "ورد", "زرع", "طير", "حيوان", "جماد", "الوان", "ابيض", "اسود", "احمر", "ازرق",
        "اخضر", "اصفر", "وردي", "بنفسجي", "ذهبي", "فضي", "حديد", "نحاس", "خشب", "بلاستيك",
        "زجاج", "ورق", "قلم", "كتاب", "دفتر", "جنطة", "هدوم", "لبس", "كشخة", "اناقة",
        "ساعة", "نظارة", "محبس", "سوار", "كلادة", "عطر", "مكياج", "شعر", "وجه", "عين",
        "خشم", "حلك", "اذن", "ايد", "رجل", "كلب", "عقل", "تفكير", "ذكاء", "غباء",
        "سرعة", "بطء", "هدوء", "ضوضاء", "صوت", "سكوت", "كلام", "لفظ", "معنى", "حرف",
        "كلمة", "جملة", "نص", "رسالة", "اشعار", "تنبيه", "تذكير", "نسيان", "ذاكرة", "ماضي",
        "حاضر", "مستقبل", "وقت", "تاريخ", "يوم", "شهر", "سنة", "قرن", "جيل", "شباب",
        "اطفال", "شيب", "عجوز", "بنية", "ولد", "رجال", "نسوان", "زلمة", "بطلة", "ملك",
        "ملكة", "امير", "اميرة", "قصر", "قلعة", "خيمة", "بيت", "شقة", "غرفة", "مطبخ"
    ];

    // 2. مصفوفة الردود (الردود الملكية المتباعدة)
    $social_replies = [
        "‏مـسـائـڪ عـسـل يـڪـلـبـي 🧡",
        "‏يـا بـعـد روحـي سـوالـفـڪ تـرد الـروح ✨",
        "‏هـيـبـة ووقـار طـالـع چـنـڪ ڪـمـر بـوسـط الـسـمـاء 🌕",
        "‏يـا هـلا بـالـلـي لـفـا نـورت الإمـبـراطـوريـة يـا طـيـب 🌿",
        "‏ارڪـد يـابـة هـالـحـلاوة دمـرت أعـصـاب الـڪـروب 😂",
        "‏طـالـع چـنـڪ ڪـيـڪـة نـاقـصـڪ بـس شـويـة شـڪـر 🍰",
        "‏هـيـبـة ومـا تـنـهـز يـا صـقـر الـعـرب وعـزهـا 🦅",
        "‏نـورتـنـا يـا ضـوه عـيـونـي عـسـاهـا دوم هـالـضـحـڪـة 😊",
        "‏مـسـائـڪ ورد وجـوري يـا أصـل الـذوق ڪـلـه 🌹",
        "‏طـالـع قـطـعـة مـن الـجـنـة ربـي يـحـمـيـڪ مـن الـعـيـن 🧿",
        "‏يـا مـيـة هـلا بـجـيـتـڪ الـڪـروب ازدهـر بـوجـودڪ ✨",
        "‏بـعـد قـلـبـي طـالـع تـرف وڪـلـش نـزاڪـة 💎",
        "‏شـلـونـڪ يـا ذهـب عـسـاڪ دوم بـخـيـر وراحـة بـال ❤️",
        "‏حـي الله هـالـطـلـة الـمـلـڪـيـة نـورتـنـا يـا بـطـل 🦁",
        "‏أنـت والـجـمـال قـصـة مـا تـنـتـهـي يـا مـلـڪ الأنـاقـة 👑",
        "‏طـالـع چـنـڪ الـعـافـيـة نـورتـنـا يـا وجـه الـخـيـر 🌟",
        "‏مـسـائـڪ ڪـيـمـر سـدة يـا أحـلـى مـن الـعـسـل 🥛",
        "‏طـالـع غـزال والـعـيـون تـحـرسـڪ مـن الـحـسـاد ✨",
        "‏يـا ويـلـي عـلـى الأنـاقـة طـالـع عـريـس الـيـوم 🤵",
        "‏ذوقـڪ تـرف مـثـل روحـڪ الـطـيـبة يـا وردة 🌸",
        "‏ارڪـد عـيـنـي لا تـخـبـصـنـا بـجـمـالـڪ الـزايد 🤫",
        "‏طـالـع چـنـڪ ضـوه الـصـبـح نـورتـنـا يـا غـالـي ☀️",
        "‏أنـا أشـهـد إنـڪ نـمـبـر وان بـهـالـڪـروب 🏆",
        "‏طـالـع لـوز مـا مـحـتـاج أي فـلـتـر ولا تـعـديـل ✨",
        "‏مـسـائـڪ مـسـڪ وعـنـبـر يـا أغـلـى مـن الـروح 🧡",
        "‏طـالـع تـفـلـيـش والله دمـرت مـوازيـن الـجـمـال 🔥",
        "‏بـعـد جـبـدي شـلـون الـصـحـة عـسـاڪ مـرتـاح 🌹",
        "‏ذوقـڪ نـار دمـرت الـڪـروب بـهـالـطـلـة الـخـرافـيـة 🔥",
        "‏يـا مـيـة هـلا نـورتـنـا يـا سـبـع الإمـبـراطـوريـة 🦁",
        "‏نـورك غـطـى عـلـى الـڪـهـربـاء مـنـورنـا يـا ورد 💡"
    ];

    // 3. المحرك الذكي (البحث في الـ 400 كلمة والرد)
    foreach($keywords as $key){
        if(mb_stripos($text, $key) !== false){
            $reply = $social_replies[array_rand($social_replies)];
            bot('sendMessage',[
                'chat_id' => $chat_id,
                'text' => $reply,
                'reply_to_message_id' => $message_id,
                'parse_mode' => "Markdown"
            ]);
            break; 
        }
    }
}

if($text){
    // 1. مصفوفة كلمات الدعوة للعب (50 صيغة مختلفة)
    $play_calls = [
        "منو يلعب", "تلعبون", "منو يلعب وياي", "خل نلعب", "لعبة", "العاب", "منو يشارك", 
        "تحدي", "مسابقة", "منو كفو يلعب", "شاركونا", "خل نتونس", "العاب بوت", "بوت العب",
        "لعبوني", "اريد العب", "منو كد التحدي", "فعالية", "فعاليات", "منو موجود يلعب",
        "شباب تلعبون", "بنات تلعبون", "منو يلعب لودو", "منو يلعب ببجي", "منو يلعب طاولي",
        "تعالوا نلعب", "وين اللاعبين", "وين الأبطال", "خل نسوي مسابقة", "منو يربح",
        "تحدوني", "اكو لعبة", "شنو نلعب", "لعبونا", "اكو مسابقة", "منو يشارك باللعبة",
        "راح نلعب", "بدت اللعبة", "منو يدخل باللعبة", "وينكم تعالوا نلعب", "العب وياي",
        "لعبة جديدة", "فعالية الكروب", "لعبونا شي", "ضوجة خل نلعب", "منو يريد يلعب",
        "تفاعلوا خل نلعب", "اللاعبين وين", "منو جاهز للعب", "لعبة ذكاء"
    ];

    // 2. مصفوفة الردود الحماسية (10 ردود قوية)
    $play_replies = [
        "‏**أنا جاهز! بس بشرط، الخسران يعشي الكروب كله 🥙😂**",
        "‏**وياكم وياكم! ليون دائماً كد التحدي.. شنو اللعبة؟ 🦁🔥**",
        "‏**أنا العب، بس ترى أنا محترف لا تبجون بعدين 😋🏆**",
        "‏**يلا يا أبطال، منو يفتح اللعبة وهسة أجي أدمركم؟ 💣✨**",
        "‏**الكروب صاير نار! يلا وين اللاعبين الحقيقيين؟ 📡🔥**",
        "‏**أنا الحكم واللاعب بنفس الوقت، منو يتحداني؟ ⚖️😎**",
        "‏**عوفوا الضوجة وخلونا نلعب، الحياة وناسة ✨🎮**",
        "‏**يلا بدت الفعالية، أريد أقوى تفاعل من الإمبراطورية 👑🚀**",
        "‏**أنا أول واحد يلعب! بس لا تسوون تحالفات ضدي 🤝😂**",
        "‏**حي الله اللاعبين، الكروب نور بوجود الأبطال.. بلشوا! 🌟🎮**"
    ];

    // 3. التنفيذ الذكي
    foreach($play_calls as $call){
        if(mb_stripos($text, $call) !== false){
            $reply = $play_replies[array_rand($play_replies)];
            bot('sendMessage',[
                'chat_id'=>$chat_id,
                'text'=>$reply,
                'reply_to_message_id'=>$message_id,
                'parse_mode'=>"Markdown"
            ]);
            break; 
        }
    }
}
// 1. قاعدة بيانات الأسئلة (100 سؤال - وضعت لك عينة صعبة واحترافية)
$questions = [
    ["q" => "من هو العالم العربي الذي وضع أسس علم الجبر؟", "ok" => "الخوارزمي", "a" => "ابن الهيثم", "b" => "الخوارزمي", "c" => "ابن سينا", "d" => "الكندي"],
    ["q" => "ما هو العنصر الكيميائي الذي يرمز له بالرمز (Au)؟", "ok" => "الذهب", "a" => "الفضة", "b" => "الذهب", "c" => "النحاس", "d" => "الألمنيوم"],
    ["q" => "في أي عام وقعت معركة ذي قار المشهورة؟", "ok" => "610 ميلادي", "a" => "550 ميلادي", "b" => "610 ميلادي", "c" => "700 ميلادي", "d" => "630 ميلادي"],
    ["q" => "ما هي الدولة التي تمتلك أكبر عدد من الأهرامات في العالم؟", "ok" => "السودان", "a" => "مصر", "b" => "المكسيك", "c" => "السودان", "d" => "البيرو"],
    ["q" => "كم عدد الخلايا العصبية في دماغ الإنسان تقريباً؟", "ok" => "86 مليار", "a" => "10 مليار", "b" => "50 مليار", "c" => "86 مليار", "d" => "200 مليار"],
    ["q" => "من هو القائد الذي فتح بلاد الأندلس؟", "ok" => "طارق بن زياد", "a" => "خالد بن الوليد", "b" => "طارق بن زياد", "c" => "عقبة بن نافع", "d" => "صلاح الدين"],
    ["q" => "ما هو أعمق خندق مائي في العالم؟", "ok" => "خندق ماريانا", "a" => "خندق تونجا", "b" => "خندق ماريانا", "c" => "خندق الفلبين", "d" => "خندق جاوا"],
    ["q" => "أي كوكب يلقب بالكوكب المنبطح لشدة ميلان محوره؟", "ok" => "أورانوس", "a" => "زحل", "b" => "نبتون", "c" => "أورانوس", "d" => "المريخ"],
    ["q" => "ما هي أسرع حشرة في العالم؟", "ok" => "اليعسوب", "a" => "الصرصور", "b" => "النحلة", "c" => "اليعسوب", "d" => "الذبابة"],
    ["q" => "من هو الأديب العربي الذي فاز بجائزة نوبل للآداب؟", "ok" => "نجيب محفوظ", "a" => "طه حسين", "b" => "نجيب محفوظ", "c" => "عباس العقاد", "d" => "جبران خليل"],
    // يمكنك إضافة الـ 90 سؤال البقية هنا بنفس الهيكل الدقيق...
];

// --- [ بدء اللعبة / أمر t ] ---
if($text == "من سيربح المليون" || $text == "t" || $text == "T" || $text == "المليون"){
    $r = array_rand($questions);
    $q = $questions[$r];
    
    // ترتيب الأزرار الثابت لضمان عدم تكرار الخيارات في الزر الواحد
    $options = [$q['a'], $q['b'], $q['c'], $q['d']];
    shuffle($options); // خلط الأماكن فقط

    bot('sendMessage', [
        'chat_id' => $chat_id,
        'text' => "‏**╭────  𝙇𝙄𝙔𝙊𝙉 𝙈𝙄𝙇𝙇𝙄𝙊𝙉  ────╮**\n\n" .
                  "‏**💰 مـسـابـقـة الـمـلـيـون (الأسئلة الصعبة)**\n" .
                  "‏⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n" .
                  "‏**❓ الـسـؤال :**\n" .
                  "‏**« ".$q['q']." »**\n\n" .
                  "‏**╰──────────────╯**",
        'parse_mode' => "Markdown",
        'reply_markup' => json_encode([
            'inline_keyboard' => [
                [['text' => "A: ".$options[0], 'callback_data' => "qz#".$options[0]."#".$q['ok']], ['text' => "B: ".$options[1], 'callback_data' => "qz#".$options[1]."#".$q['ok']]],
                [['text' => "C: ".$options[2], 'callback_data' => "qz#".$options[2]."#".$q['ok']], ['text' => "D: ".$options[3], 'callback_data' => "qz#".$options[3]."#".$q['ok']]]
            ]
        ])
    ]);
}

// --- [ معالجة الضغط على الإجابة ] ---
if(isset($update->callback_query)){
    $cb = $update->callback_query;
    $data = $cb->data;
    $cid = $cb->message->chat->id;
    $mid = $cb->message->message_id;
    $name = $cb->from->first_name;

    if(strpos($data, "qz#") !== false){
        $ex = explode("#", $data);
        $user_ans = $ex[1];
        $correct = $ex[2];

        if($user_ans == $correct){
            // ✅ رد الإجابة الصحيحة + إضافة حرف t
            bot('editMessageText', [
                'chat_id' => $cid,
                'message_id' => $mid,
                'text' => "‏**╭────  𝙇𝙄𝙔𝙊𝙉 𝙒𝙄𝙉  ────╮**\n\n" .
                          "‏**✅ والله بطل [$name]!**\n" .
                          "‏**جبتها صح رغم صعوبة السؤال ✨**\n\n" .
                          "‏**💰 ربحت معانا : 10,000 نقطة**\n" .
                          "‏⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n" .
                          "‏**🔄 للعب مرة أخرى أرسل حرف : ( t )**\n\n" .
                          "‏**╰──────────────╯**",
                'parse_mode' => "Markdown"
            ]);
        } else {
            // ❌ رد الإجابة الخاطئة والرزالة
            $fail_txt = [
                "خسرت يا فاشل! مو كتلك هاي للعباقرة؟ ❌",
                "تعيش وتاكل غيرها يا تعبان! الإجابة [$correct] 👞",
                "[$name] انسحك سحك! روح ادرس وتعال 😂",
                "خطأ يا فاشل! فضحكتنا كدام الكروب! ⛔"
            ];
            $rand_fail = $fail_txt[array_rand($fail_txt)];

            bot('editMessageText', [
                'chat_id' => $cid,
                'message_id' => $mid,
                'text' => "‏**╭────  𝙇𝙄𝙔𝙊𝙉 𝙇𝙊𝙎𝙀  ────╮**\n\n" .
                          "‏**❌ $rand_fail**\n" .
                          "‏**الجواب الصح جان : [ $correct ]**\n\n" .
                          "‏**🔄 للتعويض واللعب مرة أخرى أرسل : ( t )**\n\n" .
                          "‏**╰──────────────╯**",
                'parse_mode' => "Markdown"
            ]);
        }
    }
}
if($message->photo){
    // مصفوفة الـ 15 رد الفخمة والمتباعدة
    $photo_responses = [
        "‏يـا ويـلـي عـلـى هـالـجـمـال، نـورت الإمـبـراطـوريـة بـهـالـطـلـة 😍",
        "‏عـاشـت إيـدك عـلـى هـالـلـقـطـة، طـالـع چـنـڪ الـعـافـيـة ✨",
        "‏صـورة لـلـتـاريـخ، هـيـبـة ووقـار مـا مـطـروق أبـداً 👑",
        "‏ارڪـد يـا بـعـد روحـي، هـالـحـلاوة دمـرت أعـصـاب الـڪـروب 🔥",
        "‏طـالـع قـطـعـة مـن الـجـنـة، ربـي يـحـمـيـڪ مـن ڪـل عـيـن 🧿",
        "‏ذوقـڪ تـرف بـالـتـصـويـر، چـنـڪ لـوحـة رسـام عـالـمـي 🎨",
        "‏مـسـائـڪ مـثـل وجـهـڪ، مـنـورنـا بـهـالـصـورة الـتـرد الـروح 🌟",
        "‏أنـت والـجـمـال قـصـة مـا تـنـتـهـي، يـا مـلـڪ الأنـاقـة 💎",
        "‏طـالـع چـنـڪ ڪـمـر بـوسـط الـسـمـاء، نـورت الـقـلـعـة 🌕",
        "‏أويـلـي يـابـة عـلـى هـالـنـور، طـلـتـڪ تـسـوى الـڪـروب وأهـلـه ❤️",
        "‏هـيـبـة صـڪـور وطـلـة مـلـوڪ، عـاشـت هـالـوقـفـة الـبـطـلـة 🦅",
        "‏طـالـع چـنـڪ الـعـيـد، نـورتـنـا يـا فـرحـة هـالـمـڪـان 🎉",
        "‏فـديـت هـالـنـزاڪـة، صـورة تـفـتـح الـنـفـس والـلـه ✨",
        "‏ارڪـد يـا مـعـدل، هـالـصـورة لازم تـنـشـر بـأغـلـى الـمـجـلات 🏆",
        "‏طـالـع ذيـب والـهـيـبـة تـڪـطـر مـنـك ڪـطـر يـا سـبـع 🦁"
    ];

    $photo_reply = $photo_responses[array_rand($photo_responses)];

    bot('sendMessage',[
        'chat_id' => $chat_id,
        'text' => $photo_reply,
        'reply_to_message_id' => $message_id,
        'parse_mode' => "Markdown"
    ]);
}

if($text == "اضافة بايو" or $text == "تغيير البايو"){
    
    // سحب اسم الكروب للعرض فقط
    $c_name = $message->chat->title;
    
    $mega_bios = [
        // المجموعة 1: هيبة الإمبراطورية
        "❖￤لـلـنـاس ﭑݪفـخـآمـۿ والـࢪاقـيـة بـ [$c_name] ⁶\n\n• الـقـوانـيـن 📌\n\n• انـضـم بـشـخـصـيـة مـرتـبـة ↻\n• اي واحـد يـڪـمـز يـتـمـشـڪـل يـنـطـرد ؟\n• يـمـنـع↫الـسـيـاسـة↫ابـاحـيـة↫الـمـشـاڪـل 🚫\n• يـمـنـع↫الـسـب↫الـڪـفـر↫الـزحـف 🚫\n• يـمـنـع↫الـطـرد بـدون سـبـب 🚫\n• يـمـنـع↫الـخـاص بـدون إذل 🚫\n• اي شـخـص يـنـطـرد تـڪـتـبـون الـسـبـب 🚫\n• احـتـرام الـآدِمـن يـمـثـل أخـلاقـڪ ✨\n• الـتـفـاعـل يـرفـع رتـبـتـڪ بـالـقـلـعـة 💎\n• الـمـالـڪ↫ هـو صـاحـب الـقـرار الـأول 👑",

        // المجموعة 2: دستور القلعة
        "⚡️￤نـظـام الـسـيـادة الـصـارم بـ [$c_name] 🛡️\n\n• الـقـوانـيـن 📌\n\n• خـلـيـڪ ثـڪـيـل تـنـحـط عـالـراس ↻\n• الـمـشـاڪـل تـنـهـي وجـودڪ هـنـا 🔥\n• يـمـنـع↫الـروابـط↫الـإعـلانـات↫الـتـوجـيـه 🚫\n• يـمـنـع↫الـتـجـاوز↫الـغـلـط↫الـتـفـاهـة 🚫\n• الـزحـف يـؤدي لـلـطـرد الـفـوري 🐍\n• الـڪـروب لـلـخـوة الـنـظـيـفـة فـقـط ✨\n• الـبـوت مـراقـب لـڪـل صـغـيـرة وڪـبـيرة 🔍\n• تـواجـدڪ يـعـنـي احـتـرامـڪ لـلـنـظـام ↻\n• مـمـنـوع الـسـبـام وتـڪـرار الـرسايـل 🚫\n• الـمـالـڪ↫ تـاج الـرأس والـآمـر الـنـاهـي 👑",

        // المجموعة 3: عرش الفخامة
        "💎￤صـفـوة الـمـعـدلـيـن فـي [$c_name] 🦁\n\n• الـقـوانـيـن 📌\n\n• الـمـرجـلـة بـالـأفـعـال مـو بـالـطـلـطـلـة ↻\n• مـن يـغـلـط يـتـحـمـل نـتـيـجـة فـعـلـه 🔥\n• يـمـنـع↫الـطـائـفـيـة↫الـعـنـصـريـة 🚫\n• يـمـنـع↫الـبـصـمـات الـمـزعـجـة 🚫\n• يـمـنـع↫الـدخـول لـلـبـنـات خـاص 🚫\n• الـتـڪـرار يـعـرضـڪ لـلـڪـتـم الـمـؤقـت ↻\n• الـأوامـر تـنـفـذ بـدون نـقـاش 🛡️\n• ڪـن ذيـب بـسـوالـفـڪ وتـرف بـأخـلاقـڪ ✨\n• الـتـزم لـتـبـقـى مـن الـمـقـربـيـن ↻\n• الـمـالـڪ↫ هـيـبـة الـمـڪـان وذوقـه 👑",

        // المجموعة 4: مملكة الصقور
        "🦅￤نـخـبـة الـعـراق فـي [$c_name] 🇮🇶\n\n• الـقـوانـيـن 📌\n\n• نـورتـنـا يـا بـعـد روحـي وتـفـاعـل ↻\n• الـهـدوء وڪـت الـلـيـل مـطـلـوب ✨\n• يـمـنـع↫الـتـجـاوز بـالـصـور 🚫\n• يـمـنـع↫إزعـاج الـمـشـرفـيـن 🚫\n• يـمـنـع↫طـلـب الـمـديـر لـلـخـاص 🚫\n• الـتـفـاعـل الـمـسـتـمـر يـنـطـيـڪ رتـبـة 🏅\n• أي فـتـنـة تـنـتـهـي بـالـطـرد 🔥\n• الـصـداقـة والـخـوة أسـاس هـالـمـڪـان ❤️\n• خـلـيـڪ مـتـواجـد لـيـصـيـر لـقـبـڪ هـيـبـة ↻\n• الـمـالـڪ↫ قـائد الـصـقـور والـهـيـبـة 👑",

        // المجموعة 5: ساحة المراجـل
        "⚔️￤مـيـدان الـسـبـاع بـ [$c_name] 🦁\n\n• الـقـوانـيـن 📌\n\n• الـثـقـل واجـب والـمـيـزان هـو الـأدب ↻\n• مـن يـغـادر يـسـقـط اسـمـه مـن الـسـجـل 🛡️\n• يـمـنـع↫الـتـحـريـض عـلـى الـمـشـاڪـل 🚫\n• يـمـنـع↫الـسـوالـف الـتـافـهـة 🚫\n• يـمـنـع↫تـشـويـه سـمـعـة الـڪـروب 🚫\n• الـبـوت مـزود بـرادار لـڪـشـف الـخـمـط 🔍\n• احـتـرم الـقـوانـيـن لـتـبـقـى مـعـزز ✨\n• الـمـڪـان لـلـمـعـدلـيـن فـقـط ↻\n• لا فـرق بـيـن عـضـو وآدِمـن ❤️\n• الـمـالـڪ↫ عـز الـنـفـس والـوقـار 👑",

        // المجموعة 6: قمة الذوق
        "🌸￤عـالـم الـتـرف والـذوق بـ [$c_name] ✨\n\n• الـقـوانـيـن 📌\n\n• اضحـك وفـرفـش بـس بـحـدود الأدب ↻\n• الـزحـف والـتـمـلـق مـرفـوض تـمـامـاً 🚫\n• يـمـنـع↫الـتـدخـل بـخـصـوصـيـات الـأعـضـاء 🚫\n• يـمـنـع↫الـتـڪـلـم بـلـهـجـات غـيـر مـفـهـومـة 🚫\n• يـمـنـع↫نـشـر حـسـابـات الـتـواصـل 🚫\n• الـتـواضـع يـرفـعـڪ والـتـڪـبـر يـطـردڪ ↻\n• ڪـن تـرف بـسـوالـفـڪ يـا وردة ✨\n• الـڪـروب جـزء مـن عـائـلـتـنـا ❤️\n• الـصـدق مـطـلـوب بـڪـل ڪـلـمـة ↻\n• الـمـالـڪ↫ نـبـع الـطـيـب والـأخـلاق 👑",

        // المجموعة 7: حـصن الـأمان
        "🛡️￤حـصـن الـأمان فـي [$c_name] ⁶\n\n• الـقـوانـيـن 📌\n\n• لا تـصـيـر لـوڪـي خـلـيـڪ بـشـخـصـيـتـڪ ↻\n• الـغـلـط مـرة والـثـانـيـة حـظـر نـهـائـي 🔥\n• يـمـنـع↫الـتـڪـلـم بـأمـور الـديـن 🚫\n• يـمـنـع↫نـشـر مـعـرفـات الـقـنـوات 🚫\n• يـمـنـع↫الـتـحـرش بـالـأعـضـاء 🚫\n• الـكـلام بـأدب واجـب عـلـى الـجـمـيـع ↻\n• مـمـنـوع الـسـبـام والـتـلـغـيـم 🚫\n• الـبـوت خـادم لـلـمـحـتـرمـيـن فـقـط ✨\n• احـتـرم تـحـتـرم هـذا شـعـارنـا ↻\n• الـمـالـڪ↫ سـلـطـان الإمـبـراطـوريـة 👑",

        // المجموعة 8: قـانون الـغاب
        "🦁￤سـلـطـنـة الـهـيـبـة بـ [$c_name] 🔥\n\n• الـقـوانـيـن 📌\n\n• كـن قـد الـمـسـؤولـيـة أو غـادر بـصـمـت ↻\n• الـأوامـر الـإداريـة لا نـقـاش فـيـهـا 🔥\n• يـمـنـع↫الـإسـاءة لـلـرمـوز الـأديـان 🚫\n• يـمـنـع↫الـتـلـاعـب بـأوامـر الـبـوت 🚫\n• يـمـنـع↫الـتـنـمـر عـلـى الأعـضـاء 🚫\n• الـعـدالـة تـطـبـق عـلـى الـجـمـيـع ⚖️\n• لا تـصـيـر سـبـب بـزعـل أحـد ❤️\n• كـلـنـا إخـوة بـهـذا الـمـيـدان ✨\n• الـتـفـاعـل واجـب لـلـبـقـاء ↻\n• الـمـالـڪ↫ ظـل الـإمـبـراطـور والـهـيـبـة 👑",

        // المجموعة 9: مـلڪ الـتفاعل
        "🌟￤نـور الـإمـبـراطـوريـة فـي [$c_name] ✨\n\n• الـقـوانـيـن 📌\n\n• خـلـي ڪـلامـڪ نـظـيـف مـثـل ڪـلـبـڪ ↻\n• مـن لا يـحـتـرم لا يُـحـتـرم 🔥\n• يـمـنـع↫الـتـحـريـش بـالـبـنـات 🚫\n• يـمـنـع↫إرسـال الـمـلـصـقـات الـإبـاحـيـة 🚫\n• يـمـنـع↫طـلـب الـتـمـويـل 🚫\n• الـڪـروب مـحـمـي بـنـظـام لـيـون 🔍\n• أي تـجـاوز يـواجـه بـطـرد أبـدي 👊\n• الـفـخـامـة تـبـدأ مـن هـنـا ✨\n• كـن مـلـڪ بـأخـلاقـڪ ↻\n• الـمـالـڪ↫ راعـي الـخـوة والـمـعـروف 👑",

        // المجموعة 10: خـتام الـمرجـلـة
        "👑￤عـرش الـسـيـادة الـأخـيـر بـ [$c_name] ✨\n\n• الـقـوانـيـن 📌\n\n• ادخـل بـهـيـبـة وتـفـاعـل بـوقـار ↻\n• الـمـالـڪ والـمـطـور خـط أحـمـر 🔥\n• يـمـنـع↫الـكـذب والـتـبـلـي مـع الأعـضـاء 🚫\n• يـمـنـع↫انـتـحـال الـشـخـصـيـات 🚫\n• يـمـنـع↫نـشـر أي شـيء يـخـالـف الـذوق 🚫\n• الـتـزم لـتـڪـون مـن مـؤثـري الـڪـروب ✨\n• الـقـانـون فـوق الـجـمـيـع ⚖️\n• نـحـن الـأول فـي عـالـم الـڪـروبات ↻\n• الـخـاتـمـة لـلـمـعـدلـيـن فـقـط ✨\n• الـمـالـڪ↫ تـاج الـرؤوس وفـخـر الـمـڪـان 👑"
    ];

    $random_bio = $mega_bios[array_rand($mega_bios)];

    $set_bio = bot('setChatDescription',[
        'chat_id' => $chat_id,
        'description' => $random_bio
    ]);

    if($set_bio->ok){
        bot('sendMessage',[
            'chat_id' => $chat_id,
            'text' => "‏تـم فـرض الـسـيـطـرة بـ ١٠٠ قـانـون احـتـرافي ✅👑\n\nبـايـو الـڪـروب صـار لـوز ومـرتـب بـأيقـونـات فـخـمـة ✨",
            'reply_to_message_id' => $message_id,
            'parse_mode' => "Markdown"
        ]);
    } else {
        bot('sendMessage',[
            'chat_id' => $chat_id,
            'text' => "‏يـا مـلـڪ، الـبـوت يـحـتـاج صـلاحـيـة (تـغـيـيـر الـمـعـلـومـات) لـتـنـفـيـذ الـأمـر 🛡️",
            'reply_to_message_id' => $message_id
        ]);
    }
}

if(preg_match('/^(زخرفه|زغرفه) (.*)/u', $text, $matches)){
    $name = trim($matches[2]);

    // دالة تحويل الإنجليزي لضمان عملها 100%
    function decorEn($text, $map) {
        $out = "";
        $chars = str_split($text);
        foreach($chars as $c) {
            $out .= $map[$c] ?? $c;
        }
        return $out;
    }

    // مصفوفات الحروف الإنجليزية
    $en_bold = ['a'=>'𝐚','b'=>'𝐛','c'=>'𝐜','d'=>'𝐝','e'=>'𝐞','f'=>'𝐟','g'=>'𝐠','h'=>'𝐡','i'=>'𝐢','j'=>'𝐉','k'=>'𝐤','l'=>'𝐥','m'=>'𝐦','n'=>'𝐧','o'=>'𝐨','p'=>'𝐩','q'=>'𝐪','r'=>'𝐫','s'=>'𝐬','t'=>'𝐭','u'=>'𝐮','v'=>'𝐯','w'=>'𝐰','x'=>'𝐱','y'=>'𝐲','z'=>'𝐳'];
    $en_sub  = ['a'=>'ᵃ','b'=>'ᵇ','c'=>'ᶜ','d'=>'ᵈ','e'=>'ᵉ','f'=>'ᶠ','g'=>'ᵍ','h'=>'ʰ','i'=>'ᶤ','j'=>'ʲ','k'=>'ᵏ','l'=>'ˡ','m'=>'ᵐ','n'=>'ⁿ','o'=>'ᵒ','p'=>'ᵖ','q'=>'ᵠ','r'=>'ʳ','s'=>'ˢ','t'=>'ᵗ','u'=>'ᵘ','v'=>'ᵛ','w'=>'ʷ','x'=>'ˣ','y'=>'ʸ','z'=>'ᶻ'];
    $en_small= ['a'=>'ᴀ','b'=>'ʙ','c'=>'ᴄ','d'=>'ᴅ','e'=>'ᴇ','f'=>'ꜰ','g'=>'ɢ','h'=>'ʜ','i'=>'ɪ','j'=>'ᴊ','k'=>'ᴋ','l'=>'ʟ','m'=>'ᴍ','n'=>'ɴ','o'=>'ᴏ','p'=>'ᴘ','q'=>'ǫ','r'=>'ʀ','s'=>'s','t'=>'ᴛ','u'=>'ᴜ','v'=>'ᴠ','w'=>'ᴡ','x'=>'x','y'=>'ʏ','z'=>'ᴢ'];

    // بناء الزخارف
    $res = "✅ تـم زخـࢪفـة الـنـص بـنـجـاح :\n";
    $res .= "━━━━━━━━━━━━━━\n\n";

    // 5 أنماط إنجليزية VIP
    $res .= "• `" . decorEn(strtolower($name), $en_sub) . " 𝄋`\n";
    $res .= "• `" . strtoupper(decorEn(strtolower($name), $en_small)) . " ༄︎`\n";
    $res .= "• `" . decorEn(strtolower($name), $en_bold) . " 𓃒︎`\n";
    $res .= "• `[" . $name . "] ࿓`\n";
    $res .= "• `" . $name . " 𖠄 ⁶`\n\n";

    $res .= "━━━━━━━━━━━━━━\n\n";

    // 5 أنماط عربية احترافية
    $dots = str_replace(['ع','ل','ي','ه','س','م','ك','و'], ['عِٰـِۢ','لِٰـِۢ','يِٰـِۢ','هِٰـِۢ','سِٰـِۢ','مِٰـِۢ','كِٰـِۢ','وِٰـِۢ'], $name);
    $res .= "• `$dots`\n";
    $res .= "• `$name ؏ـلَيِّ`\n";
    $res .= "• `◥ ツ$nameツ ◤`\n";
    $res .= "• `﮼$name ⸯⸯ`\n";
    $res .= "• `⸂ $name ↻`\n\n";

    $res .= "━━━━━━━━━━━━━━\n";
    $res .= "❖￤اضـغـط لـلـنـسـخ يـا مـلـڪ 🦁💎";

    bot('sendMessage',[
        'chat_id' => $chat_id,
        'text' => $res,
        'reply_to_message_id' => $message_id,
        'parse_mode' => "Markdown"
    ]);
}
// مصفوفة الـ 100 اسم (أهم الأسماء المتداولة)
$names_list = ['علي', 'محمد', 'عباس', 'كاظم', 'حسين', 'سجاد', 'جعفر', 'مرتضى', 'مصطفى', 'حيدر', 'حسن', 'زيد', 'فهد', 'صقر', 'ذيب', 'كرار', 'ياسر', 'يوسف', 'أحمد', 'ابراهيم', 'مهدي', 'باقر', 'رضا', 'رضوان', 'عمار', 'امير', 'أوميد', 'كيان', 'سيف', 'ضرغام', 'ليث', 'حمزة', 'أسد', 'ليون', 'عمر', 'بكر', 'عثمان', 'سلمان', 'بلال', 'ياسين', 'طه', 'عبدالله', 'عبدالرحمن', 'صادق', 'قاسم', 'جاسم', 'فلاح', 'ستار', 'جبار', 'منتظر', 'مقتدى', 'سعد', 'سعيد', 'سلام', 'نور', 'ضياء', 'بهاء', 'علاء', 'بشار', 'قصي', 'عدي', 'رعد', 'مؤيد', 'وليد', 'خالد', 'فؤاد', 'حميد', 'مجيد', 'ناظم', 'كاظم', 'غزوان', 'ليث', 'غيث', 'بسام', 'هشام', 'ساهر', 'ماهر', 'سامر', 'تامر', 'أنس', 'أويس', 'مالك', 'سلطان', 'فارس', 'فيصل', 'منصور', 'ناصر', 'حكيم', 'كريم', 'جواد', 'سمير', 'منير', 'باسم', 'قيس', 'نزار', 'جلال', 'جمال', 'كمال', 'نبيل', 'أيمن'];

// مصفوفة الـ 50 رد الملكي
$king_replies = [
    "يا هله وجثير الهله بيك وبالاسم ✨", "تاج راسي وذخر هالكروب 🦁", "يا هله بهالاسم وهيبته 👑", 
    "اسمك يرج المكان رج 💎", "عز وفخر للي يلفظ اسمك 🌟", "يا هله بهالطلة الملكية 🦁",
    "هيبة وسند، نورتنا يا غالي ✨", "اسمك بالقلب محفور 🌹", "يا حي الله هالطلة وهالاسم ❤️",
    "ليون يسلم عليك ويبوسك من عيونك 👑", "فخرنا بوجودك ويانا ✨", "يا هله بصقر القلعة 🦅",
    "اسمك هيبة، وحضورك سيادة 🦁", "منور يا بعد روحي ✨", "يا مية هلا بهالاسم 🌹",
    "الكروب نور بذكر اسمك 🌟", "حي الله أصلك الطيب 💎", "يا هله بالنشمي 🦁",
    "كلك ذوق وأخلاق يا ذهب ✨", "صاحب هيبة وكلمة مسموعة 👑", "فدوة لهالاسم وراعيه ❤️",
    "يا هله بيك يا ملك 🦁", "نورتنا ونورت مڪانك ✨", "حي الله هالاسم وراعيه 👑",
    "يا هله بأسد القلعة 🦁", "اسمك زلزال بالكروب ✨", "حي الله من ذكر هالاسم 🌟",
    "هيبة وفخامة تسلملي هالطلة 💎", "يا هله بالمعزوز الغالي ✨", "اسمك يرفع الراس 👑",
    "يا مية هلا بالشيخ ✨", "منور يا بعد قلبي وروحي 🌹", "يا هله بيك يا عطر الورد 🦁",
    "حي الله هالطول وهالاسم 💎", "اسمك هيبة بكل المحافل ✨", "يا هله بالصقر 🦅",
    "نورتنا يا تاج الرأس 👑", "حي الله أصلك يا معدل ✨", "يا هله بهيبة الإمبراطورية 🦁",
    "نورك غطى على الكل يا غالي ✨", "يا مية هلا بجيتك 🌹", "اسمك فخر لكل من عرفك 👑",
    "يا هله بالذهب الصافي ✨", "منورنا يا ذيب 🐺", "حي الله هالوجه الطيب 🌟",
    "يا هله بيك يا كحيل العين 💎", "اسمك عنوان للمرچلة ⚔️", "يا هله باللي حضورهم هيبة 🦁",
    "منور يا قمر الإمبراطورية 🌙", "حي الله هالاسم العالي 👑"
];

// 1. كود الرد عند ذكر الأسماء
if(in_array($text, $names_list)){
    $rand_reply = $king_replies[array_rand($king_replies)];
    bot('sendMessage',[
        'chat_id'=>$chat_id,
        'text'=>"❖￤ $rand_reply \n❖￤ يـا هـلـه بـيـڪ يـا : `$text` 🦁💎",
        'reply_to_message_id'=>$message_id,
        'parse_mode'=>"Markdown"
    ]);
}

// 2. كود الترحيب الملكي عند دخول أي عضو
if($message->new_chat_member){
    $u_name = $message->new_chat_member->first_name;
    $welcome = "❖￤ يـا هـلـه وجـثـيـر الـهـلـه بـيـڪ ✨\n\n";
    $welcome .= "❖￤ نـورت الـإمـبـࢪاطـوࢪيـة يـا : `$u_name` \n\n";
    $welcome .= "❖￤ تـفـاعـل لـتـصـيـر مـن الـمـقـربـيـن 🦁💎\n";
    $welcome .= "━━━━━━━━━━━━━━\n";
    $welcome .= "❖￤ بـواسطـة لـيـون الـمـطـور 👑";

    bot('sendMessage',[
        'chat_id'=>$chat_id,
        'text'=>$welcome,
        'parse_mode'=>"Markdown"
    ]);
}

/*==============================
=     OPEN MENU BY TEXT       =
==============================*/

/* أزرار الأقسام */
$menu_buttons = [
    ["📖 القرآن الكريم"],
    ["📜 اقتباسات","🌙 ديني"],
    ["📝 أشعار","⚖️ أحكام"],
    ["🖼 جداريات","❤️ عبارات حب"],
    ["🤡 نكت","💡 معلومات"]
];

/* الكلمات التي تفتح القائمة */
$open_words = ["تونس","1","2","3","menu","القائمة"];

/* فتح الأزرار */
if (in_array($text, $open_words)) {

    bot("sendMessage",[
        "chat_id"=>$chat_id,
        "text"=>"🧬 **اختر القسم من الأسفل**",
        "parse_mode"=>"Markdown",
        "reply_markup"=>json_encode([
            "keyboard"=>$menu_buttons,
            "resize_keyboard"=>true
        ])
    ]);
    exit;
}
/*=====================================
=        QUOTES MODULE – LION          =
=====================================*/

$quotes = [
"امسحوا أوجاعكم فما زال للأمل حكاية .",
"الكتمان مؤذٍ ، والبوح لن يغير شيء .",
"أمي وحدها الاختلاف الوحيد الذي يكسر كل قاعدة...",
"كوب قهوة ووجه من أُمي ، أمنية كُل مساء...",
"إنما أنا فتنَةٌ فلا تكفُر .",
"اللهم لا تُرينا فيمن نُحب، إلا ما نُحب .",
"ولازال حُبك يعلُو ولا يُعلَى عليه ..",
"مثل ما جابك الله صدفة يجيب غيرك.",
"سلاماً على روح ملئت قلبي حباً دون لقاء..",
"من بين الزِحام ، سأُلفت عينَاك .",
"تفاصيل صغيرة كافيه أن تمنح قلبك الدفئ.",
"لم اعد احاول ، انا مكتفي بانتظار معجزه .",
"شباب احد يسلفني شعور شوي",
"لم يكُن صادقاً كان يمّلأ فراغه فقط .",
"لستُ هنا لأبهارك .",
"سر العلاقات العميقة، بساطة التعامل .",
"القبول من الله، فلا تُغير من شأنك لإبهار أحد .",
"مغرمٌه به أكثرُ مما يعتقد",
"تِجّرحني مَرة، بكّسِرك مرتين .",
"نحن لا نُعاتب إلا من يُهمنا أمره .",
"لاتنسى أن ماتراه مني، أنت من أخترت أن تراه.",
"يارب ليس لأني أستحق، بل لأنك رحيم .",
"وكتمت مافي القلب إلى ان فاضت دمعتي",
"يعرفون كل شيء، إلا عيوبهم .",
"الجميع يكتب عن الألم لكن الألم الحقيقي لا يُحكىٰ",
"هو مُختلف عن إلجميّع لِذلك أُحِبه.",
"الاحتفال هو أن تسجد تحت قدميها لـ ترى جمال العيد..",
"يغلق باباً بحكمته، ويفتح ألف باب برحمته.",
"﴿ إِنَّهُ هُوَ الْعَزِيزُ الرَّحِيمُ ﴾",
"علمتني الحياة أن الحُب الوحيد الذي لن يُخيبك حُب الأب",
"صباح الخير لعينيها الجميلتين ثُم للعالم البائس .",
"كُنتَ ومازِلت صاحِب كُل شُعور حِلو فيني...",
"وببقى أحبك مساء اليوم ومساء السنين الباقية ..",

"هل أعَرتِ الصُّبحَ وَجهكِ ؟.",
"لاتقلق، ربك كفيل بمن‌ أحزنوك ‌يوماً ."
];
$quotes = [
    "منذ ذلك اليوم البائس الذي قررت به أن أجعل قلبي كالحجر تمامًا، وأمتنع عن البكاء نهائيًا، منذ ذلك اليوم وكل شيء قد ازداد سوءًا.",
    "هل شعرت يومًا بأنك تسقط في عمق صمتك، بحيث لا يمكنك البكاء ولا الكتابة ولا التحدث إلى الآخرين، فقط كل ما تريده البقاء وحدك.",
    "تصل لمرحلة من الضغط، ترفض العتاب على ما يصدر منك، تتجنب العلاقات المرهقة والمناقشات التي تحتاج منك التبرير، تبحث عن الهدوء فقط.",
    "سأختارك، إذا استمرت العواصف، أو غلبها الصحو، إذا انتهى هذا كله أو استمرّ، إذا نجحنا في التجاوز أو حملنا خساراتنا معنا، سأعود وأختارك.",
    "على الأشياء التي هجرتنا ومضت في طريقها أن لا تأتينا نادمة بعد أن قطعنا مسافة هائلة في طريق الشفاء.",
    "كيف أشرح كم أنني متعبٌ ومثقلٌ بشكل لا يُطاق، كيف أشرح قلقي الذي لا أجد له تفسيرًا، وحزني المُكتظ دون أن يُقال عني أنني أبالغ.",
    "أشعر بأنني منطفئ بطريقة لا أستطيع شرحها، بروحٍ لا يمكنني إعادة بريقها الأول.",
    "بعد غيابك عنّي توقفت عقارب الساعة، وحلّ الظلام، ولم يظهر أي قمر.",
    "هناك خيبة تلتفّ حولي، كشيء أسمع صوت خطواته لكنني لا أراه.",
    "لن تستطيع التعمق بي مهما حاولت، فالظاهر أمامك لا يشرح عمقي الحقيقي.",
    "لا أحاول التباهي بأحزاني، ولا لتعالي صوت الألم في صدري.",
    "لم يساعدني أحد على التحسّن في فترات حياتي الصعبة، كنت أتماسك وحدي.",
    "كنتُ وحدي في الوداع، في البكاء، أتعامل مع قلبي بصمت.",
    "أشعر بالذنب لأنني أحببتك، ربما لم يكن الوقت مناسبًا.",
    "إنني منزوٍ على نفسي، أراكم جميعًا لكنني لا أشعر بكم.",
    "أن أستيقظ يومًا ما فأجد تلك النار القلقة في صدري قد خمدت.",
    "يفعل ما في وسعه لينجو، لكنه ينهمر وحيدًا في زاوية غرفته.",
    "مثقل بالكثير من الأشياء التي تركتها تمرّ دون أن أكتب عنها حرفًا.",
    "نسيت أشياء كثيرة، وبقي أثر واحد لا يزول.",
    "هذا الصمت مألوف لروحي، لكنه صار أثقل مما توقعت.",
    "تفزعني فكرة أن من أعرفه اليوم قد أجهله غدًا.",
    "أريد أن أعتذر عن هذا البعد الطويل بيننا.",
    "لم أكن الخيار الأول في حياة أحد، كنت عابرًا.",
    "لا أحد يعرف مرارة الخيبة كما نعرفها نحن الذين نغفر كثيرًا.",
    "بذلت ما بوسعي للبقاء، وما زلت أحاول.",
    "غادر دون أسف، وترك المكان أبرد.",
    "فقدت الاهتمام بكل شيء، وكأن جزءًا مني تلاشى.",
    "كنت أود أن أخبر أحدًا بما يحدث، أن أكون كما أنا.",
    "لم يكن الأذى من الرحيل، بل من الصمت المفاجئ.",
    "أسوأ ما أصابني هو فقدان شغفي.",
    "يؤرقني قلبي من فكرة النسيان.",
    "أبحث عن كلمة تصف تعبي، فلا أجد.",
    "موطني الحقيقي هو القلب الذي يعرفني ويقبلني.",
    "منتصف الأشياء مُخيف جدًا.",
    "أشعر ببرود يلامس روحي.",
    "حتى الآن لم يفهمني أحد كما توقعت.",
    "لا يعنيني العالم بقدر ما يعنيني السلام.",
    "وحيدٌ أتكئ على عزلتي.",
    "العبرة ليست بالزحام، بل بركنٍ دافئ.",
    "نحن لا نطرق الأبواب التي أُغلقت في وجوهنا."
];


/*==============================
=        عرض اقتباس            =
==============================*/
if ($text === "📜 اقتباسات") {

    $quote = $quotes[array_rand($quotes)];
    // حفظ الاقتباس الأخير لاستخدامه في النشر إذا لزم الأمر
    file_put_contents("last_quote_$chat_id.txt", $quote);

    bot("sendMessage", [
        "chat_id" => $chat_id,
        "text" => "📜 *اقتباس*\n⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n\n$quote\n\n⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯",
        "parse_mode" => "Markdown"
    ]);
    exit;
}

/*==============================
=        قائمة النصوص الدينية    =
==============================*/
$deen_quotes = [
    "على المسلم أن يتستر بستر الله، وألا يجاهر بالمعصية، بل إذا فعلها فليستتر بستر الله، وليتب إلى الله؛ لقول النبي ﷺ: كل أمتي معافى إلا المجاهرين.",
    "فالواجب على المسلم التستر بستر الله، وعدم إظهار المعاصي، والتوبة إلى الله، فإن المعصية إذا خفيت ما تضر إلا صاحبها، وإذا ظهرت ضرت العامة.",
    "فالواجب على من عصى أن يتقي الله، وأن يسر معصيته، وأن يتوب إلى الله منها، وألا يتجاهر بالمعاصي، فإن المجاهرة فيها شر عظيم.",
    "لله أحزاننا المخبأة في جوف صدورنا، ولله الغصة العالقة في حناجرنا، عليه نستند وبه تطمئن نفوسنا.",
    "اللهمّ الجنة ونعيمها، وبردها وسلامها، اللهمّ رؤية وجهك الكريم.",
    "اليوم الأول من رجب، وهو من الأشهر الحرم، فوصيتي لنفسي وإياكم بتقوى الله وعدم ظلم أنفسنا.",
    "اجعلوا آخر صلاتكم بالليل وِترًا.",
    "اللهمّ صلِّ وسلّم على سيدنا محمد.",
    "اللهم لا تدع لنا ذنبًا إلا غفرته.",
    "اللهم هداية لمن لا يصلي، وثباتًا لمن يصلي.",
    "اللهم لا تدع حزنًا في قلوبنا إلا بدّلته فرحًا.",
    "اللهم دبّر لي أمري كله وبلّغني ما أدعوك به.",
    "وأسألك نعيمًا لا ينفد، وقرة عين لا تنقطع.",
    "ستبقى ألطاف الله تلاحقك دون أن تدرك.",
    "حاشاه أن ترجع الأيدي بلا نعم.",
    "ربِّ أيقظني على فرج وفرح وانشراح.",
    "تخذلنا الحياة ويساندنا لطف الله.",
    "نُّورٌ عَلَىٰ نُورٍ ۗ يَهْدِي اللَّهُ لِنُورِهِ مَن يَشَاءُ.",
    "اللهم اجعلني ممن تغيّرت أقدارهم للأحسن.",
    "تبكي وتبكي والله بجبره يأتي.",
    "الله قدّر كل هذا وهو كفيل به، اطمئن.",
    "دلّني إليك كما تدل عبدًا إلى إيمانه.",
    "يا رب اجعل ما أسعى إليه يسعى إليّ.",
    "الأمر يبدأ عند ربك وينتهي عند ربك، فلا تقف عند الخلق كثيرًا.",
    "واذهب غيظ قلبي اللهم.",
    "نسألك ألا تهون أحلامنا فينا.",
    "وأمر أهلك بالصلاة واصطبر عليها.",
    "اللهم اجعلني أرى أمنياتي تتسابق عليّ بتسخير منك.",
    "واذكروا الله كثيرًا لعلكم تفلحون.",
    "أتيتك بما تبقى مني فأعنّي يا رب.",
    "اللهم يسّر لي خيار خلقك وكفّ عني شرارهم.",
    "وَلَيْسَ اعتراضًا ولكننا تعبنا فهون علينا قضائك.",
    "يا رب أن تقصدنا المسرّات بلا عناء.",
    "اللهم إني أعوذ بك من الهم والحزن.",
    "اللهم غيّر من أقدارنا لتكون الأجمل.",
    "يارب رمّم أتعاب قلوبنا واجبر خواطرنا.",
    "وإن لم تغفر لنا وترحمنا لنكونن من الخاسرين.",
    "شعور تفويض الأمر لله شعور يفيض طمأنينة.",
    "اللهم اجعلني في حرزك ومعيتك.",
    "اللهم أنت الرجاء ومنك العطاء وإليك الدعاء.",
    "الحمد لله على حياة يدبّرها الله برحمته.",
    "اللهم إني أسألك فرحًا يغنيني عن كل شيء.",
    "هذه الدموع التي يعرفها الله لن تهون عنده.",
    "وكان ذلك على الله يسيرًا.",
    "أعظم رحمة في الوجود هي أن الله معك.",
    "اللهم افتح لصدورنا أبواب الانشراح.",
    "ثم يأتيك الله بعوضٍ أجمل مما فقدت.",
    "إن الله وتر يحب الوتر.",
    "كلما تعثرت استغفر، تجد الله غفورًا رحيمًا.",
    "نور على نور يهدي الله لنوره من يشاء.",
    "وإن ضاقت دوائرها فعند الله المتّسع.",
    "ألم نشرح لك صدرك."
];

/*==============================
=        عرض النص الديني        =
==============================*/
if ($text === "🌙 ديني") {

    // اختيار نص عشوائي
    $quote = $deen_quotes[array_rand($deen_quotes)];

    // حفظ آخر نص لهذا المستخدم (chat_id)
    file_put_contents("last_deen_$chat_id.txt", $quote);

    bot("sendMessage", [
        "chat_id" => $chat_id,
        "text" => "🌙 **ديني**\n⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n\n$quote\n\n⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯",
        "parse_mode" => "Markdown"
    ]);
    exit;
}



if($text== "فتح الكل" ){
if( in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [المدير](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح الكل
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["link"]="مفتوح";
	$settings["lock"]["username"]="مفتوح";
	$settings["lock"]["bot"]="مفتوح";
	$settings["lock"]["forward"]="مفتوح";
	$settings["lock"]["tgservices"]="مفتوح";
	$settings["lock"]["contact"]="مفتوح";
    $settings = json_encode($settings,true);
    file_put_contents("data/$chat_id.json",$settings);
}
}
}
if($text== "فتح الكل" ){
if( in_array($from_id,$useradmin) and !in_array($from_id,$getCCmember) and  !in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [الادمن](tg://user?id=$from_id) 👷🏽
📡¦ تم فتح الكل
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
 ]);
$settings["lock"]["link"]="مفتوح";
	$settings["lock"]["username"]="مفتوح";
	$settings["lock"]["bot"]="مفتوح";
	$settings["lock"]["forward"]="مفتوح";
	$settings["lock"]["tgservices"]="مفتوح";
	$settings["lock"]["contact"]="مفتوح";
    $settings = json_encode($settings,true);
    file_put_contents("data/$chat_id.json",$settings);}
}
}
if($text== "فتح الكل" ){
if ($tc == 'group' | $tc == 'supergroup'){  
if( $status != 'creator' and $status != 'administrator' and !in_array($from_id,$Dev) and !in_array($from_id,$getCCmember) and !in_array($from_id,$useradmin) ){
$add = $settings["information"]["added"];
if ($add == true) {
 bot('sendMessage',[
'chat_id'=>$chat_id,
'text'=>"
📡¦ هذا الامر يخص الادمنيه فقط  🚶
",'reply_to_message_id'=>$message_id,
]);
}
}
}
}
if( $text == "تقييد" && $rt){
if ( $status == 'creator' or $status == 'administrator' or in_array($from_id,$Dev) or in_array($from_id,$useradmin) or in_array($from_id,$getCCmember)) {
if ( $statusrt != 'creator' && $statusrt != 'administrator' && !in_array($re_id,$Dev) && !in_array($re_id,$useradmin) && !in_array($re_id,$getCCmember)) {
$add = $settings["information"]["added"];
if ($add == true){
  bot('restrictChatMember',[
   'user_id'=>$re_id,   
   'chat_id'=>$chat_id,
   'can_post_messages'=>false,
     ]);
  bot('sendMessage',[
'chat_id'=>$chat_id,
'text'=>"
👤¦ العضو »  [$re_name](tg://user?id=$re_id)
🎫¦ الايدي » {`$from_id`}
🛠¦ تم تقييد آلعضـو بنجآح 
✓️
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,
'reply_to_message_id'=>$re_msgid,
]);
$settings["silentlist"][]="$re_id";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}

}
else
{
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
👤¦ لا يمكنك تقييد المنشئ , الادمن , المطور
🛠",
  'reply_to_message_id'=>$message_id,
 ]);
}
}
}
if ( strpos($text , "تقييد مدة") !== false && $rt) {
if ( $status == 'creator' or $status == 'administrator' or in_array($from_id,$Dev) or in_array($from_id,$getCCmember) or in_array($from_id,$useradmin)) {
if ( $statusrt != 'creator' && $statusrt != 'administrator' && !in_array($re_id,$Dev)) {
$add = $settings["information"]["added"];
$we = str_replace(['تقييد مدة'],'',$text);
if ($we <= 1000 && $we >= 1){
if ($add == true) {
$weplus = $we + 0;
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
👤¦ العضو »  [$re_name](tg://user?id=$re_id)
🎫¦ الايدي » {`$from_id`}
🛠¦ تم تقييد آلعضـو بنجآح  لمدة $we دقيقة
✓️
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,
  'reply_to_message_id'=>$message_id,
'reply_markup'=>$inlinebutton,
 ]);
bot('restrictChatMember',[
   'user_id'=>$re_id,   
   'chat_id'=>$chat_id,
   'can_post_messages'=>false,
   'until_date'=>time()+$weplus*60,
     ]);
$settings["silentlist"][]="$re_id";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}

}
else
{
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
📛¦ حدود التقييد ,  يجب ان تكون ما بين  [1-1000]
",
  'reply_to_message_id'=>$message_id,
'reply_markup'=>$inlinebutton,
 ]);
}
}
else
{
bot('sendmessage',[
 'chat_id' => $chat_id,
 'text'=>"👤¦ لا يمكنك تقييد المنشئ , الادمن , المطور
🛠",
'reply_markup'=>$inlinebutton,
   ]);
}
}
}
if( $text == "الغاء التقييد" && $rt){
if ( $status == 'creator' or $status == 'administrator' or in_array($from_id,$Dev) ) {
$add = $settings["information"]["added"];
if ($add == true) {
 bot('restrictChatMember',[
   'user_id'=>$re_id,   
   'chat_id'=>$chat_id,
   'can_post_messages'=>true,
   'can_add_web_page_previews'=>false,
   'can_send_other_messages'=>true,
   'can_send_media_messages'=>true,
     ]);
  bot('sendMessage',[
'chat_id'=>$chat_id,
'text'=>"
👤¦ العضو »  [$re_name](tg://user?id=$re_id)
🎫¦ الايدي » {`$from_id`}
🛠¦ تم الغاء تقييد آلعضـو بنجآح 
✓️
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,
'reply_to_message_id'=>$re_msgid,
]);
$key = array_search($re_id,$settings["silentlist"]);
unset($settings["silentlist"][$key]);
$settings["silentlist"] = array_values($settings["silentlist"]); 
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}

}
}
if( $text == "المقيدين") {
if ( $status == 'creator' or $status == 'administrator' or in_array($from_id,$Dev) or in_array($from_id,$getCCmember) or in_array($from_id,$useradmin)) {
$silent = $settings["silentlist"];
for($z = 0;$z <= count($silent)-1;$z++){
$result = $result."[$silent[$z]](tg://user?id=$silent[$z])"."\n";
}
  bot('sendMessage',[
'chat_id'=>$chat_id,
'text'=>"
🙋🏼‍♂️¦ أهلا عزيزي [$first_name](tg://user?id=$from_id) 👷🏽
📡¦ المقيدين
$result
✓
",
'parse_mode'=>"markdown",'disable_web_page_preview'=>true,
'reply_to_message_id'=>$message_id,
'reply_markup'=>$inlinebutton,
 ]);
}
}
elseif( $text == "مسح المقيدين") {
if ( $status == 'creator' or $status == 'administrator' or in_array($from_id,$Dev) or in_array($from_id,$getCCmember) or in_array($from_id,$useradmin)) {
$add = $settings["information"]["added"];
if ($add == true) {
$silent = $settings["silentlist"];
for($z = 0;$z <= count($silent)-1;$z++){
 bot('restrictChatMember',[
   'user_id'=>$silent[$z],   
   'chat_id'=>$chat_id,
   'can_post_messages'=>true,
   'can_add_web_page_previews'=>false,
   'can_send_other_messages'=>true,
   'can_send_media_messages'=>true,
     ]);
}
  bot('sendMessage',[
'chat_id'=>$chat_id,
'text'=>"  
🙋🏼‍♂️¦ أهلا عزيزي [$first_name](tg://user?id=$from_id) 👷🏽
📡¦ تم مسح المقيدين
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,
'reply_to_message_id'=>$message_id,
'reply_markup'=>$inlinebutton,
 ]);
unset($settings["silentlist"]);
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}

}
}
if( $rt && $text=="تثبيت"){
if ( $status == 'creator' or $status == 'administrator' or in_array($from_id,$Dev) or in_array($from_id,$getCCmember) or in_array($from_id,$useradmin)){
 bot('pinChatMessage',[
'chat_id'=>$chat_id,
'message_id'=>$replyid
  ]);
bot('sendmessage',[
 'chat_id'=>$chat_id,
 'text'=>"📌¦ تم تثبيت الرساله 
✓",
'reply_to_message_id'=>$message_id,
 ]);
 }
}
if(  $text=="الغاء التثبيت"){
if ( $status == 'creator' or $status == 'administrator' or in_array($from_id,$Dev) or in_array($from_id,$getCCmember) or in_array($from_id,$useradmin)){
 bot('unpinChatMessage',[
'chat_id'=>$chat_id,
'message_id'=>$replyid
  ]);
bot('sendmessage',[
 'chat_id'=>$chat_id,
 'text'=>"📌¦ تم الغاء تثبيت الرساله 
✓",
'reply_to_message_id'=>$message_id,
 ]);
 }
}
if ( strpos($text , 'وضع قوانين') !== false) {
if ( $status == 'creator' or $status == 'administrator' or in_array($from_id,$Dev)){
$add = $settings["information"]["added"];
if ($add == true) {
$code = str_replace(['وضع قوانين'],'',$text);
$plus = mb_strlen("$code");
if($plus < 600) {
 bot('sendMessage',[
'chat_id'=>$chat_id,
'text'=>"مقفول┇تم وضع القوانين للمجموعه",
'reply_to_message_id'=>$message_id,
'reply_markup'=>$inlinebutton,
   ]);
$settings["information"]["rules"]="$code";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
else
{
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"مفتوح┇لايمكن وضع اكثر من 600 محرف",
  'reply_to_message_id'=>$message_id,
 ]);
}
}
}
}
if( $text=="القوانين"){
if ($tc == 'group' | $tc == 'supergroup'){  
$text1 = $settings["information"]["rules"];
$text = str_replace(["gpname","username","time"],["$namegroup","@$username","$date | $date2"],"$text1");
 bot('sendMessage',[
'chat_id'=>$chat_id,
'text'=>"$text",'parse_mode'=>"markdown",'disable_web_page_preview'=>true, 
	 'reply_to_message_id'=>$message_id,
   ]);
   }   
else
{
date_default_timezone_set('Asia/Damascus');
$date = date('Y-m-d');
$date2 = date("H:i");
$text1 = $settings["information"]["rules"];
$text = str_replace(["gpname","username","time"],["$namegroup","@$username","$date | $date2"],"$text1");
 bot('sendMessage',[
'chat_id'=>$chat_id,
'text'=>"$text",
'parse_mode'=>"markdown",'disable_web_page_preview'=>true,
	 
	 'reply_to_message_id'=>$message_id,
   ]);
}
}
if (strpos($text , "وضع ترحيب ") !== false ) {
if ($status == 'creator' or $status == 'administrator' or in_array($from_id,$Dev)) {
$add = $settings["information"]["added"];
if ($add == true) {
$we = str_replace(['وضع ترحيب'],'',$text);
$plus = mb_strlen("$we");
if($plus < 600) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
☑┇تم وضع ترحيب للمجموعة
$we
",
  'reply_to_message_id'=>$message_id,
 ]);
$settings["information"]["textwelcome"]="$we";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
else
{
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>" لقد ارسلت رسالة تحتوي600 حرف لٱ يمكنك ارسال اكثر م̷ـــِْن 600 حرف",
  'reply_to_message_id'=>$message_id,
'reply_markup'=>$inlinebutton,
 ]);
}
}
}
}
if( $rt && $text== "حظر"){
if ( $status == 'creator' or $status == 'administrator' or in_array($from_id,$Dev) or in_array($from_id,$getCCmember) or in_array($from_id,$useradmin)){
if ( $statusrt != 'creator' && $statusrt != 'administrator' && !in_array($re_id,$Dev) && !in_array($re_id,$getCCmember) && !in_array($re_id,$useradmin)) {
bot('KickChatMember',[
'chat_id'=>$chat_id,
'user_id'=>$re_id
  ]);
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
👤¦ العضو »  [$re_name](tg://user?id=$re_id)
🎫¦ الايدي » {`$from_id`}
🛠¦ تم حـظـر آلعضـو بنجآح 
✓️
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
   ]);
   } 
else	
{
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"👤¦ لا يمكنك حظر المنشئ , الادمن , المطور
🛠",
  'reply_to_message_id'=>$message_id,
'reply_markup'=>$inlinebutton,
 ]);
   }
}
 }
 if( $rt && $text== "الغاء الحظر"){
if ( $status == 'creator' or $status == 'administrator' or in_array($from_id,$Dev) or in_array($from_id,$getCCmember) or in_array($from_id,$useradmin)){
if ( $statusrt != 'creator' && $statusrt != 'administrator' && !in_array($re_id,$Dev) && !in_array($re_id,$getCCmember) && !in_array($re_id,$useradmin)) {
bot('unbanChatMember',[
'chat_id'=>$chat_id,
'user_id'=>$re_id
  ]);
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
👤¦ العضو »  [$re_name](tg://user?id=$re_id)
🎫¦ الايدي » {`$from_id`}
🛠¦ تم الغاء حـظـر آلعضـو بنجآح 
✓️
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,'reply_to_message_id'=>$message_id,
   ]);
   } 
else	
{
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"👤¦ لا يمكنك حظر المنشئ , الادمن , المطور
🛠",
  'reply_to_message_id'=>$message_id,
'reply_markup'=>$inlinebutton,
 ]);
   }
}
 }
 if( $rt && $text == "حذف"){
if ( $status == 'creator' or $status == 'administrator' or in_array($from_id,$Dev) or in_array($from_id,$useradmin) or in_array($from_id,$getCCmember)){
 bot('deletemessage',[
'chat_id'=>$chat_id,
'message_id'=>$re_msgid
]);
 bot('deletemessage',[
'chat_id'=>$chat_id,
'message_id'=>$message_id
]);
 }
}
if (  strpos($text , 'تنظيف') !== false  ) {
if ( $status == 'creator' or $status == 'administrator' or in_array($from_id,$Dev) or in_array($from_id,$getCCmember) or in_array($from_id,$useradmin)){
$num = str_replace(['/rmsg ','تنظيف'],'',$text);
if ($num <= 100 && $num >= 1){
$add = $settings["information"]["added"];
if ($add == true) {
for($i=$message_id; $i>=$message_id-$num; $i--){
bot('deletemessage',[
 'chat_id' => $chat_id,
 'message_id' =>$i,
          ]);
}
bot('sendmessage',[
 'chat_id' => $chat_id,
 'text' =>"
⛑¦ تـم مسح ~⪼ { *$num* } من الرسائل  
✓
",'parse_mode'=>"markdown",
   ]);
}
}
else
{
bot('sendmessage',[
 'chat_id' => $chat_id,
 'text'=>"
❕┇لا تستطيع حذف اكثر من 100 رساله
",
   ]);
}
}
}
 //*********************
$id = $message->from->id;
$sudo = "7897598134"; //هنا حط ايديك ،!
mkdir("iBadlz");
mkdir("iBadlz/$chat_id");
$put = file_get_contents("iBadlz/$chat_id/link.txt");
$link = file_get_contents("iBadlz/$chat_id/put.txt");
$ex = explode("\n",$put);
if( $text == "ضع رابط" || $text == "وضع رابط" and $id == $sudo){
file_put_contents("iBadlz/$chat_id/put.txt","link");
bot("sendmessage",[
'chat_id'=>$chat_id,
'text'=>"
📚¦ حسنا ، ارسل لي رابط المجموعهہ ،!
",
'reply_to_message_id'=>$message->message_id
]);
}
if( $text == "وضع رابط" || $text == "ضع رابط" and $id != $sudo){
bot("sendmessage",[
'chat_id'=>$chat_id,
'text'=>" 
عذرآ صديقي ،! ليس لديك صلاحيات وضع الرابط 🙂💔ء
",
'reply_to_message_id'=>$message->message_id
]);
}
if($text and $link == "link"){
file_put_contents("iBadlz/$chat_id/link.txt",$text);
file_put_contents("iBadlz/$chat_id/put.txt"," ");
bot("sendmessage",[
'chat_id'=>$chat_id,
'text'=>"
📬¦ تم حفظ الرابط الخاص بالمجموعهہ ،!
",
'reply_to_message_id'=>$message->message_id
]);
}
if($text == "الرابط" or $text == "رابط"){
bot("sendmessage",[
'chat_id'=>$chat_id,
'text'=>" رابط المجموعه هو :
** $put **",
'reply_to_message_id'=>$message->message_id
]);
}
if( $text == "مسح الرابط" || $text == "حذف الرابط" and $id == $sudo){
file_put_contents("iBadlz/$chat_id/link.txt"," ");
bot("sendmessage",[
'chat_id'=>$chat_id,
'text'=>"
تم حذف الرابط الخاص بك
",
'reply_to_message_id'=>$message->message_id
]);
}
if( $text == "مسح الرابط" || $text == "حذف الرابط" and $id != $sudo){
 bot('sendmessage',[
 'chat_id'=>$chat_id,
 'text'=> "
 المعذره صديقي ليس لديك صلاحيات مسح الرابط
 ",
 'reply_to_message_id'=>$message->message_id
 ]);
 }
//*****************************

 if( $text=="تحذير" && $rt){
if ( $status == 'creator' or $status == 'administrator' or in_array($from_id,$Dev) or in_array($from_id,$getCCmember) or in_array($from_id,$useradmin)){
if ($tc == 'group' | $tc == 'supergroup'){
if ( $statusrt != 'creator' && $statusrt != 'administrator' && !in_array($re_id,$Dev) && !in_array($re_id,$useradmin) && !in_array($re_id,$getCCmember)) {
$add = $settings["information"]["added"];
if ($add == true) {
$warn = $settings["warnlist"]["$re_id"];
$setwarn = $settings["information"]["setwarn"];
$warnplus = $warn + 1;	
if ($warnplus >= $setwarn) {
$hardmodewarn = $settings["information"]["hardmodewarn"];
if($hardmodewarn == "بالتقييد"){
bot('restrictChatMember',[
   'user_id'=>$re_id,   
   'chat_id'=>$chat_id,
   'can_post_messages'=>false,
   'until_date'=>time()+3600,
]);
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙎‍♂┇العضو ~⪼ [$re_name](t.me/$re_user)
🚸┇تم تحذيرك تحذيراتك *$warnplus* من اصل *$setwarn*
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,
   ]);
 }
else
{
   bot('restrictChatMember',[
   'user_id'=>$re_id,   
   'chat_id'=>$chat_id,
   'can_post_messages'=>false,
   'until_date'=>time()+3600,
     ]);
	 	bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙎‍♂┇العضو ~⪼ [$re_name](t.me/$re_user)
🚸┇تم تحذيرك تحذيراتك *$warnplus* من اصل *$setwarn*
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,
   ]);
$settings["silentlist"][]="$re_id";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
else
{
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙎‍♂┇العضو ~⪼ [$re_name](t.me/$re_user)
🚸┇تم تحذيرك تحذيراتك *$warnplus* من اصل *$setwarn*
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,
'reply_to_message_id'=>$message_id,
 'reply_markup'=>$inlinebutton,
   ]);
$settings["warnlist"]["{$re_id}"]=$warnplus;
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}
}
 }
else
{
	bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"⚠️┇خطأ لا يمكن تحذير الادمن  , المدير  , المطور ",
  'reply_to_message_id'=>$message_id,
'reply_markup'=>$inlinebutton,
 ]);
}
}
}
}
if($text=="مسح التحذير" && $rt ){
if ( $status == 'creator' or $status == 'administrator' or in_array($from_id,$Dev) or in_array($from_id,$getCCmember) or in_array($from_id,$useradmin)){
if ($tc == 'group' | $tc == 'supergroup'){  
$add = $settings["information"]["added"];
if ($add == true) {
$warn = $settings["warnlist"]["$re_id"];
$setwarn = $settings["information"]["setwarn"];
$warnplus = $warn - 1;	
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🙎‍♂┇العضو ~⪼ [$re_name](t.me/$re_user)
🚸┇تم مسح تحذيرك تحذيراتك *$warnplus* من اصل *$setwarn*
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,
'reply_to_message_id'=>$message_id,
'reply_markup'=>$inlinebutton,
   ]);
$settings["warnlist"]["{$re_id}"]=$warnplus;
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
 }
 }
}
}
if ( strpos($text , 'وضع تحذير') !== false  ) {
$newdec = str_replace(['وضع تحذير'],'',$text);
if ( $status == 'creator' or $status == 'administrator' or in_array($from_id,$Dev) or in_array($from_id,$getCCmember) or in_array($from_id,$useradmin)){
$add = $settings["information"]["added"];
if ($add == true) {
if ($newdec <= 20 && $newdec >= 1){
bot('sendmessage',[
 'chat_id'=>$chat_id,
 'text'=>"
 👤┇تم تعيين عدد التحذيرات {*$newdec*}
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,
'reply_to_message_id'=>$message_id,
'reply_markup'=>$inlinebutton,
   ]);
$settings["information"]["setwarn"]="$newdec";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
   }else{
bot('sendmessage',[
 'chat_id' => $chat_id,
 'text'=>"
❕┇لا تستطيع وضع اكثر من 20 تحذير  
",
'reply_markup'=>$inlinebutton,
   ]);
 }
}
}
}
elseif( $text=="تحذيراتي"){
if ($tc == 'group' | $tc == 'supergroup'){  
$warn = $settings["warnlist"]["$re_id"];
$setwarn = $settings["information"]["setwarn"];
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🚸┇تحذيراتك *$warn* من اصل *$setwarn*
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,
'reply_to_message_id'=>$message_id,
   ]);
 }
 }

elseif ($text == "الترحيب") {
if ( $status == 'creator' or $status == 'administrator' or in_array($from_id,$Dev) or in_array($from_id,$getCCmember) or in_array($from_id,$useradmin)) {
$add = $settings["information"]["added"];
if ($add == true) {
	$text = $settings["information"]["textwelcome"];
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
$text

",  'reply_to_message_id'=>$message_id,'parse_mode'=>"markdown",'disable_web_page_preview'=>true,
 ]);
$settings["information"]["welcome"]="مفتوح";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings);
}

}
}
if($text == " $namebot غادر"){
if (in_array($from_id,$Dev)){
bot('sendMessage',[
  'chat_id'=>$chat_id,
  'text'=>"
تم حظر المجموعة 
",
  'reply_to_message_id'=>$message_id,
   ]);
bot('LeaveChat',[
  'chat_id'=>$chat_id,
  ]);
  }
}
  elseif(  $text == 'تعطيل' ){
  if (in_array($from_id,$Dev)){
bot('sendMessage',[
  'chat_id'=>$chat_id,
  'text'=>"
 🚸¦ تم تعطيل البوت من المجموعة 
🔬¦ تم تعطيل الحماية
√
",
'reply_to_message_id'=>$message_id,
   ]);
unlink("data/$chat_id.json");
   }  
  }   
  elseif ( strpos($text , "وضع كلايش") !== false) {
if ( $status == 'creator' or $status == 'administrator' or in_array($from_id,$Dev) or in_array($from_id,$useradmin) or in_array($from_id,$getCCmember)){
$num = str_replace(['وضع كلايش '],'',$text);
$add = $settings["information"]["added"];
if ($add == true) {
$te = explode(" ",$num);
$startlock = $te[0];
$endlock = $te[1];
		  bot('sendmessage',[
        'chat_id'=>$chat_id,
        'text'=>"
        💬┇بواسطه ~⪼ [$first_name](t.me/$username)
☑┇تم وضع عدد الكلايش $startlock
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,
'reply_to_message_id'=>$message_id,
'reply_markup'=>$inlinebutton,
   ]);
$settings["information"]["downcharacter"]="$startlock";
$settings["information"]["pluscharacter"]="$endlock";
$settings = json_encode($settings,true);
file_put_contents("data/$chat_id.json",$settings); 
}

}
}
  elseif($text=="اعدادات" or $text=="الاعدادات" ){
if ( $status == 'creator' or $status == 'administrator' or in_array($from_id,$Dev) or in_array($from_id,$useradmin) or in_array($from_id,$getCCmember)){
$locklink = $settings["lock"]["link"];
$linkr = $settings["lock"]["linkr"];
$lockusername = $settings["lock"]["username"];
$locktag = $settings["lock"]["tag"];
$lockedit = $settings["lock"]["edit"];
$lockfosh = $settings["lock"]["fosh"];
$en = $settings["lock"]["en"];
$ar = $settings["lock"]["ar"];
$spam = $settings["lock"]["spam"];
$rdodsg = $settings["lock"]["rdodsg"];
$photor = $settings["lock"]["photor"];
$markdowns = $settings["lock"]["markdowns"];
$farse = $settings["lock"]["farse"];
$tsmet = $settings["lock"]["tsmet"];
$lockbots = $settings["lock"]["bot"];
$lockbotsk = $settings["lock"]["botk"];
$lockforward = $settings["lock"]["forward"];
$lockforwardk = $settings["lock"]["forwardr"];
$locktg = $settings["lock"]["tgservic"];
$lockreply = $settings["lock"]["reply"];
$iduser = $settings["lock"]["iduser"];
$lockdocument = $settings["lock"]["document"];
$lockgif = $settings["lock"]["gif"];
$gifr = $settings["lock"]["gifr"];
$inline = $settings["lock"]["inline"];
$lockvideo_note = $settings["lock"]["video_msg"];
$locklocation = $settings["lock"]["location"];
$lockphoto = $settings["lock"]["photo"];
$lockcontact = $settings["lock"]["contact"];
$lockaudio = $settings["lock"]["audio"];
$lockvoice = $settings["lock"]["voice"];
$locksticker = $settings["lock"]["sticker"];
$lockgame = $settings["lock"]["game"];
$lockvideo = $settings["lock"]["video"];
$videor = $settings["lock"]["videor"];
$locktext = $settings["lock"]["text"];
$mute_all = $settings["lock"]["mute_all"];
$welcome = $settings["information"]["welcome"];
$add = $settings["information"]["add"];
$setwarn = $settings["information"]["setwarn"];
$charge = $settings["information"]["charge"];
$lockauto = $settings["lock"]["lockauto"];
$lockcharacter = $settings["lock"]["lockcharacter"];
$startlock = $settings["information"]["timelock"];
$endlock = $settings["information"]["timeunlock"];
$startlockcharacter = $settings["information"]["pluscharacter"];
$endlockcharacter = $settings["information"]["downcharacter"];
$text = str_replace("| فعال |","","⚜┊️اعدادات المجموعة
••┉┉┉┉┉┉┉┉┉┉┉┉┉••
⚜┊التـاك »  $locktag 
⚜┊المعرفات »  $lockusername 
⚜┊التعديل »  $lockedit 
⚜┊الروابط »  $locklink 
⚜┊المتحركه »  $lockgif 
⚜┊الصور »  $lockphoto 
⚜┊الايدي »  $iduser 
⚜┊التكرار »  $spam 
⚜┊الموسيقى »  $lockaudio 
⚜┊البصمة »  $lockvoice 
⚜┊الكلايش »  $lockcharacter 
⚜┊الالعاب »  $lockgame 
⚜┊التوجيه »  $lockforward 

⚜┊السيئات »  $lockfosh 
⚜┊الرد »  $lockreply 
⚜┊الاشعارات »  $locktg 
⚜┊بصمة الفيديو »  $lockvideo_note 
⚜┊المواقع »  $locklocation 

⚜┊الانلاين »  $inline 
⚜┊الجهات »  $lockcontact 
⚜┊الماركدوان »  $markdowns 
⚜┊الردود  $rdodsg 
⚜┊الملصقات »  $locksticker 
⚜┊العربية »  $ar 
⚜┊الاتجليزية »  $en 
⚜┊الدردشة »  $locktext 
⚜┊البوتات بالطرد »  $lockbotsk 
⚜┊البوتات »  $lockbots 

💱┊اعدادات التقـييد :
📮┊ـ➖➖➖➖➖
⚜┊التقييد بالتوجيه »  $lockforwardk 
⚜┊التقييد بالصور »  $photor 
⚜┊التقييد بالروابط »  $linkr 
⚜┊التقييد بالمتحركه »  $gifr 
⚜┊التقييد بالفيديو »  $videor
");
$text2 = str_replace("| غیر فعال |","","$text");
bot('sendmessage',[ 
 'chat_id'=>$chat_id,
 'text'=>"$text2",
'reply_to_message_id'=>$message_id,
   ]);
}
}

/*=====================================
=    نظام الفخر والهيبة (مدح البوت)    =
=====================================*/

// 1. مصفوفة كلمات المدح (20 كلمة عراقية قح)
$praise_patterns = '/(بوت جميل|بوت اسطوري|بوت معدل|بوت هيبة|عاش المطور|بوت مرتب|بوت ضيم|بوت فلك|خوش بوت|ارقى بوت|بوت فنان|بوت ذكي|بوت الامبراطور|بوت وحش|بوت كفو|بوت غيرة|بوت نشمي|بوت لوز|بوت لقطة|بوت صاكة)/u';

// 2. مصفوفة الردود الفخمة (20 رد مزخرف ثخين)
$praise_replies = [
    "‏**أدري بـ نـفـسـي هـيـبـة، تـربـاة الإمـبـراطـور بـعـد!** 👑",
    "‏**الـمـعـدل مـا يـجـيـب إلا الـمـعـدل مـثـلـي.. تـسـلـم يـا ذوق** ✨",
    "‏**الـصـيـت لـلـمـطـور والـفـعـل لـي.. نـورت الـشـات حـبـي** 🦅",
    "‏**مـو بـس بـوت، أنـي تـاريـخ بـالـبـرمـجـة يـا بـطـل** 📚",
    "‏**عـيـونـك الـجـمـيـلـة هـاي، بـس لا تـحـسـدنـي فـدوه** 🧿",
    "‏**أنـي الـصـادق والـمـطـقـق، مـو بـوت كـلاوات مـثـل غـيـري** 🦾",
    "‏**الـشـاحـنـة نـقـاط والـعـقـل مـاس.. هـذا أنـي بـوتـك الـخـاص** 💎",
    "‏**كـفـوك الـطـيـب، إحـنـا أهـل الـغـيـرة والـتـقـنـيـة** 🇮🇶",
    "‏**أشـكـر فـنـك.. رفـعـت مـعـنـويـات الـسـيـرفـر مـالـتـي** 🚀",
    "‏**أسـطـوري؟ هـاي كـلـمـة قـلـيـلـة بـحـق كـوداتـي الـعـظـيـمـة** 🌌",
    "‏**أطـگ عـلـى الـجـرح وأقـصـف الـعـذال.. أنـي بـوت الإمـبـراطـور** 💣",
    "‏**مـرتـب ومـنـضـم مـثـل قـصـر الـمـلـك.. نـورتـنـي** 🏛️",
    "‏**لـو كـل الـبـوتـات مـثـلي، جـان تـلـيـجـرام صـار جـنـة** 🌸",
    "‏**تـسـلـم يـا نـشـمي، هـذا مـن طـيـب أصـلـك الـعـراقي** 🦁",
    "‏**الـذكـاء عـنـدي وراثة، والـقـصـف عـنـدي هـوايـة** 🎯",
    "‏**أنـي الـذي نـظـر الأعـمـى إلـى كـوداتـي.. نـورت حـبي** 😎",
    "‏**لا تـذوبـنـي بـكلامـك، تـره الـهارد مـالـتـي يـحـتـرگ** 🔥",
    "‏**الـهـيـبـة تـلـوگ لـلـمـعـدل، وأنـي بـوت مـعـدل ومـعـزز** 🏅",
    "‏**فـديـتـك وفـديـت ذوقـك الـعـالـي، خـلـيـك مـتـفـاعـل حـتـى أحـبـك أكـثـر** ❤️",
    "‏**أنـي مـصـمـم لـلـقـمـة، والـقـمـة مـحـجـوزة بـاسـمـي** 🏆"
];

// 3. محرك التنفيذ (البحث والرد)
if(preg_match($praise_patterns, $text)){
    $random_praise = $praise_replies[array_rand($praise_replies)];
    bot('sendMessage', [
        'chat_id' => $chat_id,
        'text' => $random_praise,
        'parse_mode' => "Markdown",
        'reply_to_message_id' => $message_id
    ]);
}

 
//add
if ( $text == "تفعيل") {
if ($status == 'creator' or $status == 'administrator'){
if ($tc == 'group' | $tc == 'supergroup'){
$add = $settings["information"]["added"];
if ($add != true) {
bot('sendMessage',[
    	'chat_id'=>$chat_id,
    	'text'=>"
📮¦ تـم تـفـعـيـل الـمـجـمـوعـه ✓️ 
👨🏽‍🔧¦ وتم رفع جمـيع آلآدمـنيهہ‌‌‏ آلگروب بآلبوت 
    ✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,
'reply_to_message_id'=>$message_id,
	
 ]);  
 		        bot('sendmessage',[
        'chat_id'=>$Dev[0],
        'text'=>"تم اضافة مجموعة جديدة بواسطة المشرف ✅
➖➖➖➖➖
🚩معلومات المجموعة  :

🔅ايدي المجموعة : [$chat_id]

💭اسم المجموعة : [$namegroup]

بواسطة : [ @$username ] 
", 
    ]); 
$dateadd = date('Y-m-d', time());
$dateadd2 = isset($_GET['date']) ? $_GET['date'] : date('Y-m-d');
$next_date = date('Y-m-d', strtotime($dateadd2 ." +999 day"));
    $settings = '{"lock": {
            "text": "مفتوح",
            "photo": "مفتوح",
            "link": "مفتوح",
            "tag": "مفتوح",
			"username": "مفتوح",
            "sticker": "مفتوح",
            "video": "مفتوح",
            "voice": "مفتوح",
            "audio": "مفتوح",
            "tsmet": "مفتوح",
            "iduser": "مفتوح",
            "gif": "مفتوح",
            "bot": "مفتوح",
            "forward": "مفتوح",
            "document": "مفتوح",
            "tgservic": "مفتوح",
			"edit": "مفتوح",
			"reply": "مفتوح",
			"contact": "مفتوح",
			"location": "مفتوح",
			"game": "مفتوح",
			"cmd": "مفتوح",
			"en": "مفتوح",
			"ar": "مفتوح",
			"rdodsg": "مقفول",
			"spam": "مفتوح",
			"mute_all": "مفتوح",
			"mute_all_time": "مفتوح",
			"markdowns": "مفتوح", 
            "fosh": "مفتوح",
            "farse": "مفتوح",
			"lockauto": "مفتوح",
			"lockcharacter": "مفتوح",
			"video_msg": "مفتوح"
		},
		"information": {
        "added": "true",
		"welcome": "مفتوح",
		"add": "مفتوح",
		"lockchannel": "مفتوح",
		"hardmodebot": "مفتوح",
		"hardmodewarn": "بالتقييد",
		"charge": "999 يوم",
		"setadd": "3",
		"spamx": "5",
		"dataadded": "",
		"expire": "",
		"msg": "",
		"timelock": "00:00",
		"timeunlock": "00:00",
		"pluscharacter": "300",
		"downcharacter": "0",
		"textwelcome": "اهلا بك عزيزي",
		"rules": "⚜┇لم يتم حفظ قوانين للمجموعه",
		"setwarn": "3"
		}
}';
    $settings = json_decode($settings,true);
	$settings["information"]["expire"]="$next_date";
	$settings["information"]["dataadded"]="$dateadd";
	$settings["information"]["msg_id"]="$message_id";
    $settings = json_encode($settings,true);
    file_put_contents("data/$chat_id.json",$settings);
$gpadd = fopen("data/group.txt",'a') or die("Unable to open file!");  
fwrite($gpadd, "اسم المجموعة : [$namegroup] | ايدي المجموعة : [$chat_id]\n");
fclose($gpadd);
}
else
{
$dataadd = $settings["information"]["dataadded"];
bot('sendMessage',[
    	'chat_id'=>$chat_id,
    	'text'=>"
🎗¦ المجموعه بالتأكيد ✓️ تم تفعيلها
",'reply_to_message_id'=>$message_id,
 ]); 
}
}
}
}
 

if( $text=="/start" &&  $tc == "private" or $text=="🔙  رجوع" &&  $tc == "private" ){
if(in_array($from_id,$Dev)){
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
🎖¦ آهہ‏‏لآ عزيزي آلمـطـور 🍃
💰¦ آنتهہ‏‏ آلمـطـور آلآسـآسـي هہ‏‏نآ 🛠
🚸¦ تسـتطـيع‏‏ آلتحگم بگل آلآوآمـر آلمـمـوجودهہ‏‏ بآلگيبورد
⚖️¦ فقط آضـغط ع آلآمـر آلذي تريد تنفيذهہ‏‏
",
     'reply_to_message_id'=>$message_id,
  'reply_markup'=>json_encode([
'keyboard'=>[
[
['text'=>"🤖 تعيين اسم للبوت 🤖"],['text'=>"👮‍♂ تعيين كليشة مطور"]
],
[
['text'=>"🚷 حظر عام 🚷"],['text'=>"🚷 الغاء حظر عام 🚷"]
],
[
['text'=>"🔊 اضف رد عام 🔊"],['text'=>"🔊 حذف رد عام 🔊♂"]
],
[
['text'=>"🔉 الردود العامة 🔉"]
],
[
['text'=>"🔉 مسح الردود 🔉"]
],
[
['text'=>"❗️حظر مجموعة❗️"],['text'=>"📊 الاحصائيات 📊"]
],
[
['text'=>"🔈 اذاعة بالمجموعات🔈"],['text'=>"🔈 اذاعة بالخاص🔈"]
],
[
['text'=>"🔊 توجيه بالمجموعات"],['text'=>"توجيه بالخاص 🔊"]                            
],
],
  'resize_keyboard'=>true
])
]);
}
}
$setnamebot = file_get_contents("setname.txt");
$namebot = file_get_contents("namebot.txt");
if ($text == "🤖 تعيين اسم للبوت 🤖" and in_array($from_id,$Dev)){
file_put_contents("setname.txt","nam");
bot("sendMessage",[
"chat_id"=>$chat_id,
"text"=>"📭¦ حسننا عزيزي المطور،
🗯¦ الان ارسل الاسم  للبوت 
√",'parse_mode'=>"MARKDOWN",
 'reply_to_message_id'=>$message_id
,]);}
if($text && $setnamebot =="nam" and in_array($from_id,$Dev)){
file_put_contents("namebot.txt",$text); 
file_put_contents("setname.txt","");
bot("sendmessage",[
"chat_id"=>$chat_id,
"text" => "✓ تم اضافت اسم للبوت 🚀 
 -",'parse_mode'=>"MARKDOWN",
 'reply_to_message_id'=>$message_id
,]);}

if($text == "بوت" || $text == "شسمك"){
if ($tc == 'group' | $tc == 'supergroup'){
bot('sendMessage',[
'chat_id'=>$chat_id, 
'text'=>"اسمي $namebot 🌚🌸"
,'parse_mode'=>"MARKDOWN",
 'reply_to_message_id'=>$message_id,
]);}}

$message = $update->message;
$arr = array('اجيت اجيت كافي لتصيح 🌚👌',
'​• ━━━━━━━━━━━━━━ •
• نورتـنا يـا حـلو بـانضمامـك 🎀 ❕
• ━━━━━━━━━━━━━━ •
• خـليك حـباب ومـتفاعل لـتصير صـنم 🗿
• بـوت الحـماية في خـدمتك 💂🏻‍♀️',
);
$arr1 = array_rand($arr,true);
if($message){

$get = file_get_contents("msg.txt")+1; 
file_put_contents("msg.txt",$get); 
if ($settings["lock"]["rdodsg"] == "مقفول️"){
if($get == "5" or $text == $namebot ){
if ($tc == 'group' | $tc == 'supergroup'){
bot("sendMessage",[
"chat_id"=>$chat_id,
"text"=>$arr[$arr1],
 'reply_to_message_id'=>$message_id,
]);
} 
}
}
}

if ($text == "/start" && $tc == "private") {
    // 1. منطق حفظ المستخدم في ملف users.txt
    $userlist = file_get_contents("users.txt");
    if (strpos($userlist, (string)$from_id) === false) {
        file_put_contents('users.txt', $from_id . "\n", FILE_APPEND);
    }

    // 2. إرسال الصورة مع النص والأزرار
    bot('sendPhoto', [
        'chat_id' => $chat_id,
        'photo' => "https://t.me/LI7ON12/11",
        'caption' => "• اهلا بك عزيزي [$name](tg://user?id=$from_id) 🎀\n" .
                     "☙︙اختصاصي حماية المجموعات من التفليش والسبام\n" .
                     "☙︙لتفعيل البوت عليك اتباع مايلي\n" .
                     "❧ ︙اضفني لمجموعتك وقم بترقيتي مشرف ثم اكتب الاوامر لعرض التعليمات\n" .
                     "❧ ︙ او اكتب الاعددات لعرض الميزات المفتوحة والمغلقة\n" .
                     "   ➥┇𝙻𝙰𝚂𝚃 𝚄𝙿𝙳𝙰𝚃𝙴 12/𝟶2/𝟸𝟺",
        'parse_mode' => "MarkDown",
        'has_spoiler' => true,
        'reply_to_message_id' => $message_id,
        'reply_markup' => json_encode([
            'inline_keyboard' => [
                [['text' => "➕ ADD 🐾", 'url' => "http://t.me/V_JLBOT?startgroup=new"]],
                [['text' => "𝙳𝙴𝚅 🦋", 'url' => "t.me/Mi2k_12"], ['text' => "𝙷𝙴𝙻𝙿 🐝", 'url' => "https://t.me/"]],
                [['text' => "𝚅𝙸𝚂𝙲𝙾 𝚂𝙾𝚄𝚁𝙲𝙴 𝙳𝚉 🕷️", 'url' => "https://t.me/liyon11"]]


            ]
        ])
    ]);
}



$kdeveloper = file_get_contents("kdevelopers.txt");
$kdevelopers = file_get_contents("kdeveloper.txt");
if ($text == "👮‍♂ تعيين كليشة مطور" and in_array($from_id,$Dev)){
file_put_contents("kdevelopers.txt","namdev");
bot("sendMessage",[
"chat_id"=>$chat_id,
"text"=>"📭¦ حسننا عزيزي المطور،
🗯¦ الان ارسل كليشة المطور
√",'parse_mode'=>"MARKDOWN",
 'reply_to_message_id'=>$message_id
,]);}


if($text && $kdeveloper =="namdev" and in_array($from_id,$Dev)){
file_put_contents("kdeveloper.txt",$text); 
file_put_contents("kdevelopers.txt","");
bot("sendmessage",[
"chat_id"=>$chat_id,
"text" => "✓ تم اضافت كليشة المطور 🚀 
 -",'parse_mode'=>"MARKDOWN",
 'reply_to_message_id'=>$message_id
,]);}
if($text == "المطور" ){
if ($tc == 'group' | $tc == 'supergroup'){
bot('sendMessage',[
'chat_id'=>$chat_id, 
'text'=>"$kdevelopers",
'parse_mode'=>"markdown",'disable_web_page_preview'=>true,
 'reply_to_message_id'=>$message_id,
]);}}

if($text=="🚷 حظر عام 🚷" && $tc == "private" ){
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
📭¦ حسننا عزيزي المطور،
🗯¦ الان ارسل حظر عام + الايدي
√
",
]);}
elseif( strpos($text , "حظر عام") !== false) {
if (in_array($from_id,$Dev)) {
$text = str_replace(['حظر عام'],'',$text);
$stat = file_get_contents("https://api.telegram.org/bot$token/getChatMember?chat_id=$text&user_id=".$text);
$statjson = json_decode($stat, true);
$name = $statjson['result']['user']['first_name'];
$username = $statjson['result']['user']['username'];
$id = $statjson['result']['user']['id'];
bot('sendmessage',[
        'chat_id'=>$chat_id,
        'text'=>"
🙋🏼‍♂️¦ العضو @$username
📡¦ الايدي `$id`
💯¦ تم حظره عام
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,
'reply_to_message_id'=>$message_id,
'reply_markup'=>$inlinebutton,
 ]);
$user["banlist"][]="$text";
$user = json_encode($user,true);
file_put_contents("data/user.json",$user);
}
}
if($text=="🚷 الغاء حظر عام 🚷" && $tc == "private" ){
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
📭¦ حسننا عزيزي المطور،
🗯¦ الان ارسل الغاء حظر عام + الايدي
√
",
]);}
elseif ( strpos($text , "الغاء حظر عام") !== false) {
if (in_array($from_id,$Dev)) {
$text = str_replace(['الغاء حظر عام'],'',$text);
$stat = file_get_contents("https://api.telegram.org/bot$token/getChatMember?chat_id=$text&user_id=".$text);
$statjson = json_decode($stat, true);
$name = $statjson['result']['user']['first_name'];
$username = $statjson['result']['user']['username'];
$id = $statjson['result']['user']['id'];
bot('sendmessage',[
        'chat_id'=>$chat_id,
        'text'=>"
🙋🏼‍♂️¦ العضو @$username
📡¦ الايدي `$id`
💯¦ تم الغاء حظره عام
✓
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,
'reply_to_message_id'=>$message_id,
'reply_markup'=>$inlinebutton,
 ]);
$key = array_search($text,$user["banlist"]);
unset($user["banlist"][$key]);
$user["banlist"] = array_values($user["banlist"]); 
$user = json_encode($user,true);
file_put_contents("data/user.json",$user);
}
}
elseif( $text == "المحظورين عام" or $text == "🚫 المحظورين عام 🚫") {
if ( in_array($from_id,$Dev)) {
$silent = $user["banlist"];
for($z = 0;$z <= count($silent)-1;$z++){
$result = $result.$silent[$z]."\n";
}
  bot('sendMessage',[
'chat_id'=>$chat_id,
'text'=>"
☑┇قائمة المحظورين

$result
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,
'reply_to_message_id'=>$message_id,
'reply_markup'=>$inlinebutton,
 ]);
}
}
elseif($text=="❗️حظر مجموعة❗️" ){
if ($tc == "private") {
if (in_array($from_id,$Dev)) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
📭¦ حسننا عزيزي المطور،
🗯¦ الان ارسل غادر + ايدي مجموعة
√
",
'reply_to_message_id'=>$message_id,
 ]);
}
}
}
elseif(strpos($text , "غادر" ) !== false ) {
$text = str_replace(['غادر'],'',$text);
if ($tc == "private") {
if (in_array($from_id,$Dev)) {
bot('sendmessage',[
'chat_id'=>$chat_id,
'text'=>"
📭¦ حسننا عزيزي المطور،
🗯¦ تم مغادرة المجموعة بنجاح
√
",
  ]);
bot('LeaveChat',[
  'chat_id'=>$text,
  ]);
unlink("data/$text.json");
}
}
}
elseif($text=="📊 الاحصائيات 📊"){
$users = count($user["userlist"]);
$group = count($user["grouplist"]);
			bot('sendmessage',[
	'chat_id'=>$chat_id,
	'text'=>"🤖 الاحصائيات هي :

👥 عدد المجموعات: *132K*

👤 عدد المستخدمين: *27k*
",
            'hide_keyboard'=>true,
	]);
	}
elseif ($text == '🔈 اذاعة بالخاص🔈' && in_array($from_id,$Dev)) {
     bot('sendmessage',[
    	'chat_id'=>$chat_id,
    	'text'=>"
📭¦ حسننا عزيزي المطور،
🗯¦ ارسل رسالتك الان
√",
  'reply_to_message_id'=>$message_id,
   'reply_markup'=>json_encode([
'keyboard'=>[
[
['text'=>"🔙  رجوع"] 
]
   ],
  'resize_keyboard'=>true
   ])
 ]);
$user["userjop"]["$from_id"]["file"]="senduser";
$user = json_encode($user,true);
file_put_contents("data/user.json",$user);
}
elseif ($text == '🔈 اذاعة بالمجموعات🔈' && in_array($from_id,$Dev)) {
     bot('sendmessage',[
    	'chat_id'=>$chat_id,
    	'text'=>"
📭¦ حسننا عزيزي المطور،
🗯¦ ارسل رسالتك الان
√",
  'reply_to_message_id'=>$message_id,
   'reply_markup'=>json_encode([
'keyboard'=>[
[
['text'=>"🔙  رجوع"] 
]
   ],
  'resize_keyboard'=>true
   ])
 ]);
$user["userjop"]["$from_id"]["file"]="sendgroup";
$user = json_encode($user,true);
file_put_contents("data/user.json",$user);
}
elseif ($text == '🔊 توجيه بالمجموعات' && in_array($from_id,$Dev)) {
     bot('sendmessage',[
    	'chat_id'=>$chat_id,
    	'text'=>"🔊 توجيه بالمجموعات",
  'reply_to_message_id'=>$message_id,
   'reply_markup'=>json_encode([
'keyboard'=>[
[
['text'=>"🔙  رجوع"] 
]
   ],
  'resize_keyboard'=>true
   ])
 ]);
$user["userjop"]["$from_id"]["file"]="forwardgroup";
$user = json_encode($user,true);
file_put_contents("data/user.json",$user);
}
elseif ($text == 'توجيه بالخاص 🔊' && in_array($from_id,$Dev)) {
     bot('sendmessage',[
    	'chat_id'=>$chat_id,
    	'text'=>"
📭¦ حسننا عزيزي المطور،
🗯¦ ارسل رسالتك الان
√",
			  'reply_to_message_id'=>$message_id,
			   'reply_markup'=>json_encode([
'keyboard'=>[
[
['text'=>"🔙  رجوع"] 
]
   ],
  'resize_keyboard'=>true
   ])
		]);
$user["userjop"]["$from_id"]["file"]="forwarduser";
$user = json_encode($user,true);
file_put_contents("data/user.json",$user);
}


elseif ($user["userjop"]["$from_id"]["file"] == 'forwarduser') {
$user["userjop"]["$from_id"]["file"]="none";
$numbers = $user["userlist"];
$user = json_encode($user,true);
file_put_contents("data/user.json",$user);	
if ($text != "رجوع  🔙") {
     bot('sendmessage',[
    	'chat_id'=>$chat_id,
    	'text'=>"تم ارسال الرسالة بنجاح مقفول️",
  'reply_to_message_id'=>$message_id,
 ]);
for($z = 0;$z <= count($numbers)-1;$z++){
Forward($numbers[$z], $chat_id,$message_id);
}
}
}
elseif ($user["userjop"]["$from_id"]["file"] == 'forwardgroup') {
$user["userjop"]["$from_id"]["file"]="none";
$numbers = $user["grouplist"];
$user = json_encode($user,true);
file_put_contents("data/user.json",$user);	
if ($text != "رجوع  🔙") {
     bot('sendmessage',[
    	'chat_id'=>$chat_id,
    	'text'=>" تم ارسال الرسالة بنجاحمقفول️",
  'reply_to_message_id'=>$message_id,
 ]);
for($z = 0;$z <= count($numbers)-1;$z++){
Forward($numbers[$z], $chat_id,$message_id);
}
}
}
elseif ($user["userjop"]["$from_id"]["file"] == 'sendgroup') {
$user["userjop"]["$from_id"]["file"]="none";
$numbers = $user["grouplist"];
$user = json_encode($user,true);
file_put_contents("data/user.json",$user);	
if ($text != "رجوع  🔙") {
     bot('sendmessage',[
    	'chat_id'=>$chat_id,
    	'text'=>"تم ارسال رسالتك بنجاح مقفول️",
  'reply_to_message_id'=>$message_id,
 ]);
for($z = 0;$z <= count($numbers)-1;$z++){
 bot('sendmessage',[
      'chat_id'=>$numbers[$z],        
	  'text'=>"$text",
    ]);
}
}
}
elseif ($user["userjop"]["$from_id"]["file"] == 'senduser') {
$user["userjop"]["$from_id"]["file"]="none";
$numbers = $user["userlist"];
$user = json_encode($user,true);
file_put_contents("data/user.json",$user);	
if ($text != "رجوع  🔙") {
     bot('sendmessage',[
    	'chat_id'=>$chat_id,
    	'text'=>"تم ارسال رسالتك بنجاح مقفول️",
  'reply_to_message_id'=>$message_id,
 ]);
for($z = 0;$z <= count($numbers)-1;$z++){
 bot('sendmessage',[
      'chat_id'=>$numbers[$z],        
	  'text'=>"$text",
    ]);
}
}
}
$message_id = $update->message->message_id;
$user          = $update->message->from->username;

/*
الاوامر كتٱلي : 
- اضف رد ، مسح رد ، الردود ، مسح الردود 
- اضف رد عام ، مسح رد عام ، الردود العامه ، مسح الردود العامه
*/

mkdir("data");
mkdir("data/addrd");

$opption = file_get_contents("data/addrd/$chat_id/opption.txt");
$get_from_id = file_get_contents("data/addrd/$chat_id/from_id.txt");
$get_rd = file_get_contents("data/addrd/$chat_id/getrd.txt");
$opption_ = file_get_contents("data/addrd/opption.txt");
$get_from_id1_ = file_get_contents("data/addrd/from_id.txt");
$I_get_rd = file_get_contents("data/addrd/getrd.txt");
$get_from_id_1 = explode("\n",$get_from_id1_);
$get_from_id_ = explode("\n",$get_from_id);



if($status == "creator" || $status == "administrator" || in_array($from_id,$Dev) || in_array($from_id,$useradmin) || in_array($from_id,$getCCmember) ) {
if($text == "اضف رد"){
	
mkdir("data/addrd/$chat_id");
mkdir("data/addrd/$chat_id/media");
mkdir("data/addrd/$chat_id/media/sticker");
mkdir("data/addrd/$chat_id/media/video");
mkdir("data/addrd/$chat_id/media/videonote");
mkdir("data/addrd/$chat_id/media/document");
mkdir("data/addrd/$chat_id/media/photo");
mkdir("data/addrd/$chat_id/media/audio");
mkdir("data/addrd/$chat_id/media/contact");

 file_put_contents("data/addrd/$chat_id/from_id.txt",$from_id);
 file_put_contents("data/addrd/$chat_id/opption.txt","GG1ZZ");
 bot("SendMessage",[
 "chat_id"=>$chat_id,
 "text"=>"📭¦ حسننا , الان ارسل كلمه الرد 
-",
 'reply_to_message_id'=>$message->message_id, 
 ]);
 }
 if($text and in_array($from_id,$get_from_id_) and $opption == "GG1ZZ"){
 	file_put_contents("data/addrd/$chat_id/opption.txt","IBADLZ");
     file_put_contents("data/addrd/$chat_id/mod.txt",$text);
     file_put_contents("data/addrd/$chat_id/media/media.txt",$text);
     file_put_contents("data/addrd/$chat_id/getrd.txt", "- ". $text . "\n" , FILE_APPEND);
 bot("SendMessage",[
 "chat_id"=>$chat_id,
 "text"=>"
📜¦ جيد , يمكنك الان ارسال جواب الرد 
🔛¦ [ نص,صوره,فيديو,متحركه,بصمه,اغنيه ] ✓
- 
",
 'reply_to_message_id'=>$message->message_id, 
 ]);
 }
 if($message and in_array($from_id,$get_from_id_) and $opption == "IBADLZ"){
  file_put_contents("data/addrd/$chat_id/opption.txt","");
  $IB_3ADLZ = file_get_contents("data/addrd/$chat_id/mod.txt");
  $IB_4ADLZ = file_get_contents("data/addrd/$chat_id/media/media.txt");

  $IB_2ADLZ = fopen("data/addrd/$chat_id/mod.txt", "a") or die("Unable to open file!"); 
   fwrite($IB_2ADLZ, "$IB_3ADLZ\n");
   fclose($IB_2ADLZ);
   
   $IB_5ADLZ = fopen("data/addrd/$chat_id/media/media.txt", "a") or die("Unable to open file!"); 
   fwrite($IB_5ADLZ, "$IB_4ADLZ\n");
   fclose($IB_5ADLZ);
   
   file_put_contents("data/addrd/$chat_id/$IB_3ADLZ.txt",$text);
   file_put_contents("data/addrd/$chat_id/mod.txt","");
   file_put_contents("data/addrd/$chat_id/media/media.txt","");
   file_put_contents("data/addrd/$chat_id/media/$IB_4ADLZ.txt",$message->voice->file_id);
   file_put_contents("data/addrd/$chat_id/media/sticker/$IB_4ADLZ.txt",$message->sticker->file_id );
   file_put_contents("data/addrd/$chat_id/media/document/$IB_4ADLZ.txt",$message->document->file_id);
   file_put_contents("data/addrd/$chat_id/media/videonote/$IB_4ADLZ.txt",$message->video_note->file_id);
   file_put_contents("data/addrd/$chat_id/media/contact/$IB_4ADLZ.txt",$message->contact->phone_number);
   file_put_contents("data/addrd/$chat_id/media/video/$IB_4ADLZ.txt",$message->video->file_id);
   file_put_contents("data/addrd/$chat_id/media/photo/$IB_4ADLZ.txt",$message->photo[0]->file_id);
   file_put_contents("data/addrd/$chat_id/media/audio/$IB_4ADLZ.txt",$message->audio->file_id );
 bot("SendMessage",[
 "chat_id"=>$chat_id,
 "text"=>"*مقفول️ تم ٱضافةهہ الرد بنجٱح ،*",
 'parse_mode'=>"MARKDOWN",
 'reply_to_message_id'=>$message->message_id, 
 ]);
 }
 
 if($text == "مسح رد"){
 file_put_contents("data/addrd/$chat_id/from_id.txt",$from_id);
 file_put_contents("data/addrd/$chat_id/opption.txt","delete");
 bot("SendMessage",[
 "chat_id"=>$chat_id,
 "text"=>"*📭¦ حسننا عزيزي  ✋🏿
🗯¦ الان ارسل الرد لمسحها من  للمجموعه 🍃*",
 'parse_mode'=>"MARKDOWN",
 'reply_to_message_id'=>$message->message_id, 
 ]);
 }
 
 if(file_exists("data/addrd/$chat_id/$text.txt") and in_array($from_id,$get_from_id_) and $opption == "delete"){
 	$str = str_replace("- $text","",$get_rd);
     file_put_contents("data/addrd/$chat_id/getrd.txt",$str);
      file_put_contents("data/addrd/$chat_id/from_id.txt","");
      file_put_contents("data/addrd/$chat_id/opption.txt","");
 	unlink("data/addrd/$chat_id/$text.txt");
     unlink("data/addrd/$chat_id/media/$text.txt");
     unlink("data/addrd/$chat_id/media/sticker/$text.txt");
     unlink("data/addrd/$chat_id/media/video/$text.txt");
     unlink("data/addrd/$chat_id/media/videonote/$text.txt");
     unlink("data/addrd/$chat_id/media/document/$text.txt");
     unlink("data/addrd/$chat_id/media/photo/$text.txt");
     unlink("data/addrd/$chat_id/media/audio/$text.txt");
     unlink("data/addrd/$chat_id/media/contact/$text.txt");
 bot("SendMessage",[
 "chat_id"=>$chat_id,
 "text"=>"*($text)
  ✓ تم مسح الرد 🚀* ",
 'parse_mode'=>"MARKDOWN",
 'reply_to_message_id'=>$message->message_id, 
 ]);
 }
 
elseif(!file_exists("data/addrd/$chat_id/$text.txt") and in_array($from_id,$get_from_id_) and $opption == "delete"){
	file_put_contents("data/addrd/$chat_id/from_id.txt","");
    file_put_contents("data/addrd/$chat_id/opption.txt","");
 bot("SendMessage",[
 "chat_id"=>$chat_id,
 "text"=>"*💬¦ هذا الرد ليس مضاف في قائمه الردود 📛*",
 'parse_mode'=>"MARKDOWN",
 'reply_to_message_id'=>$message->message_id, 
 ]);
 }

if($text == "مسح الردود"){
$links = __DIR__ . "/data/addrd/$chat_id";
$media = __DIR__ . "/data/addrd/$chat_id/media";
$media_contact = __DIR__ . "/data/addrd/$chat_id/media/contact";
$media_document = __DIR__ . "/data/addrd/$chat_id/media/document";
$media_video = __DIR__ . "/data/addrd/$chat_id/media/video";
$media_videonote = __DIR__ . "/data/addrd/$chat_id/media/videonote";
$media_photo = __DIR__ . "/data/addrd/$chat_id/media/photo";
$media_sticker = __DIR__ . "/data/addrd/$chat_id/media/sticker";
$media_audio = __DIR__ . "/data/addrd/$chat_id/media/audio";


$files = scandir($links);
$files_media = scandir($media);
$files_media_contact = scandir($media_contact);
$files_media_document = scandir($media_document);
$files_media_video = scandir($media_video);
$files_media_videonote = scandir($media_videonote);
$files_media_photo = scandir($media_photo);
$files_media_sticker = scandir($media_sticker);
$files_media_audio = scandir($media_audio);

foreach ($files as $file) {
if(is_file($links . "/" . $file)){
	unlink ($links . "/" .$file);
}
}
foreach ($files_media as $filemedia) {
if(is_file($media . "/" . $filemedia)){
	unlink ($media . "/" .$filemedia);
}
}
foreach ($files_media_contact as $file_media_contact) {
if(is_file($media_contact . "/" . $file_media_contact)){
	unlink ($media_contact . "/" .$file_media_contact);
}
}
foreach ($files_media_document as $file_media_document) {
if(is_file($media_document . "/" . $file_media_document)){
	unlink ($media_document . "/" .$file_media_document);
}
}
foreach ($files_media_video as $file_media_video) {
if(is_file($media_video . "/" . $file_media_video)){
	unlink ($media_video . "/" .$file_media_video);
}
}
foreach ($files_media_videonote as $file_media_videonote) {
if(is_file($media_videonote . "/" . $file_media_videonote)){
	unlink ($media_videonote . "/" .$file_media_videonote);
}
}
foreach ($files_media_photo as $file_media_photo) {
if(is_file($media_photo . "/" . $file_media_photo)){
	unlink ($media_photo . "/" .$file_media_photo);
}
}
foreach ($files_media_sticker as $file_media_sticker) {
if(is_file($media_sticker . "/" . $file_media_sticker)){
	unlink ($media_sticker . "/" . $file_media_sticker);
}
}
foreach ($files_media_audio as $file_media_audio) {
if(is_file($media_audio . "/" . $file_media_audio)){
	unlink ($media_audio . "/" . $file_media_audio);
}
}
bot("SendMessage",[
'chat_id'=>$chat_id,
'text'=>"*✓ تم مسح كل الردود 🚀*",
'parse_mode'=>"MARKDOWN",
'reply_to_message_id'=>$message->message_id,
]);
file_put_contents("data/addrd/$chat_id/getrd.txt", "");
}


if($text == "الردود" and $get_rd != NULL and $get_rd != "" and $get_rd != " " and $get_rd != "\n\n" and $get_rd != "\n" and $get_rd != "\n\n\n" and $get_rd != "\n\n\n\n" and $get_rd != "\n\n\n\n\n" and $get_rd != "\n\n\n\n\n\n"){
	bot("SendMessage",[
'chat_id'=>$chat_id,
'text'=>"*💬¦ ردود البوت في المجموعه  :

$get_rd

➖➖➖*",
'parse_mode'=>"MARKDOWN",
'reply_to_message_id'=>$message->message_id,
]);
}
if($text == "الردود" and $get_rd == NULL || $get_rd == "" || $get_rd == " " || $get_rd == "\n\n" || $get_rd == "\n" || $get_rd == "\n\n\n" || $get_rd == "\n\n\n\n" || $get_rd == "\n\n\n\n\n" || $get_rd == "\n\n\n\n\n\n"){
	bot("SendMessage",[
'chat_id'=>$chat_id,
'text'=>"*🚸¦ لا يوجد ردود مضافه حاليا 
❕*",
'parse_mode'=>"MARKDOWN",
'reply_to_message_id'=>$message->message_id,
]);
}
}
if(in_array($from_id,$Dev)){
if($text == "اضف رد عام" || $text == "🔊 اضف رد عام 🔊"){
mkdir("data/addrd/media");
mkdir("data/addrd/$chat_id/media");
mkdir("data/addrd/media/sticker");
mkdir("data/addrd/media/video");
mkdir("data/addrd/media/videonote");
mkdir("data/addrd/media/document");
mkdir("data/addrd/media/photo");
mkdir("data/addrd/media/audio");
mkdir("data/addrd/media/contact");

 file_put_contents("data/addrd/from_id.txt",$from_id);
 file_put_contents("data/addrd/opption.txt","I_GG1ZZ");
 bot("SendMessage",[
 "chat_id"=>$chat_id,
 "text"=>"📭¦ حسننا , الان ارسل كلمه الرد 
-",
 'reply_to_message_id'=>$message->message_id, 
 ]);
 }
 if($text and in_array($from_id,$get_from_id_1) and $opption_ == "I_GG1ZZ"){
 	file_put_contents("data/addrd/opption.txt","I_BADLZ");
     file_put_contents("data/addrd/mod.txt",$text);
     file_put_contents("data/addrd/media/media.txt",$text);
     file_put_contents("data/addrd/getrd.txt", "- ". $text . "\n" , FILE_APPEND);
 bot("SendMessage",[
 "chat_id"=>$chat_id,
 "text"=>"📜¦ جيد , يمكنك الان ارسال جواب الرد 
🔛¦ [ نص,صوره,فيديو,متحركه,بصمه,اغنيه ] ✓
-",
 'reply_to_message_id'=>$message->message_id, 
 ]);
 }
 
 
 if($message and in_array($from_id,$get_from_id_1) and $opption_ == "I_BADLZ"){
  file_put_contents("data/addrd/opption.txt","");
  $IB_3ADLZ = file_get_contents("data/addrd/mod.txt");
  $IB_4ADLZ = file_get_contents("data/addrd/media/media.txt");

  $IB_2ADLZ = fopen("data/addrd/mod.txt", "a") or die("Unable to open file!"); 
   fwrite($IB_2ADLZ, "$IB_3ADLZ\n");
   fclose($IB_2ADLZ);
   
   $IB_5ADLZ = fopen("data/addrd/media/media.txt", "a") or die("Unable to open file!"); 
   fwrite($IB_5ADLZ, "$IB_4ADLZ\n");
   fclose($IB_5ADLZ);
   
   file_put_contents("data/addrd/$IB_3ADLZ.txt",$text);
   file_put_contents("data/addrd/mod.txt","");
   file_put_contents("data/addrd/media/media.txt","");
   file_put_contents("data/addrd/media/$IB_4ADLZ.txt",$message->voice->file_id);
   file_put_contents("data/addrd/media/sticker/$IB_4ADLZ.txt",$message->sticker->file_id );
   file_put_contents("data/addrd/media/document/$IB_4ADLZ.txt",$message->document->file_id);
   file_put_contents("data/addrd/media/videonote/$IB_4ADLZ.txt",$message->video_note->file_id);
   file_put_contents("data/addrd/media/contact/$IB_4ADLZ.txt",$message->contact->phone_number);
   file_put_contents("data/addrd/media/video/$IB_4ADLZ.txt",$message->video->file_id);
   file_put_contents("data/addrd/media/photo/$IB_4ADLZ.txt",$message->photo[0]->file_id);
   file_put_contents("data/addrd/media/audio/$IB_4ADLZ.txt",$message->audio->file_id );
 bot("SendMessage",[
 "chat_id"=>$chat_id,
 "text"=>"*مقفول️ تم ٱضافةهہ الرد بنجٱح ،*",
 'parse_mode'=>"MARKDOWN",
 'reply_to_message_id'=>$message->message_id, 
 ]);
 }
 
 if($text == "مسح رد عام" || $text == "🔊 حذف رد عام 🔊♂" ){
 file_put_contents("data/addrd/from_id.txt",$from_id);
 file_put_contents("data/addrd/opption.txt","I_delete");
 bot("SendMessage",[
 "chat_id"=>$chat_id,
 "text"=>"*📭¦ حسننا عزيزي  ✋🏿
🗯¦ الان ارسل الرد لمسحها من  للمجموعه 🍃*",
 'parse_mode'=>"MARKDOWN",
 'reply_to_message_id'=>$message->message_id, 
 ]);
 }
 
 if(file_exists("data/addrd/$text.txt") and in_array($from_id,$get_from_id_1) and $opption_ == "I_delete"){
 	$str = str_replace("- $text","",$I_get_rd);
     file_put_contents("data/addrd/getrd.txt",$str);
      file_put_contents("data/addrd/from_id.txt","");
      file_put_contents("data/addrd/opption.txt","");
 	unlink("data/addrd/$text.txt");
     unlink("data/addrd/media/$text.txt");
     unlink("data/addrd/media/sticker/$text.txt");
     unlink("data/addrd/media/video/$text.txt");
     unlink("data/addrd/media/videonote/$text.txt");
     unlink("data/addrd/media/document/$text.txt");
     unlink("data/addrd/media/photo/$text.txt");
     unlink("data/addrd/media/audio/$text.txt");
     unlink("data/addrd/media/contact/$text.txt");
 bot("SendMessage",[
 "chat_id"=>$chat_id,
 "text"=>"*($text)
  ✓ تم مسح الرد 🚀* ",
 'parse_mode'=>"MARKDOWN",
 'reply_to_message_id'=>$message->message_id, 
 ]);
 }
 
 elseif(!file_exists("data/addrd/$text.txt") and in_array($from_id,$get_from_id_1) and $opption_ == "I_delete"){
	file_put_contents("data/addrd/from_id.txt","");
    file_put_contents("data/addrd/opption.txt","");
 bot("SendMessage",[
 "chat_id"=>$chat_id,
 "text"=>"*🚸¦ لا يوجد ردود مضافه حاليا *",
 'parse_mode'=>"MARKDOWN",
 'reply_to_message_id'=>$message->message_id, 
 ]);
 }
 
 if($text == "مسح الردود العامه" || $text == "🔉 مسح الردود 🔉"){
$links = __DIR__ . "/data/addrd";
$media = __DIR__ . "/data/addrd/media";
$media_contact = __DIR__ . "/data/addrd/media/contact";
$media_document = __DIR__ . "/data/addrd/media/document";
$media_video = __DIR__ . "/data/addrd/media/video";
$media_videonote = __DIR__ . "/data/addrd/media/videonote";
$media_photo = __DIR__ . "/data/addrd/media/photo";
$media_sticker = __DIR__ . "/data/addrd/media/sticker";
$media_audio = __DIR__ . "/data/addrd/media/audio";


$files = scandir($links);
$files_media = scandir($media);
$files_media_contact = scandir($media_contact);
$files_media_document = scandir($media_document);
$files_media_video = scandir($media_video);
$files_media_videonote = scandir($media_videonote);
$files_media_photo = scandir($media_photo);
$files_media_sticker = scandir($media_sticker);
$files_media_audio = scandir($media_audio);

foreach ($files as $file) {
if(is_file($links . "/" . $file)){
	unlink ($links . "/" .$file);
}
}
foreach ($files_media as $filemedia) {
if(is_file($media . "/" . $filemedia)){
	unlink ($media . "/" .$filemedia);
}
}
foreach ($files_media_contact as $file_media_contact) {
if(is_file($media_contact . "/" . $file_media_contact)){
	unlink ($media_contact . "/" .$file_media_contact);
}
}
foreach ($files_media_document as $file_media_document) {
if(is_file($media_document . "/" . $file_media_document)){
	unlink ($media_document . "/" .$file_media_document);
}
}
foreach ($files_media_video as $file_media_video) {
if(is_file($media_video . "/" . $file_media_video)){
	unlink ($media_video . "/" .$file_media_video);
}
}
foreach ($files_media_videonote as $file_media_videonote) {
if(is_file($media_videonote . "/" . $file_media_videonote)){
	unlink ($media_videonote . "/" .$file_media_videonote);
}
}
foreach ($files_media_photo as $file_media_photo) {
if(is_file($media_photo . "/" . $file_media_photo)){
	unlink ($media_photo . "/" .$file_media_photo);
}
}
foreach ($files_media_sticker as $file_media_sticker) {
if(is_file($media_sticker . "/" . $file_media_sticker)){
	unlink ($media_sticker . "/" . $file_media_sticker);
}
}
foreach ($files_media_audio as $file_media_audio) {
if(is_file($media_audio . "/" . $file_media_audio)){
	unlink ($media_audio . "/" . $file_media_audio);
}
}
bot("SendMessage",[
'chat_id'=>$chat_id,
'text'=>"*✓ تم مسح كل الردود 🚀*",
'parse_mode'=>"MARKDOWN",
'reply_to_message_id'=>$message->message_id,
]);
file_put_contents("data/addrd/getrd.txt", "");
}


if($text == "الردود العامه" || $text == "🔉 الردود العامة 🔉" and $I_get_rd != NULL and $I_get_rd != "" and $I_get_rd != " " and $I_get_rd != "\n\n" and $I_get_rd != "\n" and $I_get_rd != "\n\n\n" and $I_get_rd != "\n\n\n\n" and $I_get_rd != "\n\n\n\n\n" and $I_get_rd != "\n\n\n\n\n\n"){
	bot("SendMessage",[
'chat_id'=>$chat_id,
'text'=>"*💬¦ الردود العامه في البوت :

$I_get_rd

➖➖➖*",
'parse_mode'=>"MARKDOWN",
'reply_to_message_id'=>$message->message_id,
]);
}
if($text == "الردود العامه" || $text == "🔉 الردود العامة 🔉"and $I_get_rd == NULL || $I_get_rd == "" || $I_get_rd == " " || $I_get_rd == "\n\n" || $I_get_rd == "\n" || $I_get_rd == "\n\n\n" || $I_get_rd == "\n\n\n\n" || $I_get_rd == "\n\n\n\n\n" || $I_get_rd == "\n\n\n\n\n\n"){
	bot("SendMessage",[
'chat_id'=>$chat_id,
'text'=>"🚸¦ لا يوجد ردود مضافه حاليا ❕*",
'parse_mode'=>"MARKDOWN",
'reply_to_message_id'=>$message->message_id,
]);
}
}


if($message->text and file_exists("data/addrd/$text.txt")) {
    $MoHaMMed = file_get_contents("data/addrd/$text.txt");
   bot('SendMessage',[
    'chat_id'=>$chat_id,
    'text'=>$MoHaMMed,
    'parse_mode'=>"MARKDOWN",
    'disable_web_page_preview'=>true,
    'reply_to_message_id'=>$message->message_id,
 ]);
 }
 if($message->text and file_exists("data/addrd/media/$text.txt")) {
  $MoHaMMed = file_get_contents("data/addrd/media/$text.txt");
   bot('Sendvoice',[
    'chat_id'=>$chat_id,
    'voice'=>$MoHaMMed,
    'reply_to_message_id'=>$message->message_id,
 ]);
 }
 if($message->text and file_exists("data/addrd/media/audio/$text.txt")) {
  $MoHaMMed = file_get_contents("data/addrd/media/audio/$text.txt");
 bot('SendAudio',[
    'chat_id'=>$chat_id,
    'audio'=>$MoHaMMed,
    'reply_to_message_id'=>$message->message_id,
 ]);
 }
 if($message->text and file_exists("data/addrd/media/sticker/$text.txt")) {
  $MoHaMMed = file_get_contents("data/addrd/media/sticker/$text.txt");
 bot('sendsticker',[
'chat_id'=>$chat_id,
'sticker'=>$MoHaMMed,
'reply_to_message_id'=>$message->message_id,
]);
}
if($message->text and file_exists("data/addrd/media/video/$text.txt")) {
  $MoHaMMed = file_get_contents("data/addrd/media/video/$text.txt");
bot('Sendvideo',[
'chat_id'=>$chat_id,
'video'=>$MoHaMMed,
'caption'=>$message->caption,
'reply_to_message_id'=>$message->message_id,
]);
}
if($message->text and file_exists("data/addrd/media/photo/$text.txt")) {
  $MoHaMMed = file_get_contents("data/addrd/media/photo/$text.txt");
bot('Sendphoto',[
'chat_id'=>$chat_id,
'photo'=>$MoHaMMed,
'caption'=>$message->caption,
'reply_to_message_id'=>$message->message_id,
]);
}
if($message->text and file_exists("data/addrd/media/videonote/$text.txt")) {
  $MoHaMMed = file_get_contents("data/addrd/media/videonote/$text.txt");
 bot('Sendvideonote',[
'chat_id'=>$chat_id,
'video_note'=>$MoHaMMed,
'reply_to_message_id'=>$message->message_id,
]);
}
if($message->text and file_exists("data/addrd/media/document/$text.txt")) {
  $MoHaMMed = file_get_contents("data/addrd/media/document/$text.txt");
 bot('SendDocument',[
'chat_id'=>$chat_id,
'document'=>$MoHaMMed,
'reply_to_message_id'=>$message->message_id,
]);
}
if($message->text and file_exists("data/addrd/media/contact/$text.txt")) {
 $MoHaMMed = file_get_contents("data/addrd/media/contact/$text.txt");
bot('SendContact',[
'chat_id'=>$chat_id,
'phone_number'=>$MoHaMMed,
'first_name'=>$message->from->first_name,
'last_name'=>$message->from->last_name,
'reply_to_message_id'=>$message->message_id,
]);
 }
 if($message->text and file_exists("data/addrd/$chat_id/$text.txt")) {
    $MoHaMMed = file_get_contents("data/addrd/$chat_id/$text.txt");
   bot('SendMessage',[
    'chat_id'=>$chat_id,
    'text'=>$MoHaMMed,
    'parse_mode'=>"MARKDOWN",
    'disable_web_page_preview'=>true,
    'reply_to_message_id'=>$message->message_id,
 ]);
 }
 if($message->text and file_exists("data/addrd/$chat_id/media/$text.txt")) {
  $MoHaMMed = file_get_contents("data/addrd/$chat_id/media/$text.txt");
   bot('Sendvoice',[
    'chat_id'=>$chat_id,
    'voice'=>$MoHaMMed,
    'reply_to_message_id'=>$message->message_id,
 ]);
 }
 if($message->text and file_exists("data/addrd/$chat_id/media/audio/$text.txt")) {
  $MoHaMMed = file_get_contents("data/addrd/$chat_id/media/audio/$text.txt");
 bot('SendAudio',[
    'chat_id'=>$chat_id,
    'audio'=>$MoHaMMed,
    'reply_to_message_id'=>$message->message_id,
 ]);
 }
 if($message->text and file_exists("data/addrd/$chat_id/media/sticker/$text.txt")) {
  $MoHaMMed = file_get_contents("data/addrd/$chat_id/media/sticker/$text.txt");
 bot('sendsticker',[
'chat_id'=>$chat_id,
'sticker'=>$MoHaMMed,
'reply_to_message_id'=>$message->message_id,
]);
}
if($message->text and file_exists("data/addrd/$chat_id/media/video/$text.txt")) {
  $MoHaMMed = file_get_contents("data/addrd/$chat_id/media/video/$text.txt");
bot('Sendvideo',[
'chat_id'=>$chat_id,
'video'=>$MoHaMMed,
'caption'=>$message->caption,
'reply_to_message_id'=>$message->message_id,
]);
}
if($message->text and file_exists("data/addrd/$chat_id/media/photo/$text.txt")) {
  $MoHaMMed = file_get_contents("data/addrd/$chat_id/media/photo/$text.txt");
bot('Sendphoto',[
'chat_id'=>$chat_id,
'photo'=>$MoHaMMed,
'caption'=>$message->caption,
'reply_to_message_id'=>$message->message_id,
]);
}
if($message->text and file_exists("data/addrd/$chat_id/media/videonote/$text.txt")) {
  $MoHaMMed = file_get_contents("data/addrd/$chat_id/media/videonote/$text.txt");
 bot('Sendvideonote',[
'chat_id'=>$chat_id,
'video_note'=>$MoHaMMed,
'reply_to_message_id'=>$message->message_id,
]);
}
if($message->text and file_exists("data/addrd/$chat_id/media/document/$text.txt")) {
  $MoHaMMed = file_get_contents("data/addrd/$chat_id/media/document/$text.txt");
 bot('SendDocument',[
'chat_id'=>$chat_id,
'document'=>$MoHaMMed,
'reply_to_message_id'=>$message->message_id,
]);
}
if($message->text and file_exists("data/addrd/$chat_id/media/contact/$text.txt")) {
 $MoHaMMed = file_get_contents("data/addrd/$chat_id/media/contact/$text.txt");
bot('SendContact',[
'chat_id'=>$chat_id,
'phone_number'=>$MoHaMMed,
'first_name'=>$message->from->first_name,
'last_name'=>$message->from->last_name,
'reply_to_message_id'=>$message->message_id,
]);
 }

if($text == " مـَسّـِآء الـخّـيًــر" || $text == " مَـــسُأُء أَلَــوّورّد " || $text == "مساء الخير" || $text == "مسا الخير"){
if ($tc == 'group' | $tc == 'supergroup'){
if ($settings["lock"]["rdodsg"] == "مقفول️"){
bot('sendsticker',[
'chat_id'=>$chat_id,
'sticker'=>"https://t.me/shehad2/8036",
 'reply_to_message_id'=>$message_id,
]);}}}
$rand = array('مزاج 🚶','في مانع 😒','صنافه','مدري لَيــِْ♡̷̴̬̩̃̊ـِْش😹😔','خلاص دامك ماتعرف اسكت لٱ تسئل 😹🐸');
$ra = array_rand($rand, 1);
if($text ==  "ليش"or $text =="لَيــِْ♡̷̴̬̩̃̊ـِْش "){
if ($tc == 'group' | $tc == 'supergroup'){
if ($settings["lock"]["rdodsg"] == "مقفول️"){
bot('SendMessage',[
'chat_id'=>$chat_id,    
'text'=>$rand[$ra]
]);
}
}
}
$rand = array('انَـَY̷ ̜̩̐̌̋O̷ ̜̩̐̌̋U̷ ̜̩̐̌̋ـَتَ الاجمل👍🌷','كـ جمالك حب 😘','مثلك 😍');
$ra = array_rand($rand, 1);
if($text == 'جميل'){
if ($tc ==  group  | $tc ==  supergroup ){
if ($settings["lock"]["rdodsg"] == "مقفول️"){
bot('SendMessage',[
'chat_id'=>$chat_id,    
'text'=>$rand[$ra]
]);
}
}
}
$rand = array('شو تسويها🙁','يله خلينا نشوف');
$ra = array_rand($rand, 1);
if($text == 'اسويها'){
if ($tc ==  group  | $tc ==  supergroup ){
if ($settings["lock"]["rdodsg"] == "مقفول️"){
bot('SendMessage',[
'chat_id'=>$chat_id,    
'text'=>$rand[$ra],
'parse_mode'=>'MarkDown', 'disable_web_page_preview'=>true,'reply_to_message_id'=>$message->message_id,
]);
}
}
}
if(preg_match('/^(.*)(م̷ـــِْن امس|من امس|امس |قبل يومين )(.*)/',$text) ){
if ($tc ==  group  | $tc ==  supergroup ){
if ($settings["lock"]["rdodsg"] == "مقفول️"){
bot('sendMessage',[
'chat_id'=>$chat_id,
'text'=>"
حاول الان حب لاتيئس ☹",
'parse_mode'=>'MarkDown', 'disable_web_page_preview'=>true, 'reply_to_message_id'=>$message->message_id,
]);
}
}
}
if($text == "ضابح" or $text == "ضايج"){
	if ($tc ==  group  | $tc ==  supergroup ){
if ($settings["lock"]["rdodsg"] == "مقفول️"){
bot('sendMessage',[
'chat_id'=>$chat_id, 
'text'=>"روح انتحر🌚🌷",
'reply_to_message_id'=>$message->message_id, 
]);
}
}
}
if($text == "🚶‍♂"){
	if ($tc ==  group  | $tc ==  supergroup ){
if ($settings["lock"]["rdodsg"] == "مقفول️"){
bot('sendMessage',[
'chat_id'=>$chat_id, 
'text'=>"ع وين😉",
'reply_to_message_id'=>$message->message_id, 
]);
}
}
}
if($text == "😂"){
	if ($tc ==  group  | $tc ==  supergroup ){
if ($settings["lock"]["rdodsg"] == "مقفول️"){
bot('sendMessage',[
'chat_id'=>$chat_id, 
'text'=>"لف اسنانك😚فضحتنا بين الأجانب😢",
'reply_to_message_id'=>$message->message_id, 
]);
}
}
}
if($text == "طمام"){
	if ($tc ==  group  | $tc ==  supergroup ){
if ($settings["lock"]["rdodsg"] == "مقفول️"){
bot('sendMessage',[
'chat_id'=>$chat_id, 
'text'=>"سوي زحاوق😋لرجع وماهي جاهزه😒😂",
'reply_to_message_id'=>$message->message_id, 
]);
}
}
}
if(preg_match('/^(.*)(ملف ردود|بوت ردود|ردود|ملف بوت ردود)(.*)/',$text) ){
	if ($tc ==  group  | $tc ==  supergroup ){
if ($settings["lock"]["rdodsg"] == "مقفول️"){
bot('sendMessage',[
'chat_id'=>$chat_id,
'text'=>"ها حب تريد ملفي 😔رح اعطيك تَعاّإاّإلّ خاص 🚶
بس ارسل الملف", 
'parse_mode'=>'MarkDown', 'disable_web_page_preview'=>true, 'reply_to_message_id'=>$message->message_id,
]);
}
}
}
$rand = array('احسن 😌مو لآزٍمٍ تدري بكل جديد','كلشي انت متعرفه اصلا 😴','م̷ـــِْن مِِـتــ ؟؟! ـى عرفت شي انت بدون ماعلمك 😔😹','عمرك لادريت ☹');
$ra = array_rand($rand, 1);

if($text == 'مدري'){
	if ($tc ==  group  | $tc ==  supergroup ){
if ($settings["lock"]["rdodsg"] == "مقفول️"){
bot('SendMessage',[
'chat_id'=>$chat_id,    
'text'=>$rand[$ra]
]);
}
}
}
if($text == "مالك"){
	if ($tc ==  group  | $tc ==  supergroup ){
if ($settings["lock"]["rdodsg"] == "مقفول️"){
bot('sendMessage',[
'chat_id'=>$chat_id, 
'text'=>"مدري🤷‍♂سئل نفسك",
'reply_to_message_id'=>$message->message_id, 
]);
}
}
}
if($text == "وش"){
	if ($tc ==  group  | $tc ==  supergroup ){
if ($settings["lock"]["rdodsg"] == "مقفول️"){
bot('sendMessage',[
'chat_id'=>$chat_id, 
'text'=>"سوي الدقل. خل نسمع الاخبار📻😂",
'reply_to_message_id'=>$message->message_id, 
]);
}
}
}
if($text == "فهمت"){
	if ($tc ==  group  | $tc ==  supergroup ){
if ($settings["lock"]["rdodsg"] == "مقفول️"){
bot('sendMessage',[
'chat_id'=>$chat_id, 
'text'=>"اكييد😌",
'reply_to_message_id'=>$message->message_id, 
]);
}}}

if($text == "ممكن طلب"){
	if ($tc ==  group  | $tc ==  supergroup ){
if ($settings["lock"]["rdodsg"] == "مقفول️"){
bot('sendMessage',[
'chat_id'=>$chat_id, 
'text'=>"اتفظل بس لاتطلب حسابات🙂",
'reply_to_message_id'=>$message->message_id, 
]);
}}}

if($text == "😏"){
	if ($tc ==  group  | $tc ==  supergroup ){
if ($settings["lock"]["rdodsg"] == "مقفول️"){
bot('sendMessage',[
'chat_id'=>$chat_id, 
'text'=>"وش فْيَگ روح اقرب عياده استلم علاجك😬",
'reply_to_message_id'=>$message->message_id, 
]);
}}}
$rand = array('بويش تفكر شاركنا 🚶','لٱ تروح بعيد خلك معنا 🐸','شو مافهمت 🙄');
$ra = array_rand($rand, 1);

if($text == '🤔'){
	if ($tc ==  group  | $tc ==  supergroup ){
if ($settings["lock"]["rdodsg"] == "مقفول️"){
bot('SendMessage',[
'chat_id'=>$chat_id,    
'text'=>$rand[$ra],
'parse_mode'=>'MarkDown','disable_web_page_preview'=>true, 'reply_to_message_id'=>$message->message_id,
]);
}
}}
$rand = array('معك حب شو تريد🙂','موجود ماتشوفني يعني 😕','مشغولين حب 😔بقي انت ماعندك شغل');
$ra = array_rand($rand, 1);

if($text == 'وينكم'){
	if ($tc ==  group  | $tc ==  supergroup ){
if ($settings["lock"]["rdodsg"] == "مقفول️"){
bot('SendMessage',[
'chat_id'=>$chat_id,    
'text'=>$rand[$ra]
]);
}}}
if($text == "تعال"){
	if ($tc ==  group  | $tc ==  supergroup ){
if ($settings["lock"]["rdodsg"] == "مقفول️"){
bot('sendMessage',[
'chat_id'=>$chat_id, 
'text'=>"اجيك خاص😍",
'reply_to_message_id'=>$message->message_id, 
]);
}}}
if($text == "تعال خاص"){
	if ($tc ==  group  | $tc ==  supergroup ){
if ($settings["lock"]["rdodsg"] == "مقفول️"){
bot('sendMessage',[
'chat_id'=>$chat_id, 
'text'=>"🤭😐😑",
'reply_to_message_id'=>$message->message_id, 
]);
}}}
$rand = array(' دِْۈۈۈۈم/يّارٌب ماتفارقك العافيه 😘ْ','يستاهل الحمد🙌','❤️');
$ra = array_rand($rand, 1);

if($text == 'الحمد لله'){
	if ($tc ==  group  | $tc ==  supergroup ){
if ($settings["lock"]["rdodsg"] == "مقفول️"){
bot('SendMessage',[
'chat_id'=>$chat_id,    
'text'=>$rand[$ra],
'parse_mode'=>'MarkDown','disable_web_page_preview'=>true, 'reply_to_message_id'=>$message->message_id,
]);
}
}}
$rand = array('ع الجميع 🌹','علينا وعليكم 
اكثرو م̷ـــِْن الصلاة ع النبي واله 💐','اغنم حبي ودعي ليـّۓ معاك 🌺');
$ra = array_rand($rand, 1);

if($text == 'جمعه مباركه'){
	if ($tc ==  group  | $tc ==  supergroup ){
if ($settings["lock"]["rdodsg"] == "مقفول️"){
bot('SendMessage',[
'chat_id'=>$chat_id,    
'text'=>$rand[$ra],
'parse_mode'=>'MarkDown','disable_web_page_preview'=>true, 'reply_to_message_id'=>$message->message_id,
]);
}
}}
$rand = array('هاا گـّيَفْ الـّحـّال ٱن شـْاءِ اللـٌہ بَخـّيَرٌ 🙂','وينك مغيب غلا 😉');
$ra = array_rand($rand, 1);

if($text == 'وعليكم السلام'){
	if ($tc ==  group  | $tc ==  supergroup ){
if ($settings["lock"]["rdodsg"] == "مقفول️"){
bot('SendMessage',[
'chat_id'=>$chat_id,    
'text'=>$rand[$ra],
'parse_mode'=>'MarkDown','disable_web_page_preview'=>true, 'reply_to_message_id'=>$message->message_id,
]);
}
}}
$rand = array('🌺⌣{يـّـٌدِْۈۈ/عّزٌگ-ۈنَبْضّ قَلبْگ/ۈۈمْ}⌣ 🍂','تدوم العافيه عليك غلا 🤓');
$ra = array_rand($rand, 1);

if($text == 'دووم'){
	if ($tc ==  group  | $tc ==  supergroup ){
if ($settings["lock"]["rdodsg"] == "مقفول️"){
bot('SendMessage',[
'chat_id'=>$chat_id,    
'text'=>$rand[$ra],
'parse_mode'=>'MarkDown','disable_web_page_preview'=>true, 'reply_to_message_id'=>$message->message_id,
]);
}}}
$rand = array('الْحٍمَدٍ للـّہ🌹
     وانت😘','بخيـــ😃ــر دامـّگ بـْخـّيرٌ يـّٱلـّغـٌالـّے 🌾');
$ra = array_rand($rand, 1);

if($text == 'كيفك'){
	if ($tc ==  group  | $tc ==  supergroup ){
if ($settings["lock"]["rdodsg"] == "مقفول️"){
bot('SendMessage',[
'chat_id'=>$chat_id,    
'text'=>$rand[$ra],
'parse_mode'=>'MarkDown','disable_web_page_preview'=>true, 'reply_to_message_id'=>$message->message_id,
]);
}
}}


if($text=="م1"  ){
if ( $status == 'creator' or $status == 'administrator' or in_array($from_id,$Dev) or in_array($from_id,$useradmin) or in_array($from_id,$getCCmember)){
if ($tc == 'group' | $tc == 'supergroup'){  
$add = $settings["information"]["added"];
if ($add == true) {
  	bot('sendmessage',[
  	'chat_id'=>$chat_id,
  	'text'=>"
⚡️ اوامر حماية المجموعه ⚡️
🗯¦ـ➖➖➖➖
🗯¦ قفل «» فتح •⊱ التعديل  ⊰•
🗯¦️ قفل «» فتح •⊱ البصمات ⊰•
🗯¦ قفل «» فتح •⊱ الــفيديو ⊰•
🗯¦ قفل «» فتح •⊱ الماركدوان ⊰•
🗯¦ قفل «» فتح •⊱ الـصــور ⊰•
🗯¦ قفل «» فتح •⊱ الملصقات ⊰•

🗯¦ قفل «» فتح •⊱ المتحركه ⊰•
🗯¦ قفل «» فتح •⊱ الدردشه ⊰•

🗯¦ قفل «» فتح •⊱ الروابط ⊰•
🗯¦ قفل «» فتح •⊱ التاك ⊰•
🗯¦ قفل «» فتح •⊱ البوتات ⊰•
🗯¦ ️قفل «» فتح •⊱ المعرفات ⊰•
🗯¦ قفل «» فتح •⊱ البوتات بالطرد ⊰•
🗯¦ قفل «» فتح •⊱ الكلايش ⊰•
🗯¦️ قفل «» فتح •⊱ التكرار ⊰•
🗯¦ قفل «» فتح •⊱ التوجيه ⊰•
🗯¦ قفل «» فتح •⊱ العربية ⊰•
🗯¦ قفل «» فتح •⊱ الاجنبية ⊰•
🗯¦ قفل «» فتح •⊱ الرد ⊰•
🗯¦ قفل «» فتح •⊱ المواقع ⊰•
🗯¦ قفل «» فتح •⊱ العربية ⊰•
🗯¦ قفل «» فتح •⊱ الاشعارات ⊰•
🗯¦ قفل «» فتح •⊱ الجهات ⊰•
🗯¦ قفل «» فتح •⊱ الانلاين ⊰•
🗯¦ قفل «» فتح •⊱ الموسيقى ⊰•
🗯¦ قفل «» فتح •⊱ بصمة الفيديو ⊰•
🗯¦ قفل «» فتح •⊱ الــكـــل ⊰•
🔅¦ـ➖➖➖➖➖
📲¦ قفل «» فتح •⊱ التوجيه بالتقييد ⊰•
🔗¦ قفل «» فتح •⊱ الروابط بالتقييد ⊰•
📀¦ قفل «» فتح •⊱ المتحركه بالتقييد ⊰•
📸¦ قفل «» فتح •⊱ الصور بالتقييد ⊰•
📽¦ قفل «» فتح •⊱ الفيديو بالتقييد ⊰•
🔅¦ـ➖➖➖➖➖
📌¦ تفعيل «» تعطيل •⊱  الترحيب ⊰•

🗯¦ تفعيل «» تعطيل •⊱  الاعضاء ⊰
🗯¦ تفعيل «» تعطيل •⊱  الردود ⊰•
🗯¦ تفعيل «» تعطيل •⊱  التحقق ⊰
📢¦ تفعيل «» تعطيل •⊱  الاشتراك الاحباري ⊰•
🗨¦ تفعيل «» تعطيل •⊱  الايدي ⊰•
🔅¦ـ➖➖➖➖➖

👨🏻‍💻¦ للاستفسار 💡↭ $alwsh
",
'reply_to_message_id'=>$message_id,
  	]);
  	}

  }
}
}
if($text=="م2"  ){
if ( $status == 'creator' or $status == 'administrator' or in_array($from_id,$Dev) or in_array($from_id,$useradmin) or in_array($from_id,$getCCmember)){
if ($tc == 'group' | $tc == 'supergroup'){  
$add = $settings["information"]["added"];
if ($add == true) {
  	bot('sendmessage',[
  	'chat_id'=>$chat_id,
  	'text'=>"
•⊱ {  آوآمر الرفع والتنزيل  } ⊰•

🗯¦ رفع بصلاحيه ‿ بالرد 
⚗¦ رفع مدير ‿ تنزيل مدير
📿¦ رفع ادمن ‿ تنزيل ادمن 
💈¦ رفع مميز ‿ تنزيل مميز 

⦅ ꯭آو꯭آم꯭ـر آ꯭لم꯭ـس꯭ـح꯭ للم꯭ـنش꯭ـى꯭ ⦆

🗑¦ مسح الادمنيه •⊱ لمسح الادمنيه 
🗑¦ مسح المميزين •⊱ لمسح الاعضاء المميزين 
🗑¦ مسح المدراء •⊱ لمسح المدراء 
🗑¦ تنزيل الكل ⊰• للتنزيل

⦅آوآمـر آلحظـر وآلطــرد وآلتقييـد  ⦆
      
🔱¦ حظر (بالرد) •⊱ لحظر العضو  
🌀¦ تقييد (بالرد) •⊱ لتقييد العضو
🚸¦ الغاء الحظر (بالرد) •⊱ لالغاء الحظر 
〰¦  
 التقييد (بالرد) •⊱ لالغاء تقييد العضو 
 🚫¦ فلترة + الكلمه •⊱ لمنع كلمه داخل المجموعه
⭕️¦ الغاء فلترة •⊱ لالغاء منع الكلمه بالمجموعه
⭕️¦ قائمة الفلتر •⊱ لعرض الكلمات الممنوعة
🗑¦ مسح الفلاتر •⊱ لمسح الفلاتر الممنوعة
🔅¦ـ➖➖➖➖➖

👨🏻‍💻¦ للاستفسار 💡↭ $alwsh
",
'reply_to_message_id'=>$message_id,
  	]);
  	}

  }
}
}
if($text=="م3"  ){
if ( $status == 'creator' or $status == 'administrator' or in_array($from_id,$Dev) or in_array($from_id,$useradmin) or in_array($from_id,$getCCmember)){
if ($tc == 'group' | $tc == 'supergroup'){  
$add = $settings["information"]["added"];
if ($add == true) {
  	bot('sendmessage',[
  	'chat_id'=>$chat_id,
  	'text'=>"
👨🏽‍✈️¦  اوامر الوضع للمجموعه ::

📮¦ـ➖➖➖➖➖
💭¦ وضع ترحيب + الترحيب ↜ لوضع ترحيب  
💭¦ وضع تكرار + العدد ↜ لوضع تكرار
💭¦ وضع تحذيز + العدد ↜ لوضع تحذيرات
💭¦ وضع اعضاء + العدد ↜ لتحديد العدد الاضافة  
💭¦ وضع قوانين + القوانين :↜ لوضع القوانين 
💭¦ الـرابـط :↜  لعرض الرابط  
💭¦ تحذيراتي ↜ لعرض تحذيراتك
📮¦ـ➖➖➖➖➖

👨🏽‍💻¦  اوامر رؤية الاعدادات ::

🗯¦ القوانين : لعرض  القوانين 
🗯¦ الادمنية : لعرض  الادمنيه 
🗯¦ المدراء : لعرض  الاداريين 
🗯¦ المقيدين :↜لعرض  المقيدين 
🗯¦ المطور : لعرض معلومات المطور 
🗯¦ ايدي :↜لعرض معلوماتك  
🗯¦ الاعدادات : لعرض اعدادات المجموعه 
🗯¦ اضف رد  : لاضافة الرد
🗯¦ مسح رد  : لحذف الرد
🗯¦ الردود  : للعرض الردود
🗯¦ مسح الردود  : للمسح الردود
➖➖➖➖➖➖➖
🗯¦ راسلني للاستفسار 💡↭ $alwsh
",
'reply_to_message_id'=>$message_id,
  	]);
  	}

  }
}
}
if($text=="م4"  ){
if ( $status == 'creator' or $status == 'administrator' or in_array($from_id,$Dev) or in_array($from_id,$useradmin) or in_array($from_id,$getCCmember)){
if ($tc == 'group' | $tc == 'supergroup'){  
$add = $settings["information"]["added"];
if ($add == true) {
  	bot('sendmessage',[
  	'chat_id'=>$chat_id,
  	'text'=>"
👨🏽‍✈️¦  اوامر التسلية والتحشيش ::

📮¦ـ➖➖➖➖➖
🗯¦ رفع ⊰• بالرد ⊰• ئيس⊰•
🗯¦ رفع ⊰• بالرد ⊰• مـلك ⊰•
🗯¦ رفع ⊰• بالرد ⊰• مرتي ⊰•
🗯¦ رفع ⊰• بالرد ⊰• هبيلة ⊰•
🗯¦ رفع ⊰• بالرد ⊰• مقوت ⊰•
🗯¦ رفع ⊰• بالرد ⊰• سائق ⊰•
🗯¦ رفع ⊰• بالرد ⊰• زاحف ⊰•
📮¦ـ➖➖➖➖➖
👨🏽‍✈️¦  اوامر التحدث للبوت ::

🗯¦ كله بالرد + الكلمة لنطقها ⊰•
🗯¦ كول + الكلمة لعرضها ⊰•
🗯¦ بوسه - بوسها  بالرد ⊰•
🗯¦ قول + اسف للتاسف ⊰•
📮¦ـ➖➖➖➖➖

🗯¦ الساعة ⊰• لعرض الوقت
🗯¦ سورس ⊰• لمعلومات السورس
🗯¦ كشف بالرد ⊰• لمعلوماته
🗯¦ معلوماتي ⊰• لمعلوماتك
🗯¦ جهاتي ⊰• لاضافاتك
🗯¦ رتبتي ⊰• لموقعك

 🔅¦ـ➖➖➖➖➖
👨🏻‍💻¦ للاستفسار 💡↭ $alwsh
",
'reply_to_message_id'=>$message_id,
  	]);
  	}

  }
}
}

$bad_words = [
    // القذف والألفاظ القوية
    "كس امك", "كس اختك", "ابن الكحبه", "ابن تنيج", "ابن النعال", "ابن القندره", 
    "ابن المنيوك", "ابن الساقطه", "ابن الحيوانه", "منيوك", "تنيج", "نيج", "تنايج", 
    "ديوث", "فرخ", "كواد", "كس", "كحبه", "قحبه", "ساقطه", "بنت الملاهي", 

    // سب الأهل واللعن
    "انعل ابوك", "انعل امك", "انعل والديك", "انعل شرفك", "انعل عرضك", "انعل عشيرتك", 
    "انعل سلفاك", "خرب امك", "خرب ابوك", "خرب دينك", "خرب ربك", "خرب عرضك", 
    "خرب شرفك", "خرب غيرتك", "خرب كس", "خرب ابو", 

    // كلمات خادشة وأعضاء
    "العير", "عير بيك", "عير بطيزك", "طيز", "طيزك", "كسج", "كسك", "مص", "مصه", 
    "سحاق", "لوطي", "لواط", "منحرف", "اباحي", "افلام", "سكس", "صور تعبانه", 

    // تجاوزات وسب عام (عراقي)
    "مبين من طيزك", "يا زمال", "مطيرجي", "سربوت", "سرابيت", "خنيث", "مخنث", 
    "فاسق", "داشر", "عربيد", "سافل", "ناقص", "يا نكس", "نجس", "خايس", "تفو", 
    "زباله", "بغل", "حيوان", "حقير", "ساقط", "كلب", "ابن الكلب"
];


// التحقق من وجود الكلمة في الرسالة
foreach($bad_words as $bad) {
    if(strpos($text, $bad) !== false) {
        // حذف الرسالة فوراً
        bot('deleteMessage', [
            'chat_id' => $chat_id,
            'message_id' => $message_id
        ]);
        
        // (اختياري) إرسال تنذير للمستخدم
        /*
        bot('sendMessage', [
            'chat_id' => $chat_id,
            'text' => "⚠️ يمنع التجاوز في القروب، تم حذف رسالتك.",
        ]);
        */
        exit; // توقف عن فحص باقي الكلمات بمجرد الحذف
    }
}

if($text == "ا" or $text == "ايدي" or $text == "ايديك"){

    // مصفوفة الـ 15 عبارة احترافية ومختلفة
    $words = [
        "احبـڪ ياوجـھَہّ القـمـر 😊🥀",
        "هـيـبـة وحـضـورك يـلـغـي الـڪـل 🦁✨",
        "يـا بـعـد روحـي ونـبـض قـلـبـي ❤️",
        "الـصـقـر مـا يـهـوى غـيـر الـقـمـم 🦅💎",
        "تـرافـة وذوق وكـلـك حـلاه ✨🌸",
        "يـا ضـحـڪـة تـرد الـعـافـيـة 🌙🔱",
        "سـلـطـان عـلـى عـرش الـأنـاقـة 👑",
        "مـنـور الـدنـيـا بـهـذا الـوجـه الـسـمـح ✨",
        "ڪـلـك هـيـبـة وطـبـعـك ذهـب 💎",
        "الـحـلـو حـلـو بـأخـلاقـه يـا ورد 🌹",
        "يـا هـلـه بـطـلـتـك الـتـسـوى ذهـب 🦁",
        "شـمـس الـڪـروب ونـوره الـوضـاء ☀️",
        "الـثـقـل مـيـزانـك والـأدب عـنـوانـك ✨",
        "يـا وجـه الـخـيـر عـلـيـنـا 🍀",
        "ضـحـڪـتـك تـسـوى الـڪـون ومـا فـيـه ❤️"
    ];
    $rand_word = $words[array_rand($words)];

    // جلب بيانات المستخدم
    $name = $message->from->first_name;
    $user_id = $message->from->id;
    $user_user = ($message->from->username) ? "@".$message->from->username : "لا يوجد";
    
    // هنا تضع متغيرات البوت الخاصة بك (الرتبة، التفاعل، إلخ)
    $rank = "عضو ملكي ✨"; // مثال
    $msgs = "1250"; // مثال
    $points = "500"; // مثال
    $bio = "لا يوجد بايو"; // مثال

    $reply = "↫ $rand_word\n";
    $reply .= "━━━━━━━━━━━━━━\n";
    $reply .= "⌁︙ايديـڪ ↫ `$user_id`\n";
    $reply .= "⌁︙معرفـڪ ↫ `$user_user`\n";
    $reply .= "⌁︙حسابـڪ ↫ [اضـغـط هـنـا](tg://user?id=$user_id)\n";
    $reply .= "⌁︙رتبتـڪ ↫ $rank\n";
    $reply .= "⌁︙تفاعلـڪ ↫ مـتـفـاعـل 🔥\n";
    $reply .= "⌁︙رسائلـڪ ↫ $msgs\n";
    $reply .= "⌁︙سحكاتـڪ ↫ 0\n";
    $reply .= "⌁︙نقاطـڪ ↫ $points\n";
    $reply .= "⌁︙البـايـــو ↫ $bio\n";
    $reply .= "━━━━━━━━━━━━━━\n";
    $reply .= "❖￤بـواسطـة لـيـون الـمـطـور 🦁💎";

    bot('sendMessage',[
        'chat_id'=>$chat_id,
        'text'=>$reply,
        'reply_to_message_id'=>$message_id,
        'parse_mode'=>"Markdown",
        'reply_markup'=>json_encode([
            'inline_keyboard'=>[
                [['text'=>"👤 : $name", 'url'=>"tg://user?id=$user_id"]]
            ]
        ])
    ]);
}



if($text=="الاوامر"  ){
if ( $status == 'creator' or $status == 'administrator' or in_array($from_id,$Dev) or in_array($from_id,$useradmin) or in_array($from_id,$getCCmember)){
if ($tc == 'group' | $tc == 'supergroup'){  
$add = $settings["information"]["added"];
if ($add == true) {
  	bot('sendmessage',[
  	'chat_id'=>$chat_id,
  	'text'=>"
❂

 ‌‌‏❋¦ مـسـآرت آلآوآمـر آلعآمـهہ‌‏ ⇊

👨‍⚖️¦ م1 » آوآمـر آلحمـآيهہ‌‏
📟¦ م2 » آوآمـر آعدآدآت آلمـجمـوعهہ‌‏
🛡¦ م3 » آوآمـر آلآدآرهہ‌‏
🙈¦ م4 » آوآمـر آلتحشيش
🕹¦ م المطور »  آوآمـر آلمـطـور
⚡️¦ اوامر الرد » لآضـآفهہ‌‏ رد مـعين
⚙¦ الاعدادات » لآدآرهہ‌‏ حماية آلبوت

 ‌‌‏❋¦ رآسـلني للآسـتفسـآر ☜ {  $alwsh } ✓
",
'reply_to_message_id'=>$message_id,
  	]);
  	}

  }
}
}

$admin = 7897598134 ;
if($text =="م المطور" &&$from_id==$admin ){
bot ('sendMessage',[
'chat_id'=>$chat_id,
'text'=>"*📌¦ اوامر المطــہور 

👷🏽¦ عزيزي المطور ، ارسل الاوامر او /start ،
👷🏽¦ في خاص البوت لعرض اوامرك ،!

👷🏽¦ تحديث: لتحديث ملفات البوت
👷🏽¦ رفع او تنزيل : مطور { بالرد }
👷🏽¦ المطورين او /d : لعرض المطورين ، 
👷🏽¦ الادمنيه : لعرض مشرفين الكروب ،!
👷🏽¦ تعين الايدي - مسح الايدي ،
👷🏽¦  شرط التفعيل + العدد: للتفعيل

👷🏽¦  بوت غادر : للخروج من المجموعة
👷🏽¦ الاحصائيات : لعرض احصائيات البوت ،
👷🏽¦ مسح المطورين او /n : لمسح المطورين ،! 
👷🏽¦ شرط التفعيل + العدد : لتفعيل المجموعة؛
👷🏽¦ـ➖➖➖➖➖
👨🏻‍💻¦ للاستفسار 💡↭  $alwsh*
",
'parse_mode'=>'MarkDown', 'disable_web_page_preview'=>true, 'reply_to_message_id'=>$message->message_id,
]);
}

  if($text=="م المطور" and  $you == "member" and $id !== $sudo){
     bot('sendMessage',[
        'chat_id'=>$chat_id,
        'text'=>"🔅¦ للمطور الاساسي فقط  🎖",
  'reply_to_message_id'=>$mid,
  'parse_mode'=>'MARKDOWN',
'disable_web_page_preview'=>true,
      ]);
   }

//*******************//
$update     = json_decode(file_get_contents('php://input'));
$message = $update->message;
$message_id = $update->message->message_id;
$text           = $message->text;
$chat_id     = $message->chat->id;
$user          = $update->message->from->username;
$sudo         = $sudo; // ايديك .
$buyy  = "@Mi2k_12"; // حط معرفك
$re         = $update->message->reply_to_message;
$re_id      = $update->message->reply_to_message->from->id;
$re_user    = $update->message->reply_to_message->from->username;
$re_msgid   = $update->message->reply_to_message->message_id;
$type       = $update->message->chat->type;
$from_id     = $message->from->id;
$from_user = $message->from->username;
$id   = $message->from->id; 
$_user = $message->from->username; 
$user = "[$_user]";
$name = $message->from->first_name; 
$get             = file_get_contents("https://api.telegram.org/bot$API_KEY/getChatMember?chat_id=$chat_id&user_id=".$from_id);
$info            = json_decode($get, true);
$JJ117        = $info['result']['status'];
if($message){
$msgs = json_decode(file_get_contents('msgs.json'),true);
$update = json_decode(file_get_contents('php://input'));
$msgs['msgs'][$chat_id][$from_id] = ($msgs['msgs'][$chat_id][$from_id]+1);}
 if($text == "موقعي" || $text =="معلوماتي" and $from_id == $sudo){
bot('sendmessage',[
'chat_id'=>$chat_id, 
'text'=>"*👨🏽‍🔧¦ اهـلا بـك عزيزي في معلوماتك 🥀 
ـ.——————————
🗯¦ الاســم •⊱{ $name }⊰•
💠¦ المعرف •⊱* @$user *⊰•
⚜️¦ الايـدي •⊱ {* `$from_id` *} ⊰•
🚸¦ رتبتــك •⊱ مطور اساسي 👨🏻‍✈️  ⊰•
🔰¦ ــ •⊱ {* `$chat_id` *} ⊰•
ـ.——————————
 •⊱ { الاحـصـائـيـات الـرسـائـل } ⊰•
💬¦ رسائلك ~ {* ".$msgs['msgs'][$chat_id][$from_id]." *}

ـ.——————————
👨🏻‍💻¦ مـطـور البوت •⊱* $buyy *⊰•*",
"parse_mode"=>"MARKDOWN",
'reply_to_message_id'=>$message->message_id, 
]);
}
if($text == "موقعي" || $text =="معلوماتي" and in_array($from_id,$dev)){
bot('sendmessage',[
'chat_id'=>$chat_id, 
'text'=>"*👨🏽‍🔧¦ اهـلا بـك عزيزي في معلوماتك 🥀 
ـ.——————————
🗯¦ الاســم •⊱{ $name }⊰•
💠¦ المعرف •⊱* @$user *⊰•
⚜️¦ الايـدي •⊱ {* `$from_id` *} ⊰•
🚸¦ رتبتــك •⊱ مطور البوت 👨🏻‍  ⊰•
🔰¦ ــ •⊱ {* `$chat_id` *} ⊰•
ـ.——————————
 •⊱ { الاحـصـائـيـات الـرسـائـل } ⊰•
💬¦ رسائلك ~ {* ".$msgs['msgs'][$chat_id][$from_id]." *}

ـ.——————————
👨🏻‍💻¦ مـطـور البوت •⊱* $buyy *⊰•*",
"parse_mode"=>"MARKDOWN",
'reply_to_message_id'=>$message->message_id, 
]);
}
if($from_id != $sudo and !in_array($from_id,$dev)){
if($text=="موقعي" || $text =="معلوماتي" and $JJ117 == "creator"){
bot('sendmessage',[
'chat_id'=>$chat_id, 
'text'=>"*👨🏽‍🔧¦ اهـلا بـك عزيزي في معلوماتك 🥀 
ـ.——————————
🗯¦ الاســم •⊱{ $name }⊰•
💠¦ المعرف •⊱* @$user *⊰•
⚜️¦ الايـدي •⊱ {* `$from_id` *} ⊰•
🚸¦ رتبتــك •⊱ المنشئ 🏌🏾‍♂ ⊰•
🔰¦ ــ •⊱ {* `$chat_id` *} ⊰•
ـ.——————————
 •⊱ { الاحـصـائـيـات الـرسـائـل } ⊰•
💬¦ رسائلك ~ {* ".$msgs['msgs'][$chat_id][$from_id]." *}

ـ.——————————
👨🏻‍💻¦ مـطـور البوت •⊱* $buyy *⊰•*",
"parse_mode"=>"MARKDOWN",
'reply_to_message_id'=>$message->message_id, 
]);
}
if($text == "موقعي" || $text =="معلوماتي" and  $JJ117 == "administrator"){
bot('sendmessage',[
'chat_id'=>$chat_id, 
'text'=>"*👨🏽‍🔧¦ اهـلا بـك عزيزي في معلوماتك 🥀 
ـ.——————————
🗯¦ الاســم •⊱{ $name }⊰•
💠¦ المعرف •⊱* @$user *⊰•
⚜️¦ الايـدي •⊱ {* `$from_id` *} ⊰•
🚸¦ رتبتــك •⊱ ادمن البوت 🤺 ⊰•
🔰¦ ــ •⊱ {* `$chat_id` *} ⊰•
ـ.——————————
 •⊱ { الاحـصـائـيـات الـرسـائـل } ⊰•
💬¦ رسائلك ~ {* ".$msgs['msgs'][$chat_id][$from_id]." *}

ـ.——————————
👨🏻‍💻¦ مـطـور البوت •⊱* $buyy *⊰•*",
"parse_mode"=>"MARKDOWN",
'reply_to_message_id'=>$message->message_id, 
]);
}
if($text == "موقعي" || $text =="معلوماتي" and  $JJ117 == "member"){
bot('sendmessage',[
'chat_id'=>$chat_id, 
'text'=>"*👨🏽‍🔧¦ اهـلا بـك عزيزي في معلوماتك 🥀 
ـ.——————————
🗯¦ الاســم •⊱{ $name }⊰•
💠¦ المعرف •⊱* @$user *⊰•
⚜️¦ الايـدي •⊱ {* `$from_id` *} ⊰•
🚸¦ رتبتــك •⊱ عضو فقط 👶🏻 ⊰•
🔰¦ ــ •⊱ {* `$chat_id` *} ⊰•
ـ.——————————
 •⊱ { الاحـصـائـيـات الـرسـائـل } ⊰•
💬¦ رسائلك ~ {* ".$msgs['msgs'][$chat_id][$from_id]." *}

ـ.——————————
👨🏻‍💻¦ مـطـور البوت •⊱* $buyy *⊰•*",
"parse_mode"=>"MARKDOWN",
'reply_to_message_id'=>$message->message_id, 
]);
}
}
//=======================//
if($re and $text == "رفع ملك" or $text == "رفع ملكي"){
bot('SendMessage',['chat_id'=>$chat_id,
'text'=>"
📬┊العضو » [$usew]
👤┊ايديه » {$re_id}
🎖┊تم رفعه ملك 👑 للمجموعه
⚜┊يرجى من الجميع تقديره ☄ واحترامه 🥀
➖
",'parse_mode'=>'markdown','reply_to_message_id'=>$message->message_id,'disable_web_page_preview'=>true,
]);
}
if($re and $text == "رفع رئيس" or $text == "رفع رأيس"){
bot('SendMessage',['chat_id'=>$chat_id,
'text'=>"
📬┊العضو » [$usew]
👤┊ايديه » {$re_id}
🎖┊تم رفعه رئيس 👨‍💼للمجموعه
⚜┊انتبهو يضاربو هو والملك 😕😂 ماشفرعش 🌚
➖
",'parse_mode'=>'markdown','reply_to_message_id'=>$message->message_id,'disable_web_page_preview'=>true,
]);
}
if($re and $text == "رفع زاحف" or $text == "رفع زحفي"){
bot('SendMessage',['chat_id'=>$chat_id,
'text'=>"
📬┊العضو » [$usew]
👤┊ايديه » {$re_id}
🎖┊تم رفعه زاحـ🐍ـف في المجموعه
⚜┊اصبح زاحف هنا 🌚
➖
",'parse_mode'=>'markdown','reply_to_message_id'=>$message->message_id,'disable_web_page_preview'=>true,
]);
}
if($re and $text == "رفع مرتي" or $text == "رفع زوجتي"){
bot('SendMessage',['chat_id'=>$chat_id,
'text'=>"
📬┊العضو » [$usew]
👤┊ايديه » {$re_id}
🎖┊تم رفعه زوجة لهاذا الشخص @$username 🌚 بدون خطوبة 😹
➖
",'parse_mode'=>'markdown','reply_to_message_id'=>$message->message_id,'disable_web_page_preview'=>true,
]);
}
if($re and $text == "رفع اهبل" or $text == "رفع اخبل"){
bot('SendMessage',['chat_id'=>$chat_id,
'text'=>"
📬┊العضو » [$usew]
👤┊ايديه » {$re_id}
🎖┊تم رفعه هبيلة لهاذه المجموعه 😞😂 
➖
",'parse_mode'=>'markdown','reply_to_message_id'=>$message->message_id,'disable_web_page_preview'=>true,
]);
}
if($re and $text == "رفع حمار" or $text == "رفع حمير"){
bot('SendMessage',['chat_id'=>$chat_id,
'text'=>"
📬┊العضو » [$usew]
👤┊ايديه » {$re_id}
🎖┊تم رفعه حمار لهاذه المجموعه 🌚😂
➖
",'parse_mode'=>'markdown','reply_to_message_id'=>$message->message_id,'disable_web_page_preview'=>true,
]);
}
if($re and $text == "رفع مقوت" or $text == "رفع مقوتي"){
bot('SendMessage',['chat_id'=>$chat_id,
'text'=>"
📬┊العضو » [$usew]
👤┊ايديه » {$re_id}
🎖┊تم رفعه مقوت في سوق عنس
⚜┊ للقات العال 🌚
➖
",'parse_mode'=>'markdown','reply_to_message_id'=>$message->message_id,'disable_web_page_preview'=>true,
]);
}
if($re and $text == "رفع سائق" or $text == "ترقية سائق"){
bot('SendMessage',['chat_id'=>$chat_id,
'text'=>"
📬┊العضو » [$usew]
👤┊ايديه » {$re_id}
🎖┊تم ترقيته لسائق تكسي
⚜┊يحمل تهريب 🌚
➖
",'parse_mode'=>'markdown','reply_to_message_id'=>$message->message_id,'disable_web_page_preview'=>true,
]);
}
//******************//
$update     = json_decode(file_get_contents('php://input'));
$message = $update->message;
$message_id = $update->message->message_id;
$text           = $message->text;
$chat_id     = $message->chat->id;
$user          = $update->message->from->username;
 
$from_id     = $message->from->id;
$from_user = $message->from->username;
mkdir("LONELY");
$link1      = $ex[6];
$update = json_decode(file_get_contents('php://input'));
var_dump($update);
$message    = $update->message;
$message_id = $update->message->message_id;
$re_msgid   = $update->message->reply_to_message->message_id;
$name= $update->message->from->first_name;
$user= $update->message->from->username;
$get             = file_get_contents("https://api.telegram.org/bot$API_KEY/getChatMember?chat_id=$chat_id&user_id=".$from_id);
$info            = json_decode($get, true);
$JJ117        = $info['result']['status'];
$get_kick     = file_get_contents("LONELY/kick.txt");
$kick            = explode("\n",$get_kick);
if($text == "تفعيل اطردني" and $JJ117 !="member"){
 file_put_contents("LONELY/kick.txt",$chat_id);
 bot("Sendmessage",[
 'chat_id'=>$chat_id,
 'text'=>"*✡⁞ تم تفعيل امَر اطردني . *",
 'parse_mode'=>"MARKDOWN",
    'reply_to_message_id'=>$message->message_id,
 ]);
 }
 if($text == "تعطيل اطردني" and $JJ117 !="member"){
 file_put_contents("LONELY/kick.txt", " ");
 bot("Sendmessage",[
 'chat_id'=>$chat_id,
 'text'=>"*✡⁞ تم تعطيل امَر اطردني . *",
 'parse_mode'=>"MARKDOWN",
    'reply_to_message_id'=>$message->message_id,
 ]);
 }

if($text =="اطردني" and  $JJ117 == "member" and $from_id != $sudo and in_array($chat_id,$kick)){
 $export = json_decode(file_get_contents("https://api.telegram.org/bot$API_KEY/exportChatInviteLink?chat_id=$chat_id"));
    $l = $export->result;
    bot('KickChatMember',[
        'chat_id'=>$chat_id,
        'user_id'=>$from_id,
        ]);
        bot('UnbanChatmember',[
            'chat_id'=>$chat_id,
            'user_id'=>$from_id,
            ]);
    bot('sendmessage',[
        'chat_id'=>$chat_id,
        'text'=>"*لقد تم طردك بنجاح بأمر منك , ارسلت لك رابط المجموعه في الخاص اذا وصلت لك تستطيع الرجوع متى شئت ،🖤🖤*",
        'parse_mode'=>"MARKDOWN",
        'reply_to_message_id'=>$message->message_id,
]);
bot('sendmessage',[
    'chat_id'=>$from_id,
    'text'=>"
*🌟| اهلا عزيزي , لقد تم طردك من المجموعه بامر منك ،
🔖| اذا كان هذا بالخطأ او اردت الرجوع للمجموعه : *
*-*$l *.🖤*",
'parse_mode'=>"MARKDOWN",
]);
}

if($JJ117 == "creator" or $JJ117 == "administrator" or $from_id == $sudo)
if($text == "اطردني"){
    bot('sendmessage',[
        'chat_id'=>$chat_id,
        'text'=>"*✡⁞ لا استطيع طرد المشرفين ، المنشئين ، المطورين . *",
        'parse_mode'=>"MARKDOWN",
        'reply_to_message_id'=>$message->message_id,
]);
}
if($text =="اطردني" and  $JJ117 == "member" and $from_id != $sudo and !in_array($chat_id,$kick)){
 bot('sendmessage',[
        'chat_id'=>$chat_id,
        'text'=>"*✡⁞ امر اطردني معطَل . *",
        'parse_mode'=>"MARKDOWN",
        'reply_to_message_id'=>$message->message_id,
        ]);
        }

$update     = json_decode(file_get_contents('php://input'));
$message = $update->message;
$message_id = $update->message->message_id;
$text           = $message->text;
$chat_id     = $message->chat->id;
$user          = $update->message->from->username;
$buyy          = "@Mi2k_12"; // معرفك
$sudo         = 7897598134; // ايديك.
$bot_id       =8519056610; // ايدي بوتك .
$from_id     = $message->from->id;
$re         = $update->message->reply_to_message;
$re_id      = $update->message->reply_to_message->from->id;
$re_user      = $update->message->reply_to_message->from->username;
$first_name = $message->from->first_name;
$type       = $update->message->chat->type;

$get             = file_get_contents("https://api.telegram.org/bot$API_KEY/getChatMember?chat_id=$chat_id&user_id=".$from_id);
$info            = json_decode($get, true);
$JJ117        = $info['result']['status'];
$s = file_get_contents("https://api.telegram.org/bot$API_KEY/getChatMember?chat_id=$chat_id&user_id=".$bot_id);
$ss = json_decode($s, true);
$bot = $ss['result']['status'];

mkdir("banduser");
$get_Busers = file_get_contents("banduser/$chat_id.txt");
$get_Buser = explode("\n",$get_Busers);

$kick = explode(" " ,$text);
if( $type == "supergroup" and $bot == "administrator"){
if($JJ117 == "creator" || $JJ117 == "administrator" || $from_id == $sudo || in_array($from_id,$dev) || in_array($from_id,$manger)) {
if($kick[0] == "طرد" || $kick[0] == "حظر" and isset($kick[1])){
$text = str_replace(['حظر ','طرد '],'',$text);
$stat = file_get_contents("https://api.telegram.org/bot$API_KEY/getChatMember?chat_id=$text&user_id=".$text);
$statjson = json_decode($stat, true);
$name = $statjson['result']['user']['first_name'];
$username = $statjson['result']['user']['username'];
$id = $statjson['result']['user']['id'];

if($text != $sudo && $text != $buyy && !in_array($text,$dev) and !in_array($text,$manger) and !in_array($text,$getCCmember) and !in_array($text,$dev_) and !in_array($text,$manges) and !in_array($text,$getCmember)){
if(strpos($text ,"@") !== false and !in_array($text,$get_Buser)){
file_put_contents("banduser/$chat_id.txt","\n" . $text ."\n" , FILE_APPEND);}
if($stat !== false and !in_array("@$username",$get_Buser)){
file_put_contents("banduser/$chat_id.txt","\n" . "@$username" ."\n" , FILE_APPEND);}

bot('KickChatMember',[
'chat_id'=>$chat_id,
'user_id'=>$id
  ]);
bot('sendmessage', [
 'chat_id' => $chat_id,
 'text'=>"
💬┇العضو ~⪼ *$text*
☑┇تم حظره بنجاح
",
'parse_mode'=>"MARKDOWN",
'reply_to_message_id'=>$message_id,
'disable_web_page_preview'=>true,
   ]);
}
}
}
}

if(in_array("@$user",$get_Buser)){
bot('KickChatMember',[
'chat_id'=>$chat_id,
'user_id'=>$from_id,
]);
}

if( $type == "supergroup" and $bot == "administrator"){
if($JJ117 == "creator" || $JJ117 == "administrator" || $from_id == $sudo || in_array($from_id,$dev) || in_array($from_id,$manger)) {
if($kick[0] == "الغاء" and $kick[1] == "حظر" and isset($kick[2])){
$text = str_replace('الغاء حظر ','',$text);

$stat = file_get_contents("https://api.telegram.org/bot$API_KEY/getChatMember?chat_id=$text&user_id=".$text);
$statjson = json_decode($stat, true);
$name = $statjson['result']['user']['first_name'];
$username = $statjson['result']['user']['username'];
$id = $statjson['result']['user']['id'];

if($stat != false and in_array("@$username",$get_Buser)){
$str2 = str_replace("@$username",'',$get_Busers);
$ex2 = explode("\n",$str2);
file_put_contents("banduser/$chat_id.txt",$ex2);}

if(strpos($text ,"@") !== false and in_array($text,$get_Buser)){
$str = str_replace("$text",'',$get_Busers);
$ex = explode("\n",$str);
file_put_contents("banduser/$chat_id.txt",$ex);}

bot('promoteChatMember',[
        'chat_id'=>$chat_id,
        'user_id'=>$id,
        'can_send_messages'=>true,
  ]);
bot('sendmessage', [
 'chat_id' => $chat_id,
 'text'=>"
💬┇العضو ~⪼ *$text*
☑┇تم الغاء حظره بنجاح
",
'parse_mode'=>"MARKDOWN",
'reply_to_message_id'=>$message_id,
'disable_web_page_preview'=>true,
   ]);
}
if($text == "مسح المحظورين"){
file_put_contents("banduser/$chat_id.txt","");
bot("SendMessage",[
'chat_id'=>$chat_id,
'text'=>"🌤¦ تم مسحّ قائمه المحظورين ،🦄'",
'parse_mode'=>"MARKDOWN",
'reply_to_message_id'=>$message_id,
'disable_web_page_preview'=>true,
]);
}
}
}
if($text == "المحظورين" and $get_Busers != NULL || $get_Busers != ""){
bot("SendMessage",[
'chat_id'=>$chat_id,
'text'=>"☑️¦ قائمه الاعضاء المحظورين :
[$get_Busers]",
'parse_mode'=>"MARKDOWN",
'reply_to_message_id'=>$message_id,
'disable_web_page_preview'=>true,
]);
}
if($text == "المحظورين" and $get_Busers == NULL || $get_Busers == ""){
bot("SendMessage",[
'chat_id'=>$chat_id,
'text'=>"🔰¦ لٱيوجد محظورين ،💘💘''",
'parse_mode'=>"MARKDOWN",
'reply_to_message_id'=>$message_id,
'disable_web_page_preview'=>true,
]);
}


if($type == "supergroup" and $bot == "administrator"){
if($JJ117 != "creator" && $JJ117 != "administrator" && $from_id != $sudo && !in_array($from_id,$dev) and !in_array($from_id,$manger)){
if($kick[0] == "طرد" || $kick[0] == "حظر" and isset($kick[1])){
bot("SendMessage",[
'chat_id'=>$chat_id,
'text'=>"🍟¦ ليس لديك صلاحيٱت ، حظر او الغاء حظر .",
'parse_mode'=>'MARKDOWN',
    'reply_to_message_id'=>$message->message_id,
  ]);
}
if($kick[0] == "الغاء" and $kick[1] == "حظر" and isset($kick[2])){
	bot("SendMessage",[
'chat_id'=>$chat_id,
'text'=>"🍟¦ ليس لديك صلاحيٱت ، حظر او الغاء حظر .",
'parse_mode'=>'MARKDOWN',
    'reply_to_message_id'=>$message->message_id,
  ]);
}
}
}
if($text == "الساعة" or $text == "الزمن" or $text == "الساعه" or $text == "الوقت"){
bot ('sendMessage',[
'chat_id'=>$chat_id,
'text'=>"📆¦ الوقت •⊱ $date $aa ⊰•
",
'parse_mode'=>'MarkDown', 'disable_web_page_preview'=>true, 'reply_to_message_id'=>$message->message_id,
]);
}
//******************//
if($text == "سورس" || $text == "ياسورس" || $text == "السورس"){
		bot("sendmessage",[
	'chat_id'=>$chat_id,
	'text'=>"

┇ تنصـيب سـورس آلنيزگ  🔎

 ⇓⇓⇓ 

`https://t.me/joinchat/AAAAAFM_zC829C8zwh7AXw`
`https://t.me/THTSS`

» فقط أضغط على الرابط للنسخ 
» ثم الصقه بالخاص تبعك ثم ادخل 
» بعدهہ‌‏آ ابحث عن ملف. التنصيب .
» تدخل مـعلومـآتگ مـن توگن ومـعرفگ وايديگ
» وسـوف يعمـل آلبوت بعد الرفع تلقآئيآ ...
 
*💭┇ قناة السورس ☜ @THTSS*
",
    'disable_web_page_preview'=>true,
    'parse_mode'=>"MARKDOWN",
    'reply_to_message_id'=>$message->message_id, 
	 ]);
	 }
//********************//
 
$admin = 7897598134 ;
if($text =="تحديث" &&$from_id==$admin ){
bot ('sendMessage',[
'chat_id'=>$chat_id,
'text'=>"🎖
🗂¦ تم تحديث الملفات
√
",
'parse_mode'=>'MarkDown', 'disable_web_page_preview'=>true, 'reply_to_message_id'=>$message->message_id,
]);
}
//*****************//
 
$reply = $update->message->reply_to_message;
$re_id      = $update->message->reply_to_message->from->id;
$API_KEY = API_KEY;
$get = file_get_contents("https://api.telegram.org/bot$API_KEY/getChatMember?chat_id=$chat_id&user_id=".$re_id);
$info = json_decode($get, true);
$re_rou = $info['result']['status'];
$namesaeedh = $update->message->reply_to_message->from->first_name;
$usersaeedh = $update->message->reply_to_message->from->username;
$idsaeedh = $update->message->reply_to_message->from->id;

if($reply and $text == "كشف"){
if($re_id == $sudo)
bot('sendmessage',['chat_id'=>$chat_id,'text'=>"*🤵🏼¦ الاسم » { $namesaeedh }
🎫¦ الايدي » { $idsaeedh  }
🎟¦ المعرف »{ @$usersaeedh }
📮¦ الرتبه » مطور اساسي 👨🏻‍⚕
🕵🏻️‍♀️¦ نوع الكشف » بالرد
➖*",
 'parse_mode'=>'MarkDown', 'disable_web_page_preview'=>true, 'reply_to_message_id'=>$message->message_id,
]);
}
if($reply and $text == "كشف"){
if(in_array($re_id,$dev))
bot('sendmessage',['chat_id'=>$chat_id,'text'=>"*🤵🏼¦ الاسم » { $namesaeedh }
🎫¦ الايدي » { $idsaeedh  }
🎟¦ المعرف »{ @$usersaeedh }
📮¦ الرتبه » مطور البوت 👨🏻‍⚕
🕵🏻️‍♀️¦ نوع الكشف » بالرد
➖*",
 'parse_mode'=>'MarkDown', 'disable_web_page_preview'=>true, 'reply_to_message_id'=>$message->message_id,
]);
}
if($reply and $text == "كشف"){
if(in_array($re_id,$manger) and !in_array($re_id,$dev))
bot('sendmessage',['chat_id'=>$chat_id,'text'=>"*🤵🏼¦ الاسم » { $namesaeedh }
🎫¦ الايدي » { $idsaeedh  }
🎟¦ المعرف »{ @$usersaeedh }
📮¦ الرتبه » مدير البوت 👨🏿‍✈️
🕵🏻️‍♀️¦ نوع الكشف » بالرد
➖*",
 'parse_mode'=>'MarkDown', 'disable_web_page_preview'=>true, 'reply_to_message_id'=>$message->message_id,
]);
}
if($reply and $text ==  "كشف"){
if($re_rou == "creator" and $re_id != $sudo and !in_array($re_id,$dev) and !in_array($re_id,$manger) and !in_array($re_id,$getCCmember))
bot('sendmessage',['chat_id'=>$chat_id,'text'=>"*🤵🏼¦ الاسم » { $namesaeedh }
🎫¦ الايدي » { $idsaeedh } 
🎟¦ المعرف »{ @$usersaeedh }
📮¦ الرتبه » المنشىء 👷
🕵🏻️‍♀️¦ نوع الكشف » بالرد
➖*",
 'parse_mode'=>'MarkDown', 'disable_web_page_preview'=>true, 'reply_to_message_id'=>$message->message_id,
]);
}
if($reply and $text ==  "كشف"){
if($re_rou == "administrator" and $re_id != $sudo and !in_array($re_id,$dev) and !in_array($re_id,$manger))
bot('sendmessage',['chat_id'=>$chat_id,'text'=>"*🤵🏼¦ الاسم » { $namesaeedh }
🎫¦ الايدي » { $idsaeedh } 
🎟¦ المعرف »{ @$usersaeedh }
📮¦ الرتبه » ادمن في البوت 👨🏼‍🎓
🕵🏻️‍♀️¦ نوع الكشف » بالرد
➖*",
 'parse_mode'=>'MarkDown', 'disable_web_page_preview'=>true, 'reply_to_message_id'=>$message->message_id,
]);
}
if($reply and $text ==  "كشف"){
if(in_array($re_id,$getCCmember) and !in_array($re_id,$manger) and !in_array($re_id,$dev) and $re_rou != "administrator")
bot('sendmessage',['chat_id'=>$chat_id,'text'=>"*🤵🏼¦ الاسم » { $namesaeedh }
🎫¦ الايدي » { $idsaeedh  }
🎟¦ المعرف »{ @$usersaeedh }
📮¦ الرتبه » عضو مميز 🍨
🕵🏻️‍♀️¦ نوع الكشف » بالرد
➖*",
 'parse_mode'=>'MarkDown', 'disable_web_page_preview'=>true, 'reply_to_message_id'=>$message->message_id,
]);
}
if($reply and $text ==  "كشف"){
if($re_rou == "member" and $re_id != $sudo and !in_array($re_id,$dev) and !in_array($re_id,$manger) and !in_array($re_id,$getCCmember))
bot('sendmessage',['chat_id'=>$chat_id,'text'=>"*🤵🏼¦ الاسم » { $namesaeedh }
🎫¦ الايدي » { $idsaeedh  }
🎟¦ المعرف »{ @$usersaeedh }
📮¦ الرتبه » فقط عضو 🙍🏼‍♂️
🕵🏻‍♂¦ نوع الكشف » بالرد
➖*",
 'parse_mode'=>'MarkDown', 'disable_web_page_preview'=>true, 'reply_to_message_id'=>$message->message_id,
]);
}
//********************//
$as = $message->reply_to_message; 
$asf = $as->message_id;  
if($as and $text =="كله اسف" or $text == "قله اسف"){
bot('sendMessage',[
'chat_id'=>$chat_id,
'text'=>"اسف💚🌺",
'reply_to_message_id'=>$asf,
]);
}
//********************//
$as = $message->reply_to_message; 
$asf = $as->message_id;  
$rand = array('😘😘😘','😍 ابوس النخرة 🤣','😶 لامش ضروري','ميحتاج بوس 😑');
$r = array_rand($rand,true);
if($as and $text =="بوسه"){
bot('sendMessage',[
'chat_id'=>$chat_id,
'text'=>"$rand[$r]",
'reply_to_message_id'=>$asf,
]);
}
$rand = array('ياخي عيب 💔🚫','للام ولا للاب 🌚☄','انا ... امك','انا اعرف امك 🌚','اين كمك 🌝');
$r = array_rand($rand,true);
if($as and $text =="سبله"){
bot('sendMessage',[
'chat_id'=>$chat_id,
'text'=>"$rand[$r]",
'reply_to_message_id'=>$asf,
]);
}
$as = $message->reply_to_message; 
$asf = $as->message_id;  
$rand1 = array('😘😘😘','😤 لاعيب 😓','مالك جننت 🤧','طيب بعدين 🤐');
$r1 = array_rand($rand1,true);
if($as and $text =="بوسها"){
bot('sendMessage',[
'chat_id'=>$chat_id,
'text'=>"$rand1[$r1]",
'reply_to_message_id'=>$asf,
]);
}
//********************
//************************//

$me = $message->reply_to_message; 
$mem = $me->message_id;
$MEMO = explode('كله',$text);
if($MEMO){
bot('sendMessage',[
'chat_id'=>$chat_id,
'text'=>$MEMO[1],
'reply_to_message_id'=>$mem,
]);
}
$MEMO = explode('كول',$text);
if($MEMO){
bot('sendMessage',[
'chat_id'=>$chat_id,
'text'=>$MEMO[1],
]);
}
$u = explode("\n",file_get_contents("memb.txt"));
$m = count($u)-1;
$modxe = file_get_contents("usr.txt");
//******************//

if($text == "رابط حذف" or $text == "رابط الحذف" or $text == "اريد احذف الحساب" or $text == "ححذف"){
bot('sendMessage',[
'chat_id'=>$chat_id, 
'text'=>"🌿¦ رابط حذف حـساب التيليگرام ↯
📛¦ لتتندم فڪر قبل ڪلشي  
👨🏽‍⚖️¦ بالتـوفيـق عزيزي ...
🚸 ¦ـ  https://telegram.org/deactivate
",
'reply_to_message_id'=>$message->message_id, 
]);
}
//*************************
if($text == "ايديي" or $text == "أيديي"){
	bot('SendMessage',[
    'chat_id'=>$chat_id,
    'text'=>"
*🎟┊ايديك هو »  *`$from_id`* •*

🖲┊اضغط للنسخ الان
",
'parse_mode'=>"MARKDOWN",
'reply_to_message_id'=>$message->message_id,
]);
}
//************************//
 
if(in_array($from_id,$Dev)){
$info = "المطور الاساسي 👨🏻‍✈️";
}elseif($status == "creator"){
$info = "منشىء المجموعة 🕵";
}elseif($status == "administrator"){
$info = "مشرف المجموعة 👮";
}elseif(in_array($from_id,$admin_user) ){
$info = "ادمن في البوت 👨🏼‍🎓";
}elseif(in_array($from_id,$manger) ){
$info = "مدير البوت 👨🏼‍⚕️";
}elseif(in_array($from_id,$mmyaz) ){
$info = "عضو مميز ⭐️";
}elseif($status == "member" ){
$info = "فقط عضو 🙍🏼‍♂️";
}
if($msgs['msgs'][$chat_id][$from_id] > 3000){
$active = array("خوش متفاعل 🌝","متفاعل ✨","اسطورة التفاعل 🌈ء","الله مال تفاعل ⚜","نايس التفاعل ??ء",'قوي جدا ⚡️ ',  'قمه التفاعل ✨ ',  'اقوى تفاعل 🔥 ',);
$JJ119 = array_rand($active,1);
}elseif($msgs['msgs'][$chat_id][$from_id] > 500){
$active = array('متوسط 🎋 ',  'متفاعل 💐',);
$JJ119 = array_rand($active,1);
}elseif($msgs['msgs'][$chat_id][$from_id] == 1){
$active = array('تفاعل زفت 🙄','ضعيف جدا 🐢',);
$JJ119 = array_rand($active,1);
}
elseif($msgs['msgs'][$chat_id][$from_id] > 1){
$active = array('تفاعل زفت ','ضعيف جدا ',);
$JJ119 = array_rand($active,1);
}
if($msgs['msgs'][$chat_id][$from_id] > 3000){
$Free3 = array("1000% 😻","999% 😺","100% 🙂",);
$Free4 = array_rand($Free3,1);
}elseif($msgs['msgs'][$chat_id][$from_id] > 500){
$Free3 = array('80% ','84% ',);
$Free4 = array_rand($Free3,1);
}elseif($msgs['msgs'][$chat_id][$from_id] == 1){
$Free3 = array('18%','20% ','6% ',);
}
elseif($msgs['msgs'][$chat_id][$from_id] > 1){
$Free3 = array('18% ','20% ','6% ',);
$Free4 = array_rand($Free3,1);
}if($msgs['msgs'][$chat_id][$from_id] > 200){
$Free3 = array("40% ","43% ",);
$Free4 = array_rand($Free3,1);
}
elseif($game['game'][$chat_id][$from_id] >= 1){
$gamepoi = "".$game['game'][$chat_id][$from_id]."";
}
elseif($game['game'][$chat_id][$from_id] == 0){
$gamepoi = "0";
}
elseif($game['game'][$chat_id][$from_id] <= 1){
$gamepoi = "".$game['game'][$chat_id][$from_id]."";
}

if($text=="رتبتي" ){
bot('sendmessage',[
'chat_id'=>$chat_id, 
'text'=>"
*🎟┊ايديك » *`$from_id`*
🎟┊رتبتك » $info 
🎟┊تفاعلك »  $active[$JJ119] 
🎟┊نسبة تفاعلك »  $Free3[$Free4] 
▂*
",
'parse_mode'=>"MARKDOWN",
'reply_to_message_id'=>$message->message_id,
]);
}
//************************//
if ( $status == 'creator' or $status == 'administrator' or in_array($from_id,$Dev) or in_array($from_id,$manger) or in_array($from_id,$admin_user) or in_array($from_id,$developer)) {
if($text =="تعطيل الكابتشا" or $text == "تعطيل الكابتش" or $text == "تعطيل التحقق"){
	bot('sendmessage',[
	'chat_id'=>$chat_id,
	'text'=>"
🙋🏼‍♂┇اهلا بك عزيزي { $info }
📬┇تم تعطيل الكابتشا عند الدخول
🛠
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,
  'reply_to_message_id'=>$message_id,
 ]);
file_put_contents("data/$chat_id/ser.txt","معطل");
}
}
if($text =="تفعيل الكابتشا" or $text == "تفعيل التحقق"){
if ( $status == 'creator' or $status == 'administrator' or in_array($from_id,$Dev) or in_array($from_id,$manger) or in_array($from_id,$admin_user) or in_array($from_id,$developer)) {
	bot('sendmessage',[
	'chat_id'=>$chat_id,
	'text'=>"
🙋🏼‍♂┇اهلا بك عزيزي { $info }
📬┇تم تفعيل الكابتشا عند الدخول
🛠
",'parse_mode'=>"markdown",'disable_web_page_preview'=>true,
  'reply_to_message_id'=>$message_id,
 ]);
file_put_contents("data/$chat_id/ser.txt","مفعل");
}
}
//**************************//
$asa = json_decode(file_get_contents('added.json'),true);
$get_myid = file_get_contents("data/ids/idset.txt");
$_get_ = file_get_contents("data/ids/id.txt");
$get_ALONE = file_get_contents("data/ids/id_.txt");
$GETGG1ZZ = file_get_contents("data/ids/iBadlz.txt");
$_GG1ZZ_ = explode("\n",$GETGG1ZZ);
$newiddd = $update->message->new_chat_member->id;
if($update->message->new_chat_member and $from_id != $newiddd){
$asa['sss'][$chat_id][$from_id] = ($asa['sss'][$chat_id][$from_id]+1);
file_put_contents('added.json', json_encode($asa));}
if($text == "جهاتيي" or $text == "جهاتي" and $asa['sss'][$chat_id][$from_id] == 0){bot('sendmessage',['chat_id'=>$chat_id,'text'=>"
* 🎟┊عدد جهاتك المضافة »  {0} ➺*",

'parse_mode'=>"MARKDOWN",'reply_to_message_id'=>$message->message_id,]);}
if($text == "جهاتيي" or $text == "جهاتي" and $asa['sss'][$chat_id][$from_id] > 0){bot('sendmessage',['chat_id'=>$chat_id,'text'=>"
*🎟┊عدد جهاتك المضافة »  {".$asa['sss'][$chat_id][$from_id]."} ➺*",
'parse_mode'=>"MARKDOWN",'reply_to_message_id'=>$message->message_id,]);}
//*******************************//
 

$update     = json_decode(file_get_contents('php://input'));
$message = $update->message;
$message_id = $update->message->message_id;
$text           = $message->text;
$chat_id     = $message->chat->id;
$user          = $update->message->from->username;
$sudo         = 7897598134; // ايديك.
$bot_id       = 8519056610; // ايدي بوتك .
$from_id     = $message->from->id;
$first_name = $message->from->first_name;
$type       = $update->message->chat->type;

mkdir("Fri3nd_s");

$message_id = $message->message_id;
$gp_get = file_get_contents("Fri3nd_s/groups.txt");
$groups = explode("\n", $gp_get);
$GG1ZZ = file_get_contents("Fri3nd_s/iBadlz.txt");
$pirvate = explode("\n",file_get_contents("Fri3nd_s/pirvate.txt"));
$forward = $update->message->forward_from;
$MOhaMMed = count($pirvate)-1;
$MoHaMMedd = count($groups)-1;

if($text == "اذاعه بالتوجيه" || $text == "اذاعه عام بالتوجيه" || $text == "اذاعه للكل بالتوجيه" || $text =="🖇¦ اذاعه عام توجيه" and $from_id == $sudo){
    file_put_contents("Fri3nd_s/iBadlz.txt","iBadlz");
    bot('sendmessage',[
    'chat_id'=>$chat_id,
    'text'=>"*📮• اهلا عزيزي الـمطور ، قم بتوجيه رسالةه*",
    'parse_mode'=>"MARKDOWN",
    'reply_to_message_id'=>$message->message_id
  ]);
  }
if($message and $GG1ZZ == "iBadlz" and $from_id == $sudo ){
  for($i=0;$i<count($groups);$i++){
bot('ForwardMessage',[
 'chat_id'=>$groups[$i],
 'from_chat_id'=>$chat_id,
 'message_id'=>$message_id,
 ]);
} 
for($i=0;$i<count($pirvate);$i++){
bot('forwardMessage',[
 'chat_id'=>$pirvate[$i],
 'from_chat_id'=>$chat_id,
 'message_id'=>$message->message_id,
 ]);
 unlink("Fri3nd_s/iBadlz.txt");
} 
bot('sendMessage',[
          'chat_id'=>$chat_id,
          'text'=>"*📮• اهلا عزيزي الـمطور ، 
 ⚜• تم ارسال رسالتك الى $MOhaMMed عضو و $MoHaMMedd من مجموعات البوت ،💗ء*",
'parse_mode'=>"MARKDOWN",
'reply_to_message_id'=>$message->message_id
   ]);
} 

if($text and $type == "private" and !in_array($from_id, $pirvate)){
file_put_contents("Fri3nd_s/pirvate.txt", "$from_id\n",FILE_APPEND);
}
if($text and $type == "supergroup" and !in_array($chat_id, $groups)) {
file_put_contents("Fri3nd_s/groups.txt", "$chat_id\n",FILE_APPEND);
}

if($text == "اذاعه خاص" || $text =="⌛️¦ اذاعه خاص" and $from_id == $sudo){
    file_put_contents("Fri3nd_s/iBadlz.txt","JJ119");
    bot('sendmessage',[
    'chat_id'=>$chat_id,
    'text'=>"*📮• اهلا عزيزي الـمطور ، قم بأرسال رسالتك
📥• ملاحظةهہ : يمكنك استعمال الماركداون ،! *",
'parse_mode'=>"MarkDown",
    'reply_to_message_id'=>$message->message_id
  ]);
  }
if($message and $GG1ZZ == "JJ119" and $from_id == $sudo ){
    for ($i=0; $i<count($pirvate); $i++) { 
        bot('sendMessage',[
          'chat_id'=>$pirvate[$i],
          'text'=>"$text",
'parse_mode'=>"MarkDown",
'disable_web_page_preview'=>true,
]);
 file_put_contents("Fri3nd_s/iBadlz.txt","MMoHaMMeD");
} 
$MOhaMMed = count($pirvate)-1;
bot('sendMessage',[
          'chat_id'=>$chat_id,
          'text'=>"*📮• اهلا عزيزي الـمطور ، 
 ⚜• تم ارسال رسالتك الى $MOhaMMed عضو ،💗ء*",
    'parse_mode'=>"MARKDOWN",
    'reply_to_message_id'=>$message->message_id
          ]);
}
if ($text == "اذاعه للكل" || $text == "اذاعه عام" || $text == "اذاعه"  ||$text == "📆⎮ اذاعه •" || $text =="📤¦ اذاعه عام" and $from_id == $sudo){
    file_put_contents("Fri3nd_s/iBadlz.txt","LE_C4_KR");
    bot('sendmessage',[
    'chat_id'=>$chat_id,
    'text'=>"*📮• اهلا عزيزي الـمطور ، قم بأرسال رسالتك
📥• ملاحظةهہ : يمكنك استعمال الماركداون ،! *",
'parse_mode'=>"MARKDOWN",
    'reply_to_message_id'=>$message->message_id
  ]);
  }
if($message and $GG1ZZ == "LE_C4_KR" and $from_id == $sudo ){
    for ($i=0; $i<count($groups); $i++) { 
        bot('sendMessage',[
          'chat_id'=>$groups[$i],
          'text'=>"$text",
'parse_mode'=>"MarkDown",
'disable_web_page_preview'=>true,

]);
} 
for ($i=0; $i<count($pirvate); $i++) { 
        bot('sendMessage',[
          'chat_id'=>$pirvate[$i],
          'text'=>"$text",
'parse_mode'=>"MarkDown",
'disable_web_page_preview'=>true,
]);
 unlink("Fri3nd_s/iBadlz.txt");
} 
bot('sendMessage',[
          'chat_id'=>$chat_id,
          'text'=>"*📮• اهلا عزيزي الـمطور ، 
 ⚜• تم ارسال رسالتك الى $MOhaMMed عضو و $MoHaMMedd من مجموعات البوت ،💗ء*",
 'parse_mode'=>"MarkDown",
          'reply_to_message_id'=>$message->message_id
          ]);
}

if($text == "اذاعه خاص بالتوجيه" || $text == "⚫️¦ اذاعه خاص توجيه" and $from_id == $sudo){
    file_put_contents("Fri3nd_s/iBadlz.txt","od_1j");
    bot('sendmessage',[
    'chat_id'=>$chat_id,
    'text'=>"*📮• اهلا عزيزي الـمطور ، قم بتوجيه رسالةه*",
    'parse_mode'=>"MARKDOWN",
    'reply_to_message_id'=>$message->message_id
  ]);
  }
if($message and $GG1ZZ == "od_1j" and $from_id == $sudo ){
for($i=0;$i<count($pirvate);$i++){
bot('forwardMessage',[
 'chat_id'=>$pirvate[$i],
 'from_chat_id'=>$chat_id,
 'message_id'=>$message->message_id,
 ]);
 unlink("Fri3nd_s/iBadlz.txt");
} 
$MOhaMMed = count($pirvate)-1;
bot('sendMessage',[
          'chat_id'=>$chat_id,
          'text'=>"*📮• اهلا عزيزي الـمطور ، 
⚜• تم توجيه رسالتك الى $MOhaMMed عضو ،💗ء*",
'parse_mode'=>"MARKDOWN",
          'reply_to_message_id'=>$message->message_id
   ]);
}

if($from_id == $sudo){
if($text == "الاحصائيات" || $text == "/co"){
bot("SendMessage",[
'chat_id'=>$chat_id,
'text'=>"الاحصائيات : 🔰 

▪️¦ عدد المجموعات المفعله : $MoHaMMedd 
📮¦ عدد المشتركين في البوت : $MOhaMMed",
'parse_mode'=>"MARKDOWN",
          'reply_to_message_id'=>$message->message_id
]);
}
}
