# Auth Generator API Documentation

**Version:** 1.0.0  
**Last Updated:** December 27, 2025

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Installation](#2-installation)
3. [Core Concepts](#3-core-concepts)
4. [API Reference](#4-api-reference)
5. [Usage Examples](#5-usage-examples)
6. [Configuration](#6-configuration)
7. [Error Handling](#7-error-handling)
8. [Performance](#8-performance)
9. [Testing](#9-testing)
10. [Troubleshooting](#10-troubleshooting)
11. [Migration Guide](#11-migration-guide)
12. [Contributing](#12-contributing)
13. [Appendix](#13-appendix)

---

## 1. Introduction

### What is Auth Generator?

Auth Generator is a powerful code generation tool that transforms human-readable authentication specifications into production-ready TypeScript code. It eliminates the repetitive task of writing authentication boilerplate by automatically generating controllers, middleware, services, types, and routes based on your specifications.

### Key Features

The Auth Generator provides comprehensive authentication functionality out of the box. It supports multiple authentication methods including email/password, OAuth, and JWT-based authentication. The generator includes built-in security features such as password hashing with bcrypt, JWT token management with RS256 algorithm, and account lockout protection against brute force attacks.

Role-Based Access Control (RBAC) is fully integrated, allowing you to define custom roles and permissions. Optional features include email verification for new accounts, password reset functionality with secure token generation, and rate limiting to protect against abuse.

The generated code is production-ready TypeScript with comprehensive type safety, Zod validation for all inputs, proper error handling with custom error classes, and detailed JSDoc documentation. The modular architecture ensures clean separation of concerns with independent controllers, services, middleware, types, and routes.

### Use Cases

Auth Generator is ideal for various scenarios. When building new applications, it provides instant authentication setup without writing boilerplate code. For existing applications, it helps standardize authentication across microservices. During prototyping, it enables rapid MVP development with production-quality auth. In learning contexts, it serves as a reference implementation of authentication best practices.

### Quick Start

Getting started with Auth Generator is straightforward. First, install the package using npm or pnpm. Then create an authentication specification file describing your requirements. Finally, run the generator to produce your authentication code. The entire process takes less than a minute from specification to working code.

```bash
# Install
npm install @smartspec/auth-generator

# Create spec file (auth-spec.md)
# See examples/auth-specs/ for templates

# Generate code
npx auth-generator generate auth-spec.md --output ./src/auth
```

---

## 2. Installation

### Prerequisites

Before installing Auth Generator, ensure your development environment meets the following requirements. You need Node.js version 18.0.0 or higher, and either npm version 8.0.0 or higher, or pnpm version 8.0.0 or higher. TypeScript 5.0.0 or higher is required for the generated code to compile properly.

### Installation Steps

The installation process is simple and follows standard npm package installation procedures.

**Using npm:**
```bash
npm install @smartspec/auth-generator
```

**Using pnpm:**
```bash
pnpm add @smartspec/auth-generator
```

**Using yarn:**
```bash
yarn add @smartspec/auth-generator
```

For development or contributing to the project, you can clone the repository and install dependencies locally.

```bash
git clone https://github.com/smartspec/auth-generator.git
cd auth-generator
pnpm install
pnpm build
```

### Verification

After installation, verify that Auth Generator is working correctly by checking the version and running a simple generation test.

```bash
# Check version
npx auth-generator --version

# Run test generation
npx auth-generator generate examples/auth-specs/minimal-auth.md --output ./test-output
```

If the generation completes successfully and produces five TypeScript files in the output directory, your installation is working correctly.

---

## 3. Core Concepts

### Auth Specification (Spec)

An Auth Specification is a Markdown document that describes your authentication requirements in a structured, human-readable format. The specification includes sections for user model definition, authentication methods, token configuration, protected and public endpoints, features, security settings, and business rules.

The specification format is designed to be intuitive and easy to write. You describe what you want in plain language with some structure, and the generator handles the implementation details. For example, you can specify "Password must be at least 8 characters" and the generator will create the appropriate validation logic.

### Abstract Syntax Tree (AST)

The Abstract Syntax Tree is an intermediate representation of your specification after parsing. The parser reads your Markdown specification and converts it into a structured JavaScript object that the generator can process. This separation of parsing and generation allows for flexibility and extensibility.

The AST contains all the information from your specification in a normalized format. It includes typed objects for user models, authentication methods, token configuration, endpoints, features, security settings, and business rules. The generator uses this AST to prepare the context for template rendering.

### Templates

Templates are Handlebars files that define the structure of the generated code. Each template corresponds to a specific file type such as controller, middleware, types, routes, or service. Templates use placeholders and conditional logic to generate code based on your specification.

The template system is powerful and flexible. It supports conditional rendering based on features, iteration over collections like roles and endpoints, custom helpers for string manipulation and logic, and nested templates for complex structures. You can also create custom templates to extend the generator's capabilities.

### Code Generation Flow

The code generation process follows a clear pipeline from specification to code. First, the specification file is read from disk. The parser then converts the Markdown content into an AST. The generator prepares the template context from the AST, extracting features, RBAC configuration, JWT settings, and security settings.

Templates are compiled using Handlebars, and each template is rendered with the prepared context. The generated code is written to the output directory, creating the necessary folder structure. The entire process typically completes in under 100 milliseconds.

### Architecture Diagram

```
┌─────────────────────┐
│  Auth Spec (MD)     │
│  - User Model       │
│  - Features         │
│  - Security         │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  AuthSpecParser     │
│  - Parse Markdown   │
│  - Extract Sections │
│  - Build AST        │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  AuthSpec (AST)     │
│  - Structured Data  │
│  - Type-Safe        │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  AuthGenerator      │
│  - Load Templates   │
│  - Prepare Context  │
│  - Render Templates │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Generated Code     │
│  - Controller       │
│  - Middleware       │
│  - Types            │
│  - Routes           │
│  - Service          │
└─────────────────────┘
```

---

## 4. API Reference

### 4.1 AuthGenerator Class

The AuthGenerator class is the main entry point for code generation. It handles template loading, context preparation, and file generation.

#### Constructor

```typescript
constructor(options?: Partial<GeneratorOptions>)
```

Creates a new AuthGenerator instance with optional configuration.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| options | `Partial<GeneratorOptions>` | No | Generator configuration options |
| options.templateDir | `string` | No | Custom template directory path (default: built-in templates) |

**Examples:**

```typescript
// Default configuration
const generator = new AuthGenerator();

// Custom template directory
const generator = new AuthGenerator({
  templateDir: '/path/to/custom/templates'
});
```

#### generateFromFile()

```typescript
async generateFromFile(
  specPath: string,
  options: GeneratorOptions
): Promise<GeneratedFile[]>
```

Generates authentication code from a specification file.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| specPath | `string` | Yes | Path to the auth specification file (.md) |
| options | `GeneratorOptions` | Yes | Generation options |
| options.outputDir | `string` | Yes | Directory where generated files will be written |
| options.overwrite | `boolean` | No | Whether to overwrite existing files (default: true) |

**Return Value:**

Returns a Promise that resolves to an array of `GeneratedFile` objects, each containing the file path, content, and type.

**Examples:**

```typescript
// Basic usage
const files = await generator.generateFromFile(
  './specs/auth-spec.md',
  {
    outputDir: './src/auth',
    overwrite: true
  }
);

console.log(`Generated ${files.length} files`);
files.forEach(file => {
  console.log(`- ${file.type}: ${file.path}`);
});

// Without writing files
const files = await generator.generateFromFile(
  './specs/auth-spec.md',
  {
    outputDir: './src/auth',
    overwrite: false
  }
);

// Files are generated but not written to disk
console.log(files[0].content); // View generated code
```

**Error Handling:**

The method throws errors in the following cases:
- File not found: If the specification file doesn't exist
- Parse error: If the specification format is invalid
- Template error: If template rendering fails
- Write error: If file writing fails (when overwrite is true)

```typescript
try {
  const files = await generator.generateFromFile(specPath, options);
} catch (error) {
  if (error.code === 'ENOENT') {
    console.error('Spec file not found');
  } else if (error.name === 'ParseError') {
    console.error('Invalid spec format:', error.message);
  } else {
    console.error('Generation failed:', error);
  }
}
```

#### generateFromContent()

```typescript
async generateFromContent(
  specContent: string,
  options: GeneratorOptions
): Promise<GeneratedFile[]>
```

Generates authentication code from a specification string.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| specContent | `string` | Yes | Auth specification content as string |
| options | `GeneratorOptions` | Yes | Generation options |

**Return Value:**

Returns a Promise that resolves to an array of `GeneratedFile` objects.

**Examples:**

```typescript
const specContent = `
# Authentication Specification

## User Model
- id: string (UUID)
- email: string (unique)
- password: string (hashed)

## Features
- Email verification: yes
- Password reset: yes
`;

const files = await generator.generateFromContent(specContent, {
  outputDir: './src/auth',
  overwrite: true
});
```

**Error Handling:**

Similar to `generateFromFile()`, but without file system read errors.

#### generate()

```typescript
async generate(
  ast: AuthSpec,
  options: GeneratorOptions
): Promise<GeneratedFile[]>
```

Generates authentication code from a parsed AST.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| ast | `AuthSpec` | Yes | Parsed authentication specification |
| options | `GeneratorOptions` | Yes | Generation options |

**Return Value:**

Returns a Promise that resolves to an array of `GeneratedFile` objects.

**Examples:**

```typescript
// Parse spec first
const parser = generator.getParser();
const ast = parser.parse(specContent);

// Modify AST if needed
ast.features.emailVerification = true;

// Generate from modified AST
const files = await generator.generate(ast, {
  outputDir: './src/auth',
  overwrite: true
});
```

**Error Handling:**

Throws errors for invalid AST structure or template rendering failures.

#### validateSpec()

```typescript
async validateSpec(specPath: string): Promise<ValidationResult>
```

Validates a specification file without generating code.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| specPath | `string` | Yes | Path to the auth specification file |

**Return Value:**

Returns a Promise that resolves to a `ValidationResult` object:

```typescript
interface ValidationResult {
  valid: boolean;
  errors: string[];
  warnings?: string[];
}
```

**Examples:**

```typescript
const result = await generator.validateSpec('./specs/auth-spec.md');

if (result.valid) {
  console.log('✓ Spec is valid');
  // Proceed with generation
} else {
  console.error('✗ Spec validation failed:');
  result.errors.forEach(error => console.error(`  - ${error}`));
}

if (result.warnings && result.warnings.length > 0) {
  console.warn('Warnings:');
  result.warnings.forEach(warning => console.warn(`  - ${warning}`));
}
```

**Error Handling:**

Throws error if file cannot be read. Returns validation errors in the result object rather than throwing.

#### getParser()

```typescript
getParser(): AuthSpecParser
```

Returns the internal parser instance for advanced usage.

**Return Value:**

Returns an `AuthSpecParser` instance.

**Use Cases:**

This method is useful when you need to parse a specification without generating code, inspect the AST structure, or implement custom generation logic.

**Examples:**

```typescript
const parser = generator.getParser();
const ast = parser.parse(specContent);

// Inspect AST
console.log('Features:', ast.features);
console.log('Roles:', ast.rbac?.roles);

// Custom processing
if (ast.features.emailVerification) {
  // Add custom email templates
}
```

### 4.2 AuthSpecParser Class

The AuthSpecParser class handles parsing of Markdown specifications into AST.

#### Constructor

```typescript
constructor()
```

Creates a new parser instance. No configuration required.

#### parse()

```typescript
parse(content: string): AuthSpec
```

Parses a specification string into an AST.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| content | `string` | Yes | Markdown specification content |

**Return Value:**

Returns an `AuthSpec` object representing the parsed specification.

**Examples:**

```typescript
import { AuthSpecParser } from '@smartspec/auth-generator';

const parser = new AuthSpecParser();
const ast = parser.parse(specContent);

console.log('User fields:', ast.userModel.fields);
console.log('Features:', ast.features);
```

### 4.3 Types & Interfaces

#### GeneratorOptions

Configuration options for code generation.

```typescript
interface GeneratorOptions {
  outputDir: string;        // Output directory path
  templateDir?: string;     // Custom template directory (optional)
  overwrite?: boolean;      // Overwrite existing files (default: true)
}
```

#### GeneratedFile

Represents a generated code file.

```typescript
interface GeneratedFile {
  path: string;            // Absolute file path
  content: string;         // Generated code content
  type: FileType;          // File type identifier
}

type FileType = 'controller' | 'middleware' | 'types' | 'routes' | 'service';
```

#### AuthSpec (AST)

The complete authentication specification structure.

```typescript
interface AuthSpec {
  userModel: UserModel;
  authMethods: AuthMethods;
  tokenConfig: TokenConfig;
  protectedEndpoints: ProtectedEndpoint[];
  publicEndpoints: PublicEndpoint[];
  features: Features;
  securitySettings: SecuritySettings;
  businessRules: BusinessRules;
  errorResponses: ErrorResponse[];
}
```

**UserModel:**

```typescript
interface UserModel {
  fields: Field[];
  indexes: Index[];
}

interface Field {
  name: string;
  type: string;
  required?: boolean;
  unique?: boolean;
  default?: any;
  validation?: string;
}
```

**Features:**

```typescript
interface Features {
  emailVerification: boolean;
  passwordReset: boolean;
  accountLockout: boolean;
  rbac?: RBACConfig;
}

interface RBACConfig {
  enabled: boolean;
  roles: Role[];
  defaultRole: string;
}

interface Role {
  name: string;
  permissions?: string[];
}
```

**TokenConfig:**

```typescript
interface TokenConfig {
  accessToken: {
    expiresIn: string;    // e.g., "15m"
    algorithm: string;    // e.g., "RS256"
  };
  refreshToken: {
    expiresIn: string;    // e.g., "7d"
  };
  issuer?: string;
  audience?: string;
}
```

**SecuritySettings:**

```typescript
interface SecuritySettings {
  passwordRequirements: {
    minLength: number;
    requireUppercase: boolean;
    requireLowercase: boolean;
    requireNumbers: boolean;
    requireSpecialChars: boolean;
    saltRounds: number;
  };
  accountSecurity: {
    maxLoginAttempts: number;
    lockoutDuration: number;  // minutes
  };
}
```

---

## 5. Usage Examples

### 5.1 Basic Usage

#### Generate from File

The most common usage pattern is generating code from a specification file.

```typescript
import { AuthGenerator } from '@smartspec/auth-generator';

const generator = new AuthGenerator();

async function generateAuth() {
  try {
    const files = await generator.generateFromFile(
      './specs/auth-spec.md',
      {
        outputDir: './src/auth',
        overwrite: true
      }
    );

    console.log(`✓ Generated ${files.length} files:`);
    files.forEach(file => {
      console.log(`  - ${file.type}: ${file.path}`);
    });
  } catch (error) {
    console.error('Generation failed:', error.message);
  }
}

generateAuth();
```

#### Generate from Content

You can also generate code from a specification string, useful for dynamic generation or testing.

```typescript
const specContent = `
# Authentication Specification: My App

## User Model
- id: string (UUID, primary key)
- email: string (required, unique)
- password: string (required, hashed)
- createdAt: datetime (auto)

## Features
- Email verification: yes
- Password reset: yes
`;

const files = await generator.generateFromContent(specContent, {
  outputDir: './src/auth'
});
```

#### Custom Output Directory

Organize generated files according to your project structure.

```typescript
// Generate to specific module
await generator.generateFromFile('./specs/auth-spec.md', {
  outputDir: './src/modules/authentication'
});

// Generate to multiple locations
const specs = ['user-auth.md', 'admin-auth.md'];

for (const spec of specs) {
  const name = spec.replace('.md', '');
  await generator.generateFromFile(`./specs/${spec}`, {
    outputDir: `./src/auth/${name}`
  });
}
```

### 5.2 Advanced Usage

#### Custom Template Directory

Use your own templates for customized code generation.

```typescript
const generator = new AuthGenerator({
  templateDir: './custom-templates'
});

// Templates should follow the same structure:
// custom-templates/
//   auth/
//     controllers/auth.controller.ts.hbs
//     middleware/auth.middleware.ts.hbs
//     types/auth.types.ts.hbs
//     routes/auth.routes.ts.hbs
//     services/auth.service.ts.hbs

const files = await generator.generateFromFile('./specs/auth-spec.md', {
  outputDir: './src/auth'
});
```

#### Generate Without Writing Files

Generate code in memory for inspection or further processing.

```typescript
const files = await generator.generateFromFile('./specs/auth-spec.md', {
  outputDir: './src/auth',
  overwrite: false  // Don't write to disk
});

// Inspect generated code
const controller = files.find(f => f.type === 'controller');
console.log('Generated controller:');
console.log(controller.content);

// Post-process code
const modifiedContent = controller.content.replace(
  'export class AuthController',
  'export class MyAuthController'
);

// Write manually
await fs.writeFile(controller.path, modifiedContent);
```

#### Validate Spec Before Generation

Always validate specifications before generation in production environments.

```typescript
async function safeGenerate(specPath: string, outputDir: string) {
  // Validate first
  const validation = await generator.validateSpec(specPath);
  
  if (!validation.valid) {
    console.error('Spec validation failed:');
    validation.errors.forEach(err => console.error(`  - ${err}`));
    return;
  }
  
  // Show warnings
  if (validation.warnings?.length > 0) {
    console.warn('Warnings:');
    validation.warnings.forEach(warn => console.warn(`  - ${warn}`));
  }
  
  // Generate
  const files = await generator.generateFromFile(specPath, { outputDir });
  console.log(`✓ Generated ${files.length} files`);
}
```

#### Access Parsed AST

Parse and inspect the AST for custom processing.

```typescript
const parser = generator.getParser();
const ast = parser.parse(specContent);

// Inspect structure
console.log('Features:', ast.features);
console.log('Roles:', ast.features.rbac?.roles);
console.log('Security:', ast.securitySettings);

// Conditional generation
if (ast.features.emailVerification) {
  console.log('Email verification enabled - will generate verification endpoints');
}

// Modify AST before generation
ast.features.accountLockout = true;
ast.securitySettings.accountSecurity.maxLoginAttempts = 3;

// Generate with modified AST
const files = await generator.generate(ast, {
  outputDir: './src/auth'
});
```

### 5.3 Integration Examples

#### Express.js Integration

Integrate generated authentication with an Express.js application.

```typescript
// Generate auth code
import { AuthGenerator } from '@smartspec/auth-generator';

const generator = new AuthGenerator();
await generator.generateFromFile('./specs/auth-spec.md', {
  outputDir: './src/auth'
});

// app.ts
import express from 'express';
import { authRouter } from './auth/routes/auth.routes';
import { AuthMiddleware } from './auth/middleware/auth.middleware';

const app = express();
const authMiddleware = new AuthMiddleware();

app.use(express.json());

// Public auth routes
app.use('/auth', authRouter);

// Protected routes
app.get('/api/profile', 
  authMiddleware.authenticate(),
  (req, res) => {
    res.json({ user: req.user });
  }
);

// Role-protected routes
app.get('/api/admin/users',
  authMiddleware.authenticate(),
  authMiddleware.requireRole('admin'),
  (req, res) => {
    // Admin only
  }
);

app.listen(3000);
```

#### NestJS Integration

Use generated code in a NestJS application.

```typescript
// Generate with NestJS-compatible templates
const generator = new AuthGenerator({
  templateDir: './templates/nestjs'
});

await generator.generateFromFile('./specs/auth-spec.md', {
  outputDir: './src/auth'
});

// auth.module.ts
import { Module } from '@nestjs/common';
import { AuthController } from './controllers/auth.controller';
import { AuthService } from './services/auth.service';
import { AuthMiddleware } from './middleware/auth.middleware';

@Module({
  controllers: [AuthController],
  providers: [AuthService, AuthMiddleware],
  exports: [AuthService, AuthMiddleware],
})
export class AuthModule {}
```

#### Standalone Usage

Use the generator in scripts or CLI tools.

```typescript
#!/usr/bin/env node

import { AuthGenerator } from '@smartspec/auth-generator';
import { Command } from 'commander';

const program = new Command();

program
  .name('auth-gen')
  .description('Generate authentication code from specification')
  .argument('<spec>', 'Path to auth specification file')
  .option('-o, --output <dir>', 'Output directory', './src/auth')
  .option('-t, --templates <dir>', 'Custom templates directory')
  .option('--no-overwrite', 'Do not overwrite existing files')
  .action(async (spec, options) => {
    const generator = new AuthGenerator({
      templateDir: options.templates
    });

    try {
      const files = await generator.generateFromFile(spec, {
        outputDir: options.output,
        overwrite: options.overwrite
      });

      console.log(`✓ Generated ${files.length} files in ${options.output}`);
    } catch (error) {
      console.error('Error:', error.message);
      process.exit(1);
    }
  });

program.parse();
```

---

## 6. Configuration

### 6.1 Generator Options

The AuthGenerator accepts configuration options to customize its behavior.

**outputDir** (required)

The directory where generated files will be written. The generator creates subdirectories for each file type (controllers, middleware, types, routes, services).

```typescript
{
  outputDir: './src/auth'  // Creates ./src/auth/controllers/, etc.
}
```

**templateDir** (optional)

Path to a custom template directory. If not provided, the generator uses built-in templates. Custom templates must follow the same structure as built-in templates.

```typescript
{
  templateDir: './my-templates/auth'
}
```

**overwrite** (optional, default: true)

Whether to overwrite existing files. When false, files are generated in memory but not written to disk, useful for previewing or post-processing.

```typescript
{
  overwrite: false  // Generate but don't write
}
```

### 6.2 Template Configuration

#### Template Structure

Templates must be organized in a specific directory structure:

```
templates/
  auth/
    controllers/
      auth.controller.ts.hbs
    middleware/
      auth.middleware.ts.hbs
    types/
      auth.types.ts.hbs
    routes/
      auth.routes.ts.hbs
    services/
      auth.service.ts.hbs
```

#### Custom Templates

To use custom templates, create your own template files following the structure above and pass the template directory to the generator.

```typescript
const generator = new AuthGenerator({
  templateDir: path.join(__dirname, 'templates')
});
```

Custom templates receive the same context as built-in templates, allowing you to customize the generated code while maintaining compatibility with the specification format.

#### Template Context

Templates receive a context object with the following structure:

```typescript
{
  features: {
    emailVerification: boolean,
    passwordReset: boolean,
    accountLockout: boolean
  },
  rbac: {
    enabled: boolean,
    roles: Array<{ name: string }>,
    defaultRole: string
  },
  jwtSettings: {
    algorithm: string,
    accessTokenExpiry: string,
    refreshTokenExpiry: string,
    issuer: string,
    audience: string
  },
  securitySettings: {
    passwordRequirements: { ... },
    accountLockout: { ... }
  },
  userModel: {
    fields: Array<{ name, type, ... }>
  },
  excludedFields: string[]
}
```

---

## 7. Error Handling

### 7.1 Common Errors

#### File Not Found

Occurs when the specification file doesn't exist at the given path.

```typescript
try {
  await generator.generateFromFile('./nonexistent.md', options);
} catch (error) {
  if (error.code === 'ENOENT') {
    console.error('Specification file not found');
    console.error('Please check the file path and try again');
  }
}
```

#### Invalid Spec Format

Occurs when the specification file has invalid format or missing required sections.

```typescript
try {
  await generator.generateFromFile('./invalid-spec.md', options);
} catch (error) {
  if (error.name === 'ParseError') {
    console.error('Invalid specification format:', error.message);
    console.error('Please check the specification syntax');
  }
}
```

#### Template Not Found

Occurs when using custom templates and a required template file is missing.

```typescript
try {
  const generator = new AuthGenerator({
    templateDir: './custom-templates'
  });
  await generator.generateFromFile(specPath, options);
} catch (error) {
  if (error.message.includes('template')) {
    console.error('Template file missing');
    console.error('Ensure all required templates exist in:', './custom-templates');
  }
}
```

#### Write Permission Errors

Occurs when the generator doesn't have permission to write to the output directory.

```typescript
try {
  await generator.generateFromFile(specPath, {
    outputDir: '/root/protected'
  });
} catch (error) {
  if (error.code === 'EACCES') {
    console.error('Permission denied');
    console.error('Please check write permissions for the output directory');
  }
}
```

### 7.2 Error Types

The generator uses custom error classes for better error handling.

**AuthGeneratorError**

Base error class for all generator errors.

```typescript
class AuthGeneratorError extends Error {
  constructor(message: string, public code?: string) {
    super(message);
    this.name = 'AuthGeneratorError';
  }
}
```

**ParserError**

Thrown when specification parsing fails.

```typescript
class ParserError extends AuthGeneratorError {
  constructor(message: string, public line?: number) {
    super(message, 'PARSE_ERROR');
    this.name = 'ParserError';
  }
}
```

**TemplateError**

Thrown when template rendering fails.

```typescript
class TemplateError extends AuthGeneratorError {
  constructor(message: string, public template?: string) {
    super(message, 'TEMPLATE_ERROR');
    this.name = 'TemplateError';
  }
}
```

### 7.3 Best Practices

#### Try-Catch Blocks

Always wrap generator calls in try-catch blocks to handle errors gracefully.

```typescript
async function generateWithErrorHandling() {
  try {
    const files = await generator.generateFromFile(specPath, options);
    console.log('✓ Generation successful');
    return files;
  } catch (error) {
    console.error('✗ Generation failed:', error.message);
    
    // Log detailed error information
    if (error.stack) {
      console.error('Stack trace:', error.stack);
    }
    
    // Return empty array or throw depending on use case
    return [];
  }
}
```

#### Error Logging

Log errors with sufficient context for debugging.

```typescript
import winston from 'winston';

const logger = winston.createLogger({ /* config */ });

try {
  await generator.generateFromFile(specPath, options);
} catch (error) {
  logger.error('Code generation failed', {
    specPath,
    outputDir: options.outputDir,
    error: error.message,
    stack: error.stack,
    timestamp: new Date().toISOString()
  });
}
```

#### Graceful Degradation

Provide fallback behavior when generation fails.

```typescript
async function generateOrUseFallback(specPath: string) {
  try {
    return await generator.generateFromFile(specPath, options);
  } catch (error) {
    console.warn('Generation failed, using fallback templates');
    
    // Use pre-generated templates or default implementation
    return loadFallbackTemplates();
  }
}
```

---

## 8. Performance

### 8.1 Benchmarks

Auth Generator is optimized for fast code generation with minimal overhead.

**Generation Speed:**

| Spec Type | Files | Lines | Time | Speed |
|-----------|-------|-------|------|-------|
| Minimal | 5 | ~800 | 40-50ms | 16,000 lines/s |
| Standard | 5 | ~1,000 | 50-60ms | 16,600 lines/s |
| Advanced | 5 | ~1,200 | 60-80ms | 15,000 lines/s |

**Memory Usage:**

The generator has a small memory footprint, typically using less than 50MB of RAM during generation.

**File I/O:**

File operations are optimized with parallel writes and efficient buffering. Writing 5 files typically takes less than 10ms on modern SSDs.

### 8.2 Optimization Tips

#### Reuse Generator Instances

Create a single generator instance and reuse it for multiple generations.

```typescript
// ✓ Good - Reuse instance
const generator = new AuthGenerator();

for (const spec of specs) {
  await generator.generateFromFile(spec, options);
}

// ✗ Bad - Create new instance each time
for (const spec of specs) {
  const generator = new AuthGenerator();
  await generator.generateFromFile(spec, options);
}
```

#### Cache Templates

Templates are automatically cached after first load. Avoid recreating generator instances to benefit from caching.

```typescript
// Templates loaded once
const generator = new AuthGenerator();

// Subsequent calls use cached templates
await generator.generateFromFile('spec1.md', options);
await generator.generateFromFile('spec2.md', options);  // Faster
```

#### Batch Generation

Generate multiple specifications in parallel for better throughput.

```typescript
const generator = new AuthGenerator();

const results = await Promise.all(
  specs.map(spec => 
    generator.generateFromFile(spec, {
      outputDir: `./src/auth/${spec.name}`
    })
  )
);

console.log(`Generated ${results.flat().length} files total`);
```

---

## 9. Testing

### 9.1 Unit Testing

Test generator functionality in isolation using mocks and fixtures.

```typescript
import { AuthGenerator } from '@smartspec/auth-generator';
import { describe, it, expect, beforeEach } from '@jest/globals';

describe('AuthGenerator', () => {
  let generator: AuthGenerator;

  beforeEach(() => {
    generator = new AuthGenerator();
  });

  it('should generate files from spec', async () => {
    const files = await generator.generateFromFile(
      './fixtures/test-spec.md',
      { outputDir: './test-output', overwrite: false }
    );

    expect(files).toHaveLength(5);
    expect(files.map(f => f.type)).toContain('controller');
    expect(files.map(f => f.type)).toContain('middleware');
  });

  it('should detect features correctly', async () => {
    const files = await generator.generateFromFile(
      './fixtures/with-email-verification.md',
      { outputDir: './test-output', overwrite: false }
    );

    const controller = files.find(f => f.type === 'controller');
    expect(controller.content).toContain('verifyEmail');
  });
});
```

### 9.2 Integration Testing

Test the complete generation pipeline with real specifications and file system operations.

```typescript
import * as fs from 'fs/promises';
import * as path from 'path';

describe('Integration Tests', () => {
  const testOutputDir = './test-output';

  afterEach(async () => {
    await fs.rm(testOutputDir, { recursive: true, force: true });
  });

  it('should generate and write files', async () => {
    const generator = new AuthGenerator();
    
    await generator.generateFromFile('./specs/auth-spec.md', {
      outputDir: testOutputDir,
      overwrite: true
    });

    // Verify files exist
    const controllerPath = path.join(testOutputDir, 'controllers/auth.controller.ts');
    const exists = await fs.access(controllerPath).then(() => true).catch(() => false);
    
    expect(exists).toBe(true);

    // Verify content
    const content = await fs.readFile(controllerPath, 'utf-8');
    expect(content).toContain('export class AuthController');
  });
});
```

---

## 10. Troubleshooting

### 10.1 Common Issues

**Generation Fails with "Template Not Found"**

Ensure all required template files exist in the template directory. The generator requires five templates: controller, middleware, types, routes, and service.

**Generated Code Has TypeScript Errors**

Check that your specification includes all required fields and that field types are valid TypeScript types. Run the TypeScript compiler on generated code to identify specific errors.

**Files Not Being Written**

Verify that the output directory exists and you have write permissions. Check that `overwrite` option is set to `true` if you want to write files.

**Slow Generation Performance**

Ensure you're reusing generator instances rather than creating new ones for each generation. Check that your disk has sufficient I/O performance.

### 10.2 Debug Mode

Enable verbose logging to diagnose issues.

```typescript
// Set environment variable
process.env.DEBUG = 'auth-generator:*';

// Or use custom logger
const generator = new AuthGenerator();
generator.on('log', (level, message) => {
  console.log(`[${level}] ${message}`);
});
```

### 10.3 Getting Help

If you encounter issues not covered in this documentation:

1. Check the GitHub issues for similar problems
2. Review the example specifications in `examples/auth-specs/`
3. Run the test suite to verify your installation
4. Open a new issue with a minimal reproduction case

---

## 11. Migration Guide

### 11.1 From Manual Auth

If you have existing authentication code and want to migrate to generated code:

1. **Create Specification:** Write a specification that matches your current implementation
2. **Generate Code:** Generate new code from the specification
3. **Compare:** Compare generated code with your existing code
4. **Test:** Ensure all functionality is preserved
5. **Replace:** Gradually replace manual code with generated code
6. **Validate:** Run your test suite to verify everything works

### 11.2 Version Upgrades

When upgrading to a new version of Auth Generator:

1. **Review Changelog:** Check for breaking changes
2. **Update Specs:** Update specifications if format changed
3. **Regenerate:** Regenerate all code with new version
4. **Test:** Run tests to catch any breaking changes
5. **Update Dependencies:** Update related dependencies if needed

---

## 12. Contributing

We welcome contributions to Auth Generator! Here's how to get started.

### 12.1 Development Setup

```bash
# Clone repository
git clone https://github.com/smartspec/auth-generator.git
cd auth-generator

# Install dependencies
pnpm install

# Build
pnpm build

# Run tests
pnpm test

# Run tests in watch mode
pnpm test:watch
```

### 12.2 Adding Features

**Parser Extensions:**

To add new specification features, modify the parser in `src/auth/auth-spec-parser.ts` and update the AST types in `src/types/auth-ast.types.ts`.

**New Templates:**

Add new template files in `templates/auth/` and update the generator to load and render them.

**Custom Helpers:**

Add new Handlebars helpers in `src/generator/handlebars-helpers.ts`.

### 12.3 Testing Guidelines

- Write tests for all new features
- Maintain test coverage above 80%
- Include both unit and integration tests
- Test with multiple specification variations

---

## 13. Appendix

### 13.1 Glossary

**AST (Abstract Syntax Tree):** Structured representation of the parsed specification

**Auth Spec:** Markdown document describing authentication requirements

**Generator:** Tool that transforms specifications into code

**Handlebars:** Template engine used for code generation

**RBAC:** Role-Based Access Control

**Template:** Handlebars file defining code structure

### 13.2 References

- [Handlebars Documentation](https://handlebarsjs.com/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [JWT Best Practices](https://tools.ietf.org/html/rfc8725)
- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)

### 13.3 Changelog

**Version 1.0.0** (December 27, 2025)
- Initial release
- Core generator functionality
- Built-in templates for TypeScript/Express
- 30+ Handlebars helpers
- Comprehensive test suite

---

**End of API Documentation**

For template-specific documentation, see [Template Usage Guide](./TEMPLATE_GUIDE.md).

For quick start examples, see [Quick Start Guide](./QUICK_START.md).
