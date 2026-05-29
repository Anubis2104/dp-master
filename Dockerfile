FROM python:3.11-slim

# Tạo user riêng (không chạy với quyền root để tăng bảo mật)
RUN groupadd -r appgroup && useradd -r -g appgroup appuser

# Cài đặt docker client để container có thể gọi docker run (sandbox code)
RUN apt-get update && apt-get install -y --no-install-recommends \
    docker.io \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements trước để tận dụng Docker layer cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copy toàn bộ source code
COPY . .

# Tạo thư mục instance (chứa SQLite DB) và cấp quyền cho appuser
RUN mkdir -p /app/instance && chown -R appuser:appgroup /app/instance

# Chuyển sang user không có quyền root
USER appuser

EXPOSE 5000

# Khởi chạy với Gunicorn: tự tạo DB trước khi start server
CMD ["sh", "-c", "python -c 'from run import app; from app.models import db; \
app.app_context().__enter__(); db.create_all()' && \
gunicorn --config gunicorn.conf.py run:app"]
