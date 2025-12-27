# Handlebars Helper Reference

**Version:** 1.0.0  
**Last Updated:** December 27, 2025

Complete reference for all Handlebars helpers available in Auth Generator templates.

---

## Quick Reference Table

| Helper | Category | Description | Example |
|--------|----------|-------------|---------|
| `uppercase` | String | Convert to UPPERCASE | `{{uppercase "user"}}` → `USER` |
| `lowercase` | String | Convert to lowercase | `{{lowercase "ADMIN"}}` → `admin` |
| `capitalize` | String | Capitalize first letter | `{{capitalize "user"}}` → `User` |
| `camelCase` | String | Convert to camelCase | `{{camelCase "user_role"}}` → `userRole` |
| `pascalCase` | String | Convert to PascalCase | `{{pascalCase "auth_service"}}` → `AuthService` |
| `snakeCase` | String | Convert to snake_case | `{{snakeCase "userId"}}` → `user_id` |
| `kebabCase` | String | Convert to kebab-case | `{{kebabCase "AuthController"}}` → `auth-controller` |
| `includes` | Array | Check if array includes value | `{{includes roles "admin"}}` |
| `length` | Array | Get array length | `{{length roles}}` |
| `join` | Array | Join array with separator | `{{join permissions ", "}}` |
| `first` | Array | Get first element | `{{first roles}}` |
| `last` | Array | Get last element | `{{last roles}}` |
| `eq` | Comparison | Equal (===) | `{{#if (eq role "admin")}}` |
| `neq` | Comparison | Not equal (!==) | `{{#if (neq status "active")}}` |
| `gt` | Comparison | Greater than (>) | `{{#if (gt count 5)}}` |
| `lt` | Comparison | Less than (<) | `{{#if (lt count 10)}}` |
| `gte` | Comparison | Greater than or equal (>=) | `{{#if (gte count 5)}}` |
| `lte` | Comparison | Less than or equal (<=) | `{{#if (lte count 10)}}` |
| `and` | Logical | Logical AND | `{{#if (and a b)}}` |
| `or` | Logical | Logical OR | `{{#if (or a b)}}` |
| `not` | Logical | Logical NOT | `{{#if (not a)}}` |
| `json` | Utility | Stringify to JSON | `{{json object}}` |
| `add` | Utility | Add numbers | `{{add 5 3}}` → `8` |
| `subtract` | Utility | Subtract numbers | `{{subtract 10 3}}` → `7` |
| `multiply` | Utility | Multiply numbers | `{{multiply 4 3}}` → `12` |
| `divide` | Utility | Divide numbers | `{{divide 10 2}}` → `5` |
| `timestamp` | Utility | Current ISO timestamp | `{{timestamp}}` |
| `formatDate` | Utility | Format date | `{{formatDate date}}` |
| `default` | Utility | Default value if null | `{{default value "fallback"}}` |
| `repeat` | Utility | Repeat string n times | `{{repeat "x" 3}}` → `xxx` |
| `truncate` | Utility | Truncate string | `{{truncate text 50}}` |
| `replace` | Utility | Replace string pattern | `{{replace path "/" "."}}` |

---

## String Helpers

### uppercase

Converts a string to uppercase.

**Signature:** `uppercase(str: string): string`

**Parameters:**
- `str` - String to convert

**Returns:** Uppercase string

**Examples:**

```handlebars
{{uppercase "user"}}
{{! Output: USER }}

export const {{uppercase role}}_PERMISSIONS = [...];
{{! Output: export const ADMIN_PERMISSIONS = [...]; }}

{{#each roles}}
  {{uppercase this.name}} = '{{this.name}}',
{{/each}}
{{! Output:
  USER = 'user',
  ADMIN = 'admin',
}}
```

**Use Cases:**
- Enum values
- Constants
- Environment variables

---

### lowercase

Converts a string to lowercase.

**Signature:** `lowercase(str: string): string`

**Parameters:**
- `str` - String to convert

**Returns:** Lowercase string

**Examples:**

```handlebars
{{lowercase "ADMIN"}}
{{! Output: admin }}

const role = '{{lowercase userRole}}';
{{! Output: const role = 'user'; }}
```

**Use Cases:**
- Normalize input
- Database queries
- Comparisons

---

### capitalize

Capitalizes the first letter of a string.

**Signature:** `capitalize(str: string): string`

**Parameters:**
- `str` - String to capitalize

**Returns:** String with first letter capitalized

**Examples:**

```handlebars
{{capitalize "user"}}
{{! Output: User }}

export class {{capitalize type}}Controller {
{{! Output: export class AuthController { }}

/**
 * {{capitalize description}}
 */
{{! Output: /** User authentication service */ }}
```

**Use Cases:**
- Class names
- Titles
- Documentation

---

### camelCase

Converts a string to camelCase.

**Signature:** `camelCase(str: string): string`

**Parameters:**
- `str` - String to convert (supports snake_case, kebab-case, spaces)

**Returns:** camelCase string

**Examples:**

```handlebars
{{camelCase "user_role"}}
{{! Output: userRole }}

{{camelCase "auth-service"}}
{{! Output: authService }}

const {{camelCase fieldName}} = req.body.{{camelCase fieldName}};
{{! Output: const userId = req.body.userId; }}
```

**Use Cases:**
- Variable names
- Method names
- Property names

---

### pascalCase

Converts a string to PascalCase.

**Signature:** `pascalCase(str: string): string`

**Parameters:**
- `str` - String to convert

**Returns:** PascalCase string

**Examples:**

```handlebars
{{pascalCase "auth_service"}}
{{! Output: AuthService }}

export class {{pascalCase name}} {
{{! Output: export class UserController { }}

import { {{pascalCase serviceName}} } from './services';
{{! Output: import { AuthService } from './services'; }}
```

**Use Cases:**
- Class names
- Interface names
- Type names

---

### snakeCase

Converts a string to snake_case.

**Signature:** `snakeCase(str: string): string`

**Parameters:**
- `str` - String to convert

**Returns:** snake_case string

**Examples:**

```handlebars
{{snakeCase "userId"}}
{{! Output: user_id }}

{{snakeCase "AuthController"}}
{{! Output: auth_controller }}

const {{snakeCase fieldName}} = ...;
{{! Output: const user_role = ...; }}
```

**Use Cases:**
- Database column names
- Environment variables
- API parameters

---

### kebabCase

Converts a string to kebab-case.

**Signature:** `kebabCase(str: string): string`

**Parameters:**
- `str` - String to convert

**Returns:** kebab-case string

**Examples:**

```handlebars
{{kebabCase "AuthController"}}
{{! Output: auth-controller }}

{{kebabCase "userRole"}}
{{! Output: user-role }}

// File: {{kebabCase componentName}}.ts
{{! Output: // File: auth-service.ts }}
```

**Use Cases:**
- File names
- URL paths
- CSS class names

---

## Array Helpers

### includes

Checks if an array includes a specific value.

**Signature:** `includes(array: any[], value: any): boolean`

**Parameters:**
- `array` - Array to search
- `value` - Value to find

**Returns:** `true` if array includes value, `false` otherwise

**Examples:**

```handlebars
{{#if (includes roles "admin")}}
  // Admin role exists
{{/if}}

{{#unless (includes excludedFields fieldName)}}
  {{fieldName}}: {{fieldType}};
{{/unless}}
```

**Use Cases:**
- Conditional rendering
- Feature checks
- Field filtering

---

### length

Returns the number of elements in an array.

**Signature:** `length(array: any[]): number`

**Parameters:**
- `array` - Array to measure

**Returns:** Number of elements

**Examples:**

```handlebars
{{length roles}}
{{! Output: 3 }}

{{#if (gt (length roles) 1)}}
  // Multiple roles
{{/if}}

// Total roles: {{length rbac.roles}}
{{! Output: // Total roles: 4 }}
```

**Use Cases:**
- Conditional logic
- Comments
- Validation

---

### join

Joins array elements with a separator.

**Signature:** `join(array: any[], separator: string): string`

**Parameters:**
- `array` - Array to join
- `separator` - Separator string

**Returns:** Joined string

**Examples:**

```handlebars
{{join permissions ", "}}
{{! Output: read, write, delete }}

const roles = [{{join (map roles "name") ", "}}];
{{! Output: const roles = [user, admin, manager]; }}

// Permissions: {{join permissions " | "}}
{{! Output: // Permissions: read | write | delete }}
```

**Use Cases:**
- Array literals
- Documentation
- Display values

---

### first

Returns the first element of an array.

**Signature:** `first(array: any[]): any`

**Parameters:**
- `array` - Array to access

**Returns:** First element or `null` if empty

**Examples:**

```handlebars
{{first roles}}
{{! Output: user }}

const defaultRole = '{{first rbac.roles.name}}';
{{! Output: const defaultRole = 'user'; }}
```

**Use Cases:**
- Default values
- Fallbacks
- Primary items

---

### last

Returns the last element of an array.

**Signature:** `last(array: any[]): any`

**Parameters:**
- `array` - Array to access

**Returns:** Last element or `null` if empty

**Examples:**

```handlebars
{{last roles}}
{{! Output: superadmin }}

// Highest role: {{last rbac.roles.name}}
{{! Output: // Highest role: superadmin }}
```

**Use Cases:**
- Highest values
- Final items
- Fallbacks

---

## Comparison Helpers

### eq

Checks if two values are equal (strict equality ===).

**Signature:** `eq(a: any, b: any): boolean`

**Parameters:**
- `a` - First value
- `b` - Second value

**Returns:** `true` if equal, `false` otherwise

**Examples:**

```handlebars
{{#if (eq role "admin")}}
  // Admin-specific code
{{/if}}

{{#if (eq algorithm "RS256")}}
  // Use RS256
{{else}}
  // Use other algorithm
{{/if}}
```

**Use Cases:**
- Conditional rendering
- Feature switches
- Value matching

---

### neq

Checks if two values are not equal (strict inequality !==).

**Signature:** `neq(a: any, b: any): boolean`

**Examples:**

```handlebars
{{#if (neq status "active")}}
  // Non-active handling
{{/if}}

{{#unless (neq role "admin")}}
  // Admin only (double negative)
{{/unless}}
```

---

### gt

Checks if first value is greater than second.

**Signature:** `gt(a: number, b: number): boolean`

**Examples:**

```handlebars
{{#if (gt minLength 8)}}
  // Strong password requirement
{{/if}}

{{#if (gt (length roles) 2)}}
  // Multiple roles
{{/if}}
```

**Use Cases:**
- Threshold checks
- Conditional logic
- Validation

---

### lt

Checks if first value is less than second.

**Signature:** `lt(a: number, b: number): boolean`

**Examples:**

```handlebars
{{#if (lt maxAttempts 5)}}
  // Strict lockout policy
{{/if}}
```

---

### gte

Checks if first value is greater than or equal to second.

**Signature:** `gte(a: number, b: number): boolean`

**Examples:**

```handlebars
{{#if (gte minLength 12)}}
  // Very strong password
{{/if}}
```

---

### lte

Checks if first value is less than or equal to second.

**Signature:** `lte(a: number, b: number): boolean`

**Examples:**

```handlebars
{{#if (lte maxAttempts 3)}}
  // Very strict policy
{{/if}}
```

---

## Logical Helpers

### and

Returns `true` if all arguments are truthy.

**Signature:** `and(...values: any[]): boolean`

**Parameters:**
- `...values` - Values to check (last argument is options object)

**Returns:** `true` if all truthy, `false` otherwise

**Examples:**

```handlebars
{{#if (and features.emailVerification features.passwordReset)}}
  // Both features enabled
{{/if}}

{{#if (and rbac.enabled (gt (length rbac.roles) 1))}}
  // RBAC with multiple roles
{{/if}}
```

**Use Cases:**
- Multiple conditions
- Feature combinations
- Complex logic

---

### or

Returns `true` if any argument is truthy.

**Signature:** `or(...values: any[]): boolean`

**Examples:**

```handlebars
{{#if (or features.emailVerification features.passwordReset)}}
  // At least one feature enabled
{{/if}}

{{#if (or (eq role "admin") (eq role "superadmin"))}}
  // High-privilege role
{{/if}}
```

**Use Cases:**
- Alternative conditions
- Fallback logic
- Multiple options

---

### not

Negates a boolean value.

**Signature:** `not(value: any): boolean`

**Examples:**

```handlebars
{{#if (not features.emailVerification)}}
  // Email verification disabled
{{/if}}

{{#if (not rbac.enabled)}}
  // No RBAC
{{/if}}
```

**Use Cases:**
- Inverse conditions
- Disabled features
- Negative checks

---

## Utility Helpers

### json

Stringifies an object to JSON with pretty formatting.

**Signature:** `json(obj: any): string`

**Parameters:**
- `obj` - Object to stringify

**Returns:** JSON string with 2-space indentation

**Examples:**

```handlebars
{{json config}}
{{! Output: {
  "key": "value",
  "nested": {
    "prop": 123
  }
} }}

// Config: {{json AUTH_CONFIG}}
{{! Output: // Config: {"jwt": {...}} }}
```

**Use Cases:**
- Debugging
- Configuration output
- Documentation

---

### add

Adds two numbers.

**Signature:** `add(a: number, b: number): number`

**Examples:**

```handlebars
{{add 5 3}}
{{! Output: 8 }}

const total = {{add maxAttempts bonusAttempts}};
{{! Output: const total = 8; }}
```

---

### subtract

Subtracts second number from first.

**Signature:** `subtract(a: number, b: number): number`

**Examples:**

```handlebars
{{subtract 10 3}}
{{! Output: 7 }}
```

---

### multiply

Multiplies two numbers.

**Signature:** `multiply(a: number, b: number): number`

**Examples:**

```handlebars
{{multiply 4 3}}
{{! Output: 12 }}

const duration = {{multiply lockoutDuration 60}};
{{! Output: const duration = 1800; (30 * 60) }}
```

---

### divide

Divides first number by second.

**Signature:** `divide(a: number, b: number): number`

**Examples:**

```handlebars
{{divide 10 2}}
{{! Output: 5 }}

{{! Safe division - returns 0 if divisor is 0 }}
{{divide 10 0}}
{{! Output: 0 }}
```

---

### timestamp

Returns current ISO timestamp.

**Signature:** `timestamp(): string`

**Returns:** ISO 8601 timestamp string

**Examples:**

```handlebars
// Generated at {{timestamp}}
{{! Output: // Generated at 2025-12-27T10:30:00.000Z }}

const generatedAt = '{{timestamp}}';
{{! Output: const generatedAt = '2025-12-27T10:30:00.000Z'; }}
```

**Use Cases:**
- Generation metadata
- Comments
- Timestamps

---

### formatDate

Formats a date to YYYY-MM-DD format.

**Signature:** `formatDate(date: Date | string): string`

**Parameters:**
- `date` - Date object or ISO string

**Returns:** Formatted date string (YYYY-MM-DD)

**Examples:**

```handlebars
{{formatDate createdAt}}
{{! Output: 2025-12-27 }}

// Created: {{formatDate user.createdAt}}
{{! Output: // Created: 2025-12-27 }}
```

**Use Cases:**
- Date display
- Comments
- Metadata

---

### default

Returns value if not null/undefined, otherwise returns default.

**Signature:** `default(value: any, defaultValue: any): any`

**Parameters:**
- `value` - Value to check
- `defaultValue` - Fallback value

**Returns:** Value or default

**Examples:**

```handlebars
{{default optionalField "N/A"}}
{{! Output: N/A (if optionalField is undefined) }}

const issuer = '{{default jwtSettings.issuer "default-issuer"}}';
{{! Output: const issuer = 'default-issuer'; }}

{{default description "No description provided"}}
```

**Use Cases:**
- Optional fields
- Fallback values
- Safe access

---

### repeat

Repeats a string n times.

**Signature:** `repeat(str: string, count: number): string`

**Parameters:**
- `str` - String to repeat
- `count` - Number of repetitions

**Returns:** Repeated string

**Examples:**

```handlebars
{{repeat "=" 40}}
{{! Output: ======================================== }}

{{repeat " " indentLevel}}
{{! Output: "    " (4 spaces if indentLevel=4) }}

// {{repeat "-" 50}}
{{! Output: // -------------------------------------------------- }}
```

**Use Cases:**
- Separators
- Indentation
- Formatting

---

### truncate

Truncates a string to maximum length, adding "..." if truncated.

**Signature:** `truncate(str: string, maxLength: number): string`

**Parameters:**
- `str` - String to truncate
- `maxLength` - Maximum length

**Returns:** Truncated string with "..." if needed

**Examples:**

```handlebars
{{truncate description 50}}
{{! Output: First 50 characters... }}

// {{truncate longComment 80}}
{{! Output: // First 80 characters of comment... }}
```

**Use Cases:**
- Comments
- Descriptions
- Display text

---

### replace

Replaces all occurrences of a pattern in a string.

**Signature:** `replace(str: string, search: string, replacement: string): string`

**Parameters:**
- `str` - String to process
- `search` - Pattern to find (regex)
- `replacement` - Replacement string

**Returns:** String with replacements

**Examples:**

```handlebars
{{replace path "/" "."}}
{{! Input: "auth/user/profile" }}
{{! Output: "auth.user.profile" }}

{{replace email "@" " at "}}
{{! Input: "user@example.com" }}
{{! Output: "user at example.com" }}

const normalized = '{{replace fieldName "-" "_"}}';
{{! Output: const normalized = 'user_name'; }}
```

**Use Cases:**
- Path conversion
- String normalization
- Format transformation

---

## Usage Tips

### Combining Helpers

Helpers can be nested for complex transformations:

```handlebars
{{uppercase (camelCase "user_role")}}
{{! Output: USERROLE }}

{{pascalCase (replace path "/" "_")}}
{{! Output: Auth_User_Profile }}

{{#if (and (eq role "admin") (gt (length permissions) 5))}}
  // Admin with many permissions
{{/if}}
```

### Helper Precedence

Inner helpers are evaluated first:

```handlebars
{{capitalize (lowercase "ADMIN")}}
{{! 1. lowercase "ADMIN" → "admin" }}
{{! 2. capitalize "admin" → "Admin" }}
{{! Output: Admin }}
```

### Error Handling

Helpers handle null/undefined gracefully:

```handlebars
{{uppercase undefined}}
{{! Output: "" (empty string) }}

{{default null "fallback"}}
{{! Output: "fallback" }}

{{length undefined}}
{{! Output: 0 }}
```

---

## See Also

- [Template Usage Guide](./TEMPLATE_GUIDE.md) - Complete template documentation
- [API Documentation](./API_DOCUMENTATION.md) - Generator API reference
- [Examples](../examples/) - Real-world template examples

---

**End of Helper Reference**
