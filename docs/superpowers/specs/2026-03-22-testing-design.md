# ShortPlay 测试完整性设计

## 1. 概述

在 Docker 容器内执行完整测试，确保功能完整性和可靠性。生成完整测试报告。

## 2. 测试环境

### 2.1 容器内测试
- 使用 `docker compose run --rm backend pytest` 执行
- 测试数据库：SQLite in-memory（现有 conftest.py）
- 报告输出到 `/app/test-results/`

### 2.2 依赖
```dockerfile
# backend/Dockerfile.test
FROM python:3.11-slim
RUN pip install pytest pytest-cov pytest-html pytest-asyncio
# 其他测试依赖
```

## 3. 测试范围

### 3.1 API 测试 (tests/api/)
- `test_projects.py` - 项目 CRUD
- `test_episodes.py` - 剧集 CRUD + extract 端点
- `test_characters.py` - 角色 CRUD
- `test_scenes.py` - 场景 CRUD
- `test_storyboards.py` - 分镜 CRUD + generate 端点

### 3.2 Service 测试 (tests/services/)
- `test_project_service.py`
- `test_episode_service.py`
- `test_character_service.py`

### 3.3 AI 功能测试 (tests/ai/)
- `test_entity_extractor.py` - FilmEntityExtractor 输出验证
- `test_storyboarder.py` - FilmStoryboarder 输出验证
- `test_end_to_end.py` - extract -> generate 完整流程

### 3.4 测试内容

| 测试类型 | 验证点 |
|----------|--------|
| API 功能 | 端点存在、参数验证、响应格式、错误码 |
| Service 逻辑 | 业务规则、数据验证、边界条件 |
| AI 输出 | 输出结构、必要字段、内容质量 |
| 端到端 | 全流程执行、数据一致性 |

## 4. 测试报告

### 4.1 报告生成
```bash
pytest --cov=app --html=test-results/report.html --cov-report=html
```

### 4.2 报告内容
- HTML 测试报告 (pytest-html)
- 覆盖率报告 (coverage)
- 输出目录: `backend/test-results/`

### 4.3 挂载配置
```yaml
# docker-compose.yml
volumes:
  - ./backend/test-results:/app/test-results
```

## 5. 执行方式

### 5.1 完整测试
```bash
docker compose run --rm backend pytest --cov=app --html=test-results/report.html
```

### 5.2 分模块测试
```bash
# API 测试
docker compose run --rm backend pytest tests/api/

# Service 测试
docker compose run --rm backend pytest tests/services/

# AI 功能测试
docker compose run --rm backend pytest tests/ai/

# 端到端测试
docker compose run --rm backend pytest tests/ai/test_end_to_end.py
```

### 5.3 带覆盖率的测试
```bash
docker compose run --rm backend pytest --cov=app --cov-report=html tests/
```

## 6. 文件变更

### 新增文件
```
backend/Dockerfile.test           # 测试容器镜像
backend/tests/ai/                # AI 功能测试目录
backend/tests/ai/__init__.py
backend/tests/ai/test_entity_extractor.py
backend/tests/ai/test_storyboarder.py
backend/tests/ai/test_end_to_end.py
backend/test-results/             # 测试报告输出目录
```

### 修改文件
```
backend/pyproject.toml            # 添加测试依赖
docker-compose.yml               # 添加 test 服务和 volume
```

## 7. 验证清单

- [ ] 测试容器可正常构建
- [ ] API 测试全部通过
- [ ] Service 测试全部通过
- [ ] AI 功能测试全部通过
- [ ] 端到端测试通过
- [ ] HTML 报告生成成功
- [ ] 覆盖率报告生成成功
