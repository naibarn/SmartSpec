import { useState } from "react";
import { trpc } from "../trpc";

export default function Factory() {
  const [projectName, setProjectName] = useState("Demo Project");
  const [projectId, setProjectId] = useState("");
  const [sessionId, setSessionId] = useState("");
  const [workspace, setWorkspace] = useState("");
  const [applyToken, setApplyToken] = useState<string>("");
  const [artifactKey, setArtifactKey] = useState("");

  const createProject = trpc.factory.createProject.useMutation();
  const createSession = trpc.factory.createSession.useMutation();
  const evalGates = trpc.factory.evaluateGates.useQuery(
    { projectId, sessionId },
    { enabled: Boolean(projectId && sessionId), refetchInterval: 5000 }
  );
  const tasks = trpc.factory.listTasks.useQuery({ projectId, sessionId }, { enabled: Boolean(projectId && sessionId), refetchInterval: 5000 });
  const reports = trpc.factory.listReports.useQuery({ projectId, sessionId }, { enabled: Boolean(projectId && sessionId), refetchInterval: 5000 });

  const requestApproval = trpc.factory.requestApplyApproval.useMutation();
  const runOrch = trpc.factory.runOrchestrator.useMutation();
  const presignGet = trpc.factory.presignGet.useMutation();

  return (
    <div style={{ padding: 16 }}>
      <h2>SaaS Factory</h2>

      <section style={{ marginTop: 16 }}>
        <h3>1) Create Project / Session</h3>
        <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
          <input value={projectName} onChange={(e) => setProjectName(e.target.value)} placeholder="Project name" />
          <button
            onClick={async () => {
              const res: any = await createProject.mutateAsync({ name: projectName });
              setProjectId(res.project.id ?? res.project?.id ?? res.projectId ?? res.id ?? "");
            }}
          >
            Create Project
          </button>

          <button
            disabled={!projectId}
            onClick={async () => {
              const res: any = await createSession.mutateAsync({ projectId, name: "Session" });
              setSessionId(res.session.id ?? res.session?.id ?? res.id ?? "");
            }}
          >
            Create Session
          </button>
        </div>
        <div style={{ marginTop: 8, fontFamily: "monospace" }}>
          projectId: {projectId || "-"}<br />
          sessionId: {sessionId || "-"}
        </div>
      </section>

      <section style={{ marginTop: 16 }}>
        <h3>2) Approval for Apply</h3>
        <button
          disabled={!projectId || !sessionId}
          onClick={async () => {
            const res: any = await requestApproval.mutateAsync({ projectId, sessionId, reason: "approve apply" });
            setApplyToken(res.token);
          }}
        >
          Request Apply Token
        </button>
        <div style={{ marginTop: 8 }}>
          <textarea value={applyToken} readOnly rows={2} style={{ width: "100%" }} />
          <div style={{ fontSize: 12, opacity: 0.8 }}>Token นี้ใช้ครั้งเดียว และหมดอายุได้</div>
        </div>
      </section>

      <section style={{ marginTop: 16 }}>
        <h3>3) Run Orchestrator</h3>
        <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
          <input value={workspace} onChange={(e) => setWorkspace(e.target.value)} placeholder="Workspace path (server can access)" style={{ minWidth: 360 }} />
          <button
            disabled={!projectId || !sessionId || !workspace}
            onClick={async () => {
              await runOrch.mutateAsync({ projectId, sessionId, workspace, apply: false, maxIterations: 4 });
            }}
          >
            Run (plan-only)
          </button>

          <button
            disabled={!projectId || !sessionId || !workspace || !applyToken}
            onClick={async () => {
              await runOrch.mutateAsync({ projectId, sessionId, workspace, apply: true, applyApprovalToken: applyToken, maxIterations: 4 });
              setApplyToken(""); // consumed
            }}
          >
            Run (apply)
          </button>
        </div>
        {runOrch.error ? <pre style={{ color: "crimson" }}>{String(runOrch.error.message)}</pre> : null}
      </section>

      <section style={{ marginTop: 16 }}>
        <h3>4) Gates / Tasks / Reports</h3>
        <pre>{JSON.stringify(evalGates.data ?? {}, null, 2)}</pre>
        <h4>Tasks</h4>
        <pre>{JSON.stringify(tasks.data ?? {}, null, 2)}</pre>
        <h4>Reports</h4>
        <pre>{JSON.stringify(reports.data ?? {}, null, 2)}</pre>
      </section>

      <section style={{ marginTop: 16 }}>
        <h3>5) Open Artifact (presigned GET)</h3>
        <div style={{ display: "flex", gap: 8 }}>
          <input value={artifactKey} onChange={(e) => setArtifactKey(e.target.value)} placeholder="artifact key" style={{ minWidth: 520 }} />
          <button
            disabled={!projectId || !sessionId || !artifactKey}
            onClick={async () => {
              const res: any = await presignGet.mutateAsync({ projectId, sessionId, key: artifactKey });
              window.open(res.url, "_blank");
            }}
          >
            Open
          </button>
        </div>
      </section>
    </div>
  );
}
