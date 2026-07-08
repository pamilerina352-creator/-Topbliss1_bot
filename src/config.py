import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Bot configuration class for @Topbliss1_bot"""
    
    # Bot settings
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN is not set in environment variables")
    
    # Server settings
    PORT = int(os.getenv('PORT', 3000))
    ENVIRONMENT = os.getenv('ENVIRONMENT', 'production')
    
    # Admin settings
    ADMIN_IDS = []
    admin_ids_str = os.getenv('ADMIN_IDS', '')
    if admin_ids_str:
        ADMIN_IDS = [int(id.strip()) for id in admin_ids_str.split(',')]
    
    # API settings
    UNSPLASH_ACCESS_KEY = os.getenv('UNSPLASH_ACCESS_KEY', '')
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    # Bot info
    BOT_NAME = "Topbliss1Bot"
    BOT_USERNAME = "@Topbliss1_bot"
    BOT_VERSION = "1.0.0"
    
    # Fallback images (reliable image sources)
    FALLBACK_IMAGES = [
        'https://picsum.photos/seed/topbliss1/800/600',
        'https://picsum.photos/seed/topbliss2/800/600',
        'https://picsum.photos/seed/topbliss3/800/600',
        'https://picsum.photos/seed/topbliss4/800/600',
        'https://picsum.photos/seed/topbliss5/800/600',
        'https://picsum.photos/seed/topbliss6/800/600',
        'https://picsum.photos/seed/topbliss7/800/600',
        'https://picsum.photos/seed/topbliss8/800/600',
    ]
    
    # Inspirational messages
    INSPIRATIONAL_MESSAGES = [
        "✨ Believe in yourself!",
        "🌟 You are capable of amazing things!",
        "💪 Stay strong, keep going!",
        "🌈 Every day is a new beginning!",
        "⭐ You are enough!",
        "🌺 Embrace the journey!",
        "🎯 Focus on your goals!",
        "💫 You are unique and special!",
    ]

def get_config():
    """Get configuration"""
    return Config()
