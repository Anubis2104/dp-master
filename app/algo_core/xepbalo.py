def solve_xep_ba_lo(weights, values, names, w_max):
    n_items = len(weights)
    
    dp = [0] * (w_max + 1)
    item_used = [-1] * (w_max + 1)

    for i in range(1, w_max + 1):
        for j in range(n_items):
            if weights[j] <= i:
                if dp[i - weights[j]] + values[j] > dp[i]:
                    dp[i] = dp[i - weights[j]] + values[j]
                    item_used[i] = j

    # Truy vết
    counts = [0] * n_items
    temp_W = w_max
    while temp_W > 0 and item_used[temp_W] != -1:
        idx = item_used[temp_W]
        counts[idx] += 1
        temp_W -= weights[idx]

    chi_tiet = []
    for i in range(n_items):
        if counts[i] > 0:
            chi_tiet.append(f"{names[i]} (nặng {weights[i]}kg, giá {values[i]}): cần {counts[i]} món")

    return {
        "success": True,
        "tong_gia_tri_cao_nhat": dp[w_max],
        "chi_tiet_chon_do": chi_tiet
    }