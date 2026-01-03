/**
 * Documentation Page
 * Design: Ethereal Gradient Flow
 * Features: Getting started guide, API reference, tutorials
 */

import { useState } from 'react';
import { motion } from 'framer-motion';
import { Link } from 'wouter';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Navbar } from '@/components/Navbar';
import { Footer } from '@/components/Footer';
import {
  Book,
  Code2,
  Rocket,
  Search,
  FileText,
  Video,
  MessageSquare,
  ArrowRight,
  ChevronRight,
  Terminal,
  Zap,
  Shield,
  Database,
  ExternalLink
} from 'lucide-react';

const quickLinks = [
  {
    icon: Rocket,
    title: 'Getting Started',
    description: 'Set up your account and create your first project in minutes.',
    href: '/docs/getting-started',
    color: 'from-violet-500 to-purple-500'
  },
  {
    icon: Code2,
    title: 'API Reference',
    description: 'Complete API documentation with examples and code snippets.',
    href: '/docs/api',
    color: 'from-teal-500 to-emerald-500'
  },
  {
    icon: FileText,
    title: 'Tutorials',
    description: 'Step-by-step guides for common use cases and workflows.',
    href: '/docs/tutorials',
    color: 'from-orange-500 to-amber-500'
  },
  {
    icon: Video,
    title: 'Video Guides',
    description: 'Watch video tutorials to learn SmartSpec Pro visually.',
    href: '/docs/videos',
    color: 'from-pink-500 to-rose-500'
  }
];

const docSections = [
  {
    title: 'Fundamentals',
    items: [
      { title: 'Introduction', href: '/docs/intro' },
      { title: 'Quick Start', href: '/docs/quickstart' },
      { title: 'Core Concepts', href: '/docs/concepts' },
      { title: 'Authentication', href: '/docs/auth' },
    ]
  },
  {
    title: 'AI Features',
    items: [
      { title: 'Code Generation', href: '/docs/code-generation' },
      { title: 'Image Generation', href: '/docs/image-generation' },
      { title: 'Video Generation', href: '/docs/video-generation' },
      { title: 'Audio & Speech', href: '/docs/audio' },
    ]
  },
  {
    title: 'Integration',
    items: [
      { title: 'REST API', href: '/docs/api/rest' },
      { title: 'Python SDK', href: '/docs/sdk/python' },
      { title: 'JavaScript SDK', href: '/docs/sdk/javascript' },
      { title: 'Webhooks', href: '/docs/webhooks' },
    ]
  },
  {
    title: 'Security',
    items: [
      { title: 'API Keys', href: '/docs/security/api-keys' },
      { title: 'MFA Setup', href: '/docs/security/mfa' },
      { title: 'Audit Logs', href: '/docs/security/audit' },
      { title: 'Best Practices', href: '/docs/security/best-practices' },
    ]
  }
];

const codeExample = `import smartspec from '@smartspec/sdk';

// Initialize the client
const client = new smartspec.Client({
  apiKey: process.env.SMARTSPEC_API_KEY
});

// Generate code from natural language
const result = await client.generate({
  prompt: "Create a REST API for user authentication",
  language: "typescript",
  framework: "express"
});

console.log(result.code);`;

const popularArticles = [
  {
    icon: Terminal,
    title: 'CLI Installation Guide',
    description: 'Install and configure the SmartSpec CLI tool',
    readTime: '5 min'
  },
  {
    icon: Zap,
    title: 'Optimizing Credit Usage',
    description: 'Tips to get the most out of your credits',
    readTime: '8 min'
  },
  {
    icon: Shield,
    title: 'Security Best Practices',
    description: 'Keep your API keys and data secure',
    readTime: '10 min'
  },
  {
    icon: Database,
    title: 'Database Integration',
    description: 'Connect SmartSpec to your database',
    readTime: '12 min'
  }
];

export default function Docs() {
  const [searchQuery, setSearchQuery] = useState('');

  return (
    <div className="min-h-screen bg-background">
      <Navbar />
      
      {/* Hero Section */}
      <section className="relative pt-32 pb-16 overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-b from-violet-500/5 via-transparent to-transparent" />
        <div className="absolute top-20 left-1/4 w-96 h-96 bg-violet-500/10 rounded-full blur-3xl" />
        <div className="absolute top-40 right-1/4 w-96 h-96 bg-teal-500/10 rounded-full blur-3xl" />
        
        <div className="container relative mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-center max-w-3xl mx-auto"
          >
            <span className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-primary/10 text-primary text-sm font-medium mb-4">
              <Book className="w-4 h-4" />
              Documentation
            </span>
            <h1 className="text-4xl sm:text-5xl md:text-6xl font-bold mb-6">
              Learn <span className="gradient-text">SmartSpec Pro</span>
            </h1>
            <p className="text-lg text-muted-foreground mb-8">
              Everything you need to build amazing applications with AI-powered code generation.
            </p>
            
            {/* Search Bar */}
            <div className="relative max-w-xl mx-auto">
              <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-muted-foreground" />
              <Input
                type="search"
                placeholder="Search documentation..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-12 pr-4 py-6 text-lg bg-background/50 backdrop-blur-sm border-border/50"
              />
            </div>
          </motion.div>
        </div>
      </section>

      {/* Quick Links */}
      <section className="py-16">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {quickLinks.map((link, index) => (
              <motion.div
                key={link.title}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
              >
                <Card className="glass-card h-full hover:shadow-xl transition-all duration-300 group cursor-pointer">
                  <CardContent className="p-6">
                    <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${link.color} flex items-center justify-center mb-4`}>
                      <link.icon className="w-6 h-6 text-white" />
                    </div>
                    <h3 className="text-lg font-semibold mb-2 group-hover:text-primary transition-colors">
                      {link.title}
                    </h3>
                    <p className="text-sm text-muted-foreground mb-4">{link.description}</p>
                    <span className="inline-flex items-center text-sm text-primary font-medium">
                      Learn more
                      <ArrowRight className="ml-1 w-4 h-4 group-hover:translate-x-1 transition-transform" />
                    </span>
                  </CardContent>
                </Card>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Code Example */}
      <section className="py-16 bg-muted/30">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
            >
              <h2 className="text-3xl font-bold mb-4">
                Simple, Powerful <span className="gradient-text">API</span>
              </h2>
              <p className="text-lg text-muted-foreground mb-6">
                Get started with just a few lines of code. Our SDK handles authentication, 
                rate limiting, and error handling automatically.
              </p>
              <div className="space-y-4">
                <div className="flex items-center gap-3">
                  <div className="w-8 h-8 rounded-full bg-green-100 flex items-center justify-center">
                    <span className="text-green-600 font-bold text-sm">1</span>
                  </div>
                  <span>Install the SDK</span>
                </div>
                <div className="flex items-center gap-3">
                  <div className="w-8 h-8 rounded-full bg-green-100 flex items-center justify-center">
                    <span className="text-green-600 font-bold text-sm">2</span>
                  </div>
                  <span>Initialize with your API key</span>
                </div>
                <div className="flex items-center gap-3">
                  <div className="w-8 h-8 rounded-full bg-green-100 flex items-center justify-center">
                    <span className="text-green-600 font-bold text-sm">3</span>
                  </div>
                  <span>Start generating code</span>
                </div>
              </div>
              <Button className="mt-8 bg-gradient-to-r from-violet-500 to-teal-400 text-white">
                View Full API Reference
                <ExternalLink className="ml-2 w-4 h-4" />
              </Button>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, x: 20 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
            >
              <div className="glass-card rounded-xl overflow-hidden">
                <div className="flex items-center gap-2 px-4 py-3 bg-muted/50 border-b border-border/50">
                  <div className="w-3 h-3 rounded-full bg-red-400" />
                  <div className="w-3 h-3 rounded-full bg-yellow-400" />
                  <div className="w-3 h-3 rounded-full bg-green-400" />
                  <span className="ml-2 text-xs text-muted-foreground">example.ts</span>
                </div>
                <pre className="p-4 overflow-x-auto text-sm">
                  <code className="text-foreground font-mono">{codeExample}</code>
                </pre>
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Documentation Sections */}
      <section className="py-16">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-12"
          >
            <h2 className="text-3xl font-bold mb-4">Browse by Category</h2>
            <p className="text-muted-foreground">
              Find what you need in our comprehensive documentation
            </p>
          </motion.div>

          <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-8">
            {docSections.map((section, index) => (
              <motion.div
                key={section.title}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
              >
                <h3 className="font-semibold mb-4 text-lg">{section.title}</h3>
                <ul className="space-y-2">
                  {section.items.map((item) => (
                    <li key={item.title}>
                      <Link href={item.href}>
                        <span className="flex items-center text-muted-foreground hover:text-foreground transition-colors cursor-pointer group">
                          <ChevronRight className="w-4 h-4 mr-1 group-hover:translate-x-1 transition-transform" />
                          {item.title}
                        </span>
                      </Link>
                    </li>
                  ))}
                </ul>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Popular Articles */}
      <section className="py-16 bg-muted/30">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-12"
          >
            <h2 className="text-3xl font-bold mb-4">Popular Articles</h2>
            <p className="text-muted-foreground">
              Most read guides and tutorials
            </p>
          </motion.div>

          <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {popularArticles.map((article, index) => (
              <motion.div
                key={article.title}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
              >
                <Card className="glass-card h-full hover:shadow-lg transition-shadow cursor-pointer group">
                  <CardContent className="p-6">
                    <div className="w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center mb-4">
                      <article.icon className="w-5 h-5 text-primary" />
                    </div>
                    <h3 className="font-semibold mb-2 group-hover:text-primary transition-colors">
                      {article.title}
                    </h3>
                    <p className="text-sm text-muted-foreground mb-3">{article.description}</p>
                    <span className="text-xs text-muted-foreground">{article.readTime} read</span>
                  </CardContent>
                </Card>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Support CTA */}
      <section className="py-16">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="glass-card rounded-2xl p-8 sm:p-12 text-center max-w-4xl mx-auto"
          >
            <MessageSquare className="w-16 h-16 mx-auto mb-6 text-primary" />
            <h2 className="text-3xl font-bold mb-4">Need Help?</h2>
            <p className="text-lg text-muted-foreground mb-8 max-w-2xl mx-auto">
              Can't find what you're looking for? Our support team is here to help.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button size="lg" className="bg-gradient-to-r from-violet-500 to-teal-400 text-white">
                Contact Support
              </Button>
              <Button size="lg" variant="outline">
                Join Community
              </Button>
            </div>
          </motion.div>
        </div>
      </section>

      <Footer />
    </div>
  );
}
