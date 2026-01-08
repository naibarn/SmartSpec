import { z } from "zod";

const EnvSchema = z.object({
  CONTROL_PLANE_URL: z.string().default("http://localhost:7070"),
  CONTROL_PLANE_API_KEY: z.string().min(24),
  ORCHESTRATOR_URL: z.string().default("http://localhost:8000"),
  ORCHESTRATOR_KEY: z.string().optional(),
});

export type ServerEnv = z.infer<typeof EnvSchema>;

export function loadServerEnv(): ServerEnv {
  const parsed = EnvSchema.safeParse(process.env);
  if (!parsed.success) {
    // eslint-disable-next-line no-console
    console.error(parsed.error.format());
    throw new Error("Invalid SmartSpecWeb server env");
  }
  return parsed.data;
}

export async function mintUserToken(env: ServerEnv, scope?: { projectId?: string; sessionId?: string }) {
  const res = await fetch(`${env.CONTROL_PLANE_URL}/api/v1/auth/token`, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({
      apiKey: env.CONTROL_PLANE_API_KEY,
      scope: { role: "user", projectId: scope?.projectId, sessionId: scope?.sessionId },
      ttlSeconds: 600,
    }),
  });
  if (!res.ok) throw new Error(`mint token failed: ${res.status}`);
  return (await res.json()) as { token: string; expiresInSeconds: number };
}
