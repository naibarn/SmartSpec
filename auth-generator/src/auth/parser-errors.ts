/**
 * Parser Error Types
 * 
 * Detailed error types for better parser error reporting
 */

export interface ParseError {
  line: number;
  column?: number;
  message: string;
  suggestion?: string;
  context?: string;
}

export class SpecParseError extends Error {
  public errors: ParseError[];

  constructor(errors: ParseError[]) {
    const message = SpecParseError.formatErrors(errors);
    super(message);
    this.name = 'SpecParseError';
    this.errors = errors;
  }

  static formatErrors(errors: ParseError[]): string {
    const lines = ['Spec parsing failed with the following errors:\n'];
    
    for (const error of errors) {
      lines.push(`  Line ${error.line}${error.column ? `:${error.column}` : ''}: ${error.message}`);
      
      if (error.context) {
        lines.push(`    Context: ${error.context}`);
      }
      
      if (error.suggestion) {
        lines.push(`    Suggestion: ${error.suggestion}`);
      }
      
      lines.push('');
    }
    
    return lines.join('\n');
  }
}

export function createParseError(
  line: number,
  message: string,
  options?: {
    column?: number;
    suggestion?: string;
    context?: string;
  }
): ParseError {
  return {
    line,
    column: options?.column,
    message,
    suggestion: options?.suggestion,
    context: options?.context,
  };
}
