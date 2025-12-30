import { useState } from 'react';
import { motion } from 'framer-motion';
import {
  Zap,
  Settings,
  Activity,
  Shield,
  TrendingUp,
  Clock,
  DollarSign,
  AlertTriangle,
  CheckCircle2,
  XCircle,
  RefreshCw,
  Save,
  TestTube
} from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import {
  Tabs,
  TabsContent,
  TabsList,
  TabsTrigger,
} from '@/components/ui/tabs';

export default function LLMGatewayPage() {
  const [activeTab, setActiveTab] = useState('overview');

  // Mock data - จะเชื่อมกับ API ในภายหลัง
  const providers = [
    {
      name: 'OpenAI',
      status: 'active',
      latency: 245,
      uptime: 99.9,
      cost: 0.002,
      models: ['gpt-4', 'gpt-3.5-turbo'],
    },
    {
      name: 'Anthropic',
      status: 'active',
      latency: 312,
      uptime: 99.8,
      cost: 0.003,
      models: ['claude-3-opus', 'claude-3-sonnet'],
    },
    {
      name: 'Google AI',
      status: 'active',
      latency: 198,
      uptime: 99.7,
      cost: 0.001,
      models: ['gemini-pro', 'gemini-ultra'],
    },
    {
      name: 'Groq',
      status: 'warning',
      latency: 89,
      uptime: 98.5,
      cost: 0.0005,
      models: ['mixtral-8x7b', 'llama2-70b'],
    },
    {
      name: 'OpenRouter',
      status: 'active',
      latency: 156,
      uptime: 99.5,
      cost: 0.0015,
      models: ['multiple'],
    },
  ];

  const tiers = [
    {
      name: 'Basic',
      description: 'For general chat and simple tasks',
      providers: ['OpenRouter', 'Groq', 'Google AI'],
      loadBalancing: 'round-robin',
      failover: true,
    },
    {
      name: 'General',
      description: 'For standard tasks',
      providers: ['OpenAI', 'Google AI', 'Anthropic'],
      loadBalancing: 'weighted',
      failover: true,
    },
    {
      name: 'Advanced',
      description: 'For complex tasks like code generation',
      providers: ['OpenAI', 'Anthropic', 'Google AI'],
      loadBalancing: 'least-latency',
      failover: true,
    },
  ];

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active':
        return 'text-green-500';
      case 'warning':
        return 'text-orange-500';
      case 'error':
        return 'text-red-500';
      default:
        return 'text-gray-500';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'active':
        return <CheckCircle2 className="h-5 w-5" />;
      case 'warning':
        return <AlertTriangle className="h-5 w-5" />;
      case 'error':
        return <XCircle className="h-5 w-5" />;
      default:
        return <Activity className="h-5 w-5" />;
    }
  };

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">LLM Gateway</h1>
          <p className="text-muted-foreground mt-1">
            Configure load balancing, failover, and provider settings
          </p>
        </div>
        <div className="flex items-center space-x-2">
          <Button variant="outline" className="rounded-full">
            <TestTube className="mr-2 h-4 w-4" />
            Test Configuration
          </Button>
          <Button className="rounded-full">
            <Save className="mr-2 h-4 w-4" />
            Save Changes
          </Button>
        </div>
      </div>

      {/* Tabs */}
      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList className="grid w-full grid-cols-4 rounded-xl">
          <TabsTrigger value="overview" className="rounded-lg">
            <Activity className="mr-2 h-4 w-4" />
            Overview
          </TabsTrigger>
          <TabsTrigger value="tiers" className="rounded-lg">
            <Zap className="mr-2 h-4 w-4" />
            Tiers
          </TabsTrigger>
          <TabsTrigger value="load-balancing" className="rounded-lg">
            <RefreshCw className="mr-2 h-4 w-4" />
            Load Balancing
          </TabsTrigger>
          <TabsTrigger value="failover" className="rounded-lg">
            <Shield className="mr-2 h-4 w-4" />
            Failover
          </TabsTrigger>
        </TabsList>

        {/* Overview Tab */}
        <TabsContent value="overview" className="space-y-6">
          {/* Provider Status Grid */}
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {providers.map((provider, index) => (
              <motion.div
                key={provider.name}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
              >
                <Card className="backdrop-blur-xl bg-card/50 border-border/50 hover:border-primary/50 transition-all rounded-2xl">
                  <CardContent className="p-6">
                    <div className="flex items-center justify-between mb-4">
                      <h3 className="font-semibold text-lg">{provider.name}</h3>
                      <div className={getStatusColor(provider.status)}>
                        {getStatusIcon(provider.status)}
                      </div>
                    </div>
                    
                    <div className="space-y-3">
                      <div className="flex items-center justify-between text-sm">
                        <span className="text-muted-foreground flex items-center">
                          <Clock className="h-4 w-4 mr-1" />
                          Latency
                        </span>
                        <span className="font-medium">{provider.latency}ms</span>
                      </div>
                      
                      <div className="flex items-center justify-between text-sm">
                        <span className="text-muted-foreground flex items-center">
                          <TrendingUp className="h-4 w-4 mr-1" />
                          Uptime
                        </span>
                        <span className="font-medium">{provider.uptime}%</span>
                      </div>
                      
                      <div className="flex items-center justify-between text-sm">
                        <span className="text-muted-foreground flex items-center">
                          <DollarSign className="h-4 w-4 mr-1" />
                          Cost/1K tokens
                        </span>
                        <span className="font-medium">${provider.cost}</span>
                      </div>
                    </div>
                    
                    <div className="mt-4 pt-4 border-t border-border/50">
                      <p className="text-xs text-muted-foreground mb-2">Models:</p>
                      <div className="flex flex-wrap gap-1">
                        {provider.models.map((model) => (
                          <span
                            key={model}
                            className="px-2 py-1 text-xs bg-primary/10 text-primary rounded-md"
                          >
                            {model}
                          </span>
                        ))}
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </motion.div>
            ))}
          </div>
        </TabsContent>

        {/* Tiers Tab */}
        <TabsContent value="tiers" className="space-y-6">
          <Card className="backdrop-blur-xl bg-card/50 border-border/50 rounded-2xl">
            <CardHeader>
              <CardTitle>Multi-Tier Strategy</CardTitle>
              <CardDescription>
                Configure provider priorities for different task complexities
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              {tiers.map((tier, index) => (
                <motion.div
                  key={tier.name}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.1 }}
                  className="p-6 rounded-xl border border-border/50 hover:border-primary/50 transition-all"
                >
                  <div className="flex items-start justify-between mb-4">
                    <div>
                      <h3 className="font-semibold text-lg">{tier.name} Tier</h3>
                      <p className="text-sm text-muted-foreground mt-1">
                        {tier.description}
                      </p>
                    </div>
                    <Button variant="outline" size="sm" className="rounded-lg">
                      <Settings className="h-4 w-4" />
                    </Button>
                  </div>

                  <div className="space-y-4">
                    <div>
                      <Label className="text-sm font-medium mb-2 block">
                        Provider Priority (Top 3)
                      </Label>
                      <div className="space-y-2">
                        {tier.providers.map((provider, i) => (
                          <div
                            key={provider}
                            className="flex items-center justify-between p-3 rounded-lg bg-muted/30"
                          >
                            <div className="flex items-center space-x-3">
                              <span className="flex items-center justify-center w-6 h-6 rounded-full bg-primary/20 text-primary text-sm font-medium">
                                {i + 1}
                              </span>
                              <span className="font-medium">{provider}</span>
                            </div>
                            <Button variant="ghost" size="sm">
                              Change
                            </Button>
                          </div>
                        ))}
                      </div>
                    </div>

                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <Label className="text-sm font-medium mb-2 block">
                          Load Balancing
                        </Label>
                        <Select defaultValue={tier.loadBalancing}>
                          <SelectTrigger className="rounded-lg">
                            <SelectValue />
                          </SelectTrigger>
                          <SelectContent>
                            <SelectItem value="round-robin">Round Robin</SelectItem>
                            <SelectItem value="weighted">Weighted</SelectItem>
                            <SelectItem value="least-latency">Least Latency</SelectItem>
                            <SelectItem value="random">Random</SelectItem>
                          </SelectContent>
                        </Select>
                      </div>

                      <div>
                        <Label className="text-sm font-medium mb-2 block">
                          Automatic Failover
                        </Label>
                        <Select defaultValue={tier.failover ? 'enabled' : 'disabled'}>
                          <SelectTrigger className="rounded-lg">
                            <SelectValue />
                          </SelectTrigger>
                          <SelectContent>
                            <SelectItem value="enabled">Enabled</SelectItem>
                            <SelectItem value="disabled">Disabled</SelectItem>
                          </SelectContent>
                        </Select>
                      </div>
                    </div>
                  </div>
                </motion.div>
              ))}
            </CardContent>
          </Card>
        </TabsContent>

        {/* Load Balancing Tab */}
        <TabsContent value="load-balancing" className="space-y-6">
          <Card className="backdrop-blur-xl bg-card/50 border-border/50 rounded-2xl">
            <CardHeader>
              <CardTitle>Load Balancing Configuration</CardTitle>
              <CardDescription>
                Configure how requests are distributed across providers
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="space-y-4">
                <div>
                  <Label className="text-sm font-medium mb-2 block">
                    Global Load Balancing Strategy
                  </Label>
                  <Select defaultValue="weighted">
                    <SelectTrigger className="rounded-lg">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="round-robin">
                        <div className="flex flex-col">
                          <span className="font-medium">Round Robin</span>
                          <span className="text-xs text-muted-foreground">
                            Distribute requests evenly
                          </span>
                        </div>
                      </SelectItem>
                      <SelectItem value="weighted">
                        <div className="flex flex-col">
                          <span className="font-medium">Weighted</span>
                          <span className="text-xs text-muted-foreground">
                            Based on provider performance
                          </span>
                        </div>
                      </SelectItem>
                      <SelectItem value="least-latency">
                        <div className="flex flex-col">
                          <span className="font-medium">Least Latency</span>
                          <span className="text-xs text-muted-foreground">
                            Route to fastest provider
                          </span>
                        </div>
                      </SelectItem>
                      <SelectItem value="cost-optimized">
                        <div className="flex flex-col">
                          <span className="font-medium">Cost Optimized</span>
                          <span className="text-xs text-muted-foreground">
                            Route to cheapest provider
                          </span>
                        </div>
                      </SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <Label className="text-sm font-medium mb-2 block">
                      Max Concurrent Requests
                    </Label>
                    <Input
                      type="number"
                      defaultValue="100"
                      className="rounded-lg"
                    />
                  </div>

                  <div>
                    <Label className="text-sm font-medium mb-2 block">
                      Request Timeout (seconds)
                    </Label>
                    <Input
                      type="number"
                      defaultValue="30"
                      className="rounded-lg"
                    />
                  </div>
                </div>

                <div>
                  <Label className="text-sm font-medium mb-2 block">
                    Provider Weights
                  </Label>
                  <div className="space-y-3">
                    {providers.slice(0, 3).map((provider) => (
                      <div key={provider.name} className="flex items-center space-x-4">
                        <span className="w-32 text-sm font-medium">{provider.name}</span>
                        <Input
                          type="range"
                          min="0"
                          max="100"
                          defaultValue="50"
                          className="flex-1"
                        />
                        <span className="w-12 text-sm text-muted-foreground">50%</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Failover Tab */}
        <TabsContent value="failover" className="space-y-6">
          <Card className="backdrop-blur-xl bg-card/50 border-border/50 rounded-2xl">
            <CardHeader>
              <CardTitle>Automatic Failover Configuration</CardTitle>
              <CardDescription>
                Configure fallback chains when providers fail
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="space-y-4">
                <div className="flex items-center justify-between p-4 rounded-lg bg-green-500/10 border border-green-500/20">
                  <div className="flex items-center space-x-3">
                    <Shield className="h-5 w-5 text-green-500" />
                    <div>
                      <p className="font-medium">Automatic Failover Enabled</p>
                      <p className="text-sm text-muted-foreground">
                        Requests will automatically retry with fallback providers
                      </p>
                    </div>
                  </div>
                  <Button variant="outline" size="sm" className="rounded-lg">
                    Disable
                  </Button>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <Label className="text-sm font-medium mb-2 block">
                      Max Retry Attempts
                    </Label>
                    <Input
                      type="number"
                      defaultValue="3"
                      className="rounded-lg"
                    />
                  </div>

                  <div>
                    <Label className="text-sm font-medium mb-2 block">
                      Retry Delay (seconds)
                    </Label>
                    <Input
                      type="number"
                      defaultValue="2"
                      className="rounded-lg"
                    />
                  </div>
                </div>

                <div>
                  <Label className="text-sm font-medium mb-3 block">
                    Failover Chain (Drag to reorder)
                  </Label>
                  <div className="space-y-2">
                    {providers.map((provider, index) => (
                      <div
                        key={provider.name}
                        className="flex items-center justify-between p-4 rounded-lg border border-border/50 hover:border-primary/50 transition-all cursor-move"
                      >
                        <div className="flex items-center space-x-3">
                          <span className="flex items-center justify-center w-8 h-8 rounded-full bg-primary/20 text-primary font-medium">
                            {index + 1}
                          </span>
                          <div>
                            <p className="font-medium">{provider.name}</p>
                            <p className="text-xs text-muted-foreground">
                              {provider.latency}ms latency • {provider.uptime}% uptime
                            </p>
                          </div>
                        </div>
                        <div className={getStatusColor(provider.status)}>
                          {getStatusIcon(provider.status)}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                <div>
                  <Label className="text-sm font-medium mb-2 block">
                    Failure Detection
                  </Label>
                  <div className="space-y-2">
                    <div className="flex items-center space-x-2">
                      <input type="checkbox" id="timeout" defaultChecked className="rounded" />
                      <label htmlFor="timeout" className="text-sm">
                        Timeout (30s)
                      </label>
                    </div>
                    <div className="flex items-center space-x-2">
                      <input type="checkbox" id="error-rate" defaultChecked className="rounded" />
                      <label htmlFor="error-rate" className="text-sm">
                        High error rate (&gt;5%)
                      </label>
                    </div>
                    <div className="flex items-center space-x-2">
                      <input type="checkbox" id="latency" defaultChecked className="rounded" />
                      <label htmlFor="latency" className="text-sm">
                        High latency (&gt;5s)
                      </label>
                    </div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}
