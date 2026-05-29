# bot_v2/bot/utils/points.py
import json
import os

# تحديد مسار ملف البيانات
DATA_DIR = os.path.join(os.getcwd(), 'bot_v2', 'data')
POINTS_FILE = os.path.join(DATA_DIR, 'points.json')
COUPONS_FILE = os.path.join(DATA_DIR, 'coupons.json')

# تخزين مؤقت في الذاكرة (RAM) بدلاً من الملف
_PENDING_REFERRALS_CACHE = {}

def load_points_data():
    """Loads points settings and packages."""
    if not os.path.exists(POINTS_FILE):
        # الإعدادات الافتراضية كما طلبت
        return {
            "referral_reward": 1,
            "transfer_fee": 1,
            "packages": { # Added transfer_fee default
                "pkg_default": {"days": 10, "price": 10}
            }
        }
    try:
        with open(POINTS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # ضمان وجود الهيكل الأساسي
            if "packages" not in data: data["packages"] = {}
            if "referral_reward" not in data: data["referral_reward"] = 1
            if "transfer_fee" not in data: data["transfer_fee"] = 1
            return data
    except:
        return {"referral_reward": 1, "transfer_fee": 1, "packages": {}}

def save_points_data(data):
    """Saves points settings."""
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(POINTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def save_pending_referral(user_id, referrer_id):
    """Saves a referral temporarily in memory until the user subscribes."""
    _PENDING_REFERRALS_CACHE[str(user_id)] = int(referrer_id)

def get_pending_referral(user_id):
    """Retrieves the pending referral for a user from memory."""
    return _PENDING_REFERRALS_CACHE.get(str(user_id))

def clear_pending_referral(user_id):
    """Removes the pending referral entry from memory."""
    if str(user_id) in _PENDING_REFERRALS_CACHE:
        del _PENDING_REFERRALS_CACHE[str(user_id)]

def load_coupons():
    """Loads all coupon codes from the JSON file."""
    if not os.path.exists(COUPONS_FILE):
        return {}
    try:
        with open(COUPONS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}

def save_coupons(data):
    """Saves all coupon codes to the JSON file."""
    with open(COUPONS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
