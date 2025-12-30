import { Link } from 'react-router-dom';
import { ArrowRight, Sparkles, Zap, Shield, Code } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { ThemeToggle } from '@/components/ThemeToggle';
import { SEO } from '@/components/SEO';
import {
  FadeIn,
  SlideInLeft,
  SlideInRight,
  StaggerContainer,
  StaggerItem,
  HoverScale,
} from '@/components/Motion';

export default function LandingPage() {
  return (
    <>
      <SEO
        title="SmartSpec Pro - AI-Native Development Framework"
        description="Build production-grade SaaS applications with AI. SmartSpec Pro generates complete, production-ready applications from natural language."
        keywords="smartspec, ai development, code generation, saas builder, llm gateway"
      />

      <div className="min-h-screen bg-gradient-to-b from-background to-muted/20">
        {/* Navigation */}
        <nav className="border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
          <div className="container mx-auto px-4 py-4">
            <div className="flex items-center justify-between">
              <FadeIn>
                <div className="flex items-center space-x-2">
                  <Sparkles className="h-6 w-6 text-primary" />
                  <span className="text-xl font-bold">SmartSpec Pro</span>
                </div>
              </FadeIn>

              <FadeIn delay={0.1}>
                <div className="flex items-center space-x-4">
                  <Link to="/features">
                    <Button variant="ghost">Features</Button>
                  </Link>
                  <Link to="/pricing">
                    <Button variant="ghost">Pricing</Button>
                  </Link>
                  <ThemeToggle />
                  <Link to="/login">
                    <Button variant="outline">Sign In</Button>
                  </Link>
                  <Link to="/register">
                    <Button>Get Started</Button>
                  </Link>
                </div>
              </FadeIn>
            </div>
          </div>
        </nav>

        {/* Hero Section */}
        <section className="container mx-auto px-4 py-20">
          <div className="text-center space-y-8">
            <FadeIn delay={0.2}>
              <Badge variant="secondary" className="mb-4">
                <Sparkles className="h-3 w-3 mr-1" />
                AI-Powered Development
              </Badge>
            </FadeIn>

            <FadeIn delay={0.3}>
              <h1 className="text-5xl md:text-7xl font-bold tracking-tight">
                Build Production-Grade
                <br />
                <span className="text-primary">SaaS in Minutes</span>
              </h1>
            </FadeIn>

            <FadeIn delay={0.4}>
              <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
                SmartSpec Pro generates complete, production-ready applications from natural
                language. Powered by advanced LLM Gateway with 5+ providers.
              </p>
            </FadeIn>

            <FadeIn delay={0.5}>
              <div className="flex items-center justify-center space-x-4">
                <Link to="/register">
                  <HoverScale>
                    <Button size="lg" className="text-lg">
                      Start Building
                      <ArrowRight className="ml-2 h-5 w-5" />
                    </Button>
                  </HoverScale>
                </Link>
                <Link to="/features">
                  <HoverScale>
                    <Button size="lg" variant="outline" className="text-lg">
                      Learn More
                    </Button>
                  </HoverScale>
                </Link>
              </div>
            </FadeIn>

            <FadeIn delay={0.6}>
              <div className="mt-12 flex items-center justify-center space-x-8 text-sm text-muted-foreground">
                <div className="flex items-center">
                  <Zap className="h-4 w-4 mr-2 text-primary" />
                  <span>83% Cost Savings</span>
                </div>
                <div className="flex items-center">
                  <Shield className="h-4 w-4 mr-2 text-primary" />
                  <span>Production-Grade</span>
                </div>
                <div className="flex items-center">
                  <Code className="h-4 w-4 mr-2 text-primary" />
                  <span>5+ LLM Providers</span>
                </div>
              </div>
            </FadeIn>
          </div>
        </section>

        {/* Features Section */}
        <section className="container mx-auto px-4 py-20">
          <div className="text-center mb-12">
            <SlideInLeft>
              <h2 className="text-4xl font-bold mb-4">Powerful Features</h2>
              <p className="text-xl text-muted-foreground">
                Everything you need to build modern applications
              </p>
            </SlideInLeft>
          </div>

          <StaggerContainer className="grid md:grid-cols-3 gap-6">
            <StaggerItem>
              <HoverScale>
                <Card className="h-full">
                  <CardHeader>
                    <Sparkles className="h-10 w-10 text-primary mb-2" />
                    <CardTitle>AI Code Generation</CardTitle>
                    <CardDescription>
                      Generate complete applications from natural language descriptions
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <ul className="space-y-2 text-sm text-muted-foreground">
                      <li>• Multi-framework support</li>
                      <li>• Production-ready code</li>
                      <li>• Best practices built-in</li>
                    </ul>
                  </CardContent>
                </Card>
              </HoverScale>
            </StaggerItem>

            <StaggerItem>
              <HoverScale>
                <Card className="h-full">
                  <CardHeader>
                    <Zap className="h-10 w-10 text-primary mb-2" />
                    <CardTitle>LLM Gateway</CardTitle>
                    <CardDescription>
                      Smart routing across 5+ LLM providers for optimal cost and performance
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <ul className="space-y-2 text-sm text-muted-foreground">
                      <li>• Auto provider selection</li>
                      <li>• 83% cost savings</li>
                      <li>• Real-time usage tracking</li>
                    </ul>
                  </CardContent>
                </Card>
              </HoverScale>
            </StaggerItem>

            <StaggerItem>
              <HoverScale>
                <Card className="h-full">
                  <CardHeader>
                    <Shield className="h-10 w-10 text-primary mb-2" />
                    <CardTitle>Credit System</CardTitle>
                    <CardDescription>
                      Pay-as-you-go pricing with transparent credit management
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <ul className="space-y-2 text-sm text-muted-foreground">
                      <li>• No subscriptions</li>
                      <li>• Transparent pricing</li>
                      <li>• Real-time balance</li>
                    </ul>
                  </CardContent>
                </Card>
              </HoverScale>
            </StaggerItem>
          </StaggerContainer>
        </section>

        {/* CTA Section */}
        <section className="container mx-auto px-4 py-20">
          <SlideInRight>
            <Card className="bg-primary text-primary-foreground">
              <CardHeader className="text-center">
                <CardTitle className="text-3xl mb-4">Ready to Build?</CardTitle>
                <CardDescription className="text-primary-foreground/80 text-lg">
                  Start building production-grade applications with AI today
                </CardDescription>
              </CardHeader>
              <CardContent className="flex justify-center">
                <Link to="/register">
                  <HoverScale>
                    <Button size="lg" variant="secondary" className="text-lg">
                      Get Started for Free
                      <ArrowRight className="ml-2 h-5 w-5" />
                    </Button>
                  </HoverScale>
                </Link>
              </CardContent>
            </Card>
          </SlideInRight>
        </section>

        {/* Footer */}
        <footer className="border-t bg-background/95 backdrop-blur">
          <div className="container mx-auto px-4 py-8">
            <div className="text-center text-sm text-muted-foreground">
              <p>© 2025 SmartSpec Pro. All rights reserved.</p>
            </div>
          </div>
        </footer>
      </div>
    </>
  );
}
