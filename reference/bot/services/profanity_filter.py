# bot/services/profanity_filter.py
# Advanced profanity filter with 3-level punishment system

import re
from typing import Tuple, Optional
from bot.core import database

# Severity levels
SEVERITY_CRITICAL = 3  # Permanent ban from marketplace
SEVERITY_HIGH = 2      # 3-day ban from comments and uploads
SEVERITY_LOW = 1       # Warning (3 strikes = 4-day ban)

# Profanity dictionary with severity levels
PROFANITY_DICT = {
    # CRITICAL - Permanent marketplace ban
    'critical': [
        # Sexual explicit
        'كس', 'نيك', 'ينيك', 'متناك', 'متناكة', 'منيوك', 'منيوكة', 'متنوك',
        'fuck', 'fucking', 'fucked', 'fucker', 'motherfucker', 'motherfucking',
        'cock', 'cocksucking', 'pussy', 'cunt', 'twat',
        
        # Extreme insults
        'ابن المتناكة', 'ابن الشرموطة', 'شرموطة', 'شرماط', 'قحبة', 'عاهرة',
        'whore', 'slut', 'bitch', 'bitches',
        
        # Religious/ethnic slurs
        'خنزير', 'خنازير', 'كافر', 'ملعون', 'ملعونة',
    ],
    
    # HIGH - 3-day ban
    'high': [
        # Strong insults
        'حمار', 'حمير', 'كلب', 'كلاب', 'ديوث', 'خول', 'مخول',
        'غبي', 'غبية', 'أحمق', 'بليد', 'جاهل', 'جاهلة',
        'حقير', 'خسيس', 'نذل', 'نذلة', 'وضيع', 'وضيعة',
        'asshole', 'bastard', 'dickhead', 'dumbass', 'jackass',
        'shit', 'shitty', 'bullshit', 'horseshit', 'dipshit',
        'damn', 'damned', 'dammit', 'crap', 'crappy',
        
        # Offensive terms
        'زق', 'شق', 'مصلع', 'محقق', 'سفيه', 'شيص', 'بطيخ',
        'متورة', 'بصخ', 'منجل', 'فاجر', 'بصيخ', 'بير', 'قحبي', 'شرموط',
        'wanker', 'dickwad', 'fuckwit', 'asshat', 'asswipe',
    ],
    
    # LOW - Warning (3 strikes)
    'low': [
        # Mild insults
        'بلاهة', 'مقرف', 'حقود', 'حاقد', 'طامع', 'طامعة', 'جشع', 'جشعة',
        'غادر', 'غادرة', 'خائن', 'خائنة', 'منافق', 'منافقة', 'فاسق', 'فاسقة',
        'قبيح', 'قبيحة', 'وسخ', 'وسخة', 'مسخ', 'مشوه',
        'piss', 'pissed', 'sucks', 'lame',
        'stupid', 'idiot', 'moron',
    ]
}

# Whitelist - Safe words that might trigger false positives
WHITELIST = [
    # Arabic safe words
    'شرح', 'شارح', 'شروح', 'تشريح', 'شرحت', 'يشرح', 'نشرح',
    'بختصار', 'اختصار', 'مختصر', 'تختصر',
    'تفاصيل', 'تفصيل', 'مفصل', 'بالتفصيل',
    'ملف', 'ملفات', 'الملف',
    'مكتبه', 'مكتبة', 'المكتبه',
    'تسجيل', 'سجل', 'مسجل',
    'دخول', 'الدخول', 'تدخل',
    'تحميل', 'تحمل', 'محمل', 'التحميل',
    'بلاي', 'ليست', 'فيديو', 'لينك',
    
    # English safe words
    'click', 'dick', 'pick', 'stick', 'trick', 'thick',  # Common words with 'ick'
    'class', 'glass', 'pass', 'mass', 'grass',  # Common words with 'ass'
    'hello', 'hell', 'shell', 'bell', 'well',  # Common words with 'hell'
    'assessment', 'classic', 'cassette',
]

# Compile regex patterns for each severity
PATTERNS = {}
for severity, words in PROFANITY_DICT.items():
    # Escape special chars
    escaped = [re.escape(word) for word in words]
    
    # Match whole words with word boundaries
    pattern = r'\b(' + '|'.join(escaped) + r')\b'
    
    # Also catch common obfuscation patterns (but more carefully)
    # Only for single-word profanity, not phrases
    obfuscated_patterns = []
    for word in words:
        if ' ' not in word:  # Skip phrases like "shut up"
            # Match variations like: f*ck, f.u.c.k, f_u_c_k, f-u-c-k
            chars = list(re.escape(word))
            obfuscated = chars[0] + r'[\*\.\s_-]+'.join(chars[1:])
            obfuscated_patterns.append(obfuscated)
    
    if obfuscated_patterns:
        pattern += r'|' + r'|'.join(obfuscated_patterns)
    
    PATTERNS[severity] = re.compile(pattern, re.IGNORECASE | re.UNICODE)


async def check_profanity(text: str, user_id: int) -> Tuple[bool, Optional[str], int]:
    """
    Check text for profanity and return (is_clean, reason, severity).
    
    Returns:
        (True, None, 0) if clean
        (False, reason, severity) if profanity found
    """
    if not text:
        return True, None, 0
    
    # Normalize text (remove extra spaces, convert to lowercase)
    normalized = ' '.join(text.lower().split())
    
    # Check whitelist first - if any whitelisted word is found, skip that word
    for safe_word in WHITELIST:
        normalized = normalized.replace(safe_word.lower(), '')
    
    # Check critical words first
    match = PATTERNS['critical'].search(normalized)
    if match:
        await apply_critical_punishment(user_id)
        return False, "🚫 تم اكتشاف محتوى غير لائق للغاية. تم حظرك نهائياً من الماركت.", SEVERITY_CRITICAL
    
    # Check high severity
    match = PATTERNS['high'].search(normalized)
    if match:
        await apply_high_punishment(user_id)
        return False, "⚠️ تم اكتشاف محتوى مسيء. تم حظرك من التعليقات والرفع لمدة 3 أيام.", SEVERITY_HIGH
    
    # Check low severity
    match = PATTERNS['low'].search(normalized)
    if match:
        warnings = await increment_user_warnings(user_id)
        if warnings >= 3:
            await apply_low_punishment(user_id)
            return False, "⚠️ تجاوزت الحد المسموح من التحذيرات. تم حظرك من التعليقات لمدة 4 أيام.", SEVERITY_LOW
        else:
            return False, f"⚠️ تحذير ({warnings}/3): يرجى استخدام لغة محترمة.", SEVERITY_LOW
    
    return True, None, 0


async def apply_critical_punishment(user_id: int):
    """Permanent marketplace ban - nuclear option."""
    import time
    
    # Set permanent ban (100 years)
    ban_until = int(time.time()) + (100 * 365 * 24 * 60 * 60)
    
    async with database.aiosqlite.connect(database.DB_NAME, timeout=30) as db:
        # Create ban record
        await db.execute('''
            INSERT OR REPLACE INTO marketplace_bans 
            (user_id, ban_type, banned_until, reason, created_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, 'permanent', ban_until, 'محتوى غير لائق', int(time.time())))
        
        # Delete all user products
        await db.execute('DELETE FROM marketplace_products WHERE owner_id = ?', (user_id,))
        
        # Delete all user comments
        await db.execute('DELETE FROM marketplace_comments WHERE user_id = ?', (user_id,))
        
        # Delete all user reviews
        await db.execute('DELETE FROM marketplace_reviews WHERE user_id = ?', (user_id,))
        
        await db.commit()


async def apply_high_punishment(user_id: int):
    """3-day ban from comments and uploads."""
    import time
    
    ban_until = int(time.time()) + (3 * 24 * 60 * 60)  # 3 days
    
    async with database.aiosqlite.connect(database.DB_NAME, timeout=30) as db:
        await db.execute('''
            INSERT OR REPLACE INTO marketplace_bans 
            (user_id, ban_type, banned_until, reason, created_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, 'comment_upload', ban_until, 'محتوى مسيء', int(time.time())))
        await db.commit()


async def apply_low_punishment(user_id: int):
    """4-day ban from comments after 3 warnings."""
    import time
    
    ban_until = int(time.time()) + (4 * 24 * 60 * 60)  # 4 days
    
    async with database.aiosqlite.connect(database.DB_NAME, timeout=30) as db:
        await db.execute('''
            INSERT OR REPLACE INTO marketplace_bans 
            (user_id, ban_type, banned_until, reason, created_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, 'comment', ban_until, 'تجاوز التحذيرات', int(time.time())))
        
        # Reset warnings
        await db.execute('DELETE FROM marketplace_warnings WHERE user_id = ?', (user_id,))
        await db.commit()


async def increment_user_warnings(user_id: int) -> int:
    """Increment user warning count and return total."""
    import time
    
    async with database.aiosqlite.connect(database.DB_NAME, timeout=30) as db:
        # Get current warnings
        async with db.execute(
            'SELECT warning_count FROM marketplace_warnings WHERE user_id = ?',
            (user_id,)
        ) as cursor:
            row = await cursor.fetchone()
        
        if row:
            new_count = row[0] + 1
            await db.execute(
                'UPDATE marketplace_warnings SET warning_count = ?, last_warning_at = ? WHERE user_id = ?',
                (new_count, int(time.time()), user_id)
            )
        else:
            new_count = 1
            await db.execute(
                'INSERT INTO marketplace_warnings (user_id, warning_count, last_warning_at) VALUES (?, ?, ?)',
                (user_id, new_count, int(time.time()))
            )
        
        await db.commit()
        return new_count


async def check_user_ban(user_id: int, action: str = 'any') -> Tuple[bool, Optional[str]]:
    """
    Check if user is banned from specific action.
    
    Args:
        user_id: User ID
        action: 'comment', 'upload', 'any'
    
    Returns:
        (is_banned, reason)
    """
    import time
    
    async with database.aiosqlite.connect(database.DB_NAME, timeout=30) as db:
        db.row_factory = database.aiosqlite.Row
        
        async with db.execute('''
            SELECT ban_type, banned_until, reason 
            FROM marketplace_bans 
            WHERE user_id = ? AND banned_until > ?
        ''', (user_id, int(time.time()))) as cursor:
            row = await cursor.fetchone()
        
        if not row:
            return False, None
        
        ban_type = row['ban_type']
        
        # Permanent ban blocks everything
        if ban_type == 'permanent':
            return True, "🚫 أنت محظور نهائياً من الماركت بسبب محتوى غير لائق."
        
        # Comment+Upload ban
        if ban_type == 'comment_upload' and action in ['comment', 'upload', 'any']:
            days_left = (row['banned_until'] - int(time.time())) // (24 * 60 * 60) + 1
            return True, f"⚠️ أنت محظور من التعليقات والرفع لمدة {days_left} يوم بسبب محتوى مسيء."
        
        # Comment-only ban
        if ban_type == 'comment' and action in ['comment', 'any']:
            days_left = (row['banned_until'] - int(time.time())) // (24 * 60 * 60) + 1
            return True, f"⚠️ أنت محظور من التعليقات لمدة {days_left} يوم."
        
        return False, None


async def clean_expired_bans():
    """Clean up expired bans (run periodically)."""
    import time
    
    async with database.aiosqlite.connect(database.DB_NAME, timeout=30) as db:
        await db.execute('DELETE FROM marketplace_bans WHERE banned_until <= ?', (int(time.time()),))
        await db.commit()


async def unban_user(user_id: int) -> bool:
    """
    Unban a user (admin function).
    Returns True if user was unbanned, False if not banned.
    """
    async with database.aiosqlite.connect(database.DB_NAME, timeout=30) as db:
        # Check if user is banned
        async with db.execute('SELECT user_id FROM marketplace_bans WHERE user_id = ?', (user_id,)) as cursor:
            row = await cursor.fetchone()
        
        if not row:
            return False
        
        # Remove ban
        await db.execute('DELETE FROM marketplace_bans WHERE user_id = ?', (user_id,))
        
        # Reset warnings
        await db.execute('DELETE FROM marketplace_warnings WHERE user_id = ?', (user_id,))
        
        await db.commit()
        return True


async def get_user_ban_info(user_id: int) -> dict:
    """Get detailed ban information for a user."""
    import time
    
    async with database.aiosqlite.connect(database.DB_NAME, timeout=30) as db:
        database.aiosqlite.Row
        
        async with db.execute('''
            SELECT ban_type, banned_until, reason, created_at
            FROM marketplace_bans 
            WHERE user_id = ?
        ''', (user_id,)) as cursor:
            row = await cursor.fetchone()
        
        if not row:
            return None
        
        return {
            'ban_type': row[0],
            'banned_until': row[1],
            'reason': row[2],
            'created_at': row[3],
            'is_active': row[1] > int(time.time()),
            'days_left': max(0, (row[1] - int(time.time())) // (24 * 60 * 60))
        }
