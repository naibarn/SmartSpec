# Developer Guide

## Development Setup

### Install Dependencies

\`\`\`bash
pnpm install
\`\`\`

### Start Development Server

\`\`\`bash
pnpm dev
\`\`\`

## Project Structure

- \`src/components/\` - Reusable components
- \`src/pages/\` - Page components
- \`src/layouts/\` - Layout components
- \`src/contexts/\` - React contexts
- \`src/services/\` - API services
- \`src/lib/\` - Utilities
- \`src/types/\` - TypeScript types

## Adding New Pages

1. Create page component in \`src/pages/\`
2. Add route in \`src/App.tsx\`
3. Update sidebar navigation in \`src/components/dashboard/Sidebar.tsx\`

## Adding shadcn/ui Components

\`\`\`bash
pnpm dlx shadcn@latest add button
\`\`\`

## Code Style

- Use TypeScript
- Follow ESLint rules
- Use Prettier for formatting
- Write meaningful commit messages

## Git Workflow

1. Create feature branch
2. Make changes
3. Commit with descriptive message
4. Push to GitHub
5. Create Pull Request

## Testing

\`\`\`bash
# Run tests (to be implemented)
pnpm test
\`\`\`

---

For more details, see [README.md](../README.md).
