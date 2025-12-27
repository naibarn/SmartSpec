/**
 * Test script for Auth Generator
 * 
 * Tests code generation from auth spec
 */

import * as path from 'path';
import { AuthGenerator } from './auth-generator';

async function main() {
  console.log('🚀 Testing Auth Generator...\n');

  // Initialize generator
  const generator = new AuthGenerator();

  // Test spec path
  const specPath = path.join(__dirname, '../../examples/auth-specs/todo-auth.md');
  const outputDir = path.join(__dirname, '../../generated/todo-app');

  console.log(`📄 Spec: ${specPath}`);
  console.log(`📁 Output: ${outputDir}\n`);

  try {
    // Validate spec first
    console.log('1️⃣ Validating spec...');
    const validation = await generator.validateSpec(specPath);
    
    if (!validation.valid) {
      console.error('❌ Validation failed:');
      validation.errors.forEach(err => console.error(`   - ${err}`));
      process.exit(1);
    }
    
    console.log('✅ Spec is valid\n');

    // Generate code
    console.log('2️⃣ Generating code...');
    const startTime = Date.now();
    
    const files = await generator.generateFromFile(specPath, {
      outputDir,
      overwrite: true,
    });
    
    const duration = Date.now() - startTime;
    
    console.log(`✅ Generated ${files.length} files in ${duration}ms\n`);

    // Show generated files
    console.log('📝 Generated files:');
    files.forEach(file => {
      const relativePath = path.relative(outputDir, file.path);
      const lines = file.content.split('\n').length;
      console.log(`   - ${relativePath} (${lines} lines, ${file.type})`);
    });

    console.log('\n✨ Generation complete!');
    console.log(`\n💡 View generated files at: ${outputDir}`);

  } catch (error) {
    console.error('\n❌ Generation failed:');
    console.error(error);
    process.exit(1);
  }
}

// Run test
main().catch(console.error);
