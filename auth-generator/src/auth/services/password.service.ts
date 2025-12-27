/**
 * Password Service
 * 
 * Handles password hashing and verification
 */

import bcrypt from 'bcrypt';
import crypto from 'crypto';

export interface PasswordRequirements {
  minLength: number;
  requireUppercase: boolean;
  requireLowercase: boolean;
  requireNumber: boolean;
  requireSpecial: boolean;
}

export class PasswordService {
  private saltRounds: number;
  private requirements: PasswordRequirements;

  constructor(requirements: PasswordRequirements, saltRounds: number = 10) {
    this.requirements = requirements;
    this.saltRounds = saltRounds;
  }

  /**
   * Hash password using bcrypt
   */
  async hashPassword(password: string): Promise<string> {
    return bcrypt.hash(password, this.saltRounds);
  }

  /**
   * Verify password against hash
   */
  async verifyPassword(password: string, hash: string): Promise<boolean> {
    return bcrypt.compare(password, hash);
  }

  /**
   * Validate password against requirements
   */
  validatePassword(password: string): { valid: boolean; errors: string[] } {
    const errors: string[] = [];

    if (password.length < this.requirements.minLength) {
      errors.push(`Password must be at least ${this.requirements.minLength} characters long`);
    }

    if (this.requirements.requireUppercase && !/[A-Z]/.test(password)) {
      errors.push('Password must contain at least one uppercase letter');
    }

    if (this.requirements.requireLowercase && !/[a-z]/.test(password)) {
      errors.push('Password must contain at least one lowercase letter');
    }

    if (this.requirements.requireNumber && !/\d/.test(password)) {
      errors.push('Password must contain at least one number');
    }

    if (this.requirements.requireSpecial && !/[!@#$%^&*(),.?":{}|<>]/.test(password)) {
      errors.push('Password must contain at least one special character');
    }

    return {
      valid: errors.length === 0,
      errors,
    };
  }

  /**
   * Generate random password
   */
  generateRandomPassword(length: number = 16): string {
    const uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
    const lowercase = 'abcdefghijklmnopqrstuvwxyz';
    const numbers = '0123456789';
    const special = '!@#$%^&*(),.?":{}|<>';
    
    let charset = '';
    let password = '';
    
    // Ensure at least one character from each required set
    if (this.requirements.requireUppercase) {
      charset += uppercase;
      password += uppercase[Math.floor(Math.random() * uppercase.length)];
    }
    
    if (this.requirements.requireLowercase) {
      charset += lowercase;
      password += lowercase[Math.floor(Math.random() * lowercase.length)];
    }
    
    if (this.requirements.requireNumber) {
      charset += numbers;
      password += numbers[Math.floor(Math.random() * numbers.length)];
    }
    
    if (this.requirements.requireSpecial) {
      charset += special;
      password += special[Math.floor(Math.random() * special.length)];
    }
    
    // Fill remaining length
    for (let i = password.length; i < length; i++) {
      password += charset[Math.floor(Math.random() * charset.length)];
    }
    
    // Shuffle password
    return password.split('').sort(() => Math.random() - 0.5).join('');
  }

  /**
   * Generate password reset token
   */
  generateResetToken(): string {
    return crypto.randomBytes(32).toString('hex');
  }

  /**
   * Generate email verification token
   */
  generateVerificationToken(): string {
    return crypto.randomBytes(32).toString('hex');
  }

  /**
   * Hash token for storage
   */
  hashToken(token: string): string {
    return crypto.createHash('sha256').update(token).digest('hex');
  }

  /**
   * Calculate password strength (0-100)
   */
  calculateStrength(password: string): number {
    let strength = 0;
    
    // Length
    if (password.length >= 8) strength += 20;
    if (password.length >= 12) strength += 10;
    if (password.length >= 16) strength += 10;
    
    // Character types
    if (/[a-z]/.test(password)) strength += 15;
    if (/[A-Z]/.test(password)) strength += 15;
    if (/\d/.test(password)) strength += 15;
    if (/[!@#$%^&*(),.?":{}|<>]/.test(password)) strength += 15;
    
    return Math.min(strength, 100);
  }
}
