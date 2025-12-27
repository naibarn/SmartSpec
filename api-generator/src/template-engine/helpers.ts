/**
 * Handlebars Helper Functions
 * Case conversion and utility functions for templates
 */

/**
 * Convert string to PascalCase
 * Example: "user_profile" -> "UserProfile"
 */
export function pascalCase(str: string): string {
  return str
    .replace(/[_-](\w)/g, (_, c) => c.toUpperCase())
    .replace(/^\w/, c => c.toUpperCase())
    .replace(/\s+/g, '');
}

/**
 * Convert string to camelCase
 * Example: "user_profile" -> "userProfile"
 */
export function camelCase(str: string): string {
  return str
    .replace(/[_-](\w)/g, (_, c) => c.toUpperCase())
    .replace(/^\w/, c => c.toLowerCase())
    .replace(/\s+/g, '');
}

/**
 * Convert string to kebab-case
 * Example: "UserProfile" -> "user-profile"
 */
export function kebabCase(str: string): string {
  return str
    .replace(/([a-z])([A-Z])/g, '$1-$2')
    .replace(/[\s_]+/g, '-')
    .toLowerCase();
}

/**
 * Convert string to snake_case
 * Example: "UserProfile" -> "user_profile"
 */
export function snakeCase(str: string): string {
  return str
    .replace(/([a-z])([A-Z])/g, '$1_$2')
    .replace(/[\s-]+/g, '_')
    .toLowerCase();
}

/**
 * Convert string to UPPER_SNAKE_CASE
 * Example: "userProfile" -> "USER_PROFILE"
 */
export function upperSnakeCase(str: string): string {
  return snakeCase(str).toUpperCase();
}

/**
 * Pluralize a word (simple English rules)
 * Example: "todo" -> "todos", "category" -> "categories"
 */
export function pluralize(str: string): string {
  if (str.endsWith('y')) {
    return str.slice(0, -1) + 'ies';
  }
  if (str.endsWith('s') || str.endsWith('x') || str.endsWith('z') || 
      str.endsWith('ch') || str.endsWith('sh')) {
    return str + 'es';
  }
  return str + 's';
}

/**
 * Singularize a word (simple English rules)
 * Example: "todos" -> "todo", "categories" -> "category"
 */
export function singularize(str: string): string {
  if (str.endsWith('ies')) {
    return str.slice(0, -3) + 'y';
  }
  if (str.endsWith('es')) {
    return str.slice(0, -2);
  }
  if (str.endsWith('s')) {
    return str.slice(0, -1);
  }
  return str;
}

/**
 * Convert field type to TypeScript type
 */
export function toTypeScriptType(fieldType: string): string {
  const typeMap: Record<string, string> = {
    'string': 'string',
    'number': 'number',
    'integer': 'number',
    'boolean': 'boolean',
    'datetime': 'Date',
    'date': 'Date',
    'time': 'string',
    'uuid': 'string',
    'json': 'any',
    'array': 'any[]'
  };

  return typeMap[fieldType] || 'any';
}

/**
 * Convert field type to Zod type
 */
export function toZodType(fieldType: string): string {
  const typeMap: Record<string, string> = {
    'string': 'z.string()',
    'number': 'z.number()',
    'integer': 'z.number().int()',
    'boolean': 'z.boolean()',
    'datetime': 'z.date()',
    'date': 'z.date()',
    'time': 'z.string()',
    'uuid': 'z.string().uuid()',
    'json': 'z.any()',
    'array': 'z.array(z.any())'
  };

  return typeMap[fieldType] || 'z.any()';
}

/**
 * Convert HTTP method to lowercase
 */
export function httpMethodLower(method: string): string {
  return method.toLowerCase();
}

/**
 * Check if field is required
 */
export function isRequired(constraints: any[]): boolean {
  return constraints.some(c => c.type === 'required');
}

/**
 * Get default value from constraints
 */
export function getDefault(constraints: any[]): any {
  const defaultConstraint = constraints.find(c => c.type === 'default');
  return defaultConstraint?.value;
}

/**
 * Get max value from constraints
 */
export function getMax(constraints: any[]): number | undefined {
  const maxConstraint = constraints.find(c => c.type === 'max');
  return maxConstraint?.value;
}

/**
 * Get min value from constraints
 */
export function getMin(constraints: any[]): number | undefined {
  const minConstraint = constraints.find(c => c.type === 'min');
  return minConstraint?.value;
}

/**
 * Format JSDoc comment
 */
export function formatJSDoc(text: string, indent: string = ''): string {
  const lines = text.split('\n');
  if (lines.length === 1) {
    return `${indent}/** ${text} */`;
  }
  return [
    `${indent}/**`,
    ...lines.map(line => `${indent} * ${line}`),
    `${indent} */`
  ].join('\n');
}

/**
 * Indent text by specified spaces
 */
export function indent(text: string, spaces: number): string {
  const indentation = ' '.repeat(spaces);
  return text.split('\n').map(line => indentation + line).join('\n');
}

/**
 * Check if value is truthy
 */
export function isTruthy(value: any): boolean {
  return !!value;
}

/**
 * Check if array is not empty
 */
export function isNotEmpty(arr: any[]): boolean {
  return arr && arr.length > 0;
}

/**
 * Join array with separator
 */
export function join(arr: any[], separator: string): string {
  return arr.join(separator);
}

/**
 * Get first element of array
 */
export function first<T>(arr: T[]): T | undefined {
  return arr[0];
}

/**
 * Get last element of array
 */
export function last<T>(arr: T[]): T | undefined {
  return arr[arr.length - 1];
}

/**
 * Check if string includes substring
 */
export function includes(str: string, substring: string): boolean {
  return !!(str && str.includes(substring));
}

/**
 * Conditional helper - block helper
 */
export function ifEquals(this: any, a: any, b: any, options: any): string {
  if (a === b) {
    return options.fn(this);
  } else {
    return options.inverse(this);
  }
}

/**
 * Logical OR
 */
export function or(...args: any[]): boolean {
  // Last argument is Handlebars options object
  const values = args.slice(0, -1);
  return values.some(v => !!v);
}

/**
 * Logical AND
 */
export function and(...args: any[]): boolean {
  // Last argument is Handlebars options object
  const values = args.slice(0, -1);
  return values.every(v => !!v);
}

/**
 * Logical NOT
 */
export function not(value: any): boolean {
  return !value;
}

/**
 * JSON stringify
 */
export function json(obj: any, indent?: number): string {
  return JSON.stringify(obj, null, indent || 2);
}

/**
 * Escape string for use in code
 */
export function escapeString(str: string): string {
  return str
    .replace(/\\/g, '\\\\')
    .replace(/"/g, '\\"')
    .replace(/'/g, "\\'")
    .replace(/\n/g, '\\n')
    .replace(/\r/g, '\\r')
    .replace(/\t/g, '\\t');
}

/**
 * Register all helpers with Handlebars
 */
export function registerHelpers(handlebars: any): void {
  handlebars.registerHelper('pascalCase', pascalCase);
  handlebars.registerHelper('camelCase', camelCase);
  handlebars.registerHelper('kebabCase', kebabCase);
  handlebars.registerHelper('snakeCase', snakeCase);
  handlebars.registerHelper('upperSnakeCase', upperSnakeCase);
  handlebars.registerHelper('pluralize', pluralize);
  handlebars.registerHelper('singularize', singularize);
  handlebars.registerHelper('toTypeScriptType', toTypeScriptType);
  handlebars.registerHelper('toZodType', toZodType);
  handlebars.registerHelper('httpMethodLower', httpMethodLower);
  handlebars.registerHelper('isRequired', isRequired);
  handlebars.registerHelper('getDefault', getDefault);
  handlebars.registerHelper('getMax', getMax);
  handlebars.registerHelper('getMin', getMin);
  handlebars.registerHelper('formatJSDoc', formatJSDoc);
  handlebars.registerHelper('indent', indent);
  handlebars.registerHelper('isTruthy', isTruthy);
  handlebars.registerHelper('isNotEmpty', isNotEmpty);
  handlebars.registerHelper('join', join);
  handlebars.registerHelper('first', first);
  handlebars.registerHelper('last', last);
  handlebars.registerHelper('includes', includes);
  handlebars.registerHelper('ifEquals', ifEquals);
  handlebars.registerHelper('or', or);
  handlebars.registerHelper('and', and);
  handlebars.registerHelper('not', not);
  handlebars.registerHelper('json', json);
  handlebars.registerHelper('escapeString', escapeString);
}
