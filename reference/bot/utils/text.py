# bot_v2/bot/utils/text.py
# Contains reusable text formatting and manipulation utilities.

import re
import os
from html.parser import HTMLParser
from typing import List, Optional
from telethon import Button

# --- HTML Stripper for cleaning text (from main.py) ---
class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.text = []
    def handle_data(self, d):
        self.text.append(d)
    def get_data(self):
        return ''.join(self.text)

def strip_html_tags(html_text: str) -> str:
    """
    Safely removes HTML tags from a string using the built-in HTMLParser.
    """
    if not html_text or not isinstance(html_text, str):
        return html_text
    s = MLStripper()
    s.feed(html_text)
    return s.get_data()


# --- PHP Error Sanitizer (from main.py) ---
# This was also used in dev_tools.py
def sanitize_php_error(text_output: str) -> str:
    """
    A simple function to clean up PHP error output.
    Replaces long paths with "./" and removes server-specific paths.
    """
    if not text_output:
        return ""
    
    # Placeholder for USER_BOTS_ROOT_DIR, which will come from bot.handlers.files
    # For now, a generic pattern will work.
    sanitized_text = re.sub(r'/app/user_bots/\d+/', './', text_output)
    
    # This specific replacement requires USER_BOTS_ROOT_DIR.
    # We will need to inject this or import it once files.py is properly loaded
    # For now, let's keep a generic replacement example.
    # sanitized_text = sanitized_text.replace(os.path.abspath(USER_BOTS_ROOT_DIR) + os.path.sep, './')
    
    return sanitized_text.strip()


# --- Smart Split for long messages (from main.py) ---
def smart_split_simple(text: str, chunk_size: int = 1500) -> List[str]:
    """
    Splits a long text into chunks, trying to preserve whole lines,
    suitable for Telegram messages.
    """
    if not text: return [""]
    chunks = []
    current_chunk = ""
    for line in text.splitlines(keepends=True):
        if len(current_chunk) + len(line) > chunk_size:
            chunks.append(current_chunk)
            current_chunk = line
        else:
            current_chunk += line  
    if current_chunk:
        chunks.append(current_chunk)
    return chunks


# --- Diff Formatter with Line Numbers (from main.py) ---
def format_diff_with_line_numbers(diff_lines: List[str]) -> str:
    """
    Formats a list of diff lines (unified diff format) into a more readable string
    with line numbers, suitable for Telegram display.
    """
    formatted_output = []
    old_ln = 0
    new_ln = 0
    hunk_started = False
    for line in diff_lines:
        if line.startswith('---') or line.startswith('+++'):
            continue
        if line.startswith('@@'):
            match = re.match(r'^@@ -(\d+)(?:,\d+)? \+(\d+)(?:,\d+)? @@', line)
            if match:
                old_ln = int(match.group(1))
                new_ln = int(match.group(2))
                if hunk_started:
                    formatted_output.append("\n. . .\n")
                hunk_started = True
            continue
        if line.startswith('-'):
            formatted_output.append(f"\u200E- {old_ln:<4} : {line[1:]}")
            old_ln += 1
            
        elif line.startswith('+'):
            formatted_output.append(f"\u200E+ {new_ln:<4} : {line[1:]}")
            new_ln += 1
            
        elif line.startswith(' '):
            formatted_output.append(f"\u200E  {new_ln:<4} : {line[1:]}")
            old_ln += 1
            new_ln += 1

    return "\n".join(formatted_output)

# --- Diff Pagination Buttons (from main.py) ---
def build_pagination_buttons(current_page: int, total_pages: int, hash_key: str, file_name: str, is_correction: bool = True) -> List[List[Button]]:
    """
    Builds pagination buttons for diff views (AI corrections/modifications).
    """
    buttons = [] 
    
    # --- Row 1: Previous/Next ---
    first_nav_row = []
    if total_pages > 1:
        if current_page > 1:
            first_nav_row.append(Button.inline("🔙 السابق", data=f"ai_diff_page:{hash_key}:{current_page-1}"))
        if current_page < total_pages:
            first_nav_row.append(Button.inline("التالي 🔜", data=f"ai_diff_page:{hash_key}:{current_page+1}"))
    if first_nav_row:
        buttons.append(first_nav_row)

    # --- Subsequent Rows: Page Numbers (4 per row) ---
    if total_pages > 1:
        page_buttons = []
        BUTTONS_PER_ROW = 4
        for num in range(1, total_pages + 1):
            if num == current_page:
                page_buttons.append(Button.inline(f"< {num} >", data="noop"))
            else:
                page_buttons.append(Button.inline(str(num), data=f"ai_diff_page:{hash_key}:{num}"))
        
        for i in range(0, len(page_buttons), BUTTONS_PER_ROW):
            row = page_buttons[i:i+BUTTONS_PER_ROW]
            buttons.append(row)

    # --- Last Row: Confirm/Cancel ---
    confirm_row = [Button.inline("❌ إلغاء", data=f"ai_cancel_correct:{file_name}")]
    if current_page == total_pages and is_correction: # Only show confirm on last page of correction
        confirm_row.insert(0, Button.inline("✅ نعم، قم بالتنفيذ", data=f"ai_confirm_correct:{hash_key}"))
    
    buttons.append(confirm_row)
    return buttons

# --- Recursive Tree View (Moved from uploads.py) ---
def generate_recursive_tree_view(path: str, prefix: str = "") -> str:
    """Generates a full, recursive tree view for a given path."""
    tree_string = ""
    try:
        items = sorted(os.listdir(path))
    except FileNotFoundError:
        return " (المجلد الرئيسي غير موجود) "

    all_items = [item for item in items]
    for i, item in enumerate(all_items):
        is_last = (i == len(all_items) - 1)
        connector = "└── " if is_last else "├── "
        item_path = os.path.join(path, item)
        
        if os.path.isdir(item_path):
            tree_string += f"{prefix}{connector}{item}/\n"
            new_prefix = prefix + ("    " if is_last else "│   ")
            tree_string += generate_recursive_tree_view(item_path, new_prefix)
        else:
            tree_string += f"{prefix}{connector}{item}\n"
            
    return tree_string

print("✅ Text utilities module initialized.")
