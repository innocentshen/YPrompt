# YPrompt - Zeabur 部署指南

本文档介绍如何将 YPrompt 项目部署到 Zeabur 平台。

## 📋 部署前准备

### 1. 项目结构说明

YPrompt 是一个 monorepo 项目，包含：
- **backend/** - Python Sanic 后端
- **frontend/** - Vue 3 + Vite 前端

### 2. Zeabur 账号

访问 [zeabur.com](https://zeabur.com) 注册账号并连接 GitHub。

## 🚀 部署步骤

### 方案一：推荐方案（使用 MySQL）

Zeabur 上的 SQLite 持久化可能不稳定，建议使用 Zeabur 提供的 MySQL 服务。

#### 步骤 1：推送代码到 GitHub

```bash
# 如果还没有 git 仓库
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/你的用户名/YPrompt.git
git push -u origin main
```

#### 步骤 2：在 Zeabur 创建项目

1. 登录 Zeabur 控制台
2. 点击 "New Project"
3. 选择 Region（建议选择离你最近的区域）

#### 步骤 3：添加 MySQL 数据库

1. 在项目中点击 "Add Service"
2. 选择 "Marketplace" → "MySQL"
3. 等待 MySQL 部署完成
4. Zeabur 会自动生成以下环境变量：
   - `MYSQL_HOST`
   - `MYSQL_PORT`
   - `MYSQL_USER`
   - `MYSQL_PASSWORD`
   - `MYSQL_DATABASE`

#### 步骤 4：部署后端服务

1. 点击 "Add Service" → "Git"
2. 选择你的 YPrompt 仓库
3. Zeabur 会自动检测为 Python 项目
4. 设置 Root Directory: `backend`
5. 添加以下环境变量：

**必需环境变量**：
```bash
# 数据库配置（使用 MySQL）
DB_TYPE=mysql
DB_HOST=${MYSQL_HOST}
DB_PORT=${MYSQL_PORT}
DB_USER=${MYSQL_USER}
DB_PASS=${MYSQL_PASSWORD}
DB_NAME=${MYSQL_DATABASE}

# JWT 密钥（生产环境必须修改）
SECRET_KEY=your-super-secret-jwt-key-change-me

# 跨域设置
ENABLE_CORS=true

# 默认管理员账号
DEFAULT_ADMIN_USERNAME=admin
DEFAULT_ADMIN_PASSWORD=your-secure-password-here
```

**可选环境变量**（如果使用 Linux.do OAuth）：
```bash
LINUX_DO_CLIENT_ID=your_client_id
LINUX_DO_CLIENT_SECRET=your_client_secret
LINUX_DO_REDIRECT_URI=https://your-frontend-domain.zeabur.app/auth/callback
```

6. 保存并等待部署完成
7. 记录后端域名（如 `backend-xxx.zeabur.app`）

#### 步骤 5：部署前端服务

1. 点击 "Add Service" → "Git"
2. 选择同一个 YPrompt 仓库
3. Zeabur 会自动检测为 Node.js 项目
4. 设置 Root Directory: `frontend`
5. 添加环境变量：

```bash
# 后端 API 地址（使用步骤 4 记录的后端域名）
VITE_API_BASE_URL=https://backend-xxx.zeabur.app
```

6. 保存并等待部署完成
7. 访问前端域名即可使用

### 方案二：使用 SQLite（不推荐）

⚠️ **警告**：Zeabur 上 SQLite 的持久化可能不稳定，数据可能丢失。

如果坚持使用 SQLite：

1. 按照方案一的步骤 1-2 创建项目
2. 跳过 MySQL 步骤，直接部署后端
3. 后端环境变量设置：

```bash
# 数据库配置（SQLite）
DB_TYPE=sqlite
SQLITE_DB_PATH=/data/yprompt.db

# JWT 密钥
SECRET_KEY=your-super-secret-jwt-key-change-me

# 跨域设置
ENABLE_CORS=true

# 默认管理员账号
DEFAULT_ADMIN_USERNAME=admin
DEFAULT_ADMIN_PASSWORD=your-secure-password-here
```

4. 需要确保 Zeabur 支持持久化卷挂载（联系 Zeabur 支持）

## 📝 初始化数据库（仅 MySQL）

### 自动初始化（推荐）

后端首次启动时会自动检测数据库并初始化表结构。

### 手动初始化（可选）

如果自动初始化失败，可以手动执行：

1. 连接到 Zeabur MySQL 数据库
2. 执行 `backend/migrations/init_mysql.sql`（如果存在）
3. 或手动创建表结构（参考 `CLAUDE.md` 中的数据库设计）

## 🔧 配置说明

### 环境变量详解

#### 后端环境变量

| 变量名 | 说明 | 默认值 | 必填 |
|--------|------|--------|------|
| `DB_TYPE` | 数据库类型 | `sqlite` | 是 |
| `DB_HOST` | MySQL主机 | - | MySQL时必填 |
| `DB_PORT` | MySQL端口 | `3306` | MySQL时必填 |
| `DB_USER` | MySQL用户名 | - | MySQL时必填 |
| `DB_PASS` | MySQL密码 | - | MySQL时必填 |
| `DB_NAME` | MySQL数据库名 | - | MySQL时必填 |
| `SQLITE_DB_PATH` | SQLite文件路径 | `../data/yprompt.db` | SQLite时必填 |
| `SECRET_KEY` | JWT密钥 | - | 是 |
| `ENABLE_CORS` | 启用跨域 | `true` | 否 |
| `DEFAULT_ADMIN_USERNAME` | 管理员用户名 | `admin` | 否 |
| `DEFAULT_ADMIN_PASSWORD` | 管理员密码 | `admin123` | 否 |
| `LINUX_DO_CLIENT_ID` | Linux.do OAuth ID | - | 否 |
| `LINUX_DO_CLIENT_SECRET` | Linux.do OAuth Secret | - | 否 |
| `LINUX_DO_REDIRECT_URI` | OAuth回调地址 | - | 否 |

#### 前端环境变量

| 变量名 | 说明 | 必填 |
|--------|------|------|
| `VITE_API_BASE_URL` | 后端 API 地址 | 是 |

### Zeabur 特殊变量

Zeabur 提供一些预定义变量：

- `${服务名.ZEABUR_WEB_URL}` - 其他服务的 URL
- 例如：`VITE_API_BASE_URL=${backend.ZEABUR_WEB_URL}`

## 🔐 安全建议

1. **修改默认密码**：
   - 修改 `SECRET_KEY` 为强随机字符串
   - 修改 `DEFAULT_ADMIN_PASSWORD` 为复杂密码

2. **环境变量安全**：
   - 不要在代码中硬编码敏感信息
   - 使用 Zeabur 环境变量管理

3. **CORS 配置**：
   - 生产环境建议限制 CORS 来源
   - 修改后端 `config/base.py` 中的 CORS 设置

4. **HTTPS**：
   - Zeabur 自动提供 HTTPS
   - 确保 OAuth 回调地址使用 HTTPS

## 📊 监控和日志

### 查看日志

在 Zeabur 控制台：
1. 选择对应服务
2. 点击 "Logs" 标签
3. 查看实时日志

### 常见问题排查

#### 后端启动失败

1. 检查环境变量是否正确设置
2. 查看日志中的错误信息
3. 确认 MySQL 连接信息正确

#### 前端无法连接后端

1. 检查 `VITE_API_BASE_URL` 是否正确
2. 确认后端 `ENABLE_CORS=true`
3. 检查后端服务是否正常运行

#### 数据库连接失败

1. 确认 MySQL 服务是否启动
2. 检查数据库环境变量
3. 查看后端日志中的详细错误

## 🔄 更新部署

### 自动部署

1. Zeabur 默认开启自动部署
2. 推送代码到 GitHub 会自动触发部署
3. 查看部署状态

### 手动部署

在 Zeabur 控制台：
1. 选择对应服务
2. 点击 "Redeploy"
3. 等待部署完成

## 📚 相关资源

- **Zeabur 文档**: https://zeabur.com/docs
- **YPrompt 文档**: 查看项目根目录 `CLAUDE.md`
- **问题反馈**: 在 GitHub 仓库提交 Issue

## 💡 提示

1. **域名配置**：
   - Zeabur 自动分配域名
   - 可以在设置中绑定自定义域名

2. **性能优化**：
   - 后端可以设置 `WORKERS` 环境变量增加并发

3. **数据备份**：
   - 定期备份 MySQL 数据库
   - 使用 Zeabur 提供的备份功能

4. **成本控制**：
   - 免费额度足够个人使用
   - 查看 Zeabur 定价页了解详情

## 🎉 完成

部署完成后，访问前端域名即可使用 YPrompt！

默认登录信息：
- 用户名：`admin`（或你设置的 `DEFAULT_ADMIN_USERNAME`）
- 密码：`admin123`（或你设置的 `DEFAULT_ADMIN_PASSWORD`）

**建议首次登录后立即修改密码！**
