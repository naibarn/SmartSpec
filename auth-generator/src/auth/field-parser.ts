/**
 * Field Parser
 * 
 * Improved parser for user model fields with better error handling
 */

import { UserField, FieldConstraint } from '../types/auth-ast.types';
import { createParseError, ParseError } from './parser-errors';

export interface FieldParseResult {
  success: boolean;
  field?: UserField;
  errors: ParseError[];
}

export class FieldParser {
  /**
   * Parse field with flexible syntax support
   * 
   * Supported formats:
   * - name: type
   * - name: type (constraints)
   * - name : type (constraints)  // extra spaces
   * - name:type(constraints)     // no spaces
   */
  parse(text: string, lineNumber: number): FieldParseResult {
    const errors: ParseError[] = [];
    
    // Trim and normalize whitespace
    const normalized = text.trim().replace(/\s+/g, ' ');
    
    if (!normalized) {
      errors.push(createParseError(lineNumber, 'Empty field definition'));
      return { success: false, errors };
    }

    // Try to extract name and rest
    const colonIndex = normalized.indexOf(':');
    if (colonIndex === -1) {
      errors.push(createParseError(
        lineNumber,
        'Missing colon separator',
        {
          context: normalized,
          suggestion: 'Field format should be: name: type (constraints)'
        }
      ));
      return { success: false, errors };
    }

    const name = normalized.substring(0, colonIndex).trim();
    const rest = normalized.substring(colonIndex + 1).trim();

    // Validate name
    if (!name) {
      errors.push(createParseError(
        lineNumber,
        'Missing field name',
        {
          context: normalized,
          suggestion: 'Field name is required before colon'
        }
      ));
      return { success: false, errors };
    }

    if (!/^[a-zA-Z_][a-zA-Z0-9_]*$/.test(name)) {
      errors.push(createParseError(
        lineNumber,
        `Invalid field name: ${name}`,
        {
          context: normalized,
          suggestion: 'Field name must start with letter or underscore, followed by letters, numbers, or underscores'
        }
      ));
      return { success: false, errors };
    }

    // Extract type and constraints
    let type: string;
    let constraintsStr: string | undefined;

    const parenIndex = rest.indexOf('(');
    if (parenIndex === -1) {
      // No constraints
      type = rest.trim();
      constraintsStr = undefined;
    } else {
      // Has constraints
      type = rest.substring(0, parenIndex).trim();
      
      const closeParen = rest.lastIndexOf(')');
      if (closeParen === -1) {
        errors.push(createParseError(
          lineNumber,
          'Unclosed parenthesis in constraints',
          {
            context: normalized,
            suggestion: 'Add closing parenthesis: )'
          }
        ));
        return { success: false, errors };
      }
      
      constraintsStr = rest.substring(parenIndex + 1, closeParen).trim();
    }

    // Validate type
    if (!type) {
      errors.push(createParseError(
        lineNumber,
        'Missing field type',
        {
          context: normalized,
          suggestion: 'Field type is required after colon'
        }
      ));
      return { success: false, errors };
    }

    // Handle enum type specially
    let enumValues: string[] | undefined;
    if (type.startsWith('enum')) {
      const enumMatch = type.match(/enum\s*\(([^)]+)\)/);
      if (enumMatch) {
        enumValues = enumMatch[1].split(',').map(v => v.trim()).filter(v => v);
        type = 'enum';
        
        if (enumValues.length === 0) {
          errors.push(createParseError(
            lineNumber,
            'Enum type requires at least one value',
            {
              context: normalized,
              suggestion: 'Example: role: enum(user, admin)'
            }
          ));
          return { success: false, errors };
        }
      }
    }

    // Parse constraints
    const constraints = constraintsStr ? this.parseConstraints(constraintsStr, lineNumber) : [];

    const field: UserField = {
      name,
      type,
      constraints,
      enumValues
    };

    return {
      success: true,
      field,
      errors: []
    };
  }

  /**
   * Parse constraints string
   */
  private parseConstraints(constraintsStr: string, lineNumber: number): FieldConstraint[] {
    const constraints: FieldConstraint[] = [];
    
    if (!constraintsStr) return constraints;

    const parts = constraintsStr.split(',').map(p => p.trim());

    for (const part of parts) {
      if (!part) continue;

      // Simple constraints
      if (part === 'required') {
        constraints.push({ type: 'required' });
      } else if (part === 'unique') {
        constraints.push({ type: 'unique' });
      } else if (part === 'auto') {
        constraints.push({ type: 'auto' });
      } else if (part === 'hashed') {
        constraints.push({ type: 'hashed' });
      } else if (part === 'primary key') {
        constraints.push({ type: 'primary key' });
      }
      // Constraints with values
      else if (part.startsWith('max')) {
        const match = part.match(/max[:\s]+(\d+)/);
        if (match) {
          constraints.push({ type: 'max', value: parseInt(match[1]) });
        }
      } else if (part.startsWith('min')) {
        const match = part.match(/min[:\s]+(\d+)/);
        if (match) {
          constraints.push({ type: 'min', value: parseInt(match[1]) });
        }
      } else if (part.startsWith('default')) {
        const match = part.match(/default[:\s]+(.+)/);
        if (match) {
          let value: any = match[1].trim();
          // Try to parse as number or boolean
          if (value === 'true') value = true;
          else if (value === 'false') value = false;
          else if (/^\d+$/.test(value)) value = parseInt(value);
          else if (/^\d+\.\d+$/.test(value)) value = parseFloat(value);
          
          constraints.push({ type: 'default', value });
        }
      }
    }

    return constraints;
  }
}
