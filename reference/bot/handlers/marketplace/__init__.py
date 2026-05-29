# bot/handlers/marketplace/__init__.py
# Marketplace handlers initialization

def setup(client):
    """Setup function called by the loader."""
    from . import browse, upload, download, reviews, manage
    
    browse.setup(client)
    upload.setup(client)
    download.setup(client)
    reviews.setup(client)
    manage.setup(client)
    
    print("✅ Marketplace handlers loaded.")
