import { describe, expect, it, vi, beforeEach } from "vitest";
import { appRouter } from "./routers";
import type { TrpcContext } from "./_core/context";
import * as db from "./db";

// Mock the database functions
vi.mock("./db", () => ({
  getGalleryItems: vi.fn(),
  getGalleryItemById: vi.fn(),
  createGalleryItem: vi.fn(),
  updateGalleryItem: vi.fn(),
  deleteGalleryItem: vi.fn(),
  incrementGalleryViews: vi.fn(),
  incrementGalleryLikes: vi.fn(),
  incrementGalleryDownloads: vi.fn(),
  getGalleryStats: vi.fn(),
}));

// Mock storage
vi.mock("./storage", () => ({
  storagePut: vi.fn().mockResolvedValue({ key: "test-key", url: "https://example.com/test.jpg" }),
}));

type AuthenticatedUser = NonNullable<TrpcContext["user"]>;

function createPublicContext(): TrpcContext {
  return {
    user: null,
    req: {
      protocol: "https",
      headers: {},
    } as TrpcContext["req"],
    res: {
      clearCookie: vi.fn(),
    } as unknown as TrpcContext["res"],
  };
}

function createUserContext(): TrpcContext {
  const user: AuthenticatedUser = {
    id: 1,
    openId: "test-user",
    email: "user@example.com",
    name: "Test User",
    loginMethod: "manus",
    role: "user",
    createdAt: new Date(),
    updatedAt: new Date(),
    lastSignedIn: new Date(),
  };

  return {
    user,
    req: {
      protocol: "https",
      headers: {},
    } as TrpcContext["req"],
    res: {
      clearCookie: vi.fn(),
    } as unknown as TrpcContext["res"],
  };
}

function createAdminContext(): TrpcContext {
  const user: AuthenticatedUser = {
    id: 1,
    openId: "admin-user",
    email: "admin@example.com",
    name: "Admin User",
    loginMethod: "manus",
    role: "admin",
    createdAt: new Date(),
    updatedAt: new Date(),
    lastSignedIn: new Date(),
  };

  return {
    user,
    req: {
      protocol: "https",
      headers: {},
    } as TrpcContext["req"],
    res: {
      clearCookie: vi.fn(),
    } as unknown as TrpcContext["res"],
  };
}

const mockGalleryItem = {
  id: 1,
  type: "image" as const,
  title: "Test Image",
  description: "A test image",
  aspectRatio: "16:9" as const,
  fileKey: "gallery/images/test.jpg",
  fileUrl: "https://example.com/test.jpg",
  thumbnailKey: null,
  thumbnailUrl: null,
  duration: null,
  demoUrl: null,
  tags: ["test", "image"],
  views: 100,
  likes: 50,
  downloads: 25,
  isPublished: true,
  isFeatured: false,
  authorId: 1,
  authorName: "Test Author",
  authorAvatar: null,
  sortOrder: 0,
  createdAt: new Date(),
  updatedAt: new Date(),
};

describe("gallery.list (public)", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("returns published gallery items for public users", async () => {
    const mockItems = [mockGalleryItem];
    vi.mocked(db.getGalleryItems).mockResolvedValue(mockItems);

    const ctx = createPublicContext();
    const caller = appRouter.createCaller(ctx);

    const result = await caller.gallery.list({ limit: 50 });

    expect(result).toEqual(mockItems);
    expect(db.getGalleryItems).toHaveBeenCalledWith({
      limit: 50,
      offset: 0,
      isPublished: true,
    });
  });

  it("filters by type when specified", async () => {
    vi.mocked(db.getGalleryItems).mockResolvedValue([]);

    const ctx = createPublicContext();
    const caller = appRouter.createCaller(ctx);

    await caller.gallery.list({ type: "video", limit: 50 });

    expect(db.getGalleryItems).toHaveBeenCalledWith({
      type: "video",
      limit: 50,
      offset: 0,
      isPublished: true,
    });
  });

  it("supports search query", async () => {
    vi.mocked(db.getGalleryItems).mockResolvedValue([]);

    const ctx = createPublicContext();
    const caller = appRouter.createCaller(ctx);

    await caller.gallery.list({ search: "landscape", limit: 50 });

    expect(db.getGalleryItems).toHaveBeenCalledWith({
      search: "landscape",
      limit: 50,
      offset: 0,
      isPublished: true,
    });
  });
});

describe("gallery.get (public)", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("returns a published gallery item", async () => {
    vi.mocked(db.getGalleryItemById).mockResolvedValue(mockGalleryItem);

    const ctx = createPublicContext();
    const caller = appRouter.createCaller(ctx);

    const result = await caller.gallery.get({ id: 1 });

    expect(result).toEqual(mockGalleryItem);
    expect(db.getGalleryItemById).toHaveBeenCalledWith(1);
  });

  it("returns null for unpublished items", async () => {
    const unpublishedItem = { ...mockGalleryItem, isPublished: false };
    vi.mocked(db.getGalleryItemById).mockResolvedValue(unpublishedItem);

    const ctx = createPublicContext();
    const caller = appRouter.createCaller(ctx);

    const result = await caller.gallery.get({ id: 1 });

    expect(result).toBeNull();
  });

  it("returns null for non-existent items", async () => {
    vi.mocked(db.getGalleryItemById).mockResolvedValue(undefined);

    const ctx = createPublicContext();
    const caller = appRouter.createCaller(ctx);

    const result = await caller.gallery.get({ id: 999 });

    expect(result).toBeNull();
  });
});

describe("gallery.view (public)", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("increments view count", async () => {
    vi.mocked(db.incrementGalleryViews).mockResolvedValue();

    const ctx = createPublicContext();
    const caller = appRouter.createCaller(ctx);

    const result = await caller.gallery.view({ id: 1 });

    expect(result).toEqual({ success: true });
    expect(db.incrementGalleryViews).toHaveBeenCalledWith(1);
  });
});

describe("gallery.like (public)", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("increments like count", async () => {
    vi.mocked(db.incrementGalleryLikes).mockResolvedValue();

    const ctx = createPublicContext();
    const caller = appRouter.createCaller(ctx);

    const result = await caller.gallery.like({ id: 1 });

    expect(result).toEqual({ success: true });
    expect(db.incrementGalleryLikes).toHaveBeenCalledWith(1);
  });
});

describe("gallery.download (public)", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("increments download count", async () => {
    vi.mocked(db.incrementGalleryDownloads).mockResolvedValue();

    const ctx = createPublicContext();
    const caller = appRouter.createCaller(ctx);

    const result = await caller.gallery.download({ id: 1 });

    expect(result).toEqual({ success: true });
    expect(db.incrementGalleryDownloads).toHaveBeenCalledWith(1);
  });
});

describe("gallery.adminList (admin only)", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("returns all items for admin users", async () => {
    const mockItems = [mockGalleryItem, { ...mockGalleryItem, id: 2, isPublished: false }];
    vi.mocked(db.getGalleryItems).mockResolvedValue(mockItems);

    const ctx = createAdminContext();
    const caller = appRouter.createCaller(ctx);

    const result = await caller.gallery.adminList({ limit: 50 });

    expect(result).toEqual(mockItems);
    expect(db.getGalleryItems).toHaveBeenCalledWith({ limit: 50, offset: 0 });
  });

  it("rejects non-admin users", async () => {
    const ctx = createUserContext();
    const caller = appRouter.createCaller(ctx);

    await expect(caller.gallery.adminList({ limit: 50 })).rejects.toThrow();
  });

  it("rejects unauthenticated users", async () => {
    const ctx = createPublicContext();
    const caller = appRouter.createCaller(ctx);

    await expect(caller.gallery.adminList({ limit: 50 })).rejects.toThrow();
  });
});

describe("gallery.create (admin only)", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("creates a new gallery item", async () => {
    vi.mocked(db.createGalleryItem).mockResolvedValue(1);

    const ctx = createAdminContext();
    const caller = appRouter.createCaller(ctx);

    const result = await caller.gallery.create({
      type: "image",
      title: "New Image",
      aspectRatio: "16:9",
      isPublished: true,
      isFeatured: false,
      sortOrder: 0,
    });

    expect(result).toEqual({ id: 1 });
    expect(db.createGalleryItem).toHaveBeenCalledWith(
      expect.objectContaining({
        type: "image",
        title: "New Image",
        aspectRatio: "16:9",
        authorId: 1,
      })
    );
  });

  it("rejects non-admin users", async () => {
    const ctx = createUserContext();
    const caller = appRouter.createCaller(ctx);

    await expect(
      caller.gallery.create({
        type: "image",
        title: "New Image",
        aspectRatio: "16:9",
        isPublished: true,
        isFeatured: false,
        sortOrder: 0,
      })
    ).rejects.toThrow();
  });
});

describe("gallery.update (admin only)", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("updates an existing gallery item", async () => {
    vi.mocked(db.updateGalleryItem).mockResolvedValue();

    const ctx = createAdminContext();
    const caller = appRouter.createCaller(ctx);

    const result = await caller.gallery.update({
      id: 1,
      data: { title: "Updated Title" },
    });

    expect(result).toEqual({ success: true });
    expect(db.updateGalleryItem).toHaveBeenCalledWith(1, expect.objectContaining({ title: "Updated Title" }));
  });

  it("rejects non-admin users", async () => {
    const ctx = createUserContext();
    const caller = appRouter.createCaller(ctx);

    await expect(
      caller.gallery.update({ id: 1, data: { title: "Updated" } })
    ).rejects.toThrow();
  });
});

describe("gallery.delete (admin only)", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("deletes a gallery item", async () => {
    vi.mocked(db.deleteGalleryItem).mockResolvedValue();

    const ctx = createAdminContext();
    const caller = appRouter.createCaller(ctx);

    const result = await caller.gallery.delete({ id: 1 });

    expect(result).toEqual({ success: true });
    expect(db.deleteGalleryItem).toHaveBeenCalledWith(1);
  });

  it("rejects non-admin users", async () => {
    const ctx = createUserContext();
    const caller = appRouter.createCaller(ctx);

    await expect(caller.gallery.delete({ id: 1 })).rejects.toThrow();
  });
});

describe("gallery.stats (admin only)", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("returns gallery statistics", async () => {
    const mockStats = {
      totalItems: 10,
      totalImages: 5,
      totalVideos: 3,
      totalWebsites: 2,
      totalViews: 1000,
      totalLikes: 500,
    };
    vi.mocked(db.getGalleryStats).mockResolvedValue(mockStats);

    const ctx = createAdminContext();
    const caller = appRouter.createCaller(ctx);

    const result = await caller.gallery.stats();

    expect(result).toEqual(mockStats);
    expect(db.getGalleryStats).toHaveBeenCalled();
  });

  it("rejects non-admin users", async () => {
    const ctx = createUserContext();
    const caller = appRouter.createCaller(ctx);

    await expect(caller.gallery.stats()).rejects.toThrow();
  });
});

describe("gallery.togglePublish (admin only)", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("toggles publish status from true to false", async () => {
    vi.mocked(db.getGalleryItemById).mockResolvedValue(mockGalleryItem);
    vi.mocked(db.updateGalleryItem).mockResolvedValue();

    const ctx = createAdminContext();
    const caller = appRouter.createCaller(ctx);

    const result = await caller.gallery.togglePublish({ id: 1 });

    expect(result).toEqual({ success: true, isPublished: false });
    expect(db.updateGalleryItem).toHaveBeenCalledWith(1, { isPublished: false });
  });

  it("toggles publish status from false to true", async () => {
    vi.mocked(db.getGalleryItemById).mockResolvedValue({ ...mockGalleryItem, isPublished: false });
    vi.mocked(db.updateGalleryItem).mockResolvedValue();

    const ctx = createAdminContext();
    const caller = appRouter.createCaller(ctx);

    const result = await caller.gallery.togglePublish({ id: 1 });

    expect(result).toEqual({ success: true, isPublished: true });
    expect(db.updateGalleryItem).toHaveBeenCalledWith(1, { isPublished: true });
  });
});

describe("gallery.toggleFeatured (admin only)", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("toggles featured status", async () => {
    vi.mocked(db.getGalleryItemById).mockResolvedValue(mockGalleryItem);
    vi.mocked(db.updateGalleryItem).mockResolvedValue();

    const ctx = createAdminContext();
    const caller = appRouter.createCaller(ctx);

    const result = await caller.gallery.toggleFeatured({ id: 1 });

    expect(result).toEqual({ success: true, isFeatured: true });
    expect(db.updateGalleryItem).toHaveBeenCalledWith(1, { isFeatured: true });
  });
});
