# PyCharm 配置指南

## 🚀 PyCharm 项目配置

### 1. 打开项目

1. 打开 PyCharm
2. 选择 `File` → `Open`
3. 选择 `cmdb-api` 项目目录
4. 点击 `OK`

### 2. 配置 Python 解释器

#### 方法一：使用现有虚拟环境

1. 打开 `File` → `Settings` (Windows/Linux) 或 `PyCharm` → `Preferences` (macOS)
2. 导航到 `Project: cmdb-api` → `Python Interpreter`
3. 点击齿轮图标 → `Add`
4. 选择 `Existing Environment`
5. 设置解释器路径：
   ```
   /Users/zhangjingbo/Documents/workspace/zhiyi/cmdb/cmdb-api/.venv/bin/python
   ```
6. 点击 `OK`

#### 方法二：创建新的虚拟环境

1. 在 `Python Interpreter` 页面点击齿轮图标 → `Add`
2. 选择 `Virtualenv Environment` → `New Environment`
3. 设置基础解释器：`Python 3.8+`
4. 设置位置：`./venv`
5. 点击 `OK`

### 3. 安装依赖

配置好解释器后，PyCharm 会自动检测 `requirements.txt` 并提示安装依赖：

1. 点击提示框中的 `Install requirements`
2. 或者手动安装：
   ```bash
   pip install -r requirements.txt
   ```

## 🔧 运行配置

### 1. 创建 Flask 运行配置

#### 开发环境配置

1. 点击右上角的 `Add Configuration` 或 `Edit Configurations`
2. 点击 `+` 号 → `Python`
3. 配置如下：

```
Name: CMDB API (Development)
Script path: 留空
Module name: flask
Parameters: --app autoapp run --host=0.0.0.0 --port=5000 --debug
Working directory: /Users/zhangjingbo/Documents/workspace/zhiyi/cmdb/cmdb-api
Environment variables:
    FLASK_ENV=development
    FLASK_APP=autoapp.py
    PYTHONPATH=/Users/zhangjingbo/Documents/workspace/zhiyi/cmdb/cmdb-api
```

#### 生产环境配置

```
Name: CMDB API (Production)
Script path: 留空
Module name: gunicorn
Parameters: -c gunicorn.conf.py autoapp:app
Working directory: /Users/zhangjingbo/Documents/workspace/zhiyi/cmdb/cmdb-api
Environment variables:
    FLASK_ENV=production
    PYTHONPATH=/Users/zhangjingbo/Documents/workspace/zhiyi/cmdb/cmdb-api
```

### 2. 创建 Celery 运行配置

```
Name: CMDB Celery Worker
Script path: 留空
Module name: celery
Parameters: -A celery_worker.celery worker -l DEBUG -E
Working directory: /Users/zhangjingbo/Documents/workspace/zhiyi/cmdb/cmdb-api
Environment variables:
    FLASK_ENV=development
    PYTHONPATH=/Users/zhangjingbo/Documents/workspace/zhiyi/cmdb/cmdb-api
```

### 3. 创建数据库迁移配置

```
Name: Flask DB Migrate
Script path: 留空
Module name: flask
Parameters: db migrate -m "migration message"
Working directory: /Users/zhangjingbo/Documents/workspace/zhiyi/cmdb/cmdb-api
Environment variables:
    FLASK_APP=autoapp.py
    PYTHONPATH=/Users/zhangjingbo/Documents/workspace/zhiyi/cmdb/cmdb-api
```

```
Name: Flask DB Upgrade
Script path: 留空
Module name: flask
Parameters: db upgrade
Working directory: /Users/zhangjingbo/Documents/workspace/zhiyi/cmdb/cmdb-api
Environment variables:
    FLASK_APP=autoapp.py
    PYTHONPATH=/Users/zhangjingbo/Documents/workspace/zhiyi/cmdb/cmdb-api
```

## 🐛 调试配置

### 1. 创建调试配置

复制开发环境配置，并启用调试：

1. 右键点击 `CMDB API (Development)` 配置
2. 选择 `Copy Configuration`
3. 重命名为 `CMDB API (Debug)`
4. 在 `Debug` 标签页中：
   - 勾选 `Debugger`
   - 设置断点条件（可选）

### 2. 设置断点

1. 在代码行号左侧点击设置断点
2. 右键断点可以设置条件
3. 使用调试配置启动应用

## 📁 项目结构配置

### 1. 标记目录

1. 右键点击 `api` 目录
2. 选择 `Mark Directory as` → `Sources Root`
3. 右键点击 `tests` 目录
4. 选择 `Mark Directory as` → `Test Sources Root`

### 2. 排除目录

1. 右键点击 `logs` 目录
2. 选择 `Mark Directory as` → `Excluded`
3. 同样处理 `__pycache__` 目录

## 🔍 代码检查配置

### 1. 配置 PEP8

1. 打开 `Settings` → `Editor` → `Code Style` → `Python`
2. 设置缩进为 4 个空格
3. 配置行长度限制为 120

### 2. 配置 Linter

1. 打开 `Settings` → `Editor` → `Inspections`
2. 启用 Python 相关检查
3. 配置 `PEP 8` 检查规则

## 🌐 数据库工具配置

### 1. 配置 MySQL 连接

1. 打开 `View` → `Tool Windows` → `Database`
2. 点击 `+` → `Data Source` → `MySQL`
3. 配置连接信息：
   ```
   Host: localhost
   Port: 3306
   Database: cmdb
   User: cmdb
   Password: 123456
   ```

### 2. 配置 Redis 连接

1. 在 Database 工具窗口中点击 `+` → `Data Source` → `Redis`
2. 配置连接信息：
   ```
   Host: localhost
   Port: 6379
   Password: (如果有)
   ```

## 📝 环境变量配置

### 1. 创建 .env 文件

在项目根目录创建 `.env` 文件：

```bash
# 开发环境配置
FLASK_ENV=development
SECRET_KEY=dev-secret-key-change-in-production
BCRYPT_LOG_ROUNDS=13

# 数据库配置
MYSQL_USER=cmdb
MYSQL_PASSWORD=123456
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_DATABASE=cmdb

# Redis 配置
CACHE_REDIS_HOST=127.0.0.1
CACHE_REDIS_PORT=6379
CACHE_REDIS_PASSWORD=

# 日志配置
LOG_LEVEL=DEBUG
```

### 2. 在运行配置中使用环境变量

在运行配置的 `Environment variables` 中添加：

```
FLASK_ENV=development
FLASK_APP=autoapp.py
SECRET_KEY=dev-secret-key-change-in-production
MYSQL_USER=cmdb
MYSQL_PASSWORD=123456
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_DATABASE=cmdb
CACHE_REDIS_HOST=127.0.0.1
CACHE_REDIS_PORT=6379
LOG_LEVEL=DEBUG
```

## 🔧 快捷键配置

### 1. 常用快捷键

- `Ctrl+Shift+F10` (Windows/Linux) / `Ctrl+Shift+R` (macOS): 运行当前文件
- `Shift+F10`: 运行配置
- `Shift+F9`: 调试配置
- `Ctrl+F8`: 切换断点
- `F8`: 单步执行
- `F7`: 步入
- `Shift+F8`: 步出

### 2. 自定义快捷键

1. 打开 `Settings` → `Keymap`
2. 搜索需要的操作
3. 右键设置快捷键

## 📊 监控和日志

### 1. 配置日志输出

在运行配置中启用控制台输出：

1. 在运行配置的 `Logs` 标签页
2. 勾选 `Show console when a message is printed to standard output`
3. 勾选 `Show console when a message is printed to standard error`

### 2. 查看应用日志

1. 打开 `View` → `Tool Windows` → `Terminal`
2. 运行：`tail -f logs/app.log`

## 🎯 最佳实践

### 1. 项目设置

- ✅ 使用虚拟环境
- ✅ 配置正确的 Python 解释器
- ✅ 标记源代码目录
- ✅ 排除不必要的目录

### 2. 运行配置

- ✅ 为不同环境创建独立配置
- ✅ 设置正确的环境变量
- ✅ 配置工作目录
- ✅ 启用日志输出

### 3. 调试配置

- ✅ 创建专门的调试配置
- ✅ 设置断点条件
- ✅ 使用变量监视器
- ✅ 查看调用栈

### 4. 代码质量

- ✅ 启用代码检查
- ✅ 配置 PEP8 规则
- ✅ 使用代码格式化
- ✅ 定期重构代码

## 🚀 快速启动检查清单

- [ ] 项目已正确打开
- [ ] Python 解释器已配置
- [ ] 依赖已安装
- [ ] 环境变量已配置
- [ ] 运行配置已创建
- [ ] 数据库连接已配置
- [ ] 日志目录已创建
- [ ] 代码检查已启用

## 📞 常见问题

### 1. 模块导入错误

**问题**: `ModuleNotFoundError: No module named 'api'`

**解决方案**:
1. 确保 `api` 目录被标记为 `Sources Root`
2. 检查 `PYTHONPATH` 环境变量
3. 重启 PyCharm

### 2. 环境变量不生效

**问题**: 环境变量在代码中无法读取

**解决方案**:
1. 检查 `.env` 文件是否存在
2. 确保在运行配置中设置了环境变量
3. 重启应用

### 3. 调试器不工作

**问题**: 断点不生效

**解决方案**:
1. 使用调试配置而不是运行配置
2. 检查断点是否在正确的行
3. 确保代码已保存

### 4. 数据库连接失败

**问题**: 无法连接到数据库

**解决方案**:
1. 检查数据库服务是否启动
2. 验证连接参数
3. 测试网络连接

---

**提示**: 配置完成后，你可以使用 PyCharm 的强大功能进行开发、调试和部署，大大提高开发效率。 