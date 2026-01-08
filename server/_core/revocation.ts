import { createClient, type RedisClientType } from "redis";

let client: RedisClientType | null = null;
let clientInit: Promise<RedisClientType | null> | null = null;

// Fallback in-memory denylist (for dev / when redis is unavailable)
const mem = new Map<string, number>(); // jti -> expMs

const PREFIX = process.env.TOKEN_REVOKE_PREFIX || "revoked:";
const REDIS_URL = process.env.REDIS_URL || process.env.TOKEN_REVOKE_REDIS_URL || "";

async function getRedis(): Promise<RedisClientType | null> {
  if (!REDIS_URL) return null;
  if (client) return client;

  if (!clientInit) {
    clientInit = (async () => {
      try {
        const c = createClient({ url: REDIS_URL });
        c.on("error", () => {
          // ignore; fallback to mem
        });
        await c.connect();
        client = c;
        return c;
      } catch {
        client = null;
        return null;
      }
    })();
  }
  return await clientInit;
}

function nowMs() {
  return Date.now();
}

export async function revokeJti(jti: string, expiresAtMs: number) {
  const ttlSeconds = Math.max(1, Math.ceil((expiresAtMs - nowMs()) / 1000));
  // Always store in memory for immediate effect
  mem.set(jti, expiresAtMs);

  const r = await getRedis();
  if (!r) return;

  try {
    await r.setEx(`${PREFIX}${jti}`, ttlSeconds, "1");
  } catch {
    // ignore
  }
}

export async function isJtiRevoked(jti: string): Promise<boolean> {
  const exp = mem.get(jti);
  if (exp && exp > nowMs()) return true;
  if (exp && exp <= nowMs()) mem.delete(jti);

  const r = await getRedis();
  if (!r) return false;

  try {
    const v = await r.get(`${PREFIX}${jti}`);
    return v === "1";
  } catch {
    return false;
  }
}

export function cleanupMem() {
  const t = nowMs();
  for (const [k, exp] of mem.entries()) {
    if (exp <= t) mem.delete(k);
  }
}
