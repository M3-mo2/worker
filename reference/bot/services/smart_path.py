import os
from bot.core.data_manager import load_bots_data
from bot.services.file_service import get_current_path, USER_BOTS_ROOT_DIR

def resolve_file_path(user_id: int, file_name: str) -> str:
    """
    Smartly resolves the absolute path of a file for a given user.
    
    Strategy:
    1. Check if 'file_name' corresponds to a registered bot in bots.json owned by user_id.
       - If found, return that specific path (fixing the issue of changing directories).
    2. If not found or ambiguous, fall back to the user's current working directory.
    """
    bots_data = load_bots_data()
    
    # Search for matches in bots.json
    matches = []
    for token, info in bots_data.items():
        if info.get('owner') == user_id:
            rel_path = info.get('path', '')
            # Check if the filename matches
            if os.path.basename(rel_path) == file_name:
                full_path = os.path.join(USER_BOTS_ROOT_DIR, rel_path)
                matches.append(full_path)
    
    if matches:
        # If we have matches, we prioritize them.
        
        # Case A: Only one bot has this filename. Perfect.
        if len(matches) == 1:
            return matches[0]
        
        # Case B: Multiple bots have this filename (e.g. bot1/run.php, bot2/run.php).
        # We try to see if one of them is in the current directory (context aware).
        current_path = get_current_path(user_id)
        for path in matches:
            if os.path.dirname(path) == current_path:
                return path
        
        # Case C: Multiple matches, none in current dir.
        # We return the first one found (or maybe the running one?).
        # Let's prioritize running bots.
        for path in matches:
            # Find the token for this path to check status
            for token, info in bots_data.items():
                if os.path.join(USER_BOTS_ROOT_DIR, info.get('path', '')) == path:
                    if info.get('status') == 'running':
                        return path
        
        return matches[0]

    # 3. Fallback: Use Current Working Directory
    current_path = get_current_path(user_id)
    return os.path.join(current_path, file_name)