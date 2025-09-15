# CMDB API 项目结构

## 📁 目录结构

```
cmdb-api/
├── 📁 api/                          # 主应用目录
│   ├── 📁 app.py                    # Flask 应用工厂
│   ├── 📁 extensions.py             # Flask 扩展配置
│   ├── 📁 lib/                      # 核心库文件
│   │   ├── 📁 cmdb/                 # CMDB 核心功能
│   │   │   ├── 📁 auto_discovery/   # 自动发现功能
│   │   │   ├── 📁 dcim/            # 数据中心基础设施管理
│   │   │   ├── 📁 ipam/            # IP 地址管理
│   │   │   └── 📁 search/          # 搜索功能
│   │   ├── 📁 common_setting/       # 通用设置
│   │   ├── 📁 perm/                # 权限管理
│   │   │   ├── 📁 acl/             # 访问控制列表
│   │   │   └── 📁 authentication/  # 认证模块
│   │   └── 📁 secrets/             # 密钥管理
│   ├── 📁 models/                   # 数据模型
│   ├── 📁 views/                    # API 视图
│   │   ├── 📁 acl/                 # 权限相关 API
│   │   ├── 📁 cmdb/                # CMDB 相关 API
│   │   └── 📁 common_setting/      # 通用设置 API
│   ├── 📁 tasks/                    # Celery 任务
│   └── 📁 resource.py               # API 资源定义
├── 📁 migrations/                   # 数据库迁移文件
├── 📁 tests/                        # 测试文件
├── 📁 logs/                         # 日志文件
├── 📁 scripts/                      # 运行脚本
│   ├── 📄 setup.sh                  # 项目初始化脚本
│   ├── 📄 start_dev.sh              # 开发环境启动脚本
│   ├── 📄 start_prod.sh             # 生产环境启动脚本
│   └── 📄 start_celery.sh           # Celery 启动脚本
├── 📄 autoapp.py                    # 应用入口
├── 📄 celery_worker.py              # Celery 工作进程
├── 📄 settings.py                   # 应用配置
├── 📄 requirements.txt              # Python 依赖
├── 📄 Pipfile                       # Pipenv 依赖管理
├── 📄 README_RUNNING.md             # 详细运行指南
├── 📄 QUICKSTART.md                 # 快速启动指南
└── 📄 PROJECT_STRUCTURE.md          # 项目结构说明
```

## 🔧 核心组件

### 1. 应用入口
- **autoapp.py**: Flask 应用入口点
- **celery_worker.py**: Celery 异步任务工作进程

### 2. 配置管理
- **settings.py**: 主配置文件
- **settings.example.py**: 配置示例文件
- **.env**: 环境变量文件 (需要创建)

### 3. 核心功能模块

#### CMDB 核心 (`api/lib/cmdb/`)
- **ci.py**: 配置项管理
- **ci_type.py**: 配置项类型管理
- **attribute.py**: 属性管理
- **relation_type.py**: 关系类型管理
- **ci_relation.py**: 配置项关系管理
- **auto_discovery/**: 自动发现功能
- **dcim/**: 数据中心基础设施管理
- **ipam/**: IP 地址管理
- **search/**: 搜索功能

#### 权限管理 (`api/lib/perm/`)
- **acl/**: 访问控制列表
  - **acl.py**: ACL 核心功能
  - **user.py**: 用户管理
  - **role.py**: 角色管理
  - **permission.py**: 权限管理
  - **resource.py**: 资源管理
- **authentication/**: 认证模块
  - **ldap.py**: LDAP 认证
  - **oauth2/**: OAuth2 认证
  - **cas/**: CAS 认证

#### 通用设置 (`api/lib/common_setting/`)
- **company_info.py**: 公司信息管理
- **department.py**: 部门管理
- **employee.py**: 员工管理
- **notice_config.py**: 通知配置

#### 密钥管理 (`api/lib/secrets/`)
- **secrets.py**: 密钥管理核心
- **vault.py**: HashiCorp Vault 集成
- **inner.py**: 内置密钥管理

### 4. API 视图 (`api/views/`)

#### ACL API (`api/views/acl/`)
- **login.py**: 登录认证
- **user.py**: 用户管理 API
- **role.py**: 角色管理 API
- **permission.py**: 权限管理 API
- **app.py**: 应用管理 API

#### CMDB API (`api/views/cmdb/`)
- **ci.py**: 配置项 API
- **ci_type.py**: 配置项类型 API
- **attribute.py**: 属性 API
- **ci_relation.py**: 配置项关系 API
- **auto_discovery.py**: 自动发现 API
- **dcim/**: 数据中心管理 API
- **ipam/**: IP 地址管理 API

#### 通用设置 API (`api/views/common_setting/`)
- **company_info.py**: 公司信息 API
- **department.py**: 部门管理 API
- **employee.py**: 员工管理 API
- **notice_config.py**: 通知配置 API

### 5. 数据模型 (`api/models/`)
- **acl.py**: 权限相关模型
- **cmdb.py**: CMDB 相关模型
- **common_setting.py**: 通用设置模型

### 6. 异步任务 (`api/tasks/`)
- **acl.py**: 权限相关任务
- **cmdb.py**: CMDB 相关任务
- **common_setting.py**: 通用设置任务

## 🚀 运行脚本

### 开发环境
```bash
# 项目初始化
./scripts/setup.sh

# 启动开发服务器
./scripts/start_dev.sh

# 启动 Celery 工作进程
./scripts/start_celery.sh
```

### 生产环境
```bash
# 启动生产服务器
./scripts/start_prod.sh

# 使用 Supervisor 管理
sudo supervisorctl start cmdb-api
sudo supervisorctl start cmdb-celery
```

## 📊 数据库结构

### 主要数据表
- **users**: 用户表
- **roles**: 角色表
- **permissions**: 权限表
- **ci_types**: 配置项类型表
- **cis**: 配置项表
- **attributes**: 属性表
- **ci_relations**: 配置项关系表
- **departments**: 部门表
- **employees**: 员工表

## 🔐 安全架构

### 认证方式
- 内置用户认证
- LDAP 认证
- OAuth2 认证
- CAS 认证

### 权限控制
- 基于角色的访问控制 (RBAC)
- 资源级权限控制
- API 级权限控制

### 密钥管理
- 内置密钥管理
- HashiCorp Vault 集成

## 📈 监控和日志

### 日志文件
- **logs/app.log**: 应用日志
- **logs/celery.log**: Celery 任务日志
- **/var/log/gunicorn/**: Gunicorn 日志

### 健康检查
- `/api/health`: 应用健康检查
- `/api/health/db`: 数据库健康检查
- `/api/health/redis`: Redis 健康检查

## 🔧 配置说明

### 环境变量
- **FLASK_ENV**: 环境类型 (development/production)
- **SECRET_KEY**: 应用密钥
- **MYSQL_***: MySQL 数据库配置
- **CACHE_REDIS_***: Redis 缓存配置
- **LDAP_***: LDAP 认证配置
- **CAS_***: CAS 认证配置
- **OAUTH2_***: OAuth2 认证配置

### 功能开关
- **USE_ACL**: 启用权限控制
- **USE_ES**: 启用 Elasticsearch
- **USE_MESSENGER**: 启用消息通知
- **SECRETS_ENGINE**: 密钥管理引擎

## 📚 相关文档

- [快速启动指南](QUICKSTART.md)
- [详细运行指南](README_RUNNING.md)
- [API 文档](http://localhost:5000/apidocs/)

---

**提示**: 这是一个企业级的 CMDB 系统，支持多种认证方式和权限控制，适合大型组织的配置管理需求。 