import { int, mysqlEnum, mysqlTable, text, timestamp, varchar, json, boolean } from "drizzle-orm/mysql-core";

/**
 * Core user table backing auth flow.
 * Extend this file with additional tables as your product grows.
 * Columns use camelCase to match both database fields and generated types.
 */
export const users = mysqlTable("users", {
  /**
   * Surrogate primary key. Auto-incremented numeric value managed by the database.
   * Use this for relations between tables.
   */
  id: int("id").autoincrement().primaryKey(),
  /** Manus OAuth identifier (openId) returned from the OAuth callback. Unique per user. */
  openId: varchar("openId", { length: 64 }).notNull().unique(),
  name: text("name"),
  email: varchar("email", { length: 320 }),
  loginMethod: varchar("loginMethod", { length: 64 }),
  role: mysqlEnum("role", ["user", "admin"]).default("user").notNull(),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
  updatedAt: timestamp("updatedAt").defaultNow().onUpdateNow().notNull(),
  lastSignedIn: timestamp("lastSignedIn").defaultNow().notNull(),
});

export type User = typeof users.$inferSelect;
export type InsertUser = typeof users.$inferInsert;

/**
 * Gallery items table - stores images, videos, and website demos
 * Supports 3 content types with different aspect ratios
 */
export const galleryItems = mysqlTable("gallery_items", {
  id: int("id").autoincrement().primaryKey(),
  
  /** Content type: image, video, or website */
  type: mysqlEnum("type", ["image", "video", "website"]).notNull(),
  
  /** Title of the gallery item */
  title: varchar("title", { length: 255 }).notNull(),
  
  /** Description of the item */
  description: text("description"),
  
  /** Aspect ratio: 1:1, 9:16, or 16:9 */
  aspectRatio: mysqlEnum("aspectRatio", ["1:1", "9:16", "16:9"]).notNull(),
  
  /** S3/R2 file key for the main content */
  fileKey: varchar("fileKey", { length: 512 }),
  
  /** Public URL for the main content */
  fileUrl: varchar("fileUrl", { length: 1024 }),
  
  /** S3/R2 file key for thumbnail */
  thumbnailKey: varchar("thumbnailKey", { length: 512 }),
  
  /** Public URL for thumbnail */
  thumbnailUrl: varchar("thumbnailUrl", { length: 1024 }),
  
  /** For videos: duration in format "M:SS" */
  duration: varchar("duration", { length: 10 }),
  
  /** For websites: demo URL (subdomain link) */
  demoUrl: varchar("demoUrl", { length: 512 }),
  
  /** Tags for filtering and SEO (stored as JSON array) */
  tags: json("tags").$type<string[]>(),
  
  /** View count */
  views: int("views").default(0).notNull(),
  
  /** Like count */
  likes: int("likes").default(0).notNull(),
  
  /** Download count (for images) */
  downloads: int("downloads").default(0).notNull(),
  
  /** Whether the item is published/visible */
  isPublished: boolean("isPublished").default(true).notNull(),
  
  /** Whether the item is featured */
  isFeatured: boolean("isFeatured").default(false).notNull(),
  
  /** Author/creator user ID */
  authorId: int("authorId").references(() => users.id),
  
  /** Author name (for display, can be custom) */
  authorName: varchar("authorName", { length: 255 }),
  
  /** Author avatar URL */
  authorAvatar: varchar("authorAvatar", { length: 512 }),
  
  /** Sort order for manual ordering */
  sortOrder: int("sortOrder").default(0).notNull(),
  
  createdAt: timestamp("createdAt").defaultNow().notNull(),
  updatedAt: timestamp("updatedAt").defaultNow().onUpdateNow().notNull(),
});

export type GalleryItem = typeof galleryItems.$inferSelect;
export type InsertGalleryItem = typeof galleryItems.$inferInsert;
