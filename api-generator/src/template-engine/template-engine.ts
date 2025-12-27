import Handlebars from 'handlebars';
import { readFileSync, readdirSync, statSync } from 'fs';
import { join, extname } from 'path';
import { registerHelpers } from './helpers';
import { APISpec, Entity, Endpoint } from '../types/ast.types';

/**
 * Template context for rendering
 */
export interface TemplateContext {
  spec: APISpec;
  entity?: Entity;
  endpoint?: Endpoint;
  [key: string]: any;
}

/**
 * Generated file
 */
export interface GeneratedFile {
  path: string;
  content: string;
}

/**
 * TemplateEngine
 * Renders code from AST using Handlebars templates
 */
export class TemplateEngine {
  private handlebars: typeof Handlebars;
  private templates: Map<string, HandlebarsTemplateDelegate>;
  private templatesDir: string;

  constructor(templatesDir: string) {
    this.handlebars = Handlebars.create();
    this.templates = new Map();
    this.templatesDir = templatesDir;

    // Register helpers
    registerHelpers(this.handlebars);

    // Load templates
    this.loadTemplates();
  }

  /**
   * Load all templates from templates directory
   */
  private loadTemplates(): void {
    this.loadTemplatesRecursive(this.templatesDir, '');
  }

  /**
   * Recursively load templates from directory
   */
  private loadTemplatesRecursive(dir: string, prefix: string): void {
    const entries = readdirSync(dir);

    for (const entry of entries) {
      const fullPath = join(dir, entry);
      const stat = statSync(fullPath);

      if (stat.isDirectory()) {
        // Recurse into subdirectory
        this.loadTemplatesRecursive(fullPath, prefix ? `${prefix}/${entry}` : entry);
      } else if (extname(entry) === '.hbs') {
        // Load template file
        const templateName = prefix ? `${prefix}/${entry}` : entry;
        const templateContent = readFileSync(fullPath, 'utf-8');
        const template = this.handlebars.compile(templateContent);
        this.templates.set(templateName, template);
      }
    }
  }

  /**
   * Render a template with context
   */
  render(templateName: string, context: TemplateContext): string {
    const template = this.templates.get(templateName);
    if (!template) {
      throw new Error(`Template not found: ${templateName}`);
    }

    return template(context);
  }

  /**
   * Generate all files for an API spec
   */
  generateAll(spec: APISpec): GeneratedFile[] {
    const files: GeneratedFile[] = [];

    // Generate files for each entity
    for (const entity of spec.entities) {
      files.push(...this.generateEntityFiles(spec, entity));
    }

    // Generate files for each endpoint
    // Endpoints are grouped by entity, so we skip individual endpoint files
    // They're included in the route files

    // Generate common files
    files.push(...this.generateCommonFiles(spec));

    return files;
  }

  /**
   * Generate files for an entity
   */
  private generateEntityFiles(spec: APISpec, entity: Entity): GeneratedFile[] {
    const files: GeneratedFile[] = [];
    const context: TemplateContext = { spec, entity };

    // Controller
    if (this.templates.has('api/controllers/entity.controller.ts.hbs')) {
      files.push({
        path: `src/controllers/${this.toKebabCase(entity.name)}.controller.ts`,
        content: this.render('api/controllers/entity.controller.ts.hbs', context)
      });
    }

    // Service
    if (this.templates.has('api/services/entity.service.ts.hbs')) {
      files.push({
        path: `src/services/${this.toKebabCase(entity.name)}.service.ts`,
        content: this.render('api/services/entity.service.ts.hbs', context)
      });
    }

    // Model
    if (this.templates.has('api/models/entity.model.ts.hbs')) {
      files.push({
        path: `src/models/${this.toKebabCase(entity.name)}.model.ts`,
        content: this.render('api/models/entity.model.ts.hbs', context)
      });
    }

    // Validator
    if (this.templates.has('api/validators/entity.validator.ts.hbs')) {
      files.push({
        path: `src/validators/${this.toKebabCase(entity.name)}.validator.ts`,
        content: this.render('api/validators/entity.validator.ts.hbs', context)
      });
    }

    // Types
    if (this.templates.has('api/types/entity.types.ts.hbs')) {
      files.push({
        path: `src/types/${this.toKebabCase(entity.name)}.types.ts`,
        content: this.render('api/types/entity.types.ts.hbs', context)
      });
    }

    // Routes
    if (this.templates.has('api/routes/entity.routes.ts.hbs')) {
      // Find endpoints for this entity
      const entityEndpoints = spec.endpoints.filter(e => 
        e.path.includes(`/${this.toKebabCase(entity.name)}`)
      );
      files.push({
        path: `src/routes/${this.toKebabCase(entity.name)}.routes.ts`,
        content: this.render('api/routes/entity.routes.ts.hbs', {
          spec,
          entity,
          endpoints: entityEndpoints
        })
      });
    }

    // Tests
    if (this.templates.has('api/tests/entity.test.ts.hbs')) {
      files.push({
        path: `tests/${this.toKebabCase(entity.name)}.test.ts`,
        content: this.render('api/tests/entity.test.ts.hbs', context)
      });
    }

    return files;
  }

  /**
   * Generate common files (index, config, etc.)
   */
  private generateCommonFiles(spec: APISpec): GeneratedFile[] {
    const files: GeneratedFile[] = [];
    const context: TemplateContext = { spec };

    // Main index
    if (this.templates.has('api/index.ts.hbs')) {
      files.push({
        path: 'src/index.ts',
        content: this.render('api/index.ts.hbs', context)
      });
    }

    // Package.json
    if (this.templates.has('api/package.json.hbs')) {
      files.push({
        path: 'package.json',
        content: this.render('api/package.json.hbs', context)
      });
    }

    // README
    if (this.templates.has('api/README.md.hbs')) {
      files.push({
        path: 'README.md',
        content: this.render('api/README.md.hbs', context)
      });
    }

    // .env.example
    if (this.templates.has('api/.env.example.hbs')) {
      files.push({
        path: '.env.example',
        content: this.render('api/.env.example.hbs', context)
      });
    }

    return files;
  }

  /**
   * Get list of available templates
   */
  getTemplateNames(): string[] {
    return Array.from(this.templates.keys());
  }

  /**
   * Check if template exists
   */
  hasTemplate(templateName: string): boolean {
    return this.templates.has(templateName);
  }

  /**
   * Helper: Convert to kebab-case
   */
  private toKebabCase(str: string): string {
    return str
      .replace(/([a-z])([A-Z])/g, '$1-$2')
      .replace(/[\s_]+/g, '-')
      .toLowerCase();
  }

  /**
   * Register a custom helper
   */
  registerHelper(name: string, fn: Handlebars.HelperDelegate): void {
    this.handlebars.registerHelper(name, fn);
  }

  /**
   * Register a partial template
   */
  registerPartial(name: string, template: string): void {
    this.handlebars.registerPartial(name, template);
  }
}
