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

EXPOSE 8080

# Dùng shell form để đọc được biến $PORT từ Railway (mặc định Railway dùng 8080)
CMD gunicorn --bind "0.0.0.0:${PORT:-8080}" --workers 2 --timeout 120 --log-level info run:app
