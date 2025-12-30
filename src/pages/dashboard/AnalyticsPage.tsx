import { useState } from 'react';
import { motion } from 'framer-motion';
import {
  TrendingUp,
  TrendingDown,
  Activity,
  DollarSign,
  Zap,
  Clock,
  Download,
  Calendar,
  BarChart3,
  PieChart as PieChartIcon,
  LineChart as LineChartIcon
} from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import {
  AreaChart,
  Area,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';

export default function AnalyticsPage() {
  const [timeRange, setTimeRange] = useState('7d');

  // Mock data - จะเชื่อมกับ API ในภายหลัง
  const usageData = [
    { date: 'Jan 1', calls: 120, cost: 2.4, tokens: 45000 },
    { date: 'Jan 2', calls: 150, cost: 3.1, tokens: 58000 },
    { date: 'Jan 3', calls: 180, cost: 3.8, tokens: 72000 },
    { date: 'Jan 4', calls: 140, cost: 2.9, tokens: 53000 },
    { date: 'Jan 5', calls: 200, cost: 4.2, tokens: 85000 },
    { date: 'Jan 6', calls: 170, cost: 3.5, tokens: 68000 },
    { date: 'Jan 7', calls: 190, cost: 4.0, tokens: 78000 },
  ];

  const providerData = [
    { name: 'OpenAI', value: 45, cost: 12.5, color: '#10b981' },
    { name: 'Anthropic', value: 30, cost: 9.8, color: '#3b82f6' },
    { name: 'Google AI', value: 15, cost: 3.2, color: '#f59e0b' },
    { name: 'Groq', value: 7, cost: 0.8, color: '#8b5cf6' },
    { name: 'OpenRouter', value: 3, cost: 0.5, color: '#ec4899' },
  ];

  const modelData = [
    { model: 'gpt-4', calls: 450, cost: 15.2, avgLatency: 2.3 },
    { model: 'gpt-3.5-turbo', calls: 320, cost: 3.8, avgLatency: 0.8 },
    { model: 'claude-3-opus', calls: 280, cost: 11.5, avgLatency: 2.1 },
    { model: 'claude-3-sonnet', calls: 150, cost: 4.2, avgLatency: 1.5 },
    { model: 'gemini-pro', calls: 180, cost: 2.8, avgLatency: 1.2 },
  ];

  const tierData = [
    { tier: 'Basic', calls: 250, cost: 2.5 },
    { tier: 'General', calls: 580, cost: 15.8 },
    { tier: 'Advanced', calls: 320, cost: 19.5 },
  ];

  const stats = {
    totalCalls: 1150,
    totalCost: 37.8,
    avgLatency: 1.6,
    successRate: 99.2,
    totalTokens: 459000,
    avgCostPerCall: 0.033,
  };

  const trends = {
    calls: { value: 12.5, isPositive: true },
    cost: { value: 8.3, isPositive: false },
    latency: { value: 5.2, isPositive: false },
    successRate: { value: 0.8, isPositive: true },
  };

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Usage Analytics</h1>
          <p className="text-muted-foreground mt-1">
            Monitor your LLM Gateway performance and costs
          </p>
        </div>
        <div className="flex items-center space-x-2">
          <Select value={timeRange} onValueChange={setTimeRange}>
            <SelectTrigger className="w-[180px] rounded-full">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="24h">Last 24 Hours</SelectItem>
              <SelectItem value="7d">Last 7 Days</SelectItem>
              <SelectItem value="30d">Last 30 Days</SelectItem>
              <SelectItem value="90d">Last 90 Days</SelectItem>
            </SelectContent>
          </Select>
          <Button variant="outline" className="rounded-full">
            <Download className="mr-2 h-4 w-4" />
            Export Report
          </Button>
        </div>
      </div>

      {/* Key Metrics */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {[
          {
            title: 'Total API Calls',
            value: stats.totalCalls.toLocaleString(),
            icon: Activity,
            trend: trends.calls,
            color: 'text-blue-500',
            bgColor: 'bg-blue-500/10',
          },
          {
            title: 'Total Cost',
            value: `$${stats.totalCost.toFixed(2)}`,
            icon: DollarSign,
            trend: trends.cost,
            color: 'text-green-500',
            bgColor: 'bg-green-500/10',
          },
          {
            title: 'Avg Latency',
            value: `${stats.avgLatency}s`,
            icon: Clock,
            trend: trends.latency,
            color: 'text-orange-500',
            bgColor: 'bg-orange-500/10',
          },
          {
            title: 'Success Rate',
            value: `${stats.successRate}%`,
            icon: Zap,
            trend: trends.successRate,
            color: 'text-purple-500',
            bgColor: 'bg-purple-500/10',
          },
        ].map((metric, index) => (
          <motion.div
            key={metric.title}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
          >
            <Card className="backdrop-blur-xl bg-card/50 border-border/50 hover:border-primary/50 transition-all rounded-2xl">
              <CardContent className="p-6">
                <div className="flex items-center justify-between mb-4">
                  <div className={`${metric.bgColor} p-3 rounded-xl`}>
                    <metric.icon className={`h-6 w-6 ${metric.color}`} />
                  </div>
                  <div className={`flex items-center space-x-1 text-sm ${
                    metric.trend.isPositive ? 'text-green-500' : 'text-red-500'
                  }`}>
                    {metric.trend.isPositive ? (
                      <TrendingUp className="h-4 w-4" />
                    ) : (
                      <TrendingDown className="h-4 w-4" />
                    )}
                    <span>{metric.trend.value}%</span>
                  </div>
                </div>
                <p className="text-sm text-muted-foreground mb-1">{metric.title}</p>
                <p className="text-3xl font-bold">{metric.value}</p>
              </CardContent>
            </Card>
          </motion.div>
        ))}
      </div>

      {/* Usage Over Time */}
      <Card className="backdrop-blur-xl bg-card/50 border-border/50 rounded-2xl">
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle>Usage Over Time</CardTitle>
              <CardDescription>API calls, cost, and tokens used</CardDescription>
            </div>
            <LineChartIcon className="h-5 w-5 text-muted-foreground" />
          </div>
        </CardHeader>
        <CardContent>
          <ResponsiveContainer width="100%" height={300}>
            <AreaChart data={usageData}>
              <defs>
                <linearGradient id="colorCalls" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3} />
                  <stop offset="95%" stopColor="#3b82f6" stopOpacity={0} />
                </linearGradient>
                <linearGradient id="colorCost" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#10b981" stopOpacity={0.3} />
                  <stop offset="95%" stopColor="#10b981" stopOpacity={0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#333" opacity={0.1} />
              <XAxis dataKey="date" stroke="#888" />
              <YAxis stroke="#888" />
              <Tooltip
                contentStyle={{
                  backgroundColor: 'rgba(0, 0, 0, 0.8)',
                  border: '1px solid #333',
                  borderRadius: '8px',
                }}
              />
              <Legend />
              <Area
                type="monotone"
                dataKey="calls"
                stroke="#3b82f6"
                fillOpacity={1}
                fill="url(#colorCalls)"
                name="API Calls"
              />
              <Area
                type="monotone"
                dataKey="cost"
                stroke="#10b981"
                fillOpacity={1}
                fill="url(#colorCost)"
                name="Cost ($)"
              />
            </AreaChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>

      {/* Provider & Model Distribution */}
      <div className="grid gap-6 md:grid-cols-2">
        {/* Provider Distribution */}
        <Card className="backdrop-blur-xl bg-card/50 border-border/50 rounded-2xl">
          <CardHeader>
            <div className="flex items-center justify-between">
              <div>
                <CardTitle>Provider Distribution</CardTitle>
                <CardDescription>Usage by LLM provider</CardDescription>
              </div>
              <PieChartIcon className="h-5 w-5 text-muted-foreground" />
            </div>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={providerData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }) => `${name} ${percent ? (percent * 100).toFixed(0) : 0}%`}
                  outerRadius={100}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {providerData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip
                  contentStyle={{
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    border: '1px solid #333',
                    borderRadius: '8px',
                  }}
                />
              </PieChart>
            </ResponsiveContainer>

            {/* Provider Legend */}
            <div className="mt-4 space-y-2">
              {providerData.map((provider) => (
                <div key={provider.name} className="flex items-center justify-between text-sm">
                  <div className="flex items-center space-x-2">
                    <div
                      className="w-3 h-3 rounded-full"
                      style={{ backgroundColor: provider.color }}
                    />
                    <span>{provider.name}</span>
                  </div>
                  <div className="flex items-center space-x-4">
                    <span className="text-muted-foreground">{provider.value}%</span>
                    <span className="font-medium">${provider.cost.toFixed(2)}</span>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        {/* Tier Distribution */}
        <Card className="backdrop-blur-xl bg-card/50 border-border/50 rounded-2xl">
          <CardHeader>
            <div className="flex items-center justify-between">
              <div>
                <CardTitle>Tier Distribution</CardTitle>
                <CardDescription>Usage by tier level</CardDescription>
              </div>
              <BarChart3 className="h-5 w-5 text-muted-foreground" />
            </div>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={tierData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#333" opacity={0.1} />
                <XAxis dataKey="tier" stroke="#888" />
                <YAxis stroke="#888" />
                <Tooltip
                  contentStyle={{
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    border: '1px solid #333',
                    borderRadius: '8px',
                  }}
                />
                <Legend />
                <Bar dataKey="calls" fill="#3b82f6" name="API Calls" radius={[8, 8, 0, 0]} />
                <Bar dataKey="cost" fill="#10b981" name="Cost ($)" radius={[8, 8, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      {/* Model Performance Table */}
      <Card className="backdrop-blur-xl bg-card/50 border-border/50 rounded-2xl">
        <CardHeader>
          <CardTitle>Model Performance</CardTitle>
          <CardDescription>Detailed metrics by model</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-border/50">
                  <th className="text-left py-3 px-4 font-medium text-muted-foreground">Model</th>
                  <th className="text-right py-3 px-4 font-medium text-muted-foreground">API Calls</th>
                  <th className="text-right py-3 px-4 font-medium text-muted-foreground">Total Cost</th>
                  <th className="text-right py-3 px-4 font-medium text-muted-foreground">Avg Cost/Call</th>
                  <th className="text-right py-3 px-4 font-medium text-muted-foreground">Avg Latency</th>
                </tr>
              </thead>
              <tbody>
                {modelData.map((model, index) => (
                  <motion.tr
                    key={model.model}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: index * 0.05 }}
                    className="border-b border-border/50 hover:bg-muted/30 transition-colors"
                  >
                    <td className="py-3 px-4 font-medium">{model.model}</td>
                    <td className="py-3 px-4 text-right">{model.calls.toLocaleString()}</td>
                    <td className="py-3 px-4 text-right">${model.cost.toFixed(2)}</td>
                    <td className="py-3 px-4 text-right">${(model.cost / model.calls).toFixed(4)}</td>
                    <td className="py-3 px-4 text-right">
                      <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${
                        model.avgLatency < 1
                          ? 'bg-green-500/10 text-green-500'
                          : model.avgLatency < 2
                          ? 'bg-orange-500/10 text-orange-500'
                          : 'bg-red-500/10 text-red-500'
                      }`}>
                        {model.avgLatency}s
                      </span>
                    </td>
                  </motion.tr>
                ))}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>

      {/* Additional Stats */}
      <div className="grid gap-4 md:grid-cols-3">
        <Card className="backdrop-blur-xl bg-card/50 border-border/50 rounded-xl">
          <CardContent className="p-6">
            <div className="flex items-center space-x-3">
              <div className="bg-blue-500/10 p-3 rounded-lg">
                <Activity className="h-6 w-6 text-blue-500" />
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Total Tokens</p>
                <p className="text-2xl font-bold">{(stats.totalTokens / 1000).toFixed(0)}K</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="backdrop-blur-xl bg-card/50 border-border/50 rounded-xl">
          <CardContent className="p-6">
            <div className="flex items-center space-x-3">
              <div className="bg-green-500/10 p-3 rounded-lg">
                <DollarSign className="h-6 w-6 text-green-500" />
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Avg Cost/Call</p>
                <p className="text-2xl font-bold">${stats.avgCostPerCall.toFixed(3)}</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="backdrop-blur-xl bg-card/50 border-border/50 rounded-xl">
          <CardContent className="p-6">
            <div className="flex items-center space-x-3">
              <div className="bg-purple-500/10 p-3 rounded-lg">
                <Calendar className="h-6 w-6 text-purple-500" />
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Time Range</p>
                <p className="text-2xl font-bold">7 Days</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
