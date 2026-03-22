import { useState } from 'react'
import { Bot, Key, Settings } from 'lucide-react'

import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'

const MODEL_TYPES = [
  { value: 1, label: '文本模型' },
  { value: 2, label: '图像模型' },
  { value: 3, label: '视频模型' },
  { value: 4, label: '语音模型' },
]

export function ModelConfigPage() {
  const [activeType, setActiveType] = useState(1)

  // Mock data - in real app would call model API
  const mockInstances = [
    { id: 1, instance_name: 'GPT-4o', model_code: 'gpt-4o', provider: 'OpenAI', status: 1 },
    { id: 2, instance_name: 'Claude-3', model_code: 'claude-3-opus', provider: 'Anthropic', status: 1 },
  ]

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">模型配置</h1>
        <p className="text-muted-foreground">管理AI模型服务商和实例配置</p>
      </div>

      <div className="grid grid-cols-4 gap-4">
        {MODEL_TYPES.map((type) => (
          <Card
            key={type.value}
            className={`cursor-pointer transition-colors ${
              activeType === type.value ? 'border-primary' : ''
            }`}
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

      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle>模型实例</CardTitle>
              <CardDescription>
                {MODEL_TYPES.find((t) => t.value === activeType)?.label}实例列表
              </CardDescription>
            </div>
            <Button>添加实例</Button>
          </div>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {mockInstances.map((instance) => (
              <div
                key={instance.id}
                className="flex items-center justify-between p-4 border rounded-lg"
              >
                <div className="flex items-center gap-4">
                  <div className="w-10 h-10 rounded-full bg-primary/10 flex items-center justify-center">
                    <Key className="w-5 h-5 text-primary" />
                  </div>
                  <div>
                    <p className="font-medium">{instance.instance_name}</p>
                    <p className="text-sm text-muted-foreground">
                      {instance.provider} · {instance.model_code}
                    </p>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <span className="px-2 py-1 text-xs rounded-full bg-green-100 text-green-700">
                    启用
                  </span>
                  <Button variant="ghost" size="sm">
                    <Settings className="w-4 h-4" />
                  </Button>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>API Key 配置</CardTitle>
          <CardDescription>配置模型服务商的API密钥</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <label className="text-sm font-medium mb-2 block">OpenAI API Key</label>
            <Input type="password" placeholder="sk-..." />
          </div>
          <div>
            <label className="text-sm font-medium mb-2 block">Anthropic API Key</label>
            <Input type="password" placeholder="sk-ant-..." />
          </div>
          <Button>保存配置</Button>
        </CardContent>
      </Card>
    </div>
  )
}
