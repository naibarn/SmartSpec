import type { Request } from "express";
import { ENV } from "./env";
import { sdk } from "./sdk";
import { verifyBearerToken } from "./tokens";
import { isJtiRevoked } from "./revocation";

export type AuthResult =
  | { ok: true; mode: "bearer"; sub: string; scopes: string[] }
  | { ok: true; mode: "session"; user: any; sub: string; scopes: string[] }
  | { ok: false; error: string };

function parseBearer(req: Request): string | null {
  const h = String(req.headers["authorization"] || "").trim();
  if (h.toLowerCase().startsWith("bearer ")) return h.slice(7).trim();
  return null;
}

function scopesForStaticToken(token: string): string[] {
  // Least-privilege defaults for server-to-server tokens
  if (ENV.mcpServerToken && token === ENV.mcpServerToken) return ["mcp:read", "mcp:write"];
  if (ENV.webGatewayToken && token === ENV.webGatewayToken) return ["llm:chat", "mcp:read", "mcp:write"];
  return [];
}

export async function authorizeRequest(
  req: Request,
  opts: { allowBearer: boolean; allowSession: boolean }
): Promise<AuthResult> {
  // 1) Bearer token (server-to-server / desktop proxy)
  if (opts.allowBearer) {
    const token = parseBearer(req);
    if (token) {
      // Static token shortcut (if configured)
      const staticScopes = scopesForStaticToken(token);
      if (staticScopes.length) {
        return { ok: true, mode: "bearer", sub: "static", scopes: staticScopes };
      }

      // Signed JWT bearer token (short-lived)
      try {
        const claims = await verifyBearerToken(token);
        const jti = String((claims as any).jti || "");
        if (jti) {
          const revoked = await isJtiRevoked(jti);
          if (revoked) return { ok: false, error: "Token revoked" };
        }
        return { ok: true, mode: "bearer", sub: String(claims.sub), scopes: claims.scopes || [] };
      } catch (e: any) {
        return { ok: false, error: e?.message || "Invalid token" };
      }
    }
  }

  // 2) Session cookie (browser UI)
  if (opts.allowSession) {
    try {
      const user = await sdk.authenticateRequest(req);
      const sub = String((user as any)?.id || (user as any)?.openId || (user as any)?.open_id || "");
      if (!sub) return { ok: false, error: "Unauthorized" };

      // Session users are interactive owners/users; allow tools but enforce per-tool policy elsewhere
      const scopes = ["llm:chat", "mcp:read", "mcp:write"];
      return { ok: true, mode: "session", user, sub, scopes };
    } catch (e: any) {
      return { ok: false, error: e?.message || "Unauthorized" };
    }
  }

  return { ok: false, error: "Unauthorized" };
}
