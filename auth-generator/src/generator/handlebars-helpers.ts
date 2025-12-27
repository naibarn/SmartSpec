/**
 * Handlebars Helpers
 * 
 * Custom helpers for code generation templates
 */

import Handlebars from 'handlebars';

/**
 * Register all custom Handlebars helpers
 */
export function registerHandlebarsHelpers(): void {
  // String manipulation helpers
  
  /**
   * Convert string to uppercase
   * Usage: {{uppercase "hello"}} => "HELLO"
   */
  Handlebars.registerHelper('uppercase', (str: string) => {
    return str ? str.toUpperCase() : '';
  });

  /**
   * Convert string to lowercase
   * Usage: {{lowercase "HELLO"}} => "hello"
   */
  Handlebars.registerHelper('lowercase', (str: string) => {
    return str ? str.toLowerCase() : '';
  });

  /**
   * Capitalize first letter
   * Usage: {{capitalize "hello"}} => "Hello"
   */
  Handlebars.registerHelper('capitalize', (str: string) => {
    return str ? str.charAt(0).toUpperCase() + str.slice(1) : '';
  });

  /**
   * Convert to camelCase
   * Usage: {{camelCase "hello_world"}} => "helloWorld"
   */
  Handlebars.registerHelper('camelCase', (str: string) => {
    if (!str) return '';
    return str.replace(/[-_](.)/g, (_, char) => char.toUpperCase());
  });

  /**
   * Convert to PascalCase
   * Usage: {{pascalCase "hello_world"}} => "HelloWorld"
   */
  Handlebars.registerHelper('pascalCase', (str: string) => {
    if (!str) return '';
    const camelCased = str.replace(/[-_](.)/g, (_, char) => char.toUpperCase());
    return camelCased.charAt(0).toUpperCase() + camelCased.slice(1);
  });

  /**
   * Convert to snake_case
   * Usage: {{snakeCase "helloWorld"}} => "hello_world"
   */
  Handlebars.registerHelper('snakeCase', (str: string) => {
    if (!str) return '';
    return str.replace(/([A-Z])/g, '_$1').toLowerCase().replace(/^_/, '');
  });

  /**
   * Convert to kebab-case
   * Usage: {{kebabCase "helloWorld"}} => "hello-world"
   */
  Handlebars.registerHelper('kebabCase', (str: string) => {
    if (!str) return '';
    return str.replace(/([A-Z])/g, '-$1').toLowerCase().replace(/^-/, '');
  });

  // Array/Collection helpers

  /**
   * Check if array includes value
   * Usage: {{#if (includes array "value")}}...{{/if}}
   */
  Handlebars.registerHelper('includes', (array: any[], value: any) => {
    return Array.isArray(array) && array.includes(value);
  });

  /**
   * Get array length
   * Usage: {{length array}}
   */
  Handlebars.registerHelper('length', (array: any[]) => {
    return Array.isArray(array) ? array.length : 0;
  });

  /**
   * Join array with separator
   * Usage: {{join array ", "}}
   */
  Handlebars.registerHelper('join', (array: any[], separator: string) => {
    return Array.isArray(array) ? array.join(separator) : '';
  });

  /**
   * Get first element of array
   * Usage: {{first array}}
   */
  Handlebars.registerHelper('first', (array: any[]) => {
    return Array.isArray(array) && array.length > 0 ? array[0] : null;
  });

  /**
   * Get last element of array
   * Usage: {{last array}}
   */
  Handlebars.registerHelper('last', (array: any[]) => {
    return Array.isArray(array) && array.length > 0 ? array[array.length - 1] : null;
  });

  // Comparison helpers

  /**
   * Check if two values are equal
   * Usage: {{#if (eq a b)}}...{{/if}}
   */
  Handlebars.registerHelper('eq', (a: any, b: any) => {
    return a === b;
  });

  /**
   * Check if two values are not equal
   * Usage: {{#if (neq a b)}}...{{/if}}
   */
  Handlebars.registerHelper('neq', (a: any, b: any) => {
    return a !== b;
  });

  /**
   * Check if a is greater than b
   * Usage: {{#if (gt a b)}}...{{/if}}
   */
  Handlebars.registerHelper('gt', (a: number, b: number) => {
    return a > b;
  });

  /**
   * Check if a is less than b
   * Usage: {{#if (lt a b)}}...{{/if}}
   */
  Handlebars.registerHelper('lt', (a: number, b: number) => {
    return a < b;
  });

  /**
   * Check if a is greater than or equal to b
   * Usage: {{#if (gte a b)}}...{{/if}}
   */
  Handlebars.registerHelper('gte', (a: number, b: number) => {
    return a >= b;
  });

  /**
   * Check if a is less than or equal to b
   * Usage: {{#if (lte a b)}}...{{/if}}
   */
  Handlebars.registerHelper('lte', (a: number, b: number) => {
    return a <= b;
  });

  /**
   * Conditional equality check (legacy)
   * Usage: {{#if (ifEquals a b)}}...{{/if}}
   */
  Handlebars.registerHelper('ifEquals', function(this: any, arg1: any, arg2: any, options: any) {
    return arg1 === arg2 ? (options.fn ? options.fn(this) : true) : (options.inverse ? options.inverse(this) : false);
  });

  // Logical helpers

  /**
   * Logical AND
   * Usage: {{#if (and a b)}}...{{/if}}
   */
  Handlebars.registerHelper('and', (...args: any[]) => {
    // Remove options object (last argument)
    const values = args.slice(0, -1);
    return values.every(v => !!v);
  });

  /**
   * Logical OR
   * Usage: {{#if (or a b)}}...{{/if}}
   */
  Handlebars.registerHelper('or', (...args: any[]) => {
    // Remove options object (last argument)
    const values = args.slice(0, -1);
    return values.some(v => !!v);
  });

  /**
   * Logical NOT
   * Usage: {{#if (not a)}}...{{/if}}
   */
  Handlebars.registerHelper('not', (value: any) => {
    return !value;
  });

  // Utility helpers

  /**
   * Stringify object to JSON
   * Usage: {{json object}}
   */
  Handlebars.registerHelper('json', (obj: any) => {
    return JSON.stringify(obj, null, 2);
  });

  /**
   * Add two numbers
   * Usage: {{add a b}}
   */
  Handlebars.registerHelper('add', (a: number, b: number) => {
    return a + b;
  });

  /**
   * Subtract two numbers
   * Usage: {{subtract a b}}
   */
  Handlebars.registerHelper('subtract', (a: number, b: number) => {
    return a - b;
  });

  /**
   * Multiply two numbers
   * Usage: {{multiply a b}}
   */
  Handlebars.registerHelper('multiply', (a: number, b: number) => {
    return a * b;
  });

  /**
   * Divide two numbers
   * Usage: {{divide a b}}
   */
  Handlebars.registerHelper('divide', (a: number, b: number) => {
    return b !== 0 ? a / b : 0;
  });

  /**
   * Get current timestamp
   * Usage: {{timestamp}}
   */
  Handlebars.registerHelper('timestamp', () => {
    return new Date().toISOString();
  });

  /**
   * Format date
   * Usage: {{formatDate date "YYYY-MM-DD"}}
   */
  Handlebars.registerHelper('formatDate', (date: Date | string, _format: string) => {
    const d = typeof date === 'string' ? new Date(date) : date;
    // Simple format implementation
    return d.toISOString().split('T')[0];
  });

  /**
   * Default value if undefined/null
   * Usage: {{default value "default"}}
   */
  Handlebars.registerHelper('default', (value: any, defaultValue: any) => {
    return value !== undefined && value !== null ? value : defaultValue;
  });

  /**
   * Repeat string n times
   * Usage: {{repeat "x" 3}} => "xxx"
   */
  Handlebars.registerHelper('repeat', (str: string, count: number) => {
    return str.repeat(count);
  });

  /**
   * Truncate string to max length
   * Usage: {{truncate "hello world" 5}} => "hello..."
   */
  Handlebars.registerHelper('truncate', (str: string, maxLength: number) => {
    if (!str || str.length <= maxLength) return str;
    return str.substring(0, maxLength) + '...';
  });

  /**
   * Replace string
   * Usage: {{replace "hello world" "world" "there"}} => "hello there"
   */
  Handlebars.registerHelper('replace', (str: string, search: string, replacement: string) => {
    return str ? str.replace(new RegExp(search, 'g'), replacement) : '';
  });
}
