def solve_day_con_tang(arr):
    n = len(arr)
    if n == 0:
        return {"success": False, "message": "Day so rong"}

    L = [1] * n
    T = [-1] * n

    for i in range(n):
        for j in range(i):
            if arr[j] < arr[i] and L[j] + 1 > L[i]:
                L[i] = L[j] + 1
                T[i] = j

    max_val = max(L) if L else 0
    curr = L.index(max_val) if L else -1

    res = []
    while curr != -1:
        res.append(arr[curr])
        curr = T[curr]
    res.reverse()

    return {
        "success": True,
        "chi_tiet": f"Do dai day con tang dai nhat la: {max_val}",
        "day_con": res,
        "day_ban_dau": arr
    }