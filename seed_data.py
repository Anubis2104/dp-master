# seed_data.py — Nội dung lý thuyết chi tiết cho 9 bài toán QHĐ

LESSON_THEORY_EXTENDED = {

    # =========================================================
    # BÀI 1: ĐỔI TIỀN (COIN CHANGE)
    # =========================================================
    'doi-tien': """
<div class="theory-section">
  <h3>🎯 Phát biểu bài toán</h3>
  <p>Cho một tập hợp mệnh giá tiền xu <code>coins = [c₁, c₂, ..., cₖ]</code> và một số tiền <code>amount</code>.
  Tìm <strong>số lượng xu ít nhất</strong> để tạo ra tổng bằng <code>amount</code>.
  Nếu không thể tạo ra đúng số tiền đó, trả về <code>-1</code>.</p>
  <div class="theory-example">
    <strong>Ví dụ:</strong> coins = [1, 5, 6, 9], amount = 11 → Kết quả: 2 (dùng 5 + 6)
  </div>
</div>

<div class="theory-section">
  <h3>🧩 Phân tích Quy Hoạch Động</h3>
  <p><strong>Trạng thái:</strong> <code>dp[i]</code> = số xu tối thiểu để đổi được <code>i</code> đồng.</p>
  <p><strong>Công thức truy hồi:</strong></p>
  <div class="formula-box">
    dp[0] = 0 &nbsp;&nbsp;&nbsp; (base case: 0 đồng cần 0 xu)<br>
    dp[i] = min( dp[i − coin] + 1 ) &nbsp; với mọi coin ∈ coins và coin ≤ i<br>
    dp[i] = ∞ &nbsp;&nbsp;&nbsp; nếu không thể tạo được i đồng
  </div>
  <p><strong>Tại sao đúng?</strong> Nếu đồng xu cuối cùng được dùng có mệnh giá <code>c</code>,
  thì ta cần <code>dp[i−c]</code> xu cho phần còn lại, cộng thêm 1 xu mệnh giá <code>c</code>.
  Ta chọn <code>c</code> sao cho tổng nhỏ nhất.</p>
</div>

<div class="theory-section">
  <h3>📊 Ví dụ minh họa: coins=[1,5,6,9], amount=11</h3>
  <div class="dp-table-wrap">
    <table class="dp-table">
      <tr>
        <th>i (đồng)</th>
        <td>0</td><td>1</td><td>2</td><td>3</td><td>4</td>
        <td>5</td><td>6</td><td>7</td><td>8</td><td>9</td>
        <td>10</td><td class="dp-highlight">11</td>
      </tr>
      <tr>
        <th>dp[i] (xu)</th>
        <td>0</td><td>1</td><td>2</td><td>3</td><td>4</td>
        <td>1</td><td>1</td><td>2</td><td>2</td><td>1</td>
        <td>2</td><td class="dp-highlight">2</td>
      </tr>
    </table>
  </div>
  <p>dp[11] = dp[11−6]+1 = dp[5]+1 = 1+1 = <strong>2</strong> ✓</p>
</div>

<div class="theory-section">
  <h3>⚡ Độ phức tạp</h3>
  <div class="complexity-grid">
    <div class="complexity-item">
      <span class="complexity-label">Thời gian</span>
      <span class="complexity-value">O(amount × |coins|)</span>
    </div>
    <div class="complexity-item">
      <span class="complexity-label">Không gian</span>
      <span class="complexity-value">O(amount)</span>
    </div>
  </div>
</div>

<div class="theory-section">
  <h3>🔄 Biến thể bài toán</h3>
  <ul>
    <li><strong>Coin Change II:</strong> Đếm số cách đổi (thay min bằng cộng dồn số cách)</li>
    <li><strong>Giới hạn số lần dùng:</strong> Bounded Knapsack biến thể</li>
    <li><strong>Đổi tiền với thứ tự quan trọng:</strong> Climbing Stairs / Permutation</li>
  </ul>
</div>

<div class="theory-section">
  <h3>🌍 Ứng dụng thực tế</h3>
  <ul>
    <li>Tối ưu hóa trả tiền thừa trong hệ thống ATM, máy bán hàng tự động</li>
    <li>Phân bổ nguồn lực tối thiểu trong lập lịch công việc</li>
    <li>Bài toán cắt que thép (Rod Cutting) — tối ưu hóa lợi nhuận</li>
  </ul>
</div>
""",

    # =========================================================
    # BÀI 2: DÃY CON TĂNG DÀI NHẤT (LIS)
    # =========================================================
    'day-con-tang': """
<div class="theory-section">
  <h3>🎯 Phát biểu bài toán</h3>
  <p>Cho dãy số nguyên <code>arr[0..n-1]</code>. Tìm <strong>dãy con tăng nghiêm ngặt dài nhất</strong>
  (các phần tử không cần liên tiếp, nhưng phải tăng dần và giữ nguyên thứ tự tương đối).</p>
  <div class="theory-example">
    <strong>Ví dụ:</strong> arr = [3, 10, 2, 1, 20] → LIS = [3, 10, 20], độ dài = <strong>3</strong>
  </div>
</div>

<div class="theory-section">
  <h3>🧩 Phân tích Quy Hoạch Động O(n²)</h3>
  <p><strong>Trạng thái:</strong> <code>dp[i]</code> = độ dài LIS kết thúc tại phần tử <code>arr[i]</code>.</p>
  <div class="formula-box">
    dp[i] = 1 &nbsp;&nbsp;&nbsp; (mỗi phần tử là LIS độ dài 1)<br>
    dp[i] = max( dp[j] + 1 ) &nbsp; với mọi j &lt; i và arr[j] &lt; arr[i]<br>
    Kết quả = max(dp[0], dp[1], ..., dp[n-1])
  </div>
</div>

<div class="theory-section">
  <h3>📊 Ví dụ minh họa: [3, 10, 2, 1, 20]</h3>
  <div class="dp-table-wrap">
    <table class="dp-table">
      <tr>
        <th>i</th><td>0</td><td>1</td><td>2</td><td>3</td><td>4</td>
      </tr>
      <tr>
        <th>arr[i]</th><td>3</td><td>10</td><td>2</td><td>1</td><td>20</td>
      </tr>
      <tr>
        <th>dp[i]</th><td>1</td><td>2</td><td>1</td><td>1</td><td class="dp-highlight">3</td>
      </tr>
      <tr>
        <th>Tiền tố</th><td>—</td><td>3</td><td>—</td><td>—</td><td>3,10</td>
      </tr>
    </table>
  </div>
  <p>dp[4]: arr[4]=20 > arr[0]=3 → dp[1] cũng → dp[4] = max(dp[0],dp[1])+1 = 2+1 = <strong>3</strong></p>
</div>

<div class="theory-section">
  <h3>🚀 Thuật toán tối ưu O(n log n) — Patience Sorting</h3>
  <p>Dùng mảng phụ <code>tails[]</code> duy trì dãy tăng ngắn nhất:
  với mỗi phần tử, dùng <strong>tìm kiếm nhị phân</strong> để tìm vị trí phù hợp thay thế hoặc mở rộng <code>tails</code>.</p>
  <div class="formula-box">
    Với arr[i]:<br>
    &nbsp;&nbsp;• Nếu arr[i] > tails.back() → append (kéo dài LIS)<br>
    &nbsp;&nbsp;• Ngược lại → thay thế phần tử nhỏ nhất trong tails ≥ arr[i]
  </div>
</div>

<div class="theory-section">
  <h3>⚡ Độ phức tạp</h3>
  <div class="complexity-grid">
    <div class="complexity-item">
      <span class="complexity-label">DP O(n²)</span>
      <span class="complexity-value">Thời gian: O(n²) / Không gian: O(n)</span>
    </div>
    <div class="complexity-item">
      <span class="complexity-label">Patience Sort</span>
      <span class="complexity-value">Thời gian: O(n log n) / Không gian: O(n)</span>
    </div>
  </div>
</div>

<div class="theory-section">
  <h3>🌍 Ứng dụng thực tế</h3>
  <ul>
    <li>So sánh chuỗi DNA trong Bioinformatics (evolutionary alignment)</li>
    <li>Phân tích xu hướng dữ liệu chuỗi thời gian (stock market)</li>
    <li>Bài toán xếp hộp (Box Stacking) — bài toán 3D mở rộng của LIS</li>
    <li>Bài toán lịch trình tàu (Train scheduling) — Dilworth's theorem</li>
  </ul>
</div>
""",

    # =========================================================
    # BÀI 3: NHÂN CHUỖI MA TRẬN (MATRIX CHAIN)
    # =========================================================
    'nhan-ma-tran': """
<div class="theory-section">
  <h3>🎯 Phát biểu bài toán</h3>
  <p>Cho <code>n</code> ma trận <code>A₁, A₂, ..., Aₙ</code> với kích thước tương ứng
  <code>p[0]×p[1], p[1]×p[2], ..., p[n-1]×p[n]</code>.
  Tìm <strong>thứ tự đặt ngoặc tối ưu</strong> sao cho số phép nhân vô hướng là <em>ít nhất</em>.</p>
  <div class="theory-example">
    <strong>Lưu ý:</strong> Kết quả ma trận không đổi, chỉ có chi phí tính toán thay đổi.<br>
    <strong>Ví dụ:</strong> A(10×30), B(30×5), C(5×60)<br>
    (AB)C: 10×30×5 + 10×5×60 = 1500 + 3000 = <strong>4500</strong> phép nhân<br>
    A(BC): 30×5×60 + 10×30×60 = 9000 + 18000 = <strong>27000</strong> phép nhân
  </div>
</div>

<div class="theory-section">
  <h3>🧩 Phân tích Quy Hoạch Động</h3>
  <p><strong>Trạng thái:</strong> <code>dp[i][j]</code> = chi phí tối thiểu để nhân dãy ma trận từ <code>Aᵢ</code> đến <code>Aⱼ</code>.</p>
  <div class="formula-box">
    dp[i][i] = 0 &nbsp;&nbsp;&nbsp; (1 ma trận, không cần nhân)<br>
    dp[i][j] = min( dp[i][k] + dp[k+1][j] + p[i]×p[k+1]×p[j+1] )<br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; với k = i, i+1, ..., j-1
  </div>
  <p><strong>Ý nghĩa:</strong> Ta "tách" tại vị trí k: nhân A[i..k] trước (chi phí dp[i][k]),
  nhân A[k+1..j] sau (chi phí dp[k+1][j]), rồi nhân hai kết quả lại (chi phí p[i]×p[k+1]×p[j+1]).</p>
</div>

<div class="theory-section">
  <h3>📊 Ví dụ minh họa: p = [10, 30, 5, 60]</h3>
  <p>3 ma trận: A₀(10×30), A₁(30×5), A₂(5×60)</p>
  <div class="dp-table-wrap">
    <table class="dp-table">
      <tr><th>dp[i][j]</th><th>j=0</th><th>j=1</th><th>j=2</th></tr>
      <tr><th>i=0</th><td>0</td><td>1500</td><td class="dp-highlight">4500</td></tr>
      <tr><th>i=1</th><td>—</td><td>0</td><td>9000</td></tr>
      <tr><th>i=2</th><td>—</td><td>—</td><td>0</td></tr>
    </table>
  </div>
  <p>dp[0][2]: k=0: dp[0][0]+dp[1][2]+10×30×60=0+9000+18000=27000; k=1: 1500+0+10×5×60=<strong>4500</strong> ✓</p>
</div>

<div class="theory-section">
  <h3>⚡ Độ phức tạp</h3>
  <div class="complexity-grid">
    <div class="complexity-item">
      <span class="complexity-label">Thời gian</span>
      <span class="complexity-value">O(n³)</span>
    </div>
    <div class="complexity-item">
      <span class="complexity-label">Không gian</span>
      <span class="complexity-value">O(n²)</span>
    </div>
    <div class="complexity-item">
      <span class="complexity-label">Brute force</span>
      <span class="complexity-value">O(4ⁿ/n^1.5) — Số Catalan</span>
    </div>
  </div>
</div>

<div class="theory-section">
  <h3>🔢 Số Catalan và tại sao DP cần thiết</h3>
  <p>Số cách đặt ngoặc cho n ma trận bằng số Catalan C(n-1):
  C(1)=1, C(2)=2, C(3)=5, C(4)=14, C(5)=42, C(10)=4862, C(20)≈6 tỷ.
  Brute force hoàn toàn không khả thi khi n lớn!</p>
</div>

<div class="theory-section">
  <h3>🌍 Ứng dụng thực tế</h3>
  <ul>
    <li>Tối ưu trình biên dịch khi tính toán biểu thức ma trận (MATLAB, NumPy)</li>
    <li>Đồ họa 3D: chuỗi phép biến đổi ma trận (rotation, translation, scale)</li>
    <li>Machine Learning: tối ưu lan truyền ngược (backpropagation)</li>
    <li>Xử lý ngôn ngữ tự nhiên: CYK Parsing Algorithm</li>
  </ul>
</div>
""",

    # =========================================================
    # BÀI 4: TÌM ĐƯỜNG NGẮN NHẤT TRÊN DAG
    # =========================================================
    'tim-duong-ngan-nhat': """
<div class="theory-section">
  <h3>🎯 Phát biểu bài toán</h3>
  <p>Cho đồ thị có hướng không có chu trình (DAG — Directed Acyclic Graph) với n đỉnh, các cạnh có trọng số
  (có thể âm). Tìm <strong>đường đi ngắn nhất</strong> từ đỉnh nguồn <code>s</code> đến tất cả các đỉnh còn lại.</p>
</div>

<div class="theory-section">
  <h3>🧩 Tại sao dùng DP trên DAG?</h3>
  <p>DAG không có chu trình → có thể sắp xếp topo → đảm bảo thứ tự xử lý nhất quán.
  Đặc biệt, không cần điều kiện trọng số dương như Dijkstra — <strong>DAG DP xử lý được trọng số âm</strong>.</p>
  <div class="formula-box">
    dist[s] = 0<br>
    dist[v] = min( dist[u] + w(u,v) ) với mọi cạnh (u→v) trong topo-order<br>
    dist[v] = ∞ nếu chưa thể đến v
  </div>
</div>

<div class="theory-section">
  <h3>📊 Quy trình giải</h3>
  <ol class="theory-steps">
    <li><strong>Sắp xếp topo:</strong> Sắp xếp các đỉnh theo thứ tự topo (DFS hoặc Kahn's algorithm)</li>
    <li><strong>Khởi tạo:</strong> dist[s]=0, dist[v]=∞ với v≠s</li>
    <li><strong>Relaxation:</strong> Duyệt theo thứ tự topo, với mỗi đỉnh u, cập nhật dist[v] cho mọi cạnh u→v</li>
    <li><strong>Kết quả:</strong> dist[] chứa khoảng cách ngắn nhất từ s đến mọi đỉnh</li>
  </ol>
</div>

<div class="theory-section">
  <h3>📊 Ví dụ minh họa</h3>
  <div class="theory-example">
    Đồ thị: 0→1(3), 0→2(6), 1→2(4), 1→3(4), 2→3(-1), 3→4(2)<br>
    Thứ tự topo: 0, 1, 2, 3, 4<br>
    dist: [0, 3, 6→7?, 6→min(7,6-1=5), 7]<br>
    Sau xử lý: dist = [0, 3, 6, 5, 7]
  </div>
</div>

<div class="theory-section">
  <h3>⚡ Độ phức tạp</h3>
  <div class="complexity-grid">
    <div class="complexity-item">
      <span class="complexity-label">Thời gian</span>
      <span class="complexity-value">O(V + E) — tuyến tính!</span>
    </div>
    <div class="complexity-item">
      <span class="complexity-label">Không gian</span>
      <span class="complexity-value">O(V + E)</span>
    </div>
    <div class="complexity-item">
      <span class="complexity-label">So với Dijkstra</span>
      <span class="complexity-value">O((V+E) log V) — DAG nhanh hơn</span>
    </div>
    <div class="complexity-item">
      <span class="complexity-label">So với Bellman-Ford</span>
      <span class="complexity-value">O(VE) — DAG nhanh hơn nhiều</span>
    </div>
  </div>
</div>

<div class="theory-section">
  <h3>🔍 So sánh các thuật toán Shortest Path</h3>
  <div class="dp-table-wrap">
    <table class="dp-table">
      <tr><th>Thuật toán</th><th>Trọng số âm</th><th>Chu trình</th><th>Độ phức tạp</th></tr>
      <tr><td>Dijkstra</td><td>❌</td><td>✅</td><td>O((V+E)logV)</td></tr>
      <tr><td>Bellman-Ford</td><td>✅</td><td>✅</td><td>O(VE)</td></tr>
      <tr><td><strong>DAG DP</strong></td><td>✅</td><td>❌ (DAG only)</td><td><strong>O(V+E)</strong></td></tr>
      <tr><td>Floyd-Warshall</td><td>✅</td><td>✅</td><td>O(V³)</td></tr>
    </table>
  </div>
</div>

<div class="theory-section">
  <h3>🌍 Ứng dụng thực tế</h3>
  <ul>
    <li>Quản lý dự án: CPM (Critical Path Method) — tìm đường găng</li>
    <li>Lập lịch công việc phụ thuộc nhau (task dependency scheduling)</li>
    <li>Tính toán lan truyền trong mạng nơ-ron (feedforward neural network)</li>
    <li>Routing trong mạng viễn thông không có vòng lặp</li>
  </ul>
</div>
""",

    # =========================================================
    # BÀI 5: TÌM KIẾM RỘNG (BFS)
    # =========================================================
    'tim-kiem-rong': """
<div class="theory-section">
  <h3>🎯 Tổng quan thuật toán BFS</h3>
  <p>BFS (Breadth-First Search — Tìm kiếm theo chiều rộng) là thuật toán duyệt đồ thị theo từng <strong>tầng (level)</strong>,
  xử lý tất cả đỉnh ở tầng k trước khi chuyển sang tầng k+1.
  BFS sử dụng <strong>Hàng đợi (Queue — FIFO)</strong> làm cấu trúc dữ liệu chính.</p>
</div>

<div class="theory-section">
  <h3>🧩 Quy trình BFS</h3>
  <ol class="theory-steps">
    <li>Khởi tạo: đẩy đỉnh bắt đầu vào Queue, đánh dấu đã thăm</li>
    <li>Lặp khi Queue không rỗng:
      <ul>
        <li>Lấy (dequeue) đỉnh u ở đầu hàng đợi</li>
        <li>Xử lý đỉnh u</li>
        <li>Với mỗi đỉnh v kề u chưa thăm: đánh dấu đã thăm, đẩy v vào Queue</li>
      </ul>
    </li>
  </ol>
  <div class="formula-box">
    Khoảng cách ngắn nhất (không trọng số):<br>
    dist[start] = 0<br>
    dist[v] = dist[u] + 1 &nbsp; khi phát hiện v từ u lần đầu tiên
  </div>
</div>

<div class="theory-section">
  <h3>📊 Ví dụ minh họa</h3>
  <div class="theory-example">
    Đồ thị: A-B, A-C, B-D, B-E, C-F<br>
    BFS từ A:<br>
    Tầng 0: A<br>
    Tầng 1: B, C<br>
    Tầng 2: D, E, F<br>
    Thứ tự duyệt: A → B → C → D → E → F
  </div>
</div>

<div class="theory-section">
  <h3>⚡ Độ phức tạp</h3>
  <div class="complexity-grid">
    <div class="complexity-item">
      <span class="complexity-label">Thời gian</span>
      <span class="complexity-value">O(V + E)</span>
    </div>
    <div class="complexity-item">
      <span class="complexity-label">Không gian</span>
      <span class="complexity-value">O(V) — cho queue và visited</span>
    </div>
  </div>
</div>

<div class="theory-section">
  <h3>🔑 Tính chất quan trọng của BFS</h3>
  <ul>
    <li><strong>Đường đi ngắn nhất (unweighted):</strong> BFS đảm bảo tìm được đường đi ít cạnh nhất từ nguồn đến đích</li>
    <li><strong>Đầy đủ (Complete):</strong> Nếu đường đi tồn tại, BFS luôn tìm thấy</li>
    <li><strong>Không tối ưu</strong> khi đồ thị có trọng số khác nhau (dùng Dijkstra thay thế)</li>
    <li><strong>Phù hợp</strong> với đồ thị có chiều sâu lớn (tránh tràn stack của DFS)</li>
  </ul>
</div>

<div class="theory-section">
  <h3>🔍 BFS vs DFS</h3>
  <div class="dp-table-wrap">
    <table class="dp-table">
      <tr><th>Tiêu chí</th><th>BFS</th><th>DFS</th></tr>
      <tr><td>Cấu trúc DL</td><td>Queue (FIFO)</td><td>Stack/Recursion</td></tr>
      <tr><td>Duyệt theo</td><td>Tầng (Level)</td><td>Nhánh (Branch)</td></tr>
      <tr><td>Đường ngắn nhất</td><td>✅ (unweighted)</td><td>❌</td></tr>
      <tr><td>Phát hiện chu trình</td><td>✅</td><td>✅</td></tr>
      <tr><td>Bộ nhớ tệ nhất</td><td>O(V) — đồ thị rộng</td><td>O(V) — đồ thị sâu</td></tr>
    </table>
  </div>
</div>

<div class="theory-section">
  <h3>🌍 Ứng dụng thực tế</h3>
  <ul>
    <li>Tìm đường ngắn nhất trong mê cung, bản đồ (Google Maps với cạnh không trọng số)</li>
    <li>Mạng xã hội: tìm "Degrees of Separation" (6 bậc phân cách)</li>
    <li>Web crawling: duyệt và lập chỉ mục trang web</li>
    <li>Giải Rubik's Cube và các bài toán trạng thái</li>
    <li>Kiểm tra đồ thị hai phía (Bipartite Check)</li>
  </ul>
</div>
""",

    # =========================================================
    # BÀI 6: TÌM KIẾM SÂU (DFS)
    # =========================================================
    'tim-kiem-sau': """
<div class="theory-section">
  <h3>🎯 Tổng quan thuật toán DFS</h3>
  <p>DFS (Depth-First Search — Tìm kiếm theo chiều sâu) là thuật toán duyệt đồ thị theo từng <strong>nhánh</strong>,
  đi sâu nhất có thể trước khi quay lui (backtrack).
  DFS sử dụng <strong>Ngăn xếp (Stack)</strong> — ngầm định qua đệ quy, hoặc tường minh.</p>
</div>

<div class="theory-section">
  <h3>🧩 Quy trình DFS (Đệ quy)</h3>
  <div class="formula-box">
    DFS(u):<br>
    &nbsp;&nbsp;1. Đánh dấu u đã thăm<br>
    &nbsp;&nbsp;2. Xử lý u (in ra, ghi nhớ, ...)<br>
    &nbsp;&nbsp;3. Với mỗi đỉnh v kề u chưa thăm:<br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;DFS(v) &nbsp; // đệ quy đi sâu
  </div>
</div>

<div class="theory-section">
  <h3>📊 Các loại cạnh trong DFS</h3>
  <p>DFS phân loại cạnh đồ thị có hướng thành 4 loại:</p>
  <div class="dp-table-wrap">
    <table class="dp-table">
      <tr><th>Loại cạnh</th><th>Ký hiệu</th><th>Ý nghĩa</th></tr>
      <tr><td>Tree Edge</td><td>→</td><td>Cạnh trong cây DFS</td></tr>
      <tr><td>Back Edge</td><td>↺</td><td>Về đỉnh tổ tiên → CHỈ THỊ CÓ CHU TRÌNH</td></tr>
      <tr><td>Forward Edge</td><td>↘</td><td>Về đỉnh con không trực tiếp</td></tr>
      <tr><td>Cross Edge</td><td>→</td><td>Sang nhánh DFS khác</td></tr>
    </table>
  </div>
</div>

<div class="theory-section">
  <h3>🔑 Thứ tự thăm trong DFS</h3>
  <p>Mỗi đỉnh có 2 timestamp quan trọng:</p>
  <ul>
    <li><code>discovery[u]</code>: thời điểm bắt đầu duyệt u</li>
    <li><code>finish[u]</code>: thời điểm kết thúc duyệt u (đã duyệt xong tất cả con của u)</li>
  </ul>
  <p><strong>Sắp xếp topo</strong> = xếp các đỉnh theo <code>finish[]</code> <em>giảm dần</em> → ứng dụng quan trọng nhất của DFS!</p>
</div>

<div class="theory-section">
  <h3>⚡ Độ phức tạp</h3>
  <div class="complexity-grid">
    <div class="complexity-item">
      <span class="complexity-label">Thời gian</span>
      <span class="complexity-value">O(V + E)</span>
    </div>
    <div class="complexity-item">
      <span class="complexity-label">Không gian</span>
      <span class="complexity-value">O(V) — call stack tối đa</span>
    </div>
  </div>
</div>

<div class="theory-section">
  <h3>🌍 Ứng dụng thực tế</h3>
  <ul>
    <li><strong>Phát hiện chu trình</strong> trong đồ thị có hướng</li>
    <li><strong>Sắp xếp topo</strong>: xây dựng thứ tự biên dịch (Makefile dependencies)</li>
    <li><strong>Thành phần liên thông mạnh (SCC)</strong>: thuật toán Tarjan, Kosaraju</li>
    <li><strong>Giải mê cung</strong> và bài toán quay lui (N-Queens, Sudoku)</li>
    <li><strong>Cây khung nhỏ nhất</strong> (tham gia với union-find)</li>
  </ul>
</div>
""",

    # =========================================================
    # BÀI 7: TÍNH SỐ TỔ HỢP (COMBINATIONS)
    # =========================================================
    'tinh-so-to-hop': """
<div class="theory-section">
  <h3>🎯 Phát biểu bài toán</h3>
  <p>Tính số tổ hợp <code>C(n, k)</code> — số cách chọn <code>k</code> phần tử từ tập <code>n</code> phần tử
  (không quan tâm thứ tự). Công thức toán học:</p>
  <div class="formula-box">
    C(n, k) = n! / (k! × (n-k)!)
  </div>
  <p>Tuy nhiên, tính trực tiếp bằng giai thừa dễ <strong>tràn số</strong> (overflow) với n lớn.
  QHĐ sử dụng <strong>Tam giác Pascal</strong> giải quyết vấn đề này.</p>
</div>

<div class="theory-section">
  <h3>🧩 Tam giác Pascal và công thức truy hồi</h3>
  <p>Dựa trên danh tính Pascal:</p>
  <div class="formula-box">
    C(n, 0) = C(n, n) = 1 &nbsp;&nbsp;&nbsp; (base case)<br>
    C(n, k) = C(n-1, k-1) + C(n-1, k)
  </div>
  <p><strong>Ý nghĩa tổ hợp:</strong> Xét phần tử thứ n: hoặc ta <em>chọn</em> nó (cần chọn thêm k-1 từ n-1 phần tử còn lại),
  hoặc ta <em>không chọn</em> (cần chọn k từ n-1 phần tử còn lại).</p>
</div>

<div class="theory-section">
  <h3>📊 Tam giác Pascal (n=0..5)</h3>
  <div class="dp-table-wrap">
    <table class="dp-table">
      <tr><th>n\k</th><th>0</th><th>1</th><th>2</th><th>3</th><th>4</th><th>5</th></tr>
      <tr><th>0</th><td>1</td><td></td><td></td><td></td><td></td><td></td></tr>
      <tr><th>1</th><td>1</td><td>1</td><td></td><td></td><td></td><td></td></tr>
      <tr><th>2</th><td>1</td><td>2</td><td>1</td><td></td><td></td><td></td></tr>
      <tr><th>3</th><td>1</td><td>3</td><td>3</td><td>1</td><td></td><td></td></tr>
      <tr><th>4</th><td>1</td><td>4</td><td>6</td><td>4</td><td>1</td><td></td></tr>
      <tr><th>5</th><td>1</td><td>5</td><td>10</td><td>10</td><td>5</td><td class="dp-highlight">1</td></tr>
    </table>
  </div>
  <p>C(5,2) = C(4,1) + C(4,2) = 4 + 6 = <strong>10</strong> ✓</p>
</div>

<div class="theory-section">
  <h3>🚀 Tối ưu không gian O(k)</h3>
  <p>Thay vì dùng bảng 2D (n+1)×(k+1), ta chỉ cần 1 mảng 1D và cập nhật <em>ngược từ k về 0</em>:</p>
  <div class="formula-box">
    dp[0] = 1<br>
    for i in range(1, n+1):<br>
    &nbsp;&nbsp;for j in range(min(i,k), 0, -1): &nbsp; // ngược từ k về 1<br>
    &nbsp;&nbsp;&nbsp;&nbsp;dp[j] += dp[j-1]
  </div>
</div>

<div class="theory-section">
  <h3>⚡ Độ phức tạp</h3>
  <div class="complexity-grid">
    <div class="complexity-item">
      <span class="complexity-label">Thời gian</span>
      <span class="complexity-value">O(n × k)</span>
    </div>
    <div class="complexity-item">
      <span class="complexity-label">Không gian (2D)</span>
      <span class="complexity-value">O(n × k)</span>
    </div>
    <div class="complexity-item">
      <span class="complexity-label">Không gian (tối ưu)</span>
      <span class="complexity-value">O(k)</span>
    </div>
  </div>
</div>

<div class="theory-section">
  <h3>🌍 Ứng dụng thực tế</h3>
  <ul>
    <li>Xác suất & thống kê: tính phân phối nhị thức B(n,p)</li>
    <li>Mật mã học: số hệ số trong khai triển đa thức (binomial theorem)</li>
    <li>Bài toán đếm: Catalan numbers, Stirling numbers</li>
    <li>Đa thức nội suy Lagrange và bài toán tối ưu tổ hợp</li>
    <li>Coin Change II (đếm số cách): biến thể trực tiếp</li>
  </ul>
</div>
""",

    # =========================================================
    # BÀI 8: XÂU CON CHUNG DÀI NHẤT (LCS)
    # =========================================================
    'xau-con-chung': """
<div class="theory-section">
  <h3>🎯 Phát biểu bài toán</h3>
  <p>Cho hai xâu <code>s1</code> độ dài <code>m</code> và <code>s2</code> độ dài <code>n</code>.
  Tìm <strong>xâu con chung dài nhất (LCS)</strong> — xâu con xuất hiện trong cả hai xâu
  (không cần liên tiếp, nhưng giữ thứ tự tương đối).</p>
  <div class="theory-example">
    <strong>Ví dụ:</strong> s1 = "ABCBDAB", s2 = "BDCABA"<br>
    LCS = "BCAB" hoặc "BDAB" → độ dài = <strong>4</strong>
  </div>
</div>

<div class="theory-section">
  <h3>🧩 Phân tích Quy Hoạch Động</h3>
  <p><strong>Trạng thái:</strong> <code>dp[i][j]</code> = độ dài LCS của <code>s1[0..i-1]</code> và <code>s2[0..j-1]</code>.</p>
  <div class="formula-box">
    dp[i][0] = dp[0][j] = 0 &nbsp;&nbsp;&nbsp; (base case: xâu rỗng)<br>
    Nếu s1[i-1] == s2[j-1]:<br>
    &nbsp;&nbsp;dp[i][j] = dp[i-1][j-1] + 1<br>
    Nếu s1[i-1] != s2[j-1]:<br>
    &nbsp;&nbsp;dp[i][j] = max(dp[i-1][j], dp[i][j-1])
  </div>
</div>

<div class="theory-section">
  <h3>📊 Ví dụ minh họa: "ABCB" và "BCB"</h3>
  <div class="dp-table-wrap">
    <table class="dp-table">
      <tr><th>dp[i][j]</th><th>""</th><th>B</th><th>C</th><th>B</th></tr>
      <tr><th>""</th><td>0</td><td>0</td><td>0</td><td>0</td></tr>
      <tr><th>A</th><td>0</td><td>0</td><td>0</td><td>0</td></tr>
      <tr><th>B</th><td>0</td><td>1</td><td>1</td><td>1</td></tr>
      <tr><th>C</th><td>0</td><td>1</td><td>2</td><td>2</td></tr>
      <tr><th>B</th><td>0</td><td>1</td><td>2</td><td class="dp-highlight">3</td></tr>
    </table>
  </div>
  <p>LCS("ABCB","BCB") = 3 → "BCB" ✓</p>
</div>

<div class="theory-section">
  <h3>🔄 Truy vết (Traceback) để tìm xâu LCS</h3>
  <p>Từ ô <code>dp[m][n]</code>, truy ngược:</p>
  <ul>
    <li>Nếu <code>s1[i-1] == s2[j-1]</code>: ký tự này thuộc LCS, đi chéo về <code>dp[i-1][j-1]</code></li>
    <li>Nếu <code>dp[i-1][j] > dp[i][j-1]</code>: đi lên <code>dp[i-1][j]</code></li>
    <li>Ngược lại: đi sang trái <code>dp[i][j-1]</code></li>
  </ul>
</div>

<div class="theory-section">
  <h3>⚡ Độ phức tạp</h3>
  <div class="complexity-grid">
    <div class="complexity-item">
      <span class="complexity-label">Thời gian</span>
      <span class="complexity-value">O(m × n)</span>
    </div>
    <div class="complexity-item">
      <span class="complexity-label">Không gian</span>
      <span class="complexity-value">O(m × n) hoặc O(min(m,n))</span>
    </div>
  </div>
</div>

<div class="theory-section">
  <h3>🔗 Mối liên hệ với bài toán khác</h3>
  <ul>
    <li><strong>Shortest Edit Distance (Levenshtein):</strong> số lần insert/delete để biến s1 thành s2</li>
    <li><strong>LCS → LIS:</strong> LCS của A và sort(A) = LIS của A</li>
    <li><strong>Diff (Unix):</strong> Thuật toán diff giữa 2 file văn bản dựa trên LCS</li>
  </ul>
</div>

<div class="theory-section">
  <h3>🌍 Ứng dụng thực tế</h3>
  <ul>
    <li>Công cụ <code>diff</code>: so sánh phiên bản file, Git diff, code review</li>
    <li>Kiểm tra đạo văn (plagiarism detection)</li>
    <li>Bioinformatics: so sánh chuỗi DNA, protein alignment</li>
    <li>Spell checker: tìm từ gần nhất</li>
  </ul>
</div>
""",

    # =========================================================
    # BÀI 9: XẾP BA LÔ 0/1 (KNAPSACK)
    # =========================================================
    'xep-ba-lo': """
<div class="theory-section">
  <h3>🎯 Phát biểu bài toán</h3>
  <p>Có <code>n</code> vật phẩm, vật thứ <code>i</code> có trọng lượng <code>w[i]</code> và giá trị <code>v[i]</code>.
  Ba lô chứa được tối đa <code>W</code> đơn vị trọng lượng.
  Mỗi vật <strong>chỉ được lấy hoặc không lấy</strong> (không phân số).
  Tối đa hóa <strong>tổng giá trị</strong> trong ba lô.</p>
  <div class="theory-example">
    <strong>Ví dụ:</strong> W=5, vật: (w=2,v=3), (w=3,v=4), (w=4,v=5)<br>
    Chọn vật 1+2: w=2+3=5 ≤ W, v=3+4=<strong>7</strong> (tối ưu)
  </div>
</div>

<div class="theory-section">
  <h3>🧩 Phân tích Quy Hoạch Động</h3>
  <p><strong>Trạng thái:</strong> <code>dp[i][w]</code> = giá trị tối đa khi xét <code>i</code> vật đầu tiên với sức chứa <code>w</code>.</p>
  <div class="formula-box">
    dp[0][w] = 0 &nbsp;&nbsp;&nbsp; (không có vật nào)<br>
    dp[i][w] = dp[i-1][w] &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; (không lấy vật i)<br>
    dp[i][w] = max(dp[i-1][w], dp[i-1][w-wᵢ] + vᵢ) &nbsp; nếu wᵢ ≤ w (lấy hoặc không)
  </div>
</div>

<div class="theory-section">
  <h3>📊 Ví dụ minh họa: W=5, 3 vật</h3>
  <div class="dp-table-wrap">
    <table class="dp-table">
      <tr>
        <th>dp[i][w]</th>
        <th>w=0</th><th>w=1</th><th>w=2</th><th>w=3</th><th>w=4</th><th>w=5</th>
      </tr>
      <tr>
        <th>i=0 (none)</th>
        <td>0</td><td>0</td><td>0</td><td>0</td><td>0</td><td>0</td>
      </tr>
      <tr>
        <th>i=1 (w=2,v=3)</th>
        <td>0</td><td>0</td><td>3</td><td>3</td><td>3</td><td>3</td>
      </tr>
      <tr>
        <th>i=2 (w=3,v=4)</th>
        <td>0</td><td>0</td><td>3</td><td>4</td><td>4</td><td class="dp-highlight">7</td>
      </tr>
      <tr>
        <th>i=3 (w=4,v=5)</th>
        <td>0</td><td>0</td><td>3</td><td>4</td><td>5</td><td class="dp-highlight">7</td>
      </tr>
    </table>
  </div>
  <p>dp[2][5] = max(dp[1][5], dp[1][2]+4) = max(3, 3+4) = <strong>7</strong> ✓</p>
</div>

<div class="theory-section">
  <h3>🚀 Tối ưu không gian O(W)</h3>
  <p>Dùng 1 mảng 1D, cập nhật <em>ngược từ W về 0</em> để tránh sử dụng lại vật phẩm:</p>
  <div class="formula-box">
    for i in range(n):<br>
    &nbsp;&nbsp;for w in range(W, w[i]-1, -1): &nbsp; // NGƯỢC để đảm bảo 0/1<br>
    &nbsp;&nbsp;&nbsp;&nbsp;dp[w] = max(dp[w], dp[w-w[i]] + v[i])
  </div>
  <p>⚠️ Nếu cập nhật xuôi (từ nhỏ đến lớn) → thành Unbounded Knapsack (lấy vô hạn lần)!</p>
</div>

<div class="theory-section">
  <h3>⚡ Độ phức tạp</h3>
  <div class="complexity-grid">
    <div class="complexity-item">
      <span class="complexity-label">Thời gian</span>
      <span class="complexity-value">O(n × W) — Pseudo-polynomial</span>
    </div>
    <div class="complexity-item">
      <span class="complexity-label">Không gian (2D)</span>
      <span class="complexity-value">O(n × W)</span>
    </div>
    <div class="complexity-item">
      <span class="complexity-label">Không gian (1D)</span>
      <span class="complexity-value">O(W)</span>
    </div>
    <div class="complexity-item">
      <span class="complexity-label">Lý thuyết</span>
      <span class="complexity-value">NP-hard (khi W là số lớn)</span>
    </div>
  </div>
</div>

<div class="theory-section">
  <h3>🔍 So sánh các biến thể Knapsack</h3>
  <div class="dp-table-wrap">
    <table class="dp-table">
      <tr><th>Biến thể</th><th>Giới hạn</th><th>Cập nhật</th><th>Độ phức tạp</th></tr>
      <tr><td><strong>0/1 Knapsack</strong></td><td>Mỗi vật ≤ 1 lần</td><td>Ngược (W → 0)</td><td>O(nW)</td></tr>
      <tr><td>Bounded Knapsack</td><td>Vật i ≤ kᵢ lần</td><td>Ngược + đếm</td><td>O(nW)</td></tr>
      <tr><td>Unbounded Knapsack</td><td>Vô hạn lần</td><td>Xuôi (0 → W)</td><td>O(nW)</td></tr>
      <tr><td>Fractional Knapsack</td><td>Lấy phân số</td><td>Greedy</td><td>O(n log n)</td></tr>
    </table>
  </div>
</div>

<div class="theory-section">
  <h3>🌍 Ứng dụng thực tế</h3>
  <ul>
    <li>Quản lý ngân sách đầu tư: chọn dự án tối ưu trong giới hạn ngân sách</li>
    <li>Cắt tải (load shedding) trong hệ thống điện</li>
    <li>Chọn cổ phiếu trong danh mục đầu tư (Portfolio optimization)</li>
    <li>Đóng gói hàng hóa vận chuyển tối ưu (cargo loading)</li>
    <li>Mật mã học: Merkle-Hellman knapsack cryptosystem</li>
  </ul>
</div>
""",
}
