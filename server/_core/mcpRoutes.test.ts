import { describe, it, expect, beforeEach, afterEach } from "vitest";
import express from "express";
import { createServer } from "http";
import fs from "fs";
import path from "path";

async function start(app: any) {
  const server = createServer(app);
  await new Promise<void>((resolve) => server.listen(0, resolve));
  const addr = server.address();
  const port = typeof addr === "object" && addr ? addr.port : 0;
  return { server, base: `http://127.0.0.1:${port}` };
}

describe("website MCP server", () => {
  const oldEnv = { ...process.env };
  let tmp: string;

  beforeEach(() => {
    process.env = { ...oldEnv };
    process.env.SMARTSPEC_MCP_TOKEN = "mcptoken";
    process.env.WEB_MCP_RPM = "9999";
    tmp = fs.mkdtempSync(path.join(process.cwd(), "tmp-workspace-"));
    process.env.WORKSPACE_ROOT = tmp;
    process.env.MCP_REQUIRE_WRITE_TOKEN = "1";
    process.env.MCP_WRITE_TOKEN = "wtoken";
  });

  afterEach(() => {
    process.env = oldEnv;
    try { fs.rmSync(tmp, { recursive: true, force: true }); } catch {}
  });

  it("lists tools via /api/mcp/tools and /mcp/tools", async () => {
    const { registerMCPRoutes } = await import("./mcpRoutes");
    const app = express();
    app.use(express.json());
    registerMCPRoutes(app);
    const { server, base } = await start(app);

    const r1 = await fetch(`${base}/api/mcp/tools`, { headers: { Authorization: "Bearer mcptoken" } });
    expect(r1.status).toBe(200);
    const j1 = await r1.json();
    expect(Array.isArray(j1.tools)).toBe(true);

    const r2 = await fetch(`${base}/mcp/tools`, { headers: { Authorization: "Bearer mcptoken" } });
    expect(r2.status).toBe(200);

    server.close();
  });

  it("enforces write token on workspace_write_file", async () => {
    const { registerMCPRoutes } = await import("./mcpRoutes");
    const app = express();
    app.use(express.json());
    registerMCPRoutes(app);
    const { server, base } = await start(app);

    const rBad = await fetch(`${base}/api/mcp/call`, {
      method: "POST",
      headers: { "Content-Type": "application/json", Authorization: "Bearer mcptoken" },
      body: JSON.stringify({ name: "workspace_write_file", arguments: { path: "a.txt", content: "hello" } }),
    });
    expect(rBad.status).toBe(400);

    const rOk = await fetch(`${base}/api/mcp/call`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer mcptoken",
        "x-mcp-write-token": "wtoken",
      },
      body: JSON.stringify({ name: "workspace_write_file", arguments: { path: "a.txt", content: "hello" } }),
    });
    expect(rOk.status).toBe(200);

    const out = fs.readFileSync(path.join(tmp, "a.txt"), "utf-8");
    expect(out).toBe("hello");

    server.close();
  });

  it("blocks path traversal", async () => {
    const { registerMCPRoutes } = await import("./mcpRoutes");
    const app = express();
    app.use(express.json());
    registerMCPRoutes(app);
    const { server, base } = await start(app);

    const r = await fetch(`${base}/api/mcp/call`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer mcptoken",
        "x-mcp-write-token": "wtoken",
      },
      body: JSON.stringify({ name: "workspace_write_file", arguments: { path: "../evil.txt", content: "x" } }),
    });
    expect(r.status).toBe(400);

    server.close();
  });
});
