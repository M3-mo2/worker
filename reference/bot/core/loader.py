# bot_v2/bot/core/loader.py
import os
import sys
import importlib.util
import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from telethon import TelegramClient

# Setup logging for the loader
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO) # Set to INFO level
# Add a handler if not already present (e.g., from main app setup)
if not logger.handlers:
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

# Define the absolute path to the 'handlers' directory
# This assumes the loader.py is at bot_v2/bot/core/loader.py
HANDLERS_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'handlers'))

def load_all_handlers(client: "TelegramClient"):
    """
    Discovers and loads all handler modules from the 'handlers' directory
    and its subdirectories. Each module is expected to have a 'setup(client)' function.
    """
    logger.info(f"🚀 Loading handlers from: {HANDLERS_PATH}")

    # Temporarily add HANDLERS_PATH to sys.path to allow direct imports of sub-packages
    # This is crucial for importlib.util.spec_from_file_location to resolve module names correctly
    original_sys_path = sys.path[:] # Save original path
    sys.path.insert(0, HANDLERS_PATH)

    for root, _, files in os.walk(HANDLERS_PATH):
        for file_name in files:
            if file_name.endswith('.py') and not file_name.startswith('__'):
                # Construct the full path to the module
                module_full_path = os.path.join(root, file_name)

                # Determine the module name relative to HANDLERS_PATH
                # Example: HANDLERS_PATH/admin/main.py -> admin.main (if HANDLERS_PATH is in sys.path)
                relative_path_segment = os.path.relpath(root, HANDLERS_PATH)
                if relative_path_segment == '.':
                    package_path = ""
                else:
                    package_path = relative_path_segment.replace(os.sep, '.') + '.'

                module_name = package_path + file_name[:-3]

                try:
                    spec = importlib.util.spec_from_file_location(module_name, module_full_path)
                    if spec is None:
                        logger.warning(f"Could not get spec for module: {module_full_path}")
                        continue
                    
                    module = importlib.util.module_from_spec(spec)
                    # Add the module to sys.modules to prevent re-import issues
                    sys.modules[module_name] = module
                    spec.loader.exec_module(module)

                    if hasattr(module, 'setup') and callable(module.setup):
                        module.setup(client)
                        logger.info(f"✅ Loaded handler: {module_name}")
                    else:
                        if not module_name.endswith('.agent'): # Skip warning for Agent class file
                            logger.warning(f"⚠️ Handler module '{module_name}' has no 'setup(client)' function. Skipping setup.")

                except Exception as e:
                    logger.error(f"❌ Failed to load handler '{module_name}' from '{module_full_path}': {e}", exc_info=True)
    
    # Restore original sys.path
    sys.path = original_sys_path

print("✅ PluginLoader module initialized.")
