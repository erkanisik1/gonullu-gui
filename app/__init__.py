from flask import Flask
from app.config import Config
from app.extensions import db, login_manager

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Extension'ları başlat
    db.init_app(app)
    login_manager.init_app(app)

    # Blueprint'leri kaydet
    from app.routes import auth, main
    app.register_blueprint(auth.bp)
    app.register_blueprint(main.bp)

    # Veritabanını oluştur
    with app.app_context():
        db.create_all()

    return app 