import os
import sys
import io
import tempfile
import subprocess
import secrets
import string
from functools import wraps
from flask import render_template, request, jsonify, redirect, url_for, flash, session, send_file, abort
from app.models import Lesson, db, User, Progress, QuizQuestion, QuizResult

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from app.algo_core.doitien import solve_doi_tien
from app.algo_core.day_con_tang_dai_nhat import solve_day_con_tang
from app.algo_core.nhanmatran import solve_nhan_ma_tran
from app.algo_core.timduongngannhat import solve_shortest_path_dag
from app.algo_core.timkiemrong import solve_bfs
from app.algo_core.timkiemsau import solve_dfs
from app.algo_core.tinhsotohop import solve_combinations
from app.algo_core.xauconchungnhat import solve_xau_con_chung
from app.algo_core.xepbalo import solve_xep_ba_lo


def init_routes(app):

    # ========================
    # DECORATORS
    # ========================
    def admin_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if not current_user.is_authenticated or current_user.role != 'admin':
                abort(403)
            return f(*args, **kwargs)
        return decorated

    # ========================
    # MIDDLEWARE
    # ========================
    @app.before_request
    def check_deleted_user():
        if current_user.is_authenticated and current_user.is_deleted:
            logout_user()
            return redirect(url_for('login'))

    # ========================
    # HELPER: Kiểm tra bài học đã mở khoá chưa
    # ========================
    def is_lesson_unlocked(lesson, user):
        """Bài đầu tiên (order=1) luôn mở. Bài N cần pass quiz bài N-1."""
        if lesson.order <= 1:
            return True
        if not user.is_authenticated:
            return False
        prev_lesson = Lesson.query.filter_by(order=lesson.order - 1).first()
        if not prev_lesson:
            return True
        passed = QuizResult.query.filter_by(
            user_id=user.id,
            lesson_id=prev_lesson.id,
            passed=True
        ).first()
        return passed is not None

    def get_lesson_unlock_map(user):
        """Trả về dict {lesson_id: True/False} cho tất cả bài học."""
        lessons = Lesson.query.order_by(Lesson.order).all()
        unlock_map = {}
        for lesson in lessons:
            unlock_map[lesson.id] = is_lesson_unlocked(lesson, user)
        return unlock_map

    # ========================
    # PUBLIC ROUTES
    # ========================
    @app.route('/')
    def index():
        lessons = Lesson.query.order_by(Lesson.order).all()
        unlock_map = get_lesson_unlock_map(current_user)
        quiz_passed_map = {}
        if current_user.is_authenticated:
            for lesson in lessons:
                qr = QuizResult.query.filter_by(
                    user_id=current_user.id,
                    lesson_id=lesson.id,
                    passed=True
                ).first()
                quiz_passed_map[lesson.id] = qr is not None
        return render_template('index.html', lessons=lessons,
                               unlock_map=unlock_map, quiz_passed_map=quiz_passed_map)

    @app.route('/theory')
    def theory():
        lessons = Lesson.query.order_by(Lesson.order).all()
        return render_template('theory.html', lessons=lessons)

    @app.route('/dashboard')
    def dashboard():
        lessons = Lesson.query.order_by(Lesson.order).all()
        progress_map = {}
        quiz_passed_map = {}
        unlock_map = {}
        if current_user.is_authenticated:
            user_progresses = Progress.query.filter_by(user_id=current_user.id).all()
            progress_map = {p.lesson_id: p for p in user_progresses}
            for lesson in lessons:
                qr = QuizResult.query.filter_by(
                    user_id=current_user.id,
                    lesson_id=lesson.id,
                    passed=True
                ).first()
                quiz_passed_map[lesson.id] = qr is not None
            unlock_map = get_lesson_unlock_map(current_user)

        roadmap = []
        for lesson in lessons:
            prog = progress_map.get(lesson.id)
            qr = quiz_passed_map.get(lesson.id, False)
            roadmap.append({
                'lesson': lesson,
                'is_completed': prog.is_completed if prog else False,
                'quiz_passed': qr,
                'unlocked': unlock_map.get(lesson.id, False),
            })

        return render_template('dashboard.html', roadmap=roadmap, lessons=lessons,
                               unlock_map=unlock_map)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            user = User.query.filter_by(username=username).first()

            if user and user.is_deleted:
                return render_template('login.html', error='Tài khoản này đã bị xóa.')

            if user and check_password_hash(user.password, password):
                if user.totp_enabled and user.totp_secret:
                    session['pre_2fa_user_id'] = user.id
                    return redirect(url_for('verify_2fa'))
                login_user(user)
                if user.role == 'admin':
                    return redirect(url_for('admin_index'))
                return redirect(url_for('dashboard'))
            else:
                return render_template('login.html', error='Tên đăng nhập hoặc mật khẩu không đúng')
        return render_template('login.html')

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            if username == 'admin':
                return render_template('register.html', error='Tên đăng nhập này đã được sử dụng.')
            user = User.query.filter_by(username=username).first()
            if user:
                return render_template('register.html', error='Tên đăng nhập đã tồn tại')
            new_user = User(username=username,
                            password=generate_password_hash(password, method='pbkdf2:sha256'),
                            role='user')
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for('dashboard'))
        return render_template('register.html')

    @app.route('/forgot-password', methods=['GET', 'POST'])
    def forgot_password():
        import pyotp
        if request.method == 'POST':
            username = request.form.get('username')
            otp_code = request.form.get('otp_code', '')
            new_password = request.form.get('new_password', '')
            confirm_password = request.form.get('confirm_password', '')

            user = User.query.filter_by(username=username).first()
            if not user or user.is_deleted:
                return render_template('forgot_password.html', error='Tài khoản không tồn tại.')
            if not user.totp_enabled or not user.totp_secret:
                return render_template('forgot_password.html',
                                       error='Tài khoản chưa bật xác thực 2 bước để khôi phục mật khẩu.')

            totp = pyotp.TOTP(user.totp_secret)
            if not totp.verify(otp_code, valid_window=1):
                return render_template('forgot_password.html', error='Mã xác thực OTP không đúng.')
            if len(new_password) < 6:
                return render_template('forgot_password.html', error='Mật khẩu mới phải có ít nhất 6 ký tự.')
            if new_password != confirm_password:
                return render_template('forgot_password.html', error='Mật khẩu xác nhận không khớp.')

            user.password = generate_password_hash(new_password, method='pbkdf2:sha256')
            db.session.commit()
            return render_template('forgot_password.html', success='Đặt lại mật khẩu thành công!')
        return render_template('forgot_password.html')

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('index'))

    # ========================
    # CÀI ĐẶT / ĐỔI MẬT KHẨU
    # ========================
    @app.route('/settings')
    @login_required
    def settings():
        return render_template('settings.html')

    @app.route('/change-password', methods=['POST'])
    @login_required
    def change_password():
        old_password = request.form.get('old_password', '')
        new_password = request.form.get('new_password', '')
        confirm_password = request.form.get('confirm_password', '')

        if not check_password_hash(current_user.password, old_password):
            return render_template('settings.html', pw_error='Mật khẩu hiện tại không đúng.')
        if len(new_password) < 6:
            return render_template('settings.html', pw_error='Mật khẩu mới phải có ít nhất 6 ký tự.')
        if new_password != confirm_password:
            return render_template('settings.html', pw_error='Mật khẩu xác nhận không khớp.')

        current_user.password = generate_password_hash(new_password, method='pbkdf2:sha256')
        db.session.commit()
        return render_template('settings.html', pw_success='Đổi mật khẩu thành công!')

    @app.route('/delete-account', methods=['POST'])
    @login_required
    def delete_account():
        password = request.form.get('password', '')
        if not check_password_hash(current_user.password, password):
            return render_template('settings.html', del_error='Mật khẩu không đúng.')

        from datetime import datetime
        random_suffix = ''.join(secrets.choice(string.ascii_lowercase + string.digits) for _ in range(12))
        current_user.username = f"deleted_{random_suffix}"
        current_user.password = generate_password_hash(secrets.token_hex(32), method='pbkdf2:sha256')
        current_user.is_deleted = True
        current_user.deleted_at = datetime.utcnow()
        current_user.totp_secret = None
        current_user.totp_enabled = False
        db.session.commit()
        logout_user()
        return redirect(url_for('index'))

    # ========================
    # 2FA
    # ========================
    @app.route('/setup-2fa', methods=['GET', 'POST'])
    @login_required
    def setup_2fa():
        import pyotp
        if request.method == 'POST':
            otp_code = request.form.get('otp_code', '')
            secret = session.get('temp_totp_secret', current_user.totp_secret)
            if not secret:
                return redirect(url_for('setup_2fa'))
            totp = pyotp.TOTP(secret)
            if totp.verify(otp_code, valid_window=1):
                current_user.totp_secret = secret
                current_user.totp_enabled = True
                db.session.commit()
                session.pop('temp_totp_secret', None)
                return render_template('settings.html', tfa_success='Xác thực 2 bước đã được bật!')
            else:
                provisioning_uri = totp.provisioning_uri(name=current_user.username, issuer_name='DPMaster')
                return render_template('setup_2fa.html', secret=secret, provisioning_uri=provisioning_uri,
                                       error='Mã xác thực không đúng. Vui lòng thử lại.')
        secret = session.get('temp_totp_secret')
        if not secret:
            import pyotp
            secret = pyotp.random_base32()
            session['temp_totp_secret'] = secret
        import pyotp
        totp = pyotp.TOTP(secret)
        provisioning_uri = totp.provisioning_uri(name=current_user.username, issuer_name='DPMaster')
        return render_template('setup_2fa.html', secret=secret, provisioning_uri=provisioning_uri)

    @app.route('/qr-code')
    @login_required
    def qr_code():
        import pyotp
        import qrcode
        secret = session.get('temp_totp_secret', current_user.totp_secret)
        if not secret:
            return '', 404
        totp = pyotp.TOTP(secret)
        provisioning_uri = totp.provisioning_uri(name=current_user.username, issuer_name='DPMaster')
        img = qrcode.make(provisioning_uri)
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        buf.seek(0)
        return send_file(buf, mimetype='image/png')

    @app.route('/verify-2fa', methods=['GET', 'POST'])
    def verify_2fa():
        import pyotp
        from time import time
        MAX_OTP_ATTEMPTS = 5
        LOCKOUT_SECONDS = 300

        user_id = session.get('pre_2fa_user_id')
        if not user_id:
            return redirect(url_for('login'))
        user = db.session.get(User, user_id)
        if not user or not user.totp_enabled:
            session.pop('pre_2fa_user_id', None)
            return redirect(url_for('login'))

        lockout_until = session.get('otp_lockout_until', 0)
        if time() < lockout_until:
            remaining = int(lockout_until - time())
            return render_template('verify_2fa.html',
                error=f'Bạn đã nhập sai quá nhiều lần. Vui lòng thử lại sau {remaining} giây.')

        if request.method == 'POST':
            otp_code = request.form.get('otp_code', '')
            totp = pyotp.TOTP(user.totp_secret)
            if totp.verify(otp_code, valid_window=1):
                session.pop('pre_2fa_user_id', None)
                session.pop('otp_attempts', None)
                session.pop('otp_lockout_until', None)
                login_user(user)
                if user.role == 'admin':
                    return redirect(url_for('admin_index'))
                return redirect(url_for('dashboard'))
            else:
                attempts = session.get('otp_attempts', 0) + 1
                session['otp_attempts'] = attempts
                if attempts >= MAX_OTP_ATTEMPTS:
                    session['otp_lockout_until'] = time() + LOCKOUT_SECONDS
                    session['otp_attempts'] = 0
                    return render_template('verify_2fa.html',
                        error=f'Bạn đã nhập sai {MAX_OTP_ATTEMPTS} lần. Bị khóa {LOCKOUT_SECONDS // 60} phút.')
                return render_template('verify_2fa.html',
                    error=f'Mã xác thực không đúng. Còn {MAX_OTP_ATTEMPTS - attempts} lần thử.')
        return render_template('verify_2fa.html')

    @app.route('/disable-2fa', methods=['POST'])
    @login_required
    def disable_2fa():
        password = request.form.get('password', '')
        if not check_password_hash(current_user.password, password):
            return render_template('settings.html', tfa_error='Mật khẩu không đúng.')
        current_user.totp_enabled = False
        current_user.totp_secret = None
        db.session.commit()
        return render_template('settings.html', tfa_success='Đã tắt xác thực 2 bước.')

    # ========================
    # BÀI HỌC
    # ========================
    @app.route('/lesson/<slug>', methods=['GET', 'POST'])
    @login_required
    def lesson_detail(slug):
        lesson = Lesson.query.filter_by(slug=slug).first_or_404()

        # Kiểm tra mở khoá
        if not is_lesson_unlocked(lesson, current_user):
            prev_lesson = Lesson.query.filter_by(order=lesson.order - 1).first()
            return render_template('locked.html', lesson=lesson, prev_lesson=prev_lesson)

        result = None
        algo_success = False

        if request.method == 'POST':
            try:
                if slug == 'doi-tien':
                    coins = [int(x.strip()) for x in request.form.get('coins').split(',')]
                    amount = int(request.form.get('amount'))
                    result = solve_doi_tien(coins, amount)
                elif slug == 'day-con-tang':
                    arr = [int(x.strip()) for x in request.form.get('arr').split(',')]
                    result = solve_day_con_tang(arr)
                elif slug == 'nhan-ma-tran':
                    p = [int(x.strip()) for x in request.form.get('p').split(',')]
                    result = solve_nhan_ma_tran(p)
                elif slug == 'tim-duong-ngan-nhat':
                    n = int(request.form.get('n'))
                    start_node = int(request.form.get('start_node'))
                    edges_raw = request.form.get('edges').strip().split('\n')
                    edges = []
                    for line in edges_raw:
                        if line.strip():
                            u, v, w = map(int, line.strip().split())
                            edges.append((u, v, w))
                    result = solve_shortest_path_dag(n, edges, start_node)
                elif slug == 'tim-kiem-rong':
                    import json
                    tree_dict = json.loads(request.form.get('tree_json'))
                    result = solve_bfs(tree_dict)
                elif slug == 'tim-kiem-sau':
                    import json
                    tree_dict = json.loads(request.form.get('tree_json'))
                    result = solve_dfs(tree_dict)
                elif slug == 'tinh-so-to-hop':
                    n = int(request.form.get('n'))
                    k = int(request.form.get('k'))
                    result = solve_combinations(n, k)
                elif slug == 'xau-con-chung':
                    s1 = request.form.get('s1').strip()
                    s2 = request.form.get('s2').strip()
                    result = solve_xau_con_chung(s1, s2)
                elif slug == 'xep-ba-lo':
                    w_max = int(request.form.get('w_max'))
                    items_raw = request.form.get('items').strip().split('\n')
                    weights, values, names = [], [], []
                    for line in items_raw:
                        if line.strip():
                            parts = line.strip().split()
                            weights.append(int(parts[0]))
                            values.append(int(parts[1]))
                            names.append(" ".join(parts[2:]))
                    result = solve_xep_ba_lo(weights, values, names, w_max)

                if result and result.get('success'):
                    algo_success = True
            except Exception as e:
                result = {"success": False, "message": f"Lỗi: {str(e)}"}

        # Cập nhật tiến độ
        prog = Progress.query.filter_by(user_id=current_user.id, lesson_id=lesson.id).first()
        if not prog:
            prog = Progress(user_id=current_user.id, lesson_id=lesson.id, is_completed=False)
            db.session.add(prog)
            db.session.commit()
        elif algo_success and not prog.is_completed:
            prog.is_completed = True
            from datetime import datetime
            prog.updated_at = datetime.utcnow()
            db.session.commit()

        # Kiểm tra đã pass quiz chưa
        quiz_passed = QuizResult.query.filter_by(
            user_id=current_user.id, lesson_id=lesson.id, passed=True
        ).first() is not None

        result_json = None
        if result:
            import json
            result_json = json.dumps(result, indent=2, ensure_ascii=False)

        return render_template('lesson.html', lesson=lesson, result=result,
                               result_json=result_json, quiz_passed=quiz_passed,
                               lesson_completed=prog.is_completed)

    # ========================
    # QUIZ
    # ========================
    @app.route('/quiz/<slug>', methods=['GET', 'POST'])
    @login_required
    def quiz(slug):
        lesson = Lesson.query.filter_by(slug=slug).first_or_404()

        if not is_lesson_unlocked(lesson, current_user):
            return redirect(url_for('index'))

        questions = QuizQuestion.query.filter_by(lesson_id=lesson.id).order_by(QuizQuestion.order).all()
        if not questions:
            return redirect(url_for('lesson_detail', slug=slug))

        # Kiểm tra đã pass chưa
        already_passed = QuizResult.query.filter_by(
            user_id=current_user.id, lesson_id=lesson.id, passed=True
        ).first()

        if request.method == 'POST':
            score = 0
            total = len(questions)
            answers = {}
            for q in questions:
                user_answer = request.form.get(f'q_{q.id}', '').upper()
                answers[q.id] = user_answer
                if user_answer == q.correct:
                    score += 1

            percentage = (score / total * 100) if total > 0 else 0
            passed = percentage >= lesson.pass_percentage

            # Lưu kết quả (chỉ lưu nếu chưa pass, hoặc luôn lưu lần mới nhất)
            qr = QuizResult(
                user_id=current_user.id,
                lesson_id=lesson.id,
                score=score,
                total=total,
                passed=passed
            )
            db.session.add(qr)
            db.session.commit()

            # Tìm bài tiếp theo
            next_lesson = Lesson.query.filter_by(order=lesson.order + 1).first()

            return render_template('quiz_result.html',
                                   lesson=lesson,
                                   questions=questions,
                                   answers=answers,
                                   score=score,
                                   total=total,
                                   percentage=percentage,
                                   passed=passed,
                                   next_lesson=next_lesson,
                                   pass_percentage=lesson.pass_percentage)

        return render_template('quiz.html', lesson=lesson, questions=questions,
                               already_passed=already_passed)

    # ========================
    # CHẠY CODE (SANDBOX)
    # ========================
    @app.route('/run_code', methods=['POST'])
    @login_required
    def run_code():
        from app.sandbox import validate_code
        data = request.get_json()
        code = data.get('code', '') if data else ''
        if not code:
            return jsonify({"success": False, "output": "Không có code để chạy."})

        is_safe, error_msg = validate_code(code)
        if not is_safe:
            return jsonify({"success": False, "output": f"⛔ Bảo mật: {error_msg}"})

        docker_enabled = os.environ.get('DOCKER_AVAILABLE', '1') != '0'
        if not docker_enabled:
            return jsonify({"success": False,
                            "output": "⚠️ Tính năng chạy code tạm thời không khả dụng trên server này.\n"
                                      "Bạn có thể copy code và chạy trực tiếp trên máy."})
        try:
            result = subprocess.run(
                ['docker', 'run', '--rm', '-i', '--net=none', '--memory=128m', '--cpus=0.5',
                 'python:3.9-slim', 'python', '-I', '-'],
                input=code, capture_output=True, text=True, timeout=5
            )
            output = result.stdout
            if result.stderr:
                output += "\nLỗi:\n" + result.stderr
            return jsonify({"success": True, "output": output})
        except subprocess.TimeoutExpired:
            return jsonify({"success": False, "output": "Lỗi: Code chạy quá 5 giây."})
        except FileNotFoundError:
            os.environ['DOCKER_AVAILABLE'] = '0'
            return jsonify({"success": False,
                            "output": "⚠️ Tính năng chạy code tạm thời không khả dụng.\n"
                                      "Bạn có thể copy code và chạy trực tiếp trên máy."})
        except Exception as e:
            return jsonify({"success": False, "output": f"Lỗi hệ thống: {str(e)}"})

    # ========================
    # ADMIN ROUTES
    # ========================
    @app.route('/admin')
    @login_required
    @admin_required
    def admin_index():
        total_users = User.query.filter_by(is_deleted=False, role='user').count()
        total_lessons = Lesson.query.count()
        total_completions = Progress.query.filter_by(is_completed=True).count()
        total_quiz_passed = QuizResult.query.filter_by(passed=True).count()
        recent_users = User.query.filter_by(is_deleted=False, role='user').order_by(User.id.desc()).limit(5).all()
        lessons = Lesson.query.order_by(Lesson.order).all()

        # Thống kê từng bài học
        lesson_stats = []
        for lesson in lessons:
            learners = Progress.query.filter_by(lesson_id=lesson.id).count()
            completions = Progress.query.filter_by(lesson_id=lesson.id, is_completed=True).count()
            quiz_passes = QuizResult.query.filter_by(lesson_id=lesson.id, passed=True).count()
            lesson_stats.append({
                'lesson': lesson,
                'learners': learners,
                'completions': completions,
                'quiz_passes': quiz_passes,
            })

        return render_template('admin/index.html',
                               total_users=total_users,
                               total_lessons=total_lessons,
                               total_completions=total_completions,
                               total_quiz_passed=total_quiz_passed,
                               recent_users=recent_users,
                               lesson_stats=lesson_stats)

    @app.route('/admin/lessons')
    @login_required
    @admin_required
    def admin_lessons():
        lessons = Lesson.query.order_by(Lesson.order).all()
        lesson_stats = []
        for lesson in lessons:
            learners = Progress.query.filter_by(lesson_id=lesson.id).count()
            completions = Progress.query.filter_by(lesson_id=lesson.id, is_completed=True).count()
            quiz_passes = QuizResult.query.filter_by(lesson_id=lesson.id, passed=True).count()
            q_count = QuizQuestion.query.filter_by(lesson_id=lesson.id).count()
            lesson_stats.append({
                'lesson': lesson,
                'learners': learners,
                'completions': completions,
                'quiz_passes': quiz_passes,
                'q_count': q_count,
            })
        return render_template('admin/lessons.html', lesson_stats=lesson_stats)

    @app.route('/admin/lessons/<int:lesson_id>/move', methods=['POST'])
    @login_required
    @admin_required
    def admin_lesson_move(lesson_id):
        direction = request.form.get('direction')  # 'up' hoặc 'down'
        lesson = Lesson.query.get_or_404(lesson_id)
        if direction == 'up' and lesson.order > 1:
            other = Lesson.query.filter_by(order=lesson.order - 1).first()
            if other:
                other.order, lesson.order = lesson.order, other.order
                db.session.commit()
        elif direction == 'down':
            other = Lesson.query.filter_by(order=lesson.order + 1).first()
            if other:
                other.order, lesson.order = lesson.order, other.order
                db.session.commit()
        return redirect(url_for('admin_lessons'))

    @app.route('/admin/students')
    @login_required
    @admin_required
    def admin_students():
        students = User.query.filter_by(is_deleted=False, role='user').order_by(User.id).all()
        lessons = Lesson.query.order_by(Lesson.order).all()

        student_data = []
        for student in students:
            completed = Progress.query.filter_by(user_id=student.id, is_completed=True).count()
            quiz_passed = QuizResult.query.filter_by(user_id=student.id, passed=True).count()
            student_data.append({
                'student': student,
                'completed_lessons': completed,
                'quiz_passed': quiz_passed,
                'total_lessons': len(lessons),
            })

        return render_template('admin/students.html', student_data=student_data, lessons=lessons)

    @app.route('/admin/student/<int:student_id>')
    @login_required
    @admin_required
    def admin_student_detail(student_id):
        student = User.query.get_or_404(student_id)
        if student.role == 'admin':
            abort(404)
        lessons = Lesson.query.order_by(Lesson.order).all()

        detail = []
        for lesson in lessons:
            prog = Progress.query.filter_by(user_id=student.id, lesson_id=lesson.id).first()
            quiz_result = QuizResult.query.filter_by(
                user_id=student.id, lesson_id=lesson.id
            ).order_by(QuizResult.taken_at.desc()).first()
            best_quiz = QuizResult.query.filter_by(
                user_id=student.id, lesson_id=lesson.id, passed=True
            ).first()
            detail.append({
                'lesson': lesson,
                'accessed': prog is not None,
                'completed': prog.is_completed if prog else False,
                'quiz_result': quiz_result,
                'quiz_passed': best_quiz is not None,
            })

        return render_template('admin/student_detail.html', student=student, detail=detail)

    # ========================
    # ERROR HANDLERS
    # ========================
    @app.errorhandler(403)
    def forbidden(e):
        return render_template('error.html', code=403,
                               message='Bạn không có quyền truy cập trang này.'), 403

    @app.errorhandler(404)
    def not_found(e):
        return render_template('error.html', code=404,
                               message='Trang không tồn tại.'), 404