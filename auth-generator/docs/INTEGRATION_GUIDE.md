# Integration Guide

**Version:** 1.0.0  
**Last Updated:** December 27, 2025

Complete guide for integrating generated authentication code with databases, email services, and deployment platforms.

---

## Table of Contents

1. [Database Integration](#1-database-integration)
2. [Email Service Integration](#2-email-service-integration)
3. [Storage Integration](#3-storage-integration)
4. [Environment Configuration](#4-environment-configuration)
5. [Deployment](#5-deployment)
6. [Monitoring & Logging](#6-monitoring--logging)
7. [Testing Integration](#7-testing-integration)

---

## 1. Database Integration

### 1.1 PostgreSQL with Prisma

**Step 1: Install Dependencies**

```bash
npm install @prisma/client
npm install -D prisma
```

**Step 2: Initialize Prisma**

```bash
npx prisma init
```

**Step 3: Define Schema**

```prisma
// prisma/schema.prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

model User {
  id        String   @id @default(uuid())
  email     String   @unique
  password  String
  role      String   @default("user")
  
  // Email verification
  emailVerified             Boolean   @default(false)
  emailVerificationToken    String?   @unique
  emailVerificationExpires  DateTime?
  
  // Password reset
  resetPasswordToken        String?   @unique
  resetPasswordExpires      DateTime?
  
  // Account lockout
  failedLoginAttempts       Int       @default(0)
  lockedUntil              DateTime?
  
  // Timestamps
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
  
  @@index([email])
  @@index([emailVerificationToken])
  @@index([resetPasswordToken])
}

model RefreshToken {
  id        String   @id @default(uuid())
  token     String   @unique
  userId    String
  expiresAt DateTime
  createdAt DateTime @default(now())
  
  @@index([token])
  @@index([userId])
}
```

**Step 4: Generate Client**

```bash
npx prisma generate
npx prisma db push
```

**Step 5: Extend Auth Service**

```typescript
// src/auth/services/auth.service.extended.ts
import { PrismaClient } from '@prisma/client';
import { AuthService } from './auth.service';
import { RegisterInput, LoginInput, TokenPair } from '../types/auth.types';
import * as bcrypt from 'bcrypt';
import * as jwt from 'jsonwebtoken';

export class AuthServiceWithDB extends AuthService {
  private prisma: PrismaClient;

  constructor() {
    super();
    this.prisma = new PrismaClient();
  }

  async register(input: RegisterInput): Promise<TokenPair> {
    // Check if user exists
    const existing = await this.prisma.user.findUnique({
      where: { email: input.email }
    });

    if (existing) {
      throw new Error('User already exists');
    }

    // Hash password
    const hashedPassword = await bcrypt.hash(input.password, 10);

    // Create user
    const user = await this.prisma.user.create({
      data: {
        email: input.email,
        password: hashedPassword,
        role: 'user',
        emailVerificationToken: this.generateToken(),
        emailVerificationExpires: new Date(Date.now() + 24 * 60 * 60 * 1000)
      }
    });

    // Generate tokens
    const tokens = this.generateTokens(user.id, user.email, user.role);

    // Store refresh token
    await this.prisma.refreshToken.create({
      data: {
        token: tokens.refreshToken,
        userId: user.id,
        expiresAt: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000)
      }
    });

    return tokens;
  }

  async login(input: LoginInput): Promise<TokenPair> {
    // Find user
    const user = await this.prisma.user.findUnique({
      where: { email: input.email }
    });

    if (!user) {
      throw new Error('Invalid credentials');
    }

    // Check account lockout
    if (user.lockedUntil && user.lockedUntil > new Date()) {
      throw new Error('Account is locked');
    }

    // Verify password
    const valid = await bcrypt.compare(input.password, user.password);

    if (!valid) {
      // Increment failed attempts
      await this.prisma.user.update({
        where: { id: user.id },
        data: {
          failedLoginAttempts: user.failedLoginAttempts + 1,
          lockedUntil: user.failedLoginAttempts + 1 >= 5
            ? new Date(Date.now() + 15 * 60 * 1000)
            : null
        }
      });

      throw new Error('Invalid credentials');
    }

    // Reset failed attempts
    await this.prisma.user.update({
      where: { id: user.id },
      data: {
        failedLoginAttempts: 0,
        lockedUntil: null
      }
    });

    // Generate tokens
    const tokens = this.generateTokens(user.id, user.email, user.role);

    // Store refresh token
    await this.prisma.refreshToken.create({
      data: {
        token: tokens.refreshToken,
        userId: user.id,
        expiresAt: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000)
      }
    });

    return tokens;
  }

  async verifyEmail(token: string): Promise<void> {
    const user = await this.prisma.user.findFirst({
      where: {
        emailVerificationToken: token,
        emailVerificationExpires: { gt: new Date() }
      }
    });

    if (!user) {
      throw new Error('Invalid or expired token');
    }

    await this.prisma.user.update({
      where: { id: user.id },
      data: {
        emailVerified: true,
        emailVerificationToken: null,
        emailVerificationExpires: null
      }
    });
  }

  private generateToken(): string {
    return Math.random().toString(36).substring(2) + Date.now().toString(36);
  }

  private generateTokens(userId: string, email: string, role: string): TokenPair {
    const accessToken = jwt.sign(
      { userId, email, role, type: 'access' },
      process.env.JWT_SECRET!,
      { expiresIn: '15m' }
    );

    const refreshToken = jwt.sign(
      { userId, email, role, type: 'refresh' },
      process.env.JWT_SECRET!,
      { expiresIn: '7d' }
    );

    return {
      accessToken,
      refreshToken,
      expiresIn: 900 // 15 minutes in seconds
    };
  }
}
```

### 1.2 MongoDB with Mongoose

**Step 1: Install Dependencies**

```bash
npm install mongoose
npm install -D @types/mongoose
```

**Step 2: Define Schema**

```typescript
// src/auth/models/user.model.ts
import mongoose, { Schema, Document } from 'mongoose';

export interface IUser extends Document {
  email: string;
  password: string;
  role: string;
  emailVerified: boolean;
  emailVerificationToken?: string;
  emailVerificationExpires?: Date;
  resetPasswordToken?: string;
  resetPasswordExpires?: Date;
  failedLoginAttempts: number;
  lockedUntil?: Date;
  createdAt: Date;
  updatedAt: Date;
}

const UserSchema = new Schema<IUser>({
  email: {
    type: String,
    required: true,
    unique: true,
    lowercase: true,
    trim: true
  },
  password: {
    type: String,
    required: true
  },
  role: {
    type: String,
    enum: ['user', 'admin'],
    default: 'user'
  },
  emailVerified: {
    type: Boolean,
    default: false
  },
  emailVerificationToken: String,
  emailVerificationExpires: Date,
  resetPasswordToken: String,
  resetPasswordExpires: Date,
  failedLoginAttempts: {
    type: Number,
    default: 0
  },
  lockedUntil: Date
}, {
  timestamps: true
});

// Indexes
UserSchema.index({ email: 1 });
UserSchema.index({ emailVerificationToken: 1 });
UserSchema.index({ resetPasswordToken: 1 });

export const User = mongoose.model<IUser>('User', UserSchema);
```

**Step 3: Connect to Database**

```typescript
// src/config/database.ts
import mongoose from 'mongoose';

export async function connectDatabase() {
  try {
    await mongoose.connect(process.env.MONGODB_URI!);
    console.log('✓ Connected to MongoDB');
  } catch (error) {
    console.error('✗ MongoDB connection error:', error);
    process.exit(1);
  }
}
```

**Step 4: Use in Auth Service**

```typescript
import { User } from '../models/user.model';

export class AuthServiceWithMongo extends AuthService {
  async register(input: RegisterInput): Promise<TokenPair> {
    const existing = await User.findOne({ email: input.email });
    if (existing) {
      throw new Error('User already exists');
    }

    const user = await User.create({
      email: input.email,
      password: await bcrypt.hash(input.password, 10),
      emailVerificationToken: this.generateToken(),
      emailVerificationExpires: new Date(Date.now() + 24 * 60 * 60 * 1000)
    });

    return this.generateTokens(user.id, user.email, user.role);
  }

  async login(input: LoginInput): Promise<TokenPair> {
    const user = await User.findOne({ email: input.email });
    if (!user) {
      throw new Error('Invalid credentials');
    }

    // Check lockout
    if (user.lockedUntil && user.lockedUntil > new Date()) {
      throw new Error('Account is locked');
    }

    // Verify password
    const valid = await bcrypt.compare(input.password, user.password);
    if (!valid) {
      user.failedLoginAttempts += 1;
      if (user.failedLoginAttempts >= 5) {
        user.lockedUntil = new Date(Date.now() + 15 * 60 * 1000);
      }
      await user.save();
      throw new Error('Invalid credentials');
    }

    // Reset failed attempts
    user.failedLoginAttempts = 0;
    user.lockedUntil = undefined;
    await user.save();

    return this.generateTokens(user.id, user.email, user.role);
  }
}
```

### 1.3 MySQL with TypeORM

**Step 1: Install Dependencies**

```bash
npm install typeorm mysql2 reflect-metadata
```

**Step 2: Define Entity**

```typescript
// src/auth/entities/user.entity.ts
import { Entity, PrimaryGeneratedColumn, Column, CreateDateColumn, UpdateDateColumn, Index } from 'typeorm';

@Entity('users')
export class User {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @Column({ unique: true })
  @Index()
  email: string;

  @Column()
  password: string;

  @Column({ default: 'user' })
  role: string;

  @Column({ default: false })
  emailVerified: boolean;

  @Column({ nullable: true })
  @Index()
  emailVerificationToken?: string;

  @Column({ nullable: true })
  emailVerificationExpires?: Date;

  @Column({ nullable: true })
  @Index()
  resetPasswordToken?: string;

  @Column({ nullable: true })
  resetPasswordExpires?: Date;

  @Column({ default: 0 })
  failedLoginAttempts: number;

  @Column({ nullable: true })
  lockedUntil?: Date;

  @CreateDateColumn()
  createdAt: Date;

  @UpdateDateColumn()
  updatedAt: Date;
}
```

**Step 3: Configure TypeORM**

```typescript
// src/config/database.ts
import { DataSource } from 'typeorm';
import { User } from '../auth/entities/user.entity';

export const AppDataSource = new DataSource({
  type: 'mysql',
  host: process.env.DB_HOST,
  port: parseInt(process.env.DB_PORT || '3306'),
  username: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  database: process.env.DB_NAME,
  entities: [User],
  synchronize: process.env.NODE_ENV === 'development',
  logging: process.env.NODE_ENV === 'development'
});
```

**Step 4: Use in Auth Service**

```typescript
import { AppDataSource } from '../../config/database';
import { User } from '../entities/user.entity';

export class AuthServiceWithTypeORM extends AuthService {
  private userRepository = AppDataSource.getRepository(User);

  async register(input: RegisterInput): Promise<TokenPair> {
    const existing = await this.userRepository.findOne({
      where: { email: input.email }
    });

    if (existing) {
      throw new Error('User already exists');
    }

    const user = this.userRepository.create({
      email: input.email,
      password: await bcrypt.hash(input.password, 10),
      emailVerificationToken: this.generateToken(),
      emailVerificationExpires: new Date(Date.now() + 24 * 60 * 60 * 1000)
    });

    await this.userRepository.save(user);

    return this.generateTokens(user.id, user.email, user.role);
  }
}
```

---

## 2. Email Service Integration

### 2.1 SendGrid

**Step 1: Install SDK**

```bash
npm install @sendgrid/mail
```

**Step 2: Create Email Service**

```typescript
// src/services/email.service.ts
import sgMail from '@sendgrid/mail';

sgMail.setApiKey(process.env.SENDGRID_API_KEY!);

export class EmailService {
  async sendVerificationEmail(email: string, token: string): Promise<void> {
    const verificationUrl = `${process.env.APP_URL}/auth/verify-email/${token}`;

    await sgMail.send({
      to: email,
      from: process.env.FROM_EMAIL!,
      subject: 'Verify your email address',
      html: `
        <h1>Email Verification</h1>
        <p>Click the link below to verify your email address:</p>
        <a href="${verificationUrl}">${verificationUrl}</a>
        <p>This link will expire in 24 hours.</p>
      `
    });
  }

  async sendPasswordResetEmail(email: string, token: string): Promise<void> {
    const resetUrl = `${process.env.APP_URL}/auth/reset-password/${token}`;

    await sgMail.send({
      to: email,
      from: process.env.FROM_EMAIL!,
      subject: 'Reset your password',
      html: `
        <h1>Password Reset</h1>
        <p>Click the link below to reset your password:</p>
        <a href="${resetUrl}">${resetUrl}</a>
        <p>This link will expire in 30 minutes.</p>
        <p>If you didn't request this, please ignore this email.</p>
      `
    });
  }
}
```

**Step 3: Integrate with Auth Service**

```typescript
import { EmailService } from '../../services/email.service';

export class AuthServiceWithEmail extends AuthServiceWithDB {
  private emailService = new EmailService();

  async register(input: RegisterInput): Promise<TokenPair> {
    const result = await super.register(input);

    // Send verification email
    const user = await this.prisma.user.findUnique({
      where: { email: input.email }
    });

    if (user?.emailVerificationToken) {
      await this.emailService.sendVerificationEmail(
        user.email,
        user.emailVerificationToken
      );
    }

    return result;
  }

  async requestPasswordReset(email: string): Promise<void> {
    const user = await this.prisma.user.findUnique({
      where: { email }
    });

    if (!user) {
      // Don't reveal if user exists
      return;
    }

    const token = this.generateToken();

    await this.prisma.user.update({
      where: { id: user.id },
      data: {
        resetPasswordToken: token,
        resetPasswordExpires: new Date(Date.now() + 30 * 60 * 1000)
      }
    });

    await this.emailService.sendPasswordResetEmail(email, token);
  }
}
```

### 2.2 Nodemailer (SMTP)

**Step 1: Install Nodemailer**

```bash
npm install nodemailer
npm install -D @types/nodemailer
```

**Step 2: Create Email Service**

```typescript
import nodemailer from 'nodemailer';

export class EmailService {
  private transporter = nodemailer.createTransporter({
    host: process.env.SMTP_HOST,
    port: parseInt(process.env.SMTP_PORT || '587'),
    secure: process.env.SMTP_SECURE === 'true',
    auth: {
      user: process.env.SMTP_USER,
      pass: process.env.SMTP_PASSWORD
    }
  });

  async sendVerificationEmail(email: string, token: string): Promise<void> {
    const verificationUrl = `${process.env.APP_URL}/auth/verify-email/${token}`;

    await this.transporter.sendMail({
      from: process.env.FROM_EMAIL,
      to: email,
      subject: 'Verify your email address',
      html: `
        <h1>Email Verification</h1>
        <p>Click the link below to verify your email address:</p>
        <a href="${verificationUrl}">${verificationUrl}</a>
      `
    });
  }
}
```

### 2.3 AWS SES

**Step 1: Install AWS SDK**

```bash
npm install @aws-sdk/client-ses
```

**Step 2: Create Email Service**

```typescript
import { SESClient, SendEmailCommand } from '@aws-sdk/client-ses';

export class EmailService {
  private ses = new SESClient({
    region: process.env.AWS_REGION,
    credentials: {
      accessKeyId: process.env.AWS_ACCESS_KEY_ID!,
      secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY!
    }
  });

  async sendVerificationEmail(email: string, token: string): Promise<void> {
    const verificationUrl = `${process.env.APP_URL}/auth/verify-email/${token}`;

    const command = new SendEmailCommand({
      Source: process.env.FROM_EMAIL,
      Destination: { ToAddresses: [email] },
      Message: {
        Subject: { Data: 'Verify your email address' },
        Body: {
          Html: {
            Data: `
              <h1>Email Verification</h1>
              <p>Click the link below to verify your email address:</p>
              <a href="${verificationUrl}">${verificationUrl}</a>
            `
          }
        }
      }
    });

    await this.ses.send(command);
  }
}
```

---

## 3. Storage Integration

### 3.1 Redis for Token Blacklist

**Step 1: Install Redis Client**

```bash
npm install redis
```

**Step 2: Create Redis Service**

```typescript
// src/services/redis.service.ts
import { createClient } from 'redis';

export class RedisService {
  private client = createClient({
    url: process.env.REDIS_URL
  });

  async connect() {
    await this.client.connect();
  }

  async blacklistToken(token: string, expiresIn: number): Promise<void> {
    await this.client.setEx(`blacklist:${token}`, expiresIn, '1');
  }

  async isTokenBlacklisted(token: string): Promise<boolean> {
    const result = await this.client.get(`blacklist:${token}`);
    return result !== null;
  }
}
```

**Step 3: Integrate with Middleware**

```typescript
import { RedisService } from '../../services/redis.service';

export class AuthMiddlewareWithRedis extends AuthMiddleware {
  private redis = new RedisService();

  async authenticate() {
    return async (req: Request, res: Response, next: NextFunction) => {
      const token = this.extractToken(req);

      if (!token) {
        return res.status(401).json({ error: 'No token provided' });
      }

      // Check blacklist
      const blacklisted = await this.redis.isTokenBlacklisted(token);
      if (blacklisted) {
        return res.status(401).json({ error: 'Token has been revoked' });
      }

      // Verify token
      try {
        const payload = jwt.verify(token, process.env.JWT_SECRET!);
        req.user = payload;
        next();
      } catch (error) {
        return res.status(401).json({ error: 'Invalid token' });
      }
    };
  }
}
```

---

## 4. Environment Configuration

### 4.1 Environment Variables

Create `.env` file:

```bash
# Application
NODE_ENV=development
PORT=3000
APP_URL=http://localhost:3000

# Database (PostgreSQL)
DATABASE_URL=postgresql://user:password@localhost:5432/myapp

# JWT
JWT_SECRET=your-secret-key-here
JWT_ACCESS_EXPIRY=15m
JWT_REFRESH_EXPIRY=7d

# Email (SendGrid)
SENDGRID_API_KEY=your-sendgrid-api-key
FROM_EMAIL=noreply@yourapp.com

# Redis
REDIS_URL=redis://localhost:6379

# AWS (if using SES)
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
```

### 4.2 Configuration Management

```typescript
// src/config/index.ts
import dotenv from 'dotenv';

dotenv.config();

export const config = {
  env: process.env.NODE_ENV || 'development',
  port: parseInt(process.env.PORT || '3000'),
  appUrl: process.env.APP_URL!,
  
  database: {
    url: process.env.DATABASE_URL!
  },
  
  jwt: {
    secret: process.env.JWT_SECRET!,
    accessExpiry: process.env.JWT_ACCESS_EXPIRY || '15m',
    refreshExpiry: process.env.JWT_REFRESH_EXPIRY || '7d'
  },
  
  email: {
    sendgridApiKey: process.env.SENDGRID_API_KEY,
    fromEmail: process.env.FROM_EMAIL!
  },
  
  redis: {
    url: process.env.REDIS_URL || 'redis://localhost:6379'
  }
};

// Validate required config
const required = ['JWT_SECRET', 'DATABASE_URL', 'FROM_EMAIL'];
for (const key of required) {
  if (!process.env[key]) {
    throw new Error(`Missing required environment variable: ${key}`);
  }
}
```

---

## 5. Deployment

### 5.1 Docker

**Dockerfile:**

```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

EXPOSE 3000

CMD ["node", "dist/index.js"]
```

**docker-compose.yml:**

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - DATABASE_URL=postgresql://postgres:password@db:5432/myapp
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=myapp
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

### 5.2 Vercel

**vercel.json:**

```json
{
  "version": 2,
  "builds": [
    {
      "src": "dist/index.js",
      "use": "@vercel/node"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "dist/index.js"
    }
  ],
  "env": {
    "NODE_ENV": "production"
  }
}
```

### 5.3 AWS Elastic Beanstalk

**.ebextensions/nodecommand.config:**

```yaml
option_settings:
  aws:elasticbeanstalk:container:nodejs:
    NodeCommand: "npm start"
  aws:elasticbeanstalk:application:environment:
    NODE_ENV: production
```

---

## 6. Monitoring & Logging

### 6.1 Winston Logger

```typescript
import winston from 'winston';

export const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: winston.format.json(),
  transports: [
    new winston.transports.File({ filename: 'error.log', level: 'error' }),
    new winston.transports.File({ filename: 'combined.log' })
  ]
});

if (process.env.NODE_ENV !== 'production') {
  logger.add(new winston.transports.Console({
    format: winston.format.simple()
  }));
}
```

### 6.2 Request Logging

```typescript
import morgan from 'morgan';

app.use(morgan('combined', {
  stream: {
    write: (message) => logger.info(message.trim())
  }
}));
```

---

## 7. Testing Integration

### 7.1 Integration Test Setup

```typescript
import { PrismaClient } from '@prisma/client';
import { AuthServiceWithDB } from '../src/auth/services/auth.service.extended';

describe('Auth Integration Tests', () => {
  let prisma: PrismaClient;
  let authService: AuthServiceWithDB;

  beforeAll(async () => {
    prisma = new PrismaClient({
      datasources: {
        db: { url: process.env.TEST_DATABASE_URL }
      }
    });
    authService = new AuthServiceWithDB();
  });

  afterAll(async () => {
    await prisma.$disconnect();
  });

  beforeEach(async () => {
    await prisma.user.deleteMany();
  });

  it('should register and login user', async () => {
    // Register
    const tokens = await authService.register({
      email: 'test@example.com',
      password: 'password123'
    });

    expect(tokens.accessToken).toBeDefined();

    // Login
    const loginTokens = await authService.login({
      email: 'test@example.com',
      password: 'password123'
    });

    expect(loginTokens.accessToken).toBeDefined();
  });
});
```

---

**End of Integration Guide**

For more information, see:
- [API Documentation](./API_DOCUMENTATION.md)
- [Template Usage Guide](./TEMPLATE_GUIDE.md)
