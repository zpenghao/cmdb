# CMDB API 运行指南

## 项目概述

这是一个基于 Flask 的 CMDB (Configuration Management Database) API 项目，提供配置管理数据库的 RESTful API 服务。

## 系统要求

- Python 3.8+
- MySQL 5.7+
- Redis 5.0+
- Elasticsearch 7.x (可选)

## 环境配置

### 1. 环境变量配置

创建 `.env` 文件并配置以下环境变量：

```bash
# =============================== 环境配置 ===========================================================
# 环境类型: development, production
FLASK_ENV=development

# =============================== 安全配置 ===========================================================
# 应用密钥 (生产环境必须修改)
SECRET_KEY=your-secret-key-here
BCRYPT_LOG_ROUNDS=13

# =============================== 数据库配置 ===========================================================
# MySQL 数据库配置
MYSQL_USER=cmdb
MYSQL_PASSWORD=123456
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_DATABASE=cmdb

# =============================== Redis 缓存配置 ===========================================================
# Redis 缓存配置
CACHE_REDIS_HOST=127.0.0.1
CACHE_REDIS_PORT=6379
CACHE_REDIS_PASSWORD=

# =============================== 邮件配置 ===========================================================
# 邮件服务器配置 (可选)
MAIL_SERVER=smtp.example.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@example.com
MAIL_PASSWORD=your-email-password
DEFAULT_MAIL_SENDER=your-email@example.com

# =============================== Elasticsearch 配置 ===========================================================
# Elasticsearch 配置 (可选)
ES_HOST=127.0.0.1
ES_PORT=9200

# =============================== 认证配置 ===========================================================
# LDAP 配置 (可选)
LDAP_SERVER=ldap://ldap.example.com
LDAP_DOMAIN=example.com
LDAP_USER_DN=cn={},ou=users,dc=example,dc=com

# CAS 配置 (可选)
CAS_SERVER=https://cas.example.com
CAS_ENABLED=false

# OAuth2 配置 (可选)
OAUTH2_CLIENT_ID=your-oauth2-client-id
OAUTH2_CLIENT_SECRET=your-oauth2-client-secret
OAUTH2_ENABLED=false

# =============================== Vault 配置 ===========================================================
# HashiCorp Vault 配置 (可选)
VAULT_URL=http://127.0.0.1:8200
VAULT_TOKEN=your-vault-token
SECRETS_ENGINE=inner  # 'inner' 或 'vault'

# =============================== 日志配置 ===========================================================
# 日志级别: DEBUG, INFO, WARNING, ERROR
LOG_LEVEL=DEBUG
```

## 开发环境运行

### 1. 安装依赖

```bash
# 激活虚拟环境
source .venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 2. 数据库初始化

```bash
# 创建数据库
mysql -u root -p -e "CREATE DATABASE cmdb CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

# 运行数据库迁移
flask db upgrade
```

### 3. 启动服务

#### 方式一：使用 Flask 开发服务器

```bash
# 激活虚拟环境
source .venv/bin/activate

# 设置环境变量
export FLASK_ENV=development
export FLASK_APP=autoapp.py

# 启动开发服务器
flask run --host=0.0.0.0 --port=5000
```

#### 方式二：使用 Python 直接运行

```bash
# 激活虚拟环境
source .venv/bin/activate

# 启动应用
python -m flask --app autoapp run --host=0.0.0.0 --port=5000 --debug
```

### 4. 启动 Celery 工作进程 (可选)

```bash
# 激活虚拟环境
source .venv/bin/activate

# 启动 Celery 工作进程
celery -A celery_worker.celery worker -l DEBUG -E
```

### 5. 访问应用

- API 文档: http://localhost:5000/apidocs/
- 健康检查: http://localhost:5000/api/health

## 生产环境运行

### 1. 使用 Gunicorn 部署

#### 创建 Gunicorn 配置文件

创建 `gunicorn.conf.py`:

```python
# Gunicorn 配置文件
bind = "0.0.0.0:5000"
workers = 4
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100
timeout = 30
keepalive = 2
preload_app = True
daemon = False
user = "www-data"
group = "www-data"
pidfile = "/var/run/gunicorn.pid"
accesslog = "/var/log/gunicorn/access.log"
errorlog = "/var/log/gunicorn/error.log"
loglevel = "info"
```

#### 启动命令

```bash
# 激活虚拟环境
source .venv/bin/activate

# 使用 Gunicorn 启动
gunicorn -c gunicorn.conf.py autoapp:app
```

### 2. 使用 Supervisor 管理进程

#### 创建 Supervisor 配置文件

创建 `/etc/supervisor/conf.d/cmdb-api.conf`:

```ini
[program:cmdb-api]
command=/path/to/your/project/.venv/bin/gunicorn -c gunicorn.conf.py autoapp:app
directory=/path/to/your/project
user=www-data
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/supervisor/cmdb-api.log
environment=FLASK_ENV="production"

[program:cmdb-celery]
command=/path/to/your/project/.venv/bin/celery -A celery_worker.celery worker -l INFO
directory=/path/to/your/project
user=www-data
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/supervisor/cmdb-celery.log
environment=FLASK_ENV="production"
```

#### 启动 Supervisor

```bash
# 重新加载配置
sudo supervisorctl reread
sudo supervisorctl update

# 启动服务
sudo supervisorctl start cmdb-api
sudo supervisorctl start cmdb-celery

# 查看状态
sudo supervisorctl status
```

### 3. 使用 Nginx 反向代理

#### Nginx 配置示例

创建 `/etc/nginx/sites-available/cmdb-api`:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /path/to/your/project/static/;
        expires 30d;
    }
}
```

#### 启用站点

```bash
# 创建软链接
sudo ln -s /etc/nginx/sites-available/cmdb-api /etc/nginx/sites-enabled/

# 测试配置
sudo nginx -t

# 重启 Nginx
sudo systemctl restart nginx
```

## 数据库管理

### 1. 数据库迁移

```bash
# 激活虚拟环境
source .venv/bin/activate

# 创建迁移文件
flask db migrate -m "描述信息"

# 应用迁移
flask db upgrade

# 回滚迁移
flask db downgrade
```

### 2. 数据库备份

```bash
# 备份数据库
mysqldump -u cmdb -p cmdb > cmdb_backup_$(date +%Y%m%d_%H%M%S).sql

# 恢复数据库
mysql -u cmdb -p cmdb < cmdb_backup_20231201_120000.sql
```

## 监控和日志

### 1. 日志配置

日志文件位置：`./logs/app.log`

### 2. 健康检查

```bash
# 检查应用状态
curl http://localhost:5000/api/health

# 检查数据库连接
curl http://localhost:5000/api/health/db

# 检查 Redis 连接
curl http://localhost:5000/api/health/redis
```

### 3. 性能监控

```bash
# 查看进程状态
ps aux | grep gunicorn
ps aux | grep celery

# 查看端口占用
netstat -tlnp | grep :5000

# 查看日志
tail -f logs/app.log
```

## 故障排除

### 1. 常见问题

#### 数据库连接失败
- 检查 MySQL 服务是否启动
- 验证数据库连接参数
- 确认数据库用户权限

#### Redis 连接失败
- 检查 Redis 服务是否启动
- 验证 Redis 连接参数
- 确认 Redis 密码配置

#### 依赖包问题
- 确保虚拟环境已激活
- 重新安装依赖：`pip install -r requirements.txt`
- 检查 Python 版本兼容性

### 2. 调试模式

```bash
# 启用调试模式
export FLASK_ENV=development
export FLASK_DEBUG=1

# 启动调试服务器
flask run --debug
```

## 安全建议

### 1. 生产环境安全配置

- 修改默认的 `SECRET_KEY`
- 使用强密码
- 启用 HTTPS
- 配置防火墙
- 定期更新依赖包
- 启用日志审计

### 2. 数据库安全

- 使用专用数据库用户
- 限制数据库访问权限
- 定期备份数据
- 启用数据库审计日志

### 3. 网络安全

- 使用反向代理 (Nginx)
- 配置 SSL/TLS 证书
- 启用 CORS 策略
- 实施速率限制

## 部署检查清单

- [ ] 环境变量配置完成
- [ ] 数据库创建并迁移完成
- [ ] Redis 服务启动
- [ ] 虚拟环境激活
- [ ] 依赖包安装完成
- [ ] 应用启动成功
- [ ] Celery 工作进程启动
- [ ] Nginx 配置完成
- [ ] SSL 证书配置 (生产环境)
- [ ] 监控和日志配置
- [ ] 备份策略制定
- [ ] 安全配置检查 