#غير حقوق واثبت انك فاشل
import telebot
import requests
import sys
import os
import re
import time
import marshal
import zlib
import base64
import lzma
import bz2
import binascii
import uuid
import ast
import builtins
from types import CodeType
from zipfile import ZipFile
from subprocess import Popen, PIPE
import threading

TOKEN = 'توكنك'
ADMIN_ID = ايديك
bot = telebot.TeleBot(TOKEN)

class Deobfuscator:
    def __init__(self, filename):
        self.filename = filename
        self.content = open(filename, 'rb').read()
        self.layers_removed = 0
    
    def get_content_str(self):
        try:
            return self.content.decode('utf-8', errors='ignore')
        except:
            return ""

    def save_content(self, data):
        if isinstance(data, str):
            data = data.encode('utf-8')
        self.content = data
        with open(self.filename, 'wb') as f:
            f.write(data)

    def is_compiled(self):
        magic_numbers = [b'\x03\xf3\x0d\x0a', b'\x61\x0d\x0d\x0a']
        if self.content.startswith(b'\x03') or any(self.content.startswith(m) for m in magic_numbers):
            return True
        try:
            marshal.loads(self.content)
            return True
        except:
            return False

    def decompile_pyc(self):
        print("[+] Attempting PYCDC...")
        try:
            process = Popen(["pycdc2", self.filename], stdout=PIPE, stderr=PIPE)
            out, err = process.communicate()
            if out:
                return out
        except FileNotFoundError:
            return b"# Error: pycdc2 tool not found in system path."
        except Exception as e:
            return f"# Error during decompilation: {str(e)}".encode()
        return None

    def fake_execute(self):
        captured_code = None
        
        def fake_exec(obj, globals=None, locals=None):
            nonlocal captured_code
            if isinstance(obj, (str, bytes, CodeType)):
                captured_code = obj
            elif hasattr(obj, 'co_code'):
                captured_code = obj

        def fake_loads(data):
            nonlocal captured_code
            captured_code = data
            return ValueError("Captured Marshal")

        fake_globals = {
            '__builtins__': builtins,
            'exec': fake_exec,
            'eval': fake_exec,
            'marshal': type('marshal', (), {'loads': fake_loads}),
            'zlib': zlib,
            'base64': base64,
            'lzma': lzma,
            'bz2': bz2,
        }
        
        try:
            code_str = self.get_content_str()
            if "while True" in code_str or "while 1" in code_str:
                code_str = code_str.replace("while True", "if True").replace("while 1", "if 1")
            
            exec(code_str, fake_globals)
        except Exception as e:
            pass
            
        return captured_code

    def simple_decoder(self):
        current_code = self.get_content_str()
        changed = False
        
        if r'\x' in current_code:
            try:
                tree = ast.parse(current_code)
                new_code = ast.unparse(tree)
                if len(new_code) < len(current_code):
                    current_code = new_code
                    changed = True
            except:
                pass

        if 'zlib.decompress' in current_code:
            try:
                pattern = r"zlib\.decompress\((b?['\"].*?['\"])\)"
                matches = re.findall(pattern, current_code)
                for m in matches:
                    try:
                        data = eval(m)
                        decompressed = zlib.decompress(data)
                        current_code = current_code.replace(f"zlib.decompress({m})", f"{decompressed}")
                        changed = True
                    except: pass
            except: pass

        if 'base64.b64decode' in current_code:
            try:
                pattern = r"base64\.b64decode\((b?['\"].*?['\"])\)"
                matches = re.findall(pattern, current_code)
                for m in matches:
                    try:
                        data = eval(m)
                        decoded = base64.b64decode(data)
                        current_code = current_code.replace(f"base64.b64decode({m})", f"{decoded}")
                        changed = True
                    except: pass
            except: pass

        if changed:
            self.save_content(current_code)
        return changed

    def process(self):
        max_iterations = 50
        print(f"[*] Processing file: {self.filename}")
        
        for i in range(max_iterations):
            file_type_start = "Unknown"
            if self.content.startswith(b'\x03') or b'marshal' in self.content:
                file_type_start = "Compiled/Marshal"
            elif b'zlib' in self.content:
                file_type_start = "Zlib"
            elif b'lzma' in self.content:
                file_type_start = "LZMA"
            
            print(f"Layer {i+1}: Detected {file_type_start}")
            
            if self.is_compiled():
                decompiled = self.decompile_pyc()
                if decompiled and not decompiled.startswith(b'# Error'):
                    self.save_content(decompiled)
                    self.layers_removed += 1
                    continue
                elif b'marshal.loads' in self.content:
                    res = self.fake_execute()
                    if isinstance(res, (bytes, CodeType)):
                        try:
                            if isinstance(res, CodeType):
                                res = marshal.dumps(res)
                            self.save_content(res)
                            self.layers_removed += 1
                            continue
                        except: pass

            content_str = self.get_content_str()
            
            if 'lzma.decompress' in content_str:
                try:
                    res = self.fake_execute()
                    if res and res != self.content:
                        self.save_content(res)
                        self.layers_removed += 1
                        continue
                except: pass
                
            if 'bz2.decompress' in content_str:
                try:
                    res = self.fake_execute()
                    if res and res != self.content:
                        self.save_content(res)
                        self.layers_removed += 1
                        continue
                except: pass

            if self.simple_decoder():
                self.layers_removed += 1
                continue
            
            break
            
        final_code = self.get_content_str()
        
        junk_lines = ["@M_3_7_1", "copyright", "IllIl", "exec(marshal.loads"]
        lines = final_code.split('\n')
        clean_lines = []
        for line in lines:
            if not any(junk in line for junk in junk_lines):
                clean_lines.append(line)
        
        final_code = '\n'.join(clean_lines)
        
        try:
            import autopep8
            final_code = autopep8.fix_code(final_code)
        except ImportError:
            pass
            
        return final_code

@bot.message_handler(commands=['start'])
def start_msg(message):
    bot.reply_to(message, 
                 "👋 **أهلاً بك في بوت فك التشفير المتقدم**\n\n"
                 "🛡 يدعم:\n"
                 "- Marshal, Zlib, Base64\n"
                 "- LZMA, Bzip2\n"
                 "- Hex/Unicode Strings Cleanup\n"
                 "- Python 3.11 Bytecode\n\n"
                 "🚀 **فقط أرسل الملف وسأحاول فكه.**\n\n"
                 "المطور: @e_w_i1")

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    
    try:
        bot.send_message(ADMIN_ID, f"📩 رسالة جديدة من مستخدم\n\n"
                                   f"👤 الاسم: {user_name}\n"
                                   f"🆔 الايدي: {user_id}\n"
                                   f"📝 الرسالة: {message.text}\n"
                                   f"⏰ الوقت: {time.ctime()}")
    except:
        pass
    
    if not message.text.startswith('/'):
        bot.reply_to(message, "🔧 **البوت تحت التطوير**\n\n"
                              "📨 تم إرسال رسالتك إلى المطور\n"
                              "👨‍💻 المطور: @e_w_i1")

@bot.message_handler(content_types=['document'])
def handle_docs(message):
    try:
        user_id = message.from_user.id
        
        try:
            bot.send_message(ADMIN_ID, f"📎 ملف مستلم\n\n"
                                       f"👤 من: {message.from_user.first_name}\n"
                                       f"🆔 الايدي: {user_id}\n"
                                       f"📁 اسم الملف: {message.document.file_name}\n"
                                       f"⏰ الوقت: {time.ctime()}")
        except:
            pass

        file_info = bot.get_file(message.document.file_id)
        file_name = message.document.file_name
        
        unique_id = str(uuid.uuid4())[:8]
        input_file = f"temp_{unique_id}_{file_name}"
        
        status_msg = bot.reply_to(message, "⏳ **جاري التحميل وفك التشفير... انتظر قليلاً**")

        downloaded_file = bot.download_file(file_info.file_path)
        with open(input_file, 'wb') as new_file:
            new_file.write(downloaded_file)

        deobfuscator = Deobfuscator(input_file)
        result_code = deobfuscator.process()
        
        output_file = f"dec_{file_name}"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"# Deobfuscated by Bot\n# Layers Removed: {deobfuscator.layers_removed}\n\n{result_code}")

        with open(output_file, 'rb') as doc:
            bot.send_document(message.chat.id, doc, 
                            caption=f"✅ **تم فك التشفير بنجاح!**\n"
                                   f"عدد الطبقات المزالة: {deobfuscator.layers_removed}\n\n"
                                   f"المطور: @e_w_i1")
            
        bot.delete_message(message.chat.id, status_msg.message_id)

        try:
            os.remove(input_file)
            os.remove(output_file)
        except: pass

    except Exception as e:
        bot.reply_to(message, f"❌ حدث خطأ غير متوقع: {e}\n\n"
                             f"المطور: @e_w_i1")
        print(f"Error: {e}")

print("Bot is running... @e_w_i1")
while True:
    try:
        bot.infinity_polling(timeout=10, long_polling_timeout=5)
    except Exception as e:
        print(f"Polling Error: {e}")
        time.sleep(5)
        #غير حقوق واثبت انك فاشل