# ShortPlay MVP 部署设计

## 1. 概述

MVP 版本：专注于功能实现，去除监控、网络限制等非核心配置。

**保留内容：**
- Docker 部署配置（端口冲突解决）
- 基础 Nginx 反向代理
- 后端 API 稳定性增强（限流/熔断/重试/错误处理/日志）

**移除内容：**
- Prometheus / Grafana 监控栈
- 复杂的网络配置
- SSL/Gzip/缓存等非必需功能

## 2. 端口配置

### 目标：避免与主机现有服务冲突

通过 `docker-compose.override.yml` 覆盖默认端口：

| 服务 | 默认端口 | 开发端口 | 说明 |
|------|----------|----------|------|
| PostgreSQL | 5432 | 5433 | 主机 5432 被占用 |
| Redis | 6379 | 6380 | 主机 6379 被占用 |
| RabbitMQ | 5672 | 5673 | 主机 5672 被占用 |
| MinIO API | 9000 | 9010 | 主机 9000 被占用 |
| Backend | 8080 | 8081 | 开发环境暴露 |
| Frontend | 3000 | 3001 | 开发环境暴露 |

**生产环境**：移除端口映射，仅内部网络通信，通过 Nginx 访问。

## 3. Docker Compose 配置

### 3.1 开发环境 (docker-compose.override.yml)
```yaml
services:
  postgres:
    ports:
      - "5433:5432"
  redis:
    ports:
      - "6380:6379"
  mq:
    ports:
      - "5673:5672"
      - "15673:15672"
  minio:
    ports:
      - "9010:9000"
      - "9011:9001"
  backend:
    ports:
      - "8081:8080"
  frontend:
    ports:
      - "3001:3000"
```

### 3.2 生产环境 (docker-compose.prod.yml)
- 移除基础设施端口映射
- Backend/Fronend 仅内部网络运行
- 通过 Nginx 反向代理访问

## 4. Nginx 配置

### 4.1 基础反向代理
```nginx
server {
    listen 80;
    server_name localhost;

    location /api/ {
        proxy_pass http://backend:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location / {
        proxy_pass http://frontend:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 4.2 功能清单
- 反向代理 /api/* → backend:8080
- 反向代理 /* → frontend:3000
- 基础代理头传递

## 5. Backend API 稳定性

### 5.1 Rate Limiting（限流）
- **实现**：slowapi
- **范围**：
  - 全局默认：100 req/min/IP
  - 认证端点：10 req/min/IP
  - 创作端点：5 req/min/IP

### 5.2 Circuit Breaker（熔断器）
- **实现**：pybreaker
- **外部服务**：MinIO, RabbitMQ
- **配置**：失败阈值 5 次，恢复超时 30 秒

### 5.3 Retry（重试机制）
- **实现**：tenacity
- **策略**：最大重试 3 次，指数退避 2s/4s/8s

### 5.4 统一错误处理
- 自定义异常类：AppException, ExternalServiceException
- 响应格式：标准 JSON { code, message, detail }

### 5.5 结构化日志
- JSON 格式日志
- 字段：timestamp, level, message, request_id, path, method, status_code

## 6. 环境变量

### 必需环境变量
```bash
DB_PASSWORD=           # PostgreSQL 密码
MQ_PASSWORD=           # RabbitMQ 密码
MINIO_ACCESS_KEY=      # MinIO access key
MINIO_SECRET_KEY=      # MinIO secret key
JWT_SECRET_KEY=        # 生产必须更换
```

## 7. 文件变更清单

### 新增文件
```
docker/
├── conf.d/
│   └── default.conf   # Nginx 基础配置
├── docker-compose.override.yml  # 开发环境端口覆盖

backend/app/core/
├── exceptions.py      # 自定义异常类
├── middleware.py      # 请求日志、错误处理中间件
├── logging.py         # 结构化日志配置
└── circuit_breaker.py # 熔断器配置

backend/app/api/v1/
└── middleware.py      # Rate limiting 中间件

docs/superpowers/specs/
└── 2026-03-22-production-deployment-design.md
```

### 修改文件
```
docker/
├── docker-compose.prod.yml  # 简化配置
└── nginx.conf               # 基础反向代理

backend/
├── Dockerfile
├── app/main.py              # 注册中间件、异常处理器
├── app/core/config.py       # 环境变量验证
└── pyproject.toml          # 添加依赖

frontend/
└── Dockerfile
```

## 8. 依赖清单

```toml
# backend/pyproject.toml 新增
slowapi = "^0.9"
pybreaker = "^1.0"
tenacity = "^8.0"
python-json-logger = "^2.0"
```

## 9. 部署流程

### 9.1 开发环境
```bash
cd docker
cp .env.example .env  # 配置环境变量
docker compose up -d  # 使用默认配置
```

### 9.2 生产环境
```bash
cd docker
docker compose -f docker-compose.prod.yml up -d
```

## 10. 验证清单

- [ ] 所有基础设施服务启动成功
- [ ] Backend /health 返回 200
- [ ] Nginx 正确反向代理 /api/* 和 /*
- [ ] Rate limiting 生效
- [ ] Circuit breaker 状态正常
- [ ] 日志输出 JSON 格式
- [ ] 端口不与主机现有服务冲突
