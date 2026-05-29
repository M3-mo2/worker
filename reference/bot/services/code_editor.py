import re
import os

class CodeEditor:
    """
    A service class to handle file manipulations in memory before saving.
    Used by the AI Agent to perform precise edits.
    """
    def __init__(self, file_path):
        """
        Initializes the CodeEditor by reading the file content into memory.
        """
        self.file_path = file_path
        self.lines = []
        self._load_file()

    def _load_file(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r', encoding='utf-8', errors='ignore') as f:
                self.lines = f.readlines()
        else:
            self.lines = []

    def get_content(self):
        return "".join(self.lines)

    def save(self, output_path=None):
        target_path = output_path or self.file_path
        try:
            with open(target_path, 'w', encoding='utf-8') as f:
                f.writelines(self.lines)
            try: os.chmod(target_path, 0o777)
            except: pass
            return {'status': 'success', 'path': target_path}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def read_lines(self, start_line, end_line):
        # Adjust for 0-based index
        start = max(0, start_line - 1)
        end = min(len(self.lines), end_line)
        
        numbered_lines = []
        for i in range(start, end):
            numbered_lines.append(f"{i + 1}: {self.lines[i]}")
        
        return "".join(numbered_lines)

    def search(self, pattern, is_regex=True, case_sensitive=False):
        """
        Searches for a pattern in the file content.
        """
        results = []
        flags = 0 if case_sensitive else re.IGNORECASE
        
        for i, line in enumerate(self.lines):
            line_num = i + 1
            match = False
            if is_regex:
                if re.search(pattern, line, flags):
                    match = True
            else:
                if case_sensitive:
                    if pattern in line: match = True
                else:
                    if pattern.lower() in line.lower(): match = True
            
            if match:
                results.append(f"{line_num}: {line.strip()}")
        
        if not results:
            return "No matches found."
        return "\n".join(results[:50]) # Limit results

    def replace_lines(self, start_line, end_line, new_content):
        """
        Replaces a block of lines with new content.
        """
        # Adjust for 0-based index
        start = max(0, start_line - 1)
        end = min(len(self.lines), end_line)
        
        # Prepare new lines
        new_lines_list = [line + '\n' for line in new_content.splitlines()]
        if new_content and not new_content.endswith('\n'):
             if new_lines_list: new_lines_list[-1] = new_lines_list[-1].rstrip('\n')

        # Replace slice
        self.lines[start:end] = new_lines_list
        return f"Replaced lines {start_line} to {end_line}."

    def insert_lines(self, at_line, new_content):
        """
        Inserts new content at a specific line number.
        """
        # Adjust for 0-based index
        idx = max(0, at_line - 1)
        
        new_lines_list = [line + '\n' for line in new_content.splitlines()]
        
        # Insert
        self.lines[idx:idx] = new_lines_list
        return f"Inserted content at line {at_line}."

    def delete_lines(self, start_line, end_line):
        """
        Deletes a block of lines.
        """
        # Adjust for 0-based index
        start = max(0, start_line - 1)
        end = min(len(self.lines), end_line)
        
        del self.lines[start:end]
        return f"Deleted lines {start_line} to {end_line}."
