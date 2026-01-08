import { ENV } from "./env";

/**
 * SmartSpecWeb gateway: OpenAI-compatible pass-through to Forge API.
 * Supports both JSON and SSE streaming.
 *
 * Secured by optional SMARTSPEC_WEB_GATEWAY_KEY header: x-gateway-key
 */
const GATEWAY_KEY = process.env.SMARTSPEC_WEB_GATEWAY_KEY ?? "";

function requireGatewayKey(req: any, res: any): boolean {
  if (!GATEWAY_KEY) return true;
  const k = req.header("x-gateway-key") || "";
  if (k !== GATEWAY_KEY) {
    res.status(401).json({ error: { message: "invalid_gateway_key" } });
    return false;
  }
  return true;
}

function resolveApiUrl() {
  return ENV.forgeApiUrl && ENV.forgeApiUrl.trim().length > 0
    ? `${ENV.forgeApiUrl.replace(/\/$/, "")}/v1/chat/completions`
    : "https://forge.manus.im/v1/chat/completions";
}

function assertApiKey() {
  if (!ENV.forgeApiKey) {
    throw new Error("BUILT_IN_FORGE_API_KEY is not configured");
  }
}

export function registerOpenAICompatRoutes(app: any) {
  app.post("/api/v1/llm/openai/chat/completions", async (req: any, res: any) => {
    if (!requireGatewayKey(req, res)) return;

    try {
      assertApiKey();
      const url = resolveApiUrl();
      const payload = req.body || {};
      const stream = !!payload.stream;

      const upstream = await fetch(url, {
        method: "POST",
        headers: {
          "content-type": "application/json",
          authorization: `Bearer ${ENV.forgeApiKey}`,
          ...(stream ? { accept: "text/event-stream" } : {}),
        },
        body: JSON.stringify(payload),
      });

      if (!upstream.ok) {
        const text = await upstream.text();
        res.status(502).json({ error: { message: `forge_error:${upstream.status}:${text}` } });
        return;
      }

      if (!stream) {
        const data = await upstream.json();
        res.json(data);
        return;
      }

      // Stream SSE bytes through
      res.status(200);
      res.setHeader("content-type", "text/event-stream");
      res.setHeader("cache-control", "no-cache, no-transform");
      res.setHeader("connection", "keep-alive");

      const body = upstream.body;
      if (!body) {
        res.write(`data: [DONE]\n\n`);
        res.end();
        return;
      }

      // Node fetch returns a ReadableStream
      const reader = (body as any).getReader();
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        if (value) res.write(Buffer.from(value));
      }
      res.end();
    } catch (e: any) {
      res.status(500).json({ error: { message: String(e?.message || e) } });
    }
  });
}
