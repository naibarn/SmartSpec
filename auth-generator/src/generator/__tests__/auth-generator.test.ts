/**
 * Auth Generator Tests
 * 
 * Unit tests for AuthGenerator class
 */

import * as fs from 'fs/promises';
import * as path from 'path';
import { AuthGenerator } from '../auth-generator';


describe('AuthGenerator', () => {
  let generator: AuthGenerator;
  const testOutputDir = path.join(__dirname, '../../../test-output');

  beforeEach(() => {
    generator = new AuthGenerator();
  });

  afterEach(async () => {
    // Clean up test output
    try {
      await fs.rm(testOutputDir, { recursive: true, force: true });
    } catch (error) {
      // Ignore errors
    }
  });

  describe('constructor', () => {
    it('should create generator instance', () => {
      expect(generator).toBeInstanceOf(AuthGenerator);
    });

    it('should accept custom template directory', () => {
      const customDir = '/custom/templates';
      const customGenerator = new AuthGenerator({ templateDir: customDir });
      expect(customGenerator).toBeInstanceOf(AuthGenerator);
    });
  });

  describe('validateSpec', () => {
    it('should validate valid spec file', async () => {
      const specPath = path.join(__dirname, '../../../examples/auth-specs/todo-auth.md');
      const result = await generator.validateSpec(specPath);
      
      expect(result.valid).toBe(true);
      expect(result.errors).toHaveLength(0);
    });

    it('should validate spec with all required sections', async () => {
      // Parser is lenient and provides defaults, so validation passes
      // This test verifies that validation works correctly
      const minimalSpec = '# Auth Spec\n\n## User Model\n\n## Features';
      const tempFile = path.join(testOutputDir, 'minimal.md');
      
      await fs.mkdir(testOutputDir, { recursive: true });
      await fs.writeFile(tempFile, minimalSpec);
      
      const result = await generator.validateSpec(tempFile);
      
      // Parser provides defaults, so this should pass
      expect(result.valid).toBe(true);
    });
  });

  describe('generateFromFile', () => {
    it('should generate files from spec file', async () => {
      const specPath = path.join(__dirname, '../../../examples/auth-specs/todo-auth.md');
      const outputDir = path.join(testOutputDir, 'from-file');
      
      const files = await generator.generateFromFile(specPath, {
        outputDir,
        overwrite: true,
      });
      
      expect(files).toHaveLength(5);
      expect(files.map(f => f.type)).toContain('controller');
      expect(files.map(f => f.type)).toContain('middleware');
      expect(files.map(f => f.type)).toContain('types');
      expect(files.map(f => f.type)).toContain('routes');
      expect(files.map(f => f.type)).toContain('service');
      
      // Check files were written
      for (const file of files) {
        const exists = await fs.access(file.path).then(() => true).catch(() => false);
        expect(exists).toBe(true);
      }
    });

    it('should generate files with correct content', async () => {
      const specPath = path.join(__dirname, '../../../examples/auth-specs/todo-auth.md');
      const outputDir = path.join(testOutputDir, 'content-check');
      
      const files = await generator.generateFromFile(specPath, {
        outputDir,
        overwrite: true,
      });
      
      const controllerFile = files.find(f => f.type === 'controller');
      expect(controllerFile).toBeDefined();
      expect(controllerFile!.content).toContain('export class AuthController');
      expect(controllerFile!.content).toContain('async register');
      expect(controllerFile!.content).toContain('async login');
      
      const middlewareFile = files.find(f => f.type === 'middleware');
      expect(middlewareFile).toBeDefined();
      expect(middlewareFile!.content).toContain('export class AuthMiddleware');
      expect(middlewareFile!.content).toContain('authenticate');
      
      const typesFile = files.find(f => f.type === 'types');
      expect(typesFile).toBeDefined();
      expect(typesFile!.content).toContain('export interface User');
      expect(typesFile!.content).toContain('export enum UserRole');
    });
  });

  describe('generateFromContent', () => {
    it('should generate files from spec content string', async () => {
      const specPath = path.join(__dirname, '../../../examples/auth-specs/todo-auth.md');
      const specContent = await fs.readFile(specPath, 'utf-8');
      const outputDir = path.join(testOutputDir, 'from-content');
      
      const files = await generator.generateFromContent(specContent, {
        outputDir,
        overwrite: true,
      });
      
      expect(files).toHaveLength(5);
    });
  });

  describe('generate', () => {
    it('should generate without writing files when overwrite is false', async () => {
      const specPath = path.join(__dirname, '../../../examples/auth-specs/todo-auth.md');
      const specContent = await fs.readFile(specPath, 'utf-8');
      const ast = generator.getParser().parse(specContent);
      const outputDir = path.join(testOutputDir, 'no-write');
      
      const files = await generator.generate(ast, {
        outputDir,
        overwrite: false,
      });
      
      expect(files).toHaveLength(5);
      
      // Check files were NOT written
      for (const file of files) {
        const exists = await fs.access(file.path).then(() => true).catch(() => false);
        expect(exists).toBe(false);
      }
    });
  });

  describe('feature detection', () => {
    it('should detect email verification feature', async () => {
      const specPath = path.join(__dirname, '../../../examples/auth-specs/todo-auth.md');
      const outputDir = path.join(testOutputDir, 'email-verify');
      
      const files = await generator.generateFromFile(specPath, {
        outputDir,
        overwrite: true,
      });
      
      const controllerFile = files.find(f => f.type === 'controller');
      expect(controllerFile!.content).toContain('verifyEmail');
    });

    it('should detect password reset feature', async () => {
      const specPath = path.join(__dirname, '../../../examples/auth-specs/todo-auth.md');
      const outputDir = path.join(testOutputDir, 'password-reset');
      
      const files = await generator.generateFromFile(specPath, {
        outputDir,
        overwrite: true,
      });
      
      const controllerFile = files.find(f => f.type === 'controller');
      expect(controllerFile!.content).toContain('requestPasswordReset');
      expect(controllerFile!.content).toContain('resetPassword');
    });

    it('should detect RBAC feature', async () => {
      const specPath = path.join(__dirname, '../../../examples/auth-specs/todo-auth.md');
      const outputDir = path.join(testOutputDir, 'rbac');
      
      const files = await generator.generateFromFile(specPath, {
        outputDir,
        overwrite: true,
      });
      
      const typesFile = files.find(f => f.type === 'types');
      expect(typesFile!.content).toContain('export enum UserRole');
      expect(typesFile!.content).toContain('USER');
      expect(typesFile!.content).toContain('ADMIN');
      
      const middlewareFile = files.find(f => f.type === 'middleware');
      expect(middlewareFile!.content).toContain('requireRole');
    });
  });

  describe('security settings', () => {
    it('should apply password requirements', async () => {
      const specPath = path.join(__dirname, '../../../examples/auth-specs/todo-auth.md');
      const outputDir = path.join(testOutputDir, 'password-req');
      
      const files = await generator.generateFromFile(specPath, {
        outputDir,
        overwrite: true,
      });
      
      const controllerFile = files.find(f => f.type === 'controller');
      // Should have min length 8
      expect(controllerFile!.content).toContain('.min(8,');
    });

    it('should apply JWT settings', async () => {
      const specPath = path.join(__dirname, '../../../examples/auth-specs/todo-auth.md');
      const outputDir = path.join(testOutputDir, 'jwt-settings');
      
      const files = await generator.generateFromFile(specPath, {
        outputDir,
        overwrite: true,
      });
      
      const typesFile = files.find(f => f.type === 'types');
      expect(typesFile!.content).toContain('RS256');
      expect(typesFile!.content).toContain('15m');
      expect(typesFile!.content).toContain('7d');
    });
  });

  describe('performance', () => {
    it('should generate files in under 1 second', async () => {
      const specPath = path.join(__dirname, '../../../examples/auth-specs/todo-auth.md');
      const outputDir = path.join(testOutputDir, 'performance');
      
      const startTime = Date.now();
      
      await generator.generateFromFile(specPath, {
        outputDir,
        overwrite: true,
      });
      
      const duration = Date.now() - startTime;
      
      expect(duration).toBeLessThan(1000); // Should be under 1 second
    });
  });

  describe('error handling', () => {
    it('should throw error for non-existent spec file', async () => {
      const nonExistentPath = '/non/existent/spec.md';
      const outputDir = path.join(testOutputDir, 'error');
      
      await expect(
        generator.generateFromFile(nonExistentPath, { outputDir })
      ).rejects.toThrow();
    });

    it('should handle invalid template directory', async () => {
      const invalidGenerator = new AuthGenerator({ 
        templateDir: '/non/existent/templates' 
      });
      
      const specPath = path.join(__dirname, '../../../examples/auth-specs/todo-auth.md');
      const outputDir = path.join(testOutputDir, 'invalid-templates');
      
      await expect(
        invalidGenerator.generateFromFile(specPath, { outputDir })
      ).rejects.toThrow();
    });
  });

  describe('file structure', () => {
    it('should create correct directory structure', async () => {
      const specPath = path.join(__dirname, '../../../examples/auth-specs/todo-auth.md');
      const outputDir = path.join(testOutputDir, 'structure');
      
      await generator.generateFromFile(specPath, {
        outputDir,
        overwrite: true,
      });
      
      // Check directories exist
      const controllersDir = path.join(outputDir, 'controllers');
      const middlewareDir = path.join(outputDir, 'middleware');
      const typesDir = path.join(outputDir, 'types');
      const routesDir = path.join(outputDir, 'routes');
      const servicesDir = path.join(outputDir, 'services');
      
      const dirs = [controllersDir, middlewareDir, typesDir, routesDir, servicesDir];
      
      for (const dir of dirs) {
        const exists = await fs.access(dir).then(() => true).catch(() => false);
        expect(exists).toBe(true);
      }
    });
  });
});
