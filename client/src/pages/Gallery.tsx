/**
 * Gallery Page - SmartSpec Pro
 * Design: Ethereal Gradient Flow
 * Features: Images, Videos, Website Demos with full SEO/ASO support
 * 
 * SEO/ASO Features:
 * - Dynamic meta tags for each content type
 * - Open Graph tags for social sharing
 * - Structured data (JSON-LD) for rich snippets
 * - Semantic HTML with proper heading hierarchy
 * - Alt text and ARIA labels for accessibility
 * - Lazy loading for performance
 */

import { useState, useEffect, useMemo } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Link } from 'wouter';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Navbar } from '@/components/Navbar';
import { Footer } from '@/components/Footer';
import {
  Image as ImageIcon,
  Video,
  Globe,
  Search,
  Filter,
  Grid3X3,
  LayoutGrid,
  Heart,
  Eye,
  Download,
  Share2,
  ExternalLink,
  Play,
  Pause,
  X,
  ChevronLeft,
  ChevronRight,
  Sparkles,
  Maximize2,
  Clock,
  User,
  Tag,
  Loader2
} from 'lucide-react';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Helmet } from 'react-helmet-async';

// Types
type ContentType = 'all' | 'images' | 'videos' | 'websites';
type AspectRatio = '1:1' | '9:16' | '16:9';
type SortOption = 'newest' | 'popular' | 'trending';

interface GalleryItem {
  id: string;
  type: 'image' | 'video' | 'website';
  title: string;
  description: string;
  thumbnail: string;
  url: string;
  aspectRatio: AspectRatio;
  author: {
    name: string;
    avatar: string;
  };
  stats: {
    views: number;
    likes: number;
    downloads?: number;
  };
  tags: string[];
  createdAt: string;
  // For websites
  demoUrl?: string;
  // For videos
  duration?: string;
}

// Cloudflare R2 base URL (placeholder - will be configured)
const R2_BASE_URL = 'https://pub-smartspec.r2.dev';

// Mock data - In production, this would come from API/R2
const mockGalleryItems: GalleryItem[] = [
  // Images
  {
    id: 'img-1',
    type: 'image',
    title: 'AI-Generated Landscape',
    description: 'Beautiful mountain landscape created with SmartSpec AI image generation',
    thumbnail: 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400&h=300&fit=crop',
    url: 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1200&h=800&fit=crop',
    aspectRatio: '16:9',
    author: { name: 'John Doe', avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=john' },
    stats: { views: 12500, likes: 890, downloads: 234 },
    tags: ['landscape', 'nature', 'ai-art', 'mountains'],
    createdAt: '2025-01-02T10:00:00Z'
  },
  {
    id: 'img-2',
    type: 'image',
    title: 'Portrait Study',
    description: 'Professional portrait generated using advanced AI models',
    thumbnail: 'https://images.unsplash.com/photo-1531746020798-e6953c6e8e04?w=400&h=600&fit=crop',
    url: 'https://images.unsplash.com/photo-1531746020798-e6953c6e8e04?w=800&h=1200&fit=crop',
    aspectRatio: '9:16',
    author: { name: 'Sarah Chen', avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=sarah' },
    stats: { views: 8900, likes: 567, downloads: 123 },
    tags: ['portrait', 'ai-art', 'professional'],
    createdAt: '2025-01-01T15:30:00Z'
  },
  {
    id: 'img-3',
    type: 'image',
    title: 'Abstract Art Collection',
    description: 'Stunning abstract artwork perfect for modern designs',
    thumbnail: 'https://images.unsplash.com/photo-1541701494587-cb58502866ab?w=400&h=400&fit=crop',
    url: 'https://images.unsplash.com/photo-1541701494587-cb58502866ab?w=800&h=800&fit=crop',
    aspectRatio: '1:1',
    author: { name: 'Mike Wilson', avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=mike' },
    stats: { views: 15200, likes: 1234, downloads: 456 },
    tags: ['abstract', 'modern', 'colorful', 'art'],
    createdAt: '2024-12-30T09:00:00Z'
  },
  {
    id: 'img-4',
    type: 'image',
    title: 'Product Photography',
    description: 'AI-enhanced product shots for e-commerce',
    thumbnail: 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400&h=400&fit=crop',
    url: 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=800&h=800&fit=crop',
    aspectRatio: '1:1',
    author: { name: 'Emily Brown', avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=emily' },
    stats: { views: 6700, likes: 345, downloads: 89 },
    tags: ['product', 'ecommerce', 'photography'],
    createdAt: '2024-12-28T14:00:00Z'
  },
  {
    id: 'img-5',
    type: 'image',
    title: 'Cyberpunk City',
    description: 'Futuristic cityscape with neon lights',
    thumbnail: 'https://images.unsplash.com/photo-1480714378408-67cf0d13bc1b?w=400&h=300&fit=crop',
    url: 'https://images.unsplash.com/photo-1480714378408-67cf0d13bc1b?w=1200&h=800&fit=crop',
    aspectRatio: '16:9',
    author: { name: 'Neo Matrix', avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=neo' },
    stats: { views: 22100, likes: 1890, downloads: 567 },
    tags: ['cyberpunk', 'city', 'neon', 'futuristic'],
    createdAt: '2024-12-27T20:00:00Z'
  },
  // Videos
  {
    id: 'vid-1',
    type: 'video',
    title: 'Motion Graphics Demo',
    description: 'Stunning motion graphics created with AI video generation',
    thumbnail: 'https://images.unsplash.com/photo-1550745165-9bc0b252726f?w=400&h=300&fit=crop',
    url: 'https://sample-videos.com/video123/mp4/720/big_buck_bunny_720p_1mb.mp4',
    aspectRatio: '16:9',
    author: { name: 'Alex Turner', avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=alex' },
    stats: { views: 23400, likes: 1890 },
    tags: ['motion', 'animation', 'ai-video'],
    createdAt: '2025-01-02T08:00:00Z',
    duration: '0:45'
  },
  {
    id: 'vid-2',
    type: 'video',
    title: 'Social Media Reel',
    description: 'Vertical video perfect for Instagram and TikTok',
    thumbnail: 'https://images.unsplash.com/photo-1611162617474-5b21e879e113?w=400&h=600&fit=crop',
    url: 'https://sample-videos.com/video123/mp4/720/big_buck_bunny_720p_1mb.mp4',
    aspectRatio: '9:16',
    author: { name: 'Lisa Park', avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=lisa' },
    stats: { views: 45600, likes: 3456 },
    tags: ['social', 'reel', 'vertical', 'trending'],
    createdAt: '2025-01-01T12:00:00Z',
    duration: '0:30'
  },
  {
    id: 'vid-3',
    type: 'video',
    title: 'Product Showcase',
    description: 'Professional product video with AI-generated effects',
    thumbnail: 'https://images.unsplash.com/photo-1492619375914-88005aa9e8fb?w=400&h=300&fit=crop',
    url: 'https://sample-videos.com/video123/mp4/720/big_buck_bunny_720p_1mb.mp4',
    aspectRatio: '16:9',
    author: { name: 'David Kim', avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=david' },
    stats: { views: 18900, likes: 1234 },
    tags: ['product', 'showcase', 'professional'],
    createdAt: '2024-12-29T16:00:00Z',
    duration: '1:20'
  },
  // Websites
  {
    id: 'web-1',
    type: 'website',
    title: 'E-Commerce Dashboard',
    description: 'Modern e-commerce admin dashboard built with SmartSpec',
    thumbnail: 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=400&h=300&fit=crop',
    url: 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=1200&h=800&fit=crop',
    aspectRatio: '16:9',
    author: { name: 'Tech Studio', avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=tech' },
    stats: { views: 34500, likes: 2890 },
    tags: ['dashboard', 'ecommerce', 'admin', 'react'],
    createdAt: '2025-01-02T11:00:00Z',
    demoUrl: 'https://demo-ecommerce.smartspec.pro'
  },
  {
    id: 'web-2',
    type: 'website',
    title: 'SaaS Landing Page',
    description: 'High-converting landing page for SaaS products',
    thumbnail: 'https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=400&h=300&fit=crop',
    url: 'https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=1200&h=800&fit=crop',
    aspectRatio: '16:9',
    author: { name: 'Design Co', avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=design' },
    stats: { views: 28700, likes: 2345 },
    tags: ['landing', 'saas', 'marketing', 'conversion'],
    createdAt: '2025-01-01T09:00:00Z',
    demoUrl: 'https://demo-saas.smartspec.pro'
  },
  {
    id: 'web-3',
    type: 'website',
    title: 'Portfolio Template',
    description: 'Creative portfolio website for designers and developers',
    thumbnail: 'https://images.unsplash.com/photo-1467232004584-a241de8bcf5d?w=400&h=300&fit=crop',
    url: 'https://images.unsplash.com/photo-1467232004584-a241de8bcf5d?w=1200&h=800&fit=crop',
    aspectRatio: '16:9',
    author: { name: 'Creative Labs', avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=creative' },
    stats: { views: 19800, likes: 1567 },
    tags: ['portfolio', 'creative', 'designer', 'developer'],
    createdAt: '2024-12-31T14:00:00Z',
    demoUrl: 'https://demo-portfolio.smartspec.pro'
  },
  {
    id: 'web-4',
    type: 'website',
    title: 'Blog Platform',
    description: 'Modern blog platform with AI content suggestions',
    thumbnail: 'https://images.unsplash.com/photo-1499750310107-5fef28a66643?w=400&h=300&fit=crop',
    url: 'https://images.unsplash.com/photo-1499750310107-5fef28a66643?w=1200&h=800&fit=crop',
    aspectRatio: '16:9',
    author: { name: 'Content Team', avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=content' },
    stats: { views: 15600, likes: 987 },
    tags: ['blog', 'content', 'publishing', 'ai'],
    createdAt: '2024-12-28T10:00:00Z',
    demoUrl: 'https://demo-blog.smartspec.pro'
  }
];

// Tab configuration
const tabs = [
  { id: 'all' as ContentType, label: 'All', icon: Grid3X3, count: mockGalleryItems.length },
  { id: 'images' as ContentType, label: 'Images', icon: ImageIcon, count: mockGalleryItems.filter(i => i.type === 'image').length },
  { id: 'videos' as ContentType, label: 'Videos', icon: Video, count: mockGalleryItems.filter(i => i.type === 'video').length },
  { id: 'websites' as ContentType, label: 'Websites', icon: Globe, count: mockGalleryItems.filter(i => i.type === 'website').length },
];

// Aspect ratio styles
const aspectRatioStyles: Record<AspectRatio, string> = {
  '1:1': 'aspect-square',
  '9:16': 'aspect-[9/16]',
  '16:9': 'aspect-video',
};

// Format number for display
const formatNumber = (num: number): string => {
  if (num >= 1000000) return `${(num / 1000000).toFixed(1)}M`;
  if (num >= 1000) return `${(num / 1000).toFixed(1)}K`;
  return num.toString();
};

// Format date for display
const formatDate = (dateString: string): string => {
  const date = new Date(dateString);
  const now = new Date();
  const diffMs = now.getTime() - date.getTime();
  const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));
  
  if (diffDays === 0) return 'Today';
  if (diffDays === 1) return 'Yesterday';
  if (diffDays < 7) return `${diffDays} days ago`;
  if (diffDays < 30) return `${Math.floor(diffDays / 7)} weeks ago`;
  return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
};

// Gallery Item Card Component
function GalleryCard({ item, onClick }: { item: GalleryItem; onClick: () => void }) {
  const [isHovered, setIsHovered] = useState(false);
  const [imageError, setImageError] = useState(false);

  // Placeholder image based on type
  const placeholderImage = item.type === 'image' 
    ? 'https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=400&h=300&fit=crop'
    : item.type === 'video'
    ? 'https://images.unsplash.com/photo-1574717024653-61fd2cf4d44d?w=400&h=300&fit=crop'
    : 'https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=400&h=300&fit=crop';

  return (
    <motion.article
      layout
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.9 }}
      transition={{ duration: 0.3 }}
      className="group relative"
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
      itemScope
      itemType={item.type === 'image' ? 'https://schema.org/ImageObject' : item.type === 'video' ? 'https://schema.org/VideoObject' : 'https://schema.org/WebSite'}
    >
      <Card 
        className="overflow-hidden bg-white/80 backdrop-blur-sm border border-gray-200 shadow-lg hover:shadow-2xl hover:shadow-violet-500/10 transition-all duration-500 cursor-pointer"
        onClick={onClick}
      >
        {/* Thumbnail */}
        <div className={`relative overflow-hidden ${aspectRatioStyles[item.aspectRatio]} bg-gradient-to-br from-violet-100 to-teal-100`}>
          <img
            src={imageError ? placeholderImage : item.thumbnail}
            alt={item.title}
            className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110"
            loading="lazy"
            onError={() => setImageError(true)}
            itemProp="thumbnailUrl"
          />
          
          {/* Overlay */}
          <div className={`absolute inset-0 bg-gradient-to-t from-black/70 via-black/20 to-transparent transition-opacity duration-300 ${isHovered ? 'opacity-100' : 'opacity-0'}`} />
          
          {/* Type Badge */}
          <div className="absolute top-3 left-3">
            <span className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-semibold backdrop-blur-sm ${
              item.type === 'image' ? 'bg-violet-500/90 text-white' :
              item.type === 'video' ? 'bg-rose-500/90 text-white' :
              'bg-teal-500/90 text-white'
            }`}>
              {item.type === 'image' && <ImageIcon className="w-3 h-3" />}
              {item.type === 'video' && <Video className="w-3 h-3" />}
              {item.type === 'website' && <Globe className="w-3 h-3" />}
              {item.type.charAt(0).toUpperCase() + item.type.slice(1)}
            </span>
          </div>

          {/* Video Duration */}
          {item.type === 'video' && item.duration && (
            <div className="absolute bottom-3 right-3">
              <span className="inline-flex items-center gap-1 px-2 py-1 rounded bg-black/70 text-white text-xs font-medium backdrop-blur-sm">
                <Clock className="w-3 h-3" />
                {item.duration}
              </span>
            </div>
          )}

          {/* Play Button for Videos */}
          {item.type === 'video' && (
            <div className={`absolute inset-0 flex items-center justify-center transition-opacity duration-300 ${isHovered ? 'opacity-100' : 'opacity-70'}`}>
              <div className="w-16 h-16 rounded-full bg-white/90 flex items-center justify-center shadow-xl">
                <Play className="w-7 h-7 text-rose-500 ml-1" fill="currentColor" />
              </div>
            </div>
          )}

          {/* Website Demo Link */}
          {item.type === 'website' && item.demoUrl && isHovered && (
            <div className="absolute inset-0 flex items-center justify-center">
              <Button 
                className="bg-white/90 text-teal-600 hover:bg-white shadow-xl"
                onClick={(e) => {
                  e.stopPropagation();
                  window.open(item.demoUrl, '_blank');
                }}
              >
                <ExternalLink className="w-4 h-4 mr-2" />
                View Live Demo
              </Button>
            </div>
          )}

          {/* Hover Actions */}
          <div className={`absolute top-3 right-3 flex gap-2 transition-all duration-300 ${isHovered ? 'opacity-100 translate-y-0' : 'opacity-0 -translate-y-2'}`}>
            <button 
              className="w-8 h-8 rounded-full bg-white/90 flex items-center justify-center hover:bg-white transition-colors shadow-lg"
              onClick={(e) => { e.stopPropagation(); }}
              aria-label="Like"
            >
              <Heart className="w-4 h-4 text-gray-700 hover:text-rose-500" />
            </button>
            <button 
              className="w-8 h-8 rounded-full bg-white/90 flex items-center justify-center hover:bg-white transition-colors shadow-lg"
              onClick={(e) => { e.stopPropagation(); }}
              aria-label="Share"
            >
              <Share2 className="w-4 h-4 text-gray-700 hover:text-violet-500" />
            </button>
          </div>
        </div>

        {/* Content */}
        <CardContent className="p-4">
          <h3 className="font-semibold text-gray-900 mb-1 line-clamp-1 group-hover:text-violet-600 transition-colors" itemProp="name">
            {item.title}
          </h3>
          <p className="text-sm text-gray-600 mb-3 line-clamp-2" itemProp="description">
            {item.description}
          </p>

          {/* Author & Stats */}
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <img 
                src={item.author.avatar} 
                alt={item.author.name}
                className="w-6 h-6 rounded-full"
                loading="lazy"
              />
              <span className="text-xs text-gray-500" itemProp="author">{item.author.name}</span>
            </div>
            <div className="flex items-center gap-3 text-xs text-gray-500">
              <span className="flex items-center gap-1">
                <Eye className="w-3.5 h-3.5" />
                {formatNumber(item.stats.views)}
              </span>
              <span className="flex items-center gap-1">
                <Heart className="w-3.5 h-3.5" />
                {formatNumber(item.stats.likes)}
              </span>
            </div>
          </div>

          {/* Tags */}
          <div className="flex flex-wrap gap-1.5 mt-3">
            {item.tags.slice(0, 3).map((tag) => (
              <span 
                key={tag} 
                className="px-2 py-0.5 rounded-full bg-gray-100 text-gray-600 text-xs hover:bg-violet-100 hover:text-violet-700 transition-colors cursor-pointer"
              >
                #{tag}
              </span>
            ))}
            {item.tags.length > 3 && (
              <span className="px-2 py-0.5 text-gray-400 text-xs">+{item.tags.length - 3}</span>
            )}
          </div>

          {/* Hidden SEO data */}
          <meta itemProp="dateCreated" content={item.createdAt} />
          <meta itemProp="interactionCount" content={`${item.stats.views} views`} />
        </CardContent>
      </Card>
    </motion.article>
  );
}

// Lightbox/Modal Component
function GalleryLightbox({ 
  item, 
  isOpen, 
  onClose,
  onPrev,
  onNext,
  hasPrev,
  hasNext
}: { 
  item: GalleryItem | null; 
  isOpen: boolean; 
  onClose: () => void;
  onPrev: () => void;
  onNext: () => void;
  hasPrev: boolean;
  hasNext: boolean;
}) {
  const [imageError, setImageError] = useState(false);

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose();
      if (e.key === 'ArrowLeft' && hasPrev) onPrev();
      if (e.key === 'ArrowRight' && hasNext) onNext();
    };
    
    if (isOpen) {
      document.addEventListener('keydown', handleKeyDown);
      document.body.style.overflow = 'hidden';
    }
    
    return () => {
      document.removeEventListener('keydown', handleKeyDown);
      document.body.style.overflow = 'unset';
    };
  }, [isOpen, hasPrev, hasNext, onClose, onPrev, onNext]);

  if (!item) return null;

  const placeholderImage = item.type === 'image' 
    ? 'https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=800&h=600&fit=crop'
    : item.type === 'video'
    ? 'https://images.unsplash.com/photo-1574717024653-61fd2cf4d44d?w=800&h=600&fit=crop'
    : 'https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=800&h=600&fit=crop';

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="max-w-6xl w-full h-[90vh] p-0 bg-black/95 border-none overflow-hidden">
        <div className="relative w-full h-full flex flex-col">
          {/* Header */}
          <div className="absolute top-0 left-0 right-0 z-20 p-4 bg-gradient-to-b from-black/80 to-transparent">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <img 
                  src={item.author.avatar} 
                  alt={item.author.name}
                  className="w-10 h-10 rounded-full border-2 border-white/30"
                />
                <div>
                  <h2 className="text-white font-semibold">{item.title}</h2>
                  <p className="text-white/70 text-sm">by {item.author.name}</p>
                </div>
              </div>
              <div className="flex items-center gap-2">
                <Button variant="ghost" size="icon" className="text-white hover:bg-white/20">
                  <Heart className="w-5 h-5" />
                </Button>
                <Button variant="ghost" size="icon" className="text-white hover:bg-white/20">
                  <Share2 className="w-5 h-5" />
                </Button>
                {item.type === 'image' && (
                  <Button variant="ghost" size="icon" className="text-white hover:bg-white/20">
                    <Download className="w-5 h-5" />
                  </Button>
                )}
                {item.type === 'website' && item.demoUrl && (
                  <Button 
                    variant="ghost" 
                    className="text-white hover:bg-white/20"
                    onClick={() => window.open(item.demoUrl, '_blank')}
                  >
                    <ExternalLink className="w-5 h-5 mr-2" />
                    Live Demo
                  </Button>
                )}
                <Button variant="ghost" size="icon" className="text-white hover:bg-white/20" onClick={onClose}>
                  <X className="w-5 h-5" />
                </Button>
              </div>
            </div>
          </div>

          {/* Main Content */}
          <div className="flex-1 flex items-center justify-center p-4 pt-20 pb-24">
            {item.type === 'image' && (
              <img
                src={imageError ? placeholderImage : item.url}
                alt={item.title}
                className="max-w-full max-h-full object-contain rounded-lg"
                onError={() => setImageError(true)}
              />
            )}
            {item.type === 'video' && (
              <div className="relative w-full max-w-4xl">
                <video
                  src={item.url}
                  poster={item.thumbnail}
                  controls
                  className="w-full rounded-lg"
                >
                  Your browser does not support the video tag.
                </video>
              </div>
            )}
            {item.type === 'website' && (
              <div className="relative w-full max-w-5xl">
                <img
                  src={imageError ? placeholderImage : item.url}
                  alt={item.title}
                  className="w-full rounded-lg shadow-2xl"
                  onError={() => setImageError(true)}
                />
                {item.demoUrl && (
                  <div className="absolute inset-0 flex items-center justify-center bg-black/30 opacity-0 hover:opacity-100 transition-opacity rounded-lg">
                    <Button 
                      size="lg"
                      className="bg-white text-teal-600 hover:bg-gray-100"
                      onClick={() => window.open(item.demoUrl, '_blank')}
                    >
                      <ExternalLink className="w-5 h-5 mr-2" />
                      Open Live Demo
                    </Button>
                  </div>
                )}
              </div>
            )}
          </div>

          {/* Navigation Arrows */}
          {hasPrev && (
            <button
              onClick={onPrev}
              className="absolute left-4 top-1/2 -translate-y-1/2 w-12 h-12 rounded-full bg-white/10 hover:bg-white/20 flex items-center justify-center text-white transition-colors"
              aria-label="Previous"
            >
              <ChevronLeft className="w-6 h-6" />
            </button>
          )}
          {hasNext && (
            <button
              onClick={onNext}
              className="absolute right-4 top-1/2 -translate-y-1/2 w-12 h-12 rounded-full bg-white/10 hover:bg-white/20 flex items-center justify-center text-white transition-colors"
              aria-label="Next"
            >
              <ChevronRight className="w-6 h-6" />
            </button>
          )}

          {/* Footer Info */}
          <div className="absolute bottom-0 left-0 right-0 z-20 p-4 bg-gradient-to-t from-black/80 to-transparent">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-4 text-white/70 text-sm">
                <span className="flex items-center gap-1">
                  <Eye className="w-4 h-4" />
                  {formatNumber(item.stats.views)} views
                </span>
                <span className="flex items-center gap-1">
                  <Heart className="w-4 h-4" />
                  {formatNumber(item.stats.likes)} likes
                </span>
                <span className="flex items-center gap-1">
                  <Clock className="w-4 h-4" />
                  {formatDate(item.createdAt)}
                </span>
              </div>
              <div className="flex flex-wrap gap-2">
                {item.tags.map((tag) => (
                  <span 
                    key={tag}
                    className="px-2 py-1 rounded-full bg-white/10 text-white/80 text-xs"
                  >
                    #{tag}
                  </span>
                ))}
              </div>
            </div>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
}

// Main Gallery Page Component
export default function Gallery() {
  const [activeTab, setActiveTab] = useState<ContentType>('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [sortBy, setSortBy] = useState<SortOption>('newest');
  const [aspectFilter, setAspectFilter] = useState<AspectRatio | 'all'>('all');
  const [selectedItem, setSelectedItem] = useState<GalleryItem | null>(null);
  const [isLightboxOpen, setIsLightboxOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  // Filter and sort items
  const filteredItems = useMemo(() => {
    let items = [...mockGalleryItems];

    // Filter by type
    if (activeTab !== 'all') {
      const typeMap: Record<ContentType, string> = {
        all: 'all',
        images: 'image',
        videos: 'video',
        websites: 'website'
      };
      items = items.filter(item => item.type === typeMap[activeTab]);
    }

    // Filter by aspect ratio
    if (aspectFilter !== 'all') {
      items = items.filter(item => item.aspectRatio === aspectFilter);
    }

    // Filter by search query
    if (searchQuery) {
      const query = searchQuery.toLowerCase();
      items = items.filter(item => 
        item.title.toLowerCase().includes(query) ||
        item.description.toLowerCase().includes(query) ||
        item.tags.some(tag => tag.toLowerCase().includes(query))
      );
    }

    // Sort items
    switch (sortBy) {
      case 'newest':
        items.sort((a, b) => new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime());
        break;
      case 'popular':
        items.sort((a, b) => b.stats.views - a.stats.views);
        break;
      case 'trending':
        items.sort((a, b) => b.stats.likes - a.stats.likes);
        break;
    }

    return items;
  }, [activeTab, searchQuery, sortBy, aspectFilter]);

  // Lightbox navigation
  const currentIndex = selectedItem ? filteredItems.findIndex(i => i.id === selectedItem.id) : -1;
  const hasPrev = currentIndex > 0;
  const hasNext = currentIndex < filteredItems.length - 1;

  const handlePrev = () => {
    if (hasPrev) {
      setSelectedItem(filteredItems[currentIndex - 1]);
    }
  };

  const handleNext = () => {
    if (hasNext) {
      setSelectedItem(filteredItems[currentIndex + 1]);
    }
  };

  const handleItemClick = (item: GalleryItem) => {
    setSelectedItem(item);
    setIsLightboxOpen(true);
  };

  // Generate structured data for SEO
  const structuredData = {
    "@context": "https://schema.org",
    "@type": "CollectionPage",
    "name": "SmartSpec Pro Gallery",
    "description": "Explore AI-generated images, videos, and website demos created with SmartSpec Pro",
    "url": "https://smartspec.pro/gallery",
    "mainEntity": {
      "@type": "ItemList",
      "numberOfItems": filteredItems.length,
      "itemListElement": filteredItems.slice(0, 10).map((item, index) => ({
        "@type": "ListItem",
        "position": index + 1,
        "item": {
          "@type": item.type === 'image' ? 'ImageObject' : item.type === 'video' ? 'VideoObject' : 'WebSite',
          "name": item.title,
          "description": item.description,
          "thumbnailUrl": item.thumbnail,
          "author": {
            "@type": "Person",
            "name": item.author.name
          }
        }
      }))
    }
  };

  return (
    <>
      {/* SEO Meta Tags */}
      <Helmet>
        <title>Gallery - AI Generated Images, Videos & Websites | SmartSpec Pro</title>
        <meta name="description" content="Explore our gallery of AI-generated images, videos, and website demos. See what's possible with SmartSpec Pro's advanced AI generation capabilities." />
        <meta name="keywords" content="AI gallery, AI generated images, AI videos, website templates, SmartSpec Pro, AI art, generative AI" />
        
        {/* Open Graph */}
        <meta property="og:title" content="SmartSpec Pro Gallery - AI Generated Content" />
        <meta property="og:description" content="Explore AI-generated images, videos, and website demos created with SmartSpec Pro" />
        <meta property="og:type" content="website" />
        <meta property="og:url" content="https://smartspec.pro/gallery" />
        <meta property="og:image" content="https://smartspec.pro/og/gallery-cover.jpg" />
        
        {/* Twitter Card */}
        <meta name="twitter:card" content="summary_large_image" />
        <meta name="twitter:title" content="SmartSpec Pro Gallery" />
        <meta name="twitter:description" content="AI-generated images, videos, and website demos" />
        
        {/* Structured Data */}
        <script type="application/ld+json">
          {JSON.stringify(structuredData)}
        </script>
      </Helmet>

      <div className="min-h-screen bg-gradient-to-b from-slate-50 via-white to-slate-50">
        <Navbar />
        
        {/* Hero Section */}
        <section className="relative pt-32 pb-16 overflow-hidden">
          {/* Background */}
          <div className="absolute inset-0">
            <div className="absolute inset-0 bg-gradient-to-br from-violet-100/40 via-transparent to-teal-100/40" />
            <motion.div 
              className="absolute top-0 left-1/4 w-[500px] h-[500px] bg-gradient-to-br from-violet-400/15 via-purple-400/15 to-fuchsia-400/15 rounded-full blur-3xl"
              animate={{
                x: [0, 30, 0],
                y: [0, 20, 0],
              }}
              transition={{
                duration: 15,
                repeat: Number.POSITIVE_INFINITY,
                ease: "easeInOut"
              }}
            />
            <motion.div 
              className="absolute top-20 right-1/4 w-[400px] h-[400px] bg-gradient-to-br from-teal-400/15 via-emerald-400/15 to-cyan-400/15 rounded-full blur-3xl"
              animate={{
                x: [0, -20, 0],
                y: [0, 30, 0],
              }}
              transition={{
                duration: 18,
                repeat: Number.POSITIVE_INFINITY,
                ease: "easeInOut"
              }}
            />
          </div>

          <div className="container relative mx-auto px-4 sm:px-6 lg:px-8">
            <motion.div 
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="text-center max-w-4xl mx-auto"
            >
              {/* Badge */}
              <motion.div
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: 0.1 }}
                className="inline-flex items-center gap-2 px-5 py-2.5 rounded-full bg-gradient-to-r from-violet-500/10 via-purple-500/10 to-fuchsia-500/10 border border-violet-200/50 backdrop-blur-sm mb-6"
              >
                <Sparkles className="w-4 h-4 text-violet-600" />
                <span className="text-sm font-semibold bg-gradient-to-r from-violet-600 to-fuchsia-600 bg-clip-text text-transparent">
                  Community Gallery
                </span>
              </motion.div>

              <motion.h1 
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.2 }}
                className="text-5xl sm:text-6xl font-bold mb-6 tracking-tight"
              >
                <span className="text-gray-900">Explore AI</span>
                <br />
                <span className="bg-gradient-to-r from-violet-600 via-purple-600 to-fuchsia-600 bg-clip-text text-transparent">
                  Creations
                </span>
              </motion.h1>

              <motion.p 
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.3 }}
                className="text-xl text-gray-600 mb-10 max-w-2xl mx-auto"
              >
                Discover stunning images, videos, and website demos created by our community 
                using SmartSpec Pro's AI generation tools.
              </motion.p>

              {/* Search Bar */}
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.4 }}
                className="max-w-2xl mx-auto"
              >
                <div className="relative">
                  <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                  <Input
                    type="search"
                    placeholder="Search images, videos, websites..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="w-full pl-12 pr-4 py-6 text-lg rounded-2xl bg-white/80 backdrop-blur-sm border-gray-200 shadow-lg shadow-gray-200/50 focus:ring-2 focus:ring-violet-500 focus:border-violet-500"
                    aria-label="Search gallery"
                  />
                </div>
              </motion.div>
            </motion.div>
          </div>
        </section>

        {/* Tabs & Filters */}
        <section className="sticky top-0 z-30 bg-white/80 backdrop-blur-lg border-b border-gray-200 shadow-sm">
          <div className="container mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex flex-col sm:flex-row items-center justify-between gap-4 py-4">
              {/* Tabs */}
              <nav className="flex items-center gap-2" role="tablist" aria-label="Gallery content types">
                {tabs.map((tab) => (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id)}
                    role="tab"
                    aria-selected={activeTab === tab.id}
                    aria-controls={`${tab.id}-panel`}
                    className={`flex items-center gap-2 px-4 py-2.5 rounded-xl text-sm font-medium transition-all duration-300 ${
                      activeTab === tab.id
                        ? 'bg-gradient-to-r from-violet-500 to-fuchsia-500 text-white shadow-lg shadow-violet-500/30'
                        : 'text-gray-600 hover:bg-gray-100'
                    }`}
                  >
                    <tab.icon className="w-4 h-4" />
                    {tab.label}
                    <span className={`px-1.5 py-0.5 rounded-full text-xs ${
                      activeTab === tab.id ? 'bg-white/20' : 'bg-gray-200'
                    }`}>
                      {tab.count}
                    </span>
                  </button>
                ))}
              </nav>

              {/* Filters */}
              <div className="flex items-center gap-3">
                {/* Aspect Ratio Filter */}
                <Select value={aspectFilter} onValueChange={(v) => setAspectFilter(v as AspectRatio | 'all')}>
                  <SelectTrigger className="w-[140px] bg-white">
                    <Filter className="w-4 h-4 mr-2 text-gray-400" />
                    <SelectValue placeholder="Aspect Ratio" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="all">All Sizes</SelectItem>
                    <SelectItem value="1:1">Square (1:1)</SelectItem>
                    <SelectItem value="9:16">Portrait (9:16)</SelectItem>
                    <SelectItem value="16:9">Landscape (16:9)</SelectItem>
                  </SelectContent>
                </Select>

                {/* Sort */}
                <Select value={sortBy} onValueChange={(v) => setSortBy(v as SortOption)}>
                  <SelectTrigger className="w-[130px] bg-white">
                    <SelectValue placeholder="Sort by" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="newest">Newest</SelectItem>
                    <SelectItem value="popular">Most Viewed</SelectItem>
                    <SelectItem value="trending">Most Liked</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>
          </div>
        </section>

        {/* Gallery Grid */}
        <section className="py-12" role="tabpanel" id={`${activeTab}-panel`} aria-labelledby={activeTab}>
          <div className="container mx-auto px-4 sm:px-6 lg:px-8">
            {isLoading ? (
              <div className="flex items-center justify-center py-20">
                <Loader2 className="w-8 h-8 animate-spin text-violet-500" />
              </div>
            ) : filteredItems.length === 0 ? (
              <div className="text-center py-20">
                <div className="w-20 h-20 mx-auto mb-6 rounded-full bg-gray-100 flex items-center justify-center">
                  <Search className="w-10 h-10 text-gray-400" />
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">No results found</h3>
                <p className="text-gray-600">Try adjusting your search or filters</p>
              </div>
            ) : (
              <motion.div 
                layout
                className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6"
              >
                <AnimatePresence mode="popLayout">
                  {filteredItems.map((item) => (
                    <GalleryCard 
                      key={item.id} 
                      item={item} 
                      onClick={() => handleItemClick(item)}
                    />
                  ))}
                </AnimatePresence>
              </motion.div>
            )}

            {/* Load More */}
            {filteredItems.length > 0 && (
              <div className="text-center mt-12">
                <Button 
                  variant="outline" 
                  size="lg"
                  className="px-8"
                  onClick={() => {
                    setIsLoading(true);
                    setTimeout(() => setIsLoading(false), 1000);
                  }}
                >
                  Load More
                </Button>
              </div>
            )}
          </div>
        </section>

        {/* CTA Section */}
        <section className="py-20">
          <div className="container mx-auto px-4 sm:px-6 lg:px-8">
            <motion.div 
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              className="relative max-w-4xl mx-auto text-center"
            >
              <div className="absolute inset-0 bg-gradient-to-r from-violet-600 via-purple-600 to-fuchsia-600 rounded-3xl transform rotate-1" />
              <div className="relative bg-gradient-to-r from-violet-500 via-purple-500 to-fuchsia-500 rounded-3xl p-10 sm:p-14 overflow-hidden">
                <div className="absolute top-0 right-0 w-64 h-64 bg-white/10 rounded-full blur-3xl" />
                <div className="absolute bottom-0 left-0 w-64 h-64 bg-white/10 rounded-full blur-3xl" />
                
                <div className="relative">
                  <h2 className="text-3xl sm:text-4xl font-bold text-white mb-4">
                    Ready to Create Your Own?
                  </h2>
                  <p className="text-xl text-white/80 mb-8 max-w-2xl mx-auto">
                    Join thousands of creators using SmartSpec Pro to generate stunning 
                    images, videos, and websites with AI.
                  </p>
                  <div className="flex flex-col sm:flex-row gap-4 justify-center">
                    <Button 
                      size="lg" 
                      className="bg-white text-violet-600 hover:bg-gray-100 px-8 py-6 text-base font-semibold shadow-xl"
                      asChild
                    >
                      <Link href="/signup">
                        Start Creating Free
                      </Link>
                    </Button>
                    <Button 
                      size="lg" 
                      variant="outline" 
                      className="border-2 border-white/50 text-white hover:bg-white/10 px-8 py-6 text-base font-semibold"
                      asChild
                    >
                      <Link href="/pricing">
                        View Pricing
                      </Link>
                    </Button>
                  </div>
                </div>
              </div>
            </motion.div>
          </div>
        </section>

        <Footer />

        {/* Lightbox */}
        <GalleryLightbox
          item={selectedItem}
          isOpen={isLightboxOpen}
          onClose={() => {
            setIsLightboxOpen(false);
            setSelectedItem(null);
          }}
          onPrev={handlePrev}
          onNext={handleNext}
          hasPrev={hasPrev}
          hasNext={hasNext}
        />
      </div>
    </>
  );
}
