def solve_doi_tien(denominations, amount):
    C = sorted(denominations)
    n = amount
    A = [float('inf')] * (n + 1)
    S = [0] * (n + 1)
    A[0] = 0

    for i in range(1, n + 1):
        for coin in C:
            if coin <= i:
                if 1 + A[i - coin] < A[i]:
                    A[i] = 1 + A[i - coin]
                    S[i] = coin

    if A[n] == float('inf'):
        return {"success": False, "message": f"Không thể đổi chính xác {n}"}
    
    ket_qua = {}
    temp_n = n
    while temp_n > 0:
        coin = S[temp_n]
        ket_qua[coin] = ket_qua.get(coin, 0) + 1
        temp_n -= coin
        
    chi_tiet = []
    for k, v in sorted(ket_qua.items(), reverse=True):
        chi_tiet.append(f"{v} to menh gia {k}")
        
    return {
        "success": True,
        "thong_bao": f"De doi {n} can tong cong {int(A[n])} to tien",
        "tong_so_to_tien": int(A[n]),
        "chi_tiet_doi_tien": chi_tiet
    }