"""
bot/handlers/ai/tools.py
Contains the AITools class which defines the callable tools for the AI Agent.
The methods in this class are passed directly to the Google GenAI SDK.
"""

import logging
import os
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)

class AITools:
    """
    A toolkit class that wraps the CodeEditor and exposes methods as AI tools.
    """
    def __init__(self, editor_instance: Any, context_data: str = None, draft_path: str = None, plan_path: str = None):
        self.editor = editor_instance
        self.context_data = context_data
        self.draft_path = draft_path
        self.plan_path = plan_path

    def search_file(self, pattern: str, is_regex: bool = True, case_sensitive: bool = False) -> Dict[str, Any]:
        """
        Searches for a pattern in the file content and returns matching lines.
        
        Args:
            pattern: The string or regex pattern to search for.
            is_regex: Treat pattern as regex. Default True.
            case_sensitive: Case sensitive search. Default False.
        """
        return {'result': self.editor.search(pattern, is_regex, case_sensitive)}

    def read_lines(self, start_line: int, end_line: int) -> Dict[str, Any]:
        """
        Reads a specific range of lines from the file.
        
        Args:
            start_line: Start line number (1-based).
            end_line: End line number (1-based).
        """
        return {'result': self.editor.read_lines(start_line, end_line)}

    def replace_lines(self, start_line: int, end_line: int, new_content: str) -> Dict[str, Any]:
        """
        Replaces a block of existing lines with new content.
        
        Args:
            start_line: Start line of block to replace.
            end_line: End line of block to replace.
            new_content: New content to insert.
        """
        return {'result': self.editor.replace_lines(start_line, end_line, new_content)}

    def insert_lines(self, at_line: int, new_content: str) -> Dict[str, Any]:
        """
        Inserts new content at a specific line number.
        
        Args:
            at_line: Line number to insert at.
            new_content: Content to insert.
        """
        return {'result': self.editor.insert_lines(at_line, new_content)}

    def delete_lines(self, start_line: int, end_line: int) -> Dict[str, Any]:
        """
        Deletes a block of lines from the file.
        
        Args:
            start_line: Start line to delete.
            end_line: End line to delete.
        """
        return {'result': self.editor.delete_lines(start_line, end_line)}

    def get_file_content(self) -> Dict[str, Any]:
        """
        Returns the entire content of the file.
        """
        return {'result': self.editor.get_content()}

    def apply_changes(self) -> Dict[str, Any]:
        """
        Saves the current state to a draft file (Final Step).
        """
        if not self.draft_path:
            return {'result': "ERROR: No draft path provided."}
        return {'result': self.editor.save(output_path=self.draft_path)}

    def read_context(self) -> Dict[str, Any]:
        """
        Reads debug logs or error messages if available.
        """
        content = f"--- DEBUG LOGS ---\n{self.context_data}\n----------------" if self.context_data else "NO CONTEXT."
        return {'result': content}

    def update_plan(self, content: str, append: bool = True) -> Dict[str, Any]:
        """
        Writes or appends to the correction plan (Markdown file).
        
        Args:
            content: The text content to write to the plan.
            append: If True, appends to the file. If False, overwrites it.
        """
        if not self.plan_path:
            return {'result': "ERROR: No plan path provided."}
        
        mode = 'a' if append else 'w'
        try:
            with open(self.plan_path, mode, encoding='utf-8') as f:
                f.write(content + "\n")
            return {'result': "Plan updated successfully."}
        except Exception as e:
            return {'result': f"ERROR writing plan: {e}"}

    def ask_user(self, question: str, options: List[str]) -> Dict[str, Any]:
        """
        Pauses execution to ask the user a multiple-choice question.
        
        Args:
            question: The question to ask the user.
            options: A list of strings representing the choices (max 5).
        """
        # This tool returns a special signal that the AgentEngine will catch
        return {'result': "STATUS_NEEDS_INPUT", 'question': question, 'options': options}

def get_tool_status_message(tool_name: str) -> str:
    """رسالة قصيرة للمستخدم توضح ماذا يفعل البوت الآن"""
    messages = {
        "search_file": "🔍 يبحث في الكود...",
        "read_lines": "📖 يقرأ سطور محددة...",
        "replace_lines": "✏️ يعدل الكود...",
        "insert_lines": "➕ يضيف كود جديد...",
        "delete_lines": "🗑️ يحذف كود...",
        "get_file_content": "📂 يقرأ الملف بالكامل...",
        "apply_changes": "💾 يحفظ التغييرات...",
    }
    if tool_name == "update_plan": return "📝 يكتب خطة التصحيح..."
    if tool_name == "ask_user": return "🤔 يحتاج لاستشارة المستخدم..."
    return messages.get(tool_name, "⚙️ يعالج...")