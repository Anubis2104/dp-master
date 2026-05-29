"""
Unit tests cho routes và sandbox.
"""
import pytest


class TestPublicRoutes:
    """Test các route không cần đăng nhập."""

    def test_index(self, client):
        response = client.get('/')
        assert response.status_code == 200

    def test_login_page(self, client):
        response = client.get('/login')
        assert response.status_code == 200

    def test_register_page(self, client):
        response = client.get('/register')
        assert response.status_code == 200

    def test_dashboard(self, client):
        response = client.get('/dashboard')
        assert response.status_code == 200


class TestAuthFlow:
    """Test luồng đăng ký → đăng nhập → đăng xuất."""

    def test_register(self, client):
        response = client.post('/register', data={
            'username': 'testuser',
            'password': 'testpass123',
        }, follow_redirects=True)
        assert response.status_code == 200

    def test_login_wrong_password(self, client):
        # Đăng ký trước
        client.post('/register', data={
            'username': 'user2',
            'password': 'pass123',
        })
        client.get('/logout')
        # Login sai
        response = client.post('/login', data={
            'username': 'user2',
            'password': 'wrongpass',
        })
        assert 'không đúng'.encode('utf-8') in response.data


class TestProtectedRoutes:
    """Test các route yêu cầu đăng nhập."""

    def test_lesson_requires_login(self, client):
        response = client.get('/lesson/doi-tien')
        assert response.status_code == 302  # Redirect to login

    def test_settings_requires_login(self, client):
        response = client.get('/settings')
        assert response.status_code == 302


class TestSandbox:
    """Test module sandbox chặn code nguy hiểm."""

    def test_safe_code(self):
        from app.sandbox import validate_code
        is_safe, _ = validate_code("print('Hello World')")
        assert is_safe is True

    def test_block_os_import(self):
        from app.sandbox import validate_code
        is_safe, msg = validate_code("import os\nos.system('rm -rf /')")
        assert is_safe is False
        assert 'os' in msg

    def test_block_subprocess(self):
        from app.sandbox import validate_code
        is_safe, _ = validate_code("import subprocess")
        assert is_safe is False

    def test_block_eval(self):
        from app.sandbox import validate_code
        is_safe, _ = validate_code("eval('__import__(\"os\")')")
        assert is_safe is False

    def test_block_open(self):
        from app.sandbox import validate_code
        is_safe, _ = validate_code("open('/etc/passwd').read()")
        assert is_safe is False

    def test_block_dunder(self):
        from app.sandbox import validate_code
        is_safe, _ = validate_code("''.__class__.__mro__")
        assert is_safe is False

    def test_allow_math(self):
        from app.sandbox import validate_code
        is_safe, _ = validate_code("import math\nprint(math.sqrt(16))")
        assert is_safe is True

    def test_code_too_long(self):
        from app.sandbox import validate_code
        is_safe, _ = validate_code("x = 1\n" * 10001)
        assert is_safe is False


class TestForgotPassword:
    """Test tính năng quên mật khẩu và khôi phục bằng OTP."""

    def test_forgot_password_page(self, client):
        response = client.get('/forgot-password')
        assert response.status_code == 200
        assert 'Khôi phục mật khẩu'.encode('utf-8') in response.data

    def test_forgot_password_nonexistent_user(self, client):
        response = client.post('/forgot-password', data={
            'username': 'nonexistent',
            'otp_code': '123456',
            'new_password': 'newpassword123',
            'confirm_password': 'newpassword123'
        })
        assert 'Tài khoản không tồn tại'.encode('utf-8') in response.data

    def test_forgot_password_no_otp_setup(self, client):
        # Tạo user không bật 2FA
        client.post('/register', data={
            'username': 'user_no_otp',
            'password': 'password123',
        })
        client.get('/logout')

        response = client.post('/forgot-password', data={
            'username': 'user_no_otp',
            'otp_code': '123456',
            'new_password': 'newpassword123',
            'confirm_password': 'newpassword123'
        })
        assert 'chưa bật xác thực 2 bước'.encode('utf-8') in response.data

    def test_forgot_password_success(self, client, app):
        import pyotp
        from app.models import User
        from run import db

        # Đăng ký user
        client.post('/register', data={
            'username': 'user_with_otp',
            'password': 'password123',
        })
        client.get('/logout')

        # Bật OTP cho user thủ công qua DB (để test)
        secret = pyotp.random_base32()
        with app.app_context():
            user = User.query.filter_by(username='user_with_otp').first()
            user.totp_secret = secret
            user.totp_enabled = True
            db.session.commit()

        # Tạo OTP đúng
        totp = pyotp.TOTP(secret)
        otp_code = totp.now()

        # Thực hiện khôi phục
        response = client.post('/forgot-password', data={
            'username': 'user_with_otp',
            'otp_code': otp_code,
            'new_password': 'newpassword12345',
            'confirm_password': 'newpassword12345'
        })
        assert 'Đặt lại mật khẩu thành công'.encode('utf-8') in response.data

        # Thử login lại với pass mới
        response = client.post('/login', data={
            'username': 'user_with_otp',
            'password': 'newpassword12345',
        })
        # Vì đã bật 2FA nên khi nhập pass đúng sẽ redirect đến verify-2fa
        assert response.status_code == 302
        assert '/verify-2fa' in response.headers['Location']

