# Deployment Guide

## Prerequisites

- Node.js 18+
- pnpm 8+
- Backend API deployed and accessible

## Environment Variables

Create `.env.production`:

\`\`\`env
VITE_API_BASE_URL=https://api.smartspecpro.com
VITE_STRIPE_PUBLISHABLE_KEY=pk_live_xxx
VITE_GOOGLE_CLIENT_ID=xxx
VITE_GITHUB_CLIENT_ID=xxx
\`\`\`

## Build for Production

\`\`\`bash
pnpm build
\`\`\`

## Deploy to Vercel

\`\`\`bash
vercel --prod
\`\`\`

## Deploy to Netlify

\`\`\`bash
netlify deploy --prod --dir=dist
\`\`\`

## Deploy with Docker

\`\`\`dockerfile
FROM node:18-alpine as build
WORKDIR /app
COPY package.json pnpm-lock.yaml ./
RUN npm install -g pnpm && pnpm install
COPY . .
RUN pnpm build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
\`\`\`

Build and run:

\`\`\`bash
docker build -t smartspec-web .
docker run -p 80:80 smartspec-web
\`\`\`

## Production Checklist

- [ ] Environment variables configured
- [ ] HTTPS enabled
- [ ] CORS configured
- [ ] Error tracking (Sentry)
- [ ] Analytics (Google Analytics)
- [ ] Performance monitoring
- [ ] Security headers
- [ ] CDN configured
- [ ] Backup strategy

---

For more details, see [README.md](../README.md).
