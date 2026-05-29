"""
Marketplace Ranking Engine
نظام الخوارزميات المحسّن للماركت
"""

import time
from typing import Dict, Literal

# ═══════════════════════════════════════════════════════════════════
# الأوزان (Weights Configuration)
# ═══════════════════════════════════════════════════════════════════

WEIGHTS = {
    'balanced': {
        'downloads': 40,
        'rating': 35,        # زيادة من 30 إلى 35
        'views': 0.15,
        'comments': 5,       # تقليل من 10 إلى 5
        'recency': 5
    },
    'downloads': {
        'downloads': 70,
        'rating': 25,        # زيادة من 20 إلى 25
        'views': 0.05,
        'comments': 2,       # تقليل من 5 إلى 2
        'recency': 0
    },
    'rating': {
        'downloads': 20,
        'rating': 75,        # زيادة من 70 إلى 75
        'views': 0,
        'comments': 5,       # تقليل من 10 إلى 5
        'recency': 0
    },
    'newest': {
        'downloads': 10,
        'rating': 10,
        'views': 0,
        'comments': 0,
        'recency': 80
    }
}

# ═══════════════════════════════════════════════════════════════════
# الحدود (Thresholds)
# ═══════════════════════════════════════════════════════════════════

MIN_RATINGS_FOR_RANKING = 3
DEFAULT_RATING_PERCENTAGE = 60      # زيادة من 50 إلى 60 (أكثر إيجابية)
RECENCY_DECAY_DAYS = 100
DISLIKE_WEIGHT = 0.3                # الديسلايك يحسب بـ 30% فقط من وزنه

# ═══════════════════════════════════════════════════════════════════
# دوال الحساب (Calculation Functions)
# ═══════════════════════════════════════════════════════════════════

def calculate_rating_score(likes: int, dislikes: int, weight: float) -> float:
    """
    حساب نقاط التقييم مع تقليل تأثير الديسلايك.
    
    Args:
        likes: عدد الإعجابات
        dislikes: عدد عدم الإعجاب
        weight: الوزن المطلوب
    
    Returns:
        float: نقاط التقييم
    """
    # تقليل تأثير الديسلايك بضربه في 0.3
    weighted_dislikes = dislikes * DISLIKE_WEIGHT
    total_ratings = likes + weighted_dislikes
    
    if (likes + dislikes) >= MIN_RATINGS_FOR_RANKING:
        rating_percentage = (likes / total_ratings) * 100
    else:
        rating_percentage = DEFAULT_RATING_PERCENTAGE
    
    return rating_percentage * weight


def calculate_recency_score(created_at: int, weight: float) -> float:
    """
    حساب نقاط الحداثة.
    
    Args:
        created_at: timestamp النشر
        weight: الوزن المطلوب
    
    Returns:
        float: نقاط الحداثة
    """
    days_old = (time.time() - created_at) / 86400  # 86400 = 24*60*60
    recency_score = max(0, 100 - days_old)
    return recency_score * weight


def calculate_quality_score(
    downloads: int,
    likes: int,
    dislikes: int,
    views: int,
    comments: int,
    created_at: int,
    mode: Literal['balanced', 'downloads', 'rating', 'newest'] = 'balanced'
) -> float:
    """
    حساب النقاط الشاملة للمنتج.
    
    Args:
        downloads: عدد التحميلات
        likes: عدد الإعجابات
        dislikes: عدد عدم الإعجاب
        views: عدد المشاهدات
        comments: عدد التعليقات
        created_at: timestamp النشر
        mode: نوع الخوارزمية
    
    Returns:
        float: النقاط الشاملة
    """
    weights = WEIGHTS[mode]
    
    # Download points
    download_points = downloads * weights['downloads']
    
    # Rating points
    rating_points = calculate_rating_score(likes, dislikes, weights['rating'])
    
    # View points
    view_points = views * weights['views']
    
    # Comment points
    comment_points = comments * weights['comments']
    
    # Recency points
    recency_points = calculate_recency_score(created_at, weights['recency'])
    
    # Total
    return download_points + rating_points + view_points + comment_points + recency_points


# ═══════════════════════════════════════════════════════════════════
# SQL Query Builder
# ═══════════════════════════════════════════════════════════════════

def build_ranking_query(
    mode: Literal['balanced', 'downloads', 'rating', 'newest'] = 'balanced'
) -> str:
    """
    بناء استعلام SQL للترتيب حسب النوع.
    
    Args:
        mode: نوع الخوارزمية
    
    Returns:
        str: ORDER BY clause
    """
    weights = WEIGHTS[mode]
    
    # Rating calculation with reduced dislike impact
    rating_calc = f'''
        CASE 
            WHEN COUNT(r.user_id) >= {MIN_RATINGS_FOR_RANKING} THEN
                (CAST(COUNT(CASE WHEN r.rating = 2 THEN 1 END) AS FLOAT) / 
                 (COUNT(CASE WHEN r.rating = 2 THEN 1 END) + (COUNT(CASE WHEN r.rating = 1 THEN 1 END) * {DISLIKE_WEIGHT})) * 100 * {weights['rating']})
            ELSE ({DEFAULT_RATING_PERCENTAGE} * {weights['rating']})
        END
    '''
    
    # Recency calculation
    if weights['recency'] > 0:
        recency_calc = f'''
            (MAX(0, {RECENCY_DECAY_DAYS} - (strftime('%s', 'now') - p.created_at) / 86400) * {weights['recency']})
        '''
    else:
        recency_calc = '0'
    
    # Full quality score
    quality_score = f'''
        (
            (p.downloads * {weights['downloads']}) +
            {rating_calc} +
            (p.views * {weights['views']}) +
            (COUNT(DISTINCT c.comment_id) * {weights['comments']}) +
            {recency_calc}
        )
    '''
    
    return quality_score


def build_search_query(
    mode: Literal['balanced', 'downloads', 'rating', 'newest'] = 'balanced',
    category: str = None,
    search_term: str = None,
    status: str = 'active'
) -> tuple[str, list]:
    """
    بناء استعلام البحث الكامل.
    
    Args:
        mode: نوع الخوارزمية
        category: التصنيف (اختياري)
        search_term: كلمة البحث (اختياري)
        status: حالة المنتج
    
    Returns:
        tuple: (query, params)
    """
    # WHERE clause
    where_parts = [f"p.status = ?"]
    params = [status]
    
    if category:
        where_parts.append("p.category = ?")
        params.append(category)
    
    if search_term:
        where_parts.append("(p.title LIKE ? OR p.description LIKE ? OR p.tags LIKE ?)")
        search_pattern = f'%{search_term}%'
        params.extend([search_pattern, search_pattern, search_pattern])
    
    where_clause = " AND ".join(where_parts)
    
    # ORDER BY clause
    order_clause = build_ranking_query(mode)
    
    # Full query
    query = f'''
        SELECT 
            p.*,
            COUNT(CASE WHEN r.rating = 2 THEN 1 END) as likes,
            COUNT(CASE WHEN r.rating = 1 THEN 1 END) as dislikes,
            COUNT(DISTINCT c.comment_id) as comment_count,
            {order_clause} as quality_score
        FROM marketplace_products p
        LEFT JOIN marketplace_reviews r ON p.product_id = r.product_id
        LEFT JOIN marketplace_comments c ON p.product_id = c.product_id
        WHERE {where_clause}
        GROUP BY p.product_id
        ORDER BY quality_score DESC
        LIMIT ? OFFSET ?
    '''
    
    return query, params


# ═══════════════════════════════════════════════════════════════════
# Mapping للأسماء القديمة
# ═══════════════════════════════════════════════════════════════════

SORT_MODE_MAP = {
    'created_at': 'newest',
    'downloads': 'downloads',
    'rating': 'rating',
    'quality': 'balanced',
    'newest': 'newest'
}


def normalize_sort_mode(sort_by: str) -> str:
    """
    تحويل الأسماء القديمة للأسماء الجديدة.
    
    Args:
        sort_by: اسم الترتيب القديم
    
    Returns:
        str: اسم الترتيب الجديد
    """
    return SORT_MODE_MAP.get(sort_by, 'balanced')
