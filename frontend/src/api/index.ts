import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    const message = error.response?.data?.message || error.message || 'An error occurred'
    return Promise.reject(new Error(message))
  }
)

export interface Project {
  id: number
  name: string
  description?: string
  cover?: string
  style_id?: number
  status: number
  consistency: number
  chapter_count: number
  progress: number
  created_at: string
  updated_at: string
}

export interface Episode {
  id: number
  project_id: number
  chapter_number: number
  name: string
  content?: string
  status: number
  progress: number
  current_step: number
  created_at: string
  updated_at: string
}

export interface Character {
  id: number
  episode_id: number
  project_id: number
  name: string
  description?: string
  avatar?: string
  video_url?: string
  created_at: string
  updated_at: string
}

export interface Scene {
  id: number
  episode_id: number
  project_id: number
  name: string
  description?: string
  thumbnail?: string
  created_at: string
  updated_at: string
}

export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  page_size: number
  total_pages?: number
}

export interface ApiResponse<T> {
  code: number
  data: T
  message: string
}

// Project APIs
export const projectApi = {
  list: (params?: { page?: number; page_size?: number; keyword?: string; status?: number }) =>
    api.get<ApiResponse<PaginatedResponse<Project>>>('/projects', { params }),

  get: (id: number) =>
    api.get<ApiResponse<Project>>(`/projects/${id}`),

  create: (data: { name: string; description?: string }) =>
    api.post<ApiResponse<Project>>('/projects', data),

  update: (id: number, data: Partial<{ name: string; description: string; status: number }>) =>
    api.put<ApiResponse<Project>>(`/projects/${id}`, data),

  delete: (id: number) =>
    api.delete<ApiResponse<{ id: number; deleted: boolean }>>(`/projects/${id}`),
}

// Episode APIs
export const episodeApi = {
  list: (projectId: number, params?: { page?: number; page_size?: number }) =>
    api.get<ApiResponse<PaginatedResponse<Episode>>>(`/projects/${projectId}/episodes`, { params }),

  get: (id: number) =>
    api.get<ApiResponse<Episode>>(`/episodes/${id}`),

  create: (projectId: number, data: { name: string; content?: string; chapter_number?: number }) =>
    api.post<ApiResponse<Episode>>(`/projects/${projectId}/episodes`, data),

  update: (id: number, data: Partial<{ name: string; content: string; current_step: number }>) =>
    api.put<ApiResponse<Episode>>(`/episodes/${id}`, data),

  delete: (id: number) =>
    api.delete<ApiResponse<{ id: number; deleted: boolean }>>(`/episodes/${id}`),

  extract: (id: number, modelInstanceId?: number) =>
    api.post<ApiResponse<{ characters: Character[]; scenes: Scene[] }>>(`/episodes/${id}/extract`, null, {
      params: { model_instance_id: modelInstanceId },
    }),
}

// Character APIs
export const characterApi = {
  list: (projectId: number, params?: { page?: number; page_size?: number; keyword?: string }) =>
    api.get<ApiResponse<PaginatedResponse<Character>>>(`/projects/${projectId}/characters`, { params }),

  get: (id: number) =>
    api.get<ApiResponse<Character>>(`/characters/${id}`),

  create: (projectId: number, data: { episode_id: number; name: string; description?: string }) =>
    api.post<ApiResponse<Character>>(`/projects/${projectId}/characters`, data),

  update: (id: number, data: Partial<{ name: string; description: string; avatar: string }>) =>
    api.put<ApiResponse<Character>>(`/characters/${id}`, data),

  delete: (id: number) =>
    api.delete<ApiResponse<{ id: number; deleted: boolean }>>(`/characters/${id}`),
}

// Scene APIs
export const sceneApi = {
  list: (projectId: number, params?: { page?: number; page_size?: number; keyword?: string }) =>
    api.get<ApiResponse<PaginatedResponse<Scene>>>(`/projects/${projectId}/scenes`, { params }),

  get: (id: number) =>
    api.get<ApiResponse<Scene>>(`/scenes/${id}`),

  create: (projectId: number, data: { episode_id: number; name: string; description?: string }) =>
    api.post<ApiResponse<Scene>>(`/projects/${projectId}/scenes`, data),

  update: (id: number, data: Partial<{ name: string; description: string; thumbnail: string }>) =>
    api.put<ApiResponse<Scene>>(`/scenes/${id}`, data),

  delete: (id: number) =>
    api.delete<ApiResponse<{ id: number; deleted: boolean }>>(`/scenes/${id}`),
}

// Model Provider APIs
export interface ModelProvider {
  id: number
  name: string
  provider_type: string  // openai/minimax/claude/custom
  api_base?: string
  api_key?: string
  status: number
  created_at: string
  updated_at: string
}

export interface ModelInstance {
  id: number
  provider_id?: number
  model_def_id?: number
  model_code: string
  model_type: number  // 1-TEXT 2-IMAGE 3-VIDEO 4-AUDIO
  instance_name: string
  scene_code?: number
  api_key?: string
  path?: string
  params?: Record<string, any>  // temperature, max_tokens, etc.
  is_default: boolean
  status: number
  created_at: string
  updated_at: string
}

export interface ProjectModelConfig {
  project_id: number
  overrides: Record<number, number | null>  // {model_type: instance_id or null}
  defaults: Record<number, { id: number; instance_name: string; model_code: string } | null>
}

// Provider APIs
export const providerApi = {
  list: () =>
    api.get<ApiResponse<ModelProvider[]>>('/providers'),

  get: (id: number) =>
    api.get<ApiResponse<ModelProvider>>(`/providers/${id}`),

  create: (data: { name: string; provider_type: string; api_base?: string; api_key?: string; status?: number }) =>
    api.post<ApiResponse<ModelProvider>>('/providers', data),

  update: (id: number, data: Partial<{ name: string; provider_type: string; api_base: string; api_key: string; status: number }>) =>
    api.put<ApiResponse<ModelProvider>>(`/providers/${id}`, data),

  delete: (id: number) =>
    api.delete<ApiResponse<{ id: number; deleted: boolean }>>(`/providers/${id}`),
}

// Model Instance APIs
export const modelApi = {
  listInstances: (params?: { provider_id?: number; model_type?: number }) =>
    api.get<ApiResponse<{ items: ModelInstance[]; total: number; page: number; page_size: number }>>('/models/instances', { params }),

  getInstance: (id: number) =>
    api.get<ApiResponse<ModelInstance>>(`/models/instances/${id}`),

  createInstance: (data: {
    model_code: string
    model_type: number
    instance_name: string
    provider_id?: number
    scene_code?: number
    api_key?: string
    params?: Record<string, any>
    path?: string
    is_default?: boolean
  }) =>
    api.post<ApiResponse<ModelInstance>>('/models/instances', data),

  updateInstance: (id: number, data: Partial<{
    model_code: string
    model_type: number
    instance_name: string
    provider_id: number
    scene_code: number
    api_key: string
    params: Record<string, any>
    path: string
    is_default: boolean
    status: number
  }>) =>
    api.put<ApiResponse<ModelInstance>>(`/models/instances/${id}`, data),

  deleteInstance: (id: number) =>
    api.delete<ApiResponse<{ id: number; deleted: boolean }>>(`/models/instances/${id}`),

  setDefault: (id: number, model_type: number) =>
    api.put<ApiResponse<any>>(`/models/instances/${id}/default`, null, { params: { model_type } }),

  getDefault: (model_type: number) =>
    api.get<ApiResponse<ModelInstance>>('/models/instances/default', { params: { model_type } }),
}

// Project Model Config APIs
export const projectModelApi = {
  getConfig: (projectId: number) =>
    api.get<ApiResponse<ProjectModelConfig>>(`/projects/${projectId}/model-config`),

  setOverride: (projectId: number, data: { model_instance_id: number; model_type: number }) =>
    api.put<ApiResponse<any>>(`/projects/${projectId}/model-config`, data),

  deleteOverride: (projectId: number, modelType: number) =>
    api.delete<ApiResponse<any>>(`/projects/${projectId}/model-config/${modelType}`),
}

export default api
