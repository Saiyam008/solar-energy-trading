import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'solar-energy-trading-super-secure-key-2025-huggingface-deployment-fixed'
    DATA_DIR = 'data'
    
    # Session cookie configuration optimized for Hugging Face proxy
    SESSION_COOKIE_NAME = 'solar_session'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = None  # Allow cookies through proxy
    SESSION_COOKIE_SECURE = False  # HF handles HTTPS at proxy level
    SESSION_COOKIE_PATH = '/'
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    
    # Remember cookie settings
    REMEMBER_COOKIE_NAME = 'solar_remember'
    REMEMBER_COOKIE_DURATION = timedelta(days=7)
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_SAMESITE = None
    REMEMBER_COOKIE_SECURE = False
    
    # Trading parameters
    MIN_ORDER_SIZE = 1  # MW
    MAX_ORDER_SIZE = 1000  # MW
    TICK_SIZE = 0.01  # Minimum price increment in Rs
    
    # Market hours (IST)
    MARKET_OPEN_HOUR = 9
    MARKET_CLOSE_HOUR = 17
    
    # Government middleman rates
    GOVT_BUYING_RATE = 7.0  # Rs/MW
    GOVT_SELLING_RATE = 11.0  # Rs/MW
    
    # P2P trading rate range
    P2P_MIN_RATE = 7.0
    P2P_MAX_RATE = 11.0
