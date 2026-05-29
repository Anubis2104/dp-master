import collections

def solve_shortest_path_dag(n, edges, start_node):
    adj = collections.defaultdict(list)
    in_degree = [0] * n

    for u, v, w in edges:
        adj[u].append((v, w))
        in_degree[v] += 1

    queue = collections.deque([i for i in range(n) if in_degree[i] == 0])
    topo_order = []

    while queue:
        u = queue.popleft()
        topo_order.append(u)
        for v, w in adj[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                queue.append(v)

    dist = [float('inf')] * n
    dist[start_node] = 0
    parent = [-1] * n

    mo_phong = []

    for u in topo_order:
        if dist[u] != float('inf'):
            for v, w in adj[u]:
                if dist[v] > dist[u] + w:
                    dist[v] = dist[u] + w
                    parent[v] = u
                    mo_phong.append(f"Cập nhật khoảng cách đến {v} từ {u} qua cạnh {w} -> Tổng mới: {dist[v]}")

    distances = {}
    for i in range(n):
        distances[f"Nút {start_node} -> {i}"] = dist[i] if dist[i] != float('inf') else "Không thể đến"

    return {
        "success": True,
        "thu_tu_topo": topo_order,
        "khoang_cach_ngan_nhat": distances,
        "lich_su_cap_nhat": mo_phong
    }