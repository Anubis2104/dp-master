def solve_dfs(tree_dict):
    if not tree_dict:
        return {"success": False, "message": "Cây rỗng"}
        
    res = []
    def dfs_preorder(node):
        if not node:
            return
        res.append(node.get("value"))
        dfs_preorder(node.get("left"))
        dfs_preorder(node.get("right"))
        
    dfs_preorder(tree_dict)
    
    return {
        "success": True,
        "thu_tu_duyet_DFS": res,
        "thong_bao": "Đã duyệt cây theo chiều sâu (Preorder) thành công"
    }
