def solve_combinations(n, k):
    if k < 0 or n < 0:
        return {"success": False, "message": "Lỗi: n và k phải là số không âm!"}
    if k > n:
        return {"success": False, "message": f"Lỗi: k ({k}) không thể lớn hơn n ({n})!"}

    dp = [[0 for _ in range(n + 1)] for _ in range(n + 1)]
    for i in range(n + 1):
        for j in range(i + 1):
            if j == 0 or j == i:
                dp[i][j] = 1
            else:
                dp[i][j] = dp[i - 1][j - 1] + dp[i - 1][j]
                
    result = dp[n][k]
    
    # Tạo tam giác Pascal dạng bảng (như yêu cầu)
    max_val = dp[n][n // 2]
    col_width = max(len(str(max_val)) + 2, 4)  # +2 cho trường hợp có ngoặc vuông []
    label_width = len(str(n))
    
    tam_giac = []
    
    # Header
    header = " " * (label_width + 1) + "|"
    for j in range(n + 1):
        header += f"{j:>{col_width}}"
    tam_giac.append(header)
    tam_giac.append("-" * len(header))
    
    # Rows
    for i in range(n + 1):
        row_str = f"{i:<{label_width}} |"
        for j in range(n + 1):
            if j <= i:
                val = dp[i][j]
                if i == n and j == k:
                    display_val = f"[{val}]"
                    row_str += f"{display_val:>{col_width}}"
                else:
                    row_str += f"{val:>{col_width}}"
        tam_giac.append(row_str)

    return {
        "success": True,
        "ket_qua": f"C({n}, {k}) = {result}",
        "tam_giac_pascal": tam_giac
    }