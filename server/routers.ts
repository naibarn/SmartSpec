import { COOKIE_NAME } from "@shared/const";
import { getSessionCookieOptions } from "./_core/cookies";
import { systemRouter } from "./_core/systemRouter";
import { publicProcedure, protectedProcedure, adminProcedure, router } from "./_core/trpc";
import { z } from "zod";
import {
  getGalleryItems,
  getGalleryItemById,
  createGalleryItem,
  updateGalleryItem,
  deleteGalleryItem,
  incrementGalleryViews,
  incrementGalleryLikes,
  incrementGalleryDownloads,
  getGalleryStats,
  type GalleryType,
  type AspectRatio
} from "./db";
import { storagePut } from "./storage";
import { nanoid } from "nanoid";

// Zod schemas for validation
const galleryTypeSchema = z.enum(["image", "video", "website"]);
const aspectRatioSchema = z.enum(["1:1", "9:16", "16:9"]);

const createGalleryItemSchema = z.object({
  type: galleryTypeSchema,
  title: z.string().min(1).max(255),
  description: z.string().optional(),
  aspectRatio: aspectRatioSchema,
  fileUrl: z.string().url().optional(),
  fileKey: z.string().optional(),
  thumbnailUrl: z.string().url().optional(),
  thumbnailKey: z.string().optional(),
  duration: z.string().optional(),
  demoUrl: z.string().url().optional(),
  tags: z.array(z.string()).optional(),
  isPublished: z.boolean().default(true),
  isFeatured: z.boolean().default(false),
  authorName: z.string().optional(),
  authorAvatar: z.string().optional(),
  sortOrder: z.number().default(0),
});

const updateGalleryItemSchema = createGalleryItemSchema.partial();

const galleryFiltersSchema = z.object({
  type: galleryTypeSchema.optional(),
  isPublished: z.boolean().optional(),
  isFeatured: z.boolean().optional(),
  search: z.string().optional(),
  limit: z.number().min(1).max(100).default(50),
  offset: z.number().min(0).default(0),
});

export const appRouter = router({
  // if you need to use socket.io, read and register route in server/_core/index.ts, all api should start with '/api/' so that the gateway can route correctly
  system: systemRouter,
  auth: router({
    me: publicProcedure.query(opts => opts.ctx.user),
    logout: publicProcedure.mutation(({ ctx }) => {
      const cookieOptions = getSessionCookieOptions(ctx.req);
      ctx.res.clearCookie(COOKIE_NAME, { ...cookieOptions, maxAge: -1 });
      return {
        success: true,
      } as const;
    }),
  }),


// AI helpers (streaming chat is served via /api/llm/stream; this router is for uploads)
ai: router({
  upload: protectedProcedure
    .input(
      z
        .object({
          fileName: z.string().min(1).max(255),
          fileType: z.string().min(1).max(255),
          fileBase64: z.string().min(1),
        })
        .refine(
          (v) => v.fileType.startsWith("image/") || v.fileType.startsWith("video/"),
          { message: "Only image/* or video/* uploads are supported" }
        )
    )
    .mutation(async ({ input, ctx }) => {
      const parts = input.fileBase64.split(",", 2);
      const b64 = parts.length === 2 ? parts[1] : input.fileBase64;
      const buf = Buffer.from(b64, "base64");
      const max = 15 * 1024 * 1024;
      if (buf.length > max) throw new Error("File too large (max 15MB)");

      const ext = (input.fileName.split(".").pop() || "").replace(/[^a-zA-Z0-9]/g, "");
      const id = nanoid(10);
      const key = `chat/uploads/${ctx.user?.id || "anon"}/${id}-${Date.now()}${ext ? "." + ext : ""}`;

      const { url } = await storagePut(key, buf, input.fileType);
      return { key, url, fileType: input.fileType };
    }),
}),

  // Gallery routes
  gallery: router({
    // Public: List gallery items (only published)
    list: publicProcedure
      .input(galleryFiltersSchema.omit({ isPublished: true }))
      .query(async ({ input }) => {
        return getGalleryItems({
          ...input,
          isPublished: true, // Only show published items to public
        });
      }),

    // Public: Get single gallery item
    get: publicProcedure
      .input(z.object({ id: z.number() }))
      .query(async ({ input }) => {
        const item = await getGalleryItemById(input.id);
        if (!item || !item.isPublished) {
          return null;
        }
        return item;
      }),

    // Public: Increment view count
    view: publicProcedure
      .input(z.object({ id: z.number() }))
      .mutation(async ({ input }) => {
        await incrementGalleryViews(input.id);
        return { success: true };
      }),

    // Public: Increment like count
    like: publicProcedure
      .input(z.object({ id: z.number() }))
      .mutation(async ({ input }) => {
        await incrementGalleryLikes(input.id);
        return { success: true };
      }),

    // Public: Increment download count
    download: publicProcedure
      .input(z.object({ id: z.number() }))
      .mutation(async ({ input }) => {
        await incrementGalleryDownloads(input.id);
        return { success: true };
      }),

    // Admin: List all gallery items (including unpublished)
    adminList: adminProcedure
      .input(galleryFiltersSchema)
      .query(async ({ input }) => {
        return getGalleryItems(input);
      }),

    // Admin: Get single gallery item (including unpublished)
    adminGet: adminProcedure
      .input(z.object({ id: z.number() }))
      .query(async ({ input }) => {
        return getGalleryItemById(input.id);
      }),

    // Admin: Create gallery item
    create: adminProcedure
      .input(createGalleryItemSchema)
      .mutation(async ({ input, ctx }) => {
        const id = await createGalleryItem({
          ...input,
          authorId: ctx.user.id,
          tags: input.tags || [],
        });
        return { id };
      }),

    // Admin: Update gallery item
    update: adminProcedure
      .input(z.object({
        id: z.number(),
        data: updateGalleryItemSchema,
      }))
      .mutation(async ({ input }) => {
        await updateGalleryItem(input.id, input.data);
        return { success: true };
      }),

    // Admin: Delete gallery item
    delete: adminProcedure
      .input(z.object({ id: z.number() }))
      .mutation(async ({ input }) => {
        await deleteGalleryItem(input.id);
        return { success: true };
      }),

    // Admin: Get gallery stats
    stats: adminProcedure.query(async () => {
      return getGalleryStats();
    }),

    // Admin: Upload file to S3
    uploadFile: adminProcedure
      .input(z.object({
        fileName: z.string(),
        fileType: z.string(),
        fileBase64: z.string(),
        folder: z.enum(["images", "videos", "thumbnails", "websites"]),
      }))
      .mutation(async ({ input, ctx }) => {
        const { fileName, fileType, fileBase64, folder } = input;
        
        // Generate unique file key
        const ext = fileName.split('.').pop() || '';
        const uniqueId = nanoid(10);
        const fileKey = `gallery/${folder}/${uniqueId}-${Date.now()}.${ext}`;
        
        // Convert base64 to buffer
        const buffer = Buffer.from(fileBase64, 'base64');
        
        // Upload to S3
        const { url } = await storagePut(fileKey, buffer, fileType);
        
        return {
          fileKey,
          fileUrl: url,
        };
      }),

    // Admin: Bulk update sort order
    updateSortOrder: adminProcedure
      .input(z.array(z.object({
        id: z.number(),
        sortOrder: z.number(),
      })))
      .mutation(async ({ input }) => {
        for (const item of input) {
          await updateGalleryItem(item.id, { sortOrder: item.sortOrder });
        }
        return { success: true };
      }),

    // Admin: Toggle publish status
    togglePublish: adminProcedure
      .input(z.object({ id: z.number() }))
      .mutation(async ({ input }) => {
        const item = await getGalleryItemById(input.id);
        if (!item) {
          throw new Error("Item not found");
        }
        await updateGalleryItem(input.id, { isPublished: !item.isPublished });
        return { success: true, isPublished: !item.isPublished };
      }),

    // Admin: Toggle featured status
    toggleFeatured: adminProcedure
      .input(z.object({ id: z.number() }))
      .mutation(async ({ input }) => {
        const item = await getGalleryItemById(input.id);
        if (!item) {
          throw new Error("Item not found");
        }
        await updateGalleryItem(input.id, { isFeatured: !item.isFeatured });
        return { success: true, isFeatured: !item.isFeatured };
      }),
  }),
});

export type AppRouter = typeof appRouter;
