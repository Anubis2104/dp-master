import os
from flask import Flask
from app.models import db, User
from app.routes import init_routes
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect

# Try to load environment variables from .env using python-dotenv, with a manual fallback
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # Manual fallback for loading .env if python-dotenv is not installed
    dotenv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
    if os.path.exists(dotenv_path):
        with open(dotenv_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if '=' in line:
                    key, val = line.split('=', 1)
                    key = key.strip()
                    val = val.strip()
                    if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
                        val = val[1:-1]
                    os.environ.setdefault(key, val)

app = Flask(__name__,
            template_folder='app/templates',
            static_folder='app/static')

# Cấu hình từ biến môi trường (không hardcode SECRET_KEY)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', 'sqlite:///dp_master.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# SECRET_KEY bắt buộc phải được đặt trong biến môi trường khi chạy production
_secret_key = os.getenv('SECRET_KEY')
if not _secret_key:
    import warnings
    warnings.warn(
        'WARNING: SECRET_KEY không được đặt! Đang dùng key tạm thời - KHÔNG an toàn cho production.',
        stacklevel=2
    )
    _secret_key = os.urandom(32).hex()
app.config['SECRET_KEY'] = _secret_key

# Chế độ debug: chỉ bật khi biến môi trường FLASK_DEBUG=1 (KHÔNG bao giờ bật trong production)
app.config['DEBUG'] = os.getenv('FLASK_DEBUG', '0') == '1'

# Khởi tạo Extensions
db.init_app(app)
migrate = Migrate(app, db)  # Flask-Migrate (thay thế migration thủ công)
csrf = CSRFProtect(app)      # CSRF Protection

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))  # Fix legacy API warning

init_routes(app)

if __name__ == '__main__':
    with app.app_context():
        # Tạo tất cả bảng nếu chưa có (dựa trên models.py)
        db.create_all()

    # debug=True chỉ khi FLASK_DEBUG=1, mặc định là False
    app.run(host='0.0.0.0', debug=app.config['DEBUG'])


