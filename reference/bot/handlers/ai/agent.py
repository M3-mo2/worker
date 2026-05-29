# bot_v2/bot/handlers/ai/agent.py
# Contains the AgentEngine class for AI-driven code modification.

import os
import json
import time
import logging
import asyncio
import traceback
import re
from typing import Dict, Any, List, Optional

from telethon.errors.rpcerrorlist import MessageNotModifiedError
from groq import Groq
from google import genai
from google.genai import types

# Import Tools from the new file
from bot.handlers.ai.tools import AITools, get_tool_status_message

# Local imports for services (will be moved/created later)
# For now, we'll assume CodeEditor exists in bot.services
# A dedicated CodeEditor service will be created in bot/services/code_editor.py
# For the purpose of getting AgentEngine to work, we might temporarily import it from the old location if necessary,
# but the plan is to move it. For now, we'll define a placeholder and remind ourselves.

# Placeholder for CodeEditor import. This will be replaced.
# from bot.services.code_editor import CodeEditor
from bot.services.code_editor import CodeEditor


# --- Logger Setup ---
# Setup logging for AI operations specific to AgentEngine
ai_logger = logging.getLogger('AI_Operations_AgentEngine')
ai_logger.setLevel(logging.INFO)
os.makedirs('logs', exist_ok=True)
ai_log_handler = logging.FileHandler('logs/ai_operations.log', encoding='utf-8')
ai_log_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
if not ai_logger.hasHandlers():
    ai_logger.addHandler(ai_log_handler)

# --- Helper Functions ---
# =========================================
# 🤖 AgentEngine V9: Multi-Provider Support
# =========================================
class AgentEngine:
    def __init__(self, user_id, file_path, context_data=None, status_msg=None):
        self.user_id = user_id
        self.file_path = file_path
        self.status_msg = status_msg
        self.file_name = os.path.basename(file_path)
        self.draft_path = file_path + ".draft"
        self.plan_path = file_path + ".plan.md"
        self.context_data = context_data
        self.session_id = f"agent_{user_id}_{int(time.time())}"
        self.logger = self._setup_logger()
        # Initialize CodeEditor - this will eventually import from bot.services.code_editor
        self.editor = CodeEditor(file_path) 
        
        # Initialize the Toolkit with the editor instance
        self.toolkit = AITools(self.editor, self.context_data, self.draft_path, self.plan_path)
        
        # Create a list of callable functions to pass to Gemini
        # The SDK will inspect these functions to generate the schema automatically.
        self.tools_list = [
            self.toolkit.search_file, self.toolkit.read_lines, self.toolkit.replace_lines,
            self.toolkit.insert_lines, self.toolkit.delete_lines, self.toolkit.get_file_content,
            self.toolkit.apply_changes, self.toolkit.read_context,
            self.toolkit.update_plan, self.toolkit.ask_user
        ]


    def _setup_logger(self):
        logger = logging.getLogger(self.session_id)
        logger.setLevel(logging.DEBUG)
        os.makedirs("logs/agents", exist_ok=True)
        handler = logging.FileHandler(f"logs/agents/{self.session_id}.log", encoding='utf-8')
        handler.setFormatter(logging.Formatter('%(asctime)s - [AI AGENT] - %(message)s'))
        logger.addHandler(handler)
        return logger

    def log(self, msg):
        self.logger.info(msg)

    async def _update_status(self, text):
        """Safely edits the status message if it exists."""
        if self.status_msg:
            try:
                # Add a thinking emoji for a better UX
                await self.status_msg.edit(f"🤔 {text}...")
            except MessageNotModifiedError:
                pass # Ignore if the message is the same
            except Exception as e:
                self.log(f"Status update failed: {e}")

    async def _execute_tool_call(self, tool_name, tool_args_dict):
        # Update UI
        await self._update_status(get_tool_status_message(tool_name))
        
        # Find the method in our toolkit
        tool_method = getattr(self.toolkit, tool_name, None)
        
        if tool_method and callable(tool_method):
            try:
                # Execute the method directly
                result = tool_method(**tool_args_dict)
                self.log(f"⚙️ Executed {tool_name}: {result.keys()}")
                return result
            except Exception as e:
                self.log(f"🔥 Error executing {tool_name}: {e}")
                return {'result': f"ERROR executing {tool_name}: {e}"}
        else:
            return {'result': f"ERROR: Tool '{tool_name}' not found."}

    async def _send_with_retry(self, chat, content, retries=3):
        """Sends a message with handling for 429 Rate Limits."""
        for attempt in range(retries):
            try:
                return await asyncio.to_thread(chat.send_message, content)
            except Exception as e:
                error_str = str(e)
                if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                    wait_time = 40 * (attempt + 1) # زودنا الوقت شوية (40, 80, 120)
                    wait_time = 10 * (attempt + 1) # قللنا وقت الانتظار لأننا هنعتمد على تغيير المفتاح في المحاولة القادمة
                    self.log(f"⚠️ [RATE LIMIT] Quota exceeded. Sleeping {wait_time}s before retry ({attempt+1}/{retries})...")
                    await asyncio.sleep(wait_time)
                else:
                    raise e
        raise Exception("❌ Failed to send message after multiple retries due to Rate Limits.")

    async def run_debug_agent(self, client, model_name, user_history=None):
        """
        The main loop for the Advanced Debugging Agent.
        """
        self.log("🚀 Starting Advanced Debug Agent...")
        
        # 1. System Prompt (The Brain)
        system_prompt = f"""
        You are a Senior PHP Architect and Security Expert. Your task is to fix a PHP file that has errors.
        File: `{self.file_name}`.
        
        You have access to tools to read code, write a plan, ask the user, and apply fixes.
        
        **PROTOCOL (Follow Strictly):**
        1.  **Analyze:** Read the code and the provided debug logs (`read_context`).
        2.  **Plan:** Create a detailed correction plan using `update_plan`. Explain the root cause and the fix.
        3.  **Consult (Optional):** If there are multiple ways to fix it (e.g., "Delete the bad code" vs "Comment it out" vs "Replace with dummy"), use `ask_user` to let the user decide.
        4.  **Execute:** Apply the fixes using `replace_lines`, `insert_lines`, etc.
        5.  **Finalize:** Call `apply_changes` ONLY when you are done.
        
        **Rules:**
        - Do NOT guess. Read the file content first.
        - If you use `ask_user`, the execution will pause. You will be resumed later with the user's choice appended to the plan.
        - Always write to the plan (`update_plan`) before executing complex changes.
        """

        # 2. Prepare Chat History
        # If we are resuming from a user choice, user_history will contain the previous turn + user's answer.
        history = user_history if user_history else []
        
        # 3. Configure Gemini
        chat = client.chats.create(
            model=model_name,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                tools=self.tools_list, # Pass functions directly for SDK v1
                temperature=0.1, # Low temperature for precision
                max_output_tokens=4000
            ),
            history=history
        )

        # 4. Start/Resume the Loop
        # If resuming, we send a "Proceed" signal. If starting, we send the trigger.
        trigger_msg = "Please start the debugging process." if not user_history else "User has selected an option. Please proceed with the plan."
        
        try:
            start_ts = time.time()
            self.log(f"📤 [REQUEST] Sending trigger: '{trigger_msg}'")
            print(f"\n👉 [DEBUG] Sending to AI: {trigger_msg}")

            # محاولة أولية لتفادي التداخل السريع
            response = await self._send_with_retry(chat, trigger_msg)
            
            print(f"👉 [DEBUG] AI Response Object Received.")
            try:
                print(f"👉 [DEBUG] AI Text: {response.text[:200] if response.text else 'NO TEXT'}")
            except Exception as e:
                print(f"👉 [DEBUG] Could not read text: {e}")

            self.log(f"📥 [RESPONSE] Received in {time.time() - start_ts:.2f}s")
            self.log(f"📝 [RESPONSE CONTENT] {response.text[:500]}..." if response.text else "No text content")
            
            # Reasoning Loop (Max 15 turns for complex debugging)
            for turn in range(15):
                self.log(f"--- Turn {turn+1}/15 ---")
                self.log("⏳ [RATE LIMIT] Sleeping 30s to avoid 429...")
                await asyncio.sleep(30) 
                
                tool_calls_responses = []
                has_function_calls = False
                
                for part in response.parts:
                    if fn_call := part.function_call:
                        print(f"👉 [DEBUG] 🛠️ Function Call Detected: {fn_call.name} | Args: {fn_call.args}")
                        has_function_calls = True
                        tool_name = fn_call.name
                        tool_args = dict(fn_call.args)
                        
                        # Execute Tool
                        tool_result = await self._execute_tool_call(tool_name, tool_args)
                        self.log(f"🔧 [TOOL RESULT] {tool_name}: {str(tool_result)[:200]}...") # Log brief result
                        print(f"👉 [DEBUG] ⚙️ Tool Executed: {tool_name} -> Result keys: {list(tool_result.keys())}")
                        
                        # Check for Special Signals
                        if tool_name == "ask_user" and tool_result.get('result') == "STATUS_NEEDS_INPUT":
                            self.log("⏸️ Agent requested user input.")
                            return {
                                "status": "NEEDS_INPUT",
                                "question": tool_result['question'],
                                "options": tool_result['options'],
                                "history": chat.history # Save history to resume later
                            }
                        
                        if tool_name == "apply_changes" and tool_result.get('result', {}).get('status') == 'success':
                            self.log("✅ Draft saved. Moving to Review Phase.")
                            return await self._run_reviewer_agent(client, model_name)

                        # Serialize result
                        content_str = json.dumps(tool_result)
                        tool_calls_responses.append(types.Part(
                            function_response=types.FunctionResponse(name=tool_name, response={"result": content_str})
                        ))
                
                if has_function_calls:
                    start_ts = time.time()
                    self.log(f"📤 [REQUEST] Sending {len(tool_calls_responses)} tool outputs...")
                    response = await self._send_with_retry(chat, tool_calls_responses)
                    print(f"👉 [DEBUG] Sent tool outputs. New Response received.")
                    self.log(f"📥 [RESPONSE] Received in {time.time() - start_ts:.2f}s")
                    self.log(f"📝 [RESPONSE CONTENT] {response.text[:500]}..." if response.text else "No text content")
                else:
                    # If the model just talks without calling tools, we nudge it or finish.
                    if "STATUS_NO_CHANGES" in response.text:
                        self.log("✅ Agent signaled NO CHANGES.")
                        return {"status": "DONE", "message": "No changes needed."}
                    # Force it to continue if it stopped prematurely
                    start_ts = time.time()
                    self.log("📤 [REQUEST] Sending continuation prompt...")
                    response = await self._send_with_retry(chat, "Please continue with the next step.")
                    print(f"👉 [DEBUG] Sent continuation prompt. New Response received.")
                    self.log(f"📥 [RESPONSE] Received in {time.time() - start_ts:.2f}s")
                    self.log(f"📝 [RESPONSE CONTENT] {response.text[:500]}..." if response.text else "No text content")

            return {"status": "ERROR", "message": "Timeout: Agent took too many turns."}

        except Exception as e:
            self.log(f"🔥 Agent Loop Error: {e}\n{traceback.format_exc()}")
            return {"status": "ERROR", "message": str(e)}

    async def _run_reviewer_agent(self, client, model_name):
        """
        A separate chat session to verify the changes against the plan.
        """
        await self._update_status("جاري المراجعة النهائية (Quality Assurance)")
        self.log("🧐 Starting Reviewer Agent...")
        
        # Read necessary files
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f: original = f.read()
            with open(self.draft_path, 'r', encoding='utf-8') as f: modified = f.read()
            with open(self.plan_path, 'r', encoding='utf-8') as f: plan = f.read()
        except Exception as e:
            return {"status": "ERROR", "message": f"Reviewer failed to read files: {e}"}

        prompt = f"""
        You are a Code Reviewer.
        Original File: `{self.file_name}`
        Plan:
        {plan}
        
        Modified Code:
        ```php
        {modified}
        ```
        
        Task: Verify if the Modified Code correctly implements the Plan and fixes the errors without introducing new ones.
        If it's good, respond with "STATUS_VERIFIED".
        If there are issues, list them briefly.
        """
        
        # Simple one-shot review
        response = await asyncio.to_thread(client.models.generate_content, model=model_name, contents=prompt)
        
        if "STATUS_VERIFIED" in response.text:
            return {"status": "DONE", "message": "Fixed and Verified."}
        else:
            # In a super-advanced version, we would loop back to the fixer. 
            # For now, we accept it but log the warning.
            self.log(f"⚠️ Reviewer had concerns: {response.text}")
            return {"status": "DONE", "message": "Fixed (with reviewer notes)."}