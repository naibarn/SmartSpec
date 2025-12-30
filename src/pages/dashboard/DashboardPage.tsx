import { motion } from 'framer-motion';
import {
  Wallet,
  Zap,
  TrendingUp,
  Activity,
  DollarSign,
  Clock,
  CheckCircle2,
  AlertCircle
} from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';

export default function DashboardPage() {
  const stats = [
    {
      title: 'Credits Balance',
      value: '12,450',
      change: '+12.5%',
      trend: 'up',
      icon: Wallet,
      color: 'text-blue-500',
      bgColor: 'bg-blue-500/10',
    },
    {
      title: 'API Requests',
      value: '45.2K',
      change: '+8.2%',
      trend: 'up',
      icon: Zap,
      color: 'text-yellow-500',
      bgColor: 'bg-yellow-500/10',
    },
    {
      title: 'Total Spend',
      value: '$234.50',
      change: '-5.4%',
      trend: 'down',
      icon: DollarSign,
      color: 'text-green-500',
      bgColor: 'bg-green-500/10',
    },
    {
      title: 'Avg Response Time',
      value: '42ms',
      change: '-12.3%',
      trend: 'down',
      icon: Clock,
      color: 'text-purple-500',
      bgColor: 'bg-purple-500/10',
    },
  ];

  const recentActivity = [
    {
      type: 'success',
      title: 'API Request Completed',
      description: 'GPT-4 completion request',
      time: '2 minutes ago',
      icon: CheckCircle2,
      color: 'text-green-500',
    },
    {
      type: 'success',
      title: 'Credits Added',
      description: '+1,000 credits purchased',
      time: '1 hour ago',
      icon: Wallet,
      color: 'text-blue-500',
    },
    {
      type: 'warning',
      title: 'Rate Limit Warning',
      description: 'Approaching hourly limit',
      time: '3 hours ago',
      icon: AlertCircle,
      color: 'text-orange-500',
    },
    {
      type: 'success',
      title: 'API Key Created',
      description: 'New production key',
      time: '1 day ago',
      icon: CheckCircle2,
      color: 'text-green-500',
    },
  ];

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Dashboard</h1>
          <p className="text-muted-foreground mt-1">
            Welcome back! Here's what's happening with your account.
          </p>
        </div>
        <Button className="rounded-full">
          <Zap className="mr-2 h-4 w-4" />
          Quick Start Guide
        </Button>
      </div>

      {/* Stats Grid */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {stats.map((stat, index) => {
          const Icon = stat.icon;
          return (
            <motion.div
              key={stat.title}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
            >
              <Card className="backdrop-blur-xl bg-card/50 border-border/50 hover:border-primary/50 transition-all rounded-2xl">
                <CardContent className="p-6">
                  <div className="flex items-center justify-between mb-4">
                    <div className={`${stat.bgColor} ${stat.color} p-3 rounded-xl`}>
                      <Icon className="h-5 w-5" />
                    </div>
                    <div className={`text-sm font-medium ${stat.trend === 'up' ? 'text-green-500' : 'text-red-500'}`}>
                      {stat.change}
                    </div>
                  </div>
                  <div>
                    <p className="text-sm text-muted-foreground mb-1">{stat.title}</p>
                    <p className="text-2xl font-bold">{stat.value}</p>
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          );
        })}
      </div>

      {/* Main Content Grid */}
      <div className="grid gap-6 lg:grid-cols-3">
        {/* Usage Chart */}
        <Card className="lg:col-span-2 backdrop-blur-xl bg-card/50 border-border/50 rounded-2xl">
          <CardHeader>
            <CardTitle>Usage Overview</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="h-[300px] flex items-center justify-center bg-muted/30 rounded-xl">
              <div className="text-center">
                <Activity className="h-12 w-12 text-muted-foreground mx-auto mb-2" />
                <p className="text-sm text-muted-foreground">Chart will be implemented in Phase 8</p>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Recent Activity */}
        <Card className="backdrop-blur-xl bg-card/50 border-border/50 rounded-2xl">
          <CardHeader>
            <CardTitle>Recent Activity</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {recentActivity.map((activity, index) => {
                const Icon = activity.icon;
                return (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: index * 0.1 }}
                    className="flex items-start space-x-3 p-3 rounded-xl hover:bg-muted/50 transition-colors"
                  >
                    <div className={`${activity.color} mt-0.5`}>
                      <Icon className="h-5 w-5" />
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium">{activity.title}</p>
                      <p className="text-xs text-muted-foreground">{activity.description}</p>
                      <p className="text-xs text-muted-foreground mt-1">{activity.time}</p>
                    </div>
                  </motion.div>
                );
              })}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Quick Actions */}
      <Card className="backdrop-blur-xl bg-card/50 border-border/50 rounded-2xl">
        <CardHeader>
          <CardTitle>Quick Actions</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4 md:grid-cols-4">
            <Button variant="outline" className="h-auto flex-col py-4 rounded-xl">
              <Wallet className="h-6 w-6 mb-2" />
              <span className="font-medium">Add Credits</span>
              <span className="text-xs text-muted-foreground mt-1">Purchase more credits</span>
            </Button>
            <Button variant="outline" className="h-auto flex-col py-4 rounded-xl">
              <Zap className="h-6 w-6 mb-2" />
              <span className="font-medium">Configure Gateway</span>
              <span className="text-xs text-muted-foreground mt-1">Setup LLM providers</span>
            </Button>
            <Button variant="outline" className="h-auto flex-col py-4 rounded-xl">
              <Activity className="h-6 w-6 mb-2" />
              <span className="font-medium">View Analytics</span>
              <span className="text-xs text-muted-foreground mt-1">Detailed insights</span>
            </Button>
            <Button variant="outline" className="h-auto flex-col py-4 rounded-xl">
              <TrendingUp className="h-6 w-6 mb-2" />
              <span className="font-medium">API Documentation</span>
              <span className="text-xs text-muted-foreground mt-1">Integration guides</span>
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
