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

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', 'sqlite:///dp_master.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

_secret_key = os.getenv('SECRET_KEY')
if not _secret_key:
    import warnings
    warnings.warn(
        'WARNING: SECRET_KEY không được đặt! Đang dùng key tạm thời - KHÔNG an toàn cho production.',
        stacklevel=2
    )
    _secret_key = os.urandom(32).hex()
app.config['SECRET_KEY'] = _secret_key
app.config['DEBUG'] = os.getenv('FLASK_DEBUG', '0') == '1'

db.init_app(app)
migrate = Migrate(app, db)
csrf = CSRFProtect(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

init_routes(app)

# ============================================================
# SEED DATA
# ============================================================
with app.app_context():
    db.create_all()

    from app.models import Lesson, QuizQuestion, QuizResult
    from werkzeug.security import generate_password_hash

    # --- Seed Admin user ---
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(
            username='admin',
            password=generate_password_hash('huunh@2104', method='pbkdf2:sha256'),
            role='admin'
        )
        db.session.add(admin)
        db.session.commit()
        print("✅ Đã tạo tài khoản admin.")

    # Đảm bảo admin luôn có role đúng (fix nếu migrate cũ)
    elif admin.role != 'admin':
        admin.role = 'admin'
        db.session.commit()

    # --- Seed Lessons ---
    lessons_data = [
        {
            'slug': 'doi-tien',
            'title': 'Đổi Tiền (Coin Change)',
            'order': 1,
            'pass_percentage': 75,
            'theory': 'Bài toán đổi tiền: Cho một tập hợp các mệnh giá tiền xu và một số tiền cần đổi, tìm số lượng xu ít nhất để đổi được số tiền đó. Đây là bài toán quy hoạch động cổ điển dựa trên tối ưu con (optimal substructure) và lưu trữ kết quả trung gian (memoization).',
            'python_code': 'def coin_change(coins, amount):\n    dp = [float("inf")] * (amount + 1)\n    dp[0] = 0\n    for coin in coins:\n        for x in range(coin, amount + 1):\n            dp[x] = min(dp[x], dp[x - coin] + 1)\n    return dp[amount] if dp[amount] != float("inf") else -1'
        },
        {
            'slug': 'day-con-tang',
            'title': 'Dãy Con Tăng Dài Nhất (LIS)',
            'order': 2,
            'pass_percentage': 75,
            'theory': 'Bài toán LIS (Longest Increasing Subsequence): Tìm dãy con tăng dài nhất trong một mảng số nguyên. Đây là bài toán quy hoạch động quan trọng với nhiều ứng dụng trong bioinformatics và phân tích chuỗi dữ liệu.',
            'python_code': 'def lis(arr):\n    n = len(arr)\n    dp = [1] * n\n    for i in range(1, n):\n        for j in range(i):\n            if arr[j] < arr[i]:\n                dp[i] = max(dp[i], dp[j] + 1)\n    return max(dp)'
        },
        {
            'slug': 'nhan-ma-tran',
            'title': 'Nhân Ma Trận (Matrix Chain)',
            'order': 3,
            'pass_percentage': 75,
            'theory': 'Bài toán nhân chuỗi ma trận: Tìm thứ tự nhân tối ưu để giảm thiểu số phép nhân vô hướng cần thực hiện. Sử dụng quy hoạch động với bảng 2 chiều và có độ phức tạp O(n³).',
            'python_code': 'def matrix_chain(p):\n    n = len(p) - 1\n    dp = [[0]*n for _ in range(n)]\n    for l in range(2, n+1):\n        for i in range(n-l+1):\n            j = i+l-1\n            dp[i][j] = float("inf")\n            for k in range(i, j):\n                cost = dp[i][k] + dp[k+1][j] + p[i]*p[k+1]*p[j+1]\n                dp[i][j] = min(dp[i][j], cost)\n    return dp[0][n-1]'
        },
        {
            'slug': 'tim-duong-ngan-nhat',
            'title': 'Tìm Đường Ngắn Nhất (DAG)',
            'order': 4,
            'pass_percentage': 75,
            'theory': 'Tìm đường đi ngắn nhất trong đồ thị có hướng không có chu trình (DAG) sử dụng quy hoạch động kết hợp với sắp xếp topo. Ưu điểm: xử lý được trọng số âm (điều Dijkstra không làm được trên DAG).',
            'python_code': 'def dag_shortest_path(n, edges, start):\n    from collections import defaultdict\n    graph = defaultdict(list)\n    for u, v, w in edges:\n        graph[u].append((v, w))\n    dist = [float("inf")] * n\n    dist[start] = 0\n    for _ in range(n - 1):\n        for u, v, w in edges:\n            if dist[u] + w < dist[v]:\n                dist[v] = dist[u] + w\n    return dist'
        },
        {
            'slug': 'tim-kiem-rong',
            'title': 'Tìm Kiếm Rộng (BFS)',
            'order': 5,
            'pass_percentage': 75,
            'theory': 'Thuật toán tìm kiếm theo chiều rộng (BFS) duyệt đồ thị theo từng tầng bằng Queue. Đảm bảo tìm đường đi ngắn nhất trong đồ thị không có trọng số. Độ phức tạp O(V+E).',
            'python_code': 'from collections import deque\ndef bfs(graph, start):\n    visited = set([start])\n    queue = deque([start])\n    order = []\n    while queue:\n        node = queue.popleft()\n        order.append(node)\n        for neighbor in graph.get(node, []):\n            if neighbor not in visited:\n                visited.add(neighbor)\n                queue.append(neighbor)\n    return order'
        },
        {
            'slug': 'tim-kiem-sau',
            'title': 'Tìm Kiếm Sâu (DFS)',
            'order': 6,
            'pass_percentage': 75,
            'theory': 'Thuật toán tìm kiếm theo chiều sâu (DFS) duyệt đồ thị theo từng nhánh đến cùng trước khi quay lui. Dùng Stack (hoặc đệ quy). Ứng dụng: phát hiện chu trình, sắp xếp topo, tìm thành phần liên thông mạnh.',
            'python_code': 'def dfs(graph, start, visited=None):\n    if visited is None:\n        visited = set()\n    visited.add(start)\n    order = [start]\n    for neighbor in graph.get(start, []):\n        if neighbor not in visited:\n            order.extend(dfs(graph, neighbor, visited))\n    return order'
        },
        {
            'slug': 'tinh-so-to-hop',
            'title': 'Tính Số Tổ Hợp (Combinations)',
            'order': 7,
            'pass_percentage': 75,
            'theory': 'Tính số tổ hợp C(n,k) sử dụng quy hoạch động với tam giác Pascal. Công thức: C(n,k) = C(n-1,k-1) + C(n-1,k). Phương pháp này tránh tràn số và hiệu quả hơn tính giai thừa trực tiếp.',
            'python_code': 'def combinations(n, k):\n    dp = [[0]*(k+1) for _ in range(n+1)]\n    for i in range(n+1):\n        dp[i][0] = 1\n    for i in range(1, n+1):\n        for j in range(1, min(i,k)+1):\n            dp[i][j] = dp[i-1][j-1] + dp[i-1][j]\n    return dp[n][k]'
        },
        {
            'slug': 'xau-con-chung',
            'title': 'Xâu Con Chung Dài Nhất (LCS)',
            'order': 8,
            'pass_percentage': 75,
            'theory': 'Bài toán LCS (Longest Common Subsequence): Tìm xâu con chung dài nhất của hai xâu ký tự. Sử dụng bảng DP 2 chiều (m+1)×(n+1). Ứng dụng trong kiểm tra đạo văn, diff công cụ, so sánh DNA.',
            'python_code': 'def lcs(s1, s2):\n    m, n = len(s1), len(s2)\n    dp = [[0]*(n+1) for _ in range(m+1)]\n    for i in range(1, m+1):\n        for j in range(1, n+1):\n            if s1[i-1] == s2[j-1]:\n                dp[i][j] = dp[i-1][j-1] + 1\n            else:\n                dp[i][j] = max(dp[i-1][j], dp[i][j-1])\n    return dp[m][n]'
        },
        {
            'slug': 'xep-ba-lo',
            'title': 'Xếp Ba Lô 0/1 (Knapsack)',
            'order': 9,
            'pass_percentage': 75,
            'theory': 'Bài toán Knapsack 0/1: Mỗi vật phẩm chỉ có thể chọn hoặc không (không phân số). Tìm tập vật phẩm tối ưu sao cho tổng giá trị lớn nhất mà không vượt quá sức chứa W. Độ phức tạp O(n×W).',
            'python_code': 'def knapsack(weights, values, W):\n    n = len(weights)\n    dp = [[0]*(W+1) for _ in range(n+1)]\n    for i in range(1, n+1):\n        for w in range(W+1):\n            dp[i][w] = dp[i-1][w]\n            if weights[i-1] <= w:\n                dp[i][w] = max(dp[i][w], dp[i-1][w-weights[i-1]] + values[i-1])\n    return dp[n][W]'
        },
    ]

    from seed_data import LESSON_THEORY_EXTENDED

    for data in lessons_data:
        lesson = Lesson.query.filter_by(slug=data['slug']).first()
        if not lesson:
            lesson = Lesson(**data)
            lesson.theory_extended = LESSON_THEORY_EXTENDED.get(data['slug'], '')
            db.session.add(lesson)
        else:
            # Cập nhật các trường
            lesson.order = data['order']
            lesson.pass_percentage = data['pass_percentage']
            lesson.title = data['title']
            lesson.theory = data['theory']
            lesson.theory_extended = LESSON_THEORY_EXTENDED.get(data['slug'], '')
    db.session.commit()
    print("✅ Seeded lessons với lý thuyết chi tiết.")


    # --- Seed Quiz Questions ---
    QUIZ_DATA = {
        'doi-tien': [
            {
                'order': 1,
                'question': 'Nguyên lý nào của Quy hoạch động được áp dụng trong bài Đổi Tiền?',
                'option_a': 'Chia để trị (Divide & Conquer)',
                'option_b': 'Tối ưu con (Optimal Substructure) + Lưu kết quả trung gian',
                'option_c': 'Thuật toán Tham lam (Greedy)',
                'option_d': 'Quay lui (Backtracking)',
                'correct': 'B',
            },
            {
                'order': 2,
                'question': 'Trong mảng dp[] của bài Đổi Tiền, dp[i] đại diện cho điều gì?',
                'option_a': 'Mệnh giá xu nhỏ nhất cần dùng',
                'option_b': 'Số xu tối thiểu để đổi được i đồng',
                'option_c': 'Tổng số cách đổi i đồng',
                'option_d': 'Số lần lặp của vòng for',
                'correct': 'B',
            },
            {
                'order': 3,
                'question': 'Nếu coins = [1, 5, 6, 9] và amount = 11, số xu ít nhất là bao nhiêu?',
                'option_a': '3 xu',
                'option_b': '2 xu (5 + 6 = 11)',
                'option_c': '4 xu',
                'option_d': '1 xu',
                'correct': 'B',
            },
            {
                'order': 4,
                'question': 'Bài toán Đổi Tiền được ứng dụng thực tế trong lĩnh vực nào?',
                'option_a': 'Tối ưu hóa hệ thống ATM và máy bán hàng tự động',
                'option_b': 'Tìm kiếm trên mạng xã hội',
                'option_c': 'Nén dữ liệu hình ảnh',
                'option_d': 'Mã hóa mật khẩu',
                'correct': 'A',
            },
        ],
        'day-con-tang': [
            {
                'order': 1,
                'question': 'Độ phức tạp thời gian của thuật toán LIS cơ bản O(n²) so với thuật toán tối ưu O(n log n) là?',
                'option_a': 'Chậm hơn — O(n²) luôn tệ hơn O(n log n) với n lớn',
                'option_b': 'Nhanh hơn với mọi input',
                'option_c': 'Bằng nhau trong mọi trường hợp',
                'option_d': 'Không thể so sánh được',
                'correct': 'A',
            },
            {
                'order': 2,
                'question': 'Với mảng [3, 10, 2, 1, 20], độ dài LIS dài nhất là bao nhiêu?',
                'option_a': '2 (ví dụ: [3, 10])',
                'option_b': '3 (ví dụ: [3, 10, 20])',
                'option_c': '4 (ví dụ: [2, 1, 20, ?])',
                'option_d': '5 (toàn bộ mảng)',
                'correct': 'B',
            },
            {
                'order': 3,
                'question': 'Trong LIS cơ bản, dp[i] lưu trữ giá trị gì?',
                'option_a': 'Giá trị arr[i]',
                'option_b': 'Độ dài LIS kết thúc tại vị trí i',
                'option_c': 'Chỉ số phần tử nhỏ nhất của LIS',
                'option_d': 'Tổng các phần tử của LIS',
                'correct': 'B',
            },
            {
                'order': 4,
                'question': 'LIS được ứng dụng trong lĩnh vực thực tế nào?',
                'option_a': 'Phân tích chuỗi DNA trong Bioinformatics và phiên bản hóa tài liệu',
                'option_b': 'Tìm đường trong bản đồ',
                'option_c': 'Tính toán số nguyên tố',
                'option_d': 'Nén video trực tuyến',
                'correct': 'A',
            },
        ],
        'nhan-ma-tran': [
            {
                'order': 1,
                'question': 'Bài toán Nhân Chuỗi Ma Trận (Matrix Chain) tìm kiếm điều gì?',
                'option_a': 'Ma trận kết quả cuối cùng',
                'option_b': 'Thứ tự đặt ngoặc tối ưu để giảm số phép nhân vô hướng',
                'option_c': 'Ma trận nghịch đảo',
                'option_d': 'Định thức của tích ma trận',
                'correct': 'B',
            },
            {
                'order': 2,
                'question': 'Độ phức tạp thời gian của thuật toán Matrix Chain DP là?',
                'option_a': 'O(n)',
                'option_b': 'O(n log n)',
                'option_c': 'O(n³)',
                'option_d': 'O(2ⁿ)',
                'correct': 'C',
            },
            {
                'order': 3,
                'question': 'Nếu không dùng DP, số cách đặt ngoặc hợp lệ cho n ma trận tăng theo công thức nào?',
                'option_a': 'Tuyến tính O(n)',
                'option_b': 'Số Catalan — tăng mũ (exponential)',
                'option_c': 'Logarithm O(log n)',
                'option_d': 'Đa thức bậc 2 O(n²)',
                'correct': 'B',
            },
            {
                'order': 4,
                'question': 'Matrix Chain Multiplication ứng dụng thực tế trong lĩnh vực nào?',
                'option_a': 'Tối ưu hóa trình biên dịch (compiler) và tính toán khoa học/đồ họa 3D',
                'option_b': 'Mã hóa dữ liệu đầu cuối',
                'option_c': 'Phân loại email spam',
                'option_d': 'Tìm kiếm toàn văn bản',
                'correct': 'A',
            },
        ],
        'tim-duong-ngan-nhat': [
            {
                'order': 1,
                'question': 'DAG là viết tắt của gì và đặc trưng nổi bật nhất của nó?',
                'option_a': 'Dense Acyclic Graph — đồ thị dày đặc',
                'option_b': 'Directed Acyclic Graph — đồ thị có hướng KHÔNG có chu trình',
                'option_c': 'Dynamic Algorithm Graph — đồ thị thuật toán động',
                'option_d': 'Double Acyclic Graph — đồ thị hai chiều',
                'correct': 'B',
            },
            {
                'order': 2,
                'question': 'Ưu điểm của DAG Shortest Path so với thuật toán Dijkstra là?',
                'option_a': 'Dijkstra nhanh hơn trong mọi trường hợp',
                'option_b': 'DAG DP xử lý được trọng số âm mà Dijkstra không thể',
                'option_c': 'DAG DP cần bộ nhớ ít hơn',
                'option_d': 'Không có sự khác biệt nào',
                'correct': 'B',
            },
            {
                'order': 3,
                'question': 'Sắp xếp topo (Topological Sort) được dùng trong DAG để làm gì?',
                'option_a': 'Tìm chu trình trong đồ thị',
                'option_b': 'Đảm bảo xử lý các đỉnh theo thứ tự từ nguồn đến đích, không bỏ sót',
                'option_c': 'Sắp xếp trọng số cạnh tăng dần',
                'option_d': 'Xác định đỉnh bậc cao nhất',
                'correct': 'B',
            },
            {
                'order': 4,
                'question': 'Bài toán tìm đường ngắn nhất trên DAG có thể giải trong độ phức tạp nào?',
                'option_a': 'O(V² + E)',
                'option_b': 'O(V + E) — tuyến tính theo số đỉnh và cạnh',
                'option_c': 'O(V log V)',
                'option_d': 'O(2^V)',
                'correct': 'B',
            },
        ],
        'tim-kiem-rong': [
            {
                'order': 1,
                'question': 'BFS sử dụng cấu trúc dữ liệu nào để quản lý các đỉnh cần duyệt?',
                'option_a': 'Stack (LIFO)',
                'option_b': 'Queue (FIFO)',
                'option_c': 'Priority Queue (Min-Heap)',
                'option_d': 'Binary Tree',
                'correct': 'B',
            },
            {
                'order': 2,
                'question': 'BFS đảm bảo tìm đường đi NGẮN NHẤT trong trường hợp nào?',
                'option_a': 'Đồ thị có trọng số dương bất kỳ',
                'option_b': 'Đồ thị không có trọng số hoặc tất cả trọng số bằng nhau',
                'option_c': 'Chỉ trên cây nhị phân cân bằng',
                'option_d': 'Đồ thị đầy đủ (complete graph)',
                'correct': 'B',
            },
            {
                'order': 3,
                'question': 'BFS KHÔNG phù hợp để giải bài toán nào?',
                'option_a': 'Kiểm tra tính liên thông của đồ thị',
                'option_b': 'Tìm đường ngắn nhất trong đồ thị có trọng số KHÁC NHAU',
                'option_c': 'Duyệt theo tầng (level-order traversal)',
                'option_d': 'Kiểm tra đồ thị hai phía (bipartite)',
                'correct': 'B',
            },
            {
                'order': 4,
                'question': 'Cho đồ thị: A→B, A→C, B→D, C→D. BFS từ A duyệt theo thứ tự nào?',
                'option_a': 'A, B, D, C',
                'option_b': 'A, C, B, D',
                'option_c': 'A, B, C, D (duyệt tầng 1 xong rồi tầng 2)',
                'option_d': 'D, B, C, A',
                'correct': 'C',
            },
        ],
        'tim-kiem-sau': [
            {
                'order': 1,
                'question': 'DFS đệ quy ngầm định sử dụng cấu trúc dữ liệu nào?',
                'option_a': 'Queue (FIFO)',
                'option_b': 'Call Stack (ngăn xếp gọi hàm đệ quy)',
                'option_c': 'Priority Queue',
                'option_d': 'Linked List',
                'correct': 'B',
            },
            {
                'order': 2,
                'question': 'DFS được ứng dụng để phát hiện điều gì trong đồ thị?',
                'option_a': 'Đường đi ngắn nhất không trọng số',
                'option_b': 'Chu trình (Cycle Detection) và Thành phần liên thông mạnh (SCC)',
                'option_c': 'Đỉnh có bậc cao nhất',
                'option_d': 'Cạnh có trọng số nhỏ nhất',
                'correct': 'B',
            },
            {
                'order': 3,
                'question': 'Sắp xếp topo (Topological Sort) bằng DFS thực hiện bằng cách nào?',
                'option_a': 'Xếp các đỉnh theo thứ tự BẮT ĐẦU duyệt DFS',
                'option_b': 'Xếp ngược thứ tự KẾT THÚC duyệt DFS (finish time giảm dần)',
                'option_c': 'Sắp xếp theo bậc (degree) của đỉnh',
                'option_d': 'Sắp xếp theo trọng số cạnh',
                'correct': 'B',
            },
            {
                'order': 4,
                'question': 'Với đồ thị: A→B, A→C, B→D (DFS từ A, ưu tiên B trước C), thứ tự duyệt là?',
                'option_a': 'A, B, C, D',
                'option_b': 'A, B, D, C',
                'option_c': 'A, C, B, D',
                'option_d': 'D, B, C, A',
                'correct': 'B',
            },
        ],
        'tinh-so-to-hop': [
            {
                'order': 1,
                'question': 'Công thức truy hồi đúng của C(n,k) trong tam giác Pascal là?',
                'option_a': 'C(n,k) = C(n-1,k) + C(n-1,k+1)',
                'option_b': 'C(n,k) = C(n-1,k-1) + C(n-1,k)',
                'option_c': 'C(n,k) = C(n,k-1) × n / k',
                'option_d': 'C(n,k) = n! / (k! × (n-k)!) — không dùng truy hồi',
                'correct': 'B',
            },
            {
                'order': 2,
                'question': 'Tính C(6,2) bằng tam giác Pascal. Kết quả là?',
                'option_a': '12',
                'option_b': '30',
                'option_c': '15',
                'option_d': '20',
                'correct': 'C',
            },
            {
                'order': 3,
                'question': 'Không gian bộ nhớ của bảng DP tính C(n,k) có thể tối ưu xuống còn?',
                'option_a': 'O(n²) — bảng 2 chiều đầy đủ',
                'option_b': 'O(n×k)',
                'option_c': 'O(k) — chỉ dùng 1 mảng 1 chiều cập nhật ngược',
                'option_d': 'O(1) — tính trực tiếp',
                'correct': 'C',
            },
            {
                'order': 4,
                'question': 'Tại sao C(n,k) = C(n, n-k)?',
                'option_a': 'Vì n = k + (n-k) nên hai vế bằng nhau',
                'option_b': 'Chọn k phần tử tương đương với loại bỏ (n-k) phần tử còn lại',
                'option_c': 'Đây chỉ là quy ước toán học, không có ý nghĩa',
                'option_d': 'Vì giai thừa có tính giao hoán',
                'correct': 'B',
            },
        ],
        'xau-con-chung': [
            {
                'order': 1,
                'question': 'LCS của "ABCBDAB" và "BDCABA" có độ dài tối đa là bao nhiêu?',
                'option_a': '3',
                'option_b': '4',
                'option_c': '5',
                'option_d': '6',
                'correct': 'B',
            },
            {
                'order': 2,
                'question': 'Bảng DP trong LCS giữa chuỗi độ dài m và n có kích thước là?',
                'option_a': 'm × n',
                'option_b': '(m+1) × (n+1) — thêm hàng và cột base case bằng 0',
                'option_c': '(m-1) × (n-1)',
                'option_d': '(m+n) × (m+n)',
                'correct': 'B',
            },
            {
                'order': 3,
                'question': 'Để khôi phục (truy vết) xâu LCS từ bảng DP, ta thực hiện bằng cách nào?',
                'option_a': 'Đọc bảng từ trái sang phải, trên xuống dưới',
                'option_b': 'Trace back từ dp[m][n] về dp[0][0] theo các bước đã đặt',
                'option_c': 'Đọc đường chéo chính của bảng',
                'option_d': 'Sắp xếp lại ký tự theo thứ tự alphabet',
                'correct': 'B',
            },
            {
                'order': 4,
                'question': 'LCS được ứng dụng trong công cụ thực tế nào?',
                'option_a': 'Công cụ diff (so sánh file) và kiểm tra đạo văn, so sánh chuỗi DNA',
                'option_b': 'Tìm kiếm web (Google Search)',
                'option_c': 'Nén ảnh JPEG',
                'option_d': 'Mã hóa RSA bất đối xứng',
                'correct': 'A',
            },
        ],
        'xep-ba-lo': [
            {
                'order': 1,
                'question': 'Sự khác biệt cơ bản giữa 0/1 Knapsack và Fractional Knapsack là?',
                'option_a': '0/1 có thể lấy phân số vật phẩm; Fractional thì không',
                'option_b': '0/1 chỉ chọn hoặc không chọn nguyên vật phẩm; Fractional cho phép lấy phân số',
                'option_c': 'Cả hai đều giải bằng Greedy',
                'option_d': 'Không có sự khác biệt nào',
                'correct': 'B',
            },
            {
                'order': 2,
                'question': 'Với W=5, items: (w=2,v=3), (w=3,v=4), (w=4,v=5). Giá trị tối ưu 0/1 Knapsack là?',
                'option_a': '5 (chỉ lấy item 3)',
                'option_b': '7 (lấy item 1 + item 2: w=2+3=5, v=3+4=7)',
                'option_c': '8',
                'option_d': '9',
                'correct': 'B',
            },
            {
                'order': 3,
                'question': 'Tại sao 0/1 Knapsack được gọi là bài toán NP-khó về mặt lý thuyết?',
                'option_a': 'Vì không có thuật toán nào giải được',
                'option_b': 'Vì khi W rất lớn (pseudo-polynomial), số trường hợp cần xét có thể lên đến 2ⁿ trong trường hợp tổng quát',
                'option_c': 'Vì phải thử tất cả hoán vị vật phẩm',
                'option_d': 'Vì bộ nhớ yêu cầu vô hạn',
                'correct': 'B',
            },
            {
                'order': 4,
                'question': 'Trong bảng DP Knapsack, dp[i][w] có ý nghĩa gì?',
                'option_a': 'Trọng lượng tối thiểu của i vật phẩm đầu tiên với sức chứa w',
                'option_b': 'Giá trị tối đa khi xét i vật phẩm đầu tiên với sức chứa tối đa w',
                'option_c': 'Số vật phẩm có thể nhét vào ba lô sức chứa w',
                'option_d': 'Chỉ số vật phẩm được chọn',
                'correct': 'B',
            },
        ],
    }

    for slug, questions in QUIZ_DATA.items():
        lesson = Lesson.query.filter_by(slug=slug).first()
        if not lesson:
            continue
        existing_count = QuizQuestion.query.filter_by(lesson_id=lesson.id).count()
        if existing_count == 0:
            for q in questions:
                question = QuizQuestion(lesson_id=lesson.id, **q)
                db.session.add(question)
    db.session.commit()
    print("✅ Seeded quiz questions.")


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=app.config['DEBUG'])
