/**
 * Auth Generator
 * 
 * Generates authentication code from auth spec
 */

import * as fs from 'fs/promises';
import * as path from 'path';
import Handlebars from 'handlebars';
import { AuthSpecParser } from '../auth/auth-spec-parser';
import { AuthSpec } from '../types/auth-ast.types';
import { registerHandlebarsHelpers } from './handlebars-helpers';

export interface GeneratorOptions {
  outputDir: string;
  templateDir?: string;
  overwrite?: boolean;
}

export interface GeneratedFile {
  path: string;
  content: string;
  type: 'controller' | 'service' | 'middleware' | 'types' | 'routes';
}

export class AuthGenerator {
  private parser: AuthSpecParser;
  private templateDir: string;
  private templates: Map<string, HandlebarsTemplateDelegate> = new Map();

  constructor(options?: { templateDir?: string }) {
    this.parser = new AuthSpecParser();
    this.templateDir = options?.templateDir || path.join(__dirname, '../../templates/auth');
  }

  /**
   * Generate auth code from spec file
   */
  async generateFromFile(specPath: string, options: GeneratorOptions): Promise<GeneratedFile[]> {
    // Read spec file
    const specContent = await fs.readFile(specPath, 'utf-8');

    // Parse spec
    const ast = this.parser.parse(specContent);

    // Generate code
    return this.generate(ast, options);
  }

  /**
   * Generate auth code from spec content
   */
  async generateFromContent(specContent: string, options: GeneratorOptions): Promise<GeneratedFile[]> {
    // Parse spec
    const ast = this.parser.parse(specContent);

    // Generate code
    return this.generate(ast, options);
  }

  /**
   * Generate auth code from AST
   */
  async generate(ast: AuthSpec, options: GeneratorOptions): Promise<GeneratedFile[]> {
    // Load templates
    await this.loadTemplates();

    // Register Handlebars helpers
    this.registerHelpers();

    // Prepare template context
    const context = this.prepareContext(ast);

    // Generate files
    const files: GeneratedFile[] = [];

    // Generate controller
    files.push({
      path: path.join(options.outputDir, 'controllers/auth.controller.ts'),
      content: this.renderTemplate('controller', context),
      type: 'controller',
    });

    // Generate middleware
    files.push({
      path: path.join(options.outputDir, 'middleware/auth.middleware.ts'),
      content: this.renderTemplate('middleware', context),
      type: 'middleware',
    });

    // Generate types
    files.push({
      path: path.join(options.outputDir, 'types/auth.types.ts'),
      content: this.renderTemplate('types', context),
      type: 'types',
    });

    // Generate routes
    files.push({
      path: path.join(options.outputDir, 'routes/auth.routes.ts'),
      content: this.renderTemplate('routes', context),
      type: 'routes',
    });

    // Generate service (template reference only)
    files.push({
      path: path.join(options.outputDir, 'services/auth.service.ts'),
      content: this.renderTemplate('service', context),
      type: 'service',
    });

    // Write files to disk if requested
    if (options.overwrite !== false) {
      await this.writeFiles(files);
    }

    return files;
  }

  /**
   * Load Handlebars templates
   */
  private async loadTemplates(): Promise<void> {
    const templateFiles = {
      controller: 'controllers/auth.controller.ts.hbs',
      middleware: 'middleware/auth.middleware.ts.hbs',
      types: 'types/auth.types.ts.hbs',
      routes: 'routes/auth.routes.ts.hbs',
      service: 'services/auth.service.ts.hbs',
    };

    for (const [name, file] of Object.entries(templateFiles)) {
      const templatePath = path.join(this.templateDir, file);
      const templateContent = await fs.readFile(templatePath, 'utf-8');
      const template = Handlebars.compile(templateContent);
      this.templates.set(name, template);
    }
  }

  /**
   * Register Handlebars helpers
   */
  private registerHelpers(): void {
    registerHandlebarsHelpers();
  }

  /**
   * Prepare template context from AST
   */
  private prepareContext(ast: AuthSpec): any {
    // Extract features
    const features = {
      emailVerification: ast.features.emailVerification || false,
      passwordReset: ast.features.passwordReset || false,
      accountLockout: ast.securitySettings.accountSecurity ? true : false,
    };

    // Extract RBAC config from user model
    const hasRoleField = ast.userModel.fields.some(f => f.name === 'role' && f.type === 'enum');
    const roleField = ast.userModel.fields.find(f => f.name === 'role');
    const rbac = hasRoleField && roleField ? {
      enabled: true,
      roles: roleField.enumValues?.map(role => ({ name: role })) || [],
      defaultRole: roleField.enumValues?.[0] || 'user',
    } : {
      enabled: false,
      roles: [],
      defaultRole: 'user',
    };

    // Extract JWT settings
    const jwtSettings = {
      algorithm: ast.tokenConfig?.algorithm || 'RS256',
      accessTokenExpiry: ast.tokenConfig?.accessToken?.expiresIn || '15m',
      refreshTokenExpiry: ast.tokenConfig?.refreshToken?.expiresIn || '7d',
      issuer: 'smartspec-app',
      audience: 'smartspec-users',
    };

    // Extract security settings
    const securitySettings = {
      passwordRequirements: {
        minLength: ast.securitySettings.passwordRequirements?.minLength || 8,
        requireUppercase: ast.securitySettings.passwordRequirements?.requireUppercase ?? true,
        requireLowercase: ast.securitySettings.passwordRequirements?.requireLowercase ?? true,
        requireNumbers: ast.securitySettings.passwordRequirements?.requireNumber ?? true,
        requireSpecialChars: ast.securitySettings.passwordRequirements?.requireSpecial ?? false,
        saltRounds: 10,
      },
      accountLockout: {
        maxAttempts: ast.securitySettings.accountSecurity?.maxLoginAttempts || 5,
        lockoutDuration: this.parseDuration(ast.securitySettings.accountSecurity?.lockoutDuration) || 30,
      },
    };

    // Extract user model
    const userModel = {
      fields: ast.userModel.fields || [],
    };

    // Fields to exclude from user model (handled separately or auto-generated)
    const excludedFields = [
      'id', 'email', 'password', 'role', 
      'emailVerified', 'emailVerificationToken', 'emailVerificationExpires',
      'failedLoginAttempts', 'lockedUntil',
      'resetPasswordToken', 'resetPasswordExpires',
      'createdAt', 'updatedAt'
    ];

    return {
      features,
      rbac,
      jwtSettings,
      securitySettings,
      userModel,
      excludedFields,
    };
  }

  /**
   * Render template with context
   */
  private renderTemplate(name: string, context: any): string {
    const template = this.templates.get(name);
    if (!template) {
      throw new Error(`Template not found: ${name}`);
    }

    return template(context);
  }

  /**
   * Write generated files to disk
   */
  private async writeFiles(files: GeneratedFile[]): Promise<void> {
    for (const file of files) {
      // Create directory if it doesn't exist
      const dir = path.dirname(file.path);
      await fs.mkdir(dir, { recursive: true });

      // Write file
      await fs.writeFile(file.path, file.content, 'utf-8');
    }
  }

  /**
   * Parse duration string to minutes
   */
  private parseDuration(duration?: string): number {
    if (!duration) return 30;
    
    const match = duration.match(/(\d+)(m|h|d)/);
    if (!match) return 30;
    
    const value = parseInt(match[1]);
    const unit = match[2];
    
    switch (unit) {
      case 'm': return value;
      case 'h': return value * 60;
      case 'd': return value * 60 * 24;
      default: return 30;
    }
  }

  /**
   * Get parser instance (for testing)
   */
  getParser(): AuthSpecParser {
    return this.parser;
  }

  /**
   * Validate spec without generating code
   */
  async validateSpec(specPath: string): Promise<{ valid: boolean; errors: string[] }> {
    try {
      const specContent = await fs.readFile(specPath, 'utf-8');
      const ast = this.parser.parse(specContent);
      
      // Basic validation
      const errors: string[] = [];

      if (!ast.userModel) {
        errors.push('User model is required');
      }

      if (!ast.tokenConfig) {
        errors.push('Token configuration is required');
      }

      if (!ast.securitySettings) {
        errors.push('Security settings are required');
      }

      return {
        valid: errors.length === 0,
        errors,
      };
    } catch (error) {
      return {
        valid: false,
        errors: [error instanceof Error ? error.message : 'Unknown error'],
      };
    }
  }
}
