import type { Request, Response } from "express";
import { invokeLLM } from "./llm";

function assertGatewayKey(req: Request) {
  const required = process.env.SMARTSPEC_WEB_GATEWAY_KEY || "";
  if (!required) return; // dev mode
  const got = (req.header("x-gateway-key") || "").trim();
  if (got !== required) {
    const err = new Error("Unauthorized");
    // @ts-ignore
    err.status = 401;
    throw err;
  }
}

export async function openaiChatCompletions(req: Request, res: Response) {
  try {
    assertGatewayKey(req);

    // Accept OpenAI-compatible request payload as-is:
    // { model, messages, tools, tool_choice, response_format, ... }
    const body = req.body ?? {};
    const messages = body.messages ?? [];

    const result = await invokeLLM({
      messages,
      tools: body.tools,
      tool_choice: body.tool_choice,
      toolChoice: body.toolChoice,
      response_format: body.response_format,
      responseFormat: body.responseFormat,
      output_schema: body.output_schema,
      outputSchema: body.outputSchema,
      max_tokens: body.max_tokens,
      maxTokens: body.maxTokens,
    });

    res.json(result);
  } catch (e: any) {
    const status = e?.status || 500;
    res.status(status).json({ error: e?.message || "Gateway error" });
  }
}
