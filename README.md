# ShortPlay - AI 短剧生成平台

基于 FastAPI + React + TailwindCSS + PostgreSQL 构建的 AI 短剧创作平台。

## 项目结构

```
shortplay/
├── docs/               # 项目文档
│   ├── 1-项目概述.md    # 项目概述
│   ├── 2-架构设计.md    # 架构设计
│   ├── 3-数据库设计.md  # 数据库设计 (PostgreSQL)
│   ├── 4-API文档.md     # API 文档
│   ├── 5-测试文档.md     # 测试文档
│   └── 6-部署文档.md     # 部署文档
│
├── backend/            # 后端 (FastAPI)
│   ├── app/
│   │   ├── api/v1/    # API 路由
│   │   ├── core/      # 核心配置
│   │   ├── models/    # SQLAlchemy 模型
│   │   ├── schemas/   # Pydantic 模式
│   │   ├── services/  # 业务逻辑
│   │   └── repositories/ # 数据访问层
│   ├── tests/         # 测试代码
│   ├── pyproject.toml
│   └── Dockerfile
│
├── frontend/           # 前端 (React + TailwindCSS)
│   ├── src/
│   │   ├── components/ # 组件
│   │   ├── pages/     # 页面
│   │   ├── hooks/     # Hooks
│   │   └── api/       # API 客户端
│   ├── package.json
│   └── Dockerfile
│
└── docker/             # Docker 配置
    ├── docker-compose.yml       # 开发环境
    └── docker-compose.prod.yml  # 生产环境
```

## 快速开始

### 1. 启动基础设施

```bash
cd docker
docker compose up -d
```

### 2. 启动后端

```bash
cd backend
pip install -e .
uvicorn app.main:app --reload --port 8080
```

### 3. 启动前端

```bash
cd frontend
npm install
npm run dev
```

### 4. 访问

- 前端: http://localhost:3000
- API 文档: http://localhost:8080/docs

## 功能模块

| 模块 | 描述 |
|------|------|
| 项目管理 | 创建/编辑/删除/搜索项目 |
| 章节管理 | 章节 CRUD + 步骤状态 |
| 信息提取 | LLM 提取角色 + 场景 |
| 资产管理 | 角色/场景图片管理 |
| 分镜管理 | 镜头脚本 + 关联资产 |
| 视频生成 | 首帧 + 分镜视频生成 |
| 模型管理 | 多厂商模型配置 |
| 提示词管理 | 模板管理 |

## 技术栈

| 层级 | 技术 |
|------|------|
| 后端 | FastAPI, SQLAlchemy, Pydantic |
| 前端 | React 18, TypeScript, TailwindCSS |
| 数据库 | PostgreSQL 16 + pgvector |
| 缓存 | Redis 7 |
| 消息队列 | RabbitMQ 4.x |
| 搜索引擎 | Elasticsearch 8.11 |
| 对象存储 | MinIO |

## 运行测试

```bash
cd backend
pytest --cov=app
```

## 生产部署

```bash
docker compose -f docker/docker-compose.prod.yml up -d
```
