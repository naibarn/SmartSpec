#!/usr/bin/env node

import { Command } from 'commander';
import { readFileSync, writeFileSync, mkdirSync } from 'fs';
import { join, dirname } from 'path';
import { SpecParser } from './parser/spec-parser';
import { TemplateEngine } from './template-engine/template-engine';

const program = new Command();

program
  .name('api-generator')
  .description('Generate API code from markdown specification')
  .version('1.0.0');

program
  .command('generate')
  .description('Generate API code from spec file')
  .argument('<spec-file>', 'Path to markdown spec file')
  .option('-o, --output <dir>', 'Output directory', './output')
  .option('-t, --templates <dir>', 'Templates directory', join(__dirname, '../templates'))
  .action(async (specFile: string, options: { output: string; templates: string }) => {
    try {
      console.log('🚀 Starting API generation...\n');

      // Read spec file
      console.log(`📄 Reading spec: ${specFile}`);
      const markdown = readFileSync(specFile, 'utf-8');

      // Parse spec
      console.log('🔍 Parsing specification...');
      const parser = new SpecParser();
      const ast = await parser.parse(markdown);
      console.log(`✅ Parsed: ${ast.entities.length} entities, ${ast.endpoints.length} endpoints\n`);

      // Initialize template engine
      console.log(`📝 Loading templates from: ${options.templates}`);
      const engine = new TemplateEngine(options.templates);
      console.log(`✅ Loaded ${engine.getTemplateNames().length} templates\n`);

      // Generate files
      console.log('⚙️  Generating code...');
      const files = engine.generateAll(ast);
      console.log(`✅ Generated ${files.length} files\n`);

      // Write files
      console.log(`💾 Writing files to: ${options.output}`);
      for (const file of files) {
        const fullPath = join(options.output, file.path);
        const dir = dirname(fullPath);
        
        // Create directory if it doesn't exist
        mkdirSync(dir, { recursive: true });
        
        // Write file
        writeFileSync(fullPath, file.content, 'utf-8');
        console.log(`  ✓ ${file.path}`);
      }

      console.log('\n🎉 Generation complete!');
      console.log(`\n📁 Output directory: ${options.output}`);
      console.log(`📊 Files generated: ${files.length}`);
      
    } catch (error) {
      console.error('\n❌ Error:', error instanceof Error ? error.message : error);
      process.exit(1);
    }
  });

program
  .command('parse')
  .description('Parse spec file and show AST')
  .argument('<spec-file>', 'Path to markdown spec file')
  .option('-o, --output <file>', 'Output JSON file')
  .action(async (specFile: string, options: { output?: string }) => {
    try {
      console.log('🔍 Parsing specification...\n');

      // Read spec file
      const markdown = readFileSync(specFile, 'utf-8');

      // Parse spec
      const parser = new SpecParser();
      const ast = await parser.parse(markdown);

      // Output
      const json = JSON.stringify(ast, null, 2);
      
      if (options.output) {
        writeFileSync(options.output, json, 'utf-8');
        console.log(`✅ AST written to: ${options.output}`);
      } else {
        console.log(json);
      }

      console.log(`\n📊 Summary:`);
      console.log(`  Name: ${ast.name}`);
      console.log(`  Entities: ${ast.entities.length}`);
      console.log(`  Endpoints: ${ast.endpoints.length}`);
      console.log(`  Business Rules: ${ast.businessRules.length}`);
      
    } catch (error) {
      console.error('\n❌ Error:', error instanceof Error ? error.message : error);
      process.exit(1);
    }
  });

program
  .command('templates')
  .description('List available templates')
  .option('-t, --templates <dir>', 'Templates directory', join(__dirname, '../templates'))
  .action((options: { templates: string }) => {
    try {
      const engine = new TemplateEngine(options.templates);
      const templates = engine.getTemplateNames();

      console.log(`📝 Available templates (${templates.length}):\n`);
      for (const template of templates.sort()) {
        console.log(`  • ${template}`);
      }
      
    } catch (error) {
      console.error('\n❌ Error:', error instanceof Error ? error.message : error);
      process.exit(1);
    }
  });

program.parse();
