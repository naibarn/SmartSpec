/**
 * Auth Service
 * 
 * Main authentication service that coordinates JWT and Password services
 */

import { JWTService, JWTPayload, TokenPair } from './jwt.service';
import { PasswordService } from './password.service';

export interface User {
  id: string;
  email: string;
  password: string;
  role: string;
  isActive: boolean;
  isEmailVerified: boolean;
  emailVerificationToken?: string;
  passwordResetToken?: string;
  passwordResetExpires?: Date;
  failedLoginAttempts: number;
  lockedUntil?: Date;
  createdAt: Date;
  updatedAt: Date;
}

export interface RegisterInput {
  email: string;
  password: string;
  name?: string;
}

export interface LoginInput {
  email: string;
  password: string;
}

export interface AuthResult {
  user: Omit<User, 'password'>;
  tokens: TokenPair;
}

export class AuthService {
  private jwtService: JWTService;
  private passwordService: PasswordService;
  private maxLoginAttempts: number;
  private lockoutDuration: number; // in minutes

  constructor(
    jwtService: JWTService,
    passwordService: PasswordService,
    maxLoginAttempts: number = 5,
    lockoutDuration: number = 30
  ) {
    this.jwtService = jwtService;
    this.passwordService = passwordService;
    this.maxLoginAttempts = maxLoginAttempts;
    this.lockoutDuration = lockoutDuration;
  }

  /**
   * Register new user
   */
  async register(input: RegisterInput): Promise<AuthResult> {
    // Validate password
    const validation = this.passwordService.validatePassword(input.password);
    if (!validation.valid) {
      throw new Error(validation.errors.join(', '));
    }

    // Hash password
    const hashedPassword = await this.passwordService.hashPassword(input.password);

    // Generate verification token
    const verificationToken = this.passwordService.generateVerificationToken();
    const hashedVerificationToken = this.passwordService.hashToken(verificationToken);

    // Create user (this would be done by the database layer)
    const user: User = {
      id: this.generateId(),
      email: input.email,
      password: hashedPassword,
      role: 'user',
      isActive: true,
      isEmailVerified: false,
      emailVerificationToken: hashedVerificationToken,
      failedLoginAttempts: 0,
      createdAt: new Date(),
      updatedAt: new Date(),
    };

    // Generate tokens
    const tokens = this.jwtService.generateTokenPair({
      userId: user.id,
      email: user.email,
      role: user.role,
    });

    // Return user without password
    const { password, ...userWithoutPassword } = user;

    return {
      user: userWithoutPassword,
      tokens,
    };
  }

  /**
   * Login user
   */
  async login(input: LoginInput, user: User): Promise<AuthResult> {
    // Check if account is locked
    if (user.lockedUntil && user.lockedUntil > new Date()) {
      const minutesLeft = Math.ceil((user.lockedUntil.getTime() - Date.now()) / 60000);
      throw new Error(`Account is locked. Try again in ${minutesLeft} minutes`);
    }

    // Check if account is active
    if (!user.isActive) {
      throw new Error('Account is not active');
    }

    // Verify password
    const isPasswordValid = await this.passwordService.verifyPassword(
      input.password,
      user.password
    );

    if (!isPasswordValid) {
      // Increment failed attempts
      user.failedLoginAttempts += 1;

      // Lock account if max attempts reached
      if (user.failedLoginAttempts >= this.maxLoginAttempts) {
        user.lockedUntil = new Date(Date.now() + this.lockoutDuration * 60000);
        throw new Error('Too many failed login attempts. Account is locked');
      }

      throw new Error('Invalid credentials');
    }

    // Reset failed attempts on successful login
    user.failedLoginAttempts = 0;
    user.lockedUntil = undefined;

    // Generate tokens
    const tokens = this.jwtService.generateTokenPair({
      userId: user.id,
      email: user.email,
      role: user.role,
    });

    // Return user without password
    const { password, ...userWithoutPassword } = user;

    return {
      user: userWithoutPassword,
      tokens,
    };
  }

  /**
   * Refresh tokens
   */
  async refreshTokens(refreshToken: string, user: User): Promise<TokenPair> {
    // Verify refresh token
    const decoded = this.jwtService.verifyRefreshToken(refreshToken);

    // Check if user ID matches
    if (decoded.userId !== user.id) {
      throw new Error('Invalid refresh token');
    }

    // Generate new tokens
    return this.jwtService.generateTokenPair({
      userId: user.id,
      email: user.email,
      role: user.role,
    });
  }

  /**
   * Verify email
   */
  async verifyEmail(token: string, user: User): Promise<boolean> {
    const hashedToken = this.passwordService.hashToken(token);

    if (user.emailVerificationToken !== hashedToken) {
      throw new Error('Invalid verification token');
    }

    // Mark email as verified
    user.isEmailVerified = true;
    user.emailVerificationToken = undefined;

    return true;
  }

  /**
   * Request password reset
   */
  async requestPasswordReset(email: string): Promise<string> {
    // Generate reset token
    const resetToken = this.passwordService.generateResetToken();
    const hashedToken = this.passwordService.hashToken(resetToken);

    // Set expiry (1 hour)
    const expires = new Date(Date.now() + 60 * 60 * 1000);

    // Store hashed token and expiry in user record
    // (this would be done by the database layer)

    return resetToken; // Send this via email
  }

  /**
   * Reset password
   */
  async resetPassword(token: string, newPassword: string, user: User): Promise<boolean> {
    // Validate new password
    const validation = this.passwordService.validatePassword(newPassword);
    if (!validation.valid) {
      throw new Error(validation.errors.join(', '));
    }

    // Verify token
    const hashedToken = this.passwordService.hashToken(token);
    if (user.passwordResetToken !== hashedToken) {
      throw new Error('Invalid reset token');
    }

    // Check if token is expired
    if (user.passwordResetExpires && user.passwordResetExpires < new Date()) {
      throw new Error('Reset token has expired');
    }

    // Hash new password
    const hashedPassword = await this.passwordService.hashPassword(newPassword);

    // Update user
    user.password = hashedPassword;
    user.passwordResetToken = undefined;
    user.passwordResetExpires = undefined;

    return true;
  }

  /**
   * Change password (when user is logged in)
   */
  async changePassword(
    user: User,
    currentPassword: string,
    newPassword: string
  ): Promise<boolean> {
    // Verify current password
    const isPasswordValid = await this.passwordService.verifyPassword(
      currentPassword,
      user.password
    );

    if (!isPasswordValid) {
      throw new Error('Current password is incorrect');
    }

    // Validate new password
    const validation = this.passwordService.validatePassword(newPassword);
    if (!validation.valid) {
      throw new Error(validation.errors.join(', '));
    }

    // Hash new password
    const hashedPassword = await this.passwordService.hashPassword(newPassword);

    // Update user
    user.password = hashedPassword;

    return true;
  }

  /**
   * Verify access token
   */
  verifyAccessToken(token: string): JWTPayload {
    return this.jwtService.verifyAccessToken(token);
  }

  /**
   * Generate random ID (placeholder - use UUID in production)
   */
  private generateId(): string {
    return Math.random().toString(36).substring(2, 15);
  }
}
