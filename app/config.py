import os
from pathlib import Path

class Config:
    # Temel dizin yapısı
    BASE_DIR = Path(__file__).resolve().parent.parent
    DB_DIR = BASE_DIR / 'data'
    
    # Veritabanı dizinini oluştur
    DB_DIR.mkdir(exist_ok=True)
    
    # SQLAlchemy ayarları
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DB_DIR}/site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Flask-WTF ayarları
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    
    # Uygulama ayarları
    DEBUG = True
    PORT = 5002 