# ShortPlay - AI 短剧生成平台

## 1. 项目概述

**ShortPlay** 是一个面向短剧创作的全流程AI生成平台，使用 FastAPI + React + TailwindCSS + PostgreSQL 构建。

### 核心功能流程
```
文本输入 → 信息提取 → 角色/场景资产生成 → 分镜管理 → 视频生成 → 视频编辑
```

### 技术栈

| 层级 | 技术选型 |
|------|----------|
| 后端框架 | FastAPI (Python 3.11+) |
| 前端框架 | React 18 + TypeScript |
| UI框架 | TailwindCSS + shadcn/ui |
| 数据库 | PostgreSQL 15 |
| 缓存 | Redis 7 |
| 消息队列 | RabbitMQ 4.x |
| 搜索引擎 | Elasticsearch 8.11 (IK+pinyin) |
| 向量数据库 | PostgreSQL pgvector |
| 对象存储 | MinIO |
| 容器化 | Docker + Docker Compose |

---

## 2. 功能模块

### 2.1 项目管理 (Project)
- 创建/编辑/删除项目
- 项目列表分页 + 关键词搜索
- 项目状态筛选（草稿/处理中/已完成）
- 项目封面管理

### 2.2 章节管理 (Episode)
- 创建/编辑/删除章节
- 步骤状态维护 (current_step)
- 步骤跳转控制

### 2.3 信息提取 (Extraction)
- 从章节文本提取角色与场景
- 支持重新提取
- 手动选择文本模型

### 2.4 资产管理 (Asset)
- 角色/场景 CRUD
- 角色图/场景图生成 + 再生
- 图片上传替换
- 资产搜索 (Elasticsearch)

### 2.5 分镜管理 (Storyboard)
- 生成分镜（可选向量检索增强）
- 镜头配置（类型、时长、描述）
- 角色关联（最多3个）
- 场景关联（必须1个）

### 2.6 视频生成 (Video)
- 首帧提示词生成
- 首帧图片生成
- 分镜视频生成
- WebSocket状态推送

### 2.7 模型管理 (Model)
- 厂商管理
- 模型实例 (TEXT/IMAGE/VIDEO/AUDIO)
- 默认模型设置

### 2.8 提示词管理 (Prompt)
- 多场景提示词模板
- 默认提示词设置

---

## 3. 数据库设计

### 核心表结构

1. **project** - 项目表
2. **episode** - 章节表
3. **character** - 角色表
4. **scene** - 场景表
5. **storyboard** - 分镜表
6. **storyboard_character** - 分镜角色关联表
7. **storyboard_scene** - 分镜场景关联表
8. **generated_image** - 生成图片表
9. **video_task** - 视频任务表
10. **model_definition** - 模型定义表
11. **model_instance** - 模型实例表
12. **model_instance_default** - 默认模型配置表
13. **prompt_template** - 提示词模板表
14. **prompt_template_default** - 默认提示词配置表
15. **style_template** - 风格模板表

---

## 4. API 设计

采用 RESTful + WebSocket 混合架构。

详细 API 文档见 `docs/4-api.md`

---

## 5. 测试策略

- 单元测试 (pytest)
- API 集成测试
- 覆盖率目标: 80%+

详细测试文档见 `docs/5-testing.md`
