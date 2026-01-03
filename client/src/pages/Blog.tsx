/**
 * Blog & Changelog Page - SmartSpec Pro
 * Blog posts, updates, and changelog
 */

import { useState } from 'react';
import { motion } from 'framer-motion';
import { Button } from '@/components/ui/button';
import { Navbar } from '@/components/Navbar';
import { Footer } from '@/components/Footer';
import {
  Calendar,
  Clock,
  User,
  Tag,
  ArrowRight,
  Sparkles,
  Zap,
  Shield,
  Rocket,
  ChevronRight,
  BookOpen,
  History,
} from 'lucide-react';

type TabType = 'blog' | 'changelog';

interface BlogPost {
  id: string;
  title: string;
  excerpt: string;
  content: string;
  author: string;
  authorAvatar: string;
  date: string;
  readTime: string;
  category: string;
  tags: string[];
  image: string;
  featured?: boolean;
}

interface ChangelogEntry {
  version: string;
  date: string;
  type: 'major' | 'minor' | 'patch';
  title: string;
  description: string;
  changes: {
    type: 'added' | 'improved' | 'fixed' | 'removed';
    text: string;
  }[];
}

const blogPosts: BlogPost[] = [
  {
    id: '1',
    title: 'Introducing SmartSpec Pro 2.0: The Future of AI-Powered Development',
    excerpt: 'We\'re excited to announce the biggest update to SmartSpec Pro yet, featuring advanced AI models, workflow automation, and enterprise-grade security.',
    content: '',
    author: 'Sarah Chen',
    authorAvatar: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=100&h=100&fit=crop',
    date: 'Jan 2, 2026',
    readTime: '5 min read',
    category: 'Product Update',
    tags: ['AI', 'Product', 'Release'],
    image: 'https://images.unsplash.com/photo-1677442136019-21780ecad995?w=800&h=400&fit=crop',
    featured: true,
  },
  {
    id: '2',
    title: 'Best Practices for AI-Assisted Code Generation',
    excerpt: 'Learn how to write effective prompts and leverage SmartSpec Pro\'s AI capabilities to generate production-ready code.',
    content: '',
    author: 'Michael Park',
    authorAvatar: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=100&h=100&fit=crop',
    date: 'Dec 28, 2025',
    readTime: '8 min read',
    category: 'Tutorial',
    tags: ['Tutorial', 'AI', 'Best Practices'],
    image: 'https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&h=400&fit=crop',
  },
  {
    id: '3',
    title: 'Building Scalable SaaS Applications with SmartSpec Pro',
    excerpt: 'A comprehensive guide to architecting and building scalable SaaS applications using our AI-powered platform.',
    content: '',
    author: 'Emily Rodriguez',
    authorAvatar: 'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=100&h=100&fit=crop',
    date: 'Dec 20, 2025',
    readTime: '12 min read',
    category: 'Guide',
    tags: ['SaaS', 'Architecture', 'Guide'],
    image: 'https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=800&h=400&fit=crop',
  },
  {
    id: '4',
    title: 'Security Best Practices for Generated Code',
    excerpt: 'Understanding how SmartSpec Pro ensures security in generated code and what you can do to maintain best practices.',
    content: '',
    author: 'David Kim',
    authorAvatar: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=100&h=100&fit=crop',
    date: 'Dec 15, 2025',
    readTime: '6 min read',
    category: 'Security',
    tags: ['Security', 'Best Practices'],
    image: 'https://images.unsplash.com/photo-1563986768609-322da13575f3?w=800&h=400&fit=crop',
  },
];

const changelog: ChangelogEntry[] = [
  {
    version: '2.0.0',
    date: 'Jan 2, 2026',
    type: 'major',
    title: 'SmartSpec Pro 2.0',
    description: 'Major release with new AI models, workflow automation, and enterprise features.',
    changes: [
      { type: 'added', text: 'Multi-modal AI generation (Image, Video, Audio)' },
      { type: 'added', text: 'Workflow automation system' },
      { type: 'added', text: 'Enterprise SSO support' },
      { type: 'added', text: 'Advanced analytics dashboard' },
      { type: 'improved', text: 'Code generation accuracy by 40%' },
      { type: 'improved', text: 'Response time reduced by 60%' },
      { type: 'fixed', text: 'Memory leak in long-running sessions' },
    ],
  },
  {
    version: '1.9.5',
    date: 'Dec 20, 2025',
    type: 'patch',
    title: 'Bug Fixes & Performance',
    description: 'Various bug fixes and performance improvements.',
    changes: [
      { type: 'fixed', text: 'Fixed code highlighting in dark mode' },
      { type: 'fixed', text: 'Resolved timeout issues with large projects' },
      { type: 'improved', text: 'Better error messages for API failures' },
    ],
  },
  {
    version: '1.9.0',
    date: 'Dec 10, 2025',
    type: 'minor',
    title: 'New Templates & Integrations',
    description: 'Added new project templates and third-party integrations.',
    changes: [
      { type: 'added', text: 'Next.js 15 project template' },
      { type: 'added', text: 'Stripe payment integration template' },
      { type: 'added', text: 'GitHub Actions CI/CD templates' },
      { type: 'improved', text: 'Template customization options' },
    ],
  },
  {
    version: '1.8.0',
    date: 'Nov 25, 2025',
    type: 'minor',
    title: 'Collaboration Features',
    description: 'New team collaboration and sharing features.',
    changes: [
      { type: 'added', text: 'Real-time collaboration on projects' },
      { type: 'added', text: 'Team workspaces' },
      { type: 'added', text: 'Project sharing and permissions' },
      { type: 'improved', text: 'Comment and feedback system' },
    ],
  },
];

const categories = ['All', 'Product Update', 'Tutorial', 'Guide', 'Security', 'Case Study'];

export default function Blog() {
  const [activeTab, setActiveTab] = useState<TabType>('blog');
  const [selectedCategory, setSelectedCategory] = useState('All');

  const filteredPosts = selectedCategory === 'All'
    ? blogPosts
    : blogPosts.filter(post => post.category === selectedCategory);

  const featuredPost = blogPosts.find(post => post.featured);
  const regularPosts = filteredPosts.filter(post => !post.featured);

  const getChangeTypeColor = (type: string) => {
    switch (type) {
      case 'added': return 'bg-green-100 text-green-700';
      case 'improved': return 'bg-blue-100 text-blue-700';
      case 'fixed': return 'bg-orange-100 text-orange-700';
      case 'removed': return 'bg-red-100 text-red-700';
      default: return 'bg-gray-100 text-gray-700';
    }
  };

  const getVersionColor = (type: string) => {
    switch (type) {
      case 'major': return 'from-purple-500 to-pink-500';
      case 'minor': return 'from-blue-500 to-cyan-500';
      case 'patch': return 'from-gray-400 to-gray-500';
      default: return 'from-gray-400 to-gray-500';
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-purple-50/30 to-pink-50/20">
      <Navbar />

      {/* Hero Section */}
      <section className="pt-32 pb-16 px-4">
        <div className="container max-w-6xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            <span className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/60 backdrop-blur-sm border border-purple-100 text-sm text-purple-600 mb-6">
              <Sparkles className="w-4 h-4" />
              Stay Updated
            </span>
            <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold text-gray-900 mb-6">
              Blog &{' '}
              <span className="bg-gradient-to-r from-purple-600 via-pink-500 to-orange-400 bg-clip-text text-transparent">
                Changelog
              </span>
            </h1>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Latest news, tutorials, and updates from the SmartSpec Pro team.
            </p>
          </motion.div>

          {/* Tab Switcher */}
          <div className="flex justify-center mt-10">
            <div className="inline-flex bg-white/60 backdrop-blur-sm rounded-xl p-1.5 border border-white/50">
              <button
                onClick={() => setActiveTab('blog')}
                className={`flex items-center gap-2 px-6 py-3 rounded-lg font-medium transition-all duration-300 ${
                  activeTab === 'blog'
                    ? 'bg-gradient-to-r from-purple-500 to-pink-500 text-white shadow-lg'
                    : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                <BookOpen className="w-4 h-4" />
                Blog
              </button>
              <button
                onClick={() => setActiveTab('changelog')}
                className={`flex items-center gap-2 px-6 py-3 rounded-lg font-medium transition-all duration-300 ${
                  activeTab === 'changelog'
                    ? 'bg-gradient-to-r from-purple-500 to-pink-500 text-white shadow-lg'
                    : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                <History className="w-4 h-4" />
                Changelog
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Blog Content */}
      {activeTab === 'blog' && (
        <>
          {/* Category Filter */}
          <section className="py-4 px-4">
            <div className="container max-w-6xl mx-auto">
              <div className="flex flex-wrap gap-2 justify-center">
                {categories.map((category) => (
                  <button
                    key={category}
                    onClick={() => setSelectedCategory(category)}
                    className={`px-4 py-2 rounded-full text-sm font-medium transition-all duration-300 ${
                      selectedCategory === category
                        ? 'bg-gradient-to-r from-purple-500 to-pink-500 text-white shadow-md'
                        : 'bg-white/60 text-gray-600 hover:bg-white hover:text-gray-900 border border-white/50'
                    }`}
                  >
                    {category}
                  </button>
                ))}
              </div>
            </div>
          </section>

          {/* Featured Post */}
          {featuredPost && selectedCategory === 'All' && (
            <section className="py-8 px-4">
              <div className="container max-w-6xl mx-auto">
                <motion.article
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="bg-white/70 backdrop-blur-xl rounded-3xl border border-white/50 shadow-xl shadow-purple-500/10 overflow-hidden"
                >
                  <div className="grid md:grid-cols-2 gap-0">
                    <div className="relative h-64 md:h-auto">
                      <img
                        src={featuredPost.image}
                        alt={featuredPost.title}
                        className="absolute inset-0 w-full h-full object-cover"
                      />
                      <div className="absolute top-4 left-4">
                        <span className="px-3 py-1 bg-gradient-to-r from-purple-500 to-pink-500 text-white text-xs font-semibold rounded-full">
                          Featured
                        </span>
                      </div>
                    </div>
                    <div className="p-8 flex flex-col justify-center">
                      <div className="flex items-center gap-4 mb-4">
                        <span className="px-3 py-1 bg-purple-100 text-purple-600 text-xs font-medium rounded-full">
                          {featuredPost.category}
                        </span>
                        <span className="text-sm text-gray-500 flex items-center gap-1">
                          <Calendar className="w-4 h-4" />
                          {featuredPost.date}
                        </span>
                      </div>
                      <h2 className="text-2xl md:text-3xl font-bold text-gray-900 mb-4">
                        {featuredPost.title}
                      </h2>
                      <p className="text-gray-600 mb-6">{featuredPost.excerpt}</p>
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-3">
                          <img
                            src={featuredPost.authorAvatar}
                            alt={featuredPost.author}
                            className="w-10 h-10 rounded-full object-cover"
                          />
                          <div>
                            <p className="font-medium text-gray-900">{featuredPost.author}</p>
                            <p className="text-sm text-gray-500">{featuredPost.readTime}</p>
                          </div>
                        </div>
                        <Button className="bg-gradient-to-r from-purple-600 to-pink-500 hover:from-purple-700 hover:to-pink-600 text-white">
                          Read More
                          <ArrowRight className="w-4 h-4 ml-2" />
                        </Button>
                      </div>
                    </div>
                  </div>
                </motion.article>
              </div>
            </section>
          )}

          {/* Blog Posts Grid */}
          <section className="py-8 px-4 pb-20">
            <div className="container max-w-6xl mx-auto">
              <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
                {regularPosts.map((post, index) => (
                  <motion.article
                    key={post.id}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: index * 0.1 }}
                    className="bg-white/70 backdrop-blur-xl rounded-2xl border border-white/50 shadow-lg shadow-purple-500/5 overflow-hidden hover:shadow-xl hover:shadow-purple-500/10 transition-all duration-300 group"
                  >
                    <div className="relative h-48 overflow-hidden">
                      <img
                        src={post.image}
                        alt={post.title}
                        className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                      />
                      <div className="absolute top-4 left-4">
                        <span className="px-3 py-1 bg-white/90 backdrop-blur-sm text-purple-600 text-xs font-medium rounded-full">
                          {post.category}
                        </span>
                      </div>
                    </div>
                    <div className="p-6">
                      <div className="flex items-center gap-4 text-sm text-gray-500 mb-3">
                        <span className="flex items-center gap-1">
                          <Calendar className="w-4 h-4" />
                          {post.date}
                        </span>
                        <span className="flex items-center gap-1">
                          <Clock className="w-4 h-4" />
                          {post.readTime}
                        </span>
                      </div>
                      <h3 className="text-lg font-bold text-gray-900 mb-2 line-clamp-2 group-hover:text-purple-600 transition-colors">
                        {post.title}
                      </h3>
                      <p className="text-gray-600 text-sm mb-4 line-clamp-2">
                        {post.excerpt}
                      </p>
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-2">
                          <img
                            src={post.authorAvatar}
                            alt={post.author}
                            className="w-8 h-8 rounded-full object-cover"
                          />
                          <span className="text-sm text-gray-600">{post.author}</span>
                        </div>
                        <ChevronRight className="w-5 h-5 text-gray-400 group-hover:text-purple-500 group-hover:translate-x-1 transition-all" />
                      </div>
                    </div>
                  </motion.article>
                ))}
              </div>
            </div>
          </section>
        </>
      )}

      {/* Changelog Content */}
      {activeTab === 'changelog' && (
        <section className="py-8 px-4 pb-20">
          <div className="container max-w-4xl mx-auto">
            <div className="relative">
              {/* Timeline Line */}
              <div className="absolute left-8 top-0 bottom-0 w-0.5 bg-gradient-to-b from-purple-500 via-pink-500 to-orange-400 hidden md:block" />

              {/* Changelog Entries */}
              <div className="space-y-8">
                {changelog.map((entry, index) => (
                  <motion.div
                    key={entry.version}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: index * 0.1 }}
                    className="relative md:pl-20"
                  >
                    {/* Version Badge */}
                    <div className="hidden md:flex absolute left-0 top-0 w-16 h-16 rounded-2xl bg-gradient-to-br items-center justify-center text-white font-bold shadow-lg"
                      style={{
                        background: `linear-gradient(135deg, ${
                          entry.type === 'major' ? '#8b5cf6, #ec4899' :
                          entry.type === 'minor' ? '#3b82f6, #06b6d4' :
                          '#9ca3af, #6b7280'
                        })`
                      }}
                    >
                      {entry.version}
                    </div>

                    {/* Content Card */}
                    <div className="bg-white/70 backdrop-blur-xl rounded-2xl border border-white/50 shadow-lg shadow-purple-500/5 p-6">
                      <div className="flex flex-wrap items-center gap-3 mb-4">
                        <span className={`md:hidden px-3 py-1 rounded-full text-sm font-bold text-white bg-gradient-to-r ${getVersionColor(entry.type)}`}>
                          v{entry.version}
                        </span>
                        <span className="text-sm text-gray-500 flex items-center gap-1">
                          <Calendar className="w-4 h-4" />
                          {entry.date}
                        </span>
                        <span className={`px-2 py-0.5 rounded text-xs font-medium ${
                          entry.type === 'major' ? 'bg-purple-100 text-purple-700' :
                          entry.type === 'minor' ? 'bg-blue-100 text-blue-700' :
                          'bg-gray-100 text-gray-700'
                        }`}>
                          {entry.type.charAt(0).toUpperCase() + entry.type.slice(1)} Release
                        </span>
                      </div>

                      <h3 className="text-xl font-bold text-gray-900 mb-2">
                        {entry.title}
                      </h3>
                      <p className="text-gray-600 mb-4">{entry.description}</p>

                      <div className="space-y-2">
                        {entry.changes.map((change, changeIndex) => (
                          <div
                            key={changeIndex}
                            className="flex items-start gap-3"
                          >
                            <span className={`px-2 py-0.5 rounded text-xs font-medium ${getChangeTypeColor(change.type)}`}>
                              {change.type}
                            </span>
                            <span className="text-gray-700 text-sm">{change.text}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  </motion.div>
                ))}
              </div>
            </div>

            {/* Load More */}
            <div className="text-center mt-12">
              <Button
                variant="outline"
                className="border-purple-200 text-purple-600 hover:bg-purple-50"
              >
                View All Releases
                <ArrowRight className="w-4 h-4 ml-2" />
              </Button>
            </div>
          </div>
        </section>
      )}

      <Footer />
    </div>
  );
}
