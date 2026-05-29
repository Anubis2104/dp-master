"""
Gunicorn configuration cho Railway deployment.
"""
import os

# ==========================================
# Server socket - Railway cung cấp PORT env var (mặc định 8080)
# ==========================================
bind = f"0.0.0.0:{os.getenv('PORT', '8080')}"

# ==========================================
# Worker processes - giới hạn để tránh OOM trên Railway free tier
# ==========================================
workers = 2
worker_class = 'sync'
threads = 1
timeout = 120              # Đủ lâu cho code sandbox chạy
keepalive = 5

# ==========================================
# Logging
# ==========================================
accesslog = '-'
errorlog = '-'
loglevel = 'info'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s %(D)sµs'

# ==========================================
# Process naming
# ==========================================
proc_name = 'dp_master'
