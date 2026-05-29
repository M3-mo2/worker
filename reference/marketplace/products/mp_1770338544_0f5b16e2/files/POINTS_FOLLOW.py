import asyncio
import re
from telethon import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.errors import FloodWaitError, ChannelsTooMuchError, ChatWriteForbiddenError
import os
from colorama import init, Fore, Back, Style
import time
from datetime import datetime

init(autoreset=True)

# DEV : @M3_mo2  &   @M1telegramM1 


# معلوماتك
#_________________________________________________#
api_id = 
api_hash = 'yor api'
phone = '+' 
#_________________________________________________#

bot_username = '@a3kbot'
start_command = '/start'
collect_button_text = '❇️'
join_channels_text = '📣'
confirm_subscription_button_text = '✅'
continue_collecting_text = 'استمرار'

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    clear_screen()
    banner = f"""
{Fore.CYAN}╔═══════════════════════════════════════════════════════════════════════╗
║ {Fore.RED}███████╗ ██████╗ ██╗     ██╗      ██████╗ ██╗   ██╗     ██╗{Fore.CYAN}        ║
║ {Fore.RED}██╔════╝██╔═══██╗██║     ██║     ██╔═══██╗██║   ██║   ██╔╝{Fore.CYAN}        ║
║ {Fore.RED}█████╗  ██║   ██║██║     ██║     ██║   ██║██║   ██║  ██╔╝{Fore.CYAN}         ║
║ {Fore.RED}██╔══╝  ██║   ██║██║     ██║     ██║   ██║██║   ██║ ██╔╝{Fore.CYAN}          ║
║ {Fore.RED}██║     ╚██████╔╝███████╗███████╗╚██████╔╝╚██████╔╝██╔╝{Fore.CYAN}           ║
║ {Fore.RED}╚═╝      ╚═════╝ ╚══════╝╚══════╝ ╚═════╝  ╚═════╝ ╚═╝{Fore.CYAN}            ║
║                                                                   ║
║ {Fore.MAGENTA}██████╗  ██████╗ ██╗███╗   ██╗████████╗███████╗{Fore.CYAN}                 ║
║ {Fore.MAGENTA}██╔══██╗██╔═══██╗██║████╗  ██║╚══██╔══╝██╔════╝{Fore.CYAN}                 ║
║ {Fore.MAGENTA}██████╔╝██║   ██║██║██╔██╗ ██║   ██║   ███████╗{Fore.CYAN}                 ║
║ {Fore.MAGENTA}██╔═══╝ ██║   ██║██║██║╚██╗██║   ██║   ╚════██║{Fore.CYAN}                 ║
║ {Fore.MAGENTA}██║     ╚██████╔╝██║██║ ╚████║   ██║   ███████║{Fore.CYAN}                 ║
║ {Fore.MAGENTA}╚═╝      ╚═════╝ ╚═╝╚═╝  ╚═══╝   ╚═╝   ╚══════╝{Fore.CYAN}                 ║
╚═══════════════════════════════════════════════════════════════════════╝
    """
    print(banner)
    print(f"{Fore.CYAN}╔═══════════════════════════════════════════════════════════════════════╗")
    print(f"║ {Fore.GREEN}✨ 𝚄𝙻𝚃𝚁𝙰 𝚂𝙿𝙴𝙴𝙳 𝙿𝙾𝙸𝙽𝚃𝚂 𝙲𝙾𝙻𝙻𝙴𝙲𝚃𝙾𝚁 ✨{Fore.CYAN}                                ║")
    print(f"║ {Fore.YELLOW}⌚ 𝚃𝙸𝙼𝙴: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Fore.CYAN}                                    ║")
    print(f"║ {Fore.RED}💎 𝙳𝙴𝚅𝙴𝙻𝙾𝙿𝙴𝙳 𝙱𝚈: @M3_mo2 💎{Fore.CYAN}                                        ║")
    print(f"╚═══════════════════════════════════════════════════════════════════════╝\n")

def print_status(message, status="info"):
    colors = {
        "success": Fore.GREEN + "✓ ",
        "error": Fore.RED + "✖ ",
        "info": Fore.CYAN + "❯ ",
        "warning": Fore.YELLOW + "⚡ "
    }
    color = colors.get(status, Fore.WHITE)
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"{Fore.BLUE}[{timestamp}] {color}{message}{Style.RESET_ALL}")

def print_progress_bar(progress, total, prefix='🔄 PROGRESS:', suffix='COMPLETE', length=50):
    filled_length = int(length * progress // total)
    bar = '█' * filled_length + '░' * (length - filled_length)
    percentage = progress / total * 100
    print(f'\r{Fore.CYAN}{prefix} |{Fore.GREEN}{bar}{Fore.CYAN}| {percentage:.1f}% {suffix}', end='')
    if progress == total:
        print()

async def find_and_click_button(button_text, retries=3, delay=0.2):
    for attempt in range(retries):
        try:
            async for message in client.iter_messages(bot_username, limit=3):
                if message.buttons:
                    for row in message.buttons:
                        for button in row:
                            if isinstance(button_text, (list, tuple)):
                                if any(text in button.text for text in button_text):
                                    await button.click()
                                    print_status(f"💫 CLICKED: {button.text}", "success")
                                    await asyncio.sleep(delay)
                                    return True
                            elif button_text in button.text:
                                await button.click()
                                print_status(f"💫 CLICKED: {button.text}", "success")
                                await asyncio.sleep(delay)
                                return True
            await asyncio.sleep(delay)
        except Exception as e:
            print_status(f"ATTEMPT {attempt + 1}: {str(e)}", "error")
            await asyncio.sleep(delay)
    return False

async def extract_channel_info(retries=3, delay=0.2):
    channel_pattern = r'@(\w+)'
    points_pattern = r'(\d+)\s*نقطة'
    
    for attempt in range(retries):
        try:
            async for message in client.iter_messages(bot_username, limit=3):
                if not message.message:
                    continue
                    
                if 'اشترگ في القناة' in message.message or 'اشترك في القناة' in message.message:
                    channel_match = re.search(channel_pattern, message.message)
                    points_match = re.search(points_pattern, message.message)
                    
                    if channel_match:
                        channel = channel_match.group(1)
                        points = points_match.group(1) if points_match else "0"
                        print(f"\n{Fore.CYAN}{'═'*65}")
                        print_status(f"🌟 NEW CHANNEL DETECTED:", "info")
                        print_status(f"📢 CHANNEL: @{channel}", "info")
                        print_status(f"💎 POINTS: {points}", "info")
                        print(f"{Fore.CYAN}{'═'*65}\n")
                        return f"@{channel}", points
                        
            await asyncio.sleep(delay)
        except Exception as e:
            print_status(f"ATTEMPT {attempt + 1}: {str(e)}", "error")
            await asyncio.sleep(delay)
    return None, None

async def verify_and_continue(channel_username, retries=3, delay=0.2):
    for attempt in range(retries):
        try:
            if await find_and_click_button(confirm_subscription_button_text):
                print_status(f"✅ SUBSCRIPTION VERIFIED: {channel_username}", "success")
                await asyncio.sleep(0.2)
                
                if await find_and_click_button(['استمرار في تجميع 📣', 'استمرار']):
                    print_status("🔄 PROCEEDING TO NEXT CHANNEL", "success")
                    return True
                    
            await asyncio.sleep(delay)
        except Exception as e:
            print_status(f"VERIFICATION ATTEMPT {attempt + 1}: {str(e)}", "error")
            await asyncio.sleep(delay)
    return False

async def join_channels_and_verify():
    while True:
        try:
            print_banner()
            await client.start(phone)
            print_status("🚀 تم تشغيل النظام بنجاح", "success")
            
            while True:
                await client.send_message(bot_username, start_command)
                print_status("📤 جاري بدء التجميع", "success")
                await asyncio.sleep(0.3)

                if not await find_and_click_button(collect_button_text):
                    print_status("⚡ جاري المحاولة مرة أخرى", "warning")
                    continue

                await asyncio.sleep(0.2)
                
                if not await find_and_click_button(join_channels_text):
                    print_status("⚡ جاري إعادة المحاولة", "warning")
                    continue

                await asyncio.sleep(0.2)
                successful_joins = 0
                total_points = 0
                target_channels = 100
                start_time = time.time()

                while True:
                    channel_info = await extract_channel_info()
                    channel_username, points = channel_info if channel_info else (None, None)
                    
                    if not channel_username:
                        print_status("⚡ جاري البحث عن قنوات جديدة", "warning")
                        await asyncio.sleep(2)
                        break

                    try:
                        await client(JoinChannelRequest(channel_username))
                        print_status(f"✅ تم الانضمام: {channel_username}", "success")
                        await asyncio.sleep(0.3)
                        
                        if await verify_and_continue(channel_username):
                            successful_joins += 1
                            points = int(points) if points and points.isdigit() else 7
                            total_points += points
                            
                            elapsed_time = time.time() - start_time
                            speed = successful_joins / elapsed_time if elapsed_time > 0 else 0
                            
                            print_progress_bar(successful_joins, target_channels)
                            print_status(f"📊 الإحصائيات: {successful_joins} قناة | {total_points} نقطة | {speed:.2f} قناة/ثانية", "success")
                        else:
                            print_status(f"⚡ جاري التحقق: {channel_username}", "warning")
                        
                        await asyncio.sleep(0.3)
                        
                    except FloodWaitError as e:
                        wait_time = e.seconds
                        print_status(f"⏳ يرجى الانتظار: {wait_time} ثانية", "warning")
                        for remaining in range(wait_time, 0, -1):
                            print(f"\r{Fore.YELLOW}⏳ متبقي: {remaining} ثانية...{Style.RESET_ALL}", end='')
                            await asyncio.sleep(1)
                        print()
                    except ChannelsTooMuchError:
                        print_status("⚡ تم الوصول للحد الأقصى من القنوات", "warning")
                        await asyncio.sleep(10)
                        break
                    except ChatWriteForbiddenError:
                        print_status(f"⚡ لا يمكن الكتابة في {channel_username}", "warning")
                        continue
                    except Exception as e:
                        print_status(f"⚡ جاري المحاولة: {str(e)}", "warning")
                        await asyncio.sleep(0.3)
                        continue

                if successful_joins > 0:
                    elapsed_time = time.time() - start_time
                    print(f"\n{Fore.CYAN}{'═'*65}")
                    print_status("📊 إحصائيات التجميع:", "info")
                    print_status(f"📈 عدد القنوات: {successful_joins}", "success")
                    print_status(f"💎 مجموع النقاط: {total_points}", "success")
                    print_status(f"⚡ متوسط السرعة: {successful_joins / elapsed_time:.2f} قناة/ثانية", "success")
                    print_status(f"⏱️ الوقت المستغرق: {elapsed_time:.1f} ثانية", "success")
                    print(f"{Fore.CYAN}{'═'*65}\n")
                
                print_status("⚡ جاري البحث عن قنوات جديدة", "warning")
                await asyncio.sleep(3)

        except Exception as e:
            print_status(f"⚡ جاري إعادة المحاولة: {str(e)}", "warning")
            await asyncio.sleep(3)

client = TelegramClient('session_name', api_id, api_hash)

if __name__ == "__main__":
    asyncio.run(join_channels_and_verify())