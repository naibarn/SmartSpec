import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import {
  Wallet,
  TrendingUp,
  TrendingDown,
  Plus,
  Download,
  Filter,
  Search,
  ArrowUpRight,
  ArrowDownRight,
  DollarSign,
  Zap,
  Calendar
} from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';

export default function CreditsPage() {
  const navigate = useNavigate();
  const [filter, setFilter] = useState('all');

  // Mock data - จะเชื่อมกับ API ในภายหลัง
  const balance = {
    current: 12450,
    purchased: 15000,
    used: 2550,
    change: '+12.5%',
    trend: 'up',
  };

  const stats = [
    {
      title: 'Total Purchased',
      value: '15,000',
      icon: DollarSign,
      color: 'text-green-500',
      bgColor: 'bg-green-500/10',
    },
    {
      title: 'Total Used',
      value: '2,550',
      icon: Zap,
      color: 'text-orange-500',
      bgColor: 'bg-orange-500/10',
    },
    {
      title: 'This Month',
      value: '850',
      icon: Calendar,
      color: 'text-blue-500',
      bgColor: 'bg-blue-500/10',
    },
  ];

  const transactions = [
    {
      id: 1,
      type: 'purchase',
      amount: 5000,
      description: 'Credit Package - Pro',
      date: '2025-12-30 10:30',
      balance: 12450,
      status: 'completed',
    },
    {
      id: 2,
      type: 'usage',
      amount: -150,
      description: 'LLM API Call - GPT-4',
      date: '2025-12-30 09:15',
      balance: 7450,
      status: 'completed',
    },
    {
      id: 3,
      type: 'usage',
      amount: -200,
      description: 'LLM API Call - Claude 3',
      date: '2025-12-29 18:45',
      balance: 7600,
      status: 'completed',
    },
    {
      id: 4,
      type: 'purchase',
      amount: 10000,
      description: 'Credit Package - Business',
      date: '2025-12-28 14:20',
      balance: 7800,
      status: 'completed',
    },
    {
      id: 5,
      type: 'bonus',
      amount: 500,
      description: 'Referral Bonus',
      date: '2025-12-27 11:00',
      balance: -2200,
      status: 'completed',
    },
    {
      id: 6,
      type: 'usage',
      amount: -300,
      description: 'LLM API Call - Gemini Pro',
      date: '2025-12-27 09:30',
      balance: -2700,
      status: 'completed',
    },
  ];

  const getTransactionIcon = (type: string) => {
    if (type === 'purchase' || type === 'bonus') {
      return <ArrowDownRight className="h-4 w-4" />;
    }
    return <ArrowUpRight className="h-4 w-4" />;
  };

  const getTransactionColor = (type: string) => {
    if (type === 'purchase' || type === 'bonus') {
      return 'text-green-500';
    }
    return 'text-red-500';
  };

  const filteredTransactions = transactions.filter((t) => {
    if (filter === 'all') return true;
    return t.type === filter;
  });

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Credits</h1>
          <p className="text-muted-foreground mt-1">
            Manage your credits and view transaction history
          </p>
        </div>
        <Button 
          size="lg" 
          className="rounded-full shadow-lg shadow-primary/25"
          onClick={() => navigate('/dashboard/credits/buy')}
        >
          <Plus className="mr-2 h-5 w-5" />
          Buy Credits
        </Button>
      </div>

      {/* Balance Card - Large & Prominent */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <Card className="backdrop-blur-xl bg-gradient-to-br from-primary/10 via-card/50 to-primary/5 border-2 border-primary/20 rounded-3xl overflow-hidden">
          <CardContent className="p-8">
            <div className="flex items-start justify-between mb-6">
              <div>
                <p className="text-sm text-muted-foreground mb-2">Current Balance</p>
                <div className="flex items-baseline space-x-3">
                  <h2 className="text-5xl font-bold">{balance.current.toLocaleString()}</h2>
                  <span className="text-lg text-muted-foreground">credits</span>
                </div>
                <div className={`flex items-center mt-3 ${balance.trend === 'up' ? 'text-green-500' : 'text-red-500'}`}>
                  {balance.trend === 'up' ? (
                    <TrendingUp className="h-4 w-4 mr-1" />
                  ) : (
                    <TrendingDown className="h-4 w-4 mr-1" />
                  )}
                  <span className="text-sm font-medium">{balance.change} from last month</span>
                </div>
              </div>
              <div className="bg-primary/20 p-4 rounded-2xl">
                <Wallet className="h-8 w-8 text-primary" />
              </div>
            </div>

            {/* Usage Bar */}
            <div className="space-y-2">
              <div className="flex items-center justify-between text-sm">
                <span className="text-muted-foreground">Usage</span>
                <span className="font-medium">{balance.used.toLocaleString()} / {balance.purchased.toLocaleString()} credits</span>
              </div>
              <div className="h-3 bg-muted/30 rounded-full overflow-hidden">
                <motion.div
                  initial={{ width: 0 }}
                  animate={{ width: `${(balance.used / balance.purchased) * 100}%` }}
                  transition={{ duration: 1, ease: 'easeOut' }}
                  className="h-full bg-gradient-to-r from-primary to-primary/60 rounded-full"
                />
              </div>
            </div>
          </CardContent>
        </Card>
      </motion.div>

      {/* Stats Grid */}
      <div className="grid gap-4 md:grid-cols-3">
        {stats.map((stat, index) => {
          const Icon = stat.icon;
          return (
            <motion.div
              key={stat.title}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 + 0.2 }}
            >
              <Card className="backdrop-blur-xl bg-card/50 border-border/50 hover:border-primary/50 transition-all rounded-2xl">
                <CardContent className="p-6">
                  <div className="flex items-center justify-between mb-4">
                    <div className={`${stat.bgColor} ${stat.color} p-3 rounded-xl`}>
                      <Icon className="h-5 w-5" />
                    </div>
                  </div>
                  <p className="text-sm text-muted-foreground mb-1">{stat.title}</p>
                  <p className="text-2xl font-bold">{stat.value}</p>
                </CardContent>
              </Card>
            </motion.div>
          );
        })}
      </div>

      {/* Transaction History */}
      <Card className="backdrop-blur-xl bg-card/50 border-border/50 rounded-2xl">
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle>Transaction History</CardTitle>
            <div className="flex items-center space-x-2">
              <Button variant="outline" size="sm" className="rounded-lg">
                <Download className="mr-2 h-4 w-4" />
                Export
              </Button>
            </div>
          </div>
        </CardHeader>
        <CardContent>
          {/* Filters */}
          <div className="flex flex-col sm:flex-row gap-4 mb-6">
            <div className="flex-1 relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <Input
                placeholder="Search transactions..."
                className="pl-10 rounded-lg"
              />
            </div>
            <Select value={filter} onValueChange={setFilter}>
              <SelectTrigger className="w-full sm:w-[180px] rounded-lg">
                <Filter className="mr-2 h-4 w-4" />
                <SelectValue placeholder="Filter" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Types</SelectItem>
                <SelectItem value="purchase">Purchases</SelectItem>
                <SelectItem value="usage">Usage</SelectItem>
                <SelectItem value="bonus">Bonuses</SelectItem>
                <SelectItem value="refund">Refunds</SelectItem>
              </SelectContent>
            </Select>
          </div>

          {/* Transaction List */}
          <div className="space-y-2">
            {filteredTransactions.map((transaction, index) => (
              <motion.div
                key={transaction.id}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.05 }}
                className="flex items-center justify-between p-4 rounded-xl hover:bg-muted/50 transition-colors"
              >
                <div className="flex items-center space-x-4">
                  <div className={`${getTransactionColor(transaction.type)} p-2 rounded-lg bg-muted/50`}>
                    {getTransactionIcon(transaction.type)}
                  </div>
                  <div>
                    <p className="font-medium">{transaction.description}</p>
                    <p className="text-sm text-muted-foreground">{transaction.date}</p>
                  </div>
                </div>
                <div className="text-right">
                  <p className={`font-semibold ${getTransactionColor(transaction.type)}`}>
                    {transaction.amount > 0 ? '+' : ''}{transaction.amount.toLocaleString()}
                  </p>
                  <p className="text-sm text-muted-foreground">
                    Balance: {transaction.balance.toLocaleString()}
                  </p>
                </div>
              </motion.div>
            ))}
          </div>

          {/* Pagination */}
          <div className="flex items-center justify-between mt-6 pt-6 border-t border-border/50">
            <p className="text-sm text-muted-foreground">
              Showing 1-6 of 24 transactions
            </p>
            <div className="flex items-center space-x-2">
              <Button variant="outline" size="sm" className="rounded-lg">
                Previous
              </Button>
              <Button variant="outline" size="sm" className="rounded-lg">
                Next
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Quick Actions */}
      <Card className="backdrop-blur-xl bg-card/50 border-border/50 rounded-2xl">
        <CardHeader>
          <CardTitle>Quick Actions</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4 md:grid-cols-3">
            <Button variant="outline" className="h-auto flex-col py-6 rounded-xl hover:border-primary/50">
              <Plus className="h-8 w-8 mb-3 text-primary" />
              <span className="font-semibold text-lg">Buy Credits</span>
              <span className="text-sm text-muted-foreground mt-1">Purchase credit packages</span>
            </Button>
            <Button variant="outline" className="h-auto flex-col py-6 rounded-xl hover:border-primary/50">
              <Download className="h-8 w-8 mb-3 text-primary" />
              <span className="font-semibold text-lg">Export History</span>
              <span className="text-sm text-muted-foreground mt-1">Download transactions</span>
            </Button>
            <Button variant="outline" className="h-auto flex-col py-6 rounded-xl hover:border-primary/50">
              <TrendingUp className="h-8 w-8 mb-3 text-primary" />
              <span className="font-semibold text-lg">View Analytics</span>
              <span className="text-sm text-muted-foreground mt-1">Detailed usage insights</span>
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
