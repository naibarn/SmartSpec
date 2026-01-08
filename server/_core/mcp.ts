import fs from "fs";
import path from "path";
import crypto from "crypto";

const GATEWAY_KEY = process.env.SMARTSPEC_WEB_GATEWAY_KEY ?? "";
const WORKSPACE_ROOT = process.env.WORKSPACE_ROOT ?? process.cwd();

const ENABLE_WRITE = (process.env.MCP_ENABLE_WORKSPACE_WRITE ?? "0") === "1";
const WRITE_TOKEN = (process.env.MCP_WRITE_TOKEN ?? "").trim();

const MAX_READ_BYTES = parseInt(process.env.MCP_MAX_READ_BYTES ?? "1048576");
const MAX_WRITE_BYTES = parseInt(process.env.MCP_MAX_WRITE_BYTES ?? "2097152");

const AUDIT_LOG_BASE = (process.env.MCP_AUDIT_LOG_PATH ?? "logs/mcp_audit.jsonl").trim();
const AUDIT_ROTATE_DAILY = (process.env.MCP_AUDIT_ROTATE_DAILY ?? "1") !== "0";
const AUDIT_RETENTION_DAYS = parseInt(process.env.MCP_AUDIT_RETENTION_DAYS ?? "30");

const CONTROL_PLANE_BASE_URL = (process.env.CONTROL_PLANE_BASE_URL ?? "").replace(/\/$/, "");
const CONTROL_PLANE_API_KEY = process.env.CONTROL_PLANE_API_KEY ?? "";

const DEFAULT_READ_EXTS = (process.env.MCP_READ_EXT_ALLOWLIST ??
  ".md,.txt,.json,.yaml,.yml,.toml,.ts,.tsx,.js,.jsx,.py,.css,.html,.env,.csv")
  .split(",").map(s => s.trim()).filter(Boolean);

const DEFAULT_WRITE_EXTS = (process.env.MCP_WRITE_EXT_ALLOWLIST ??
  ".md,.txt,.json,.yaml,.yml,.toml,.ts,.tsx,.js,.jsx,.py,.css,.html,.env,.csv")
  .split(",").map(s => s.trim()).filter(Boolean);

const PATH_ALLOWLIST = (process.env.MCP_PATH_ALLOWLIST ?? "").split(",").map(s => s.trim()).filter(Boolean);
const PATH_DENYLIST = (process.env.MCP_PATH_DENYLIST ?? ".git,node_modules,dist,build,logs,.env")
  .split(",").map(s => s.trim()).filter(Boolean);

function ensureDirForFile(p: string) {
  fs.mkdirSync(path.dirname(p), { recursive: true });
}

function sha256Json(obj: any) {
  try {
    const s = JSON.stringify(obj);
    return crypto.createHash("sha256").update(s).digest("hex");
  } catch {
    return crypto.createHash("sha256").update(String(obj)).digest("hex");
  }
}

function auditResolvePath(base: string) {
  if (!AUDIT_ROTATE_DAILY) return base;
  const date = new Date().toISOString().slice(0, 10).replace(/-/g, "");
  if (base.includes("{date}")) return base.replace("{date}", date);
  if (base.endsWith(".jsonl")) return base.slice(0, -5) + `.${date}.jsonl`;
  return base + `.${date}`;
}

function auditCleanup(base: string) {
  if (!AUDIT_ROTATE_DAILY || !(AUDIT_RETENTION_DAYS > 0)) return;
  try {
    const dir = path.dirname(base) || ".";
    const bn = path.basename(base);
    const prefix = bn.endsWith(".jsonl") ? bn.slice(0, -5) + "." : bn + ".";
    const suffix = bn.endsWith(".jsonl") ? ".jsonl" : "";
    const cutoff = Date.now() - AUDIT_RETENTION_DAYS * 24 * 60 * 60 * 1000;

    for (const fn of fs.readdirSync(dir)) {
      if (!fn.startsWith(prefix) || (suffix && !fn.endsWith(suffix))) continue;
      let mid = fn.slice(prefix.length);
      if (suffix && mid.endsWith(suffix)) mid = mid.slice(0, -suffix.length);
      if (!/^\d{8}$/.test(mid)) continue;

      const y = parseInt(mid.slice(0, 4), 10);
      const m = parseInt(mid.slice(4, 6), 10) - 1;
      const d = parseInt(mid.slice(6, 8), 10);
      const dt = Date.UTC(y, m, d);
      if (dt < cutoff) {
        try { fs.unlinkSync(path.join(dir, fn)); } catch {}
      }
    }
  } catch {}
}

function audit(entry: any) {
  try {
    const p = auditResolvePath(AUDIT_LOG_BASE);
    ensureDirForFile(p);
    fs.appendFileSync(p, JSON.stringify(entry) + "\n", "utf-8");
    auditCleanup(AUDIT_LOG_BASE);
  } catch {}
}

function requireGatewayKey(req: any, res: any): boolean {
  if (!GATEWAY_KEY) return true;
  const k = req.header("x-gateway-key") || "";
  if (k !== GATEWAY_KEY) {
    res.status(401).json({ error: { message: "invalid_gateway_key" } });
    return false;
  }
  return true;
}

function resolveWorkspacePath(rel: string) {
  const abs = path.resolve(WORKSPACE_ROOT, rel);
  const rootAbs = path.resolve(WORKSPACE_ROOT);
  if (!abs.startsWith(rootAbs + path.sep) && abs !== rootAbs) {
    throw new Error("path_outside_workspace_root");
  }
  return abs;
}

function isProbablyBinary(buf: Buffer) {
  return buf.includes(0);
}

function checkPathPolicy(rel: string, mode: "read" | "write") {
  if (PATH_DENYLIST.length > 0) {
    const denied = PATH_DENYLIST.some(prefix => {
      const p = prefix.replace(/\/+$/, "");
      return rel === p || rel.startsWith(p + "/");
    });
    if (denied) throw new Error("path_denied");
  }

  if (PATH_ALLOWLIST.length > 0) {
    const ok = PATH_ALLOWLIST.some(prefix => {
      const p = prefix.replace(/\/+$/, "");
      return rel === p || rel.startsWith(p + "/");
    });
    if (!ok) throw new Error("path_not_allowed");
  }

  const ext = path.extname(rel).toLowerCase();
  const allowed = mode === "read" ? DEFAULT_READ_EXTS : DEFAULT_WRITE_EXTS;
  if (allowed.length > 0 && ext && !allowed.includes(ext)) {
    throw new Error("extension_not_allowed");
  }
}

type ToolDef = {
  name: string;
  description: string;
  parameters: any;
  permission: "read" | "write" | "net";
  handler: (args: any, traceId: string) => Promise<any>;
};

const tools: ToolDef[] = [
  {
    name: "ping",
    description: "Health check tool. Returns ok:true and timestamp.",
    parameters: { type: "object", properties: {}, additionalProperties: false },
    permission: "read",
    handler: async () => ({ ok: true, ts: Date.now() }),
  },
  {
    name: "artifact_get_url",
    description: "Return a presigned GET URL for an artifact in Control Plane (server-side).",
    parameters: {
      type: "object",
      properties: { sessionId: { type: "string" }, key: { type: "string" } },
      required: ["sessionId", "key"],
      additionalProperties: false,
    },
    permission: "net",
    handler: async (args: any) => {
      if (!CONTROL_PLANE_BASE_URL || !CONTROL_PLANE_API_KEY) throw new Error("control_plane_not_configured");
      const url =
        `${CONTROL_PLANE_BASE_URL}/api/v1/sessions/${encodeURIComponent(String(args.sessionId))}/artifacts/presign-get?` +
        new URLSearchParams({ key: String(args.key) }).toString();
      const r = await fetch(url, { headers: { "x-api-key": CONTROL_PLANE_API_KEY } });
      if (!r.ok) throw new Error(`control_plane_error:${r.status}:${await r.text()}`);
      return await r.json();
    },
  },
  {
    name: "workspace_read_file",
    description: "Read a UTF-8 text file from WORKSPACE_ROOT (policy enforced).",
    parameters: {
      type: "object",
      properties: { path: { type: "string" }, maxBytes: { type: "number" } },
      required: ["path"],
      additionalProperties: false,
    },
    permission: "read",
    handler: async (args: any) => {
      const rel = String(args.path);
      checkPathPolicy(rel, "read");
      const p = resolveWorkspacePath(rel);
      const st = fs.statSync(p);
      if (!st.isFile()) throw new Error("not_a_file");
      const maxBytes = Math.min(Number(args.maxBytes || MAX_READ_BYTES), MAX_READ_BYTES);
      if (st.size > maxBytes) throw new Error("file_too_large");
      const buf = fs.readFileSync(p);
      if (isProbablyBinary(buf)) throw new Error("binary_file_denied");
      return { path: rel, content: buf.toString("utf-8") };
    },
  },
  {
    name: "workspace_write_file",
    description: "Write a UTF-8 text file into WORKSPACE_ROOT (policy enforced). Requires MCP_ENABLE_WORKSPACE_WRITE=1 and optional MCP_WRITE_TOKEN.",
    parameters: {
      type: "object",
      properties: {
        path: { type: "string" },
        content: { type: "string" },
        overwrite: { type: "boolean", default: true },
        writeToken: { type: "string", description: "Required if MCP_WRITE_TOKEN is set on server." },
      },
      required: ["path", "content"],
      additionalProperties: false,
    },
    permission: "write",
    handler: async (args: any) => {
      if (!ENABLE_WRITE) throw new Error("write_disabled");
      if (WRITE_TOKEN) {
        const tok = String(args.writeToken || "");
        if (tok !== WRITE_TOKEN) throw new Error("write_token_required");
      }
      const rel = String(args.path);
      checkPathPolicy(rel, "write");
      const p = resolveWorkspacePath(rel);
      const overwrite = args.overwrite !== false;
      if (!overwrite && fs.existsSync(p)) throw new Error("file_exists");
      const buf = Buffer.from(String(args.content), "utf-8");
      if (buf.length > MAX_WRITE_BYTES) throw new Error("content_too_large");
      fs.mkdirSync(path.dirname(p), { recursive: true });
      fs.writeFileSync(p, buf);
      return { ok: true, path: rel, bytes: buf.length };
    },
  },
];

export function registerMcpRoutes(app: any) {
  app.get("/api/mcp/policy", (req: any, res: any) => {
    if (!requireGatewayKey(req, res)) return;
    res.json({
      workspaceRoot: WORKSPACE_ROOT,
      enableWrite: ENABLE_WRITE,
      writeTokenRequired: Boolean(WRITE_TOKEN),
      maxReadBytes: MAX_READ_BYTES,
      maxWriteBytes: MAX_WRITE_BYTES,
      readExtAllowlist: DEFAULT_READ_EXTS,
      writeExtAllowlist: DEFAULT_WRITE_EXTS,
      pathAllowlist: PATH_ALLOWLIST,
      pathDenylist: PATH_DENYLIST,
      controlPlaneConfigured: Boolean(CONTROL_PLANE_BASE_URL && CONTROL_PLANE_API_KEY),
      audit: { path: AUDIT_LOG_BASE, rotateDaily: AUDIT_ROTATE_DAILY, retentionDays: AUDIT_RETENTION_DAYS },
    });
  });

  app.get("/api/mcp/tools", (req: any, res: any) => {
    if (!requireGatewayKey(req, res)) return;
    const openaiTools = tools.map(t => ({ type: "function", function: { name: t.name, description: t.description, parameters: t.parameters } }));
    res.json({ tools: openaiTools });
  });

  app.post("/api/mcp/invoke", async (req: any, res: any) => {
    if (!requireGatewayKey(req, res)) return;

    const traceId = req.header("x-trace-id") || crypto.randomUUID();
    const started = Date.now();

    const { name, arguments: args } = req.body || {};
    const tool = tools.find(t => t.name === name);
    if (!tool) {
      res.status(404).json({ error: { message: "tool_not_found" }, traceId });
      return;
    }

    const argsHash = sha256Json(args || {});
    try {
      const result = await tool.handler(args || {}, traceId);
      const tookMs = Date.now() - started;
      const resultHash = sha256Json(result);

      audit({ ts: Date.now(), traceId, tool: name, permission: tool.permission, argsHash, resultHash, ok: true, tookMs });
      res.json({ ok: true, name, result, traceId, tookMs, argsHash, resultHash });
    } catch (e: any) {
      const tookMs = Date.now() - started;
      const err = String(e?.message || e);
      const resultHash = sha256Json({ error: err });

      audit({ ts: Date.now(), traceId, tool: name, permission: tool.permission, argsHash, resultHash, ok: false, tookMs, error: err });
      res.status(400).json({ ok: false, name, error: err, traceId, tookMs, argsHash, resultHash });
    }
  });
}
