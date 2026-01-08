import express from "express";
import { createServer } from "http";
import { fileURLToPath } from "url";
import path from "path";
import cookieParser from "cookie-parser";

import { createContext } from "../context";
import { appRouter } from "../routers";
import { createTRPCExpressMiddleware } from "@trpc/server/adapters/express";
import { serveStatic, setupVite } from "./vite";
import { registerLLMRoutes } from "./llmRoutes";
import { registerMCPRoutes } from "./mcpRoutes";
import { registerOAuthRoutes } from "./oauth";
import { ENV } from "./env";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
app.disable("x-powered-by");

// Baseline security headers (lightweight; no external deps)
app.use((_req, res, next) => {
  res.setHeader("X-Content-Type-Options", "nosniff");
  res.setHeader("X-Frame-Options", "DENY");
  res.setHeader("Referrer-Policy", "no-referrer");
  res.setHeader("Permissions-Policy", "camera=(), microphone=(), geolocation=()");
  next();
});

app.use(express.json({ limit: "50mb" }));
app.use(express.urlencoded({ limit: "50mb", extended: true }));
app.use(cookieParser(ENV.cookieSecret));

// REST/SSE endpoints
registerLLMRoutes(app);
registerMCPRoutes(app);

// OAuth routes
registerOAuthRoutes(app);

app.use(
  "/api/trpc",
  createTRPCExpressMiddleware({
    router: appRouter,
    createContext,
  })
);

async function main() {
  const server = createServer(app);

  if (process.env.NODE_ENV === "development") {
    await setupVite(app, server);
  } else {
    serveStatic(app);
  }

  // Prefer PORT, else pick a free one
  const preferred = parseInt(process.env.PORT || "3000");
  const port = Number.isFinite(preferred) ? preferred : 3000;

  server.listen(port, () => {
    console.log(`SmartSpecWeb listening on http://localhost:${port}`);
  });
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
