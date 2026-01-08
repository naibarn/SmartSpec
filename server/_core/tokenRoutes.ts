import type { Express, Request, Response } from "express";
import fs from "fs";
import path from "path";
import { authorizeRequest } from "./authz";
import { mintBearerToken, verifyBearerToken } from "./tokens";
import { rateLimit } from "./limits";
import { ENV } from "./env";
import { revokeJti } from "./revocation";

const DEFAULT_SCOPES = ["llm:chat", "mcp:read"];

function isOwner(user: any): boolean {
  const openId = String(user?.openId || user?.open_id || "");
  return Boolean(ENV.ownerOpenId) && openId === ENV.ownerOpenId;
}

function unauthorized(res: Response, msg = "Unauthorized") {
  res.status(401).json({ error: { message: msg } });
}

function badRequest(res: Response, msg: string) {
  res.status(400).json({ error: { message: msg } });
}

function writeAuthAudit(entry: any) {
  try {
    const dir = path.resolve(process.cwd(), "logs");
    fs.mkdirSync(dir, { recursive: true });
    fs.appendFileSync(path.join(dir, "auth_audit.log"), JSON.stringify(entry) + "\n");
  } catch {
    // ignore
  }
}

/**
 * CSRF protection for cookie-auth endpoints:
 * - Require Origin header to match current host (same-origin)
 */
function requireSameOrigin(req: Request): { ok: boolean; reason?: string } {
  const origin = String(req.headers["origin"] || "");
  if (!origin) return { ok: false, reason: "Missing Origin" };

  let o: URL;
  try {
    o = new URL(origin);
  } catch {
    return { ok: false, reason: "Invalid Origin" };
  }

  const host = String(req.headers["x-forwarded-host"] || req.headers["host"] || "");
  if (!host) return { ok: false, reason: "Missing Host" };

  const expected = host.toLowerCase();
  const actual = (o.host || "").toLowerCase();

  if (actual !== expected) return { ok: false, reason: `Origin mismatch (${actual} != ${expected})` };
  return { ok: true };
}

export function registerTokenRoutes(app: Express) {
  const limiter = rateLimit("token", { rpm: 30 });
  const revokeLimiter = rateLimit("token_revoke", { rpm: 60 });

  /**
   * Issue short-lived bearer tokens for desktop/runner/proxy integrations.
   * Auth: session cookie only (owner only).
   * Security: same-origin check to mitigate CSRF.
   */
  app.post("/api/auth/token", limiter, async (req: Request, res: Response) => {
    const originCheck = requireSameOrigin(req);
    if (!originCheck.ok) {
      writeAuthAudit({
        ts: new Date().toISOString(),
        event: "token_issue_denied",
        reason: originCheck.reason,
        ip: req.ip,
        ua: req.headers["user-agent"] || "",
      });
      return unauthorized(res, "CSRF protection: origin denied");
    }

    const auth = await authorizeRequest(req, { allowBearer: false, allowSession: true });
    if (!auth.ok || !("user" in auth) || !auth.user) {
      writeAuthAudit({
        ts: new Date().toISOString(),
        event: "token_issue_denied",
        reason: auth.ok ? "no session" : auth.error,
        ip: req.ip,
        ua: req.headers["user-agent"] || "",
      });
      return unauthorized(res);
    }
    if (!isOwner(auth.user)) {
      writeAuthAudit({
        ts: new Date().toISOString(),
        event: "token_issue_denied",
        reason: "owner_only",
        sub: String(auth.user?.id || auth.user?.openId || auth.user?.open_id || ""),
        ip: req.ip,
        ua: req.headers["user-agent"] || "",
      });
      return unauthorized(res, "Owner only");
    }

    const body = req.body || {};
    const scopes = Array.isArray(body.scopes) ? body.scopes.map(String) : DEFAULT_SCOPES;
    const ttlSeconds = body.ttlSeconds ? Number(body.ttlSeconds) : 15 * 60;

    // Safety: clamp scopes to allowlist
    const allow = new Set(["llm:chat", "mcp:read", "mcp:write", "mcp:*", "*"]);
    const filtered = scopes.filter((s: string) => allow.has(s));
    if (!filtered.length) return badRequest(res, "No valid scopes requested");

    const sub = String(auth.user?.id || auth.user?.openId || auth.user?.open_id || "owner");
    const minted = await mintBearerToken({ sub, scopes: filtered, ttlSeconds });

    writeAuthAudit({
      ts: new Date().toISOString(),
      event: "token_issued",
      sub,
      scopes: filtered,
      expiresAt: minted.expiresAt,
      ip: req.ip,
      ua: req.headers["user-agent"] || "",
    });

    res.json({
      token: minted.token,
      scopes: filtered,
      expiresAt: minted.expiresAt,
    });
  });

  /**
   * Revoke a previously issued bearer token immediately (denylist by jti).
   * Auth: session cookie only (owner only) + CSRF same-origin.
   * Body: { token: "<bearer>" }
   */
  app.post("/api/auth/token/revoke", revokeLimiter, async (req: Request, res: Response) => {
    const originCheck = requireSameOrigin(req);
    if (!originCheck.ok) {
      writeAuthAudit({
        ts: new Date().toISOString(),
        event: "token_revoke_denied",
        reason: originCheck.reason,
        ip: req.ip,
        ua: req.headers["user-agent"] || "",
      });
      return unauthorized(res, "CSRF protection: origin denied");
    }

    const auth = await authorizeRequest(req, { allowBearer: false, allowSession: true });
    if (!auth.ok || !("user" in auth) || !auth.user) return unauthorized(res);
    if (!isOwner(auth.user)) return unauthorized(res, "Owner only");

    const token = String((req.body || {}).token || "").trim();
    if (!token) return badRequest(res, "Missing token");

    try {
      const claims = await verifyBearerToken(token);
      const jti = String((claims as any).jti || "");
      const exp = Number((claims as any).exp || 0);
      if (!jti || !exp) return badRequest(res, "Invalid token");
      await revokeJti(jti, exp * 1000);

      writeAuthAudit({
        ts: new Date().toISOString(),
        event: "token_revoked",
        jti,
        exp,
        ip: req.ip,
        ua: req.headers["user-agent"] || "",
      });

      res.json({ ok: true });
    } catch (e: any) {
      writeAuthAudit({
        ts: new Date().toISOString(),
        event: "token_revoke_failed",
        reason: e?.message || "invalid token",
        ip: req.ip,
        ua: req.headers["user-agent"] || "",
      });
      return badRequest(res, "Invalid token");
    }
  });
}
