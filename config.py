import os

class Config:
    # Temel konfigürasyon
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'gizli-anahtar-buraya'
    
    # Veritabanı konfigürasyonu
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DB_DIR = os.path.join(BASE_DIR, 'data')
    if not os.path.exists(DB_DIR):
        os.makedirs(DB_DIR)
    
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(DB_DIR, 'site.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False 