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

import { useState, useMemo } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Navbar } from '@/components/Navbar';
import { Footer } from '@/components/Footer';
import { trpc } from '@/lib/trpc';
import {
  Image as ImageIcon,
  Video,
  Globe,
  Search,
  Grid3X3,
  Heart,
  Eye,
  Download,
  Share2,
  ExternalLink,
  Play,
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
import { toast } from 'sonner';

// Types
type ContentType = 'all' | 'image' | 'video' | 'website';
type AspectRatio = '1:1' | '9:16' | '16:9';
type SortOption = 'newest' | 'popular' | 'trending';

interface GalleryItem {
  id: number;
  type: 'image' | 'video' | 'website';
  title: string;
  description: string | null;
  thumbnailUrl: string | null;
  fileUrl: string | null;
  aspectRatio: AspectRatio;
  authorName: string | null;
  authorAvatar: string | null;
  views: number;
  likes: number;
  downloads: number;
  tags: string[] | null;
  createdAt: Date;
  demoUrl: string | null;
  duration: string | null;
}

// Aspect ratio styles
const aspectRatioStyles: Record<AspectRatio, string> = {
  '1:1': 'aspect-square',
  '9:16': 'aspect-[9/16]',
  '16:9': 'aspect-video',
};

// Animation variants
const fadeInUp = {
  initial: { opacity: 0, y: 20 },
  animate: { opacity: 1, y: 0 },
  exit: { opacity: 0, y: -20 }
};

const staggerContainer = {
  animate: {
    transition: {
      staggerChildren: 0.05
    }
  }
};

// Format number helper
const formatNumber = (num: number): string => {
  if (num >= 1000000) return (num / 1000000).toFixed(1) + 'M';
  if (num >= 1000) return (num / 1000).toFixed(1) + 'K';
  return num.toString();
};

// Format date helper
const formatDate = (date: Date): string => {
  return new Date(date).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  });
};

export default function Gallery() {
  const [activeTab, setActiveTab] = useState<ContentType>('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [sortBy, setSortBy] = useState<SortOption>('newest');
  const [selectedItem, setSelectedItem] = useState<GalleryItem | null>(null);
  const [isLightboxOpen, setIsLightboxOpen] = useState(false);

  // Fetch gallery items from API
  const { data: items, isLoading, error } = trpc.gallery.list.useQuery({
    type: activeTab === 'all' ? undefined : activeTab,
    search: searchQuery || undefined,
    limit: 50,
  });

  // Mutations
  const viewMutation = trpc.gallery.view.useMutation();
  const likeMutation = trpc.gallery.like.useMutation();
  const downloadMutation = trpc.gallery.download.useMutation();

  // Tab configuration
  const tabs = useMemo(() => {
    const allCount = items?.length || 0;
    const imageCount = items?.filter(i => i.type === 'image').length || 0;
    const videoCount = items?.filter(i => i.type === 'video').length || 0;
    const websiteCount = items?.filter(i => i.type === 'website').length || 0;

    return [
      { id: 'all' as ContentType, label: 'All', icon: Grid3X3, count: allCount },
      { id: 'image' as ContentType, label: 'Images', icon: ImageIcon, count: imageCount },
      { id: 'video' as ContentType, label: 'Videos', icon: Video, count: videoCount },
      { id: 'website' as ContentType, label: 'Websites', icon: Globe, count: websiteCount },
    ];
  }, [items]);

  // Sort items
  const sortedItems = useMemo(() => {
    if (!items) return [];
    
    const sorted = [...items];
    switch (sortBy) {
      case 'popular':
        return sorted.sort((a, b) => b.views - a.views);
      case 'trending':
        return sorted.sort((a, b) => b.likes - a.likes);
      case 'newest':
      default:
        return sorted.sort((a, b) => new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime());
    }
  }, [items, sortBy]);

  // Handle item click
  const handleItemClick = (item: GalleryItem) => {
    setSelectedItem(item);
    setIsLightboxOpen(true);
    viewMutation.mutate({ id: item.id });
  };

  // Handle like
  const handleLike = (item: GalleryItem, e: React.MouseEvent) => {
    e.stopPropagation();
    likeMutation.mutate({ id: item.id });
    toast.success('Added to favorites!');
  };

  // Handle download
  const handleDownload = (item: GalleryItem, e: React.MouseEvent) => {
    e.stopPropagation();
    if (item.fileUrl) {
      downloadMutation.mutate({ id: item.id });
      window.open(item.fileUrl, '_blank');
      toast.success('Download started!');
    }
  };

  // Handle share
  const handleShare = (item: GalleryItem, e: React.MouseEvent) => {
    e.stopPropagation();
    const url = `${window.location.origin}/gallery?item=${item.id}`;
    navigator.clipboard.writeText(url);
    toast.success('Link copied to clipboard!');
  };

  // Navigate lightbox
  const navigateLightbox = (direction: 'prev' | 'next') => {
    if (!selectedItem || !sortedItems.length) return;
    const currentIndex = sortedItems.findIndex(i => i.id === selectedItem.id);
    const newIndex = direction === 'prev'
      ? (currentIndex - 1 + sortedItems.length) % sortedItems.length
      : (currentIndex + 1) % sortedItems.length;
    setSelectedItem(sortedItems[newIndex]);
    viewMutation.mutate({ id: sortedItems[newIndex].id });
  };

  // Get type icon
  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'image': return <ImageIcon className="w-4 h-4" />;
      case 'video': return <Video className="w-4 h-4" />;
      case 'website': return <Globe className="w-4 h-4" />;
      default: return null;
    }
  };

  // Structured data for SEO
  const structuredData = {
    "@context": "https://schema.org",
    "@type": "CollectionPage",
    "name": "SmartSpec Pro Gallery",
    "description": "Explore AI-generated images, videos, and website demos created with SmartSpec Pro",
    "url": `${window.location.origin}/gallery`,
    "mainEntity": {
      "@type": "ItemList",
      "numberOfItems": sortedItems.length,
      "itemListElement": sortedItems.slice(0, 10).map((item, index) => ({
        "@type": "ListItem",
        "position": index + 1,
        "item": {
          "@type": item.type === 'video' ? 'VideoObject' : item.type === 'website' ? 'WebPage' : 'ImageObject',
          "name": item.title,
          "description": item.description,
          "thumbnailUrl": item.thumbnailUrl || item.fileUrl,
          "dateCreated": item.createdAt,
        }
      }))
    }
  };

  return (
    <>
      <Helmet>
        <title>Gallery - SmartSpec Pro | AI-Generated Content Showcase</title>
        <meta name="description" content="Explore our gallery of AI-generated images, videos, and website demos. See what's possible with SmartSpec Pro's advanced AI capabilities." />
        <meta name="keywords" content="AI gallery, AI images, AI videos, website demos, SmartSpec Pro, AI art, generated content" />
        
        {/* Open Graph */}
        <meta property="og:title" content="Gallery - SmartSpec Pro" />
        <meta property="og:description" content="Explore AI-generated images, videos, and website demos" />
        <meta property="og:type" content="website" />
        <meta property="og:url" content={`${window.location.origin}/gallery`} />
        
        {/* Twitter Card */}
        <meta name="twitter:card" content="summary_large_image" />
        <meta name="twitter:title" content="Gallery - SmartSpec Pro" />
        <meta name="twitter:description" content="Explore AI-generated images, videos, and website demos" />
        
        {/* Structured Data */}
        <script type="application/ld+json">
          {JSON.stringify(structuredData)}
        </script>
      </Helmet>

      <div className="min-h-screen bg-background">
        <Navbar />
        
        {/* Hero Section */}
        <section className="relative pt-24 pb-12 overflow-hidden">
          {/* Background */}
          <div className="absolute inset-0">
            <div className="absolute top-0 left-1/4 w-96 h-96 bg-violet-500/20 rounded-full blur-3xl" />
            <div className="absolute bottom-0 right-1/4 w-96 h-96 bg-teal-500/20 rounded-full blur-3xl" />
          </div>
          
          <div className="container relative mx-auto px-4 sm:px-6 lg:px-8">
            <motion.div 
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="text-center max-w-3xl mx-auto"
            >
              <span className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-primary/10 text-primary text-sm font-medium mb-4">
                <Sparkles className="w-4 h-4" />
                AI-Powered Creations
              </span>
              <h1 className="text-4xl sm:text-5xl font-bold mb-4">
                Explore Our <span className="gradient-text">Gallery</span>
              </h1>
              <p className="text-lg text-muted-foreground">
                Discover stunning AI-generated images, videos, and website demos created with SmartSpec Pro.
              </p>
            </motion.div>
          </div>
        </section>

        {/* Filters Section */}
        <section className="sticky top-16 z-40 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 border-b">
          <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-4">
            <div className="flex flex-col lg:flex-row gap-4 items-center justify-between">
              {/* Tabs */}
              <div className="flex gap-2 overflow-x-auto pb-2 lg:pb-0 w-full lg:w-auto">
                {tabs.map((tab) => (
                  <Button
                    key={tab.id}
                    variant={activeTab === tab.id ? "default" : "outline"}
                    size="sm"
                    onClick={() => setActiveTab(tab.id)}
                    className="whitespace-nowrap"
                  >
                    <tab.icon className="w-4 h-4 mr-2" />
                    {tab.label}
                    <span className="ml-2 px-2 py-0.5 rounded-full bg-background/20 text-xs">
                      {tab.count}
                    </span>
                  </Button>
                ))}
              </div>

              {/* Search & Sort */}
              <div className="flex gap-3 w-full lg:w-auto">
                <div className="relative flex-1 lg:w-64">
                  <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
                  <Input
                    placeholder="Search gallery..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="pl-10"
                  />
                </div>
                <Select value={sortBy} onValueChange={(v) => setSortBy(v as SortOption)}>
                  <SelectTrigger className="w-32">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="newest">Newest</SelectItem>
                    <SelectItem value="popular">Popular</SelectItem>
                    <SelectItem value="trending">Trending</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>
          </div>
        </section>

        {/* Gallery Grid */}
        <section className="py-12">
          <div className="container mx-auto px-4 sm:px-6 lg:px-8">
            {isLoading ? (
              <div className="flex items-center justify-center py-20">
                <Loader2 className="w-8 h-8 animate-spin text-primary" />
              </div>
            ) : error ? (
              <div className="text-center py-20">
                <p className="text-muted-foreground">Failed to load gallery items</p>
              </div>
            ) : sortedItems.length === 0 ? (
              <div className="text-center py-20">
                <div className="w-20 h-20 rounded-full bg-muted flex items-center justify-center mx-auto mb-4">
                  <ImageIcon className="w-10 h-10 text-muted-foreground" />
                </div>
                <h3 className="text-xl font-semibold mb-2">No items found</h3>
                <p className="text-muted-foreground">
                  {searchQuery ? 'Try a different search term' : 'Gallery is empty'}
                </p>
              </div>
            ) : (
              <motion.div
                variants={staggerContainer}
                initial="initial"
                animate="animate"
                className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6"
              >
                <AnimatePresence mode="popLayout">
                  {sortedItems.map((item) => (
                    <motion.div
                      key={item.id}
                      variants={fadeInUp}
                      layout
                      layoutId={`gallery-item-${item.id}`}
                    >
                      <Card 
                        className="group cursor-pointer overflow-hidden hover:shadow-xl transition-all duration-300"
                        onClick={() => handleItemClick(item)}
                      >
                        {/* Thumbnail */}
                        <div className={`relative ${aspectRatioStyles[item.aspectRatio]} bg-muted overflow-hidden`}>
                          <img
                            src={item.thumbnailUrl || item.fileUrl || '/placeholder.jpg'}
                            alt={item.title}
                            className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                            loading="lazy"
                          />
                          
                          {/* Overlay */}
                          <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />
                          
                          {/* Type Badge */}
                          <div className="absolute top-3 left-3">
                            <span className="inline-flex items-center gap-1 px-2 py-1 rounded-full bg-black/50 text-white text-xs backdrop-blur-sm">
                              {getTypeIcon(item.type)}
                              <span className="capitalize">{item.type}</span>
                            </span>
                          </div>

                          {/* Duration for videos */}
                          {item.type === 'video' && item.duration && (
                            <div className="absolute bottom-3 right-3">
                              <span className="inline-flex items-center gap-1 px-2 py-1 rounded bg-black/70 text-white text-xs">
                                <Clock className="w-3 h-3" />
                                {item.duration}
                              </span>
                            </div>
                          )}

                          {/* Play button for videos */}
                          {item.type === 'video' && (
                            <div className="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
                              <div className="w-16 h-16 rounded-full bg-white/90 flex items-center justify-center">
                                <Play className="w-8 h-8 text-primary ml-1" />
                              </div>
                            </div>
                          )}

                          {/* Actions */}
                          <div className="absolute bottom-3 left-3 right-3 flex justify-between items-center opacity-0 group-hover:opacity-100 transition-opacity">
                            <div className="flex gap-2">
                              <Button
                                size="icon"
                                variant="secondary"
                                className="h-8 w-8 bg-white/90 hover:bg-white"
                                onClick={(e) => handleLike(item, e)}
                              >
                                <Heart className="w-4 h-4" />
                              </Button>
                              {item.type === 'image' && (
                                <Button
                                  size="icon"
                                  variant="secondary"
                                  className="h-8 w-8 bg-white/90 hover:bg-white"
                                  onClick={(e) => handleDownload(item, e)}
                                >
                                  <Download className="w-4 h-4" />
                                </Button>
                              )}
                              <Button
                                size="icon"
                                variant="secondary"
                                className="h-8 w-8 bg-white/90 hover:bg-white"
                                onClick={(e) => handleShare(item, e)}
                              >
                                <Share2 className="w-4 h-4" />
                              </Button>
                            </div>
                            {item.type === 'website' && item.demoUrl && (
                              <Button
                                size="sm"
                                className="h-8 bg-white/90 hover:bg-white text-foreground"
                                onClick={(e) => {
                                  e.stopPropagation();
                                  window.open(item.demoUrl!, '_blank');
                                }}
                              >
                                <ExternalLink className="w-4 h-4 mr-1" />
                                Demo
                              </Button>
                            )}
                          </div>
                        </div>

                        {/* Content */}
                        <CardContent className="p-4">
                          <h3 className="font-semibold truncate mb-1">{item.title}</h3>
                          
                          {/* Author */}
                          {item.authorName && (
                            <div className="flex items-center gap-2 mb-2">
                              <div className="w-5 h-5 rounded-full bg-gradient-to-br from-violet-500 to-teal-400 flex items-center justify-center text-white text-xs">
                                {item.authorName.charAt(0)}
                              </div>
                              <span className="text-sm text-muted-foreground truncate">
                                {item.authorName}
                              </span>
                            </div>
                          )}

                          {/* Stats */}
                          <div className="flex items-center gap-4 text-sm text-muted-foreground">
                            <span className="flex items-center gap-1">
                              <Eye className="w-4 h-4" />
                              {formatNumber(item.views)}
                            </span>
                            <span className="flex items-center gap-1">
                              <Heart className="w-4 h-4" />
                              {formatNumber(item.likes)}
                            </span>
                            {item.type === 'image' && (
                              <span className="flex items-center gap-1">
                                <Download className="w-4 h-4" />
                                {formatNumber(item.downloads)}
                              </span>
                            )}
                          </div>
                        </CardContent>
                      </Card>
                    </motion.div>
                  ))}
                </AnimatePresence>
              </motion.div>
            )}
          </div>
        </section>

        {/* Lightbox */}
        <Dialog open={isLightboxOpen} onOpenChange={setIsLightboxOpen}>
          <DialogContent className="max-w-5xl p-0 overflow-hidden">
            {selectedItem && (
              <div className="relative">
                {/* Navigation */}
                <Button
                  variant="ghost"
                  size="icon"
                  className="absolute left-4 top-1/2 -translate-y-1/2 z-10 bg-black/50 hover:bg-black/70 text-white"
                  onClick={() => navigateLightbox('prev')}
                >
                  <ChevronLeft className="w-6 h-6" />
                </Button>
                <Button
                  variant="ghost"
                  size="icon"
                  className="absolute right-4 top-1/2 -translate-y-1/2 z-10 bg-black/50 hover:bg-black/70 text-white"
                  onClick={() => navigateLightbox('next')}
                >
                  <ChevronRight className="w-6 h-6" />
                </Button>

                {/* Content */}
                <div className="aspect-video bg-black flex items-center justify-center">
                  {selectedItem.type === 'video' ? (
                    <video
                      src={selectedItem.fileUrl || ''}
                      controls
                      autoPlay
                      className="max-w-full max-h-full"
                    />
                  ) : (
                    <img
                      src={selectedItem.fileUrl || selectedItem.thumbnailUrl || ''}
                      alt={selectedItem.title}
                      className="max-w-full max-h-full object-contain"
                    />
                  )}
                </div>

                {/* Info */}
                <div className="p-6 bg-background">
                  <DialogHeader>
                    <DialogTitle className="text-xl">{selectedItem.title}</DialogTitle>
                  </DialogHeader>
                  
                  {selectedItem.description && (
                    <p className="text-muted-foreground mt-2">{selectedItem.description}</p>
                  )}

                  <div className="flex flex-wrap items-center gap-4 mt-4">
                    {/* Author */}
                    {selectedItem.authorName && (
                      <div className="flex items-center gap-2">
                        <User className="w-4 h-4 text-muted-foreground" />
                        <span>{selectedItem.authorName}</span>
                      </div>
                    )}
                    
                    {/* Date */}
                    <div className="flex items-center gap-2 text-muted-foreground">
                      <Clock className="w-4 h-4" />
                      <span>{formatDate(selectedItem.createdAt)}</span>
                    </div>

                    {/* Stats */}
                    <div className="flex items-center gap-4 text-muted-foreground">
                      <span className="flex items-center gap-1">
                        <Eye className="w-4 h-4" />
                        {formatNumber(selectedItem.views)}
                      </span>
                      <span className="flex items-center gap-1">
                        <Heart className="w-4 h-4" />
                        {formatNumber(selectedItem.likes)}
                      </span>
                    </div>
                  </div>

                  {/* Tags */}
                  {selectedItem.tags && selectedItem.tags.length > 0 && (
                    <div className="flex flex-wrap gap-2 mt-4">
                      {selectedItem.tags.map((tag, index) => (
                        <span
                          key={index}
                          className="inline-flex items-center gap-1 px-2 py-1 rounded-full bg-muted text-sm"
                        >
                          <Tag className="w-3 h-3" />
                          {tag}
                        </span>
                      ))}
                    </div>
                  )}

                  {/* Actions */}
                  <div className="flex gap-3 mt-6">
                    <Button onClick={(e) => handleLike(selectedItem, e)}>
                      <Heart className="w-4 h-4 mr-2" />
                      Like
                    </Button>
                    {selectedItem.type === 'image' && (
                      <Button variant="outline" onClick={(e) => handleDownload(selectedItem, e)}>
                        <Download className="w-4 h-4 mr-2" />
                        Download
                      </Button>
                    )}
                    <Button variant="outline" onClick={(e) => handleShare(selectedItem, e)}>
                      <Share2 className="w-4 h-4 mr-2" />
                      Share
                    </Button>
                    {selectedItem.type === 'website' && selectedItem.demoUrl && (
                      <Button
                        variant="outline"
                        onClick={() => window.open(selectedItem.demoUrl!, '_blank')}
                      >
                        <ExternalLink className="w-4 h-4 mr-2" />
                        View Demo
                      </Button>
                    )}
                  </div>
                </div>
              </div>
            )}
          </DialogContent>
        </Dialog>

        <Footer />
      </div>
    </>
  );
}
