#!/usr/bin/env node
import{c as l}from"../chunk-ZIJ7SYOQ.js";import{PGlite as h}from"@electric-sql/pglite";import{parseArgs as v}from"node:util";var t=v({options:{db:{type:"string",short:"d",default:"memory://",help:"Database path (relative or absolute). Use memory:// for in-memory database."},port:{type:"string",short:"p",default:"5432",help:"Port to listen on"},host:{type:"string",short:"h",default:"127.0.0.1",help:"Host to bind to"},path:{type:"string",short:"u",default:void 0,help:"unix socket to bind to. Takes precedence over host:port"},debug:{type:"string",short:"v",default:"0",help:"Debug level (0-5)"},help:{type:"boolean",short:"?",default:!1,help:"Show help"}}}),b=`PGlite Socket Server
Usage: pglite-server [options]

Options:
  -d, --db=PATH       Database path (default: memory://)
  -p, --port=PORT     Port to listen on (default: 5432)
  -h, --host=HOST     Host to bind to (default: 127.0.0.1)
  -u, --path=UNIX     Unix socket to bind to (default: undefined). Takes precedence over host:port
  -v, --debug=LEVEL   Debug level 0-5 (default: 0)
`;t.values.help&&(console.log(b),process.exit(0));async function f(){try{let e=t.values.db,d=parseInt(t.values.port,10),c=t.values.host,p=t.values.path,u=t.values.debug,n=parseInt(u,10);console.log(`Initializing PGLite with database: ${e}`),console.log(`Debug level: ${n}`);let a=new h(e,{debug:n});await a.waitReady,console.log("PGlite database initialized");let o=new l({db:a,port:d,host:c,path:p,inspect:n>0});o.addEventListener("listening",s=>{let r=s.detail;console.log(`PGLiteSocketServer listening on ${JSON.stringify(r)}`)}),o.addEventListener("connection",s=>{let{clientAddress:r,clientPort:g}=s.detail;console.log(`Client connected from ${r}:${g}`)}),o.addEventListener("error",s=>{let r=s.detail;console.error("Socket server error:",r)}),await o.start();let i=async()=>{console.log(`
Shutting down PGLiteSocketServer...`),await o.stop(),await a.close(),console.log("Server stopped"),process.exit(0)};process.on("SIGINT",i),process.on("SIGTERM",i)}catch(e){console.error("Failed to start PGLiteSocketServer:",e),process.exit(1)}}f().catch(e=>{console.error("Unhandled error:",e),process.exit(1)});
//# sourceMappingURL=server.js.map