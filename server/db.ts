import { eq, desc, asc, and, sql, like, or } from "drizzle-orm";
import { drizzle } from "drizzle-orm/mysql2";
import { InsertUser, users, galleryItems, InsertGalleryItem, GalleryItem } from "../drizzle/schema";
import { ENV } from './_core/env';

let _db: ReturnType<typeof drizzle> | null = null;

// Lazily create the drizzle instance so local tooling can run without a DB.
export async function getDb() {
  if (!_db && process.env.DATABASE_URL) {
    try {
      _db = drizzle(process.env.DATABASE_URL);
    } catch (error) {
      console.warn("[Database] Failed to connect:", error);
      _db = null;
    }
  }
  return _db;
}

export async function upsertUser(user: InsertUser): Promise<void> {
  if (!user.openId) {
    throw new Error("User openId is required for upsert");
  }

  const db = await getDb();
  if (!db) {
    console.warn("[Database] Cannot upsert user: database not available");
    return;
  }

  try {
    const values: InsertUser = {
      openId: user.openId,
    };
    const updateSet: Record<string, unknown> = {};

    const textFields = ["name", "email", "loginMethod"] as const;
    type TextField = (typeof textFields)[number];

    const assignNullable = (field: TextField) => {
      const value = user[field];
      if (value === undefined) return;
      const normalized = value ?? null;
      values[field] = normalized;
      updateSet[field] = normalized;
    };

    textFields.forEach(assignNullable);

    if (user.lastSignedIn !== undefined) {
      values.lastSignedIn = user.lastSignedIn;
      updateSet.lastSignedIn = user.lastSignedIn;
    }
    if (user.role !== undefined) {
      values.role = user.role;
      updateSet.role = user.role;
    } else if (user.openId === ENV.ownerOpenId) {
      values.role = 'admin';
      updateSet.role = 'admin';
    }

    if (!values.lastSignedIn) {
      values.lastSignedIn = new Date();
    }

    if (Object.keys(updateSet).length === 0) {
      updateSet.lastSignedIn = new Date();
    }

    await db.insert(users).values(values).onDuplicateKeyUpdate({
      set: updateSet,
    });
  } catch (error) {
    console.error("[Database] Failed to upsert user:", error);
    throw error;
  }
}

export async function getUserByOpenId(openId: string) {
  const db = await getDb();
  if (!db) {
    console.warn("[Database] Cannot get user: database not available");
    return undefined;
  }

  const result = await db.select().from(users).where(eq(users.openId, openId)).limit(1);

  return result.length > 0 ? result[0] : undefined;
}

// ==================== Gallery Queries ====================

export type GalleryType = 'image' | 'video' | 'website';
export type AspectRatio = '1:1' | '9:16' | '16:9';

export interface GalleryFilters {
  type?: GalleryType;
  isPublished?: boolean;
  isFeatured?: boolean;
  search?: string;
  limit?: number;
  offset?: number;
}

/**
 * Get all gallery items with optional filters
 */
export async function getGalleryItems(filters: GalleryFilters = {}): Promise<GalleryItem[]> {
  const db = await getDb();
  if (!db) {
    console.warn("[Database] Cannot get gallery items: database not available");
    return [];
  }

  const conditions = [];
  
  if (filters.type) {
    conditions.push(eq(galleryItems.type, filters.type));
  }
  
  if (filters.isPublished !== undefined) {
    conditions.push(eq(galleryItems.isPublished, filters.isPublished));
  }
  
  if (filters.isFeatured !== undefined) {
    conditions.push(eq(galleryItems.isFeatured, filters.isFeatured));
  }
  
  if (filters.search) {
    conditions.push(
      or(
        like(galleryItems.title, `%${filters.search}%`),
        like(galleryItems.description, `%${filters.search}%`)
      )
    );
  }

  let query = db.select().from(galleryItems);
  
  if (conditions.length > 0) {
    query = query.where(and(...conditions)) as typeof query;
  }
  
  query = query.orderBy(asc(galleryItems.sortOrder), desc(galleryItems.createdAt)) as typeof query;
  
  if (filters.limit) {
    query = query.limit(filters.limit) as typeof query;
  }
  
  if (filters.offset) {
    query = query.offset(filters.offset) as typeof query;
  }

  return await query;
}

/**
 * Get a single gallery item by ID
 */
export async function getGalleryItemById(id: number): Promise<GalleryItem | undefined> {
  const db = await getDb();
  if (!db) {
    console.warn("[Database] Cannot get gallery item: database not available");
    return undefined;
  }

  const result = await db.select().from(galleryItems).where(eq(galleryItems.id, id)).limit(1);
  return result.length > 0 ? result[0] : undefined;
}

/**
 * Create a new gallery item
 */
export async function createGalleryItem(item: InsertGalleryItem): Promise<number> {
  const db = await getDb();
  if (!db) {
    throw new Error("Database not available");
  }

  const result = await db.insert(galleryItems).values(item);
  return result[0].insertId;
}

/**
 * Update a gallery item
 */
export async function updateGalleryItem(id: number, item: Partial<InsertGalleryItem>): Promise<void> {
  const db = await getDb();
  if (!db) {
    throw new Error("Database not available");
  }

  await db.update(galleryItems).set(item).where(eq(galleryItems.id, id));
}

/**
 * Delete a gallery item
 */
export async function deleteGalleryItem(id: number): Promise<void> {
  const db = await getDb();
  if (!db) {
    throw new Error("Database not available");
  }

  await db.delete(galleryItems).where(eq(galleryItems.id, id));
}

/**
 * Increment view count
 */
export async function incrementGalleryViews(id: number): Promise<void> {
  const db = await getDb();
  if (!db) return;

  await db.update(galleryItems)
    .set({ views: sql`${galleryItems.views} + 1` })
    .where(eq(galleryItems.id, id));
}

/**
 * Increment like count
 */
export async function incrementGalleryLikes(id: number): Promise<void> {
  const db = await getDb();
  if (!db) return;

  await db.update(galleryItems)
    .set({ likes: sql`${galleryItems.likes} + 1` })
    .where(eq(galleryItems.id, id));
}

/**
 * Increment download count
 */
export async function incrementGalleryDownloads(id: number): Promise<void> {
  const db = await getDb();
  if (!db) return;

  await db.update(galleryItems)
    .set({ downloads: sql`${galleryItems.downloads} + 1` })
    .where(eq(galleryItems.id, id));
}

/**
 * Get gallery stats
 */
export async function getGalleryStats(): Promise<{
  totalItems: number;
  totalImages: number;
  totalVideos: number;
  totalWebsites: number;
  totalViews: number;
  totalLikes: number;
}> {
  const db = await getDb();
  if (!db) {
    return {
      totalItems: 0,
      totalImages: 0,
      totalVideos: 0,
      totalWebsites: 0,
      totalViews: 0,
      totalLikes: 0
    };
  }

  const [stats] = await db.select({
    totalItems: sql<number>`COUNT(*)`,
    totalImages: sql<number>`SUM(CASE WHEN type = 'image' THEN 1 ELSE 0 END)`,
    totalVideos: sql<number>`SUM(CASE WHEN type = 'video' THEN 1 ELSE 0 END)`,
    totalWebsites: sql<number>`SUM(CASE WHEN type = 'website' THEN 1 ELSE 0 END)`,
    totalViews: sql<number>`SUM(views)`,
    totalLikes: sql<number>`SUM(likes)`
  }).from(galleryItems);

  return {
    totalItems: Number(stats.totalItems) || 0,
    totalImages: Number(stats.totalImages) || 0,
    totalVideos: Number(stats.totalVideos) || 0,
    totalWebsites: Number(stats.totalWebsites) || 0,
    totalViews: Number(stats.totalViews) || 0,
    totalLikes: Number(stats.totalLikes) || 0
  };
}
