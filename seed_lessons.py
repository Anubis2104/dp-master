import os
from run import app
from app.models import db, Lesson

def get_code(filename):
    path = os.path.join(os.path.dirname(__file__), 'app', 'algo_core', filename)
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    return ""

lessons = [
    ("doi-tien", "Đổi tiền", "Quy hoạch động (Dynamic Programming) là phương pháp giải quyết các bài toán phức tạp bằng cách chia chúng thành các bài toán con đơn giản hơn. Nó tối ưu hóa quá trình tính toán bằng cách lưu trữ kết quả của các bài toán con (thường là trong một bảng hoặc mảng) để tránh việc tính toán lại nhiều lần. Trong bài toán đổi tiền, quy hoạch động giúp ta tìm số lượng đồng xu ít nhất bằng cách xét từng số tiền từ nhỏ đến lớn.", "doitien.py"),
    ("day-con-tang", "Dãy con tăng dài nhất (LIS)", "Quy hoạch động (Dynamic Programming): Phương pháp này sử dụng một mảng để lưu độ dài dãy con tăng dài nhất kết thúc tại mỗi phần tử. Bằng cách duyệt qua các phần tử trước đó và sử dụng kết quả đã tính toán, ta có thể xây dựng giải pháp tối ưu cho toàn bộ dãy mà không cần duyệt tất cả các tổ hợp.", "day_con_tang_dai_nhat.py"),
    ("nhan-ma-tran", "Nhân chuỗi ma trận", "Quy hoạch động: Bài toán này áp dụng quy hoạch động để tìm thứ tự nhân các ma trận sao cho tổng số phép tính vô hướng là nhỏ nhất. Bằng cách tính toán chi phí nhân từ các chuỗi con nhỏ nhất (kích thước 2, 3...) và kết hợp chúng lại, ta đảm bảo luôn đạt được chi phí tối thiểu cho toàn bộ chuỗi ma trận.", "nhanmatran.py"),
    ("tim-duong-ngan-nhat", "Đường đi ngắn nhất trên DAG", "Quy hoạch động: Trên đồ thị có hướng không chu trình (DAG), ta có thể sắp xếp topo các đỉnh, sau đó cập nhật khoảng cách ngắn nhất đến các đỉnh lân cận theo thứ tự đó. Phương pháp này tận dụng tính chất không có chu trình để đảm bảo khoảng cách đến một đỉnh là tối ưu khi duyệt qua nó.", "timduongngannhat.py"),
    ("tim-kiem-rong", "Tìm kiếm theo chiều rộng (BFS)", "BFS (Breadth-First Search) duyệt cây hoặc đồ thị theo từng cấp độ, sử dụng cấu trúc dữ liệu Hàng đợi (Queue) để lưu trữ các đỉnh cần duyệt. Nó đảm bảo các đỉnh ở gần đỉnh gốc sẽ được duyệt trước.", "timkiemrong.py"),
    ("tim-kiem-sau", "Tìm kiếm theo chiều sâu (DFS)", "DFS (Depth-First Search) là thuật toán duyệt đi sâu vào nhánh con càng xa càng tốt trước khi quay lui. Nó thường được cài đặt bằng đệ quy hoặc cấu trúc dữ liệu Ngăn xếp (Stack).", "timkiemsau.py"),
    ("tinh-so-to-hop", "Tính số tổ hợp C(n, k)", "Quy hoạch động: Số tổ hợp chập k của n phần tử có thể được tính bằng công thức truy hồi C(n, k) = C(n-1, k-1) + C(n-1, k). Quy hoạch động tối ưu hóa việc tính toán này bằng cách lập bảng (như tam giác Pascal) để lưu các giá trị đã tính, tránh tính lại C(n, k) nhiều lần.", "tinhsotohop.py"),
    ("xau-con-chung", "Xâu con chung dài nhất (LCS)", "Quy hoạch động: Để tìm xâu con chung dài nhất của hai xâu, ta lập một bảng hai chiều, trong đó mỗi ô lưu độ dài xâu con chung dài nhất của tiền tố hai xâu. Bằng cách dựa vào các ô liền trước đã tính, ta thu được kết quả tối ưu mà không phải thử tất cả các xâu con.", "xauconchungnhat.py"),
    ("xep-ba-lo", "Bài toán Cái túi (0/1 Knapsack)", "Quy hoạch động: Đây là bài toán kinh điển của quy hoạch động. Để đạt giá trị lớn nhất trong giới hạn trọng lượng, ta xét từng vật phẩm và quyết định chọn hay không chọn dựa trên việc so sánh giá trị khi thêm vật phẩm đó vào phần trọng lượng còn lại so với giá trị tối ưu nếu bỏ qua nó.", "xepbalo.py")
]

with app.app_context():
    for slug, title, theory, filename in lessons:
        lesson = Lesson.query.filter_by(slug=slug).first()
        code = get_code(filename)
        if lesson:
            lesson.title = title
            lesson.theory = theory
            lesson.python_code = code
        else:
            db.session.add(Lesson(slug=slug, title=title, theory=theory, python_code=code))
    db.session.commit()
    print("Seeded successfully!")
