# API 文档

## 1. API 规范

### 1.1 基础信息

- **Base URL**: `http://localhost:8080/api/v1`
- **Content-Type**: `application/json`
- **认证方式**: Bearer Token (JWT)

### 1.2 响应格式

```json
{
  "code": 200,
  "data": { ... },
  "message": "success"
}
```

### 1.3 错误响应

```json
{
  "code": 400,
  "data": null,
  "message": "错误描述"
}
```

### 1.4 HTTP 状态码

| 状态码 | 描述 |
|--------|------|
| 200 | 成功 |
| 201 | 创建成功 |
| 400 | 请求参数错误 |
| 401 | 未授权 |
| 403 | 禁止访问 |
| 404 | 资源不存在 |
| 500 | 服务器错误 |

---

## 2. 项目管理 (Project)

### 2.1 创建项目

```
POST /api/v1/projects
```

**请求体:**
```json
{
  "name": "我的短剧",
  "description": "项目描述",
  "style_id": 1
}
```

**响应:**
```json
{
  "code": 200,
  "data": {
    "id": 1,
    "name": "我的短剧",
    "description": "项目描述",
    "cover": null,
    "style_id": 1,
    "status": 0,
    "progress": 0,
    "created_at": "2026-03-22T10:00:00Z"
  }
}
```

### 2.2 项目列表

```
GET /api/v1/projects
```

**查询参数:**
| 参数 | 类型 | 描述 |
|------|------|------|
| page | int | 页码 (默认1) |
| page_size | int | 每页数量 (默认10) |
| status | int | 状态筛选 (可选) |
| keyword | string | 关键词搜索 (可选) |

**响应:**
```json
{
  "code": 200,
  "data": {
    "items": [...],
    "total": 100,
    "page": 1,
    "page_size": 10
  }
}
```

### 2.3 获取项目详情

```
GET /api/v1/projects/{id}
```

### 2.4 更新项目

```
PUT /api/v1/projects/{id}
```

### 2.5 删除项目

```
DELETE /api/v1/projects/{id}
```

---

## 3. 章节管理 (Episode)

### 3.1 创建章节

```
POST /api/v1/projects/{project_id}/episodes
```

**请求体:**
```json
{
  "name": "第一章",
  "content": "章节内容..."
}
```

### 3.2 章节列表

```
GET /api/v1/projects/{project_id}/episodes
```

### 3.3 获取章节详情

```
GET /api/v1/episodes/{id}
```

### 3.4 更新章节

```
PUT /api/v1/episodes/{id}
```

### 3.5 删除章节

```
DELETE /api/v1/episodes/{id}
```

### 3.6 信息提取

```
POST /api/v1/episodes/{id}/extract
```

**请求体:**
```json
{
  "model_instance_id": 1,
  "use_vector": false
}
```

**响应:**
```json
{
  "code": 200,
  "data": {
    "characters": [
      {
        "id": 1,
        "name": "角色名称",
        "description": "角色描述"
      }
    ],
    "scenes": [
      {
        "id": 1,
        "name": "场景名称",
        "description": "场景描述"
      }
    ]
  }
}
```

---

## 4. 角色管理 (Character)

### 4.1 获取角色列表

```
GET /api/v1/projects/{project_id}/characters
```

### 4.2 创建角色

```
POST /api/v1/projects/{project_id}/characters
```

**请求体:**
```json
{
  "episode_id": 1,
  "name": "角色名称",
  "description": "角色描述"
}
```

### 4.3 更新角色

```
PUT /api/v1/characters/{id}
```

### 4.4 删除角色

```
DELETE /api/v1/characters/{id}
```

### 4.5 生成角色图片

```
POST /api/v1/characters/{id}/generate-image
```

**请求体:**
```json
{
  "model_instance_id": 7,
  "style_id": 2
}
```

---

## 5. 场景管理 (Scene)

### 5.1 获取场景列表

```
GET /api/v1/projects/{project_id}/scenes
```

### 5.2 创建场景

```
POST /api/v1/projects/{project_id}/scenes
```

### 5.3 更新场景

```
PUT /api/v1/scenes/{id}
```

### 5.4 删除场景

```
DELETE /api/v1/scenes/{id}
```

### 5.5 生成场景图片

```
POST /api/v1/scenes/{id}/generate-image
```

---

## 6. 分镜管理 (Storyboard)

### 6.1 获取分镜列表

```
GET /api/v1/episodes/{episode_id}/storyboards
```

### 6.2 生成分镜

```
POST /api/v1/episodes/{episode_id}/storyboards/generate
```

**请求体:**
```json
{
  "model_instance_id": 10,
  "use_vector": false
}
```

### 6.3 更新分镜

```
PUT /api/v1/storyboards/{id}
```

### 6.4 删除分镜

```
DELETE /api/v1/storyboards/{id}
```

### 6.5 关联角色

```
POST /api/v1/storyboards/{id}/characters
```

**请求体:**
```json
{
  "character_ids": [1, 2, 3]
}
```

### 6.6 关联场景

```
POST /api/v1/storyboards/{id}/scene
```

**请求体:**
```json
{
  "scene_id": 1
}
```

---

## 7. 视频任务 (Video Task)

### 7.1 生成首帧提示词

```
POST /api/v1/storyboards/{id}/first-frame-prompt
```

### 7.2 生成首帧图片

```
POST /api/v1/storyboards/{id}/first-frame-image
```

### 7.3 生成分镜视频

```
POST /api/v1/storyboards/{id}/generate-video
```

**请求体:**
```json
{
  "model_instance_id": 11,
  "duration": 5
}
```

### 7.4 获取任务状态

```
GET /api/v1/video-tasks/{id}
```

### 7.5 WebSocket 推送

```
WS /api/v1/ws/{project_id}
```

**推送消息格式:**
```json
{
  "type": "video_task_update",
  "data": {
    "task_id": 1,
    "status": "success",
    "progress": 100,
    "video_url": "..."
  }
}
```

---

## 8. 模型管理 (Model)

### 8.1 获取模型厂商列表

```
GET /api/v1/model-definitions
```

### 8.2 创建模型厂商

```
POST /api/v1/model-definitions
```

### 8.3 获取模型实例列表

```
GET /api/v1/model-instances
```

**查询参数:**
| 参数 | 类型 | 描述 |
|------|------|------|
| model_type | int | 模型类型 (可选) |
| scene_code | int | 场景代码 (可选) |

### 8.4 创建模型实例

```
POST /api/v1/model-instances
```

**请求体:**
```json
{
  "model_def_id": 1,
  "model_code": "gpt-4o",
  "model_type": 1,
  "instance_name": "GPT-4o",
  "scene_code": 1,
  "api_key": "sk-...",
  "params": {
    "max_tokens": 8192,
    "temperature": 0.3
  }
}
```

### 8.5 更新模型实例

```
PUT /api/v1/model-instances/{id}
```

### 8.6 删除模型实例

```
DELETE /api/v1/model-instances/{id}
```

### 8.7 设置默认模型

```
PUT /api/v1/model-instances/{id}/default
```

---

## 9. 提示词管理 (Prompt)

### 9.1 获取提示词列表

```
GET /api/v1/prompt-templates
```

**查询参数:**
| 参数 | 类型 | 描述 |
|------|------|------|
| scene_code | int | 场景代码 (可选) |

### 9.2 创建提示词

```
POST /api/v1/prompt-templates
```

### 9.3 更新提示词

```
PUT /api/v1/prompt-templates/{id}
```

### 9.4 删除提示词

```
DELETE /api/v1/prompt-templates/{id}
```

### 9.5 设置默认提示词

```
PUT /api/v1/prompt-templates/{id}/default
```

---

## 10. 搜索 (Search)

### 10.1 搜索项目

```
GET /api/v1/search/projects
```

**查询参数:**
| 参数 | 类型 | 描述 |
|------|------|------|
| keyword | string | 关键词 |
| suggest | bool | 是否返回补全建议 |

### 10.2 搜索角色

```
GET /api/v1/search/characters
```

### 10.3 搜索场景

```
GET /api/v1/search/scenes
```

---

## 11. 文件上传 (File)

### 11.1 上传图片

```
POST /api/v1/files/upload
```

**Form Data:**
| 字段 | 类型 | 描述 |
|------|------|------|
| file | file | 图片文件 |
| type | string | avatar/thumbnail/cover |

**响应:**
```json
{
  "code": 200,
  "data": {
    "url": "http://minio:9000/shortplay/xxx.png"
  }
}
```

---

## 12. 风格模板 (Style)

### 12.1 获取风格列表

```
GET /api/v1/style-templates
```

### 12.2 创建风格

```
POST /api/v1/style-templates
```

### 12.3 更新风格

```
PUT /api/v1/style-templates/{id}
```

### 12.4 删除风格

```
DELETE /api/v1/style-templates/{id}
```

### 12.5 设置默认风格

```
PUT /api/v1/style-templates/{id}/default
```
