import type { Express, Request, Response } from "express";
import { ENV } from "./env";
import { authorizeRequest } from "./authz";
import { enforceJsonBodyMaxBytes, rateLimit } from "./limits";

const MAX_LLM_BODY_BYTES = parseInt(process.env.WEB_LLM_MAX_BODY_BYTES || "2097152"); // 2MB
const LLM_RPM = parseInt(process.env.WEB_LLM_RPM || "120");

function assertLlmConfig() {
  if (!ENV.forgeApiUrl || !ENV.forgeApiKey) {
    throw new Error(
      "LLM upstream missing: set BUILT_IN_FORGE_API_URL and BUILT_IN_FORGE_API_KEY"
    );
  }
}

function resolveChatUrl(): string {
  const base = ENV.forgeApiUrl.replace(/\/+$/, "");
  return `${base}/v1/chat/completions`;
}

function upstreamHeaders() {
  return {
    Authorization: `Bearer ${ENV.forgeApiKey}`,
    "Content-Type": "application/json",
  };
}

async function proxyChat(req: Request, res: Response, mode: "stream" | "json") {
  assertLlmConfig();
  const url = resolveChatUrl();

  const controller = new AbortController();
  req.on("close", () => controller.abort());

  const stream = mode === "stream";
  const upstream = await fetch(url, {
    method: "POST",
    headers: upstreamHeaders(),
    body: JSON.stringify({ ...req.body, stream }),
    signal: controller.signal,
  });

  if (!upstream.ok) {
    const message = await upstream.text().catch(() => upstream.statusText);
    res.status(upstream.status || 500).json({ error: { message } });
    return;
  }

  if (!stream) {
    const text = await upstream.text();
    res.status(upstream.status);
    res.type(upstream.headers.get("content-type") || "application/json");
    res.send(text);
    return;
  }

  if (!upstream.body) {
    res.status(500).json({ error: { message: "Upstream stream body missing" } });
    return;
  }

  res.status(200);
  res.setHeader("Content-Type", "text/event-stream; charset=utf-8");
  res.setHeader("Cache-Control", "no-cache, no-transform");
  res.setHeader("Connection", "keep-alive");

  const reader = upstream.body.getReader();
  try {
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      if (value) res.write(Buffer.from(value));
    }
  } finally {
    try { reader.releaseLock(); } catch {}
    res.end();
  }
}

function unauthorized(res: Response) {
  res.status(401).json({ error: { message: "Unauthorized" } });
}

export function registerLLMRoutes(app: Express) {
  const guard = async (req: Request, res: Response): Promise<boolean> => {
    const auth = await authorizeRequest(req, { allowBearer: true, allowSession: true });
    if (!auth.ok) {
      unauthorized(res);
      return false;
    }
    return true;
  };

  const llmLimiter = rateLimit("llm", { rpm: LLM_RPM });

  // OpenAI-compatible gateway endpoints for LLM proxy callers.
  app.post(
    "/v1/chat/completions",
    llmLimiter,
    enforceJsonBodyMaxBytes(MAX_LLM_BODY_BYTES),
    async (req: Request, res: Response) => {
      if (!(await guard(req, res))) return;
      const stream = Boolean(req.body?.stream);
      try {
        await proxyChat(req, res, stream ? "stream" : "json");
      } catch (err: any) {
        res.status(500).json({ error: { message: err?.message || "LLM error" } });
      }
    }
  );

  // Minimal models endpoint (optional but helps OpenAI-compatible clients)
  app.get("/v1/models", llmLimiter, async (req: Request, res: Response) => {
    if (!(await guard(req, res))) return;
    res.json({
      object: "list",
      data: [
        { id: "gpt-4.1-mini", object: "model" },
        { id: "gpt-4o-mini", object: "model" },
      ],
    });
  });

  // UI-friendly REST wrappers (same auth rules)
  app.post(
    "/api/llm/chat",
    llmLimiter,
    enforceJsonBodyMaxBytes(MAX_LLM_BODY_BYTES),
    async (req: Request, res: Response) => {
      if (!(await guard(req, res))) return;
      try {
        await proxyChat(req, res, "json");
      } catch (err: any) {
        res.status(500).json({ error: { message: err?.message || "LLM error" } });
      }
    }
  );

  app.post(
    "/api/llm/stream",
    llmLimiter,
    enforceJsonBodyMaxBytes(MAX_LLM_BODY_BYTES),
    async (req: Request, res: Response) => {
      if (!(await guard(req, res))) return;
      try {
        await proxyChat(req, res, "stream");
      } catch (err: any) {
        // Best-effort SSE error
        res.status(200);
        res.setHeader("Content-Type", "text/event-stream; charset=utf-8");
        res.write(`event: error\n`);
        res.write(
          `data: ${JSON.stringify({ message: err?.message || "Stream error" })}\n\n`
        );
        res.write(`data: [DONE]\n\n`);
        res.end();
      }
    }
  );
}
