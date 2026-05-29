# bot_v2/bot/utils/backup.py
import os
import zipfile

def create_backup_zip(source_dir, output_filename):
    """
    Compresses the source_dir into a zip file.
    The zip file will contain the source_dir as the root folder.
    Excludes .git, __pycache__, .pyc, .log, and the output file itself.
    """
    with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        parent_dir = os.path.dirname(source_dir)
        for root, dirs, files in os.walk(source_dir):
            # Exclude common junk directories
            if any(junk in root.split(os.path.sep) for junk in ['__pycache__', '.git', '.idea', '.vscode', 'node_modules', '.next']):
                continue
            
            for file in files:
                # Don't zip the zip file itself if it's being created inside the source dir
                if file == os.path.basename(output_filename): 
                    continue
                # Exclude temporary and compiled files
                if file.endswith('.pyc') or file.endswith('.log') or file.endswith('.tmp'):
                    continue
                    
                file_path = os.path.join(root, file)
                # Create arcname such that the source_dir is the top level folder in zip
                # e.g., if source is /root/bot_v2, file is /root/bot_v2/main.py
                # arcname becomes bot_v2/main.py
                arcname = os.path.relpath(file_path, parent_dir)
                zipf.write(file_path, arcname)
