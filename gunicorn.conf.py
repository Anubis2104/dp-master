"""
Gunicorn configuration cho production deployment.
Điều chỉnh các giá trị theo tài nguyên của server.
"""
import multiprocessing
import os

# ==========================================
# Server socket
# ==========================================
bind = f"0.0.0.0:{os.getenv('PORT', '5000')}"
backlog = 2048

# ==========================================
# Worker processes
# ==========================================
# Công thức: (2 * số CPU) + 1 - phù hợp cho I/O-bound app (Flask + SQLite)
workers = int(os.getenv('WEB_CONCURRENCY', multiprocessing.cpu_count() * 2 + 1))
worker_class = 'sync'      # Sync worker - phù hợp với SQLite
threads = 2                # 2 thread mỗi worker
worker_connections = 1000
timeout = 30               # Timeout 30s (đủ để chạy code sandbox)
keepalive = 2

# ==========================================
# Bảo mật
# ==========================================
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# ==========================================
# Logging
# ==========================================
accesslog = '-'   # Log ra stdout (tốt cho Docker)
errorlog = '-'    # Log lỗi ra stderr
loglevel = os.getenv('LOG_LEVEL', 'info')
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)sµs'

# ==========================================
# Process naming
# ==========================================
proc_name = 'dp_master'
