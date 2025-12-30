import { Link } from 'react-router-dom';
import { Sparkles, ArrowRight, Check } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { ThemeToggle } from '@/components/ThemeToggle';
import { SEO } from '@/components/SEO';

export default function PricingPage() {
  const plans = [
    {
      name: 'Free',
      price: '$0',
      desc: 'Perfect for trying out',
      features: ['10,000 requests/month', 'Basic analytics', 'Community support', '1 API key'],
      cta: 'Get Started',
      popular: false,
    },
    {
      name: 'Pro',
      price: '$49',
      desc: 'For growing teams',
      features: ['1M requests/month', 'Advanced analytics', 'Priority support', 'Unlimited API keys', 'Team collaboration'],
      cta: 'Start Free Trial',
      popular: true,
    },
    {
      name: 'Enterprise',
      price: 'Custom',
      desc: 'For large organizations',
      features: ['Unlimited requests', 'Custom analytics', 'Dedicated support', 'SLA guarantee', 'Custom integrations'],
      cta: 'Contact Sales',
      popular: false,
    },
  ];

  return (
    <>
      <SEO title="Pricing - SmartSpec Pro" description="Simple, transparent pricing" />
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
            <h1 className="text-5xl md:text-6xl font-bold mb-6">Simple, <span className="text-primary">Transparent Pricing</span></h1>
            <p className="text-xl text-muted-foreground">Choose the plan that fits your needs</p>
          </div>
        </section>

        <section className="pb-20 px-4">
          <div className="container mx-auto grid md:grid-cols-3 gap-6 max-w-6xl">
            {plans.map((plan) => (
              <Card key={plan.name} className={`backdrop-blur-xl bg-card/50 rounded-3xl ${plan.popular ? 'border-2 border-primary shadow-lg shadow-primary/20' : 'border-border/50'}`}>
                <CardContent className="p-8">
                  {plan.popular && (
                    <div className="bg-primary/10 text-primary text-sm font-medium px-3 py-1 rounded-full inline-block mb-4">
                      Most Popular
                    </div>
                  )}
                  <h3 className="text-2xl font-bold mb-2">{plan.name}</h3>
                  <div className="text-4xl font-bold mb-2">{plan.price}<span className="text-lg text-muted-foreground">/mo</span></div>
                  <p className="text-muted-foreground mb-6">{plan.desc}</p>
                  <Link to="/register">
                    <Button className={`w-full rounded-full ${plan.popular ? '' : 'variant-outline'}`}>
                      {plan.cta}
                    </Button>
                  </Link>
                  <ul className="mt-6 space-y-3">
                    {plan.features.map((f) => (
                      <li key={f} className="flex items-start">
                        <Check className="h-5 w-5 text-primary mr-2 flex-shrink-0 mt-0.5" />
                        <span>{f}</span>
                      </li>
                    ))}
                  </ul>
                </CardContent>
              </Card>
            ))}
          </div>
        </section>
      </div>
    </>
  );
}
