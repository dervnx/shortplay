# 大模型配置设计

> **Goal:** 支持多 Provider、自定义 Endpoint 和参数配置，提供全局默认 + 项目级覆盖的灵活模型选择机制

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      前端模型配置                            │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐    ┌─────────────────────────────┐   │
│  │   全局默认配置   │    │     Provider 管理            │   │
│  │  (模型配置页)    │    │  - OpenAI / MiniMax / 自定义 │   │
│  │                 │    │  - API Key / Endpoint / 参数  │   │
│  └────────┬────────┘    └─────────────────────────────┘   │
│           │                                               │
│           ▼                                               │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              项目级模型覆盖 (可选)                     │   │
│  │         ProjectDetailPage → 模型选择卡              │   │
│  └─────────────────────────────────────────────────────┘   │
│           │                                               │
│           ▼                                               │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              快速切换器 (使用点)                      │   │
│  │   EpisodeDetailPage → 提取信息/生成图片 侧边栏       │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## Data Model

### Provider (ModelProvider)
- `id` (PK)
- `name` (string, e.g., "MiniMax", "OpenAI")
- `provider_type` (enum: openai/minimax/claude/custom)
- `api_base` (string, API endpoint URL)
- `api_key` (string, encrypted)
- `status` (int, 0=disabled, 1=enabled)
- `created_at`, `updated_at`

### ModelInstance
- `id` (PK)
- `provider_id` (FK → ModelProvider)
- `model_code` (string, e.g., "gpt-4o", "MiniMax-Text-01")
- `model_type` (int, 1=文本, 2=图像, 3=视频, 4=语音)
- `instance_name` (string, display name)
- `is_default` (bool, 是否全局默认)
- `params` (JSON, temperature, max_tokens 等)
- `status` (int, 0=disabled, 1=enabled)
- `created_at`, `updated_at`

### ProjectModelOverride
- `id` (PK)
- `project_id` (FK → Project)
- `model_instance_id` (FK → ModelInstance)
- `model_type` (int, 1-4)
- `created_at`, `updated_at`

## API Endpoints

### Provider APIs
```
GET    /api/models/providers          # List providers
POST   /api/models/providers          # Create provider
GET    /api/models/providers/{id}    # Get provider
PUT    /api/models/providers/{id}    # Update provider
DELETE /api/models/providers/{id}    # Delete provider
```

### Instance APIs
```
GET    /api/models/instances         # List instances (filter by type/provider)
POST   /api/models/instances          # Create instance
GET    /api/models/instances/{id}    # Get instance
PUT    /api/models/instances/{id}    # Update instance
DELETE /api/models/instances/{id}    # Delete instance
PUT    /api/models/instances/{id}/default  # Set as default for type
GET    /api/models/instances/default  # Get defaults by type
```

### Project Override APIs
```
GET    /api/projects/{id}/model-config      # Get project model config (override + defaults)
PUT    /api/projects/{id}/model-config      # Set project model override
DELETE /api/projects/{id}/model-config/{type}  # Remove override
```

## Frontend Components

1. **ModelConfigPage** - Provider + Instance 管理，设定全局默认
2. **ProjectModelCard** - ProjectDetailPage 中的模型选择，显示/设置项目级覆盖
3. **ModelQuickSwitcher** - 使用点的快速切换浮层

## LLM Call Flow

```python
# 优先级：项目覆盖 > 全局默认 > 异常
def get_llm_for_task(project_id: int, task_type: int):
    # 1. Check project override
    if override := get_project_model_override(project_id, task_type):
        return create_llm(override.instance)
    # 2. Get global default
    if default := get_default_model(task_type):
        return create_llm(default)
    # 3. Error
    raise NoModelConfiguredError(task_type)
```

## Implementation Tasks

1. Create ModelProvider model and migration
2. Update ModelInstance model (add provider_id, is_default, params)
3. Create ProjectModelOverride model
4. Create Provider API routes
5. Update Instance API routes
6. Create Project Model Config API
7. Create frontend API client functions
8. Update ModelConfigPage to use real APIs
9. Add ProjectModelCard to ProjectDetailPage
10. Create ModelQuickSwitcher component
