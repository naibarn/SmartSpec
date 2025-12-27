# Template Usage Guide - Outline

## Document Structure

### 1. **Introduction**
   - What are Templates?
   - Why Use Templates?
   - Template Engine (Handlebars)
   - Template Architecture

### 2. **Template Basics**

#### 2.1 **Template Structure**
   - File organization
   - Naming conventions
   - File extensions (.hbs)

#### 2.2 **Template Syntax**
   - Variables: `{{variable}}`
   - Comments: `{{! comment }}`
   - Blocks: `{{#if}}...{{/if}}`
   - Partials: `{{> partial}}`

#### 2.3 **Context Data**
   - What is context?
   - Context structure
   - Accessing nested data

### 3. **Built-in Templates**

#### 3.1 **Controller Template**
   - Location: `templates/auth/controllers/auth.controller.ts.hbs`
   - Purpose: Generate auth endpoints
   - Available Context:
     - `features`
     - `securitySettings`
     - `rbac`
     - `userModel`
   - Generated Output
   - Customization Points

#### 3.2 **Middleware Template**
   - Location: `templates/auth/middleware/auth.middleware.ts.hbs`
   - Purpose: Generate JWT verification and RBAC
   - Available Context:
     - `features`
     - `rbac`
     - `jwtSettings`
   - Generated Output
   - Customization Points

#### 3.3 **Types Template**
   - Location: `templates/auth/types/auth.types.ts.hbs`
   - Purpose: Generate TypeScript types
   - Available Context:
     - `rbac`
     - `features`
     - `securitySettings`
     - `jwtSettings`
     - `userModel`
   - Generated Output
   - Customization Points

#### 3.4 **Routes Template**
   - Location: `templates/auth/routes/auth.routes.ts.hbs`
   - Purpose: Generate Express routes
   - Available Context:
     - `features`
   - Generated Output
   - Customization Points

#### 3.5 **Service Template**
   - Location: `templates/auth/services/auth.service.ts.hbs`
   - Purpose: Generate auth business logic
   - Available Context:
     - `features`
     - `securitySettings`
     - `rbac`
   - Generated Output
   - Customization Points

### 4. **Handlebars Helpers**

#### 4.1 **String Helpers**
   - `uppercase` - Convert to UPPERCASE
   - `lowercase` - Convert to lowercase
   - `capitalize` - Capitalize first letter
   - `camelCase` - Convert to camelCase
   - `pascalCase` - Convert to PascalCase
   - `snakeCase` - Convert to snake_case
   - `kebabCase` - Convert to kebab-case

#### 4.2 **Array Helpers**
   - `includes` - Check if array includes value
   - `length` - Get array length
   - `join` - Join array with separator
   - `first` - Get first element
   - `last` - Get last element

#### 4.3 **Comparison Helpers**
   - `eq` - Equal (===)
   - `neq` - Not equal (!==)
   - `gt` - Greater than (>)
   - `lt` - Less than (<)
   - `gte` - Greater than or equal (>=)
   - `lte` - Less than or equal (<=)

#### 4.4 **Logical Helpers**
   - `and` - Logical AND
   - `or` - Logical OR
   - `not` - Logical NOT

#### 4.5 **Utility Helpers**
   - `json` - Stringify to JSON
   - `add` - Add numbers
   - `subtract` - Subtract numbers
   - `multiply` - Multiply numbers
   - `divide` - Divide numbers
   - `timestamp` - Current ISO timestamp
   - `formatDate` - Format date
   - `default` - Default value if null/undefined
   - `repeat` - Repeat string n times
   - `truncate` - Truncate string
   - `replace` - Replace string pattern

### 5. **Template Context Reference**

#### 5.1 **Features Object**
```typescript
{
  emailVerification: boolean,
  passwordReset: boolean,
  accountLockout: boolean
}
```

#### 5.2 **RBAC Object**
```typescript
{
  enabled: boolean,
  roles: Array<{ name: string }>,
  defaultRole: string
}
```

#### 5.3 **JWT Settings Object**
```typescript
{
  algorithm: string,
  accessTokenExpiry: string,
  refreshTokenExpiry: string,
  issuer: string,
  audience: string
}
```

#### 5.4 **Security Settings Object**
```typescript
{
  passwordRequirements: {
    minLength: number,
    requireUppercase: boolean,
    requireLowercase: boolean,
    requireNumbers: boolean,
    requireSpecialChars: boolean,
    saltRounds: number
  },
  accountLockout: {
    maxAttempts: number,
    lockoutDuration: number
  }
}
```

#### 5.5 **User Model Object**
```typescript
{
  fields: Array<{
    name: string,
    type: string,
    optional?: boolean
  }>
}
```

#### 5.6 **Excluded Fields Array**
```typescript
['email', 'password', 'role', 'emailVerified', 'failedLoginAttempts', 'lockedUntil']
```

### 6. **Creating Custom Templates**

#### 6.1 **Template Creation Process**
   - Step 1: Create .hbs file
   - Step 2: Define context requirements
   - Step 3: Write template code
   - Step 4: Test template
   - Step 5: Register template

#### 6.2 **Template Best Practices**
   - Keep templates simple
   - Use helpers for complex logic
   - Provide sensible defaults
   - Add comments
   - Test edge cases

#### 6.3 **Custom Helper Creation**
   - When to create custom helpers
   - Helper function signature
   - Registration process
   - Testing helpers

### 7. **Template Examples**

#### 7.1 **Conditional Rendering**
```handlebars
{{#if features.emailVerification}}
  // Email verification code
{{/if}}
```

#### 7.2 **Iterating Arrays**
```handlebars
{{#each rbac.roles}}
  {{uppercase this.name}}
{{/each}}
```

#### 7.3 **Nested Conditionals**
```handlebars
{{#if rbac.enabled}}
  {{#each rbac.roles}}
    // Role-specific code
  {{/each}}
{{/if}}
```

#### 7.4 **Using Helpers**
```handlebars
{{capitalize fieldName}}
{{uppercase roleName}}
{{json contextObject}}
```

#### 7.5 **Default Values**
```handlebars
{{default optionalValue "defaultValue"}}
```

### 8. **Template Debugging**

#### 8.1 **Common Issues**
   - Undefined variables
   - Helper not found
   - Syntax errors
   - Context mismatch

#### 8.2 **Debug Techniques**
   - Use `{{json this}}` to inspect context
   - Add debug comments
   - Test with minimal context
   - Check helper registration

#### 8.3 **Validation**
   - Syntax validation
   - Context validation
   - Output validation

### 9. **Template Variants**

#### 9.1 **Basic Variant**
   - Minimal features
   - Simple RBAC
   - Standard security

#### 9.2 **Standard Variant**
   - Email verification
   - Password reset
   - Basic RBAC
   - Account lockout

#### 9.3 **Advanced Variant**
   - All features
   - Complex RBAC
   - Enhanced security
   - Custom fields

#### 9.4 **Enterprise Variant**
   - SSO integration
   - Multi-factor auth
   - Advanced audit logging
   - Custom workflows

### 10. **Template Maintenance**

#### 10.1 **Version Control**
   - Template versioning
   - Breaking changes
   - Migration guides

#### 10.2 **Testing Templates**
   - Unit tests
   - Integration tests
   - Snapshot tests

#### 10.3 **Documentation**
   - Template comments
   - Context documentation
   - Example outputs

### 11. **Advanced Topics**

#### 11.1 **Template Composition**
   - Using partials
   - Template inheritance
   - Shared components

#### 11.2 **Performance Optimization**
   - Template caching
   - Compilation optimization
   - Context preparation

#### 11.3 **Internationalization**
   - Multi-language templates
   - Locale-specific output
   - Translation helpers

### 12. **Migration & Upgrades**

#### 12.1 **Template Migration**
   - Migrating from old templates
   - Breaking changes
   - Compatibility mode

#### 12.2 **Custom Template Migration**
   - Updating custom templates
   - New helper adoption
   - Context changes

### 13. **Appendix**

#### 13.1 **Complete Helper Reference**
   - All helpers with examples
   - Parameter descriptions
   - Return values

#### 13.2 **Template Cheat Sheet**
   - Common patterns
   - Quick reference
   - Code snippets

#### 13.3 **Troubleshooting Guide**
   - Error messages
   - Solutions
   - Prevention tips

---

## Document Metadata

- **Target Audience:** Template developers and customizers
- **Skill Level:** Intermediate
- **Prerequisites:** Basic Handlebars knowledge
- **Estimated Reading Time:** 45-60 minutes
- **Format:** Markdown with code examples
- **Maintenance:** Updated with template changes
