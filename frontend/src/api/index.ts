import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api/v1'

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

export default api
