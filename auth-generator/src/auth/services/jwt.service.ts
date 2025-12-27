/**
 * JWT Service
 * 
 * Handles JWT token generation and verification
 */

import jwt from 'jsonwebtoken';
import { TokenConfig } from '../../types/auth-ast.types';

export interface JWTPayload {
  userId: string;
  email: string;
  role: string;
  [key: string]: any;
}

export interface TokenPair {
  accessToken: string;
  refreshToken: string;
}

export class JWTService {
  private accessTokenSecret: string;
  private refreshTokenSecret: string;
  private config: TokenConfig;

  constructor(config: TokenConfig, accessSecret: string, refreshSecret: string) {
    this.config = config;
    this.accessTokenSecret = accessSecret;
    this.refreshTokenSecret = refreshSecret;
  }

  /**
   * Generate access and refresh tokens
   */
  generateTokenPair(payload: JWTPayload): TokenPair {
    const accessToken = this.generateAccessToken(payload);
    const refreshToken = this.generateRefreshToken(payload);
    
    return { accessToken, refreshToken };
  }

  /**
   * Generate access token
   */
  generateAccessToken(payload: JWTPayload): string {
    return jwt.sign(
      payload,
      this.accessTokenSecret,
      {
        expiresIn: this.config.accessToken.expiresIn,
        algorithm: this.config.algorithm as jwt.Algorithm,
      }
    );
  }

  /**
   * Generate refresh token
   */
  generateRefreshToken(payload: JWTPayload): string {
    return jwt.sign(
      { userId: payload.userId },
      this.refreshTokenSecret,
      {
        expiresIn: this.config.refreshToken.expiresIn,
        algorithm: this.config.algorithm as jwt.Algorithm,
      }
    );
  }

  /**
   * Verify access token
   */
  verifyAccessToken(token: string): JWTPayload {
    try {
      const decoded = jwt.verify(token, this.accessTokenSecret, {
        algorithms: [this.config.algorithm as jwt.Algorithm],
      });
      
      return decoded as JWTPayload;
    } catch (error) {
      throw new Error('Invalid or expired access token');
    }
  }

  /**
   * Verify refresh token
   */
  verifyRefreshToken(token: string): { userId: string } {
    try {
      const decoded = jwt.verify(token, this.refreshTokenSecret, {
        algorithms: [this.config.algorithm as jwt.Algorithm],
      });
      
      return decoded as { userId: string };
    } catch (error) {
      throw new Error('Invalid or expired refresh token');
    }
  }

  /**
   * Decode token without verification (for debugging)
   */
  decode(token: string): any {
    return jwt.decode(token);
  }

  /**
   * Get token expiry time
   */
  getTokenExpiry(token: string): number | null {
    const decoded = this.decode(token);
    return decoded?.exp || null;
  }

  /**
   * Check if token is expired
   */
  isTokenExpired(token: string): boolean {
    const expiry = this.getTokenExpiry(token);
    if (!expiry) return true;
    
    return Date.now() >= expiry * 1000;
  }
}
