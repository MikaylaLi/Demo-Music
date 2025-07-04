import os
from datetime import timedelta

class Config:
    # Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'majorchord_secret_key_2024'
    DEBUG = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    
    # Database Configuration
    DATABASE = 'majorchord.db'
    
    # API Configuration
    API_TITLE = 'MajorChord API'
    API_VERSION = 'v1.0'
    API_DESCRIPTION = 'AI-powered music recommendations based on health and wellness'
    
    # Session Configuration
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    
    # CORS Configuration
    CORS_ORIGINS = [
        'http://localhost:3000',
        'http://localhost:5000',
        'http://127.0.0.1:5000',
        'http://127.0.0.1:3000'
    ]
    
    # Music Recommendation Settings
    MAX_RECOMMENDATIONS = 20
    DEFAULT_RECOMMENDATIONS = 10
    
    # Health Tracking Settings
    HEALTH_METRICS = [
        'stress_level',
        'sleep_quality', 
        'mood_score',
        'energy_level'
    ]
    
    # Music Categories
    MOODS = [
        'calm', 'energetic', 'focused', 'joyful', 'peaceful',
        'serene', 'upbeat', 'cheerful', 'contemplative', 'soothing',
        'relaxing', 'tranquil', 'bright', 'exciting', 'mellow',
        'neutral', 'concentrated', 'uplifting', 'bright', 'tranquil'
    ]
    
    GENRES = [
        'Ambient', 'Classical', 'Piano', 'Rock', 'Pop',
        'Lo-Fi', 'Electronic', 'Nature', 'Sleep Music'
    ]

class DevelopmentConfig(Config):
    DEBUG = True
    
class ProductionConfig(Config):
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    
class TestingConfig(Config):
    TESTING = True
    DATABASE = 'test_majorchord.db'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
} 