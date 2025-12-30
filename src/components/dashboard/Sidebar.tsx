import { Link, useLocation } from 'react-router-dom';
import { motion } from 'framer-motion';
import {
  LayoutDashboard,
  Wallet,
  Zap,
  BarChart3,
  Settings,
  CreditCard,
  Key,
  Users,
  ChevronLeft,
  Sparkles,
  Activity,
  Database
} from 'lucide-react';
import { cn } from '@/lib/utils';
import { Button } from '@/components/ui/button';

interface SidebarProps {
  collapsed: boolean;
  onToggle: () => void;
}

export function Sidebar({ collapsed, onToggle }: SidebarProps) {
  const location = useLocation();

  const menuItems = [
    {
      title: 'Dashboard',
      icon: LayoutDashboard,
      href: '/dashboard',
      badge: null,
    },
    {
      title: 'LLM Gateway',
      icon: Zap,
      href: '/dashboard/llm-gateway',
      badge: 'New',
    },
    {
      title: 'Usage & Analytics',
      icon: BarChart3,
      href: '/dashboard/analytics',
      badge: null,
    },
    {
      title: 'Credits',
      icon: Wallet,
      href: '/dashboard/credits',
      badge: null,
    },
    {
      title: 'Payments',
      icon: CreditCard,
      href: '/dashboard/payments',
      badge: null,
    },
    {
      title: 'API Keys',
      icon: Key,
      href: '/dashboard/api-keys',
      badge: null,
    },
    {
      title: 'Monitoring',
      icon: Activity,
      href: '/dashboard/monitoring',
      badge: null,
    },
    {
      title: 'Logs',
      icon: Database,
      href: '/dashboard/logs',
      badge: null,
    },
    {
      title: 'Settings',
      icon: Settings,
      href: '/dashboard/settings',
      badge: null,
    },
  ];

  const adminItems = [
    {
      title: 'Admin Panel',
      icon: Users,
      href: '/dashboard/admin',
      badge: 'Admin',
    },
  ];

  const isActive = (href: string) => {
    if (href === '/dashboard') {
      return location.pathname === '/dashboard';
    }
    return location.pathname.startsWith(href);
  };

  return (
    <motion.aside
      initial={false}
      animate={{ width: collapsed ? 80 : 280 }}
      transition={{ duration: 0.3, ease: 'easeInOut' }}
      className="fixed left-0 top-0 h-screen bg-card/50 backdrop-blur-xl border-r border-border/50 z-40 flex flex-col"
    >
      {/* Header */}
      <div className="h-16 flex items-center justify-between px-4 border-b border-border/50">
        {!collapsed && (
          <Link to="/dashboard" className="flex items-center space-x-2">
            <div className="relative">
              <div className="absolute inset-0 bg-primary/20 blur-lg rounded-full" />
              <Sparkles className="h-6 w-6 text-primary relative" />
            </div>
            <span className="font-bold text-lg">SmartSpec Pro</span>
          </Link>
        )}
        {collapsed && (
          <Link to="/dashboard" className="flex items-center justify-center w-full">
            <Sparkles className="h-6 w-6 text-primary" />
          </Link>
        )}
      </div>

      {/* Toggle Button */}
      <Button
        variant="ghost"
        size="icon"
        onClick={onToggle}
        className="absolute -right-3 top-20 h-6 w-6 rounded-full border border-border/50 bg-background shadow-md hover:bg-muted z-50"
      >
        <ChevronLeft
          className={cn(
            'h-4 w-4 transition-transform',
            collapsed && 'rotate-180'
          )}
        />
      </Button>

      {/* Navigation */}
      <nav className="flex-1 overflow-y-auto py-4 px-2 space-y-1">
        {menuItems.map((item) => {
          const Icon = item.icon;
          const active = isActive(item.href);

          return (
            <Link key={item.href} to={item.href}>
              <motion.div
                whileHover={{ x: 4 }}
                className={cn(
                  'flex items-center space-x-3 px-3 py-2.5 rounded-xl transition-colors relative',
                  active
                    ? 'bg-primary/10 text-primary'
                    : 'text-muted-foreground hover:bg-muted hover:text-foreground'
                )}
              >
                {active && (
                  <motion.div
                    layoutId="sidebar-indicator"
                    className="absolute left-0 top-0 bottom-0 w-1 bg-primary rounded-r-full"
                    transition={{ type: 'spring', stiffness: 300, damping: 30 }}
                  />
                )}
                <Icon className="h-5 w-5 flex-shrink-0" />
                {!collapsed && (
                  <>
                    <span className="flex-1 font-medium">{item.title}</span>
                    {item.badge && (
                      <span className="px-2 py-0.5 text-xs font-medium bg-primary/20 text-primary rounded-full">
                        {item.badge}
                      </span>
                    )}
                  </>
                )}
              </motion.div>
            </Link>
          );
        })}

        {/* Admin Section */}
        <div className="pt-4 mt-4 border-t border-border/50">
          {adminItems.map((item) => {
            const Icon = item.icon;
            const active = isActive(item.href);

            return (
              <Link key={item.href} to={item.href}>
                <motion.div
                  whileHover={{ x: 4 }}
                  className={cn(
                    'flex items-center space-x-3 px-3 py-2.5 rounded-xl transition-colors',
                    active
                      ? 'bg-primary/10 text-primary'
                      : 'text-muted-foreground hover:bg-muted hover:text-foreground'
                  )}
                >
                  <Icon className="h-5 w-5 flex-shrink-0" />
                  {!collapsed && (
                    <>
                      <span className="flex-1 font-medium">{item.title}</span>
                      {item.badge && (
                        <span className="px-2 py-0.5 text-xs font-medium bg-orange-500/20 text-orange-500 rounded-full">
                          {item.badge}
                        </span>
                      )}
                    </>
                  )}
                </motion.div>
              </Link>
            );
          })}
        </div>
      </nav>

      {/* Footer */}
      {!collapsed && (
        <div className="p-4 border-t border-border/50">
          <div className="bg-gradient-to-br from-primary/10 to-primary/5 rounded-xl p-4">
            <h4 className="font-semibold text-sm mb-1">Need Help?</h4>
            <p className="text-xs text-muted-foreground mb-3">
              Check our documentation
            </p>
            <Button size="sm" variant="outline" className="w-full rounded-lg">
              View Docs
            </Button>
          </div>
        </div>
      )}
    </motion.aside>
  );
}
