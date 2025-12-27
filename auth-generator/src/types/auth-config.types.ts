/**
 * Auth Configuration Types
 * 
 * TypeScript types for Auth Generator configuration
 */

export interface AuthGeneratorConfig {
  variant: 'basic' | 'standard' | 'advanced' | 'enterprise';
  outputDir: string;
  overwrite: boolean;
  generateTests: boolean;
  generateDocs: boolean;
}

export interface AuthConfig {
  // User model configuration
  userModel: UserModelConfig;
  
  // Authentication methods
  methods: AuthMethodsConfig;
  
  // Token configuration
  tokens: TokensConfig;
  
  // Authorization configuration
  authorization: AuthorizationConfig;
  
  // Security configuration
  security: SecurityConfig;
  
  // Business rules
  registration: RegistrationConfig;
  
  // Multi-tenancy
  multiTenancy: MultiTenancyConfig;
  
  // Plugins
  plugins?: AuthPlugin[];
}

export interface UserModelConfig {
  fields: string[];
  customFields?: string[];
  roleField: string;
  emailField: string;
}

export interface AuthMethodsConfig {
  password: PasswordAuthConfig;
  oauth?: OAuthAuthConfig;
  sso?: SSOAuthConfig;
  twoFactor?: TwoFactorAuthConfig;
}

export interface PasswordAuthConfig {
  enabled: boolean;
  minLength: number;
  requireUppercase: boolean;
  requireLowercase: boolean;
  requireNumber: boolean;
  requireSpecial: boolean;
}

export interface OAuthAuthConfig {
  enabled: boolean;
  providers: string[];
}

export interface SSOAuthConfig {
  enabled: boolean;
  provider?: string;
}

export interface TwoFactorAuthConfig {
  enabled: boolean;
  required: boolean;
  methods: string[];
}

export interface TokensConfig {
  strategy: 'jwt' | 'session' | 'hybrid';
  accessToken: AccessTokenConfig;
  refreshToken: RefreshTokenConfig;
  blacklist: BlacklistConfig;
}

export interface AccessTokenConfig {
  expiresIn: string;
  algorithm: 'RS256' | 'HS256';
}

export interface RefreshTokenConfig {
  expiresIn: string;
  rotation: boolean;
}

export interface BlacklistConfig {
  enabled: boolean;
  storage: 'redis' | 'database' | 'memory';
}

export interface AuthorizationConfig {
  type: 'rbac' | 'abac' | 'custom';
  roles: string[];
  permissions: { [role: string]: string[] };
  policies?: Policy[];
}

export interface Policy {
  effect: 'allow' | 'deny';
  actions: string[];
  resources: string[];
  conditions?: { [key: string]: any };
}

export interface SecurityConfig {
  rateLimit: { [category: string]: RateLimitConfig };
  sessionTimeout: string;
  maxLoginAttempts: number;
  lockoutDuration: string;
}

export interface RateLimitConfig {
  requests: number;
  window: string;
}

export interface RegistrationConfig {
  requireApproval: boolean;
  requireEmailVerification: boolean;
  allowedDomains: string[];
}

export interface MultiTenancyConfig {
  enabled: boolean;
  tenantField?: string;
}

export interface AuthPlugin {
  name: string;
  authenticate(credentials: any): Promise<any>;
  validate?(token: string): Promise<any>;
}
