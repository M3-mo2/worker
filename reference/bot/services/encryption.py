# bot_v2/bot/services/encryption.py
# Encapsulates encryption and decryption logic, primarily for web editor file paths.

import os
from cryptography.fernet import Fernet, InvalidToken
from typing import Optional, Union

# --- Encryption Key Management ---
# The encryption.key file is expected to be in the root of the bot_v2 project
ENCRYPTION_KEY_FILE = 'encryption.key'
_cipher_suite: Optional[Fernet] = None

def _initialize_cipher_suite():
    global _cipher_suite
    if _cipher_suite is None:
        try:
            # Look for encryption.key in the current working directory of the bot_v2 application
            # During refactoring, this will be in the `bot_v2` root.
            key_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', ENCRYPTION_KEY_FILE)
            if not os.path.exists(key_path):
                # Fallback to current script directory in case of different execution context
                key_path = os.path.join(os.getcwd(), ENCRYPTION_KEY_FILE)
            
            with open(key_path, 'rb') as key_file:
                ENCRYPTION_KEY = key_file.read()
            _cipher_suite = Fernet(ENCRYPTION_KEY)
            print("✅ Encryption Service: Encryption key loaded successfully.")
        except FileNotFoundError:
            print("⚠️ encryption.key not found. Generating a new one...")
            try:
                new_key = Fernet.generate_key()
                with open(key_path, 'wb') as key_file:
                    key_file.write(new_key)
                _cipher_suite = Fernet(new_key)
                print("✅ Encryption Service: New encryption key generated and loaded.")
            except Exception as e:
                print(f"CRITICAL: Failed to generate encryption key: {e}")
                _cipher_suite = None
        except Exception as e:
            print(f"CRITICAL: Error loading encryption key: {e}. WebApp editor will not function correctly.")
            _cipher_suite = None

def get_cipher_suite() -> Optional[Fernet]:
    if _cipher_suite is None:
        _initialize_cipher_suite()
    return _cipher_suite


def encrypt_path(path: str) -> Optional[str]:
    """Encrypts a file path string."""
    cipher = get_cipher_suite()
    if cipher:
        try:
            return cipher.encrypt(path.encode('utf-8')).decode('utf-8')
        except Exception as e:
            print(f"Encryption failed for path '{path}': {e}")
            return None
    return None

def decrypt_path(encrypted_path: str) -> Optional[str]:
    """Decrypts an encrypted file path string."""
    cipher = get_cipher_suite()
    if cipher:
        try:
            return cipher.decrypt(encrypted_path.encode('utf-8')).decode('utf-8')
        except InvalidToken:
            print(f"Decryption failed: Invalid token for path '{encrypted_path}'")
            return None
        except Exception as e:
            print(f"Decryption failed for path '{encrypted_path}': {e}")
            return None
    return None

# Initialize on module load
_initialize_cipher_suite()

print("✅ Encryption Service module initialized.")
