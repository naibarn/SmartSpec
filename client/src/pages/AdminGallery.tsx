/**
 * Admin Gallery Management Page
 * CRUD operations for gallery items (images, videos, websites)
 */

import { useAuth } from "@/_core/hooks/useAuth";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Textarea } from "@/components/ui/textarea";
import { Switch } from "@/components/ui/switch";
import { Badge } from "@/components/ui/badge";
import { Skeleton } from "@/components/ui/skeleton";
import { trpc } from "@/lib/trpc";
import { getLoginUrl } from "@/const";
import {
  Image,
  Video,
  Globe,
  Plus,
  MoreVertical,
  Pencil,
  Trash2,
  Eye,
  EyeOff,
  Star,
  StarOff,
  Upload,
  Search,
  BarChart3,
  ArrowLeft,
  Loader2,
  X,
  Download,
  Heart,
} from "lucide-react";
import { useState, useRef, useCallback } from "react";
import { Link } from "wouter";
import { toast } from "sonner";

type GalleryType = "image" | "video" | "website";
type AspectRatio = "1:1" | "9:16" | "16:9";

interface GalleryItem {
  id: number;
  type: GalleryType;
  title: string;
  description: string | null;
  aspectRatio: AspectRatio;
  fileKey: string | null;
  fileUrl: string | null;
  thumbnailKey: string | null;
  thumbnailUrl: string | null;
  duration: string | null;
  demoUrl: string | null;
  tags: string[] | null;
  views: number;
  likes: number;
  downloads: number;
  isPublished: boolean;
  isFeatured: boolean;
  authorId: number | null;
  authorName: string | null;
  authorAvatar: string | null;
  sortOrder: number;
  createdAt: Date;
  updatedAt: Date;
}

interface FormData {
  type: GalleryType;
  title: string;
  description: string;
  aspectRatio: AspectRatio;
  fileUrl: string;
  thumbnailUrl: string;
  duration: string;
  demoUrl: string;
  tags: string;
  isPublished: boolean;
  isFeatured: boolean;
  authorName: string;
  sortOrder: number;
}

const defaultFormData: FormData = {
  type: "image",
  title: "",
  description: "",
  aspectRatio: "16:9",
  fileUrl: "",
  thumbnailUrl: "",
  duration: "",
  demoUrl: "",
  tags: "",
  isPublished: true,
  isFeatured: false,
  authorName: "",
  sortOrder: 0,
};

export default function AdminGallery() {
  const { user, loading: authLoading } = useAuth();
  const [activeTab, setActiveTab] = useState<"all" | GalleryType>("all");
  const [searchQuery, setSearchQuery] = useState("");
  const [isCreateDialogOpen, setIsCreateDialogOpen] = useState(false);
  const [isEditDialogOpen, setIsEditDialogOpen] = useState(false);
  const [isDeleteDialogOpen, setIsDeleteDialogOpen] = useState(false);
  const [selectedItem, setSelectedItem] = useState<GalleryItem | null>(null);
  const [formData, setFormData] = useState<FormData>(defaultFormData);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const thumbnailInputRef = useRef<HTMLInputElement>(null);

  // tRPC queries
  const utils = trpc.useUtils();
  const { data: items, isLoading } = trpc.gallery.adminList.useQuery({
    type: activeTab === "all" ? undefined : activeTab,
    search: searchQuery || undefined,
    limit: 100,
  });
  const { data: stats } = trpc.gallery.stats.useQuery();

  // tRPC mutations
  const createMutation = trpc.gallery.create.useMutation({
    onSuccess: () => {
      toast.success("Gallery item created successfully");
      setIsCreateDialogOpen(false);
      setFormData(defaultFormData);
      utils.gallery.adminList.invalidate();
      utils.gallery.stats.invalidate();
    },
    onError: (error) => {
      toast.error(`Failed to create: ${error.message}`);
    },
  });

  const updateMutation = trpc.gallery.update.useMutation({
    onSuccess: () => {
      toast.success("Gallery item updated successfully");
      setIsEditDialogOpen(false);
      setSelectedItem(null);
      utils.gallery.adminList.invalidate();
    },
    onError: (error) => {
      toast.error(`Failed to update: ${error.message}`);
    },
  });

  const deleteMutation = trpc.gallery.delete.useMutation({
    onSuccess: () => {
      toast.success("Gallery item deleted successfully");
      setIsDeleteDialogOpen(false);
      setSelectedItem(null);
      utils.gallery.adminList.invalidate();
      utils.gallery.stats.invalidate();
    },
    onError: (error) => {
      toast.error(`Failed to delete: ${error.message}`);
    },
  });

  const togglePublishMutation = trpc.gallery.togglePublish.useMutation({
    onSuccess: (data) => {
      toast.success(data.isPublished ? "Item published" : "Item unpublished");
      utils.gallery.adminList.invalidate();
    },
  });

  const toggleFeaturedMutation = trpc.gallery.toggleFeatured.useMutation({
    onSuccess: (data) => {
      toast.success(data.isFeatured ? "Item featured" : "Item unfeatured");
      utils.gallery.adminList.invalidate();
    },
  });

  const uploadFileMutation = trpc.gallery.uploadFile.useMutation();

  // File upload handler
  const handleFileUpload = useCallback(
    async (file: File, type: "main" | "thumbnail") => {
      setIsUploading(true);
      setUploadProgress(0);

      try {
        // Read file as base64
        const reader = new FileReader();
        const base64Promise = new Promise<string>((resolve, reject) => {
          reader.onload = () => {
            const result = reader.result as string;
            // Remove data URL prefix
            const base64 = result.split(",")[1];
            resolve(base64);
          };
          reader.onerror = reject;
        });
        reader.readAsDataURL(file);
        const fileBase64 = await base64Promise;

        // Determine folder based on file type
        let folder: "images" | "videos" | "thumbnails" | "websites" = "images";
        if (type === "thumbnail") {
          folder = "thumbnails";
        } else if (file.type.startsWith("video/")) {
          folder = "videos";
        }

        setUploadProgress(50);

        const result = await uploadFileMutation.mutateAsync({
          fileName: file.name,
          fileType: file.type,
          fileBase64,
          folder,
        });

        setUploadProgress(100);

        if (type === "main") {
          setFormData((prev) => ({
            ...prev,
            fileUrl: result.fileUrl,
          }));
        } else {
          setFormData((prev) => ({
            ...prev,
            thumbnailUrl: result.fileUrl,
          }));
        }

        toast.success("File uploaded successfully");
      } catch (error) {
        toast.error("Failed to upload file");
        console.error(error);
      } finally {
        setIsUploading(false);
        setUploadProgress(0);
      }
    },
    [uploadFileMutation]
  );

  // Form handlers
  const handleCreate = () => {
    createMutation.mutate({
      type: formData.type,
      title: formData.title,
      description: formData.description || undefined,
      aspectRatio: formData.aspectRatio,
      fileUrl: formData.fileUrl || undefined,
      thumbnailUrl: formData.thumbnailUrl || undefined,
      duration: formData.duration || undefined,
      demoUrl: formData.demoUrl || undefined,
      tags: formData.tags ? formData.tags.split(",").map((t) => t.trim()) : undefined,
      isPublished: formData.isPublished,
      isFeatured: formData.isFeatured,
      authorName: formData.authorName || undefined,
      sortOrder: formData.sortOrder,
    });
  };

  const handleUpdate = () => {
    if (!selectedItem) return;
    updateMutation.mutate({
      id: selectedItem.id,
      data: {
        type: formData.type,
        title: formData.title,
        description: formData.description || undefined,
        aspectRatio: formData.aspectRatio,
        fileUrl: formData.fileUrl || undefined,
        thumbnailUrl: formData.thumbnailUrl || undefined,
        duration: formData.duration || undefined,
        demoUrl: formData.demoUrl || undefined,
        tags: formData.tags ? formData.tags.split(",").map((t) => t.trim()) : undefined,
        isPublished: formData.isPublished,
        isFeatured: formData.isFeatured,
        authorName: formData.authorName || undefined,
        sortOrder: formData.sortOrder,
      },
    });
  };

  const handleDelete = () => {
    if (!selectedItem) return;
    deleteMutation.mutate({ id: selectedItem.id });
  };

  const openEditDialog = (item: GalleryItem) => {
    setSelectedItem(item);
    setFormData({
      type: item.type,
      title: item.title,
      description: item.description || "",
      aspectRatio: item.aspectRatio,
      fileUrl: item.fileUrl || "",
      thumbnailUrl: item.thumbnailUrl || "",
      duration: item.duration || "",
      demoUrl: item.demoUrl || "",
      tags: item.tags?.join(", ") || "",
      isPublished: item.isPublished,
      isFeatured: item.isFeatured,
      authorName: item.authorName || "",
      sortOrder: item.sortOrder,
    });
    setIsEditDialogOpen(true);
  };

  const openDeleteDialog = (item: GalleryItem) => {
    setSelectedItem(item);
    setIsDeleteDialogOpen(true);
  };

  // Auth check
  if (authLoading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <Loader2 className="w-8 h-8 animate-spin text-primary" />
      </div>
    );
  }

  if (!user) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <Card className="w-full max-w-md">
          <CardHeader>
            <CardTitle>Sign in Required</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <p className="text-muted-foreground">
              You need to sign in to access the admin panel.
            </p>
            <Button
              onClick={() => (window.location.href = getLoginUrl())}
              className="w-full"
            >
              Sign In
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  if (user.role !== "admin") {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <Card className="w-full max-w-md">
          <CardHeader>
            <CardTitle>Access Denied</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <p className="text-muted-foreground">
              You don't have permission to access the admin panel.
            </p>
            <Link href="/">
              <Button variant="outline" className="w-full">
                <ArrowLeft className="w-4 h-4 mr-2" />
                Back to Home
              </Button>
            </Link>
          </CardContent>
        </Card>
      </div>
    );
  }

  const getTypeIcon = (type: GalleryType) => {
    switch (type) {
      case "image":
        return <Image className="w-4 h-4" />;
      case "video":
        return <Video className="w-4 h-4" />;
      case "website":
        return <Globe className="w-4 h-4" />;
    }
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="sticky top-0 z-50 border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <div className="container flex h-16 items-center justify-between">
          <div className="flex items-center gap-4">
            <Link href="/">
              <Button variant="ghost" size="icon">
                <ArrowLeft className="w-5 h-5" />
              </Button>
            </Link>
            <h1 className="text-xl font-semibold">Gallery Management</h1>
          </div>
          <Button onClick={() => setIsCreateDialogOpen(true)}>
            <Plus className="w-4 h-4 mr-2" />
            Add Item
          </Button>
        </div>
      </header>

      <main className="container py-8">
        {/* Stats Cards */}
        <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4 mb-8">
          <Card>
            <CardContent className="p-4">
              <div className="flex items-center gap-2 text-muted-foreground mb-1">
                <BarChart3 className="w-4 h-4" />
                <span className="text-sm">Total</span>
              </div>
              <p className="text-2xl font-bold">{stats?.totalItems || 0}</p>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="p-4">
              <div className="flex items-center gap-2 text-muted-foreground mb-1">
                <Image className="w-4 h-4" />
                <span className="text-sm">Images</span>
              </div>
              <p className="text-2xl font-bold">{stats?.totalImages || 0}</p>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="p-4">
              <div className="flex items-center gap-2 text-muted-foreground mb-1">
                <Video className="w-4 h-4" />
                <span className="text-sm">Videos</span>
              </div>
              <p className="text-2xl font-bold">{stats?.totalVideos || 0}</p>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="p-4">
              <div className="flex items-center gap-2 text-muted-foreground mb-1">
                <Globe className="w-4 h-4" />
                <span className="text-sm">Websites</span>
              </div>
              <p className="text-2xl font-bold">{stats?.totalWebsites || 0}</p>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="p-4">
              <div className="flex items-center gap-2 text-muted-foreground mb-1">
                <Eye className="w-4 h-4" />
                <span className="text-sm">Views</span>
              </div>
              <p className="text-2xl font-bold">{stats?.totalViews || 0}</p>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="p-4">
              <div className="flex items-center gap-2 text-muted-foreground mb-1">
                <Heart className="w-4 h-4" />
                <span className="text-sm">Likes</span>
              </div>
              <p className="text-2xl font-bold">{stats?.totalLikes || 0}</p>
            </CardContent>
          </Card>
        </div>

        {/* Filters */}
        <div className="flex flex-col sm:flex-row gap-4 mb-6">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
            <Input
              placeholder="Search gallery items..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-10"
            />
          </div>
          <Tabs value={activeTab} onValueChange={(v) => setActiveTab(v as typeof activeTab)}>
            <TabsList>
              <TabsTrigger value="all">All</TabsTrigger>
              <TabsTrigger value="image">
                <Image className="w-4 h-4 mr-1" />
                Images
              </TabsTrigger>
              <TabsTrigger value="video">
                <Video className="w-4 h-4 mr-1" />
                Videos
              </TabsTrigger>
              <TabsTrigger value="website">
                <Globe className="w-4 h-4 mr-1" />
                Websites
              </TabsTrigger>
            </TabsList>
          </Tabs>
        </div>

        {/* Gallery Grid */}
        {isLoading ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {[...Array(8)].map((_, i) => (
              <Card key={i}>
                <Skeleton className="aspect-video" />
                <CardContent className="p-4">
                  <Skeleton className="h-5 w-3/4 mb-2" />
                  <Skeleton className="h-4 w-1/2" />
                </CardContent>
              </Card>
            ))}
          </div>
        ) : items && items.length > 0 ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {items.map((item) => (
              <Card key={item.id} className="group overflow-hidden">
                <div className="relative aspect-video bg-muted">
                  {item.thumbnailUrl || item.fileUrl ? (
                    <img
                      src={item.thumbnailUrl || item.fileUrl || ""}
                      alt={item.title}
                      className="w-full h-full object-cover"
                    />
                  ) : (
                    <div className="w-full h-full flex items-center justify-center">
                      {getTypeIcon(item.type)}
                    </div>
                  )}
                  
                  {/* Status badges */}
                  <div className="absolute top-2 left-2 flex gap-1">
                    {!item.isPublished && (
                      <Badge variant="secondary" className="bg-yellow-500/90 text-white">
                        <EyeOff className="w-3 h-3 mr-1" />
                        Draft
                      </Badge>
                    )}
                    {item.isFeatured && (
                      <Badge variant="secondary" className="bg-violet-500/90 text-white">
                        <Star className="w-3 h-3 mr-1" />
                        Featured
                      </Badge>
                    )}
                  </div>

                  {/* Type badge */}
                  <Badge
                    variant="secondary"
                    className="absolute top-2 right-2 bg-black/50 text-white"
                  >
                    {getTypeIcon(item.type)}
                    <span className="ml-1 capitalize">{item.type}</span>
                  </Badge>

                  {/* Duration for videos */}
                  {item.type === "video" && item.duration && (
                    <Badge
                      variant="secondary"
                      className="absolute bottom-2 right-2 bg-black/70 text-white"
                    >
                      {item.duration}
                    </Badge>
                  )}
                </div>

                <CardContent className="p-4">
                  <div className="flex items-start justify-between gap-2">
                    <div className="min-w-0 flex-1">
                      <h3 className="font-medium truncate">{item.title}</h3>
                      <p className="text-sm text-muted-foreground truncate">
                        {item.aspectRatio} • {item.views} views
                      </p>
                    </div>
                    <DropdownMenu>
                      <DropdownMenuTrigger asChild>
                        <Button variant="ghost" size="icon" className="shrink-0">
                          <MoreVertical className="w-4 h-4" />
                        </Button>
                      </DropdownMenuTrigger>
                      <DropdownMenuContent align="end">
                        <DropdownMenuItem onClick={() => openEditDialog(item)}>
                          <Pencil className="w-4 h-4 mr-2" />
                          Edit
                        </DropdownMenuItem>
                        <DropdownMenuItem
                          onClick={() => togglePublishMutation.mutate({ id: item.id })}
                        >
                          {item.isPublished ? (
                            <>
                              <EyeOff className="w-4 h-4 mr-2" />
                              Unpublish
                            </>
                          ) : (
                            <>
                              <Eye className="w-4 h-4 mr-2" />
                              Publish
                            </>
                          )}
                        </DropdownMenuItem>
                        <DropdownMenuItem
                          onClick={() => toggleFeaturedMutation.mutate({ id: item.id })}
                        >
                          {item.isFeatured ? (
                            <>
                              <StarOff className="w-4 h-4 mr-2" />
                              Unfeature
                            </>
                          ) : (
                            <>
                              <Star className="w-4 h-4 mr-2" />
                              Feature
                            </>
                          )}
                        </DropdownMenuItem>
                        <DropdownMenuItem
                          onClick={() => openDeleteDialog(item)}
                          className="text-destructive"
                        >
                          <Trash2 className="w-4 h-4 mr-2" />
                          Delete
                        </DropdownMenuItem>
                      </DropdownMenuContent>
                    </DropdownMenu>
                  </div>

                  {/* Stats */}
                  <div className="flex items-center gap-4 mt-3 text-sm text-muted-foreground">
                    <span className="flex items-center gap-1">
                      <Eye className="w-3 h-3" />
                      {item.views}
                    </span>
                    <span className="flex items-center gap-1">
                      <Heart className="w-3 h-3" />
                      {item.likes}
                    </span>
                    {item.type === "image" && (
                      <span className="flex items-center gap-1">
                        <Download className="w-3 h-3" />
                        {item.downloads}
                      </span>
                    )}
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        ) : (
          <Card className="p-12">
            <div className="text-center">
              <div className="w-16 h-16 rounded-full bg-muted flex items-center justify-center mx-auto mb-4">
                <Image className="w-8 h-8 text-muted-foreground" />
              </div>
              <h3 className="text-lg font-medium mb-2">No gallery items yet</h3>
              <p className="text-muted-foreground mb-4">
                Get started by adding your first gallery item.
              </p>
              <Button onClick={() => setIsCreateDialogOpen(true)}>
                <Plus className="w-4 h-4 mr-2" />
                Add Item
              </Button>
            </div>
          </Card>
        )}
      </main>

      {/* Create/Edit Dialog */}
      <Dialog
        open={isCreateDialogOpen || isEditDialogOpen}
        onOpenChange={(open) => {
          if (!open) {
            setIsCreateDialogOpen(false);
            setIsEditDialogOpen(false);
            setSelectedItem(null);
            setFormData(defaultFormData);
          }
        }}
      >
        <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle>
              {isEditDialogOpen ? "Edit Gallery Item" : "Add Gallery Item"}
            </DialogTitle>
            <DialogDescription>
              {isEditDialogOpen
                ? "Update the details of this gallery item."
                : "Add a new image, video, or website demo to the gallery."}
            </DialogDescription>
          </DialogHeader>

          <div className="grid gap-6 py-4">
            {/* Type & Aspect Ratio */}
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label>Type</Label>
                <Select
                  value={formData.type}
                  onValueChange={(v) =>
                    setFormData((prev) => ({ ...prev, type: v as GalleryType }))
                  }
                >
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="image">
                      <div className="flex items-center gap-2">
                        <Image className="w-4 h-4" />
                        Image
                      </div>
                    </SelectItem>
                    <SelectItem value="video">
                      <div className="flex items-center gap-2">
                        <Video className="w-4 h-4" />
                        Video
                      </div>
                    </SelectItem>
                    <SelectItem value="website">
                      <div className="flex items-center gap-2">
                        <Globe className="w-4 h-4" />
                        Website
                      </div>
                    </SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label>Aspect Ratio</Label>
                <Select
                  value={formData.aspectRatio}
                  onValueChange={(v) =>
                    setFormData((prev) => ({ ...prev, aspectRatio: v as AspectRatio }))
                  }
                >
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="1:1">1:1 (Square)</SelectItem>
                    <SelectItem value="9:16">9:16 (Portrait)</SelectItem>
                    <SelectItem value="16:9">16:9 (Landscape)</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>

            {/* Title */}
            <div className="space-y-2">
              <Label>Title</Label>
              <Input
                value={formData.title}
                onChange={(e) =>
                  setFormData((prev) => ({ ...prev, title: e.target.value }))
                }
                placeholder="Enter title..."
              />
            </div>

            {/* Description */}
            <div className="space-y-2">
              <Label>Description</Label>
              <Textarea
                value={formData.description}
                onChange={(e) =>
                  setFormData((prev) => ({ ...prev, description: e.target.value }))
                }
                placeholder="Enter description..."
                rows={3}
              />
            </div>

            {/* File Upload */}
            <div className="space-y-2">
              <Label>
                {formData.type === "image"
                  ? "Image"
                  : formData.type === "video"
                  ? "Video"
                  : "Screenshot"}
              </Label>
              <div className="flex gap-2">
                <Input
                  value={formData.fileUrl}
                  onChange={(e) =>
                    setFormData((prev) => ({ ...prev, fileUrl: e.target.value }))
                  }
                  placeholder="Enter URL or upload file..."
                  className="flex-1"
                />
                <Button
                  type="button"
                  variant="outline"
                  onClick={() => fileInputRef.current?.click()}
                  disabled={isUploading}
                >
                  {isUploading ? (
                    <Loader2 className="w-4 h-4 animate-spin" />
                  ) : (
                    <Upload className="w-4 h-4" />
                  )}
                </Button>
                <input
                  ref={fileInputRef}
                  type="file"
                  accept={
                    formData.type === "video" ? "video/*" : "image/*"
                  }
                  className="hidden"
                  onChange={(e) => {
                    const file = e.target.files?.[0];
                    if (file) handleFileUpload(file, "main");
                  }}
                />
              </div>
              {formData.fileUrl && (
                <div className="relative aspect-video bg-muted rounded-lg overflow-hidden mt-2">
                  {formData.type === "video" ? (
                    <video
                      src={formData.fileUrl}
                      className="w-full h-full object-cover"
                      controls
                    />
                  ) : (
                    <img
                      src={formData.fileUrl}
                      alt="Preview"
                      className="w-full h-full object-cover"
                    />
                  )}
                  <Button
                    variant="destructive"
                    size="icon"
                    className="absolute top-2 right-2"
                    onClick={() =>
                      setFormData((prev) => ({ ...prev, fileUrl: "" }))
                    }
                  >
                    <X className="w-4 h-4" />
                  </Button>
                </div>
              )}
            </div>

            {/* Thumbnail (for videos and websites) */}
            {(formData.type === "video" || formData.type === "website") && (
              <div className="space-y-2">
                <Label>Thumbnail</Label>
                <div className="flex gap-2">
                  <Input
                    value={formData.thumbnailUrl}
                    onChange={(e) =>
                      setFormData((prev) => ({ ...prev, thumbnailUrl: e.target.value }))
                    }
                    placeholder="Enter thumbnail URL or upload..."
                    className="flex-1"
                  />
                  <Button
                    type="button"
                    variant="outline"
                    onClick={() => thumbnailInputRef.current?.click()}
                    disabled={isUploading}
                  >
                    {isUploading ? (
                      <Loader2 className="w-4 h-4 animate-spin" />
                    ) : (
                      <Upload className="w-4 h-4" />
                    )}
                  </Button>
                  <input
                    ref={thumbnailInputRef}
                    type="file"
                    accept="image/*"
                    className="hidden"
                    onChange={(e) => {
                      const file = e.target.files?.[0];
                      if (file) handleFileUpload(file, "thumbnail");
                    }}
                  />
                </div>
              </div>
            )}

            {/* Duration (for videos) */}
            {formData.type === "video" && (
              <div className="space-y-2">
                <Label>Duration</Label>
                <Input
                  value={formData.duration}
                  onChange={(e) =>
                    setFormData((prev) => ({ ...prev, duration: e.target.value }))
                  }
                  placeholder="e.g., 2:30"
                />
              </div>
            )}

            {/* Demo URL (for websites) */}
            {formData.type === "website" && (
              <div className="space-y-2">
                <Label>Demo URL</Label>
                <Input
                  value={formData.demoUrl}
                  onChange={(e) =>
                    setFormData((prev) => ({ ...prev, demoUrl: e.target.value }))
                  }
                  placeholder="https://demo.example.com"
                />
              </div>
            )}

            {/* Tags */}
            <div className="space-y-2">
              <Label>Tags (comma separated)</Label>
              <Input
                value={formData.tags}
                onChange={(e) =>
                  setFormData((prev) => ({ ...prev, tags: e.target.value }))
                }
                placeholder="e.g., landscape, nature, photography"
              />
            </div>

            {/* Author Name */}
            <div className="space-y-2">
              <Label>Author Name</Label>
              <Input
                value={formData.authorName}
                onChange={(e) =>
                  setFormData((prev) => ({ ...prev, authorName: e.target.value }))
                }
                placeholder="Enter author name..."
              />
            </div>

            {/* Sort Order */}
            <div className="space-y-2">
              <Label>Sort Order</Label>
              <Input
                type="number"
                value={formData.sortOrder}
                onChange={(e) =>
                  setFormData((prev) => ({
                    ...prev,
                    sortOrder: parseInt(e.target.value) || 0,
                  }))
                }
                placeholder="0"
              />
            </div>

            {/* Toggles */}
            <div className="flex items-center gap-8">
              <div className="flex items-center gap-2">
                <Switch
                  checked={formData.isPublished}
                  onCheckedChange={(checked) =>
                    setFormData((prev) => ({ ...prev, isPublished: checked }))
                  }
                />
                <Label>Published</Label>
              </div>
              <div className="flex items-center gap-2">
                <Switch
                  checked={formData.isFeatured}
                  onCheckedChange={(checked) =>
                    setFormData((prev) => ({ ...prev, isFeatured: checked }))
                  }
                />
                <Label>Featured</Label>
              </div>
            </div>
          </div>

          <DialogFooter>
            <Button
              variant="outline"
              onClick={() => {
                setIsCreateDialogOpen(false);
                setIsEditDialogOpen(false);
                setSelectedItem(null);
                setFormData(defaultFormData);
              }}
            >
              Cancel
            </Button>
            <Button
              onClick={isEditDialogOpen ? handleUpdate : handleCreate}
              disabled={
                !formData.title ||
                createMutation.isPending ||
                updateMutation.isPending
              }
            >
              {(createMutation.isPending || updateMutation.isPending) && (
                <Loader2 className="w-4 h-4 mr-2 animate-spin" />
              )}
              {isEditDialogOpen ? "Save Changes" : "Create"}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Delete Confirmation Dialog */}
      <Dialog open={isDeleteDialogOpen} onOpenChange={setIsDeleteDialogOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Delete Gallery Item</DialogTitle>
            <DialogDescription>
              Are you sure you want to delete "{selectedItem?.title}"? This action
              cannot be undone.
            </DialogDescription>
          </DialogHeader>
          <DialogFooter>
            <Button
              variant="outline"
              onClick={() => {
                setIsDeleteDialogOpen(false);
                setSelectedItem(null);
              }}
            >
              Cancel
            </Button>
            <Button
              variant="destructive"
              onClick={handleDelete}
              disabled={deleteMutation.isPending}
            >
              {deleteMutation.isPending && (
                <Loader2 className="w-4 h-4 mr-2 animate-spin" />
              )}
              Delete
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
}
