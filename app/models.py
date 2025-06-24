from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app.extensions import db, login_manager
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # İlişkiler
    tasks = db.relationship('Task', backref='author', lazy='dynamic')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')  # pending, in_progress, completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f'<Task {self.title}>'

# Veritabanı işlemleri için yardımcı fonksiyonlar
def init_db():
    """Veritabanını başlat ve tabloları oluştur"""
    db.create_all()

def add_user(username, email, password):
    """Yeni kullanıcı ekle"""
    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return user

def get_user_by_username(username):
    """Kullanıcı adına göre kullanıcı getir"""
    return User.query.filter_by(username=username).first()

def get_user_by_email(email):
    """E-posta adresine göre kullanıcı getir"""
    return User.query.filter_by(email=email).first()

def add_task(title, description, user_id):
    """Yeni görev ekle"""
    task = Task(title=title, description=description, user_id=user_id)
    db.session.add(task)
    db.session.commit()
    return task

def get_user_tasks(user_id):
    """Kullanıcının görevlerini getir"""
    return Task.query.filter_by(user_id=user_id).order_by(Task.created_at.desc()).all()

def update_task_status(task_id, status):
    """Görev durumunu güncelle"""
    task = Task.query.get_or_404(task_id)
    task.status = status
    task.updated_at = datetime.utcnow()
    db.session.commit()
    return task

def delete_task(task_id):
    """Görevi sil"""
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()

@login_manager.user_loader
def get_user_by_id(user_id):
    return User.query.get(int(user_id)) 