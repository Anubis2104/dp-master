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

# Tạo tất cả bảng khi app khởi động (chạy cả khi dùng Gunicorn lẫn python run.py)
with app.app_context():
    db.create_all()

    # Auto-seed: Tạo dữ liệu bài học nếu database đang rỗng
    from app.models import Lesson
    if Lesson.query.count() == 0:
        lessons_data = [
            {
                'slug': 'doi-tien',
                'title': 'Đổi Tiền (Coin Change)',
                'theory': 'Bài toán đổi tiền: Cho một tập hợp các mệnh giá tiền xu và một số tiền cần đổi, tìm số lượng xu ít nhất để đổi được số tiền đó. Đây là bài toán quy hoạch động cổ điển.',
                'python_code': 'def coin_change(coins, amount):\n    dp = [float("inf")] * (amount + 1)\n    dp[0] = 0\n    for coin in coins:\n        for x in range(coin, amount + 1):\n            dp[x] = min(dp[x], dp[x - coin] + 1)\n    return dp[amount] if dp[amount] != float("inf") else -1'
            },
            {
                'slug': 'day-con-tang',
                'title': 'Dãy Con Tăng Dài Nhất (LIS)',
                'theory': 'Bài toán LIS (Longest Increasing Subsequence): Tìm dãy con tăng dài nhất trong một mảng số nguyên. Đây là bài toán quy hoạch động quan trọng với ứng dụng rộng rãi.',
                'python_code': 'def lis(arr):\n    n = len(arr)\n    dp = [1] * n\n    for i in range(1, n):\n        for j in range(i):\n            if arr[j] < arr[i]:\n                dp[i] = max(dp[i], dp[j] + 1)\n    return max(dp)'
            },
            {
                'slug': 'nhan-ma-tran',
                'title': 'Nhân Ma Trận (Matrix Chain)',
                'theory': 'Bài toán nhân chuỗi ma trận: Tìm thứ tự nhân tối ưu để giảm thiểu số phép nhân cần thực hiện. Sử dụng quy hoạch động với bảng 2 chiều.',
                'python_code': 'def matrix_chain(p):\n    n = len(p) - 1\n    dp = [[0]*n for _ in range(n)]\n    for l in range(2, n+1):\n        for i in range(n-l+1):\n            j = i+l-1\n            dp[i][j] = float("inf")\n            for k in range(i, j):\n                cost = dp[i][k] + dp[k+1][j] + p[i]*p[k+1]*p[j+1]\n                dp[i][j] = min(dp[i][j], cost)\n    return dp[0][n-1]'
            },
            {
                'slug': 'tim-duong-ngan-nhat',
                'title': 'Tìm Đường Ngắn Nhất (DAG Shortest Path)',
                'theory': 'Tìm đường đi ngắn nhất trong đồ thị có hướng không có chu trình (DAG) sử dụng quy hoạch động kết hợp với sắp xếp topo.',
                'python_code': 'def dag_shortest_path(n, edges, start):\n    from collections import defaultdict\n    graph = defaultdict(list)\n    for u, v, w in edges:\n        graph[u].append((v, w))\n    dist = [float("inf")] * n\n    dist[start] = 0\n    # Relaxation\n    for _ in range(n - 1):\n        for u, v, w in edges:\n            if dist[u] + w < dist[v]:\n                dist[v] = dist[u] + w\n    return dist'
            },
            {
                'slug': 'tim-kiem-rong',
                'title': 'Tìm Kiếm Rộng (BFS)',
                'theory': 'Thuật toán tìm kiếm theo chiều rộng (BFS - Breadth-First Search) duyệt đồ thị theo từng tầng. Dùng để tìm đường đi ngắn nhất trong đồ thị không có trọng số.',
                'python_code': 'from collections import deque\ndef bfs(graph, start):\n    visited = set([start])\n    queue = deque([start])\n    order = []\n    while queue:\n        node = queue.popleft()\n        order.append(node)\n        for neighbor in graph.get(node, []):\n            if neighbor not in visited:\n                visited.add(neighbor)\n                queue.append(neighbor)\n    return order'
            },
            {
                'slug': 'tim-kiem-sau',
                'title': 'Tìm Kiếm Sâu (DFS)',
                'theory': 'Thuật toán tìm kiếm theo chiều sâu (DFS - Depth-First Search) duyệt đồ thị theo từng nhánh đến cùng trước khi quay lui. Ứng dụng trong phát hiện chu trình, sắp xếp topo.',
                'python_code': 'def dfs(graph, start, visited=None):\n    if visited is None:\n        visited = set()\n    visited.add(start)\n    order = [start]\n    for neighbor in graph.get(start, []):\n        if neighbor not in visited:\n            order.extend(dfs(graph, neighbor, visited))\n    return order'
            },
            {
                'slug': 'tinh-so-to-hop',
                'title': 'Tính Số Tổ Hợp (Combinations)',
                'theory': 'Tính số tổ hợp C(n,k) sử dụng quy hoạch động với tam giác Pascal. Phương pháp này hiệu quả và tránh tràn số so với tính trực tiếp bằng giai thừa.',
                'python_code': 'def combinations(n, k):\n    dp = [[0]*(k+1) for _ in range(n+1)]\n    for i in range(n+1):\n        dp[i][0] = 1\n    for i in range(1, n+1):\n        for j in range(1, min(i,k)+1):\n            dp[i][j] = dp[i-1][j-1] + dp[i-1][j]\n    return dp[n][k]'
            },
            {
                'slug': 'xau-con-chung',
                'title': 'Xâu Con Chung Dài Nhất (LCS)',
                'theory': 'Bài toán LCS (Longest Common Subsequence): Tìm xâu con chung dài nhất của hai xâu ký tự. Đây là bài toán quy hoạch động cơ bản với bảng 2 chiều.',
                'python_code': 'def lcs(s1, s2):\n    m, n = len(s1), len(s2)\n    dp = [[0]*(n+1) for _ in range(m+1)]\n    for i in range(1, m+1):\n        for j in range(1, n+1):\n            if s1[i-1] == s2[j-1]:\n                dp[i][j] = dp[i-1][j-1] + 1\n            else:\n                dp[i][j] = max(dp[i-1][j], dp[i][j-1])\n    return dp[m][n]'
            },
            {
                'slug': 'xep-ba-lo',
                'title': 'Xếp Ba Lô (0/1 Knapsack)',
                'theory': 'Bài toán xếp ba lô 0/1: Cho n vật phẩm, mỗi vật có trọng lượng và giá trị, chọn các vật để tổng giá trị lớn nhất mà không vượt quá sức chứa của ba lô.',
                'python_code': 'def knapsack(weights, values, W):\n    n = len(weights)\n    dp = [[0]*(W+1) for _ in range(n+1)]\n    for i in range(1, n+1):\n        for w in range(W+1):\n            dp[i][w] = dp[i-1][w]\n            if weights[i-1] <= w:\n                dp[i][w] = max(dp[i][w], dp[i-1][w-weights[i-1]] + values[i-1])\n    return dp[n][W]'
            },
        ]
        for data in lessons_data:
            lesson = Lesson(**data)
            db.session.add(lesson)
        db.session.commit()
        print("✅ Auto-seeded 9 lessons vào database.")

if __name__ == '__main__':
    # debug=True chỉ khi FLASK_DEBUG=1, mặc định là False
    app.run(host='0.0.0.0', debug=app.config['DEBUG'])


