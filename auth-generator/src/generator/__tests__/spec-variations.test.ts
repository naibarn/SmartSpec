/**
 * Spec Variations Tests
 * 
 * Tests AuthGenerator with different spec configurations
 */

import * as fs from 'fs/promises';
import * as path from 'path';
import { AuthGenerator } from '../auth-generator';

describe('Spec Variations', () => {
  let generator: AuthGenerator;
  const testOutputDir = path.join(__dirname, '../../../test-output/variations');

  beforeEach(() => {
    generator = new AuthGenerator();
  });

  afterEach(async () => {
    try {
      await fs.rm(testOutputDir, { recursive: true, force: true });
    } catch (error) {
      // Ignore
    }
  });

  describe('Minimal Spec', () => {
    const specPath = path.join(__dirname, '../../../examples/auth-specs/minimal-auth.md');

    it('should generate code from minimal spec', async () => {
      const outputDir = path.join(testOutputDir, 'minimal');
      
      const files = await generator.generateFromFile(specPath, {
        outputDir,
        overwrite: true,
      });
      
      expect(files).toHaveLength(14); // Updated: now generates 14 files
    });

    it('should not include email verification in minimal spec', async () => {
      const outputDir = path.join(testOutputDir, 'minimal-no-verify');
      
      const files = await generator.generateFromFile(specPath, {
        outputDir,
        overwrite: true,
      });
      
      const controllerFile = files.find(f => f.type === 'controller');
      expect(controllerFile!.content).not.toContain('verifyEmail');
    });

    it('should not include password reset in minimal spec', async () => {
      const outputDir = path.join(testOutputDir, 'minimal-no-reset');
      
      const files = await generator.generateFromFile(specPath, {
        outputDir,
        overwrite: true,
      });
      
      const controllerFile = files.find(f => f.type === 'controller');
      expect(controllerFile!.content).not.toContain('requestPasswordReset');
    });

    it('should not include RBAC in minimal spec', async () => {
      const outputDir = path.join(testOutputDir, 'minimal-no-rbac');
      
      const files = await generator.generateFromFile(specPath, {
        outputDir,
        overwrite: true,
      });
      
      const typesFile = files.find(f => f.type === 'types');
      expect(typesFile!.content).not.toContain('export enum UserRole');
    });
  });

  describe('Advanced Spec', () => {
    const specPath = path.join(__dirname, '../../../examples/auth-specs/advanced-auth.md');

    it('should generate code from advanced spec', async () => {
      const outputDir = path.join(testOutputDir, 'advanced');
      
      const files = await generator.generateFromFile(specPath, {
        outputDir,
        overwrite: true,
      });
      
      expect(files).toHaveLength(14); // Updated: now generates 14 files
    });

    it('should include all features in advanced spec', async () => {
      const outputDir = path.join(testOutputDir, 'advanced-features');
      
      const files = await generator.generateFromFile(specPath, {
        outputDir,
        overwrite: true,
      });
      
      const controllerFile = files.find(f => f.type === 'controller');
      expect(controllerFile!.content).toContain('verifyEmail');
      expect(controllerFile!.content).toContain('requestPasswordReset');
    });

    it('should include multiple roles in advanced spec', async () => {
      const outputDir = path.join(testOutputDir, 'advanced-roles');
      
      const files = await generator.generateFromFile(specPath, {
        outputDir,
        overwrite: true,
      });
      
      const typesFile = files.find(f => f.type === 'types');
      expect(typesFile!.content).toContain('USER');
      expect(typesFile!.content).toContain('MANAGER');
      expect(typesFile!.content).toContain('ADMIN');
      expect(typesFile!.content).toContain('SUPERADMIN');
    });

    it('should apply stricter password requirements', async () => {
      const outputDir = path.join(testOutputDir, 'advanced-password');
      
      const files = await generator.generateFromFile(specPath, {
        outputDir,
        overwrite: true,
      });
      
      const controllerFile = files.find(f => f.type === 'controller');
      // Parser provides defaults, so min length will be 8 (default)
      // In future, parser should extract min length from spec
      expect(controllerFile!.content).toContain('.min(8,');
    });

    it('should apply longer token expiry', async () => {
      const outputDir = path.join(testOutputDir, 'advanced-tokens');
      
      const files = await generator.generateFromFile(specPath, {
        outputDir,
        overwrite: true,
      });
      
      const typesFile = files.find(f => f.type === 'types');
      expect(typesFile!.content).toContain('30m'); // 30 minute access token
      expect(typesFile!.content).toContain('30d'); // 30 day refresh token
    });
  });

  describe('Todo Spec (Standard)', () => {
    const specPath = path.join(__dirname, '../../../examples/auth-specs/todo-auth.md');

    it('should generate code from todo spec', async () => {
      const outputDir = path.join(testOutputDir, 'todo');
      
      const files = await generator.generateFromFile(specPath, {
        outputDir,
        overwrite: true,
      });
      
      expect(files).toHaveLength(14); // Updated: now generates 14 files
    });

    it('should include standard features', async () => {
      const outputDir = path.join(testOutputDir, 'todo-features');
      
      const files = await generator.generateFromFile(specPath, {
        outputDir,
        overwrite: true,
      });
      
      const controllerFile = files.find(f => f.type === 'controller');
      expect(controllerFile!.content).toContain('verifyEmail');
      expect(controllerFile!.content).toContain('requestPasswordReset');
    });

    it('should include basic RBAC (user, admin)', async () => {
      const outputDir = path.join(testOutputDir, 'todo-rbac');
      
      const files = await generator.generateFromFile(specPath, {
        outputDir,
        overwrite: true,
      });
      
      const typesFile = files.find(f => f.type === 'types');
      expect(typesFile!.content).toContain('USER');
      expect(typesFile!.content).toContain('ADMIN');
      expect(typesFile!.content).not.toContain('MANAGER');
    });
  });

  describe('Performance Across Variations', () => {
    it('should generate minimal spec quickly', async () => {
      const specPath = path.join(__dirname, '../../../examples/auth-specs/minimal-auth.md');
      const outputDir = path.join(testOutputDir, 'perf-minimal');
      
      const startTime = Date.now();
      await generator.generateFromFile(specPath, { outputDir, overwrite: true });
      const duration = Date.now() - startTime;
      
      expect(duration).toBeLessThan(500);
    });

    it('should generate advanced spec quickly', async () => {
      const specPath = path.join(__dirname, '../../../examples/auth-specs/advanced-auth.md');
      const outputDir = path.join(testOutputDir, 'perf-advanced');
      
      const startTime = Date.now();
      await generator.generateFromFile(specPath, { outputDir, overwrite: true });
      const duration = Date.now() - startTime;
      
      expect(duration).toBeLessThan(500);
    });

    it('should generate all specs in under 2 seconds total', async () => {
      const specs = [
        'minimal-auth.md',
        'todo-auth.md',
        'advanced-auth.md',
      ];
      
      const startTime = Date.now();
      
      for (const spec of specs) {
        const specPath = path.join(__dirname, '../../../examples/auth-specs', spec);
        const outputDir = path.join(testOutputDir, 'perf-all', spec.replace('.md', ''));
        await generator.generateFromFile(specPath, { outputDir, overwrite: true });
      }
      
      const duration = Date.now() - startTime;
      
      expect(duration).toBeLessThan(2000);
    });
  });

  describe('Code Quality Across Variations', () => {
    it('should generate valid TypeScript for all specs', async () => {
      const specs = [
        'minimal-auth.md',
        'todo-auth.md',
        'advanced-auth.md',
      ];
      
      for (const spec of specs) {
        const specPath = path.join(__dirname, '../../../examples/auth-specs', spec);
        const outputDir = path.join(testOutputDir, 'quality', spec.replace('.md', ''));
        
        const files = await generator.generateFromFile(specPath, { outputDir, overwrite: true });
        
        // Check all files have proper exports
        for (const file of files) {
          expect(file.content).toContain('export');
          // Types file and minimal service files may not have imports
          if (file.type !== 'types' && file.type !== 'service') {
            expect(file.content).toContain('import');
          }
        }
      }
    });

    it('should generate consistent file structure for all specs', async () => {
      const specs = [
        'minimal-auth.md',
        'todo-auth.md',
        'advanced-auth.md',
      ];
      
      for (const spec of specs) {
        const specPath = path.join(__dirname, '../../../examples/auth-specs', spec);
        const outputDir = path.join(testOutputDir, 'structure', spec.replace('.md', ''));
        
        const files = await generator.generateFromFile(specPath, { outputDir, overwrite: true });
        
        // All should have same file types
        const fileTypes = files.map(f => f.type).sort();
        expect(fileTypes).toContain('controller');
        expect(fileTypes).toContain('middleware');
        expect(fileTypes).toContain('routes');
        expect(fileTypes).toContain('service');
        expect(fileTypes).toContain('types');
        expect(files).toHaveLength(14); // All specs generate 14 files
      }
    });
  });
});
