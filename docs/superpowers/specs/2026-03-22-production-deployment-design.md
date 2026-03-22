# ShortPlay 生产部署优化设计

## 1. 概述

将 ShortPlay AI 短剧生成平台优化为可执行的生产版本。优化涵盖：Docker 部署配置（端口冲突解决）、后端 API 稳定性增强（限流/熔断/重试/错误处理/日志）、Nginx 生产配置、监控栈（Prometheus + Grafana）。

## 2. 端口配置方案

### 目标：避免与主机现有服务冲突

| 服务 | 原端口 (容器) | 新端口 (主机) | 说明 |
|------|---------------|---------------|------|
| PostgreSQL | 5432 | 5433 | 主机 5432 被占用 |
| Redis | 6379 | 6380 | 主机 6379 被 oexam-redis 占用 |
| RabbitMQ | 5672 | 5673 | 主机 5672 被 shortplay-mq 占用 |
| RabbitMQ Management | 15672 | 15673 | |
| MinIO API | 9000 | 9010 | 主机 9000 被 Portainer 占用 |
| MinIO Console | 9001 | 9011 | |
| Elasticsearch | 9200 | 9201 | 主机 9200 被 shortplay-es 占用 |
| Elasticsearch Transport | 9300 | 9301 | |
| Backend API | 8080 | 8081 | 内部网络通信，不暴露到主机 |
| Frontend | 3000 | 3001 | 内部网络通信，不暴露到主机 |
| Nginx | 80, 443 | 80, 443 | 保持不变，作为入口 |

### 实现方式
- `docker-compose.prod.yml` 中移除基础设施服务的端口映射（内部网络足够）
- Backend/Fronend 仅在 docker 内部网络运行，通过 Nginx 反向代理访问
- 添加 `docker-compose.override.yml` 用于本地开发覆盖端口

## 3. Docker Compose 生产配置

### 3.1 网络配置
```yaml
networks:
  shortplay-network:
    driver: bridge
```
所有服务加入统一内部网络，不暴露端口到主机（除 Nginx 80/443）。

### 3.2 服务依赖链
```
Nginx → Backend → PostgreSQL, Redis, RabbitMQ, MinIO, Elasticsearch
                     ↓
              Prometheus (metrics)
                     ↓
              Grafana (visualization)
```

### 3.3 Health Check 增强
- 所有服务添加有条件的 depends_on（service_healthy）
- Backend 依赖：postgres, redis, mq 全部健康
- 前端不依赖 backend（前端静态资源独立）

### 3.4 资源限制
```yaml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
        reservations:
          cpus: '0.5'
          memory: 512M
```

## 4. Nginx 配置

### 4.1 文件结构
```
docker/
├── nginx.conf              # 主配置
├── conf.d/
│   ├── backend.conf        # API 反向代理
│   ├── frontend.conf       # 前端静态资源
│   └── upstream.conf      # upstream 定义
└── ssl/                    # SSL 证书目录（挂载）
```

### 4.2 功能清单
- **反向代理**：/api/* → backend:8080, /* → frontend:3000
- **SSL Termination**：支持 HTTP/2，配置自有证书或 Let's Encrypt
- **Gzip 压缩**：text/html, text/css, application/json, application/javascript
- **静态资源缓存**：CSS/JS 1d, 图片 7d, 字体 30d
- **请求限流**：
  - /api/auth/*: 10 req/min（登录注册）
  - /api/*: 100 req/min（普通 API）
- **安全头**：X-Frame-Options, X-Content-Type-Options, X-XSS-Protection
- **连接超时**：proxy_connect_timeout 60s, proxy_send_timeout 60s

### 4.3 Nginx 配置片段
```nginx
# 限流 zone
limit_req_zone $binary_remote_addr zone=api_auth:10m rate=10r/m;
limit_req_zone $binary_remote_addr zone=api_general:10m rate=100r/m;

# Gzip
gzip on;
gzip_types text/plain text/css application/json application/javascript text/xml application/xml;
gzip_min_length 1000;
```

## 5. Backend API 稳定性

### 5.1 Rate Limiting（限流）
- **实现**：slowapi（基于 limits）
- **范围**：
  - 全局默认：100 req/min/IP
  - 认证端点：10 req/min/IP
  - 创作端点（生成内容）：5 req/min/IP
- **响应**：
  ```json
  {
    "code": 429,
    "message": "Rate limit exceeded",
    "detail": "Try again in 60 seconds"
  }
  ```

### 5.2 Circuit Breaker（熔断器）
- **实现**：pybreaker
- **外部服务**：
  - MinIO（文件存储）
  - Elasticsearch（搜索）
  - RabbitMQ（消息队列）
- **配置**：
  - 失败阈值：5 次
  - 恢复超时：30 秒
  - 成功阈值（恢复）：3 次
- **状态**：
  - OPEN：快速失败，返回 503
  - HALF-OPEN：探测是否恢复
  - CLOSED：正常

### 5.3 Retry（重试机制）
- **实现**：tenacity
- **场景**：外部服务调用
- **策略**：
  - 最大重试：3 次
  - 指数退避：2^n 秒（2s, 4s, 8s）
  - 可重试异常：ConnectionError, Timeout

### 5.4 统一错误处理
- **实现**：FastAPI 异常处理器 + 自定义异常类
- **异常类型**：
  - `AppException`：业务异常（携带错误码）
  - `ExternalServiceException`：外部服务异常
  - `ValidationException`：验证异常
- **响应格式**：
  ```json
  {
    "code": 400,
    "message": "Validation failed",
    "detail": {
      "field": "email",
      "error": "Invalid format"
    },
    "request_id": "uuid"
  }
  ```

### 5.5 结构化日志
- **格式**：JSON
- **字段**：
  - timestamp, level, message, request_id, user_id, path, method, status_code, duration_ms
- **实现**：python-json-logger + 自定义 formatter
- **级别**：
  - DEBUG：详细调试
  - INFO：请求/响应
  - WARNING：可恢复问题
  - ERROR：异常

## 6. 监控栈

### 6.1 Prometheus
- **服务发现**：docker-compose labels
- **抓取目标**：
  - backend:8080/metrics
  - nginx:9090/metrics（可选）
- **指标**：
  - http_requests_total（Counter）
  - http_request_duration_seconds（Histogram）
  - external_service_calls_total（Counter）
  - circuit_breaker_state（Gauge）

### 6.2 Grafana
- **数据源**：Prometheus
- **Dashboard**：
  - API 请求概览（QPS, 延迟, 错误率）
  - 服务健康状态
  - Circuit Breaker 状态
  - 外部服务调用统计

### 6.3 Docker Compose 集成
```yaml
prometheus:
  image: prom/prometheus:latest
  volumes:
    - ./prometheus.yml:/etc/prometheus/prometheus.yml
  ports:
    - "9091:9090"

grafana:
  image: grafana/grafana:latest
  ports:
    - "3002:3000"
  environment:
    - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_PASSWORD:-admin}
```

## 7. 环境变量管理

### 7.1 必需环境变量
```bash
# 数据库
DB_PASSWORD=           # PostgreSQL 密码

# Redis
REDIS_PASSWORD=        # Redis 密码（可选）

# RabbitMQ
MQ_PASSWORD=           # RabbitMQ 密码

# MinIO
MINIO_ACCESS_KEY=      # MinIO access key
MINIO_SECRET_KEY=      # MinIO secret key

# JWT
JWT_SECRET_KEY=        # 生产必须更换

# Grafana
GRAFANA_PASSWORD=      # Grafana admin 密码

# SSL（可选）
SSL_CERT_PATH=         # SSL 证书路径
SSL_KEY_PATH=         # SSL 私钥路径
```

### 7.2 环境变量验证
- 使用 pydantic 进行启动时验证
- 缺失必需变量时应用启动失败（fail-fast）

## 8. 文件变更清单

### 新增文件
```
docker/
├── conf.d/
│   ├── upstream.conf
│   ├── backend.conf
│   └── frontend.conf
├── prometheus.yml
└── grafana/
    └── provisioning/
        └── dashboards/
            └── api-dashboard.json

backend/app/core/
├── exceptions.py          # 自定义异常类
├── middleware.py          # 请求日志、错误处理中间件
├── logging.py            # 结构化日志配置
└── circuit_breaker.py     # 熔断器配置

backend/app/api/v1/
└── middleware.py          # Rate limiting 中间件

docs/superpowers/specs/
└── 2026-03-22-production-deployment-design.md
```

### 修改文件
```
docker/
├── docker-compose.prod.yml    # 端口调整、资源限制、监控栈
├── docker-compose.override.yml # 本地开发覆盖
└── nginx.conf                 # 完整 nginx 配置

backend/
├── Dockerfile                  # 添加 curl 用于 healthcheck
├── app/main.py                 # 注册中间件、异常处理器
├── app/core/config.py          # 增强环境变量验证
├── pyproject.toml              # 添加依赖：slowapi, pybreaker, tenacity, python-json-logger

frontend/
└── Dockerfile                  # 多阶段构建优化
```

### 删除/注释文件
- 无

## 9. 部署流程

### 9.1 生产部署
```bash
# 1. 配置环境变量
cp .env.example .env
vim .env  # 填写所有必需变量

# 2. 构建并启动
cd docker
docker compose -f docker-compose.prod.yml up -d

# 3. 验证
curl https://your-domain/health
```

### 9.2 本地开发
```bash
# 使用 override 覆盖生产配置
docker compose -f docker-compose.yml -f docker-compose.override.yml up -d
```

## 10. 验证清单

- [ ] 所有基础设施服务启动成功
- [ ] Backend /health 返回 200
- [ ] Nginx 正确反向代理 /api/* 和 /*
- [ ] Rate limiting 生效（超过限制返回 429）
- [ ] Circuit breaker 状态正常（CLOSED）
- [ ] 日志输出 JSON 格式
- [ ] Prometheus 抓取到 backend 指标
- [ ] Grafana dashboard 可访问
- [ ] 端口不与主机现有服务冲突
