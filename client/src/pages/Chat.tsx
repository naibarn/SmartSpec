import { useEffect, useMemo, useRef, useState } from "react";
import { useLocation } from "wouter";
import { trpc } from "@/lib/trpc";
import { useAuth } from "@/contexts/AuthContext";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Loader2, Paperclip, Send, X } from "lucide-react";
import { Streamdown } from "streamdown";

type ChatMessage =
  | { role: "system" | "user"; content: any }
  | { role: "assistant"; content: string };

type Attachment = {
  key: string;
  url: string;
  fileType: string;
  fileName: string;
};

function asUserContent(text: string, atts: Attachment[]) {
  const parts: any[] = [];
  if (text.trim().length > 0) parts.push({ type: "text", text });

  for (const a of atts) {
    if (a.fileType.startsWith("image/")) {
      parts.push({ type: "image_url", image_url: { url: a.url } });
    } else {
      // Most OpenAI-compatible chat endpoints don't accept video inputs directly.
      parts.push({ type: "text", text: `Video: ${a.url}` });
    }
  }
  return parts.length === 1 ? parts[0].text : parts;
}

function renderUserContent(content: any) {
  if (typeof content === "string") return <div className="whitespace-pre-wrap">{content}</div>;
  if (Array.isArray(content)) {
    return (
      <div className="space-y-2">
        {content.map((p: any, i: number) => {
          if (p?.type === "text") return <div key={i} className="whitespace-pre-wrap">{p.text}</div>;
          if (p?.type === "image_url") {
            const url = p?.image_url?.url;
            return url ? (
              <img key={i} src={url} alt="uploaded" className="max-h-64 rounded-md border" />
            ) : null;
          }
          return null;
        })}
      </div>
    );
  }
  return null;
}

export default function Chat() {
  const { isLoading, isAuthenticated } = useAuth();
  const [, setLocation] = useLocation();

  const [messages, setMessages] = useState<ChatMessage[]>([
    { role: "system", content: "You are a helpful assistant." },
  ]);
  const [input, setInput] = useState("");
  const [attachments, setAttachments] = useState<Attachment[]>([]);
  const [isStreaming, setIsStreaming] = useState(false);
  const [toolEvents, setToolEvents] = useState<string[]>([]);
  const [approvalEvents, setApprovalEvents] = useState<string[]>([]);

  const fileRef = useRef<HTMLInputElement>(null);
  const bottomRef = useRef<HTMLDivElement>(null);

  const uploadMutation = trpc.ai.upload.useMutation();

  useEffect(() => {
    if (!isLoading && !isAuthenticated) setLocation("/login");
  }, [isLoading, isAuthenticated, setLocation]);

  const displayMessages = useMemo(
    () => messages.filter((m) => m.role !== "system"),
    [messages]
  );

  const scrollToBottom = () =>
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });

  const handlePickFile = () => fileRef.current?.click();

  const onFiles = async (files: FileList | null) => {
    if (!files || files.length === 0) return;
    const file = files[0];

    const toBase64 = (f: File) =>
      new Promise<string>((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => resolve(String(reader.result || ""));
        reader.onerror = reject;
        reader.readAsDataURL(f);
      });

    const fileBase64 = await toBase64(file);
    const res = await uploadMutation.mutateAsync({
      fileName: file.name,
      fileType: file.type || "application/octet-stream",
      fileBase64,
    });

    setAttachments((prev) => [
      ...prev,
      { key: res.key, url: res.url, fileType: res.fileType, fileName: file.name },
    ]);
  };

  const removeAttachment = (key: string) => {
    setAttachments((prev) => prev.filter((a) => a.key !== key));
  };

  const startStream = async (newMessages: ChatMessage[]) => {
    setIsStreaming(true);
    setToolEvents([]);
    setApprovalEvents([]);

    setMessages((prev) => [...prev, { role: "assistant", content: "" }]);

    const body = {
      model: "gpt-4.1-mini",
      messages: newMessages
        .filter((m) => m.role !== "assistant")
        .map((m) => ({ role: m.role, content: m.content })),
      stream: true,
    };

    const resp = await fetch("/api/llm/stream", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });

    if (!resp.ok || !resp.body) {
      const txt = await resp.text().catch(() => "stream failed");
      setMessages((prev) => {
        const copy = [...prev];
        const last = copy[copy.length - 1];
        if (last?.role === "assistant") last.content += `\n\n[error] ${txt}`;
        return copy;
      });
      setIsStreaming(false);
      return;
    }

    const reader = resp.body.getReader();
    const decoder = new TextDecoder("utf-8");
    let buf = "";
    let curEvent: string | undefined;

    const appendAssistant = (delta: string) => {
      if (!delta) return;
      setMessages((prev) => {
        const copy = [...prev];
        const last = copy[copy.length - 1];
        if (last?.role === "assistant") last.content += delta;
        return copy;
      });
      scrollToBottom();
    };

    try {
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        buf += decoder.decode(value, { stream: true });

        while (true) {
          const idx = buf.indexOf("\n");
          if (idx < 0) break;
          const line = buf.slice(0, idx).replace(/\r$/, "");
          buf = buf.slice(idx + 1);

          if (line.startsWith("event:")) {
            curEvent = line.slice("event:".length).trim() || undefined;
            continue;
          }
          if (line.startsWith("data:")) {
            const data = line.slice("data:".length).trim();
            if (data === "[DONE]") {
              setIsStreaming(false);
              return;
            }

            if (curEvent === "tool_status") {
              setToolEvents((prev) => [...prev, data]);
              continue;
            }
            if (curEvent === "tool_approval_required") {
              setApprovalEvents((prev) => [...prev, data]);
              continue;
            }

            try {
              const j = JSON.parse(data);
              const delta = j?.choices?.[0]?.delta?.content;
              if (typeof delta === "string") appendAssistant(delta);
            } catch {
              appendAssistant(data);
            }
            continue;
          }
          if (line.trim() === "") {
            curEvent = undefined;
          }
        }
      }
    } finally {
      setIsStreaming(false);
      try { reader.releaseLock(); } catch {}
    }
  };

  const onSend = async () => {
    if (isStreaming) return;
    const text = input.trim();
    if (!text && attachments.length === 0) return;

    const content = asUserContent(text, attachments);
    const next = [...messages, { role: "user" as const, content }];

    setMessages(next);
    setInput("");
    setAttachments([]);
    scrollToBottom();

    await startStream(next);
  };

  return (
    <div className="mx-auto flex w-full max-w-6xl flex-col gap-4 p-6">
      <div className="flex items-center justify-between">
        <div className="text-xl font-semibold">Chat</div>
        <div className="flex items-center gap-2">
          {isStreaming ? (
            <Badge variant="secondary" className="gap-2">
              <Loader2 className="size-4 animate-spin" /> Streaming
            </Badge>
          ) : (
            <Badge variant="outline">Ready</Badge>
          )}
        </div>
      </div>

      <div className="grid grid-cols-1 gap-4 lg:grid-cols-[1fr_360px]">
        <Card className="flex h-[70vh] flex-col overflow-hidden">
          <ScrollArea className="flex-1">
            <div className="flex flex-col gap-4 p-4">
              {displayMessages.map((m, i) => (
                <div
                  key={i}
                  className={
                    m.role === "user"
                      ? "ml-auto max-w-[85%] rounded-lg bg-primary px-3 py-2 text-primary-foreground"
                      : "mr-auto max-w-[85%] rounded-lg bg-muted px-3 py-2 text-foreground"
                  }
                >
                  {m.role === "assistant" ? (
                    <Streamdown>{m.content}</Streamdown>
                  ) : (
                    renderUserContent(m.content)
                  )}
                </div>
              ))}
              <div ref={bottomRef} />
            </div>
          </ScrollArea>

          <div className="border-t p-3">
            {attachments.length > 0 && (
              <div className="mb-2 flex flex-wrap gap-2">
                {attachments.map((a) => (
                  <div key={a.key} className="relative">
                    <Badge variant="secondary" className="gap-2 pr-8">
                      {a.fileType.startsWith("image/") ? "IMG" : "VID"} {a.fileName}
                    </Badge>
                    <button
                      className="absolute right-1 top-1/2 -translate-y-1/2 rounded p-1 hover:bg-muted"
                      onClick={() => removeAttachment(a.key)}
                      aria-label="Remove attachment"
                    >
                      <X className="size-3" />
                    </button>
                  </div>
                ))}
              </div>
            )}

            {attachments.some((a) => a.fileType.startsWith("image/")) && (
              <div className="mb-2 flex flex-wrap gap-2">
                {attachments
                  .filter((a) => a.fileType.startsWith("image/"))
                  .map((a) => (
                    <img
                      key={a.key}
                      src={a.url}
                      alt={a.fileName}
                      className="h-16 w-16 rounded border object-cover"
                    />
                  ))}
              </div>
            )}

            {attachments.some((a) => a.fileType.startsWith("video/")) && (
              <div className="mb-2 space-y-2">
                {attachments
                  .filter((a) => a.fileType.startsWith("video/"))
                  .map((a) => (
                    <video key={a.key} src={a.url} controls className="w-full rounded border" />
                  ))}
              </div>
            )}

            <div className="flex gap-2">
              <Button
                variant="outline"
                onClick={handlePickFile}
                disabled={uploadMutation.isPending || isStreaming}
              >
                <Paperclip className="size-4" />
              </Button>
              <input
                ref={fileRef}
                type="file"
                accept="image/*,video/*"
                className="hidden"
                onChange={(e) => onFiles(e.target.files)}
              />
              <Textarea
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Type a message…"
                className="min-h-[44px] resize-none"
                onKeyDown={(e) => {
                  if (e.key === "Enter" && !e.shiftKey) {
                    e.preventDefault();
                    onSend();
                  }
                }}
                disabled={isStreaming}
              />
              <Button onClick={onSend} disabled={isStreaming || uploadMutation.isPending}>
                <Send className="size-4" />
              </Button>
            </div>
            {uploadMutation.isPending && (
              <div className="mt-2 text-sm text-muted-foreground">Uploading…</div>
            )}
          </div>
        </Card>

        <div className="flex flex-col gap-4">
          <Card className="p-4">
            <div className="mb-2 font-medium">Tool status</div>
            {toolEvents.length === 0 ? (
              <div className="text-sm text-muted-foreground">No tool events</div>
            ) : (
              <div className="space-y-2">
                {toolEvents.slice(-8).map((t, i) => (
                  <pre key={i} className="overflow-auto rounded bg-muted p-2 text-xs">
                    {t}
                  </pre>
                ))}
              </div>
            )}
          </Card>

          <Card className="p-4">
            <div className="mb-2 font-medium">Approvals</div>
            {approvalEvents.length === 0 ? (
              <div className="text-sm text-muted-foreground">No approval events</div>
            ) : (
              <div className="space-y-2">
                {approvalEvents.slice(-8).map((t, i) => (
                  <pre key={i} className="overflow-auto rounded bg-muted p-2 text-xs">
                    {t}
                  </pre>
                ))}
              </div>
            )}
          </Card>

          <Card className="p-4">
            <div className="mb-2 font-medium">Notes</div>
            <div className="text-sm text-muted-foreground">
              Images are sent as OpenAI-compatible <code>image_url</code> parts.
              Videos are uploaded and sent as a URL in text.
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
}
