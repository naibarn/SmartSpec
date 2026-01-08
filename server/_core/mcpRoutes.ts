import type { Express, Request, Response } from "express";
import crypto from "crypto";
import fs from "fs";
import path from "path";
import { storageGet } from "../storage";
import { authorizeRequest } from "./authz";
import { rateLimit } from "./limits";
import { hasScope } from "./tokens";

type ToolDef = {
  name: string;
  description: string;
  inputSchema: any;
};

const WORKSPACE_ROOT = process.env.WORKSPACE_ROOT
  ? path.resolve(process.env.WORKSPACE_ROOT)
  : path.resolve(process.cwd(), "workspace");

const MAX_READ_BYTES = parseInt(process.env.MCP_MAX_READ_BYTES || "1048576"); // 1MB
const MAX_WRITE_BYTES = parseInt(process.env.MCP_MAX_WRITE_BYTES || "1048576"); // 1MB
const EXT_ALLOW = new Set(
  (process.env.MCP_EXT_ALLOWLIST ||
    ".md,.txt,.json,.yaml,.yml,.ts,.tsx,.js,.py,.css,.html")
    .split(",")
    .map((s) => s.trim())
    .filter(Boolean)
);

const REQUIRE_WRITE_TOKEN = process.env.MCP_REQUIRE_WRITE_TOKEN === "1";
const WRITE_TOKEN = process.env.MCP_WRITE_TOKEN || "";
const MCP_RPM = parseInt(process.env.WEB_MCP_RPM || "240");

function safeJoin(rel: string): string {
  const cleaned = rel.replace(/^[\\/]+/, "");
  const full = path.resolve(WORKSPACE_ROOT, cleaned);
  if (!full.startsWith(WORKSPACE_ROOT + path.sep) && full !== WORKSPACE_ROOT) {
    throw new Error("Path escapes WORKSPACE_ROOT");
  }
  return full;
}

function assertExtAllowed(p: string) {
  const ext = path.extname(p).toLowerCase();
  if (ext && !EXT_ALLOW.has(ext)) throw new Error(`Extension not allowed: ${ext}`);
}

function writeAudit(entry: any) {
  try {
    const dir = path.resolve(process.cwd(), "logs");
    fs.mkdirSync(dir, { recursive: true });
    fs.appendFileSync(path.join(dir, "mcp_audit.log"), JSON.stringify(entry) + "\n");
  } catch {
    // ignore
  }
}

const tools: ToolDef[] = [
  {
    name: "artifact_get_url",
    description: "Resolve an artifact storage key to a downloadable URL (via storage proxy).",
    inputSchema: {
      type: "object",
      properties: { key: { type: "string" } },
      required: ["key"],
      additionalProperties: false,
    },
  },
  {
    name: "workspace_read_file",
    description:
      "Read a file from WORKSPACE_ROOT with allowlisted extensions and size limit.",
    inputSchema: {
      type: "object",
      properties: { path: { type: "string" } },
      required: ["path"],
      additionalProperties: false,
    },
  },
  {
    name: "workspace_write_file",
    description:
      "Write a file into WORKSPACE_ROOT (optional x-mcp-write-token). Extension allowlist + size limit.",
    inputSchema: {
      type: "object",
      properties: {
        path: { type: "string" },
        content: { type: "string" },
        overwrite: { type: "boolean" },
      },
      required: ["path", "content"],
      additionalProperties: false,
    },
  },
];

function requiredScopeForTool(name: string): string {
  if (name === "workspace_write_file") return "mcp:write";
  return "mcp:read";
}

async function callTool(name: string, args: any, req: Request, auth: any) {
  const traceId = (req.headers["x-trace-id"] as string) || crypto.randomUUID();
  const argsHash = crypto.createHash("sha256").update(JSON.stringify(args || {})).digest("hex");

  const baseAudit = {
    ts: new Date().toISOString(),
    traceId,
    tool: name,
    argsHash,
    ip: req.ip,
    ua: req.headers["user-agent"] || "",
    sub: auth?.sub || null,
    authMode: auth?.mode || null,
  };

  try {
    if (name === "artifact_get_url") {
      const key = String(args?.key || "");
      const res = await storageGet(key);
      writeAudit({ ...baseAudit, ok: true });
      return { ok: true, content: [{ type: "text", text: res.url }], url: res.url };
    }

    if (name === "workspace_read_file") {
      const rel = String(args?.path || "");
      const full = safeJoin(rel);
      assertExtAllowed(full);

      const st = fs.statSync(full);
      if (!st.isFile()) throw new Error("Not a file");
      if (st.size > MAX_READ_BYTES) throw new Error("File too large");

      const buf = fs.readFileSync(full);
      writeAudit({ ...baseAudit, ok: true, bytes: buf.length });
      return { ok: true, content: [{ type: "text", text: buf.toString("utf-8") }] };
    }

    if (name === "workspace_write_file") {
      if (REQUIRE_WRITE_TOKEN) {
        const token = String(req.headers["x-mcp-write-token"] || "");
        if (!WRITE_TOKEN || token !== WRITE_TOKEN) throw new Error("Write token required");
      }
      const rel = String(args?.path || "");
      const content = String(args?.content ?? "");
      const overwrite = Boolean(args?.overwrite ?? true);

      const full = safeJoin(rel);
      assertExtAllowed(full);

      const bytes = Buffer.byteLength(content, "utf-8");
      if (bytes > MAX_WRITE_BYTES) throw new Error("Content too large");

      fs.mkdirSync(path.dirname(full), { recursive: true });
      if (!overwrite && fs.existsSync(full)) throw new Error("File exists");
      fs.writeFileSync(full, content, "utf-8");

      writeAudit({ ...baseAudit, ok: true, bytes });
      return { ok: true, content: [{ type: "text", text: "OK" }] };
    }

    throw new Error(`Unknown tool: ${name}`);
  } catch (err: any) {
    writeAudit({ ...baseAudit, ok: false, error: String(err?.message || err) });
    throw err;
  }
}

async function requireMcpAuth(req: Request): Promise<any | null> {
  const auth = await authorizeRequest(req, { allowBearer: true, allowSession: true });
  if (!auth.ok) return null;
  if (!hasScope(auth.scopes, "mcp:read")) return null;
  return auth;
}

export function registerMCPRoutes(app: Express) {
  const limiter = rateLimit("mcp", { rpm: MCP_RPM });

  const toolsHandler = async (req: Request, res: Response) => {
    const auth = await requireMcpAuth(req);
    if (!auth) {
      writeAudit({
        ts: new Date().toISOString(),
        traceId: (req.headers["x-trace-id"] as string) || crypto.randomUUID(),
        tool: "__list_tools__",
        ok: false,
        error: "Unauthorized",
        ip: req.ip,
        ua: req.headers["user-agent"] || "",
      });
      res.status(401).json({ ok: false, error: { message: "Unauthorized" } });
      return;
    }
    res.json({ tools });
  };

  const callHandler = async (req: Request, res: Response) => {
    const auth = await requireMcpAuth(req);
    if (!auth) {
      writeAudit({
        ts: new Date().toISOString(),
        traceId: (req.headers["x-trace-id"] as string) || crypto.randomUUID(),
        tool: "__call__",
        ok: false,
        error: "Unauthorized",
        ip: req.ip,
        ua: req.headers["user-agent"] || "",
      });
      res.status(401).json({ ok: false, error: { message: "Unauthorized" } });
      return;
    }
    try {
      const { name, arguments: args } = req.body || {};
      const toolName = String(name || "");
      const required = requiredScopeForTool(toolName);
      if (!hasScope(auth.scopes, required)) {
        writeAudit({
          ts: new Date().toISOString(),
          traceId: (req.headers["x-trace-id"] as string) || crypto.randomUUID(),
          tool: toolName,
          ok: false,
          error: `Missing scope: ${required}`,
          sub: auth?.sub || null,
          authMode: auth?.mode || null,
          ip: req.ip,
          ua: req.headers["user-agent"] || "",
        });
        res.status(403).json({ ok: false, error: { message: `Missing scope: ${required}` } });
        return;
      }

      const result = await callTool(toolName, args, req, auth);
      res.json(result);
    } catch (err: any) {
      res.status(400).json({ ok: false, error: { message: err?.message || "Tool error" } });
    }
  };

  app.get("/api/mcp/tools", limiter, toolsHandler);
  app.post("/api/mcp/call", limiter, callHandler);
  app.get("/mcp/tools", limiter, toolsHandler);
  app.post("/mcp/call", limiter, callHandler);
}
