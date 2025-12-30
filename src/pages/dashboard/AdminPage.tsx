import { useState } from 'react';
import { motion } from 'framer-motion';
import {
  Users,
  Settings,
  Shield,
  Activity,
  Server,
  AlertTriangle,
  CheckCircle2,
  Clock,
  Search,
  MoreVertical,
  UserPlus,
  Edit,
  Trash2,
  Ban,
  UserCheck,
  Mail,
  Calendar,
  DollarSign,
  Zap,
  FileText
} from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import {
  Tabs,
  TabsContent,
  TabsList,
  TabsTrigger,
} from '@/components/ui/tabs';

export default function AdminPage() {
  const [searchQuery, setSearchQuery] = useState('');
  const [filterRole, setFilterRole] = useState('all');
  const [filterStatus, setFilterStatus] = useState('all');

  // Mock data - จะเชื่อมกับ API ในภายหลัง
  const users = [
    {
      id: 1,
      name: 'John Doe',
      email: 'john@example.com',
      role: 'admin',
      status: 'active',
      credits: 12450,
      totalSpent: 238.00,
      lastActive: '2025-01-15 14:30',
      joinDate: '2024-12-01',
      apiCalls: 1150,
    },
    {
      id: 2,
      name: 'Jane Smith',
      email: 'jane@example.com',
      role: 'user',
      status: 'active',
      credits: 5230,
      totalSpent: 125.00,
      lastActive: '2025-01-15 12:15',
      joinDate: '2024-12-15',
      apiCalls: 680,
    },
    {
      id: 3,
      name: 'Bob Johnson',
      email: 'bob@example.com',
      role: 'user',
      status: 'suspended',
      credits: 0,
      totalSpent: 49.00,
      lastActive: '2025-01-10 09:45',
      joinDate: '2025-01-05',
      apiCalls: 250,
    },
    {
      id: 4,
      name: 'Alice Williams',
      email: 'alice@example.com',
      role: 'user',
      status: 'active',
      credits: 8750,
      totalSpent: 189.00,
      lastActive: '2025-01-15 16:20',
      joinDate: '2024-11-20',
      apiCalls: 920,
    },
    {
      id: 5,
      name: 'Charlie Brown',
      email: 'charlie@example.com',
      role: 'moderator',
      status: 'active',
      credits: 15000,
      totalSpent: 450.00,
      lastActive: '2025-01-15 11:00',
      joinDate: '2024-10-15',
      apiCalls: 2150,
    },
  ];

  const systemStats = {
    totalUsers: 1250,
    activeUsers: 980,
    suspendedUsers: 15,
    totalRevenue: 125450.00,
    totalCredits: 15500000,
    totalApiCalls: 2850000,
    avgResponseTime: 1.2,
    uptime: 99.95,
  };

  const systemHealth = [
    { name: 'API Gateway', status: 'healthy', uptime: 99.98, latency: 45 },
    { name: 'Database', status: 'healthy', uptime: 99.99, latency: 12 },
    { name: 'LLM Providers', status: 'warning', uptime: 99.85, latency: 1200 },
    { name: 'Payment System', status: 'healthy', uptime: 99.95, latency: 250 },
    { name: 'Auth Service', status: 'healthy', uptime: 99.97, latency: 85 },
  ];

  const auditLogs = [
    {
      id: 1,
      user: 'admin@smartspec.com',
      action: 'User Suspended',
      target: 'bob@example.com',
      timestamp: '2025-01-15 14:30:00',
      details: 'Suspended for policy violation',
    },
    {
      id: 2,
      user: 'admin@smartspec.com',
      action: 'System Settings Updated',
      target: 'Rate Limits',
      timestamp: '2025-01-15 13:15:00',
      details: 'Increased rate limit to 1000/hour',
    },
    {
      id: 3,
      user: 'moderator@smartspec.com',
      action: 'User Credits Added',
      target: 'alice@example.com',
      timestamp: '2025-01-15 12:00:00',
      details: 'Added 5000 credits (refund)',
    },
    {
      id: 4,
      user: 'admin@smartspec.com',
      action: 'Provider Configuration',
      target: 'OpenAI',
      timestamp: '2025-01-15 10:30:00',
      details: 'Updated API key',
    },
  ];

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active':
        return 'text-green-500 bg-green-500/10';
      case 'suspended':
        return 'text-red-500 bg-red-500/10';
      case 'inactive':
        return 'text-gray-500 bg-gray-500/10';
      default:
        return 'text-gray-500 bg-gray-500/10';
    }
  };

  const getRoleBadgeColor = (role: string) => {
    switch (role) {
      case 'admin':
        return 'bg-purple-500/10 text-purple-500 border-purple-500/20';
      case 'moderator':
        return 'bg-blue-500/10 text-blue-500 border-blue-500/20';
      case 'user':
        return 'bg-gray-500/10 text-gray-500 border-gray-500/20';
      default:
        return 'bg-gray-500/10 text-gray-500 border-gray-500/20';
    }
  };

  const getHealthStatusColor = (status: string) => {
    switch (status) {
      case 'healthy':
        return 'text-green-500 bg-green-500/10';
      case 'warning':
        return 'text-orange-500 bg-orange-500/10';
      case 'error':
        return 'text-red-500 bg-red-500/10';
      default:
        return 'text-gray-500 bg-gray-500/10';
    }
  };

  const getHealthIcon = (status: string) => {
    switch (status) {
      case 'healthy':
        return <CheckCircle2 className="h-4 w-4" />;
      case 'warning':
        return <AlertTriangle className="h-4 w-4" />;
      case 'error':
        return <AlertTriangle className="h-4 w-4" />;
      default:
        return null;
    }
  };

  const filteredUsers = users.filter((user) => {
    const matchesSearch =
      user.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      user.email.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesRole = filterRole === 'all' || user.role === filterRole;
    const matchesStatus = filterStatus === 'all' || user.status === filterStatus;
    return matchesSearch && matchesRole && matchesStatus;
  });

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Admin Dashboard</h1>
          <p className="text-muted-foreground mt-1">
            Manage users, system settings, and monitor health
          </p>
        </div>
        <Button className="rounded-full">
          <UserPlus className="mr-2 h-4 w-4" />
          Add User
        </Button>
      </div>

      {/* System Stats */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {[
          {
            title: 'Total Users',
            value: systemStats.totalUsers.toLocaleString(),
            icon: Users,
            color: 'text-blue-500',
            bgColor: 'bg-blue-500/10',
            subtitle: `${systemStats.activeUsers} active`,
          },
          {
            title: 'Total Revenue',
            value: `$${(systemStats.totalRevenue / 1000).toFixed(1)}K`,
            icon: DollarSign,
            color: 'text-green-500',
            bgColor: 'bg-green-500/10',
            subtitle: 'All time',
          },
          {
            title: 'API Calls',
            value: `${(systemStats.totalApiCalls / 1000000).toFixed(1)}M`,
            icon: Zap,
            color: 'text-orange-500',
            bgColor: 'bg-orange-500/10',
            subtitle: 'Total processed',
          },
          {
            title: 'System Uptime',
            value: `${systemStats.uptime}%`,
            icon: Activity,
            color: 'text-purple-500',
            bgColor: 'bg-purple-500/10',
            subtitle: 'Last 30 days',
          },
        ].map((stat, index) => (
          <motion.div
            key={stat.title}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
          >
            <Card className="backdrop-blur-xl bg-card/50 border-border/50 hover:border-primary/50 transition-all rounded-2xl">
              <CardContent className="p-6">
                <div className="flex items-center justify-between mb-4">
                  <div className={`${stat.bgColor} p-3 rounded-xl`}>
                    <stat.icon className={`h-6 w-6 ${stat.color}`} />
                  </div>
                </div>
                <p className="text-sm text-muted-foreground mb-1">{stat.title}</p>
                <p className="text-3xl font-bold mb-1">{stat.value}</p>
                <p className="text-xs text-muted-foreground">{stat.subtitle}</p>
              </CardContent>
            </Card>
          </motion.div>
        ))}
      </div>

      {/* Main Tabs */}
      <Tabs defaultValue="users" className="space-y-6">
        <TabsList className="grid w-full grid-cols-4 lg:w-auto lg:inline-grid rounded-full">
          <TabsTrigger value="users" className="rounded-full">
            <Users className="h-4 w-4 mr-2" />
            Users
          </TabsTrigger>
          <TabsTrigger value="health" className="rounded-full">
            <Activity className="h-4 w-4 mr-2" />
            System Health
          </TabsTrigger>
          <TabsTrigger value="logs" className="rounded-full">
            <FileText className="h-4 w-4 mr-2" />
            Audit Logs
          </TabsTrigger>
          <TabsTrigger value="settings" className="rounded-full">
            <Settings className="h-4 w-4 mr-2" />
            Settings
          </TabsTrigger>
        </TabsList>

        {/* Users Tab */}
        <TabsContent value="users" className="space-y-4">
          <Card className="backdrop-blur-xl bg-card/50 border-border/50 rounded-2xl">
            <CardHeader>
              <div className="flex items-center justify-between">
                <div>
                  <CardTitle>User Management</CardTitle>
                  <CardDescription>Manage all users and their permissions</CardDescription>
                </div>
              </div>
            </CardHeader>
            <CardContent>
              {/* Filters */}
              <div className="flex items-center space-x-4 mb-6">
                <div className="flex-1">
                  <div className="relative">
                    <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                    <Input
                      placeholder="Search users..."
                      value={searchQuery}
                      onChange={(e) => setSearchQuery(e.target.value)}
                      className="pl-10 rounded-lg"
                    />
                  </div>
                </div>
                <Select value={filterRole} onValueChange={setFilterRole}>
                  <SelectTrigger className="w-[150px] rounded-lg">
                    <SelectValue placeholder="Role" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">All Roles</SelectItem>
                    <SelectItem value="admin">Admin</SelectItem>
                    <SelectItem value="moderator">Moderator</SelectItem>
                    <SelectItem value="user">User</SelectItem>
                  </SelectContent>
                </Select>
                <Select value={filterStatus} onValueChange={setFilterStatus}>
                  <SelectTrigger className="w-[150px] rounded-lg">
                    <SelectValue placeholder="Status" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">All Status</SelectItem>
                    <SelectItem value="active">Active</SelectItem>
                    <SelectItem value="suspended">Suspended</SelectItem>
                    <SelectItem value="inactive">Inactive</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              {/* Users Table */}
              <div className="space-y-3">
                {filteredUsers.map((user, index) => (
                  <motion.div
                    key={user.id}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: index * 0.05 }}
                    className="p-4 rounded-xl border border-border/50 hover:border-primary/50 transition-all"
                  >
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-4 flex-1">
                        <div className="bg-primary/10 p-3 rounded-xl">
                          <Users className="h-5 w-5 text-primary" />
                        </div>

                        <div className="flex-1">
                          <div className="flex items-center space-x-2 mb-1">
                            <p className="font-medium">{user.name}</p>
                            <span
                              className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium border ${getRoleBadgeColor(
                                user.role
                              )}`}
                            >
                              {user.role}
                            </span>
                            <span
                              className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium ${getStatusColor(
                                user.status
                              )}`}
                            >
                              {user.status}
                            </span>
                          </div>
                          <div className="flex items-center space-x-4 text-sm text-muted-foreground">
                            <span className="flex items-center">
                              <Mail className="h-3 w-3 mr-1" />
                              {user.email}
                            </span>
                            <span className="flex items-center">
                              <Calendar className="h-3 w-3 mr-1" />
                              Joined {new Date(user.joinDate).toLocaleDateString()}
                            </span>
                            <span className="flex items-center">
                              <Clock className="h-3 w-3 mr-1" />
                              Last active {new Date(user.lastActive).toLocaleString()}
                            </span>
                          </div>
                        </div>
                      </div>

                      <div className="flex items-center space-x-6">
                        <div className="text-right">
                          <p className="text-sm text-muted-foreground">Credits</p>
                          <p className="font-semibold">{user.credits.toLocaleString()}</p>
                        </div>
                        <div className="text-right">
                          <p className="text-sm text-muted-foreground">Spent</p>
                          <p className="font-semibold">${user.totalSpent.toFixed(2)}</p>
                        </div>
                        <div className="text-right">
                          <p className="text-sm text-muted-foreground">API Calls</p>
                          <p className="font-semibold">{user.apiCalls.toLocaleString()}</p>
                        </div>

                        <DropdownMenu>
                          <DropdownMenuTrigger asChild>
                            <Button variant="ghost" size="sm" className="h-8 w-8 p-0">
                              <MoreVertical className="h-4 w-4" />
                            </Button>
                          </DropdownMenuTrigger>
                          <DropdownMenuContent align="end">
                            <DropdownMenuItem>
                              <Edit className="mr-2 h-4 w-4" />
                              Edit User
                            </DropdownMenuItem>
                            <DropdownMenuItem>
                              <Shield className="mr-2 h-4 w-4" />
                              Change Role
                            </DropdownMenuItem>
                            <DropdownMenuItem>
                              <DollarSign className="mr-2 h-4 w-4" />
                              Add Credits
                            </DropdownMenuItem>
                            {user.status === 'active' ? (
                              <DropdownMenuItem className="text-orange-500">
                                <Ban className="mr-2 h-4 w-4" />
                                Suspend User
                              </DropdownMenuItem>
                            ) : (
                              <DropdownMenuItem className="text-green-500">
                                <UserCheck className="mr-2 h-4 w-4" />
                                Activate User
                              </DropdownMenuItem>
                            )}
                            <DropdownMenuItem className="text-red-500">
                              <Trash2 className="mr-2 h-4 w-4" />
                              Delete User
                            </DropdownMenuItem>
                          </DropdownMenuContent>
                        </DropdownMenu>
                      </div>
                    </div>
                  </motion.div>
                ))}
              </div>

              {/* Pagination */}
              <div className="flex items-center justify-between mt-6 pt-6 border-t border-border/50">
                <p className="text-sm text-muted-foreground">
                  Showing {filteredUsers.length} of {users.length} users
                </p>
                <div className="flex items-center space-x-2">
                  <Button variant="outline" size="sm" className="rounded-lg" disabled>
                    Previous
                  </Button>
                  <Button variant="outline" size="sm" className="rounded-lg">
                    Next
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* System Health Tab */}
        <TabsContent value="health" className="space-y-4">
          <Card className="backdrop-blur-xl bg-card/50 border-border/50 rounded-2xl">
            <CardHeader>
              <CardTitle>System Health</CardTitle>
              <CardDescription>Monitor system components and performance</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {systemHealth.map((component, index) => (
                  <motion.div
                    key={component.name}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: index * 0.1 }}
                    className="p-4 rounded-xl border border-border/50"
                  >
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-4">
                        <div className={`p-3 rounded-xl ${getHealthStatusColor(component.status)}`}>
                          {component.status === 'healthy' ? (
                            <Server className="h-5 w-5" />
                          ) : (
                            <AlertTriangle className="h-5 w-5" />
                          )}
                        </div>
                        <div>
                          <div className="flex items-center space-x-2 mb-1">
                            <p className="font-medium">{component.name}</p>
                            <span
                              className={`inline-flex items-center space-x-1 px-2 py-0.5 rounded-full text-xs font-medium ${getHealthStatusColor(
                                component.status
                              )}`}
                            >
                              {getHealthIcon(component.status)}
                              <span className="capitalize">{component.status}</span>
                            </span>
                          </div>
                          <p className="text-sm text-muted-foreground">
                            Uptime: {component.uptime}% | Latency: {component.latency}ms
                          </p>
                        </div>
                      </div>
                      <Button variant="outline" size="sm" className="rounded-lg">
                        View Details
                      </Button>
                    </div>
                  </motion.div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Audit Logs Tab */}
        <TabsContent value="logs" className="space-y-4">
          <Card className="backdrop-blur-xl bg-card/50 border-border/50 rounded-2xl">
            <CardHeader>
              <CardTitle>Audit Logs</CardTitle>
              <CardDescription>Track all administrative actions</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {auditLogs.map((log, index) => (
                  <motion.div
                    key={log.id}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: index * 0.05 }}
                    className="p-4 rounded-xl border border-border/50"
                  >
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <div className="flex items-center space-x-2 mb-2">
                          <span className="font-medium">{log.action}</span>
                          <span className="text-sm text-muted-foreground">→</span>
                          <span className="text-sm text-muted-foreground">{log.target}</span>
                        </div>
                        <p className="text-sm text-muted-foreground mb-2">{log.details}</p>
                        <div className="flex items-center space-x-4 text-xs text-muted-foreground">
                          <span className="flex items-center">
                            <Users className="h-3 w-3 mr-1" />
                            {log.user}
                          </span>
                          <span className="flex items-center">
                            <Clock className="h-3 w-3 mr-1" />
                            {log.timestamp}
                          </span>
                        </div>
                      </div>
                    </div>
                  </motion.div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Settings Tab */}
        <TabsContent value="settings" className="space-y-4">
          <div className="grid gap-4 md:grid-cols-2">
            <Card className="backdrop-blur-xl bg-card/50 border-border/50 rounded-2xl">
              <CardHeader>
                <CardTitle>General Settings</CardTitle>
                <CardDescription>Configure system-wide settings</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <label className="text-sm font-medium mb-2 block">Site Name</label>
                  <Input defaultValue="SmartSpec Pro" className="rounded-lg" />
                </div>
                <div>
                  <label className="text-sm font-medium mb-2 block">Support Email</label>
                  <Input defaultValue="support@smartspecpro.com" className="rounded-lg" />
                </div>
                <div>
                  <label className="text-sm font-medium mb-2 block">Default Credits</label>
                  <Input defaultValue="1000" type="number" className="rounded-lg" />
                </div>
                <Button className="w-full rounded-lg">Save Changes</Button>
              </CardContent>
            </Card>

            <Card className="backdrop-blur-xl bg-card/50 border-border/50 rounded-2xl">
              <CardHeader>
                <CardTitle>Rate Limits</CardTitle>
                <CardDescription>Configure API rate limits</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <label className="text-sm font-medium mb-2 block">Requests per Hour</label>
                  <Input defaultValue="1000" type="number" className="rounded-lg" />
                </div>
                <div>
                  <label className="text-sm font-medium mb-2 block">Requests per Day</label>
                  <Input defaultValue="10000" type="number" className="rounded-lg" />
                </div>
                <div>
                  <label className="text-sm font-medium mb-2 block">Burst Limit</label>
                  <Input defaultValue="100" type="number" className="rounded-lg" />
                </div>
                <Button className="w-full rounded-lg">Update Limits</Button>
              </CardContent>
            </Card>

            <Card className="backdrop-blur-xl bg-card/50 border-border/50 rounded-2xl">
              <CardHeader>
                <CardTitle>Email Settings</CardTitle>
                <CardDescription>Configure email notifications</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <label className="text-sm font-medium mb-2 block">SMTP Host</label>
                  <Input defaultValue="smtp.gmail.com" className="rounded-lg" />
                </div>
                <div>
                  <label className="text-sm font-medium mb-2 block">SMTP Port</label>
                  <Input defaultValue="587" type="number" className="rounded-lg" />
                </div>
                <div>
                  <label className="text-sm font-medium mb-2 block">From Email</label>
                  <Input defaultValue="noreply@smartspecpro.com" className="rounded-lg" />
                </div>
                <Button className="w-full rounded-lg">Save Email Settings</Button>
              </CardContent>
            </Card>

            <Card className="backdrop-blur-xl bg-card/50 border-border/50 rounded-2xl">
              <CardHeader>
                <CardTitle>Security</CardTitle>
                <CardDescription>Configure security settings</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <label className="text-sm font-medium mb-2 block">Session Timeout (minutes)</label>
                  <Input defaultValue="60" type="number" className="rounded-lg" />
                </div>
                <div>
                  <label className="text-sm font-medium mb-2 block">Max Login Attempts</label>
                  <Input defaultValue="5" type="number" className="rounded-lg" />
                </div>
                <div>
                  <label className="text-sm font-medium mb-2 block">Password Min Length</label>
                  <Input defaultValue="8" type="number" className="rounded-lg" />
                </div>
                <Button className="w-full rounded-lg">Update Security</Button>
              </CardContent>
            </Card>
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
}
