#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🤖 Gemini CLI Advanced Bot v3.0 - Smart Detection Edition
Bot عبقري يكتشف كل شيء بنفسه ويتحكم في Gemini CLI بكل ذكاء

المميزات:
- Auto-detection ذكي للـ CLI وخصائصه
- Logging شامل لكل حاجة (input/output/patterns)
- Pattern recognition تلقائي متقدم
- Adaptive interaction بناءً على ما يكتشفه
- حفظ كامل للعمليات والـ diagnostics
- معالجة أخطاء ذكية جداً
- Detailed analysis reports
"""

import subprocess
import sys
import time
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Tuple
import re
import threading
import queue
import shutil


class AdvancedLogger:
    """Logger متقدم جداً يسجل كل حاجة بالتفصيل الممل"""
    
    def __init__(self, log_dir: Path):
        self.log_dir = log_dir
        self.log_dir.mkdir(exist_ok=True)
        
        # ملفات السجل المختلفة
        self.main_log = log_dir / 'bot.log'
        self.interaction_log = log_dir / 'interactions.log'
        self.diagnostics_log = log_dir / 'diagnostics.log'
        self.patterns_log = log_dir / 'patterns.log'
        self.raw_output_log = log_dir / 'raw_output.log'
        self.analysis_log = log_dir / 'analysis.log'
    
    def log_main(self, message: str, level: str = "INFO"):
        """السجل الرئيسي"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        log_entry = f"[{timestamp}] [{level}] {message}"
        print(log_entry)
        
        with open(self.main_log, 'a', encoding='utf-8') as f:
            f.write(log_entry + '\n')
    
    def log_interaction(self, interaction_type: str, content: str, metadata: Dict = None):
        """تسجيل التفاعلات"""
        timestamp = datetime.now().isoformat()
        entry = {
            'timestamp': timestamp,
            'type': interaction_type,
            'content': content,
            'metadata': metadata or {}
        }
        
        with open(self.interaction_log, 'a', encoding='utf-8') as f:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')
    
    def log_diagnostic(self, diagnostic_type: str, data: Dict):
        """تسجيل التشخيصات"""
        timestamp = datetime.now().isoformat()
        entry = {
            'timestamp': timestamp,
            'type': diagnostic_type,
            'data': data
        }
        
        with open(self.diagnostics_log, 'a', encoding='utf-8') as f:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')
    
    def log_pattern(self, pattern_type: str, pattern: str, matched_text: str = ""):
        """تسجيل الأنماط المكتشفة"""
        entry = f"[{datetime.now().isoformat()}] [{pattern_type}] Pattern: {pattern}"
        if matched_text:
            entry += f" => Matched: {matched_text[:100]}"
        
        with open(self.patterns_log, 'a', encoding='utf-8') as f:
            f.write(entry + '\n')
    
    def log_raw_output(self, output: str, label: str = "OUTPUT"):
        """تسجيل المخرجات الخام"""
        with open(self.raw_output_log, 'a', encoding='utf-8') as f:
            f.write(f"\n{'='*60}\n")
            f.write(f"[{label}] @ {datetime.now().isoformat()}\n")
            f.write(f"{'='*60}\n")
            f.write(output)
            f.write("\n" + "="*60 + "\n")
    
    def log_analysis(self, analysis_type: str, analysis_data: Dict):
        """تسجيل التحليلات"""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'type': analysis_type,
            'data': analysis_data
        }
        
        with open(self.analysis_log, 'a', encoding='utf-8') as f:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')


class CLIDetector:
    """كاشف ذكي جداً للـ CLI وكل خصائصه"""
    
    def __init__(self, logger: AdvancedLogger):
        self.logger = logger
        self.detected_features = {}
        self.is_interactive = False
        self.prompts = []
        self.output_patterns = []
        self.error_patterns = []
        self.success_patterns = []
    
    def detect_cli(self, cli_command: str, cwd: Path = None) -> Dict:
        """كشف الـ CLI وكل خصائصه"""
        self.logger.log_main(f"🔍 Starting comprehensive CLI detection for: {cli_command}")
        
        features = {
            'command': cli_command,
            'timestamp': datetime.now().isoformat(),
            'initial_output': '',
            'has_prompt': False,
            'has_menu': False,
            'is_interactive': False,
            'detected_prompts': [],
            'detected_patterns': [],
            'error_indicators': [],
            'success_indicators': [],
            'estimated_interaction_type': 'unknown',
            'requires_batch_mode': False,
            'requires_setup': False,
            'is_running': False
        }
        
        try:
            self.logger.log_main("📤 Spawning CLI process with improved handling...")
            
            process = subprocess.Popen(
                cli_command,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT, # Merge stderr to see errors like missing API key
                encoding='utf-8',
                shell=True,
                text=True,
                bufsize=1,  # Line Buffered is crucial for Windows
                universal_newlines=True,
                cwd=str(cwd) if cwd else None
            )
            
            self.logger.log_main("⏳ Waiting 5 seconds for initial output (checking continuously)...")
            
            initial_output = ""
            test_response = ""
            
            # استنى 5 ثواني وحاول اقرأ
            for i in range(5):
                time.sleep(1)
                try:
                    # حاول قراءة من stdout
                    if process.stdout.readable():
                        chunk = process.stdout.read(100)
                        if chunk:
                            initial_output += chunk
                            self.logger.log_main(f"   📥 Got output (iteration {i+1}): {len(chunk)} bytes")
                except:
                    pass
            
            self.logger.log_raw_output(initial_output, "INITIAL_CLI_OUTPUT")
            features['initial_output'] = initial_output[:2000]
            features['is_running'] = process.poll() is None
            
            # تحليل المخرجات
            self._analyze_output(initial_output, features)
            
            # محاولة إرسال مدخل تجريبي
            self.logger.log_main("📝 Trying to send test input (Enter key)...")
            try:
                if process.poll() is not None:
                    raise Exception(f"Process exited prematurely with code {process.returncode}")

                # اكتب Enter بدل 'test'
                process.stdin.write('\n')
                process.stdin.flush()
                
                self.logger.log_main("⏳ Waiting for response to Enter...")
                time.sleep(2)
                
                try:
                    if process.stdout.readable():
                        chunk = process.stdout.read(500)
                        if chunk:
                            test_response = chunk
                            self.logger.log_raw_output(test_response, "TEST_INPUT_RESPONSE")
                            features['test_response'] = test_response[:2000]
                            self.logger.log_main("✅ CLI accepted input")
                            features['is_interactive'] = True
                except:
                    pass
                
            except Exception as e:
                self.logger.log_main(f"⚠️ Test input failed: {e}", "WARNING")
                features['requires_setup'] = True
            
            # أغلق الـ process
            try:
                if process.poll() is None:
                    process.stdin.write('exit\n')
                    process.stdin.flush()
                time.sleep(0.5)
                process.terminate()
                time.sleep(1)
                if process.poll() is None:
                    process.kill()
            except:
                pass
            
            # حفظ النتائج
            self.detected_features = features
            self.logger.log_diagnostic("cli_detection_complete", features)
            self.logger.log_main("✅ CLI detection completed successfully", "SUCCESS")
            
            return features
            
        except Exception as e:
            self.logger.log_main(f"❌ Detection error: {e}", "ERROR")
            self.logger.log_diagnostic("detection_error", {
                'error': str(e),
                'type': type(e).__name__
            })
            return features
    
    def _analyze_output(self, output: str, features: Dict):
        """تحليل المخرجات بعمق"""
        self.logger.log_main("🔬 Analyzing output patterns...")
        
        lines = output.split('\n')
        
        # كشف وضع الـ Batch (المشكلة اللي عندك)
        if "No input provided via stdin" in output or "--prompt option" in output:
            features['requires_batch_mode'] = True
            self.logger.log_main("⚠️ CLI detected as Batch-Only (Requires --prompt)", "WARNING")
        
        # كشف الـ prompts
        prompt_keywords = ['>', ':', '$', '#', 'Q:', '?', '▶', '→', 'Input:', 'Enter:']
        for line in lines:
            for prompt in prompt_keywords:
                if prompt in line:
                    features['detected_prompts'].append(prompt)
                    self.logger.log_pattern("prompt_detected", prompt, line)
        
        # كشف القوائس
        if any(x in output for x in ['[1]', '[2]', '1.', '2.', 'Select', 'Choose']):
            features['has_menu'] = True
            self.logger.log_pattern("menu_detected", "Numbered menu found", output[:100])
        
        # كشف الأخطاء
        error_keywords = ['error', 'failed', 'not found', 'invalid', 'خطأ', 'Error', 'Failed']
        for keyword in error_keywords:
            if keyword.lower() in output.lower():
                features['error_indicators'].append(keyword)
                self.logger.log_pattern("error_indicator", keyword, output[:100])
        
        # كشف النجاح
        success_keywords = ['success', 'connected', 'ready', 'initialized', 'أهلا', 'مرحبا', 'Hello', 'Welcome']
        for keyword in success_keywords:
            if keyword.lower() in output.lower():
                features['success_indicators'].append(keyword)
                self.logger.log_pattern("success_indicator", keyword, output[:100])
        
        # تحديد نوع التفاعل
        if features['has_menu']:
            features['estimated_interaction_type'] = 'menu_driven'
        elif features['detected_prompts']:
            features['estimated_interaction_type'] = 'prompt_based'
        elif 'error' not in output.lower():
            features['estimated_interaction_type'] = 'potentially_interactive'
        
        self.logger.log_analysis("output_analysis", features)


class GeminiBot:
    """Bot عبقري جداً يتعلم بنفسه"""
    
    def __init__(self, cli_command: str = 'npx gemini', auto_save: bool = True, cwd: Path = None, api_key: str = None):
        """تهيئة البوت الذكي"""
        self.cli_command = cli_command
        self.auto_save = auto_save
        self.cwd = cwd
        self.config_dir = Path.home() / '.gemini_bot'
        self.config_dir.mkdir(exist_ok=True)
        
        # تهيئة Logger
        self.logger = AdvancedLogger(self.config_dir)
        
        # ملفات الحفظ
        self.history_file = self.config_dir / 'chat_history.json'
        self.knowledge_file = self.config_dir / 'cli_knowledge.json'
        self.detection_file = self.config_dir / 'cli_detection.json'
        
        # متغيرات الحالة
        self.process: Optional[subprocess.Popen] = None
        self.conversation_history: List[Dict] = []
        self.cli_knowledge = {}
        self.cli_detection = {}
        self.is_running = False
        self.use_batch_mode = False # وضع التشغيل المتقطع
        
        # صف انتظار للمخرجات وتسجيل خام (الحل المجنون)
        self.output_queue = queue.Queue()
        self.raw_stream_log = self.config_dir / 'FULL_RAW_STREAM.log'
        
        # كاشف الـ CLI
        self.detector = CLIDetector(self.logger)
        
        # تحميل البيانات السابقة
        self._load_all_data()
        
        # --- FIX: Check for API Key ---
        if api_key:
            os.environ['GEMINI_API_KEY'] = api_key
            self.logger.log_main("✅ Custom API Key injected into environment")
            
        if 'GEMINI_API_KEY' not in os.environ:
            self.logger.log_main("⚠️ GEMINI_API_KEY not found in environment")
            print("\n" + "!"*60)
            print("🔑 ENTER GEMINI API KEY")
            print("!"*60)
            key = input("Paste your API Key here: ").strip()
            if key:
                os.environ['GEMINI_API_KEY'] = key
                self.logger.log_main("✅ API Key injected into environment")
        # ------------------------------
        
        # إظهار رسالة البداية
        self._show_startup()
    
    def _load_all_data(self):
        """تحميل جميع البيانات المحفوظة"""
        # تحميل السجل
        if self.history_file.exists():
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    self.conversation_history = json.load(f)
                self.logger.log_main(f"📖 Loaded {len(self.conversation_history)} messages from history")
            except Exception as e:
                self.logger.log_main(f"⚠️ Error loading history: {e}", "WARNING")
        
        # تحميل المعرفة
        if self.knowledge_file.exists():
            try:
                with open(self.knowledge_file, 'r', encoding='utf-8') as f:
                    self.cli_knowledge = json.load(f)
                self.logger.log_main(f"🧠 Loaded CLI knowledge")
            except Exception as e:
                self.logger.log_main(f"⚠️ Error loading knowledge: {e}", "WARNING")
        
        # تحميل نتائج الكشف
        if self.detection_file.exists():
            try:
                with open(self.detection_file, 'r', encoding='utf-8') as f:
                    self.cli_detection = json.load(f)
                self.logger.log_main(f"🔍 Loaded previous detection results")
            except Exception as e:
                self.logger.log_main(f"⚠️ Error loading detection: {e}", "WARNING")
    
    def _save_all_data(self):
        """حفظ جميع البيانات"""
        # حفظ السجل
        if self.auto_save:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.conversation_history, f, ensure_ascii=False, indent=2)
        
        # حفظ المعرفة
        with open(self.knowledge_file, 'w', encoding='utf-8') as f:
            json.dump(self.cli_knowledge, f, ensure_ascii=False, indent=2)
        
        # حفظ الكشف
        with open(self.detection_file, 'w', encoding='utf-8') as f:
            json.dump(self.cli_detection, f, ensure_ascii=False, indent=2)
    
    def _show_startup(self):
        """عرض رسالة البداية"""
        print("\n" + "="*75)
        print("🤖 GEMINI CLI ADVANCED BOT v3.0 - Smart Detection Edition")
        print("="*75)
        print(f"📁 Config Directory: {self.config_dir}")
        print(f"📊 Logging Files:")
        print(f"   • bot.log - Main operations log")
        print(f"   • interactions.log - All I/O interactions")
        print(f"   • diagnostics.log - System diagnostics")
        print(f"   • patterns.log - Detected patterns")
        print(f"   • raw_output.log - Raw CLI output")
        print(f"   • analysis.log - Detailed analysis")
        print("="*75 + "\n")
        
        self.logger.log_main("Bot initialized successfully")
    
    def start_with_detection(self):
        """بدء الـ CLI مع الكشف الذكي الشامل"""
        self.logger.log_main("="*75)
        self.logger.log_main("🚀 STARTING SMART CLI DETECTION & INITIALIZATION")
        self.logger.log_main("="*75)
        
        # خطوة 1: كشف الـ CLI
        self.logger.log_main(f"\n[STEP 1/3] Running CLI detection...")
        detection_results = self.detector.detect_cli(self.cli_command, cwd=self.cwd)
        self.cli_detection = detection_results
        
        # التحقق من وضع الـ Batch
        if detection_results.get('requires_batch_mode'):
            self.logger.log_main("🔄 Switching to BATCH MODE (One-Shot) due to CLI limitations")
            self.use_batch_mode = True
            # لا نوقف هنا، سنكمل ولكن سنغير طريقة الإرسال
        
        # خطوة 2: حفظ النتائج
        self.logger.log_main(f"\n[STEP 2/3] Saving detection results...")
        self.cli_knowledge['detected_features'] = detection_results
        self.cli_knowledge['cli_command'] = self.cli_command
        self.cli_knowledge['last_detection'] = datetime.now().isoformat()
        self._save_all_data()
        
        # عرض نتائج الكشف
        print("\n" + "="*75)
        print("📊 DETECTION RESULTS SUMMARY")
        print("="*75)
        print(f"Command: {detection_results['command']}")
        print(f"Is Interactive: {detection_results['is_interactive']}")
        print(f"Requires Setup: {detection_results['requires_setup']}")
        print(f"Estimated Type: {detection_results['estimated_interaction_type']}")
        print(f"Initial Output Length: {len(detection_results['initial_output'])} bytes")
        if detection_results['initial_output']:
            print(f"Initial Output Preview: {detection_results['initial_output'][:200]}")
        print("="*75)
        
        # خطوة 3: محاولة البدء
        self.logger.log_main(f"\n[STEP 3/3] Starting CLI process...")
        
        if self.use_batch_mode:
            self.is_running = True
            self.logger.log_main("✅ Bot started in BATCH MODE (Will spawn process per command)", "SUCCESS")
            return True
            
        try:
            self.process = subprocess.Popen(
                self.cli_command,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT, # Important: Merge stderr to see errors
                encoding='utf-8',
                errors='replace', # عشان لو فيه رموز غريبة ميموتش
                bufsize=1,  # Line Buffered
                shell=True,
                text=True,
                universal_newlines=True,
                cwd=str(self.cwd) if self.cwd else None
            )
            
            self.is_running = True
            
            # --- NEW: تشغيل قارئ الخلفية المجنون ---
            self.logger.log_main(f"🔴 STARTING CRAZY RAW RECORDING TO: {self.raw_stream_log}")
            
            def _continuous_reader():
                """قارئ خلفية يسجل كل همسة بتطلع من الـ CLI"""
                try:
                    with open(self.raw_stream_log, 'a', encoding='utf-8', buffering=1) as f:
                        f.write(f"\n{'='*50}\nSESSION START: {datetime.now()}\n{'='*50}\n")
                        while self.is_running and self.process:
                            char = self.process.stdout.read(1) # اقرأ بالحرف الواحد
                            if not char: break
                            f.write(char) # سجل في الملف فوراً
                            self.output_queue.put(char) # ابعته للبوت
                except Exception as e:
                    self.logger.log_main(f"❌ Reader died: {e}", "ERROR")

            threading.Thread(target=_continuous_reader, daemon=True).start()
            # ---------------------------------------
            
            time.sleep(2)
            
            # تحقق من أن الـ process يعمل
            if self.process.poll() is not None:
                self.logger.log_main("❌ Process exited immediately", "ERROR")
                return False
            
            self.logger.log_main("✅ CLI process started successfully", "SUCCESS")
            self.logger.log_interaction("process_started", "CLI process created", {
                'pid': self.process.pid,
                'command': self.cli_command,
                'is_running': True
            })
            
            return True
            
        except Exception as e:
            self.logger.log_main(f"❌ Failed to start CLI: {e}", "ERROR")
            self.logger.log_diagnostic("startup_error", {
                'error': str(e),
                'command': self.cli_command,
                'type': type(e).__name__
            })
            return False
    
    def _check_and_handle_menu(self, buffer: str) -> bool:
        """فحص ومعالجة القوائم التفاعلية بشكل ديناميكي"""
        # تنظيف النص من أكواد الألوان للتحليل
        clean_buffer = re.sub(r'\x1b\[[0-9;]*m', '', buffer)
        
        # شرط مبدئي: وجود خيارات مرقمة (1. و 2. على الأقل)
        if "1." in clean_buffer and "2." in clean_buffer:
            lines = clean_buffer.split('\n')
            options = []
            prompt_text = "Select an option:"
            
            for line in lines:
                line = line.strip()
                # تجاهل خطوط الإطار
                if set(line).issubset(set("─│╭╮╰╯ ")):
                    continue
                    
                # محاولة استخراج السؤال
                if "?" in line or ":" in line:
                    if not re.search(r'\d+\.', line): 
                        prompt_text = line.replace('│', '').strip()

                # استخراج الخيارات: يبحث عن "رقم. نص"
                match = re.search(r'(?:[│\s]*)(?:[●?]\s*)?(\d+)\.\s+([^│]+)', line)
                if match:
                    idx = int(match.group(1))
                    text = match.group(2).strip()
                    options.append((idx, text))

            if len(options) >= 2:
                options.sort(key=lambda x: x[0])
                print("\n" + "═"*60)
                print("🚨 INTERACTION REQUIRED")
                print(f"❓ {prompt_text}")
                print("═"*60)
                for idx, text in options:
                    print(f"   {idx}. {text}")
                print("═"*60)
                
                while True:
                    try:
                        choice_str = input(f"👉 Select option (1-{len(options)}): ").strip()
                        choice = int(choice_str)
                        if any(opt[0] == choice for opt in options):
                            break
                    except ValueError:
                        pass
                
                # إرسال المفاتيح (نفترض المؤشر يبدأ عند 1)
                down_presses = choice - 1
                keys = ("\x1b[B" * down_presses) + "\n"
                
            self.process.stdin.write(keys)
            self.process.stdin.flush()
            self.logger.log_main(f"✅ Handled dynamic menu: Selected option {choice}")
            return True
        return False

    def send_message_smart(self, message: str, wait_time: float = 2.5) -> bool:
        """إرسال رسالة بشكل ذكي مع timeout محسن"""
        if not self.is_running:
            self.logger.log_main("⚠️ CLI not running", "WARNING")
            return False
        
        # تحويل لمسار الـ Batch لو مفعل
        if self.use_batch_mode:
            return self._send_batch_message(message)
            
        try:
            self.logger.log_main(f"📤 Sending message: {message[:60]}...")
            self.logger.log_interaction("message_sent", message, {
                'length': len(message),
                'timestamp': datetime.now().isoformat()
            })
            
            if self.process.poll() is not None:
                self.logger.log_main(f"❌ Process is dead (Exit Code: {self.process.returncode})", "ERROR")
                return False
            
            # إرسال الرسالة مع فحص الـ stream
            try:
                self.process.stdin.write(message + '\n')
                self.process.stdin.flush()
                self.logger.log_main(f"✓ Message written to stdin successfully")
            except Exception as e:
                self.logger.log_main(f"❌ Error writing to stdin: {e}", "ERROR")
                return False
            
            # حفظ في السجل
            self.conversation_history.append({
                'timestamp': datetime.now().isoformat(),
                'type': 'user',
                'message': message,
                'status': 'sent'
            })
            
            # انتظ الرد مع timeout أفضل
            self.logger.log_main(f"⏳ Waiting {wait_time}s for response (checking every 0.5s)...")
            
            response = ""
            start_time = time.time()
            menu_handled = False
            
            print(f"\n🤖 Bot:")
            
            # القراءة من الـ Queue بدلاً من stdout مباشرة عشان منضيعش حاجة
            while time.time() - start_time < wait_time:
                if self.process.poll() is not None:
                    break
                try:
                    char = self.output_queue.get(timeout=0.1)
                    response += char
                    print(char, end='', flush=True)
                    start_time = time.time() # تجديد الوقت مع كل حرف عشان الردود الطويلة متقطعش
                    
                    # كشف القائمة التفاعلية
                    if not menu_handled and ("1." in response and "2." in response):
                        time.sleep(0.3) # انتظار اكتمال النص
                        while not self.output_queue.empty():
                            extra_char = self.output_queue.get()
                            response += extra_char
                            print(extra_char, end='', flush=True)
                            
                        if self._check_and_handle_menu(response):
                            menu_handled = True
                            start_time = time.time() # إعادة تصفير الوقت
                            wait_time = 10.0 # زيادة وقت الانتظار للتنفيذ
                            
                except queue.Empty:
                    continue
            
            print() # سطر جديد بعد انتهاء الرد
            
            if response:
                self.logger.log_raw_output(response, "BOT_RESPONSE")
                self.logger.log_main(f"✅ Received {len(response)} bytes of response")
                
                # عرض الرد
                # print(f"\n🤖 Bot:\n{response}\n") # تم إلغاؤه لأننا طبعنا بالفعل
                
                self.conversation_history.append({
                    'timestamp': datetime.now().isoformat(),
                    'type': 'bot',
                    'message': response,
                    'status': 'received'
                })
            else:
                self.logger.log_main("⚠️ No response received (Process may need setup)", "WARNING")
                print("⚠️ No response from CLI - it may require setup/authentication first")
            
            self._save_all_data()
            return True
            
        except Exception as e:
            self.logger.log_main(f"❌ Error sending message: {e}", "ERROR")
            self.logger.log_diagnostic("send_error", {
                'error': str(e),
                'message_preview': message[:100],
                'type': type(e).__name__
            })
            return False
    
    def _send_batch_message(self, message: str) -> bool:
        """إرسال رسالة في وضع الـ Batch مع عرض النتيجة حرف بحرف (Streaming)"""
        try:
            self.logger.log_main(f"📤 Sending BATCH message: {message[:60]}...")
            
            # تجهيز الأمر مع الهروب من الرموز الخاصة
            safe_message = message.replace('"', '\\"')
            # --- FIX: Add the --yolo flag to enable all tools in batch mode ---
            batch_cmd = f'{self.cli_command} --yolo --prompt "{safe_message}"'
            
            self.logger.log_main(f"🚀 Spawning batch process (Streaming Mode)...")
            
            # استخدام Popen بدلاً من run لقراءة المخرجات لحظياً
            process = subprocess.Popen(
                batch_cmd,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding='utf-8',
                errors='replace',
                cwd=str(self.cwd) if self.cwd else None,
                bufsize=0 # Unbuffered output
            )
            
            print(f"\n🤖 Bot:")
            response = ""
            
            # حلقة قراءة المخرجات حرفاً بحرف
            while True:
                char = process.stdout.read(1)
                if not char and process.poll() is not None:
                    break
                if char:
                    print(char, end='', flush=True)
                    response += char
            
            # قراءة الأخطاء إن وجدت بعد الانتهاء
            stderr_output = process.stderr.read()
            if stderr_output:
                self.logger.log_main(f"⚠️ Batch stderr: {stderr_output}", "WARNING")
            
            print() # سطر جديد في النهاية
            
            self.logger.log_raw_output(response, "BATCH_RESPONSE")
            
            self.conversation_history.append({
                'timestamp': datetime.now().isoformat(),
                'type': 'bot',
                'message': response,
                'status': 'received'
            })
            return True
            
        except Exception as e:
            self.logger.log_main(f"❌ Batch execution failed: {e}", "ERROR")
            return False

    def interactive_mode(self):
        """وضع تفاعلي ذكي"""
        if not self.start_with_detection():
            self.logger.log_main("❌ Failed to start bot. Check logs for details.", "ERROR")
            return
        
        print("\n" + "="*75)
        print("💬 INTERACTIVE MODE - Smart Detection Enabled")
        print("="*75)
        print("Commands: 'help' | 'logs' | 'knowledge' | 'detection' | 'exit'")
        print("="*75 + "\n")
        
        self.logger.log_main("Entered interactive mode")
        
        try:
            while self.is_running:
                try:
                    user_input = input("\n👤 You: ").strip()
                    
                    if not user_input:
                        continue
                    
                    # أوامر خاصة
                    if user_input.lower() == 'exit':
                        self.logger.log_main("User requested exit")
                        break
                    
                    elif user_input.lower() == 'logs':
                        self._show_logs_summary()
                        continue
                    
                    elif user_input.lower() == 'knowledge':
                        self._show_knowledge()
                        continue
                    
                    elif user_input.lower() == 'detection':
                        self._show_detection()
                        continue
                    
                    elif user_input.lower() == 'help':
                        self._show_help()
                        continue
                    
                    # إرسال رسالة عادية
                    self.send_message_smart(user_input, wait_time=3.0)
                    
                except KeyboardInterrupt:
                    self.logger.log_main("User interrupted with Ctrl+C")
                    break
                except EOFError:
                    break
        
        finally:
            self.close()
    
    def _show_logs_summary(self):
        """عرض ملخص السجلات"""
        print("\n" + "="*75)
        print("📊 LOGS SUMMARY")
        print("="*75)
        
        for log_file in ['bot.log', 'interactions.log', 'diagnostics.log', 'patterns.log', 'raw_output.log', 'analysis.log']:
            path = self.config_dir / log_file
            if path.exists():
                size = path.stat().st_size / 1024
                lines = len(path.read_text(encoding='utf-8', errors='ignore').split('\n'))
                print(f"📄 {log_file:20} | Size: {size:8.2f} KB | Lines: {lines:5}")
        
        print("="*75)
    
    def _show_knowledge(self):
        """عرض المعرفة المكتشفة"""
        print("\n" + "="*75)
        print("🧠 LEARNED CLI KNOWLEDGE")
        print("="*75)
        if self.cli_knowledge:
            print(json.dumps(self.cli_knowledge, ensure_ascii=False, indent=2))
        else:
            print("❌ No knowledge learned yet")
        print("="*75)
    
    def _show_detection(self):
        """عرض نتائج الكشف"""
        print("\n" + "="*75)
        print("🔍 CLI DETECTION RESULTS")
        print("="*75)
        if self.cli_detection:
            print(json.dumps(self.cli_detection, ensure_ascii=False, indent=2))
        else:
            print("❌ No detection results available")
        print("="*75)
    
    def _show_help(self):
        """عرض المساعدة"""
        help_text = """
╔══════════════════════════════════════════════════════════════════╗
║         🆘 SMART BOT COMMANDS & FEATURES                         ║
╚══════════════════════════════════════════════════════════════════╝

📝 MESSAGE INPUT:
  • Type any message to send to Gemini CLI
  • Bot automatically detects and logs all responses

⚙️  SPECIAL COMMANDS:
  • 'logs'       - Show detailed logs summary
  • 'knowledge'  - Show learned CLI knowledge
  • 'detection'  - Show CLI detection results
  • 'help'       - Show this help message
  • 'exit'       - Exit the program

🔍 AUTO-DETECTION CAPABILITIES:
  ✓ Detects CLI type & interaction patterns
  ✓ Learns from every interaction
  ✓ Adapts response handling dynamically
  ✓ Identifies prompt types & menu structures
  ✓ Recognizes success/error indicators
  ✓ Logs everything for analysis

📊 COMPREHENSIVE LOGGING:
  • bot.log          - Main operations
  • interactions.log - All I/O events
  • diagnostics.log  - System diagnostics
  • patterns.log     - Pattern detection
  • raw_output.log   - Raw CLI output
  • analysis.log     - Deep analysis
        """
        print(help_text)
    
    def close(self):
        """إغلاق الـ CLI بشكل آمن"""
        try:
            if self.process and self.is_running and not self.use_batch_mode:
                self.logger.log_main("🛑 Closing CLI process...")
                
                try:
                    if self.process.poll() is None:
                        self.process.stdin.write('exit\n')
                        self.process.stdin.flush()
                except:
                    pass
                
                time.sleep(1)
                
                if self.process.poll() is None:
                    self.logger.log_main("Terminating process...")
                    self.process.terminate()
                    time.sleep(1)
                
                if self.process.poll() is None:
                    self.logger.log_main("Force killing process...")
                    self.process.kill()
                
                self.is_running = False
                self.logger.log_main("✅ CLI closed successfully", "SUCCESS")
                
        except Exception as e:
            self.logger.log_main(f"⚠️ Error during close: {e}", "WARNING")
            self.is_running = False


def main():
    """الدالة الرئيسية"""
    print("\n" + "="*50)
    print("⚙️  CONFIGURATION")
    print("="*50)
    
    # 1. Working Directory
    target_dir = input("📂 Enter working directory path (Press Enter for current): ").strip().strip('"').strip("'")
    cwd = Path(target_dir).expanduser().resolve() if target_dir else None
    
    if cwd and not cwd.exists():
        print(f"❌ Directory not found: {cwd}")
        return

    # 2. API Key
    use_custom_key = input("🔑 Do you want to use a specific API Key? (y/n): ").strip().lower()
    api_key = None
    if use_custom_key == 'y':
        api_key = input("   Paste your API Key: ").strip()

    bot = GeminiBot(cwd=cwd, api_key=api_key)
    bot.interactive_mode()


if __name__ == '__main__':
    main()
