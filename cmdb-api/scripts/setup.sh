#!/bin/bash

# CMDB API 项目初始化设置脚本

set -e

echo "🚀 CMDB API 项目初始化设置..."

# 检查 Python 版本
echo "🔍 检查 Python 版本..."
python_version=$(python3 --version 2>&1 | awk '{print $2}' | cut -d. -f1,2)
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python 版本过低，需要 Python 3.8+，当前版本: $python_version"
    exit 1
fi
echo "✅ Python 版本: $python_version"

# 创建虚拟环境
if [ ! -d ".venv" ]; then
    echo "📦 创建虚拟环境..."
    python3 -m venv .venv
    echo "✅ 虚拟环境创建成功"
else
    echo "✅ 虚拟环境已存在"
fi

# 激活虚拟环境
echo "📦 激活虚拟环境..."
source .venv/bin/activate

# 升级 pip
echo "⬆️ 升级 pip..."
pip install --upgrade pip

# 安装依赖
echo "📦 安装项目依赖..."
pip install -r requirements.txt
echo "✅ 依赖安装完成"

# 创建环境变量文件
if [ ! -f ".env" ]; then
    echo "📝 创建环境变量文件..."
    cat > .env << EOF
# =============================== 环境配置 ===========================================================
FLASK_ENV=development

# =============================== 安全配置 ===========================================================
SECRET_KEY=dev-secret-key-change-in-production
BCRYPT_LOG_ROUNDS=13

# =============================== 数据库配置 ===========================================================
MYSQL_USER=cmdb
MYSQL_PASSWORD=123456
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_DATABASE=cmdb

# =============================== Redis 缓存配置 ===========================================================
CACHE_REDIS_HOST=127.0.0.1
CACHE_REDIS_PORT=6379
CACHE_REDIS_PASSWORD=

# =============================== 日志配置 ===========================================================
LOG_LEVEL=DEBUG
EOF
    echo "✅ 环境变量文件创建完成"
else
    echo "✅ 环境变量文件已存在"
fi

# 创建日志目录
echo "📁 创建日志目录..."
mkdir -p logs
echo "✅ 日志目录创建完成"

# 检查数据库连接
echo "🔍 检查数据库连接..."
if command -v mysql &> /dev/null; then
    echo "📊 MySQL 客户端已安装"
else
    echo "⚠️  MySQL 客户端未安装，请手动安装 MySQL"
fi

# 检查 Redis 连接
echo "🔍 检查 Redis 连接..."
if command -v redis-cli &> /dev/null; then
    echo "📊 Redis 客户端已安装"
else
    echo "⚠️  Redis 客户端未安装，请手动安装 Redis"
fi

# 设置脚本权限
echo "🔧 设置脚本权限..."
chmod +x scripts/*.sh
echo "✅ 脚本权限设置完成"

echo ""
echo "🎉 项目初始化完成！"
echo ""
echo "📋 下一步操作："
echo "1. 启动 MySQL 和 Redis 服务"
echo "2. 创建数据库: mysql -u root -p -e 'CREATE DATABASE cmdb CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;'"
echo "3. 运行数据库迁移: flask db upgrade"
echo "4. 启动开发服务器: ./scripts/start_dev.sh"
echo "5. 启动 Celery 工作进程: ./scripts/start_celery.sh"
echo ""
echo "📚 更多信息请查看 README_RUNNING.md" 