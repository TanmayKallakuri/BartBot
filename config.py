"""
Configuration file for BARTBot
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG = os.getenv('FLASK_DEBUG', 'False') == 'True'
    
    # Twilio
    TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
    TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
    TWILIO_WHATSAPP_NUMBER = os.getenv('TWILIO_WHATSAPP_NUMBER')
    
    # BART API
    BART_API_KEY = os.getenv('BART_API_KEY', 'MW9S-E7SL-26DU-VV8V')
    BART_API_BASE_URL = 'https://api.bart.gov/api'
    
    # Google Maps
    GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')

    # OpenAI (for AI-powered message understanding)
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

    # Weather
    OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')
    OPENWEATHER_BASE_URL = 'https://api.openweathermap.org/data/2.5'
    
    # Twitter
    TWITTER_BEARER_TOKEN = os.getenv('TWITTER_BEARER_TOKEN')
    BART_TWITTER_HANDLE = 'SFBART'
    
    # Uber
    UBER_CLIENT_ID = os.getenv('UBER_CLIENT_ID')
    UBER_CLIENT_SECRET = os.getenv('UBER_CLIENT_SECRET')
    
    # Lyft
    LYFT_CLIENT_ID = os.getenv('LYFT_CLIENT_ID')
    LYFT_CLIENT_SECRET = os.getenv('LYFT_CLIENT_SECRET')
    
    # Database
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///bartbot.db')
    
    # Redis
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    
    # Bot Behavior
    MAX_DELAY_ALERT_MINUTES = 10  # Alert user for delays > 10 mins
    PATTERN_DETECTION_THRESHOLD = 4  # Suggest profile after 4 identical routes
    DEFAULT_SEARCH_RADIUS_KM = 2  # Search for stations within 2km
    QUIET_MODE_ENABLED = True
    
    # Cache TTL (Time To Live in seconds)
    BART_SCHEDULE_CACHE_TTL = 60  # 1 minute
    WEATHER_CACHE_TTL = 600  # 10 minutes
    STATION_INFO_CACHE_TTL = 86400  # 24 hours

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False

# Config dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
