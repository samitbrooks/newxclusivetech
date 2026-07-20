#!/usr/bin/env node
/* Structural sanity check for the most recently generated blog post.
   This is the technical guardrail replacing a "build step" on a plain
   static-HTML site: if this fails, the workflow must not commit/push. */

import fs from 'node:fs';
import path from 'node:path';
import { execSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..');

function getChangedBlogFiles() {
  const output = execSync('git diff --name-only -- blog/*.html', { cwd: ROOT }).toString();
  return output.split('\n').map((s) => s.trim()).filter(Boolean);
}

function countOccurrences(str, sub) {
  return str.split(sub).length - 1;
}

function checkFile(relPath) {
  const fullPath = path.join(ROOT, relPath);
  const content = fs.readFileSync(fullPath, 'utf8');

  const checks = [
    ['has <html>', content.includes('<html')],
    ['has </html>', content.includes('</html>')],
    ['has <title>', content.includes('<title>')],
    ['balanced <div>/</div>', countOccurrences(content, '<div') === countOccurrences(content, '</div>')],
    ['balanced <section>/</section>', countOccurrences(content, '<section') === countOccurrences(content, '</section>')],
    ['has valid JSON-LD', hasValidJsonLd(content)]
  ];

  const failed = checks.filter(([, ok]) => !ok);
  if (failed.length > 0) {
    console.error(`FAILED checks for ${relPath}:`);
    failed.forEach(([name]) => console.error(`  - ${name}`));
    return false;
  }
  console.log(`OK: ${relPath}`);
  return true;
}

function hasValidJsonLd(content) {
  const matches = [...content.matchAll(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/g)];
  if (matches.length === 0) return false;
  return matches.every(([, block]) => {
    try {
      JSON.parse(block);
      return true;
    } catch {
      return false;
    }
  });
}

const files = getChangedBlogFiles();
if (files.length === 0) {
  console.error('No changed blog HTML files found to check. Aborting.');
  process.exit(1);
}

const results = files.map(checkFile);
if (results.some((ok) => !ok)) {
  console.error('One or more sanity checks failed. Nothing will be committed.');
  process.exit(1);
}

console.log('All sanity checks passed.');
