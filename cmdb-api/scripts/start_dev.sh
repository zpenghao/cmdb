#!/bin/bash

# CMDB API 开发环境启动脚本

set -e

echo "🚀 启动 CMDB API 开发环境..."

# 检查虚拟环境
if [ ! -d ".venv" ]; then
    echo "❌ 虚拟环境不存在，请先创建虚拟环境"
    exit 1
fi

# 激活虚拟环境
echo "📦 激活虚拟环境..."
source .venv/bin/activate

# 检查依赖
echo "🔍 检查依赖..."
pip list | grep -E "(Flask|PyJWT|marshmallow)" || {
    echo "❌ 依赖不完整，正在安装..."
    pip install -r requirements.txt
}

# 检查环境变量文件
if [ ! -f ".env" ]; then
    echo "⚠️  .env 文件不存在，请创建并配置环境变量"
    echo "📝 参考 .env.example 文件"
    exit 1
fi

# 设置环境变量
export FLASK_ENV=development
export FLASK_APP=autoapp.py

# 检查数据库连接
echo "🔍 检查数据库连接..."
python -c "
import os
from sqlalchemy import create_engine
try:
    engine = create_engine(os.getenv('SQLALCHEMY_DATABASE_URI'))
    engine.connect()
    print('✅ 数据库连接成功')
except Exception as e:
    print(f'❌ 数据库连接失败: {e}')
    exit(1)
" || exit 1

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

# 启动应用
echo "🌟 启动 Flask 开发服务器..."
echo "📍 访问地址: http://localhost:5000"
echo "📚 API 文档: http://localhost:5000/apidocs/"
echo "🔧 调试模式已启用"
echo ""

flask run --host=0.0.0.0 --port=5000 --debug 