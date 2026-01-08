export const ENV = {
  appId: process.env.VITE_APP_ID ?? "",
  cookieSecret: process.env.JWT_SECRET ?? "",
  databaseUrl: process.env.DATABASE_URL ?? "",
  oAuthServerUrl: process.env.OAUTH_SERVER_URL ?? "",
  ownerOpenId: process.env.OWNER_OPEN_ID ?? "",
  isProduction: process.env.NODE_ENV === "production",
  forgeApiUrl: process.env.BUILT_IN_FORGE_API_URL ?? "",
  forgeApiKey: process.env.BUILT_IN_FORGE_API_KEY ?? "",

  // Optional bearer tokens for non-browser callers (e.g. LLM proxy -> website gateway / MCP).
  // If unset, only session-cookie auth is accepted.
  webGatewayToken:
    process.env.SMARTSPEC_WEB_GATEWAY_TOKEN ??
    process.env.WEB_GATEWAY_TOKEN ??
    "",
  mcpServerToken:
    process.env.SMARTSPEC_MCP_TOKEN ??
    process.env.MCP_SERVER_TOKEN ??
    process.env.SMARTSPEC_WEB_GATEWAY_TOKEN ??
    process.env.WEB_GATEWAY_TOKEN ??
    "",
};
