/**
 * Auth AST Types
 * 
 * TypeScript types for Auth Specification Abstract Syntax Tree
 */

export interface AuthSpec {
  userModel: UserModel;
  authMethods: AuthMethods;
  tokenConfig: TokenConfig;
  protectedEndpoints: ProtectedEndpoint[];
  publicEndpoints: PublicEndpoint[];
  features: Features;
  securitySettings: SecuritySettings;
  businessRules: BusinessRules;
  errorResponses: ErrorResponse[];
}

export interface UserModel {
  fields: UserField[];
  indexes: Index[];
}

export interface UserField {
  name: string;
  type: string;  // 'string', 'number', 'boolean', 'datetime', 'enum'
  constraints: FieldConstraint[];
  enumValues?: string[];  // For enum type
}

export interface FieldConstraint {
  type: string;  // 'required', 'unique', 'max', 'min', 'default', 'auto', 'hashed', 'primary key'
  value?: any;
}

export interface Index {
  fields: string[];
  unique: boolean;
}

export interface AuthMethods {
  password: boolean;
  oauth?: OAuthConfig;
  sso?: SSOConfig;
  twoFactor?: TwoFactorConfig;
}

export interface OAuthConfig {
  enabled: boolean;
  providers: string[];  // 'google', 'github', 'facebook', etc.
}

export interface SSOConfig {
  enabled: boolean;
  provider?: string;  // 'okta', 'auth0', 'azure', etc.
}

export interface TwoFactorConfig {
  enabled: boolean;
  required: boolean;
  methods: string[];  // 'totp', 'sms', 'email'
}

export interface TokenConfig {
  accessToken: TokenSettings;
  refreshToken: TokenSettings;
  algorithm: string;  // 'RS256', 'HS256', etc.
}

export interface TokenSettings {
  expiresIn: string;  // '15m', '7d', etc.
  rotation?: boolean;
}

export interface ProtectedEndpoint {
  method: string;  // 'GET', 'POST', 'PUT', 'DELETE'
  path: string;
  authRequired: boolean;
  role?: string;
  ownerOnly?: boolean;
}

export interface PublicEndpoint {
  method: string;
  path: string;
  description: string;
  category: string;  // 'authentication', 'user-profile', etc.
}

export interface Features {
  emailVerification: boolean;
  passwordReset: boolean;
  rateLimit: RateLimitConfig;
  sessionManagement: string;  // 'jwt', 'session', 'hybrid'
  tokenBlacklist: TokenBlacklistConfig;
}

export interface RateLimitConfig {
  enabled: boolean;
  limits: { [endpoint: string]: RateLimit };
}

export interface RateLimit {
  requests: number;
  window: string;  // '1m', '1h', etc.
}

export interface TokenBlacklistConfig {
  enabled: boolean;
  storage: string;  // 'redis', 'database', 'memory'
}

export interface SecuritySettings {
  passwordRequirements: PasswordRequirements;
  rateLimits: { [category: string]: RateLimit };
  accountSecurity: AccountSecurity;
}

export interface PasswordRequirements {
  minLength: number;
  requireUppercase: boolean;
  requireLowercase: boolean;
  requireNumber: boolean;
  requireSpecial: boolean;
}

export interface AccountSecurity {
  maxLoginAttempts: number;
  lockoutWindow: string;  // '15m', '30m', etc.
  lockoutDuration: string;
  passwordResetTokenExpiry: string;
  emailVerificationTokenExpiry: string;
}

export interface BusinessRules {
  registration: RegistrationRules;
  login: LoginRules;
  tokenRefresh: TokenRefreshRules;
  passwordReset: PasswordResetRules;
  authorization: AuthorizationRules;
}

export interface RegistrationRules {
  emailMustBeUnique: boolean;
  passwordRequirements: string;
  defaultRole: string;
  emailVerificationRequired: boolean;
}

export interface LoginRules {
  emailAndPasswordRequired: boolean;
  accountMustBeActive: boolean;
  failedAttemptsTracked: boolean;
  resetFailedAttemptsOnSuccess: boolean;
}

export interface TokenRefreshRules {
  refreshTokenMustBeValid: boolean;
  issueNewTokens: boolean;
  invalidateOldRefreshToken: boolean;
}

export interface PasswordResetRules {
  resetTokenSentToEmail: boolean;
  tokenValidDuration: string;
  oldPasswordNotRequired: boolean;
  invalidateAllSessionsAfterReset: boolean;
}

export interface AuthorizationRules {
  userCanOnlyAccessOwn: boolean;
  adminCanAccessAll: boolean;
  adminCanDeleteAny: boolean;
  userCanOnlyDeleteOwn: boolean;
}

export interface ErrorResponse {
  statusCode: number;
  error: string;
  message: string;
  code: string;
  additionalFields?: { [key: string]: any };
}
