def solve_nhan_ma_tran(p):
    n = len(p) - 1
    if n <= 0:
        return {"success": False, "message": "Dữ liệu ma trận không hợp lệ"}

    dp = [[0] * n for _ in range(n)]
    trace = [[0] * n for _ in range(n)]
    mo_phong = []

    for L in range(2, n + 1):
        mo_phong.append(f"--- Nhóm có độ dài {L} ---")
        for i in range(n - L + 1):
            j = i + L - 1
            dp[i][j] = float('inf')
            for k in range(i, j):
                cost = dp[i][k] + dp[k + 1][j] + p[i] * p[k + 1] * p[j + 1]
                mo_phong.append(f"Thử ngắt tại k={k} (Ma trận {i}..{k} và {k+1}..{j}): Chi phí {cost}")
                if cost < dp[i][j]:
                    dp[i][j] = cost
                    trace[i][j] = k
            mo_phong.append(f"==> Tối ưu đoạn [{i}..{j}] là: {dp[i][j]}")

    def get_optimal_parens(i, j):
        if i == j:
            return f"A{i+1}"
        else:
            k = trace[i][j]
            left = get_optimal_parens(i, k)
            right = get_optimal_parens(k + 1, j)
            return f"({left}{right})"

    return {
        "success": True,
        "chi_phi_nho_nhat": int(dp[0][n - 1]),
        "cach_dat_ngoac": get_optimal_parens(0, n - 1),
        "mo_phong": mo_phong,
        "kich_thuoc_ma_tran": p
    }