import sys
from core.config import config
from core.bot import bot
from services.cleaner import cleaner
from services.oauth import oauth_manager

import handlers.commands
import handlers.messages
import handlers.video
import handlers.playlist
import handlers.callbacks


def main():
    try:
        config.validate()
        print("✓ Configuration validated")
        
        if not oauth_manager.verify():
            print("✗ OAuth authentication required to continue")
            sys.exit(1)
        
        cleaner.start()
        print("✓ File cleaner started")
        
        print("✓ Bot is running...")
        bot.infinity_polling(timeout=60, long_polling_timeout=60)
        
    except KeyboardInterrupt:
        print("\n✓ Bot stopped by user")
        cleaner.stop()
        sys.exit(0)
        
    except Exception as e:
        print(f"✗ Fatal error: {e}")
        cleaner.stop()
        sys.exit(1)


if __name__ == "__main__":
    main()
