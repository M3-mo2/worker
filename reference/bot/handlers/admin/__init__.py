# bot_v2/bot/handlers/admin/__init__.py
# This __init__.py file is responsible for aggregating and setting up
# all admin-related handlers within the 'admin' sub-package.

from . import main
from . import users
from . import broadcast
from . import subscriptions
from . import settings
from . import fsub
from . import stats
from . import giveaways
from . import points
from . import marketplace_admin
from . import marketplace_products
from . import marketplace_users
from . import marketplace_reports
from . import marketplace_stats
from . import marketplace_categories
from . import marketplace_advanced
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from telethon import TelegramClient

def setup(client: "TelegramClient"):
    """
    Sets up all admin-related handlers and sub-handlers by calling their
    respective setup functions.
    """
    main.setup(client)
    users.setup(client)
    broadcast.setup(client)
    subscriptions.setup(client)
    settings.setup(client)
    fsub.setup(client)
    stats.setup(client)
    giveaways.setup(client)
    points.setup(client)
    marketplace_admin.setup(client)
    marketplace_products.setup(client)
    marketplace_users.setup(client)
    marketplace_reports.setup(client)
    marketplace_stats.setup(client)
    marketplace_categories.setup(client)
    marketplace_advanced.setup(client)
    print("✅ Admin handlers package setup complete.")
