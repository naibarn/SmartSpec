import { TemplateEngine } from '../../src/template-engine/template-engine';
import { SpecParser } from '../../src/parser/spec-parser';
import { readFileSync } from 'fs';
import { join } from 'path';

describe('TemplateEngine', () => {
  let engine: TemplateEngine;
  let parser: SpecParser;
  let todoSpec: string;

  beforeAll(() => {
    const templatesDir = join(__dirname, '../../templates');
    engine = new TemplateEngine(templatesDir);
    parser = new SpecParser();
    todoSpec = readFileSync(join(__dirname, '../../examples/api-specs/todo.md'), 'utf-8');
  });

  describe('initialization', () => {
    it('should load templates', () => {
      const templates = engine.getTemplateNames();
      expect(templates.length).toBeGreaterThan(0);
    });

    it('should have controller template', () => {
      expect(engine.hasTemplate('api/controllers/entity.controller.ts.hbs')).toBe(true);
    });

    it('should have service template', () => {
      expect(engine.hasTemplate('api/services/entity.service.ts.hbs')).toBe(true);
    });

    it('should have model template', () => {
      expect(engine.hasTemplate('api/models/entity.model.ts.hbs')).toBe(true);
    });

    it('should have validator template', () => {
      expect(engine.hasTemplate('api/validators/entity.validator.ts.hbs')).toBe(true);
    });
  });

  describe('generateAll', () => {
    it('should generate all files for todo spec', async () => {
      const ast = await parser.parse(todoSpec);
      const files = engine.generateAll(ast);

      expect(files.length).toBeGreaterThan(0);
      
      // Should have files for both entities (Todo and User)
      const todoPaths = files.filter(f => f.path.includes('todo'));
      const userPaths = files.filter(f => f.path.includes('user'));
      
      expect(todoPaths.length).toBeGreaterThan(0);
      expect(userPaths.length).toBeGreaterThan(0);
    });

    it('should generate controller files', async () => {
      const ast = await parser.parse(todoSpec);
      const files = engine.generateAll(ast);

      const controllers = files.filter(f => f.path.includes('controllers'));
      expect(controllers.length).toBe(2); // Todo and User
    });

    it('should generate service files', async () => {
      const ast = await parser.parse(todoSpec);
      const files = engine.generateAll(ast);

      const services = files.filter(f => f.path.includes('services'));
      expect(services.length).toBe(2); // Todo and User
    });

    it('should generate model files', async () => {
      const ast = await parser.parse(todoSpec);
      const files = engine.generateAll(ast);

      const models = files.filter(f => f.path.includes('models'));
      expect(models.length).toBe(2); // Todo and User
    });

    it('should generate validator files', async () => {
      const ast = await parser.parse(todoSpec);
      const files = engine.generateAll(ast);

      const validators = files.filter(f => f.path.includes('validators'));
      expect(validators.length).toBe(2); // Todo and User
    });

    it('should generate route files', async () => {
      const ast = await parser.parse(todoSpec);
      const files = engine.generateAll(ast);

      const routes = files.filter(f => f.path.includes('routes'));
      expect(routes.length).toBe(2); // Todo and User
    });
  });

  describe('generated content', () => {
    it('should generate valid TypeScript code', async () => {
      const ast = await parser.parse(todoSpec);
      const files = engine.generateAll(ast);

      for (const file of files) {
        // Check that content is not empty
        expect(file.content.length).toBeGreaterThan(0);
        
        // Check that TypeScript files have proper imports
        if (file.path.endsWith('.ts')) {
          expect(file.content).toContain('import');
        }
      }
    });

    it('should include entity names in generated code', async () => {
      const ast = await parser.parse(todoSpec);
      const files = engine.generateAll(ast);

      const todoController = files.find(f => f.path.includes('todo.controller'));
      expect(todoController).toBeDefined();
      expect(todoController!.content).toContain('TodoController');
      expect(todoController!.content).toContain('TodoService');
    });

    it('should include validation schemas', async () => {
      const ast = await parser.parse(todoSpec);
      const files = engine.generateAll(ast);

      const todoValidator = files.find(f => f.path.includes('todo.validator'));
      expect(todoValidator).toBeDefined();
      expect(todoValidator!.content).toContain('TodoCreateSchema');
      expect(todoValidator!.content).toContain('TodoUpdateSchema');
      expect(todoValidator!.content).toContain('z.string()');
    });

    it('should include field constraints', async () => {
      const ast = await parser.parse(todoSpec);
      const files = engine.generateAll(ast);

      const todoValidator = files.find(f => f.path.includes('todo.validator'));
      expect(todoValidator).toBeDefined();
      // Title has max 200 chars
      expect(todoValidator!.content).toContain('.max(200)');
      // Description has max 1000 chars
      expect(todoValidator!.content).toContain('.max(1000)');
    });

    it('should include CRUD operations', async () => {
      const ast = await parser.parse(todoSpec);
      const files = engine.generateAll(ast);

      const todoController = files.find(f => f.path.includes('todo.controller'));
      expect(todoController).toBeDefined();
      expect(todoController!.content).toContain('getAll');
      expect(todoController!.content).toContain('getById');
      expect(todoController!.content).toContain('create');
      expect(todoController!.content).toContain('update');
      expect(todoController!.content).toContain('delete');
    });

    it('should include authentication checks', async () => {
      const ast = await parser.parse(todoSpec);
      const files = engine.generateAll(ast);

      const todoController = files.find(f => f.path.includes('todo.controller'));
      expect(todoController).toBeDefined();
      expect(todoController!.content).toContain('req.user');
    });
  });

  describe('render', () => {
    it('should render controller template', async () => {
      const ast = await parser.parse(todoSpec);
      const entity = ast.entities[0]; // Todo entity

      const content = engine.render('api/controllers/entity.controller.ts.hbs', {
        spec: ast,
        entity
      });

      expect(content).toContain('TodoController');
      expect(content).toContain('export class');
    });

    it('should render validator template', async () => {
      const ast = await parser.parse(todoSpec);
      const entity = ast.entities[0]; // Todo entity

      const content = engine.render('api/validators/entity.validator.ts.hbs', {
        spec: ast,
        entity
      });

      expect(content).toContain('TodoCreateSchema');
      expect(content).toContain('z.object');
    });
  });
});
