# CMDB API 快速启动指南

## 🚀 5分钟快速启动

### 1. 环境准备

确保你的系统已安装：
- Python 3.8+
- MySQL 5.7+
- Redis 5.0+

### 2. 一键初始化

```bash
# 运行初始化脚本
./scripts/setup.sh
```

### 3. 启动服务

```bash
# 启动 MySQL 和 Redis (根据你的系统)
# macOS: brew services start mysql redis
# Ubuntu: sudo systemctl start mysql redis-server

# 创建数据库
mysql -u root -p -e "CREATE DATABASE cmdb CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

# 运行数据库迁移
source .venv/bin/activate
flask db upgrade

# 启动开发服务器
./scripts/start_dev.sh
```

### 4. 访问应用

- 🌐 应用地址: http://localhost:5000
- 📚 API 文档: http://localhost:5000/apidocs/
- 🔍 健康检查: http://localhost:5000/api/health

## 🔧 常用命令

### 开发环境

```bash
# 启动开发服务器
./scripts/start_dev.sh

# 启动 Celery 工作进程
./scripts/start_celery.sh

# 数据库迁移
flask db migrate -m "描述"
flask db upgrade
```

### 生产环境

```bash
# 启动生产服务器
./scripts/start_prod.sh

# 使用 Supervisor 管理 (推荐)
sudo supervisorctl start cmdb-api
sudo supervisorctl start cmdb-celery
```

### 数据库管理

```bash
# 备份数据库
mysqldump -u cmdb -p cmdb > backup.sql

# 恢复数据库
mysql -u cmdb -p cmdb < backup.sql

# 查看迁移历史
flask db history
```

## 📋 环境变量配置

创建 `.env` 文件：

```bash
# 开发环境
FLASK_ENV=development
SECRET_KEY=your-secret-key
MYSQL_USER=cmdb
MYSQL_PASSWORD=123456
MYSQL_HOST=127.0.0.1
MYSQL_DATABASE=cmdb
CACHE_REDIS_HOST=127.0.0.1
```

## 🐛 常见问题

### 1. 依赖安装失败
```bash
# 重新安装依赖
pip install -r requirements.txt --force-reinstall
```

### 2. 数据库连接失败
```bash
# 检查 MySQL 服务
sudo systemctl status mysql

# 检查连接参数
mysql -u cmdb -p -h 127.0.0.1 cmdb
```

### 3. Redis 连接失败
```bash
# 检查 Redis 服务
sudo systemctl status redis

# 测试连接
redis-cli ping
```

### 4. 端口被占用
```bash
# 查看端口占用
lsof -i :5000

# 杀死进程
kill -9 <PID>
```

## 📊 监控和日志

```bash
# 查看应用日志
tail -f logs/app.log

# 查看 Celery 日志
tail -f logs/celery.log

# 查看 Gunicorn 日志
tail -f /var/log/gunicorn/error.log
```

## 🔒 安全配置

生产环境必须修改：

1. **SECRET_KEY**: 使用强随机密钥
2. **数据库密码**: 使用强密码
3. **Redis 密码**: 启用认证
4. **HTTPS**: 配置 SSL 证书
5. **防火墙**: 限制端口访问

## 📞 获取帮助

- 📚 详细文档: [README_RUNNING.md](README_RUNNING.md)
- 🐛 问题反馈: 提交 Issue
- 💬 技术支持: 联系开发团队

---

**提示**: 首次运行建议使用开发环境，熟悉后再部署到生产环境。 