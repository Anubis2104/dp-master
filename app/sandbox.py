"""
Module sandbox: Kiểm tra bảo mật code Python trước khi thực thi.
Sử dụng AST (Abstract Syntax Tree) để phân tích và chặn các pattern nguy hiểm.
"""
import ast

# Danh sách module bị cấm (truy cập hệ thống, mạng, file...)
BLOCKED_MODULES = frozenset({
    'os', 'sys', 'subprocess', 'shutil', 'socket', 'http', 'urllib',
    'requests', 'ftplib', 'smtplib', 'ctypes', 'multiprocessing',
    'threading', 'signal', 'importlib', 'pkgutil', 'code', 'codeop',
    'compileall', 'py_compile', 'pathlib', 'glob', 'tempfile',
    'fileinput', 'pickle', 'shelve', 'marshal', 'dbm', 'sqlite3',
    'webbrowser', 'antigravity', 'turtle', 'tkinter', 'builtins',
})

# Danh sách hàm built-in bị cấm
BLOCKED_BUILTINS = frozenset({
    'exec', 'eval', 'compile', '__import__', 'globals', 'locals',
    'getattr', 'setattr', 'delattr', 'open', 'input', 'breakpoint',
    'exit', 'quit',
})

# Danh sách thuộc tính dunder nguy hiểm
BLOCKED_DUNDERS = frozenset({
    '__import__', '__builtins__', '__subclasses__', '__class__',
    '__bases__', '__mro__', '__globals__', '__code__', '__reduce__',
    '__reduce_ex__', '__getstate__', '__setstate__',
})


def validate_code(code: str) -> tuple:
    """
    Kiểm tra code Python có an toàn để thực thi hay không.
    
    Returns:
        tuple: (is_safe: bool, error_message: str)
    """
    # Giới hạn kích thước code (tránh DOS)
    if len(code) > 10_000:
        return False, "Code quá dài (tối đa 10.000 ký tự)."

    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return False, f"Lỗi cú pháp dòng {e.lineno}: {e.msg}"

    for node in ast.walk(tree):
        # Kiểm tra import trực tiếp: import os, import sys
        if isinstance(node, ast.Import):
            for alias in node.names:
                root = alias.name.split('.')[0]
                if root in BLOCKED_MODULES:
                    return False, f"Module '{alias.name}' không được phép sử dụng."

        # Kiểm tra import from: from os import path
        if isinstance(node, ast.ImportFrom):
            if node.module:
                root = node.module.split('.')[0]
                if root in BLOCKED_MODULES:
                    return False, f"Module '{node.module}' không được phép sử dụng."

        # Kiểm tra gọi hàm nguy hiểm: exec(), eval(), open()...
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id in BLOCKED_BUILTINS:
                return False, f"Hàm '{node.func.id}()' không được phép sử dụng."

        # Kiểm tra truy cập thuộc tính dunder nguy hiểm
        if isinstance(node, ast.Attribute):
            if node.attr in BLOCKED_DUNDERS:
                return False, f"Truy cập '{node.attr}' không được phép."

    return True, ""
