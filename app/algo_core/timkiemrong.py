from collections import deque

def solve_bfs(tree_dict):
    if not tree_dict:
        return {"success": False, "message": "Cây rỗng"}
    
    queue = deque([tree_dict])
    res = []
    
    while queue:
        current = queue.popleft()
        res.append(current.get("value"))
        
        left = current.get("left")
        if left:
            queue.append(left)
            
        right = current.get("right")
        if right:
            queue.append(right)
            
    return {
        "success": True,
        "thu_tu_duyet_BFS": res,
        "thong_bao": "Đã duyệt cây theo chiều rộng thành công"
    }
