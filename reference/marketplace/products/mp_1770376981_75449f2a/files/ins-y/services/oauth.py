import asyncio
from pytubefix.innertube import InnerTube


class OAuthManager:
    def __init__(self):
        self.authenticated = False
    
    def verify(self):
        try:
            print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            print("🔐 YouTube OAuth Authentication Required")
            print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
            innertube = InnerTube(
                client='TV',
                use_oauth=True,
                allow_cache=True
            )
            
            if not innertube.access_token:
                innertube.fetch_bearer_token()
            
            self.authenticated = True
            print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
            print("✓ Authentication successful")
            print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
            return True
            
        except Exception as e:
            print(f"\n✗ Authentication failed: {e}")
            return False


oauth_manager = OAuthManager()
