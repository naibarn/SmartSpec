import type { Request, Response, NextFunction } from "express";

type Bucket = { ts: number[] };

const buckets = new Map<string, Bucket>();

function now() {
  return Date.now();
}

function keyFor(req: Request, namespace: string) {
  const ip = (req.headers["x-forwarded-for"] as string)?.split(",")[0]?.trim() || req.ip || "unknown";
  const token = (req.headers["authorization"] as string) || "";
  // include token prefix so shared NAT doesn't penalize everyone too much
  const tokenHint = token ? token.slice(0, 24) : "";
  return `${namespace}:${ip}:${tokenHint}`;
}

/**
 * Simple in-memory sliding-window rate limiter.
 * NOTE: for multi-instance production, put this behind a shared store (Redis) or gateway.
 */
export function rateLimit(namespace: string, opts: { rpm: number; windowMs?: number }) {
  const rpm = Math.max(1, opts.rpm);
  const windowMs = Math.max(1_000, opts.windowMs ?? 60_000);

  return (req: Request, res: Response, next: NextFunction) => {
    const k = keyFor(req, namespace);
    const b = buckets.get(k) ?? { ts: [] };
    const t = now();

    // prune
    const cutoff = t - windowMs;
    b.ts = b.ts.filter((x) => x > cutoff);

    if (b.ts.length >= rpm) {
      res.status(429).json({
        error: { message: "Rate limit exceeded", type: "rate_limit" },
      });
      return;
    }

    b.ts.push(t);
    buckets.set(k, b);
    next();
  };
}

export function enforceJsonBodyMaxBytes(maxBytes: number) {
  const limit = Math.max(1_024, maxBytes);
  return (req: Request, res: Response, next: NextFunction) => {
    try {
      const body = req.body ?? {};
      const size = Buffer.byteLength(JSON.stringify(body), "utf-8");
      if (size > limit) {
        res.status(413).json({ error: { message: `Request body too large (max ${limit} bytes)` } });
        return;
      }
    } catch {
      // ignore
    }
    next();
  };
}
