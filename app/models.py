from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    # 2FA fields
    totp_secret = db.Column(db.String(32), nullable=True)  # Base32 key
    totp_enabled = db.Column(db.Boolean, default=False)
    # Soft delete fields
    is_deleted = db.Column(db.Boolean, default=False)
    deleted_at = db.Column(db.DateTime, nullable=True)
    # Quan hệ với bảng tiến độ
    progresses = db.relationship('Progress', backref='student', lazy=True)

    @property
    def is_active(self):
        """Override Flask-Login: chặn user đã bị soft-delete đăng nhập."""
        return not self.is_deleted

class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(50), unique=True, nullable=False) # ví dụ: 'doi-tien'
    title = db.Column(db.String(100), nullable=False)
    theory = db.Column(db.Text, nullable=True)
    python_code = db.Column(db.Text, nullable=True)

class Progress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'), nullable=False)
    is_completed = db.Column(db.Boolean, default=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
