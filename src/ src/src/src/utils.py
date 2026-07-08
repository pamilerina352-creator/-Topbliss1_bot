import logging
import random
import time
from datetime import datetime
from typing import Dict, Any, Optional
import requests

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Global statistics
user_stats = {}
total_items_sent = 0
bot_start_time = time.time()

def track_user(user_id: int, username: str = None):
    """Track user in statistics"""
    if user_id not in user_stats:
        user_stats[user_id] = {
            'items_received': 0,
            'first_seen': datetime.now(),
            'username': username or 'No username',
            'last_active': datetime.now()
        }
        logger.info(f"👤 New user: {user_id} ({username or 'No username'})")
    else:
        user_stats[user_id]['last_active'] = datetime.now()
        if username:
            user_stats[user_id]['username'] = username

def update_user_stats(user_id: int):
    """Update user statistics"""
    global total_items_sent
    if user_id in user_stats:
        user_stats[user_id]['items_received'] += 1
    total_items_sent += 1

def is_admin(user_id: int, admin_ids: list) -> bool:
    """Check if user is admin"""
    return user_id in admin_ids

def get_fallback_content(config) -> Dict[str, str]:
    """Get fallback content"""
    url = random.choice(config.FALLBACK_IMAGES)
    message = random.choice(config.INSPIRATIONAL_MESSAGES)
    return {
        'url': url,
        'title': message,
        'source': 'Topbliss Library',
        'id': str(int(datetime.now().timestamp()))
    }

async def get_random_content(config) -> Dict[str, str]:
    """Get random content from Unsplash or fallback"""
    # Try Unsplash API first
    if config.UNSPLASH_ACCESS_KEY:
        try:
            response = requests.get(
                'https://api.unsplash.com/photos/random',
                params={
                    'query': 'inspirational motivation nature',
                    'orientation': 'landscape',
                    'count': 1
                },
                headers={
                    'Authorization': f'Client-ID {config.UNSPLASH_ACCESS_KEY}'
                },
                timeout=5
            )
            response.raise_for_status()
            data = response.json()
            if data and 'urls' in data:
                return {
                    'url': data['urls']['regular'],
                    'title': data.get('alt_description', 'Inspirational Content'),
                    'source': 'Unsplash',
                    'id': data.get('id', str(int(datetime.now().timestamp())))
                }
        except Exception as e:
            logger.warning(f"⚠️ Unsplash API error: {e}")
    
    # Fallback to local content
    return get_fallback_content(config)

async def search_content(query: str, config) -> Optional[Dict[str, str]]:
    """Search for content by keyword"""
    if config.UNSPLASH_ACCESS_KEY and len(query) > 2:
        try:
            response = requests.get(
                'https://api.unsplash.com/photos/random',
                params={
                    'query': query,
                    'orientation': 'landscape',
                    'count': 1
                },
                headers={
                    'Authorization': f'Client-ID {config.UNSPLASH_ACCESS_KEY}'
                },
                timeout=5
            )
            response.raise_for_status()
            data = response.json()
            if data and 'urls' in data:
                return {
                    'url': data['urls']['regular'],
                    'title': data.get('alt_description', f'Content for "{query}"'),
                    'source': 'Unsplash',
                    'id': data.get('id', str(int(datetime.now().timestamp())))
                }
        except Exception as e:
            logger.warning(f"⚠️ Search error: {e}")
    
    return None

def get_uptime() -> str:
    """Get bot uptime"""
    uptime_seconds = int(time.time() - bot_start_time)
    hours = uptime_seconds // 3600
    minutes = (uptime_seconds % 3600) // 60
    seconds = uptime_seconds % 60
    return f"{hours}h {minutes}m {seconds}s"

def get_bot_stats() -> Dict[str, Any]:
    """Get bot statistics"""
    return {
        'total_users': len(user_stats),
        'total_items': total_items_sent,
        'uptime': get_uptime()
    }
