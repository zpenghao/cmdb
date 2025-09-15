#!/bin/bash

# CMDB API Celery 工作进程启动脚本

set -e

echo "🚀 启动 CMDB API Celery 工作进程..."

# 检查虚拟环境
if [ ! -d ".venv" ]; then
    echo "❌ 虚拟环境不存在，请先创建虚拟环境"
    exit 1
fi

# 激活虚拟环境
echo "📦 激活虚拟环境..."
source .venv/bin/activate

# 检查环境变量文件
if [ ! -f ".env" ]; then
    echo "⚠️  .env 文件不存在，使用默认配置"
fi

# 检查依赖
echo "🔍 检查依赖..."
pip list | grep -E "(celery|redis)" || {
    echo "❌ 依赖不完整，正在安装..."
    pip install -r requirements.txt
}

# 检查 Redis 连接
echo "🔍 检查 Redis 连接..."
python -c "
import redis
import os
try:
    r = redis.Redis(
        host=os.getenv('CACHE_REDIS_HOST', '127.0.0.1'),
        port=int(os.getenv('CACHE_REDIS_PORT', 6379)),
        password=os.getenv('CACHE_REDIS_PASSWORD', ''),
        decode_responses=True
    )
    r.ping()
    print('✅ Redis 连接成功')
except Exception as e:
    print(f'❌ Redis 连接失败: {e}')
    exit(1)
" || exit 1

# 创建日志目录
mkdir -p logs

# 启动 Celery 工作进程
echo "🌟 启动 Celery 工作进程..."
echo "📊 队列: 默认队列"
echo "🔧 日志级别: INFO"
echo "📝 日志文件: logs/celery.log"
echo ""

# 设置环境变量
export FLASK_ENV=${FLASK_ENV:-production}

# 启动 Celery
celery -A celery_worker.celery worker \
    --loglevel=INFO \
    --concurrency=4 \
    --max-tasks-per-child=1000 \
    --without-gossip \
    --without-mingle \
    --without-heartbeat \
    -E 