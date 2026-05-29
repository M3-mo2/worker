# bot_v2/bot/services/billing_service.py
# Centralized service for managing user subscriptions, plans, and related tiers.

from typing import Dict, Any, Tuple, Optional
from datetime import datetime
import time # For time.time() if _TZ is not available

from bot.core.data_manager import load_all_users, save_all_users, load_bots_data, save_bots_data
from bot.utils.time import _now_ts, _TZ # Import time utilities

def update_user_bot_tiers(user_id_str: str, new_tier: str):
    """
    Updates the 'tier' for all bots owned by a user in bots.json.
    This ensures the webhook dispatcher uses the correct tier.
    """
    try:
        user_id_int = int(user_id_str)
    except ValueError:
        print(f"[Tier Update] Invalid user_id_str: {user_id_str}")
        return

    print(f"[Tier Update] Setting tier for user {user_id_int} to {new_tier}")
    bots_data = load_bots_data()
    updated = False
    
    for token, info in bots_data.items():
        if info.get('owner') == user_id_int:
            if info.get('tier') != new_tier:
                info['tier'] = new_tier
                updated = True
    
    if updated:
        save_bots_data(bots_data)
        print(f"[Tier Update] bots.json saved for user {user_id_int}.")
    else:
        print(f"[Tier Update] No bots found or no update needed for user {user_id_int}.")


def check_subscription_expiry(user_id_str: str, user_data: Dict[str, Any], current_time: Optional[int] = None) -> Tuple[bool, Dict[str, Any]]:
    """
    Checks if a user's 'pro' plan has expired.
    If yes, demotes them and cleans up flags.
    Returns (bool: was_demoted, dict: updated_user_data)
    
    NOTE: Does NOT demote top developers (plan_source = 'top_developer')
    """
    if user_data.get('plan') == 'pro':
        # Skip expiry check for top developers
        if user_data.get('plan_source') == 'top_developer':
            return False, user_data
        
        expiry_ts = user_data.get('plan_expiry')
        
        now = current_time if current_time is not None else _now_ts()
        
        if expiry_ts and now > expiry_ts:
            print(f"[Expiry] User {user_id_str} subscription expired.")
            user_data['plan'] = 'free'
            user_data.pop('plan_expiry', None)
            user_data.pop('expiry_warning_sent', None) 
            
            try:
                # Use the local update_user_bot_tiers function in this service
                update_user_bot_tiers(user_id_str, 'free')
            except Exception as e:
                print(f"[Expiry] CRITICAL: Failed to update bots.json for {user_id_str}: {e}")
                
            return True, user_data
    
    return False, user_data


def grant_top_developer_pro(user_id_str: str, rank: int) -> Dict[str, Any]:
    """
    Grant PRO to top developer with special flag.
    This PRO never expires unless they leave top 3.
    """
    print(f"[TopDev] Granting PRO to user {user_id_str} (rank {rank})")
    
    all_users = load_all_users()
    user_data = all_users.get(user_id_str, {})
    
    # Set PRO with special flag
    user_data['plan'] = 'pro'
    user_data['plan_source'] = 'top_developer'
    user_data['top_developer_rank'] = rank
    user_data['plan_expiry'] = None  # No expiry for top devs
    user_data.pop('expiry_warning_sent', None)  # Clear any warnings
    
    all_users[user_id_str] = user_data
    save_all_users(all_users)
    
    # Update bots tier
    update_user_bot_tiers(user_id_str, 'pro')
    
    print(f"[TopDev] PRO granted to {user_id_str}")
    return user_data


def revoke_top_developer_pro(user_id_str: str) -> Dict[str, Any]:
    """
    Revoke PRO from ex-top developer.
    Only revokes if the PRO source is 'top_developer'.
    """
    print(f"[TopDev] Revoking PRO from user {user_id_str}")
    
    all_users = load_all_users()
    user_data = all_users.get(user_id_str, {})
    
    # Only revoke if source is top_developer
    if user_data.get('plan_source') == 'top_developer':
        user_data['plan'] = 'free'
        user_data.pop('plan_source', None)
        user_data.pop('top_developer_rank', None)
        user_data.pop('plan_expiry', None)
        
        all_users[user_id_str] = user_data
        save_all_users(all_users)
        
        # Update bots tier
        update_user_bot_tiers(user_id_str, 'free')
        
        print(f"[TopDev] PRO revoked from {user_id_str}")
    else:
        print(f"[TopDev] User {user_id_str} has PRO from another source, not revoking")
    
    return user_data

print("✅ Billing Service initialized.")
