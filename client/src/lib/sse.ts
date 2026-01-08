export type SSEEvent = {
  event?: string;
  data: string;
};

export function parseSSE(text: string): SSEEvent[] {
  const lines = text.split(/\r?\n/);
  const out: SSEEvent[] = [];
  let curEvent: string | undefined = undefined;
  let curData: string[] = [];

  const flush = () => {
    if (curEvent !== undefined || curData.length > 0) {
      out.push({ event: curEvent, data: curData.join("\n") });
    }
    curEvent = undefined;
    curData = [];
  };

  for (const line of lines) {
    if (line.startsWith("event:")) {
      curEvent = line.slice("event:".length).trim() || undefined;
      continue;
    }
    if (line.startsWith("data:")) {
      curData.push(line.slice("data:".length).trim());
      continue;
    }
    if (line.trim() === "") {
      flush();
    }
  }
  flush();
  return out;
}
