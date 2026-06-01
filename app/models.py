from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    # Phân quyền: 'user' (học viên) hoặc 'admin'
    role = db.Column(db.String(10), default='user', nullable=False)
    # 2FA fields
    totp_secret = db.Column(db.String(32), nullable=True)
    totp_enabled = db.Column(db.Boolean, default=False)
    # Soft delete fields
    is_deleted = db.Column(db.Boolean, default=False)
    deleted_at = db.Column(db.DateTime, nullable=True)
    # Quan hệ
    progresses = db.relationship('Progress', backref='student', lazy=True)
    quiz_results = db.relationship('QuizResult', backref='student_quiz', lazy=True)

    @property
    def is_active(self):
        """Override Flask-Login: chặn user đã bị soft-delete đăng nhập."""
        return not self.is_deleted

    @property
    def is_admin(self):
        return self.role == 'admin'


class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(50), unique=True, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    theory = db.Column(db.Text, nullable=True)
    python_code = db.Column(db.Text, nullable=True)
    # Thứ tự bài học (1-9)
    order = db.Column(db.Integer, default=0, nullable=False)
    # % câu đúng tối thiểu để mở khoá bài tiếp theo
    pass_percentage = db.Column(db.Integer, default=75, nullable=False)
    # Quan hệ
    quiz_questions = db.relationship('QuizQuestion', backref='lesson', lazy=True,
                                     order_by='QuizQuestion.order')


class Progress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'), nullable=False)
    is_completed = db.Column(db.Boolean, default=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)


class QuizQuestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'), nullable=False)
    question = db.Column(db.Text, nullable=False)
    option_a = db.Column(db.String(500), nullable=False)
    option_b = db.Column(db.String(500), nullable=False)
    option_c = db.Column(db.String(500), nullable=False)
    option_d = db.Column(db.String(500), nullable=False)
    correct = db.Column(db.String(1), nullable=False)  # 'A', 'B', 'C', 'D'
    order = db.Column(db.Integer, default=0)


class QuizResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)       # Số câu đúng
    total = db.Column(db.Integer, nullable=False)       # Tổng số câu
    passed = db.Column(db.Boolean, default=False)       # Đạt hay không
    taken_at = db.Column(db.DateTime, default=datetime.utcnow)
    lesson = db.relationship('Lesson', foreign_keys=[lesson_id])
