# PyCharm 配置文件导入指南

## 🚀 快速导入配置

### 方法一：直接复制配置

1. 打开 PyCharm
2. 点击右上角的 `Edit Configurations`
3. 点击 `+` 号 → `Python`
4. 按照以下配置手动创建：

#### CMDB API (Development)
```
Name: CMDB API (Development)
Module name: flask
Parameters: --app autoapp run --host=0.0.0.0 --port=5000 --debug
Working directory: /Users/zhangjingbo/Documents/workspace/zhiyi/cmdb/cmdb-api
Environment variables:
    FLASK_ENV=development
    FLASK_APP=autoapp.py
    PYTHONPATH=/Users/zhangjingbo/Documents/workspace/zhiyi/cmdb/cmdb-api
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

#### CMDB Celery Worker
```
Name: CMDB Celery Worker
Module name: celery
Parameters: -A celery_worker.celery worker -l DEBUG -E
Working directory: /Users/zhangjingbo/Documents/workspace/zhiyi/cmdb/cmdb-api
Environment variables: (同上)
```

#### Flask DB Migrate
```
Name: Flask DB Migrate
Module name: flask
Parameters: db migrate -m "migration message"
Working directory: /Users/zhangjingbo/Documents/workspace/zhiyi/cmdb/cmdb-api
Environment variables:
    FLASK_APP=autoapp.py
    PYTHONPATH=/Users/zhangjingbo/Documents/workspace/zhiyi/cmdb/cmdb-api
    (其他环境变量同上)
```

#### Flask DB Upgrade
```
Name: Flask DB Upgrade
Module name: flask
Parameters: db upgrade
Working directory: /Users/zhangjingbo/Documents/workspace/zhiyi/cmdb/cmdb-api
Environment variables: (同上)
```

### 方法二：导入 XML 配置文件

1. 将 `pycharm_configs/` 目录下的 `.run.xml` 文件复制到：
   ```
   ~/.PyCharm*/config/runConfigurations/
   ```
   或者
   ```
   ~/Library/Application Support/JetBrains/PyCharm*/runConfigurations/
   ```

2. 重启 PyCharm

3. 配置会自动出现在运行配置列表中

## 🔧 配置说明

### 环境变量说明

- **FLASK_ENV**: 环境类型 (development/production)
- **FLASK_APP**: Flask 应用入口文件
- **PYTHONPATH**: Python 模块搜索路径
- **SECRET_KEY**: 应用密钥
- **MYSQL_***: MySQL 数据库连接参数
- **CACHE_REDIS_***: Redis 缓存连接参数
- **LOG_LEVEL**: 日志级别

### 路径配置

请根据你的实际项目路径修改以下配置：

- **Working directory**: 项目根目录路径
- **PYTHONPATH**: 项目根目录路径
- **Python interpreter**: 虚拟环境中的 Python 解释器路径

## 🎯 使用建议

### 1. 开发流程

1. 启动 **CMDB API (Development)** 运行配置
2. 启动 **CMDB Celery Worker** 运行配置
3. 需要数据库迁移时使用 **Flask DB Migrate**
4. 应用迁移时使用 **Flask DB Upgrade**

### 2. 调试配置

1. 复制 **CMDB API (Development)** 配置
2. 重命名为 **CMDB API (Debug)**
3. 在代码中设置断点
4. 使用调试模式启动

### 3. 快捷键

- `Shift+F10`: 运行当前配置
- `Shift+F9`: 调试当前配置
- `Ctrl+Shift+F10`: 运行当前文件

## 📝 注意事项

1. **路径修改**: 确保所有路径都指向你的实际项目位置
2. **环境变量**: 根据你的实际环境修改数据库连接参数
3. **Python 解释器**: 确保使用项目的虚拟环境
4. **依赖安装**: 确保所有依赖都已正确安装

## 🐛 常见问题

### 1. 模块导入错误
- 检查 `PYTHONPATH` 环境变量
- 确保 `api` 目录被标记为 `Sources Root`

### 2. 环境变量不生效
- 检查环境变量配置
- 重启 PyCharm

### 3. 端口被占用
- 修改 `Parameters` 中的端口号
- 或者杀死占用端口的进程

---

**提示**: 配置完成后，你可以直接在 PyCharm 中运行和调试 CMDB API 项目，大大提高开发效率。 