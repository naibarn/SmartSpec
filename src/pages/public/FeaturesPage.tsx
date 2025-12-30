import { Link } from 'react-router-dom';
import { Sparkles, ArrowRight, Zap, Shield, TrendingUp, Users, Code, BarChart } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { ThemeToggle } from '@/components/ThemeToggle';
import { SEO } from '@/components/SEO';

export default function FeaturesPage() {
  const features = [
    { icon: Zap, title: 'Lightning Fast', desc: 'Sub-50ms latency', color: 'text-yellow-500', bg: 'bg-yellow-500/10' },
    { icon: Shield, title: 'Enterprise Security', desc: 'SOC 2 compliant', color: 'text-blue-500', bg: 'bg-blue-500/10' },
    { icon: TrendingUp, title: 'Cost Optimization', desc: 'Save up to 40%', color: 'text-green-500', bg: 'bg-green-500/10' },
    { icon: Users, title: 'Team Collaboration', desc: 'Role-based access', color: 'text-purple-500', bg: 'bg-purple-500/10' },
    { icon: Code, title: 'Developer Experience', desc: 'Simple REST API', color: 'text-pink-500', bg: 'bg-pink-500/10' },
    { icon: BarChart, title: 'Advanced Analytics', desc: 'Real-time tracking', color: 'text-orange-500', bg: 'bg-orange-500/10' },
  ];

  return (
    <>
      <SEO title="Features - SmartSpec Pro" description="Explore SmartSpec Pro features" />
      <div className="min-h-screen bg-gradient-to-br from-background via-background to-primary/5">
        <header className="fixed top-0 left-0 right-0 z-50 backdrop-blur-xl bg-background/80 border-b border-border/50">
          <nav className="container mx-auto px-4 py-4 flex items-center justify-between">
            <Link to="/" className="flex items-center space-x-2">
              <Sparkles className="h-8 w-8 text-primary" />
              <span className="text-2xl font-bold">SmartSpec Pro</span>
            </Link>
            <div className="flex items-center space-x-4">
              <ThemeToggle />
              <Link to="/login"><Button variant="ghost">Sign In</Button></Link>
              <Link to="/register"><Button className="rounded-full">Get Started <ArrowRight className="ml-2 h-4 w-4" /></Button></Link>
            </div>
          </nav>
        </header>

        <section className="pt-32 pb-20 px-4">
          <div className="container mx-auto text-center max-w-4xl">
            <h1 className="text-5xl md:text-6xl font-bold mb-6">Powerful <span className="text-primary">Features</span></h1>
            <p className="text-xl text-muted-foreground">Everything you need to build AI applications</p>
          </div>
        </section>

        <section className="pb-20 px-4">
          <div className="container mx-auto grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {features.map((f) => (
              <Card key={f.title} className="backdrop-blur-xl bg-card/50 border-border/50 hover:border-primary/50 transition-all rounded-2xl">
                <CardContent className="p-6">
                  <div className={`${f.bg} ${f.color} w-14 h-14 rounded-2xl flex items-center justify-center mb-4`}>
                    <f.icon className="h-7 w-7" />
                  </div>
                  <h3 className="text-xl font-semibold mb-2">{f.title}</h3>
                  <p className="text-muted-foreground">{f.desc}</p>
                </CardContent>
              </Card>
            ))}
          </div>
        </section>
      </div>
    </>
  );
}
