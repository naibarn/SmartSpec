import { describe, it, expect } from "vitest";
import { parseSSE } from "./sse";

describe("parseSSE", () => {
  it("parses event+data blocks", () => {
    const payload = [
      "event: tool_status",
      "data: {\"name\":\"workspace_read_file\"}",
      "",
      "data: {\"choices\":[{\"delta\":{\"content\":\"Hi\"}}]}",
      "",
      "data: [DONE]",
      "",
    ].join("\n");

    const ev = parseSSE(payload);
    expect(ev[0].event).toBe("tool_status");
    expect(ev[0].data).toContain("workspace_read_file");
    expect(ev[1].event).toBeUndefined();
    expect(ev[1].data).toContain("choices");
    expect(ev[2].data).toBe("[DONE]");
  });
});
