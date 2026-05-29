# bot_v2/bot/services/__init__.py
# This __init__.py file defines what is exposed by the 'services' package.

from . import billing_service
from . import code_editor
from . import php_engine
# Backward compatibility alias
from . import php_engine as docker
from . import encryption
from . import file_service
from . import telegram
from . import user_service

print("✅ Services package initialized.")
