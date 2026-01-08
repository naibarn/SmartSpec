import { z } from "zod";
import { publicProcedure, router } from "../trpc"; // adjust to your project helper
import { loadServerEnv, mintUserToken } from "../controlPlaneClient";

const env = loadServerEnv();

async function cpFetch(path: string, token: string, init?: RequestInit) {
  const res = await fetch(`${env.CONTROL_PLANE_URL}${path}`, {
    ...init,
    headers: {
      ...(init?.headers || {}),
      authorization: `Bearer ${token}`,
      "content-type": "application/json",
    },
  });
  const text = await res.text();
  if (!res.ok) throw new Error(text || `control-plane error ${res.status}`);
  return text ? JSON.parse(text) : {};
}

export const factoryRouter = router({
  createProject: publicProcedure.input(z.object({ name: z.string().min(1) })).mutation(async ({ input }) => {
    const { token } = await mintUserToken(env);
    return cpFetch(`/api/v1/projects`, token, { method: "POST", body: JSON.stringify({ name: input.name }) });
  }),

  createSession: publicProcedure.input(z.object({ projectId: z.string(), name: z.string().optional() })).mutation(async ({ input }) => {
    const { token } = await mintUserToken(env, { projectId: input.projectId });
    return cpFetch(`/api/v1/projects/${input.projectId}/sessions`, token, { method: "POST", body: JSON.stringify({ name: input.name ?? null }) });
  }),

  getSession: publicProcedure.input(z.object({ projectId: z.string(), sessionId: z.string() })).query(async ({ input }) => {
    const { token } = await mintUserToken(env, { projectId: input.projectId, sessionId: input.sessionId });
    return cpFetch(`/api/v1/sessions/${input.sessionId}`, token, { method: "GET" });
  }),

  listTasks: publicProcedure.input(z.object({ projectId: z.string(), sessionId: z.string() })).query(async ({ input }) => {
    const { token } = await mintUserToken(env, { projectId: input.projectId, sessionId: input.sessionId });
    return cpFetch(`/api/v1/sessions/${input.sessionId}/tasks`, token, { method: "GET" });
  }),

  listReports: publicProcedure.input(z.object({ projectId: z.string(), sessionId: z.string() })).query(async ({ input }) => {
    const { token } = await mintUserToken(env, { projectId: input.projectId, sessionId: input.sessionId });
    return cpFetch(`/api/v1/sessions/${input.sessionId}/reports`, token, { method: "GET" });
  }),

  evaluateGates: publicProcedure.input(z.object({ projectId: z.string(), sessionId: z.string() })).query(async ({ input }) => {
    const { token } = await mintUserToken(env, { projectId: input.projectId, sessionId: input.sessionId });
    return cpFetch(`/api/v1/sessions/${input.sessionId}/gates/evaluate`, token, { method: "GET" });
  }),

  presignGet: publicProcedure.input(z.object({ projectId: z.string(), sessionId: z.string(), key: z.string() })).mutation(async ({ input }) => {
    const { token } = await mintUserToken(env, { projectId: input.projectId, sessionId: input.sessionId });
    return cpFetch(`/api/v1/sessions/${input.sessionId}/artifacts/presign-get?key=${encodeURIComponent(input.key)}`, token, { method: "GET" });
  }),

  requestApplyApproval: publicProcedure.input(z.object({ projectId: z.string(), sessionId: z.string(), reason: z.string().optional() })).mutation(async ({ input }) => {
    const { token } = await mintUserToken(env, { projectId: input.projectId, sessionId: input.sessionId });
    return cpFetch(`/api/v1/sessions/${input.sessionId}/approvals/apply`, token, { method: "POST", body: JSON.stringify({ reason: input.reason ?? null }) });
  }),

  runOrchestrator: publicProcedure.input(z.object({
    projectId: z.string(),
    sessionId: z.string(),
    workspace: z.string(),
    apply: z.boolean().default(false),
    applyApprovalToken: z.string().optional(),
    maxIterations: z.number().int().min(1).max(50).default(8),
  })).mutation(async ({ input }) => {
    // Orchestrator is localhost-only by default. For web deployments, run orchestrator as a server-side job.
    // This endpoint is provided for dev/staging where SmartSpecWeb server can reach orchestrator.
    const headers: Record<string, string> = { "content-type": "application/json" };
    if (env.ORCHESTRATOR_KEY) headers["x-orchestrator-key"] = env.ORCHESTRATOR_KEY;

    const res = await fetch(`${env.ORCHESTRATOR_URL}/api/v1/orchestrator/factory/run`, {
      method: "POST",
      headers,
      body: JSON.stringify({
        projectId: input.projectId,
        sessionId: input.sessionId,
        workspace: input.workspace,
        apply: input.apply,
        applyApprovalToken: input.applyApprovalToken ?? null,
        maxIterations: input.maxIterations,
      }),
    });
    const text = await res.text();
    if (!res.ok) throw new Error(text || `orchestrator error ${res.status}`);
    return text ? JSON.parse(text) : {};
  }),
});
