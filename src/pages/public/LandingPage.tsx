import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { 
  Sparkles, 
  Zap, 
  Shield, 
  TrendingUp, 
  ArrowRight,
  Star,
  Users,
  Code
} from 'lucide-react';

import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { ThemeToggle } from '@/components/ThemeToggle';
import { SEO } from '@/components/SEO';

export default function LandingPage() {
  return (
    <>
      <SEO
        title="SmartSpec Pro - AI-Powered LLM Gateway"
        description="The most advanced LLM gateway platform for developers. Manage multiple AI providers, track usage, and optimize costs with SmartSpec Pro."
        keywords="LLM gateway, AI platform, OpenAI, Claude, GPT-4, API management"
      />

      <div className="min-h-screen bg-gradient-to-br from-background via-background to-primary/5">
        {/* Header */}
        <header className="fixed top-0 left-0 right-0 z-50 backdrop-blur-xl bg-background/80 border-b border-border/50">
          <nav className="container mx-auto px-4 py-4">
            <div className="flex items-center justify-between">
              <Link to="/" className="flex items-center space-x-2 group">
                <div className="relative">
                  <div className="absolute inset-0 bg-primary/20 blur-xl rounded-full group-hover:bg-primary/30 transition-all" />
                  <Sparkles className="h-8 w-8 text-primary relative" />
                </div>
                <span className="text-2xl font-bold bg-gradient-to-r from-primary to-primary/60 bg-clip-text text-transparent">
                  SmartSpec Pro
                </span>
              </Link>

              <div className="hidden md:flex items-center space-x-8">
                <Link to="/features" className="text-muted-foreground hover:text-foreground transition-colors">
                  Features
                </Link>
                <Link to="/pricing" className="text-muted-foreground hover:text-foreground transition-colors">
                  Pricing
                </Link>
                <a href="https://docs.smartspecpro.com" className="text-muted-foreground hover:text-foreground transition-colors">
                  Docs
                </a>
              </div>

              <div className="flex items-center space-x-4">
                <ThemeToggle />
                <Link to="/login">
                  <Button variant="ghost" className="hidden md:inline-flex">
                    Sign In
                  </Button>
                </Link>
                <Link to="/register">
                  <Button className="rounded-full">
                    Get Started
                    <ArrowRight className="ml-2 h-4 w-4" />
                  </Button>
                </Link>
              </div>
            </div>
          </nav>
        </header>

        {/* Hero Section */}
        <section className="pt-32 pb-20 px-4">
          <div className="container mx-auto">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
              className="text-center max-w-4xl mx-auto"
            >
              {/* Badge */}
              <motion.div
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: 0.2 }}
                className="inline-flex items-center space-x-2 bg-primary/10 backdrop-blur-sm border border-primary/20 rounded-full px-4 py-2 mb-8"
              >
                <Star className="h-4 w-4 text-primary fill-primary" />
                <span className="text-sm font-medium">Trusted by 10,000+ developers</span>
              </motion.div>

              {/* Heading */}
              <motion.h1
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.3 }}
                className="text-5xl md:text-7xl font-bold mb-6 leading-tight"
              >
                <span className="bg-gradient-to-r from-foreground via-foreground to-primary bg-clip-text text-transparent">
                  The Future of
                </span>
                <br />
                <span className="bg-gradient-to-r from-primary via-primary to-primary/60 bg-clip-text text-transparent">
                  LLM Gateway
                </span>
              </motion.h1>

              {/* Description */}
              <motion.p
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.4 }}
                className="text-xl md:text-2xl text-muted-foreground mb-10 leading-relaxed"
              >
                Manage multiple AI providers, track usage, and optimize costs
                <br className="hidden md:block" />
                with the most advanced LLM gateway platform.
              </motion.p>

              {/* CTA Buttons */}
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.5 }}
                className="flex flex-col sm:flex-row items-center justify-center gap-4"
              >
                <Link to="/register">
                  <Button size="lg" className="rounded-full px-8 text-lg h-14 shadow-lg shadow-primary/25 hover:shadow-xl hover:shadow-primary/30 transition-all">
                    Start Free Trial
                    <ArrowRight className="ml-2 h-5 w-5" />
                  </Button>
                </Link>
                <Link to="/features">
                  <Button size="lg" variant="outline" className="rounded-full px-8 text-lg h-14 backdrop-blur-sm">
                    Explore Features
                  </Button>
                </Link>
              </motion.div>

              {/* Stats */}
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.6 }}
                className="grid grid-cols-3 gap-8 mt-16 max-w-2xl mx-auto"
              >
                <div className="text-center">
                  <div className="text-3xl font-bold text-primary mb-1">99.9%</div>
                  <div className="text-sm text-muted-foreground">Uptime</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-primary mb-1">10M+</div>
                  <div className="text-sm text-muted-foreground">API Calls/Day</div>
                </div>
                <div className="text-center">
                  <div className="text-3xl font-bold text-primary mb-1">&lt;50ms</div>
                  <div className="text-sm text-muted-foreground">Latency</div>
                </div>
              </motion.div>
            </motion.div>

            {/* Hero Image/Dashboard Preview */}
            <motion.div
              initial={{ opacity: 0, y: 40 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.7, duration: 0.8 }}
              className="mt-20 max-w-6xl mx-auto"
            >
              <div className="relative">
                {/* Glow Effect */}
                <div className="absolute inset-0 bg-gradient-to-r from-primary/20 via-primary/30 to-primary/20 blur-3xl opacity-50" />
                
                {/* Dashboard Preview Card */}
                <Card className="relative backdrop-blur-xl bg-card/50 border-2 border-primary/20 shadow-2xl rounded-3xl overflow-hidden">
                  <CardContent className="p-8">
                    <div className="aspect-video bg-gradient-to-br from-primary/10 via-background to-primary/5 rounded-2xl flex items-center justify-center">
                      <div className="text-center">
                        <Code className="h-20 w-20 text-primary/40 mx-auto mb-4" />
                        <p className="text-muted-foreground">Dashboard Preview</p>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </div>
            </motion.div>
          </div>
        </section>

        {/* Features Section */}
        <section className="py-20 px-4">
          <div className="container mx-auto">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6 }}
              className="text-center mb-16"
            >
              <h2 className="text-4xl md:text-5xl font-bold mb-4">
                Why Choose <span className="text-primary">SmartSpec Pro</span>
              </h2>
              <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
                Everything you need to build, deploy, and scale AI-powered applications
              </p>
            </motion.div>

            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
              {[
                {
                  icon: Zap,
                  title: 'Lightning Fast',
                  description: 'Sub-50ms latency with global edge network',
                  color: 'text-yellow-500',
                  bgColor: 'bg-yellow-500/10',
                },
                {
                  icon: Shield,
                  title: 'Enterprise Security',
                  description: 'SOC 2 compliant with end-to-end encryption',
                  color: 'text-blue-500',
                  bgColor: 'bg-blue-500/10',
                },
                {
                  icon: TrendingUp,
                  title: 'Cost Optimization',
                  description: 'Save up to 40% with intelligent routing',
                  color: 'text-green-500',
                  bgColor: 'bg-green-500/10',
                },
                {
                  icon: Users,
                  title: 'Team Collaboration',
                  description: 'Built for teams with role-based access',
                  color: 'text-purple-500',
                  bgColor: 'bg-purple-500/10',
                },
              ].map((feature, index) => (
                <motion.div
                  key={feature.title}
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ delay: index * 0.1 }}
                >
                  <Card className="h-full backdrop-blur-xl bg-card/50 border-border/50 hover:border-primary/50 transition-all duration-300 hover:shadow-lg hover:shadow-primary/10 rounded-2xl">
                    <CardContent className="p-6">
                      <div className={`${feature.bgColor} ${feature.color} w-14 h-14 rounded-2xl flex items-center justify-center mb-4`}>
                        <feature.icon className="h-7 w-7" />
                      </div>
                      <h3 className="text-xl font-semibold mb-2">{feature.title}</h3>
                      <p className="text-muted-foreground">{feature.description}</p>
                    </CardContent>
                  </Card>
                </motion.div>
              ))}
            </div>
          </div>
        </section>

        {/* CTA Section */}
        <section className="py-20 px-4">
          <div className="container mx-auto">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              className="relative"
            >
              <div className="absolute inset-0 bg-gradient-to-r from-primary/20 via-primary/30 to-primary/20 blur-3xl opacity-50" />
              
              <Card className="relative backdrop-blur-xl bg-gradient-to-br from-primary/10 via-card/50 to-primary/5 border-2 border-primary/20 rounded-3xl overflow-hidden">
                <CardContent className="p-12 md:p-16 text-center">
                  <h2 className="text-4xl md:text-5xl font-bold mb-6">
                    Ready to Get Started?
                  </h2>
                  <p className="text-xl text-muted-foreground mb-8 max-w-2xl mx-auto">
                    Join thousands of developers building the future with SmartSpec Pro
                  </p>
                  <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
                    <Link to="/register">
                      <Button size="lg" className="rounded-full px-8 text-lg h-14 shadow-lg shadow-primary/25">
                        Start Free Trial
                        <ArrowRight className="ml-2 h-5 w-5" />
                      </Button>
                    </Link>
                    <Link to="/pricing">
                      <Button size="lg" variant="outline" className="rounded-full px-8 text-lg h-14 backdrop-blur-sm">
                        View Pricing
                      </Button>
                    </Link>
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          </div>
        </section>

        {/* Footer */}
        <footer className="border-t border-border/50 py-12 px-4">
          <div className="container mx-auto">
            <div className="grid md:grid-cols-4 gap-8 mb-8">
              <div>
                <Link to="/" className="flex items-center space-x-2 mb-4">
                  <Sparkles className="h-6 w-6 text-primary" />
                  <span className="text-lg font-bold">SmartSpec Pro</span>
                </Link>
                <p className="text-sm text-muted-foreground">
                  The most advanced LLM gateway platform for developers.
                </p>
              </div>

              <div>
                <h3 className="font-semibold mb-4">Product</h3>
                <ul className="space-y-2 text-sm text-muted-foreground">
                  <li><Link to="/features" className="hover:text-foreground transition-colors">Features</Link></li>
                  <li><Link to="/pricing" className="hover:text-foreground transition-colors">Pricing</Link></li>
                </ul>
              </div>

              <div>
                <h3 className="font-semibold mb-4">Company</h3>
                <ul className="space-y-2 text-sm text-muted-foreground">
                  <li><a href="#" className="hover:text-foreground transition-colors">About</a></li>
                  <li><a href="#" className="hover:text-foreground transition-colors">Contact</a></li>
                </ul>
              </div>

              <div>
                <h3 className="font-semibold mb-4">Legal</h3>
                <ul className="space-y-2 text-sm text-muted-foreground">
                  <li><a href="#" className="hover:text-foreground transition-colors">Privacy</a></li>
                  <li><a href="#" className="hover:text-foreground transition-colors">Terms</a></li>
                </ul>
              </div>
            </div>

            <div className="border-t border-border/50 pt-8 text-center text-sm text-muted-foreground">
              <p>&copy; 2025 SmartSpec Pro. All rights reserved.</p>
            </div>
          </div>
        </footer>
      </div>
    </>
  );
}
