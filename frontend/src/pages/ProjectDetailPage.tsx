import { useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { ArrowLeft, Plus, Play, Users, MapPin, Clapperboard, Bot, Star } from 'lucide-react'
import toast from 'react-hot-toast'

import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'
import { projectApi, episodeApi, characterApi, sceneApi, projectModelApi, modelApi, ProjectModelConfig } from '@/api'

const STEPS = [
  { key: 0, label: '输入内容', icon: '📝' },
  { key: 1, label: '提取信息', icon: '🔍' },
  { key: 2, label: '生成图片', icon: '🖼️' },
  { key: 4, label: '固定角色', icon: '👥' },
  { key: 5, label: '生成分镜', icon: '🎬' },
  { key: 6, label: '生成视频', icon: '🎥' },
]

const MODEL_TYPES = [
  { value: 1, label: '文本模型' },
  { value: 2, label: '图像模型' },
  { value: 3, label: '视频模型' },
  { value: 4, label: '语音模型' },
]

export function ProjectDetailPage() {
  const { projectId } = useParams<{ projectId: string }>()
  const navigate = useNavigate()
  const queryClient = useQueryClient()
  const [activeTab, setActiveTab] = useState<'episodes' | 'characters' | 'scenes' | 'models'>('episodes')

  const { data: project } = useQuery({
    queryKey: ['project', projectId],
    queryFn: () => projectApi.get(Number(projectId)),
    select: (res) => res.data.data,
  })

  const { data: episodes } = useQuery({
    queryKey: ['episodes', projectId],
    queryFn: () => episodeApi.list(Number(projectId)),
    select: (res) => res.data.data,
  })

  const { data: characters } = useQuery({
    queryKey: ['characters', projectId],
    queryFn: () => characterApi.list(Number(projectId)),
    select: (res) => res.data.data,
  })

  const { data: scenes } = useQuery({
    queryKey: ['scenes', projectId],
    queryFn: () => sceneApi.list(Number(projectId)),
    select: (res) => res.data.data,
  })

  const { data: modelConfig, refetch: refetchModelConfig } = useQuery<ProjectModelConfig>({
    queryKey: ['project-model-config', projectId],
    queryFn: () => projectModelApi.getConfig(Number(projectId)).then(res => res.data.data),
    enabled: activeTab === 'models',
  })

  const { data: allInstances } = useQuery({
    queryKey: ['instances'],
    queryFn: async () => {
      const res = await modelApi.listInstances()
      return res.data.data.items
    },
    enabled: activeTab === 'models',
  })

  const setModelOverrideMutation = useMutation({
    mutationFn: (data: { model_instance_id: number; model_type: number }) =>
      projectModelApi.setOverride(Number(projectId), data),
    onSuccess: () => {
      refetchModelConfig()
      toast.success('模型配置已更新')
    },
    onError: () => toast.error('更新失败'),
  })

  const deleteModelOverrideMutation = useMutation({
    mutationFn: (modelType: number) =>
      projectModelApi.deleteOverride(Number(projectId), modelType),
    onSuccess: () => {
      refetchModelConfig()
      toast.success('已恢复全局默认')
    },
    onError: () => toast.error('更新失败'),
  })

  const createEpisodeMutation = useMutation({
    mutationFn: (data: { name: string }) => episodeApi.create(Number(projectId), data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['episodes', projectId] })
      toast.success('章节创建成功')
    },
    onError: () => toast.error('章节创建失败'),
  })

  const handleCreateEpisode = () => {
    const name = prompt('请输入章节名称:')
    if (!name) return
    createEpisodeMutation.mutate({ name })
  }

  if (!project) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-pulse text-muted-foreground">加载中...</div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <Button variant="ghost" onClick={() => navigate('/projects')}>
          <ArrowLeft className="w-4 h-4 mr-2" />
          返回
        </Button>
        <div className="flex-1">
          <h1 className="text-3xl font-bold tracking-tight">{project.name}</h1>
          {project.description && (
            <p className="text-muted-foreground">{project.description}</p>
          )}
        </div>
      </div>

      {/* Progress Bar */}
      <Card>
        <CardContent className="pt-6">
          <div className="flex items-center justify-between mb-4">
            <span className="text-sm font-medium">创作进度</span>
            <span className="text-sm text-muted-foreground">{project.progress}%</span>
          </div>
          <div className="h-2 bg-gray-100 rounded-full overflow-hidden mb-4">
            <div
              className="h-full bg-primary rounded-full transition-all"
              style={{ width: `${project.progress}%` }}
            />
          </div>
          <div className="flex justify-between">
            {STEPS.map((step) => (
              <div
                key={step.key}
                className={`flex flex-col items-center text-xs ${
                  project.progress >= step.key * 15
                    ? 'text-primary'
                    : 'text-muted-foreground'
                }`}
              >
                <span>{step.icon}</span>
                <span className="mt-1">{step.label}</span>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Tabs */}
      <div className="flex gap-1 border-b">
        {[
          { key: 'episodes', label: '章节', icon: Clapperboard, count: episodes?.total || 0 },
          { key: 'characters', label: '角色', icon: Users, count: characters?.total || 0 },
          { key: 'scenes', label: '场景', icon: MapPin, count: scenes?.total || 0 },
          { key: 'models', label: '模型配置', icon: Bot, count: 0 },
        ].map((tab) => (
          <button
            key={tab.key}
            onClick={() => setActiveTab(tab.key as typeof activeTab)}
            className={`flex items-center gap-2 px-4 py-3 text-sm font-medium border-b-2 transition-colors ${
              activeTab === tab.key
                ? 'border-primary text-primary'
                : 'border-transparent text-muted-foreground hover:text-foreground'
            }`}
          >
            <tab.icon className="w-4 h-4" />
            {tab.label}
            <span className="ml-1 px-2 py-0.5 rounded-full bg-gray-100 text-xs">
              {tab.count}
            </span>
          </button>
        ))}
      </div>

      {/* Tab Content */}
      {activeTab === 'episodes' && (
        <div className="space-y-4">
          <Button onClick={handleCreateEpisode} disabled={createEpisodeMutation.isPending}>
            <Plus className="w-4 h-4 mr-2" />
            新建章节
          </Button>
          {episodes?.items.length === 0 ? (
            <Card className="py-8">
              <CardContent className="flex flex-col items-center justify-center text-center">
                <Clapperboard className="w-10 h-10 text-muted-foreground mb-3" />
                <p className="text-muted-foreground">暂无章节</p>
              </CardContent>
            </Card>
          ) : (
            <div className="grid gap-4">
              {episodes?.items.map((episode) => (
                <Card key={episode.id} className="hover:border-primary transition-colors">
                  <CardContent className="flex items-center justify-between p-4">
                    <div>
                      <h3 className="font-medium">{episode.name}</h3>
                      <p className="text-sm text-muted-foreground">
                        第{episode.chapter_number}章 · {episode.current_step === 0 ? '待开始' : episode.progress + '%'}
                      </p>
                    </div>
                    <div className="flex gap-2">
                      {episode.current_step >= 1 && (
                        <Button size="sm" variant="outline">
                          提取信息
                        </Button>
                      )}
                      {episode.current_step >= 5 && (
                        <Button size="sm">
                          <Play className="w-4 h-4 mr-1" />
                          生成视频
                        </Button>
                      )}
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          )}
        </div>
      )}

      {activeTab === 'characters' && (
        <div className="space-y-4">
          {characters?.items.length === 0 ? (
            <Card className="py-8">
              <CardContent className="flex flex-col items-center justify-center text-center">
                <Users className="w-10 h-10 text-muted-foreground mb-3" />
                <p className="text-muted-foreground">暂无角色</p>
                <p className="text-sm text-muted-foreground">在章节中提取信息后自动生成</p>
              </CardContent>
            </Card>
          ) : (
            <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4">
              {characters?.items.map((character) => (
                <Card key={character.id} className="overflow-hidden">
                  <div className="aspect-square bg-gray-100 flex items-center justify-center">
                    {character.avatar ? (
                      <img src={character.avatar} alt={character.name} className="w-full h-full object-cover" />
                    ) : (
                      <span className="text-3xl font-bold text-gray-300">
                        {character.name.charAt(0)}
                      </span>
                    )}
                  </div>
                  <CardContent className="p-3">
                    <p className="font-medium text-sm truncate">{character.name}</p>
                  </CardContent>
                </Card>
              ))}
            </div>
          )}
        </div>
      )}

      {activeTab === 'scenes' && (
        <div className="space-y-4">
          {scenes?.items.length === 0 ? (
            <Card className="py-8">
              <CardContent className="flex flex-col items-center justify-center text-center">
                <MapPin className="w-10 h-10 text-muted-foreground mb-3" />
                <p className="text-muted-foreground">暂无场景</p>
                <p className="text-sm text-muted-foreground">在章节中提取信息后自动生成</p>
              </CardContent>
            </Card>
          ) : (
            <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4">
              {scenes?.items.map((scene) => (
                <Card key={scene.id} className="overflow-hidden">
                  <div className="aspect-video bg-gray-100 flex items-center justify-center">
                    {scene.thumbnail ? (
                      <img src={scene.thumbnail} alt={scene.name} className="w-full h-full object-cover" />
                    ) : (
                      <MapPin className="w-8 h-8 text-gray-300" />
                    )}
                  </div>
                  <CardContent className="p-3">
                    <p className="font-medium text-sm truncate">{scene.name}</p>
                  </CardContent>
                </Card>
              ))}
            </div>
          )}
        </div>
      )}

      {activeTab === 'models' && (
        <div className="space-y-4">
          <Card>
            <CardContent className="pt-6">
              <p className="text-sm text-muted-foreground mb-4">
                设置本项目使用的模型。默认使用全局配置，您也可以为项目单独配置。
              </p>
              <div className="space-y-4">
                {MODEL_TYPES.map((type) => {
                  const overrideId = modelConfig?.overrides?.[type.value]
                  const defaultInfo = modelConfig?.defaults?.[type.value]
                  const instances = allInstances?.filter((i: any) => i.model_type === type.value) || []

                  return (
                    <div key={type.value} className="flex items-center justify-between p-4 border rounded-lg">
                      <div>
                        <p className="font-medium">{type.label}</p>
                        {overrideId ? (
                          <p className="text-sm text-muted-foreground">
                            当前: {instances.find((i: any) => i.id === overrideId)?.instance_name || 'Unknown'}
                          </p>
                        ) : defaultInfo ? (
                          <p className="text-sm text-muted-foreground flex items-center gap-1">
                            <Star className="w-3 h-3 text-yellow-500" />
                            全局默认: {defaultInfo.instance_name}
                          </p>
                        ) : (
                          <p className="text-sm text-muted-foreground">未配置</p>
                        )}
                      </div>
                      <div className="flex items-center gap-2">
                        <select
                          className="p-2 border rounded-md text-sm"
                          value={overrideId || ''}
                          onChange={(e) => {
                            const val = e.target.value
                            if (val) {
                              setModelOverrideMutation.mutate({ model_instance_id: Number(val), model_type: type.value })
                            }
                          }}
                        >
                          <option value="">使用全局默认</option>
                          {instances.map((inst: any) => (
                            <option key={inst.id} value={inst.id}>{inst.instance_name}</option>
                          ))}
                        </select>
                        {overrideId && (
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => deleteModelOverrideMutation.mutate(type.value)}
                          >
                            恢复默认
                          </Button>
                        )}
                      </div>
                    </div>
                  )
                })}
              </div>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  )
}
