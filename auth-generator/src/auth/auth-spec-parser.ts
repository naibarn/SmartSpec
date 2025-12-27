/**
 * Auth Spec Parser
 * 
 * Parses markdown auth specification into AST
 */

import { marked } from 'marked';
import { FieldParser } from './field-parser';
// import { SpecParseError, createParseError, ParseError } from './parser-errors';
import {
  AuthSpec,
  UserModel,
  UserField,
  // FieldConstraint,
  Index,
  AuthMethods,
  TokenConfig,
  ProtectedEndpoint,
  PublicEndpoint,
  Features,
  SecuritySettings,
  BusinessRules,
  ErrorResponse,
  RBAC,
} from '../types/auth-ast.types';

export class AuthSpecParser {
  private fieldParser: FieldParser;

  constructor() {
    this.fieldParser = new FieldParser();
  }
  parse(markdown: string): AuthSpec {
    const tokens = marked.lexer(markdown);
    
    const userModel = this.parseUserModel(tokens);
    const rbac = this.extractRBACFromUserModel(userModel);
    
    return {
      userModel,
      authMethods: this.parseAuthMethods(tokens),
      tokenConfig: this.parseTokenConfig(tokens),
      protectedEndpoints: this.parseProtectedEndpoints(tokens),
      publicEndpoints: this.parsePublicEndpoints(tokens),
      features: this.parseFeatures(tokens),
      securitySettings: this.parseSecuritySettings(tokens),
      businessRules: this.parseBusinessRules(tokens),
      errorResponses: this.parseErrorResponses(tokens),
      rbac,
    };
  }

  /**
   * Extract RBAC configuration from user model role field
   */
  private extractRBACFromUserModel(userModel: UserModel): RBAC | undefined {
    // Find role field
    const roleField = userModel.fields.find(f => f.name === 'role' && f.type === 'enum');
    
    if (!roleField || !roleField.enumValues || roleField.enumValues.length === 0) {
      return undefined;
    }
    
    // Create RBAC config from enum values
    return {
      enabled: true,
      roles: roleField.enumValues,
      defaultRole: roleField.enumValues[0], // First role is default
      permissions: {}, // Empty for now
    };
  }

  private parseUserModel(tokens: any[]): UserModel {
    const fields: UserField[] = [];
    const indexes: Index[] = [];
    
    let inUserModel = false;
    let inFields = false;
    let inIndexes = false;
    
    for (const token of tokens) {
      if (token.type === 'heading' && token.depth === 2) {
        inUserModel = token.text === 'User Model';
        inFields = false;
        inIndexes = false;
      }
      
      if (inUserModel && token.type === 'heading' && token.depth === 3) {
        inFields = token.text === 'Fields';
        inIndexes = token.text === 'Indexes';
      }
      
      if (inFields && token.type === 'list') {
        let lineNumber = 0;
        for (const item of token.items) {
          lineNumber++;
          const field = this.parseField(item.text, lineNumber);
          if (field) fields.push(field);
        }
      }
      
      if (inIndexes && token.type === 'list') {
        for (const item of token.items) {
          const index = this.parseIndex(item.text);
          if (index) indexes.push(index);
        }
      }
    }
    
    return { fields, indexes };
  }

  private parseField(text: string, lineNumber: number = 0): UserField | null {
    const result = this.fieldParser.parse(text, lineNumber);
    
    if (!result.success) {
      // Log errors but don't throw - allow parser to continue
      console.warn(`Field parse error at line ${lineNumber}:`);
      for (const error of result.errors) {
        console.warn(`  ${error.message}`);
        if (error.suggestion) {
          console.warn(`  Suggestion: ${error.suggestion}`);
        }
      }
      return null;
    }
    
    return result.field || null;
  }

  /*
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  private parseConstraints(constraintsStr: string): FieldConstraint[] {
    const constraints: FieldConstraint[] = [];
    
    if (!constraintsStr) return constraints;
    
    const parts = constraintsStr.split(',').map(p => p.trim());
    
    for (const part of parts) {
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
      } else if (part.startsWith('max ')) {
        const value = parseInt(part.substring(4));
        constraints.push({ type: 'max', value });
      } else if (part.startsWith('min ')) {
        const value = parseInt(part.substring(4));
        constraints.push({ type: 'min', value });
      } else if (part.startsWith('default:')) {
        const value = part.substring(8).trim();
        constraints.push({ type: 'default', value });
      }
    }
    
    return constraints;
  }
  */

  private parseIndex(text: string): Index | null {
    // Format: "field (unique)" or "field"
    const match = text.match(/^(\w+)\s*(\(unique\))?/);
    if (!match) return null;
    
    const fields = [match[1]];
    const unique = !!match[2];
    
    return { fields, unique };
  }

  private parseAuthMethods(tokens: any[]): AuthMethods {
    let password = false;
    
    for (const token of tokens) {
      if (token.type === 'heading' && token.depth === 2) {
        if (token.text === 'Authentication Methods') {
          // Look for next list
          const nextToken = tokens[tokens.indexOf(token) + 1];
          if (nextToken && nextToken.type === 'list') {
            for (const item of nextToken.items) {
              if (item.text.includes('Email/Password')) {
                password = true;
              }
            }
          }
        }
      }
    }
    
    return { password };
  }

  private parseTokenConfig(tokens: any[]): TokenConfig {
    let accessTokenExpiry = '15m';
    let refreshTokenExpiry = '7d';
    let algorithm = 'RS256';
    
    for (const token of tokens) {
      if (token.type === 'heading' && token.depth === 2) {
        if (token.text === 'Token Configuration') {
          // Look for next list
          const nextToken = tokens[tokens.indexOf(token) + 1];
          if (nextToken && nextToken.type === 'list') {
            for (const item of nextToken.items) {
              const text = item.text;
              if (text.includes('Access Token:')) {
                const match = text.match(/(\d+)\s*(minutes?|hours?|days?)/);
                if (match) {
                  const value = match[1];
                  const unit = match[2].charAt(0);  // m, h, d
                  accessTokenExpiry = `${value}${unit}`;
                }
              } else if (text.includes('Refresh Token:')) {
                const match = text.match(/(\d+)\s*(days?|hours?)/);
                if (match) {
                  const value = match[1];
                  const unit = match[2].charAt(0);
                  refreshTokenExpiry = `${value}${unit}`;
                }
              } else if (text.includes('Algorithm:')) {
                const match = text.match(/Algorithm:\s*(\w+)/);
                if (match) {
                  algorithm = match[1];
                }
              }
            }
          }
        }
      }
    }
    
    return {
      accessToken: { expiresIn: accessTokenExpiry },
      refreshToken: { expiresIn: refreshTokenExpiry, rotation: true },
      algorithm,
    };
  }

  private parseProtectedEndpoints(tokens: any[]): ProtectedEndpoint[] {
    const endpoints: ProtectedEndpoint[] = [];
    
    let inProtectedEndpoints = false;
    
    for (const token of tokens) {
      if (token.type === 'heading' && token.depth === 2) {
        inProtectedEndpoints = token.text === 'Protected Endpoints';
      }
      
      if (inProtectedEndpoints && token.type === 'list') {
        for (const item of token.items) {
          const endpoint = this.parseProtectedEndpoint(item.text);
          if (endpoint) endpoints.push(endpoint);
        }
      }
    }
    
    return endpoints;
  }

  private parseProtectedEndpoint(text: string): ProtectedEndpoint | null {
    // Format: "GET /api/todos (auth required, role: user)"
    const match = text.match(/^(GET|POST|PUT|DELETE|PATCH)\s+(\/[^\s(]+)\s*\(([^)]+)\)/);
    if (!match) return null;
    
    const method = match[1];
    const path = match[2];
    const requirementsStr = match[3];
    
    const authRequired = requirementsStr.includes('auth required');
    
    let role: string | undefined;
    const roleMatch = requirementsStr.match(/role:\s*(\w+)/);
    if (roleMatch) {
      role = roleMatch[1];
    }
    
    const ownerOnly = requirementsStr.includes('owner only');
    
    return { method, path, authRequired, role, ownerOnly };
  }

  private parsePublicEndpoints(tokens: any[]): PublicEndpoint[] {
    const endpoints: PublicEndpoint[] = [];
    
    let inPublicEndpoints = false;
    let currentCategory = '';
    
    for (const token of tokens) {
      if (token.type === 'heading' && token.depth === 2) {
        inPublicEndpoints = token.text === 'Public Endpoints';
      }
      
      if (inPublicEndpoints && token.type === 'heading' && token.depth === 3) {
        currentCategory = token.text.toLowerCase().replace(/\s+/g, '-');
      }
      
      if (inPublicEndpoints && token.type === 'list') {
        for (const item of token.items) {
          const endpoint = this.parsePublicEndpoint(item.text, currentCategory);
          if (endpoint) endpoints.push(endpoint);
        }
      }
    }
    
    return endpoints;
  }

  private parsePublicEndpoint(text: string, category: string): PublicEndpoint | null {
    // Format: "POST /auth/register - Register new user"
    const match = text.match(/^(GET|POST|PUT|DELETE|PATCH)\s+(\/[^\s-]+)\s*-\s*(.+)/);
    if (!match) return null;
    
    const method = match[1];
    const path = match[2];
    const description = match[3];
    
    return { method, path, description, category };
  }

  private parseFeatures(tokens: any[]): Features {
    let emailVerification = false;
    let passwordReset = false;
    let rateLimitEnabled = false;
    let sessionManagement = 'jwt';
    let tokenBlacklistEnabled = false;
    
    for (const token of tokens) {
      if (token.type === 'heading' && token.depth === 2) {
        if (token.text === 'Features') {
          const nextToken = tokens[tokens.indexOf(token) + 1];
          if (nextToken && nextToken.type === 'list') {
            for (const item of nextToken.items) {
              const text = item.text;
              if (text.includes('Email verification:')) {
                emailVerification = text.includes('yes');
              } else if (text.includes('Password reset:')) {
                passwordReset = text.includes('yes');
              } else if (text.includes('Rate limiting:')) {
                rateLimitEnabled = !text.includes('no');
              } else if (text.includes('Session management:')) {
                if (text.includes('JWT')) sessionManagement = 'jwt';
                else if (text.includes('session')) sessionManagement = 'session';
                else if (text.includes('hybrid')) sessionManagement = 'hybrid';
              } else if (text.includes('Token blacklist:')) {
                tokenBlacklistEnabled = text.includes('yes');
              }
            }
          }
        }
      }
    }
    
    return {
      emailVerification,
      passwordReset,
      rateLimit: { enabled: rateLimitEnabled, limits: {} },
      sessionManagement,
      tokenBlacklist: { enabled: tokenBlacklistEnabled, storage: 'redis' },
    };
  }

  private parseSecuritySettings(_tokens: any[]): SecuritySettings {
    const passwordRequirements = {
      minLength: 8,
      requireUppercase: false,
      requireLowercase: false,
      requireNumber: false,
      requireSpecial: false,
    };
    
    const rateLimits: { [category: string]: any } = {};
    
    const accountSecurity = {
      maxLoginAttempts: 5,
      lockoutWindow: '15m',
      lockoutDuration: '30m',
      passwordResetTokenExpiry: '1h',
      emailVerificationTokenExpiry: '24h',
    };
    
    // Parse from spec...
    // (Implementation similar to above)
    
    return {
      passwordRequirements,
      rateLimits,
      accountSecurity,
    };
  }

  private parseBusinessRules(_tokens: any[]): BusinessRules {
    // Default business rules
    return {
      registration: {
        emailMustBeUnique: true,
        passwordRequirements: 'Must meet strength requirements',
        defaultRole: 'user',
        emailVerificationRequired: true,
      },
      login: {
        emailAndPasswordRequired: true,
        accountMustBeActive: true,
        failedAttemptsTracked: true,
        resetFailedAttemptsOnSuccess: true,
      },
      tokenRefresh: {
        refreshTokenMustBeValid: true,
        issueNewTokens: true,
        invalidateOldRefreshToken: true,
      },
      passwordReset: {
        resetTokenSentToEmail: true,
        tokenValidDuration: '1h',
        oldPasswordNotRequired: true,
        invalidateAllSessionsAfterReset: true,
      },
      authorization: {
        userCanOnlyAccessOwn: true,
        adminCanAccessAll: true,
        adminCanDeleteAny: true,
        userCanOnlyDeleteOwn: true,
      },
    };
  }

  private parseErrorResponses(_tokens: any[]): ErrorResponse[] {
    const errors: ErrorResponse[] = [];
    
    // Parse error responses from spec...
    // (Implementation similar to above)
    
    return errors;
  }
}
