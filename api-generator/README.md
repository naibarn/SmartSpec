# SmartSpec API Generator

**Version:** 1.0.0  
**Status:** Week 0 - Setup  
**Approach:** Hybrid (Template 80% + AI 20%)

---

## Quick Start

```bash
# Generate API from spec
npm run generate -- --spec examples/api-specs/todo.md --output output/todo-api

# Run tests
npm test

# Build
npm run build
```

---

## Project Structure

```
api-generator/
├── src/                      # Source code
│   ├── parser/              # Markdown spec parser
│   ├── analyzer/            # Complexity analyzer
│   ├── template-engine/     # Template-based generation
│   ├── ai-assistant/        # AI-assisted generation
│   ├── validator/           # Code validation
│   ├── output-writer/       # File writer
│   └── utils/               # Utilities
├── templates/               # Code templates
│   └── api/                # API templates
│       ├── controllers/
│       ├── services/
│       ├── models/
│       ├── validators/
│       ├── routes/
│       ├── middleware/
│       └── tests/
├── examples/                # Example specs
│   └── api-specs/
├── tests/                   # Tests
│   ├── unit/
│   └── integration/
├── docs/                    # Documentation
└── output/                  # Generated code (gitignored)
```

---

## Architecture

### Components

1. **Parser** - Parse markdown spec → AST
2. **Analyzer** - Analyze complexity → Template vs AI
3. **Template Engine** - Generate code from templates
4. **AI Assistant** - Generate complex code with AI
5. **Validator** - Validate generated code
6. **Output Writer** - Write files to disk

### Workflow

```
Input Spec (Markdown)
    ↓
Parser → AST
    ↓
Analyzer → Complexity Analysis
    ↓
    ├─→ Template Engine (80%)
    └─→ AI Assistant (20%)
    ↓
Merge & Validate
    ↓
Output Writer
    ↓
Generated API (TypeScript)
```

---

## Development Status

### Week 0 (Current)
- [x] Requirements finalized
- [x] Project structure created
- [ ] Package.json setup
- [ ] TypeScript configuration
- [ ] Template design
- [ ] Example specs

### Week 1-2 (Next)
- [ ] Parser implementation
- [ ] Template engine
- [ ] Basic CRUD generation
- [ ] Demo preparation

---

## Tech Stack

- **Language:** TypeScript
- **Runtime:** Node.js 18+
- **Template Engine:** Handlebars
- **AI:** OpenAI GPT-4
- **Testing:** Jest + Supertest
- **Validation:** Zod
- **Database:** PostgreSQL + Prisma

---

## Requirements

See: [API_GENERATOR_REQUIREMENTS.md](../.smartspec/workflows/API_GENERATOR_REQUIREMENTS.md)

---

## Contributing

1. Follow TypeScript best practices
2. Write tests for all features
3. Update documentation
4. Run linter before commit

---

## License

MIT
