/**
 * Dashboard Page - SmartSpec Pro
 * User dashboard after login
 */

import { useEffect } from 'react';
import { useLocation } from 'wouter';
import { motion } from 'framer-motion';
import { useAuth } from '@/contexts/AuthContext';
import { Button } from '@/components/ui/button';
import {
  Sparkles,
  Image,
  Video,
  Music,
  CreditCard,
  Settings,
  LogOut,
  TrendingUp,
  Clock,
  Zap,
  ChevronRight,
  Plus,
  MessageSquare,
} from 'lucide-react';

export default function Dashboard() {
  const { user, isLoading, isAuthenticated, logout } = useAuth();
  const [, setLocation] = useLocation();

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      setLocation('/login');
    }
  }, [isLoading, isAuthenticated, setLocation]);

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 via-purple-50/30 to-pink-50/20 flex items-center justify-center">
        <div className="animate-spin w-8 h-8 border-4 border-purple-500 border-t-transparent rounded-full" />
      </div>
    );
  }

  if (!user) {
    return null;
  }

  const stats = [
    { label: 'Credits Available', value: (user.credits ?? 0).toString(), icon: Zap, color: 'text-yellow-500' },
    { label: 'Generations Today', value: '12', icon: TrendingUp, color: 'text-green-500' },
    { label: 'Total Projects', value: '24', icon: Image, color: 'text-purple-500' },
    { label: 'Time Saved', value: '48h', icon: Clock, color: 'text-blue-500' },
  ];

  const quickActions = [
    { label: 'Generate Image', icon: Image, href: '/generate/image', color: 'from-purple-500 to-pink-500' },
    { label: 'Chat (LLM)', icon: MessageSquare, href: '/chat', color: 'from-teal-500 to-violet-500' },
    { label: 'Generate Video', icon: Video, href: '/generate/video', color: 'from-blue-500 to-cyan-500' },
    { label: 'Generate Audio', icon: Music, href: '/generate/audio', color: 'from-orange-500 to-red-500' },
    { label: 'Buy Credits', icon: CreditCard, href: '/credits', color: 'from-green-500 to-emerald-500' },
  ];

  const recentActivity = [
    { type: 'image', title: 'Abstract Art Generation', time: '2 hours ago', status: 'completed' },
    { type: 'video', title: 'Product Demo Video', time: '5 hours ago', status: 'completed' },
    { type: 'image', title: 'Logo Design Concept', time: '1 day ago', status: 'completed' },
    { type: 'audio', title: 'Podcast Intro', time: '2 days ago', status: 'completed' },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-purple-50/30 to-pink-50/20">
      {/* Sidebar */}
      <aside className="fixed left-0 top-0 bottom-0 w-64 bg-white/70 backdrop-blur-xl border-r border-gray-200/50 p-6 hidden lg:block">
        <div className="flex items-center gap-3 mb-8">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center">
            <Sparkles className="w-5 h-5 text-white" />
          </div>
          <span className="text-xl font-bold text-gray-900">SmartSpec</span>
        </div>

        <nav className="space-y-2">
          {[
            { label: 'Dashboard', icon: TrendingUp, active: true },
            { label: 'Generate', icon: Sparkles },
            { label: 'Gallery', icon: Image },
            { label: 'Credits', icon: CreditCard },
            { label: 'Settings', icon: Settings },
          ].map((item) => (
            <button
              key={item.label}
              className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl text-left transition-all ${
                item.active
                  ? 'bg-gradient-to-r from-purple-500/10 to-pink-500/10 text-purple-700'
                  : 'text-gray-600 hover:bg-gray-100'
              }`}
            >
              <item.icon className="w-5 h-5" />
              <span className="font-medium">{item.label}</span>
            </button>
          ))}
        </nav>

        <div className="absolute bottom-6 left-6 right-6">
          <Button
            variant="ghost"
            onClick={logout}
            className="w-full justify-start text-gray-600 hover:text-red-600"
          >
            <LogOut className="w-5 h-5 mr-3" />
            Sign Out
          </Button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="lg:ml-64 p-6 lg:p-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Welcome back, {user.name.split(' ')[0]}!
          </h1>
          <p className="text-gray-600">
            Here's what's happening with your account today.
          </p>
        </motion.div>

        {/* Stats Grid */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-8"
        >
          {stats.map((stat, index) => (
            <div
              key={index}
              className="bg-white/70 backdrop-blur-xl rounded-2xl border border-white/50 p-6 shadow-lg shadow-purple-500/5"
            >
              <div className="flex items-center justify-between mb-4">
                <stat.icon className={`w-8 h-8 ${stat.color}`} />
                <span className="text-xs font-medium text-gray-500 bg-gray-100 px-2 py-1 rounded-full">
                  {user.plan.toUpperCase()}
                </span>
              </div>
              <div className="text-3xl font-bold text-gray-900 mb-1">{stat.value}</div>
              <div className="text-sm text-gray-500">{stat.label}</div>
            </div>
          ))}
        </motion.div>

        {/* Quick Actions */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="mb-8"
        >
          <h2 className="text-xl font-bold text-gray-900 mb-4">Quick Actions</h2>
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
            {quickActions.map((action, index) => (
              <button
                key={index}
                className="group relative bg-white/70 backdrop-blur-xl rounded-2xl border border-white/50 p-6 shadow-lg shadow-purple-500/5 hover:shadow-xl transition-all duration-300 overflow-hidden"
              >
                <div className={`absolute inset-0 bg-gradient-to-br ${action.color} opacity-0 group-hover:opacity-10 transition-opacity`} />
                <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${action.color} flex items-center justify-center mb-4`}>
                  <action.icon className="w-6 h-6 text-white" />
                </div>
                <div className="font-semibold text-gray-900">{action.label}</div>
                <ChevronRight className="absolute right-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400 group-hover:text-gray-600 transition-colors" />
              </button>
            ))}
          </div>
        </motion.div>

        {/* Recent Activity */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
        >
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-bold text-gray-900">Recent Activity</h2>
            <Button variant="ghost" size="sm" className="text-purple-600">
              View All
              <ChevronRight className="w-4 h-4 ml-1" />
            </Button>
          </div>
          <div className="bg-white/70 backdrop-blur-xl rounded-2xl border border-white/50 shadow-lg shadow-purple-500/5 overflow-hidden">
            {recentActivity.map((activity, index) => (
              <div
                key={index}
                className={`flex items-center gap-4 p-4 ${
                  index !== recentActivity.length - 1 ? 'border-b border-gray-100' : ''
                }`}
              >
                <div className={`w-10 h-10 rounded-xl flex items-center justify-center ${
                  activity.type === 'image' ? 'bg-purple-100 text-purple-600' :
                  activity.type === 'video' ? 'bg-blue-100 text-blue-600' :
                  'bg-orange-100 text-orange-600'
                }`}>
                  {activity.type === 'image' ? <Image className="w-5 h-5" /> :
                   activity.type === 'video' ? <Video className="w-5 h-5" /> :
                   <Music className="w-5 h-5" />}
                </div>
                <div className="flex-1">
                  <div className="font-medium text-gray-900">{activity.title}</div>
                  <div className="text-sm text-gray-500">{activity.time}</div>
                </div>
                <span className="px-2 py-1 text-xs font-medium bg-green-100 text-green-700 rounded-full">
                  {activity.status}
                </span>
              </div>
            ))}
          </div>
        </motion.div>

        {/* Floating Action Button */}
        <button className="fixed bottom-8 right-8 w-14 h-14 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full shadow-lg shadow-purple-500/30 flex items-center justify-center text-white hover:shadow-xl hover:shadow-purple-500/40 transition-all duration-300 lg:hidden">
          <Plus className="w-6 h-6" />
        </button>
      </main>
    </div>
  );
}
