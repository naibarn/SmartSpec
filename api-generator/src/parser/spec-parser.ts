import { marked } from 'marked';
import {
  APISpec,
  Entity,
  Field,
  Endpoint,
  Parameter,
  // Response,
  ErrorResponse,
  BusinessRule,
  FieldType,
  HttpMethod,
  ParameterLocation,
  FieldConstraint,
  Relationship,
  Index
} from '../types/ast.types';

/**
 * SpecParser
 * Parses markdown API specification to AST
 */
export class SpecParser {
  /**
   * Parse markdown spec file to APISpec AST
   */
  async parse(markdown: string): Promise<APISpec> {
    // Parse markdown to tokens
    const tokens = marked.lexer(markdown);

    // Initialize AST
    const spec: APISpec = {
      name: '',
      version: '1.0',
      entities: [],
      endpoints: [],
      businessRules: [],
      metadata: {}
    };

    // Extract spec name and version from first heading
    const firstHeading = tokens.find(t => t.type === 'heading' && t.depth === 1);
    if (firstHeading && 'text' in firstHeading) {
      spec.name = this.extractSpecName(firstHeading.text);
    }

    // Parse sections
    let currentSection: string | null = null;
    let currentSubsection: string | null = null;
    let sectionContent: string[] = [];

    for (let i = 0; i < tokens.length; i++) {
      const token = tokens[i];

      if (token.type === 'heading') {
        // Process previous section
        if (currentSection && sectionContent.length > 0) {
          this.processSection(spec, currentSection, currentSubsection, sectionContent.join('\n'));
          sectionContent = [];
        }

        // Start new section
        if (token.depth === 2) {
          currentSection = 'text' in token ? token.text : '';
          currentSubsection = null;
        } else if (token.depth === 3) {
          currentSubsection = 'text' in token ? token.text : '';
        }
      } else {
        // Accumulate section content
        if ('raw' in token) {
          sectionContent.push(token.raw);
        }
      }
    }

    // Process last section
    if (currentSection && sectionContent.length > 0) {
      this.processSection(spec, currentSection, currentSubsection, sectionContent.join('\n'));
    }

    return spec;
  }

  /**
   * Extract spec name from heading text
   */
  private extractSpecName(text: string): string {
    // Remove "API Specification:" prefix if present
    return text.replace(/^API Specification:\s*/i, '').trim();
  }

  /**
   * Process a section of the spec
   */
  private processSection(
    spec: APISpec,
    section: string,
    subsection: string | null,
    content: string
  ): void {
    const sectionLower = section.toLowerCase();

    if (sectionLower.includes('entit')) {
      // Entities section
      if (subsection) {
        const entity = this.parseEntity(subsection, content);
        spec.entities.push(entity);
      }
    } else if (sectionLower.includes('endpoint')) {
      // Endpoints section
      if (subsection) {
        const endpoint = this.parseEndpoint(subsection, content);
        spec.endpoints.push(endpoint);
      }
    } else if (sectionLower.includes('business rule')) {
      // Business rules section
      const rules = this.parseBusinessRules(content);
      spec.businessRules.push(...rules);
    } else if (sectionLower.includes('rate limit')) {
      // Rate limiting section
      spec.rateLimit = this.parseRateLimit(content);
    }
  }

  /**
   * Parse entity definition
   */
  private parseEntity(name: string, content: string): Entity {
    const entity: Entity = {
      name: name.trim(),
      fields: [],
      relationships: [],
      indexes: []
    };

    const lines = content.split('\n');
    let currentSubsection: string | null = null;

    for (const line of lines) {
      const trimmed = line.trim();

      // Check for subsection headers
      if (trimmed.startsWith('**') && trimmed.endsWith('**')) {
        currentSubsection = trimmed.replace(/\*\*/g, '').toLowerCase();
        continue;
      }

      // Parse based on current subsection
      if (currentSubsection === 'fields:' || currentSubsection === 'fields') {
        if (trimmed.startsWith('- `') || trimmed.startsWith('* `')) {
          const field = this.parseField(trimmed);
          if (field) {
            entity.fields.push(field);
          }
        }
      } else if (currentSubsection === 'relationships:' || currentSubsection === 'relationships') {
        if (trimmed.startsWith('- ') || trimmed.startsWith('* ')) {
          const relationship = this.parseRelationship(trimmed);
          if (relationship) {
            entity.relationships.push(relationship);
          }
        }
      } else if (currentSubsection === 'indexes:' || currentSubsection === 'indexes') {
        if (trimmed.startsWith('- `') || trimmed.startsWith('* `')) {
          const index = this.parseIndex(trimmed);
          if (index) {
            entity.indexes.push(index);
          }
        }
      }
    }

    return entity;
  }

  /**
   * Parse field definition
   * Format: - `fieldName`: type (constraints)
   */
  private parseField(line: string): Field | null {
    // Extract field name and definition
    const match = line.match(/[`]([^`]+)[`]:\s*(.+)/);
    if (!match) return null;

    const fieldName = match[1].trim();
    const definition = match[2].trim();

    // Parse type and constraints
    const parts = definition.split('(');
    const typePart = parts[0].trim();
    const constraintsPart = parts.length > 1 ? parts[1].replace(')', '').trim() : '';

    const field: Field = {
      name: fieldName,
      type: this.parseFieldType(typePart),
      constraints: this.parseConstraints(constraintsPart)
    };

    // Check for UUID in constraints (overrides type)
    if (constraintsPart.toLowerCase().includes('uuid')) {
      field.type = 'uuid';
    }

    // Check for special flags
    if (constraintsPart.includes('primary key')) {
      field.isPrimaryKey = true;
    }
    if (constraintsPart.includes('foreign key')) {
      field.isForeignKey = true;
      const fkMatch = constraintsPart.match(/foreign key to (\w+)/i);
      if (fkMatch) {
        field.foreignKeyTo = fkMatch[1];
      }
    }
    if (constraintsPart.includes('auto-generated') || constraintsPart.includes('auto-updated')) {
      field.isAutoGenerated = true;
    }

    return field;
  }

  /**
   * Parse field type
   */
  private parseFieldType(typeStr: string): FieldType {
    const lower = typeStr.toLowerCase();
    
    // Check UUID first (before string)
    if (lower === 'uuid' || lower.includes('uuid')) return 'uuid';
    if (lower.includes('datetime')) return 'datetime';
    if (lower.includes('date')) return 'date';
    if (lower.includes('time')) return 'time';
    if (lower.includes('bool')) return 'boolean';
    if (lower.includes('int')) return 'integer';
    if (lower.includes('number') || lower.includes('float') || lower.includes('decimal')) return 'number';
    if (lower.includes('json')) return 'json';
    if (lower.includes('array')) return 'array';
    
    return 'string'; // default
  }

  /**
   * Parse field constraints
   */
  private parseConstraints(constraintsStr: string): FieldConstraint[] {
    const constraints: FieldConstraint[] = [];
    const parts = constraintsStr.split(',').map(p => p.trim());

    for (const part of parts) {
      const lower = part.toLowerCase();

      if (lower === 'required') {
        constraints.push({ type: 'required' });
      } else if (lower === 'unique') {
        constraints.push({ type: 'unique' });
      } else if (lower.startsWith('max')) {
        const match = part.match(/max\s+(\d+)/i);
        if (match) {
          constraints.push({ type: 'max', value: parseInt(match[1]) });
        }
      } else if (lower.startsWith('min')) {
        const match = part.match(/min\s+(\d+)/i);
        if (match) {
          constraints.push({ type: 'min', value: parseInt(match[1]) });
        }
      } else if (lower.startsWith('default')) {
        const match = part.match(/default:\s*(.+)/i);
        if (match) {
          let value: any = match[1].trim();
          // Parse boolean
          if (value === 'true') value = true;
          else if (value === 'false') value = false;
          // Parse number
          else if (!isNaN(Number(value))) value = Number(value);
          
          constraints.push({ type: 'default', value });
        }
      }
    }

    return constraints;
  }

  /**
   * Parse relationship
   */
  private parseRelationship(line: string): Relationship | null {
    const lower = line.toLowerCase();
    
    let type: Relationship['type'] | null = null;
    let entity: string | null = null;

    if (lower.includes('belongs to')) {
      type = 'many-to-one';
      const match = line.match(/belongs to (\w+)/i);
      if (match) entity = match[1];
    } else if (lower.includes('has many')) {
      type = 'one-to-many';
      const match = line.match(/has many (\w+)/i);
      if (match) entity = match[1];
    } else if (lower.includes('has one')) {
      type = 'one-to-one';
      const match = line.match(/has one (\w+)/i);
      if (match) entity = match[1];
    }

    if (type && entity) {
      return { type, entity };
    }

    return null;
  }

  /**
   * Parse index
   */
  private parseIndex(line: string): Index | null {
    const match = line.match(/[`]([^`]+)[`]/);
    if (!match) return null;

    const fieldName = match[1].trim();
    const unique = line.toLowerCase().includes('unique');

    return {
      fields: [fieldName],
      unique
    };
  }

  /**
   * Parse endpoint definition
   */
  private parseEndpoint(heading: string, content: string): Endpoint {
    // Extract method and path from heading
    // Format: "GET /api/todos" or "POST /api/todos"
    const match = heading.match(/^(GET|POST|PUT|PATCH|DELETE)\s+(.+)$/i);
    
    const method: HttpMethod = match ? (match[1].toUpperCase() as HttpMethod) : 'GET';
    const path = match ? match[2].trim() : heading;

    const endpoint: Endpoint = {
      method,
      path,
      description: '',
      requiresAuth: false,
      parameters: [],
      responses: [],
      errors: []
    };

    const lines = content.split('\n');
    let currentSubsection: string | null = null;
    let codeBlock: string[] = [];
    let inCodeBlock = false;

    for (const line of lines) {
      const trimmed = line.trim();

      // Handle code blocks
      if (trimmed.startsWith('```')) {
        if (inCodeBlock) {
          // End of code block
          inCodeBlock = false;
          // Process code block based on current subsection
          if (currentSubsection === 'request body:') {
            endpoint.requestBody = codeBlock.join('\n');
          }
          codeBlock = [];
        } else {
          // Start of code block
          inCodeBlock = true;
        }
        continue;
      }

      if (inCodeBlock) {
        codeBlock.push(line);
        continue;
      }

      // Check for subsection headers
      if (trimmed.startsWith('**') && trimmed.endsWith('**')) {
        currentSubsection = trimmed.replace(/\*\*/g, '').toLowerCase();
        continue;
      }

      // Parse based on content
      if (trimmed.startsWith('- ') || trimmed.startsWith('* ')) {
        const content = trimmed.substring(2);

        if (currentSubsection === 'query parameters:' || currentSubsection === 'path parameters:') {
          const param = this.parseParameter(content, currentSubsection.includes('query') ? 'query' : 'path');
          if (param) {
            endpoint.parameters.push(param);
          }
        } else if (currentSubsection === 'errors:') {
          const error = this.parseError(content);
          if (error) {
            endpoint.errors.push(error);
          }
        }
      } else if (trimmed.startsWith('Description:')) {
        endpoint.description = trimmed.replace('Description:', '').trim();
      } else if (trimmed.startsWith('Authentication:') || trimmed.startsWith('**Authentication:**')) {
        const authText = trimmed.replace(/\*\*/g, '').toLowerCase();
        endpoint.requiresAuth = authText.includes('required') && !authText.includes('not required');
      }
    }

    return endpoint;
  }

  /**
   * Parse parameter
   */
  private parseParameter(line: string, location: ParameterLocation): Parameter | null {
    // Format: name: type (optional/required, constraints)
    const match = line.match(/([^:]+):\s*(.+)/);
    if (!match) return null;

    const name = match[1].trim();
    const definition = match[2].trim();

    const parts = definition.split('(');
    const typePart = parts[0].trim();
    const constraintsPart = parts.length > 1 ? parts[1].replace(')', '').trim() : '';

    const required = constraintsPart.toLowerCase().includes('required') || 
                    !constraintsPart.toLowerCase().includes('optional');

    return {
      name,
      location,
      type: this.parseFieldType(typePart),
      required,
      constraints: this.parseConstraints(constraintsPart)
    };
  }

  /**
   * Parse error response
   */
  private parseError(line: string): ErrorResponse | null {
    // Format: 400: Message or 400 Bad Request: Message
    const match = line.match(/^(\d{3})(?:\s+[\w\s]+)?:\s*(.+)$/);
    if (!match) return null;

    const statusCode = parseInt(match[1]);
    const message = match[2].trim();

    return {
      statusCode,
      code: this.statusCodeToErrorCode(statusCode),
      message
    };
  }

  /**
   * Convert status code to error code
   */
  private statusCodeToErrorCode(statusCode: number): string {
    const codeMap: Record<number, string> = {
      400: 'VALIDATION_ERROR',
      401: 'UNAUTHORIZED',
      403: 'FORBIDDEN',
      404: 'NOT_FOUND',
      409: 'CONFLICT',
      429: 'RATE_LIMIT_EXCEEDED',
      500: 'INTERNAL_ERROR'
    };

    return codeMap[statusCode] || 'ERROR';
  }

  /**
   * Parse business rules
   */
  private parseBusinessRules(content: string): BusinessRule[] {
    const rules: BusinessRule[] = [];
    const lines = content.split('\n');

    for (const line of lines) {
      const trimmed = line.trim();
      if (trimmed.startsWith('-') || trimmed.startsWith('*') || trimmed.match(/^\d+\./)) {
        const description = trimmed.replace(/^[-*\d.]\s*/, '').trim();
        if (description) {
          rules.push({
            type: 'business-logic',
            description
          });
        }
      }
    }

    return rules;
  }

  /**
   * Parse rate limit configuration
   */
  private parseRateLimit(content: string): any {
    const lines = content.split('\n');
    
    for (const line of lines) {
      const trimmed = line.trim();
      if (trimmed.startsWith('- **Rate:**') || trimmed.startsWith('* **Rate:**')) {
        const match = trimmed.match(/(\d+)\s+requests?\s+per\s+(.+)/i);
        if (match) {
          return {
            requests: parseInt(match[1]),
            window: match[2].trim(),
            scope: 'per-user'
          };
        }
      }
    }

    return undefined;
  }
}
