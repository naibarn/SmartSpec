import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import express from "express";
import { createServer } from "http";

function makeStream(body: string) {
  const enc = new TextEncoder();
  const chunks = body.split("");
  let i = 0;
  return new ReadableStream<Uint8Array>({
    pull(controller) {
      if (i >= chunks.length) {
        controller.close();
        return;
      }
      controller.enqueue(enc.encode(chunks[i++]));
    },
  });
}

async function start(app: any) {
  const server = createServer(app);
  await new Promise<void>((resolve) => server.listen(0, resolve));
  const addr = server.address();
  const port = typeof addr === "object" && addr ? addr.port : 0;
  return { server, base: `http://127.0.0.1:${port}` };
}

describe("website gateway /v1/chat/completions", () => {
  const oldEnv = { ...process.env };

  beforeEach(() => {
    process.env = { ...oldEnv };
    process.env.BUILT_IN_FORGE_API_URL = "http://upstream.local";
    process.env.BUILT_IN_FORGE_API_KEY = "forge-key";
    process.env.SMARTSPEC_WEB_GATEWAY_TOKEN = "gwtoken";
    process.env.WEB_LLM_RPM = "9999";
  });

  afterEach(() => {
    process.env = oldEnv;
    vi.restoreAllMocks();
  });

  it("rejects without auth", async () => {
    const { registerLLMRoutes } = await import("./llmRoutes");
    const app = express();
    app.use(express.json());
    registerLLMRoutes(app);
    const { server, base } = await start(app);

    const r = await fetch(`${base}/v1/chat/completions`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ model: "gpt-4.1-mini", messages: [{ role: "user", content: "hi" }] }),
    });

    expect(r.status).toBe(401);
    server.close();
  });

  it("proxies non-stream with bearer token", async () => {
    const { registerLLMRoutes } = await import("./llmRoutes");

    const fake = vi.fn(async () => {
      return new Response(
        JSON.stringify({ id: "x", object: "chat.completion", choices: [{ index: 0, message: { role: "assistant", content: "ok" } }] }),
        { status: 200, headers: { "content-type": "application/json" } }
      );
    });
    // @ts-ignore
    globalThis.fetch = fake;

    const app = express();
    app.use(express.json());
    registerLLMRoutes(app);
    const { server, base } = await start(app);

    const r = await fetch(`${base}/v1/chat/completions`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer gwtoken",
      },
      body: JSON.stringify({ model: "gpt-4.1-mini", messages: [{ role: "user", content: "hi" }] }),
    });

    expect(r.status).toBe(200);
    const j = await r.json();
    expect(j.choices?.[0]?.message?.content).toBe("ok");
    expect(fake).toHaveBeenCalled();
    server.close();
  });

  it("proxies stream and returns event-stream", async () => {
    const { registerLLMRoutes } = await import("./llmRoutes");

    const sse = [
      "data: " + JSON.stringify({ id: "x", object: "chat.completion.chunk", choices: [{ index: 0, delta: { role: "assistant" } }] }),
      "",
      "data: " + JSON.stringify({ id: "x", object: "chat.completion.chunk", choices: [{ index: 0, delta: { content: "Hi" } }] }),
      "",
      "data: [DONE]",
      "",
    ].join("\n");

    const fake = vi.fn(async () => {
      return new Response(makeStream(sse), {
        status: 200,
        headers: { "content-type": "text/event-stream" },
      });
    });
    // @ts-ignore
    globalThis.fetch = fake;

    const app = express();
    app.use(express.json());
    registerLLMRoutes(app);
    const { server, base } = await start(app);

    const r = await fetch(`${base}/v1/chat/completions`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer gwtoken",
      },
      body: JSON.stringify({ model: "gpt-4.1-mini", messages: [{ role: "user", content: "hi" }], stream: true }),
    });

    expect(r.status).toBe(200);
    expect(r.headers.get("content-type") || "").toContain("text/event-stream");
    const txt = await r.text();
    expect(txt).toContain("data: [DONE]");
    server.close();
  });
});
