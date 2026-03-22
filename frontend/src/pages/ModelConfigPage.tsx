import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { Bot, Key, Settings, Plus, Trash2, Star } from 'lucide-react'
import toast from 'react-hot-toast'

import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { providerApi, modelApi, ModelProvider, ModelInstance } from '@/api'

const MODEL_TYPES = [
  { value: 1, label: '文本模型' },
  { value: 2, label: '图像模型' },
  { value: 3, label: '视频模型' },
  { value: 4, label: '语音模型' },
]

const PROVIDER_TYPES = [
  { value: 'openai', label: 'OpenAI' },
  { value: 'minimax', label: 'MiniMax' },
  { value: 'claude', label: 'Claude' },
  { value: 'custom', label: '自定义' },
]

export function ModelConfigPage() {
  const queryClient = useQueryClient()
  const [activeType, setActiveType] = useState(1)
  const [showProviderForm, setShowProviderForm] = useState(false)
  const [showInstanceForm, setShowInstanceForm] = useState(false)
  const [editingProvider, setEditingProvider] = useState<ModelProvider | null>(null)
  const [editingInstance, setEditingInstance] = useState<ModelInstance | null>(null)

  // Provider form state
  const [providerForm, setProviderForm] = useState({
    name: '',
    provider_type: 'openai',
    api_base: '',
    api_key: '',
  })

  // Instance form state
  const [instanceForm, setInstanceForm] = useState({
    model_code: '',
    model_type: 1,
    instance_name: '',
    provider_id: undefined as number | undefined,
    api_key: '',
    params: {} as Record<string, any>,
  })

  // Queries
  const { data: providers, isLoading: providersLoading } = useQuery({
    queryKey: ['providers'],
    queryFn: async () => {
      const res = await providerApi.list()
      return res.data.data
    },
  })

  const { data: instances, isLoading: instancesLoading } = useQuery({
    queryKey: ['instances', activeType],
    queryFn: async () => {
      const res = await modelApi.listInstances({ model_type: activeType })
      return res.data.data.items
    },
  })

  // Provider mutations
  const createProviderMutation = useMutation({
    mutationFn: (data: typeof providerForm) => providerApi.create(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['providers'] })
      toast.success('Provider created')
      setShowProviderForm(false)
      setProviderForm({ name: '', provider_type: 'openai', api_base: '', api_key: '' })
    },
    onError: () => toast.error('Failed to create provider'),
  })

  const updateProviderMutation = useMutation({
    mutationFn: ({ id, data }: { id: number; data: Partial<typeof providerForm> }) =>
      providerApi.update(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['providers'] })
      toast.success('Provider updated')
      setEditingProvider(null)
    },
    onError: () => toast.error('Failed to update provider'),
  })

  const deleteProviderMutation = useMutation({
    mutationFn: (id: number) => providerApi.delete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['providers'] })
      toast.success('Provider deleted')
    },
    onError: () => toast.error('Failed to delete provider'),
  })

  // Instance mutations
  const createInstanceMutation = useMutation({
    mutationFn: (data: typeof instanceForm) => modelApi.createInstance(data as any),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['instances'] })
      toast.success('Instance created')
      setShowInstanceForm(false)
      setInstanceForm({ model_code: '', model_type: activeType, instance_name: '', provider_id: undefined, api_key: '', params: {} })
    },
    onError: () => toast.error('Failed to create instance'),
  })

  const updateInstanceMutation = useMutation({
    mutationFn: ({ id, data }: { id: number; data: Partial<typeof instanceForm> }) =>
      modelApi.updateInstance(id, data as any),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['instances'] })
      toast.success('Instance updated')
      setEditingInstance(null)
    },
    onError: () => toast.error('Failed to update instance'),
  })

  const deleteInstanceMutation = useMutation({
    mutationFn: (id: number) => modelApi.deleteInstance(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['instances'] })
      toast.success('Instance deleted')
    },
    onError: () => toast.error('Failed to delete instance'),
  })

  const setDefaultMutation = useMutation({
    mutationFn: ({ id, modelType }: { id: number; modelType: number }) =>
      modelApi.setDefault(id, modelType),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['instances'] })
      toast.success('Default model set')
    },
    onError: () => toast.error('Failed to set default'),
  })

  const handleProviderSubmit = () => {
    if (editingProvider) {
      updateProviderMutation.mutate({ id: editingProvider.id, data: providerForm })
    } else {
      createProviderMutation.mutate(providerForm)
    }
  }

  const handleInstanceSubmit = () => {
    if (editingInstance) {
      updateInstanceMutation.mutate({ id: editingInstance.id, data: instanceForm })
    } else {
      createInstanceMutation.mutate(instanceForm)
    }
  }

  const getProviderName = (providerId: number | undefined) => {
    if (!providerId) return 'N/A'
    const provider = providers?.find((p: ModelProvider) => p.id === providerId)
    return provider?.name || 'Unknown'
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">模型配置</h1>
        <p className="text-muted-foreground">管理AI模型服务商和实例配置</p>
      </div>

      {/* Provider Management */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle>模型服务商</CardTitle>
              <CardDescription>添加和管理AI模型服务商（如OpenAI、MiniMax）</CardDescription>
            </div>
            <Button onClick={() => { setEditingProvider(null); setShowProviderForm(true) }}>
              <Plus className="w-4 h-4 mr-2" />
              添加服务商
            </Button>
          </div>
        </CardHeader>
        <CardContent>
          {providersLoading ? (
            <div className="text-center py-4 text-muted-foreground">Loading...</div>
          ) : providers?.length === 0 ? (
            <div className="text-center py-4 text-muted-foreground">暂无服务商配置</div>
          ) : (
            <div className="space-y-4">
              {providers?.map((provider: ModelProvider) => (
                <div key={provider.id} className="flex items-center justify-between p-4 border rounded-lg">
                  <div className="flex items-center gap-4">
                    <div className="w-10 h-10 rounded-full bg-primary/10 flex items-center justify-center">
                      <Bot className="w-5 h-5 text-primary" />
                    </div>
                    <div>
                      <p className="font-medium">{provider.name}</p>
                      <p className="text-sm text-muted-foreground">
                        {PROVIDER_TYPES.find(t => t.value === provider.provider_type)?.label} · {provider.api_base || 'No API Base'}
                      </p>
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className={`px-2 py-1 text-xs rounded-full ${provider.status === 1 ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-700'}`}>
                      {provider.status === 1 ? '启用' : '禁用'}
                    </span>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => {
                        setEditingProvider(provider)
                        setProviderForm({
                          name: provider.name,
                          provider_type: provider.provider_type,
                          api_base: provider.api_base || '',
                          api_key: provider.api_key || '',
                        })
                        setShowProviderForm(true)
                      }}
                    >
                      <Settings className="w-4 h-4" />
                    </Button>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => deleteProviderMutation.mutate(provider.id)}
                    >
                      <Trash2 className="w-4 h-4 text-red-500" />
                    </Button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>

      {/* Model Type Tabs */}
      <div className="grid grid-cols-4 gap-4">
        {MODEL_TYPES.map((type) => (
          <Card
            key={type.value}
            className={`cursor-pointer transition-colors ${activeType === type.value ? 'border-primary' : ''}`}
            onClick={() => setActiveType(type.value)}
          >
            <CardContent className="p-4 text-center">
              <Bot className={`w-8 h-8 mx-auto mb-2 ${activeType === type.value ? 'text-primary' : 'text-gray-400'}`} />
              <p className={`font-medium ${activeType === type.value ? 'text-primary' : ''}`}>
                {type.label}
              </p>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Instance Management */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle>模型实例</CardTitle>
              <CardDescription>
                {MODEL_TYPES.find((t) => t.value === activeType)?.label}实例列表
              </CardDescription>
            </div>
            <Button onClick={() => { setEditingInstance(null); setShowInstanceForm(true); setInstanceForm(f => ({ ...f, model_type: activeType })) }}>
              <Plus className="w-4 h-4 mr-2" />
              添加实例
            </Button>
          </div>
        </CardHeader>
        <CardContent>
          {instancesLoading ? (
            <div className="text-center py-4 text-muted-foreground">Loading...</div>
          ) : instances?.length === 0 ? (
            <div className="text-center py-4 text-muted-foreground">暂无实例配置</div>
          ) : (
            <div className="space-y-4">
              {instances?.map((instance: ModelInstance) => (
                <div key={instance.id} className="flex items-center justify-between p-4 border rounded-lg">
                  <div className="flex items-center gap-4">
                    <div className="w-10 h-10 rounded-full bg-primary/10 flex items-center justify-center">
                      <Key className="w-5 h-5 text-primary" />
                    </div>
                    <div>
                      <p className="font-medium flex items-center gap-2">
                        {instance.instance_name}
                        {instance.is_default && (
                          <Star className="w-4 h-4 text-yellow-500 fill-yellow-500" />
                        )}
                      </p>
                      <p className="text-sm text-muted-foreground">
                        {getProviderName(instance.provider_id)} · {instance.model_code}
                      </p>
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    {instance.is_default ? (
                      <span className="px-2 py-1 text-xs rounded-full bg-yellow-100 text-yellow-700">
                        默认
                      </span>
                    ) : (
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => setDefaultMutation.mutate({ id: instance.id, modelType: instance.model_type })}
                      >
                        <Star className="w-4 h-4 mr-1" />
                        设为默认
                      </Button>
                    )}
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => {
                        setEditingInstance(instance)
                        setInstanceForm({
                          model_code: instance.model_code,
                          model_type: instance.model_type,
                          instance_name: instance.instance_name,
                          provider_id: instance.provider_id,
                          api_key: instance.api_key || '',
                          params: instance.params || {},
                        })
                        setShowInstanceForm(true)
                      }}
                    >
                      <Settings className="w-4 h-4" />
                    </Button>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => deleteInstanceMutation.mutate(instance.id)}
                    >
                      <Trash2 className="w-4 h-4 text-red-500" />
                    </Button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>

      {/* Provider Form Modal */}
      {showProviderForm && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <Card className="w-full max-w-md">
            <CardHeader>
              <CardTitle>{editingProvider ? '编辑服务商' : '添加服务商'}</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <label className="text-sm font-medium mb-2 block">名称</label>
                <Input
                  value={providerForm.name}
                  onChange={(e) => setProviderForm({ ...providerForm, name: e.target.value })}
                  placeholder="如: MiniMax官方"
                />
              </div>
              <div>
                <label className="text-sm font-medium mb-2 block">类型</label>
                <select
                  className="w-full p-2 border rounded-md"
                  value={providerForm.provider_type}
                  onChange={(e) => setProviderForm({ ...providerForm, provider_type: e.target.value })}
                >
                  {PROVIDER_TYPES.map((type) => (
                    <option key={type.value} value={type.value}>{type.label}</option>
                  ))}
                </select>
              </div>
              <div>
                <label className="text-sm font-medium mb-2 block">API Base URL</label>
                <Input
                  value={providerForm.api_base}
                  onChange={(e) => setProviderForm({ ...providerForm, api_base: e.target.value })}
                  placeholder="如: https://api.minimax.chat/v1"
                />
              </div>
              <div>
                <label className="text-sm font-medium mb-2 block">API Key</label>
                <Input
                  type="password"
                  value={providerForm.api_key}
                  onChange={(e) => setProviderForm({ ...providerForm, api_key: e.target.value })}
                  placeholder="sk-..."
                />
              </div>
              <div className="flex gap-2 justify-end">
                <Button variant="outline" onClick={() => setShowProviderForm(false)}>取消</Button>
                <Button onClick={handleProviderSubmit} disabled={createProviderMutation.isPending || updateProviderMutation.isPending}>
                  {editingProvider ? '更新' : '创建'}
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Instance Form Modal */}
      {showInstanceForm && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <Card className="w-full max-w-md">
            <CardHeader>
              <CardTitle>{editingInstance ? '编辑实例' : '添加实例'}</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <label className="text-sm font-medium mb-2 block">实例名称</label>
                <Input
                  value={instanceForm.instance_name}
                  onChange={(e) => setInstanceForm({ ...instanceForm, instance_name: e.target.value })}
                  placeholder="如: MiniMax-Text-01"
                />
              </div>
              <div>
                <label className="text-sm font-medium mb-2 block">模型代码</label>
                <Input
                  value={instanceForm.model_code}
                  onChange={(e) => setInstanceForm({ ...instanceForm, model_code: e.target.value })}
                  placeholder="如: MiniMax-Text-01"
                />
              </div>
              <div>
                <label className="text-sm font-medium mb-2 block">服务商</label>
                <select
                  className="w-full p-2 border rounded-md"
                  value={instanceForm.provider_id || ''}
                  onChange={(e) => setInstanceForm({ ...instanceForm, provider_id: e.target.value ? Number(e.target.value) : undefined })}
                >
                  <option value="">选择服务商</option>
                  {providers?.map((p: ModelProvider) => (
                    <option key={p.id} value={p.id}>{p.name}</option>
                  ))}
                </select>
              </div>
              <div>
                <label className="text-sm font-medium mb-2 block">API Key (可选)</label>
                <Input
                  type="password"
                  value={instanceForm.api_key}
                  onChange={(e) => setInstanceForm({ ...instanceForm, api_key: e.target.value })}
                  placeholder="sk-... (覆盖服务商配置)"
                />
              </div>
              <div className="flex gap-2 justify-end">
                <Button variant="outline" onClick={() => setShowInstanceForm(false)}>取消</Button>
                <Button onClick={handleInstanceSubmit} disabled={createInstanceMutation.isPending || updateInstanceMutation.isPending}>
                  {editingInstance ? '更新' : '创建'}
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  )
}
