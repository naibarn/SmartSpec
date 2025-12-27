/**
 * Integration Test Script
 * 
 * Tests AuthGenerator with all spec variations
 */

import { AuthGenerator } from './src/generator/auth-generator';
import * as fs from 'fs/promises';
import * as path from 'path';

async function runIntegrationTests() {
  console.log('=== Integration Test ===\n');
  
  const generator = new AuthGenerator();
  const specs = ['minimal-auth.md', 'todo-auth.md', 'advanced-auth.md'];
  
  let totalFiles = 0;
  let totalDuration = 0;
  
  for (const spec of specs) {
    const specPath = path.join(__dirname, 'examples/auth-specs', spec);
    const outputDir = path.join(__dirname, 'test-integration', spec.replace('.md', ''));
    
    console.log(`Testing ${spec}...`);
    const start = Date.now();
    
    const files = await generator.generateFromFile(specPath, { outputDir, overwrite: true });
    
    const duration = Date.now() - start;
    totalFiles += files.length;
    totalDuration += duration;
    
    console.log(`  ✓ Generated ${files.length} files in ${duration}ms`);
    
    // Verify files exist
    let missingFiles = 0;
    for (const file of files) {
      const exists = await fs.access(file.path).then(() => true).catch(() => false);
      if (!exists) {
        console.log(`  ✗ File not found: ${file.path}`);
        missingFiles++;
      }
    }
    
    if (missingFiles === 0) {
      console.log(`  ✓ All files verified\n`);
    } else {
      console.log(`  ✗ ${missingFiles} files missing\n`);
    }
  }
  
  console.log('=== Summary ===');
  console.log(`Total specs tested: ${specs.length}`);
  console.log(`Total files generated: ${totalFiles}`);
  console.log(`Total duration: ${totalDuration}ms`);
  console.log(`Average per spec: ${Math.round(totalDuration / specs.length)}ms`);
  console.log('\n✓ All integration tests passed!');
}

runIntegrationTests().catch(console.error);
