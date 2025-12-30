# SmartSpec Pro - Web Dashboard Development Plan

**Version:** 1.0  
**Date:** 2025-12-30  
**Project:** Web Dashboard Frontend for SmartSpec Pro  
**Domain:** https://smartspecpro.com

---

## Executive Summary

สร้าง Web Dashboard Frontend สำหรับ SmartSpec Pro ที่เชื่อมต่อกับ Backend APIs และ LLM Gateway ที่มีอยู่แล้ว โดยแบ่งการพัฒนาเป็น 10 Phases ชัดเจน แต่ละ Phase จะ commit และ push ไป GitHub

**Tech Stack:**
- React 18 + TypeScript
- Vite (Build Tool)
- Tailwind CSS + shadcn/ui
- React Router v6
- TanStack Query (React Query)
- Axios (HTTP Client)
- React Helmet Async (SEO)

**Backend APIs (มีอยู่แล้ว):**
- `/api/auth/*` - Authentication
- `/api/credits/*` - Credits Management
- `/api/llm/*` - LLM Gateway
- `/api/payments/*` - Payment Processing
- `/api/analytics/*` - Usage Analytics
- `/api/dashboard/*` - Dashboard Data

---

## Development Phases

### Phase 1: Project Setup & Core Structure ✅ COMPLETED

**Duration:** 1 day  
**Status:** ✅ Complete

**Completed:**
- ✅ Vite + React + TypeScript setup
- ✅ Tailwind CSS configuration
- ✅ shadcn/ui installation
- ✅ Project structure creation
- ✅ Path aliases configuration
- ✅ Basic components (Button, Card, Input, Label, Badge)
- ✅ Utility functions (cn)
- ✅ SEO component
- ✅ TypeScript types
- ✅ API service layer
- ✅ Auth context
- ✅ Protected routes
- ✅ App router structure

**Files Created:**
```
web-dashboard/
├── src/
│   ├── components/
│   │   ├── ui/              # shadcn/ui components
│   │   ├── SEO.tsx          # SEO component
│   │   └── ProtectedRoute.tsx
│   ├── contexts/
│   │   └── AuthContext.tsx  # Auth state management
│   ├── services/
│   │   └── api.ts           # API client
│   ├── types/
│   │   └── index.ts         # TypeScript types
│   ├── lib/
│   │   └── utils.ts         # Utility functions
│   ├── pages/
│   │   ├── public/          # Public pages
│   │   ├── auth/            # Auth pages
│   │   └── dashboard/       # Dashboard pages
│   └── App.tsx              # Main app with routing
├── tailwind.config.js
├── components.json
└── package.json
```

**Git Commit:**
```bash
git add .
git commit -m "Phase 1: Project setup and core structure"
git push origin main
```

---

### Phase 2: Authentication System

**Duration:** 2-3 days  
**Status:** 🔄 Next

**Goal:** สร้างระบบ Authentication ที่เชื่อมต่อกับ Backend APIs

**Components to Build:**

#### 1. Login Page (`/login`)
**File:** `src/pages/auth/LoginPage.tsx`

**Features:**
- Email + Password form
- Form validation (React Hook Form + Zod)
- Error handling
- "Remember me" checkbox
- "Forgot password?" link
- "Sign up" link
- Loading states
- Success redirect to dashboard

**API Integration:**
- `POST /api/auth/login`
- Store JWT token in localStorage
- Update Auth context

**UI Design:**
```
┌─────────────────────────────────────┐
│                                     │
│  [SmartSpec Pro Logo]               │
│                                     │
│  Welcome Back                       │
│  Sign in to your account            │
│                                     │
│  Email                              │
│  [___________________________]      │
│                                     │
│  Password                           │
│  [___________________________]      │
│                                     │
│  [✓] Remember me   Forgot password? │
│                                     │
│  [Sign In]                          │
│                                     │
│  Don't have an account? Sign up     │
│                                     │
└─────────────────────────────────────┘
```

#### 2. Register Page (`/register`)
**File:** `src/pages/auth/RegisterPage.tsx`

**Features:**
- Email, Username, Password, Confirm Password
- Form validation
- Password strength indicator
- Terms of Service checkbox
- Error handling
- Success redirect to dashboard

**API Integration:**
- `POST /api/auth/register`

**UI Design:**
```
┌─────────────────────────────────────┐
│                                     │
│  [SmartSpec Pro Logo]               │
│                                     │
│  Create Account                     │
│  Start building with AI             │
│                                     │
│  Email                              │
│  [___________________________]      │
│                                     │
│  Username                           │
│  [___________________________]      │
│                                     │
│  Password                           │
│  [___________________________]      │
│  [Password Strength: ████░░]        │
│                                     │
│  Confirm Password                   │
│  [___________________________]      │
│                                     │
│  [✓] I agree to Terms of Service    │
│                                     │
│  [Create Account]                   │
│                                     │
│  Already have an account? Sign in   │
│                                     │
└─────────────────────────────────────┘
```

#### 3. Password Reset Page (`/reset-password`)
**File:** `src/pages/auth/ResetPasswordPage.tsx`

**Features:**
- Email input
- Send reset link
- Success message
- Back to login link

**API Integration:**
- `POST /api/auth/forgot-password`

#### 4. Form Validation
**Dependencies:**
```bash
pnpm add react-hook-form zod @hookform/resolvers
```

**Validation Schema:**
```typescript
// src/lib/validations/auth.ts
import { z } from 'zod';

export const loginSchema = z.object({
  email: z.string().email('Invalid email address'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
});

export const registerSchema = z.object({
  email: z.string().email('Invalid email address'),
  username: z.string().min(3, 'Username must be at least 3 characters'),
  password: z.string()
    .min(8, 'Password must be at least 8 characters')
    .regex(/[A-Z]/, 'Password must contain uppercase letter')
    .regex(/[a-z]/, 'Password must contain lowercase letter')
    .regex(/[0-9]/, 'Password must contain number'),
  confirmPassword: z.string(),
}).refine((data) => data.password === data.confirmPassword, {
  message: "Passwords don't match",
  path: ["confirmPassword"],
});
```

**Deliverables:**
- ✅ Login page with form validation
- ✅ Register page with password strength
- ✅ Password reset page
- ✅ Form validation schemas
- ✅ Error handling
- ✅ Loading states
- ✅ Success redirects

**Git Commit:**
```bash
git add .
git commit -m "Phase 2: Authentication system (Login, Register, Reset)"
git push origin main
```

---

### Phase 3: Public Website

**Duration:** 3-4 days  
**Status:** ⏳ Pending

**Goal:** สร้าง Public Website สำหรับ Marketing และ SEO

**Pages to Build:**

#### 1. Landing Page (`/`)
**File:** `src/pages/public/LandingPage.tsx`

**Sections:**
1. **Hero Section**
   - Headline: "Build Production-Grade SaaS in Minutes with AI"
   - Subheadline: "SmartSpec Pro generates complete applications from natural language"
   - CTA: "Start Building" → `/register`
   - Demo video or screenshot

2. **Features Section**
   - Autopilot Code Generation
   - LLM Gateway with 5+ providers
   - Production-Grade Quality
   - Built-in Authentication
   - Credit-Based Pricing
   - Multi-Framework Support

3. **How It Works**
   - Step 1: Describe your app
   - Step 2: AI generates code
   - Step 3: Review & customize
   - Step 4: Deploy

4. **Pricing Preview**
   - Credit packages
   - "View Pricing" → `/pricing`

5. **CTA Section**
   - "Ready to build?"
   - Sign Up button

**SEO:**
- Title: "SmartSpec Pro - AI-Native Development Framework"
- Description: "Build production-grade SaaS applications with AI"
- Keywords: "ai development, code generation, saas builder"
- Open Graph tags
- Schema.org markup

#### 2. Features Page (`/features`)
**File:** `src/pages/public/FeaturesPage.tsx`

**Features to Highlight:**
- **LLM Gateway**
  - 5+ providers (OpenAI, Anthropic, Google, Groq, Ollama)
  - Auto-selection by task & budget
  - 83% cost savings
  - Real-time usage tracking

- **Autopilot System**
  - Natural language to code
  - Multi-step workflows
  - Progress tracking
  - Resume capability

- **Credit System**
  - Pay-as-you-go
  - No subscriptions
  - Transparent pricing
  - Real-time balance

- **Security**
  - JWT authentication
  - Rate limiting
  - Secure API endpoints
  - Data encryption

#### 3. Pricing Page (`/pricing`)
**File:** `src/pages/public/PricingPage.tsx`

**Credit Packages:**
```
┌─────────────────────────┐
│ Starter - $10           │
│ 10 credits              │
│ ~100 LLM calls          │
│ Perfect for testing     │
│ [Buy Now]               │
└─────────────────────────┘

┌─────────────────────────┐
│ Pro - $50 (Popular)     │
│ 50 credits              │
│ ~500 LLM calls          │
│ Build 2-3 apps          │
│ [Buy Now]               │
└─────────────────────────┘

┌─────────────────────────┐
│ Business - $100         │
│ 100 credits             │
│ ~1000 LLM calls         │
│ Build 5-10 apps         │
│ [Buy Now]               │
└─────────────────────────┘

┌─────────────────────────┐
│ Enterprise - $500       │
│ 500 credits             │
│ ~5000 LLM calls         │
│ Unlimited apps          │
│ [Buy Now]               │
└─────────────────────────┘
```

**FAQ Section:**
- How are credits calculated?
- What happens when I run out?
- Can I get a refund?
- How much does each LLM call cost?

**Components to Build:**
- Navigation bar
- Footer
- Feature cards
- Pricing cards
- CTA buttons

**Dependencies:**
```bash
pnpm dlx shadcn@latest add navigation-menu
```

**Deliverables:**
- ✅ Landing page with SEO
- ✅ Features page
- ✅ Pricing page
- ✅ Navigation component
- ✅ Footer component
- ✅ Responsive design

**Git Commit:**
```bash
git add .
git commit -m "Phase 3: Public website (Landing, Features, Pricing)"
git push origin main
```

---

### Phase 4: Dashboard Layout & Navigation

**Duration:** 2-3 days  
**Status:** ⏳ Pending

**Goal:** สร้าง Dashboard Layout พร้อม Sidebar และ Navigation

**Components to Build:**

#### 1. Dashboard Layout
**File:** `src/pages/dashboard/DashboardLayout.tsx`

**Structure:**
```
┌─────────────────────────────────────────────┐
│ [Logo] SmartSpec Pro    [User] [Logout]    │ ← Header
├──────────┬──────────────────────────────────┤
│          │                                  │
│ Sidebar  │ Content Area                     │
│          │                                  │
│ • Home   │ <Outlet /> (React Router)        │
│ • Credits│                                  │
│ • LLM    │                                  │
│ • Usage  │                                  │
│ • Payment│                                  │
│ • Settings│                                 │
│          │                                  │
└──────────┴──────────────────────────────────┘
```

#### 2. Sidebar Component
**File:** `src/components/dashboard/Sidebar.tsx`

**Menu Items:**
- 🏠 Dashboard (`/dashboard`)
- 💰 Credits (`/dashboard/credits`)
- 🤖 LLM Gateway (`/dashboard/llm`)
- 📊 Analytics (`/dashboard/analytics`)
- 💳 Payment (`/dashboard/payment`)
- ⚙️ Settings (`/dashboard/settings`)

**Features:**
- Active state highlighting
- Collapsible on mobile
- Icon + label
- Badge for notifications

#### 3. Header Component
**File:** `src/components/dashboard/Header.tsx`

**Elements:**
- Logo + Title
- Credit balance display
- User dropdown menu
  - Profile
  - Settings
  - Logout

#### 4. Dashboard Home
**File:** `src/pages/dashboard/DashboardHome.tsx`

**Widgets:**
```
┌─────────────────────────────────────────────┐
│ Welcome back, John!                         │
│                                             │
│ ┌──────────┐ ┌──────────┐ ┌──────────┐     │
│ │ Credits  │ │ LLM Calls│ │ Projects │     │
│ │ $45.50   │ │ 234      │ │ 3        │     │
│ └──────────┘ └──────────┘ └──────────┘     │
│                                             │
│ Recent Activity:                            │
│ • 2 hours ago: Generated auth system        │
│ • 5 hours ago: Created database schema      │
│ • Yesterday: Built landing page             │
│                                             │
│ Quick Actions:                              │
│ [Top Up Credits] [View Usage] [New Project] │
└─────────────────────────────────────────────┘
```

**Dependencies:**
```bash
pnpm dlx shadcn@latest add sheet avatar dropdown-menu
```

**Deliverables:**
- ✅ Dashboard layout with sidebar
- ✅ Header with user menu
- ✅ Sidebar navigation
- ✅ Dashboard home page
- ✅ Responsive design
- ✅ Mobile menu

**Git Commit:**
```bash
git add .
git commit -m "Phase 4: Dashboard layout and navigation"
git push origin main
```

---

### Phase 5: Credits Management UI

**Duration:** 2-3 days  
**Status:** ⏳ Pending

**Goal:** สร้าง UI สำหรับจัดการ Credits

**Page:** `src/pages/dashboard/CreditsPage.tsx`

**API Integration:**
- `GET /api/credits/balance` - Get balance
- `GET /api/credits/transactions` - Get history
- `POST /api/credits/calculate` - Calculate credits

**Sections:**

#### 1. Credit Balance Card
```
┌─────────────────────────────────────────────┐
│ Credit Balance                              │
│                                             │
│ Current Balance: $45.50                     │
│ (45,500 credits)                            │
│                                             │
│ Last Top-Up: Dec 25, 2025 ($50)            │
│                                             │
│ [Top Up Credits]                            │
└─────────────────────────────────────────────┘
```

#### 2. Top-Up Section
```
┌─────────────────────────────────────────────┐
│ Top Up Credits                              │
│                                             │
│ Select Package:                             │
│ ┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐   │
│ │  $10  │ │  $50  │ │ $100  │ │ $500  │   │
│ │ 10K   │ │ 50K   │ │ 100K  │ │ 500K  │   │
│ │credits│ │credits│ │credits│ │credits│   │
│ └───────┘ └───────┘ └───────┘ └───────┘   │
│                                             │
│ Or enter custom amount:                     │
│ $ [_______]  = _____ credits                │
│                                             │
│ [Proceed to Payment]                        │
└─────────────────────────────────────────────┘
```

#### 3. Transaction History
```
┌─────────────────────────────────────────────┐
│ Transaction History                         │
│                                             │
│ Filter: [All Types ▼] [Last 30 Days ▼]     │
│                                             │
│ Date       | Type     | Amount   | Balance │
│ ──────────────────────────────────────────  │
│ Dec 29 3pm | Usage    | -$0.45   | $45.50  │
│ Dec 29 2pm | Usage    | -$0.12   | $45.95  │
│ Dec 25 10am| Top-up   | +$50.00  | $46.07  │
│ Dec 24 5pm | Usage    | -$1.80   | -$3.93  │
│                                             │
│ [Load More] [Export CSV]                    │
└─────────────────────────────────────────────┘
```

#### 4. Usage Statistics
```
┌─────────────────────────────────────────────┐
│ Usage Statistics (Last 30 Days)             │
│                                             │
│ Total Spent: $54.50                         │
│ Total Calls: 234                            │
│ Avg per Call: $0.23                         │
│                                             │
│ [Bar Chart: Daily Usage]                    │
└─────────────────────────────────────────────┘
```

**Components:**
- Credit balance card
- Top-up package selector
- Custom amount calculator
- Transaction table
- Usage chart

**Dependencies:**
```bash
pnpm add recharts
pnpm dlx shadcn@latest add table select
```

**Deliverables:**
- ✅ Credits page with balance display
- ✅ Top-up package selector
- ✅ Transaction history table
- ✅ Usage statistics chart
- ✅ Credit calculator

**Git Commit:**
```bash
git add .
git commit -m "Phase 5: Credits management UI"
git push origin main
```

---

### Phase 6: LLM Gateway UI & Usage Tracking

**Duration:** 3-4 days  
**Status:** ⏳ Pending

**Goal:** สร้าง UI สำหรับ LLM Gateway และ Usage Tracking

**Page:** `src/pages/dashboard/LLMGatewayPage.tsx`

**API Integration:**
- `GET /api/llm/providers` - List providers
- `POST /api/llm/invoke` - Invoke LLM
- `GET /api/llm/usage` - Get usage stats
- `GET /api/llm/balance` - Get balance

**Sections:**

#### 1. LLM Playground
```
┌─────────────────────────────────────────────┐
│ LLM Playground                              │
│                                             │
│ Provider: [Auto-Select ▼]                   │
│ Model: [Auto-Select ▼]                      │
│ Task Type: [Simple ▼]                       │
│ Budget: [Cost ▼]                            │
│                                             │
│ Prompt:                                     │
│ ┌─────────────────────────────────────────┐ │
│ │                                         │ │
│ │ Enter your prompt here...               │ │
│ │                                         │ │
│ └─────────────────────────────────────────┘ │
│                                             │
│ Max Tokens: [1000]  Temperature: [0.7]      │
│                                             │
│ Estimated Cost: $0.05                       │
│                                             │
│ [Generate]                                  │
│                                             │
│ Response:                                   │
│ ┌─────────────────────────────────────────┐ │
│ │                                         │ │
│ │ Response will appear here...            │ │
│ │                                         │ │
│ └─────────────────────────────────────────┘ │
│                                             │
│ Actual Cost: $0.04 | Tokens: 234           │
│ Provider: OpenAI | Model: gpt-3.5-turbo    │
│ Latency: 1.2s                               │
└─────────────────────────────────────────────┘
```

#### 2. Provider Status
```
┌─────────────────────────────────────────────┐
│ LLM Providers                               │
│                                             │
│ Provider   | Status  | Models | Avg Cost   │
│ ──────────────────────────────────────────  │
│ OpenAI     | ✅ Active| 5      | $0.002/1K  │
│ Anthropic  | ✅ Active| 3      | $0.008/1K  │
│ Google     | ✅ Active| 2      | $0.001/1K  │
│ Groq       | ✅ Active| 2      | $0.0001/1K │
│ Ollama     | ⚠️ Local | 10     | Free       │
└─────────────────────────────────────────────┘
```

#### 3. Usage History
```
┌─────────────────────────────────────────────┐
│ LLM Usage History                           │
│                                             │
│ Filter: [All Providers ▼] [Last 7 Days ▼]  │
│                                             │
│ Time    | Provider | Model    | Tokens| Cost│
│ ──────────────────────────────────────────  │
│ 3:45 PM | OpenAI   | GPT-4    | 1,234 |$0.45│
│ 2:30 PM | Anthropic| Claude   | 567   |$0.12│
│ 1:15 PM | Google   | Gemini   | 890   |$0.08│
│ 12:00 PM| OpenAI   | GPT-3.5  | 234   |$0.03│
│                                             │
│ Total: 2,925 tokens | $0.68                 │
│                                             │
│ [Export CSV] [View Details]                 │
└─────────────────────────────────────────────┘
```

#### 4. Cost Analytics
```
┌─────────────────────────────────────────────┐
│ Cost Analytics (Last 30 Days)               │
│                                             │
│ [Line Chart: Daily Cost by Provider]        │
│                                             │
│ Total Cost: $54.50                          │
│ Avg Daily: $1.82                            │
│                                             │
│ By Provider:                                │
│ • OpenAI: $32.40 (59%)                      │
│ • Anthropic: $15.20 (28%)                   │
│ • Google: $6.90 (13%)                       │
└─────────────────────────────────────────────┘
```

**Components:**
- LLM playground
- Provider selector
- Prompt input
- Response display
- Provider status table
- Usage history table
- Cost analytics chart

**Dependencies:**
```bash
pnpm dlx shadcn@latest add textarea select tabs
```

**Deliverables:**
- ✅ LLM playground interface
- ✅ Provider status display
- ✅ Usage history table
- ✅ Cost analytics chart
- ✅ Real-time cost estimation

**Git Commit:**
```bash
git add .
git commit -m "Phase 6: LLM Gateway UI and usage tracking"
git push origin main
```

---

### Phase 7: Payment Integration (Stripe)

**Duration:** 2-3 days  
**Status:** ⏳ Pending

**Goal:** เชื่อมต่อ Stripe Payment Gateway

**Page:** `src/pages/dashboard/PaymentPage.tsx`

**API Integration:**
- `POST /api/payments/create-checkout` - Create checkout
- `GET /api/payments/history` - Payment history
- `GET /api/payments/status/:id` - Payment status

**Dependencies:**
```bash
pnpm add @stripe/stripe-js @stripe/react-stripe-js
```

**Sections:**

#### 1. Payment Form
```
┌─────────────────────────────────────────────┐
│ Top Up Credits                              │
│                                             │
│ Select Package:                             │
│ ○ $10 → 10,000 credits                      │
│ ● $50 → 50,000 credits (Popular)            │
│ ○ $100 → 100,000 credits                    │
│ ○ $500 → 500,000 credits                    │
│                                             │
│ Or enter custom amount:                     │
│ $ [50.00] = 50,000 credits                  │
│                                             │
│ Payment Method:                             │
│ [Stripe Card Payment]                       │
│                                             │
│ [Proceed to Checkout]                       │
└─────────────────────────────────────────────┘
```

#### 2. Stripe Checkout Flow
```
User clicks "Proceed to Checkout"
        ↓
Create Stripe Checkout Session
        ↓
Redirect to Stripe
        ↓
User completes payment
        ↓
Stripe webhook → Add credits
        ↓
Redirect back to success page
        ↓
Show success message + new balance
```

#### 3. Payment History
```
┌─────────────────────────────────────────────┐
│ Payment History                             │
│                                             │
│ Date       | Amount | Credits | Status      │
│ ──────────────────────────────────────────  │
│ Dec 25 10am| $50.00 | 50,000  | ✅ Completed│
│ Dec 15 2pm | $100.00| 100,000 | ✅ Completed│
│ Dec 1 9am  | $10.00 | 10,000  | ✅ Completed│
│                                             │
│ Total Paid: $160.00                         │
│ Total Credits: 160,000                      │
│                                             │
│ [Download Receipt] [View Details]           │
└─────────────────────────────────────────────┘
```

#### 4. Success Page
**File:** `src/pages/dashboard/PaymentSuccessPage.tsx`

```
┌─────────────────────────────────────────────┐
│                                             │
│           ✅ Payment Successful!            │
│                                             │
│ You've successfully added 50,000 credits    │
│                                             │
│ New Balance: $95.50 (95,500 credits)        │
│                                             │
│ Transaction ID: txn_1234567890              │
│ Amount Paid: $50.00                         │
│ Credits Added: 50,000                       │
│                                             │
│ [View Receipt] [Back to Dashboard]          │
│                                             │
└─────────────────────────────────────────────┘
```

**Components:**
- Payment form
- Stripe Elements integration
- Package selector
- Payment history table
- Success/failure pages
- Receipt display

**Deliverables:**
- ✅ Stripe checkout integration
- ✅ Payment form
- ✅ Payment history
- ✅ Success/failure pages
- ✅ Receipt generation
- ✅ Webhook handling (backend)

**Git Commit:**
```bash
git add .
git commit -m "Phase 7: Stripe payment integration"
git push origin main
```

---

### Phase 8: Analytics Dashboard

**Duration:** 2-3 days  
**Status:** ⏳ Pending

**Goal:** สร้าง Analytics Dashboard สำหรับ Usage Statistics

**Page:** `src/pages/dashboard/AnalyticsPage.tsx`

**API Integration:**
- `GET /api/analytics/usage` - Usage stats
- `GET /api/analytics/cost` - Cost breakdown
- `GET /api/analytics/trends` - Trends

**Sections:**

#### 1. Overview Cards
```
┌─────────────────────────────────────────────┐
│ Analytics Overview (Last 30 Days)           │
│                                             │
│ ┌──────────┐ ┌──────────┐ ┌──────────┐     │
│ │Total Cost│ │LLM Calls │ │Avg/Call  │     │
│ │ $54.50   │ │ 234      │ │ $0.23    │     │
│ │ +12%     │ │ +8%      │ │ +4%      │     │
│ └──────────┘ └──────────┘ └──────────┘     │
└─────────────────────────────────────────────┘
```

#### 2. Usage Trends
```
┌─────────────────────────────────────────────┐
│ Usage Trends                                │
│                                             │
│ [Line Chart: Daily LLM Calls & Cost]        │
│                                             │
│ Time Range: [Last 30 Days ▼]                │
└─────────────────────────────────────────────┘
```

#### 3. Provider Breakdown
```
┌─────────────────────────────────────────────┐
│ Usage by Provider                           │
│                                             │
│ [Pie Chart: Provider Distribution]          │
│                                             │
│ Provider   | Calls | Cost   | Percentage   │
│ ──────────────────────────────────────────  │
│ OpenAI     | 140   | $32.40 | 59%          │
│ Anthropic  | 65    | $15.20 | 28%          │
│ Google     | 29    | $6.90  | 13%          │
└─────────────────────────────────────────────┘
```

#### 4. Model Breakdown
```
┌─────────────────────────────────────────────┐
│ Usage by Model                              │
│                                             │
│ Model        | Calls | Avg Cost | Total    │
│ ──────────────────────────────────────────  │
│ GPT-4        | 45    | $0.45    | $20.25   │
│ GPT-3.5      | 95    | $0.12    | $11.40   │
│ Claude-3     | 65    | $0.23    | $14.95   │
│ Gemini Pro   | 29    | $0.24    | $6.96    │
└─────────────────────────────────────────────┘
```

#### 5. Cost Forecast
```
┌─────────────────────────────────────────────┐
│ Cost Forecast (Next 30 Days)                │
│                                             │
│ Based on current usage:                     │
│ Estimated Cost: $60.50                      │
│ Estimated Calls: 260                        │
│                                             │
│ [Line Chart: Forecast vs Actual]            │
└─────────────────────────────────────────────┘
```

**Components:**
- Overview cards with trends
- Line charts (usage over time)
- Pie charts (provider distribution)
- Bar charts (model comparison)
- Data tables
- Export functionality

**Dependencies:**
```bash
pnpm add recharts date-fns
pnpm dlx shadcn@latest add tabs
```

**Deliverables:**
- ✅ Analytics overview page
- ✅ Usage trend charts
- ✅ Provider breakdown
- ✅ Model comparison
- ✅ Cost forecast
- ✅ Export to CSV

**Git Commit:**
```bash
git add .
git commit -m "Phase 8: Analytics dashboard with charts"
git push origin main
```

---

### Phase 9: Admin Dashboard

**Duration:** 3-4 days  
**Status:** ⏳ Pending

**Goal:** สร้าง Admin Dashboard สำหรับจัดการระบบ

**Page:** `src/pages/admin/AdminDashboardPage.tsx`

**API Integration:**
- `GET /api/admin/users` - List users
- `GET /api/admin/stats` - System stats
- `POST /api/admin/credits/adjust` - Adjust credits
- `GET /api/admin/transactions` - All transactions

**Access Control:**
- Only accessible by admin users
- Check `user.is_admin` in Auth context
- Redirect non-admins to dashboard

**Sections:**

#### 1. System Overview
```
┌─────────────────────────────────────────────┐
│ System Overview                             │
│                                             │
│ ┌──────────┐ ┌──────────┐ ┌──────────┐     │
│ │Total Users│Active Users│Total Revenue│    │
│ │ 1,234    │ 567 (30d) │ $12,345     │    │
│ └──────────┘ └──────────┘ └──────────┘     │
│                                             │
│ ┌──────────┐ ┌──────────┐ ┌──────────┐     │
│ │LLM Calls │ Avg/User   │ Uptime      │    │
│ │ 45,678   │ 37         │ 99.9%       │    │
│ └──────────┘ └──────────┘ └──────────┘     │
└─────────────────────────────────────────────┘
```

#### 2. User Management
```
┌─────────────────────────────────────────────┐
│ User Management                             │
│                                             │
│ Search: [____________] [Search]             │
│                                             │
│ Email        | Credits | Status  | Actions  │
│ ──────────────────────────────────────────  │
│ john@ex.com  | $45.50  | Active  | [Edit]   │
│ jane@ex.com  | $12.30  | Active  | [Edit]   │
│ bob@ex.com   | $0.00   | Paused  | [Edit]   │
│                                             │
│ [1] [2] [3] ... [10] Next →                 │
└─────────────────────────────────────────────┘
```

#### 3. User Detail Modal
```
┌─────────────────────────────────────────────┐
│ User: john@example.com                      │
│                                             │
│ Profile:                                    │
│ • Name: John Doe                            │
│ • Email: john@example.com                   │
│ • Joined: Dec 1, 2025                       │
│ • Status: Active                            │
│                                             │
│ Credits:                                    │
│ • Balance: $45.50 (45,500 credits)          │
│ • Total Topped Up: $100.00                  │
│ • Total Used: $54.50                        │
│                                             │
│ Adjust Credits:                             │
│ Amount: [______] Reason: [______]           │
│ [Add Credits] [Deduct Credits]              │
│                                             │
│ Actions:                                    │
│ [Suspend User] [Delete User]                │
│                                             │
│ [Close]                                     │
└─────────────────────────────────────────────┘
```

#### 4. Revenue Analytics
```
┌─────────────────────────────────────────────┐
│ Revenue Analytics                           │
│                                             │
│ [Line Chart: Daily Revenue]                 │
│                                             │
│ This Month: $3,456                          │
│ Last Month: $2,890 (+19.6%)                 │
│                                             │
│ Top Users by Revenue:                       │
│ 1. john@example.com - $234                  │
│ 2. jane@example.com - $189                  │
│ 3. bob@example.com - $156                   │
└─────────────────────────────────────────────┘
```

#### 5. System Configuration
```
┌─────────────────────────────────────────────┐
│ System Configuration                        │
│                                             │
│ Credit Markup: [15]%                        │
│ Min Top-Up: $[5.00]                         │
│ Max Top-Up: $[10000.00]                     │
│                                             │
│ LLM Providers:                              │
│ ☑ OpenAI                                    │
│ ☑ Anthropic                                 │
│ ☑ Google                                    │
│ ☑ Groq                                      │
│ ☐ Ollama (Local)                            │
│                                             │
│ [Save Changes]                              │
└─────────────────────────────────────────────┘
```

**Components:**
- System stats cards
- User management table
- User detail modal
- Credit adjustment form
- Revenue charts
- Configuration form

**Dependencies:**
```bash
pnpm dlx shadcn@latest add dialog alert-dialog
```

**Deliverables:**
- ✅ Admin dashboard overview
- ✅ User management interface
- ✅ Credit adjustment tool
- ✅ Revenue analytics
- ✅ System configuration
- ✅ Access control

**Git Commit:**
```bash
git add .
git commit -m "Phase 9: Admin dashboard"
git push origin main
```

---

### Phase 10: Testing, Documentation & Deployment

**Duration:** 2-3 days  
**Status:** ⏳ Pending

**Goal:** Testing, Documentation และ Deployment

**Tasks:**

#### 1. Testing
- Unit tests for components
- Integration tests for API calls
- E2E tests for critical flows
- Manual testing checklist

**Testing Tools:**
```bash
pnpm add -D vitest @testing-library/react @testing-library/jest-dom
pnpm add -D @testing-library/user-event
```

**Test Coverage:**
- Auth flow (login, register, logout)
- Credits management
- Payment flow
- LLM invocation
- Admin functions

#### 2. Documentation

**Files to Create:**
- `README.md` - Project overview
- `SETUP.md` - Setup instructions
- `API.md` - API documentation
- `DEPLOYMENT.md` - Deployment guide
- `CONTRIBUTING.md` - Contribution guidelines

**README.md Structure:**
```markdown
# SmartSpec Pro - Web Dashboard

## Overview
Web dashboard for SmartSpec Pro

## Features
- Authentication
- Credits management
- LLM Gateway
- Payment integration
- Analytics
- Admin dashboard

## Tech Stack
- React 18 + TypeScript
- Vite
- Tailwind CSS + shadcn/ui
- React Router
- TanStack Query

## Setup
See SETUP.md

## Deployment
See DEPLOYMENT.md
```

#### 3. Environment Configuration

**`.env.example`:**
```env
VITE_API_URL=http://localhost:8000
VITE_STRIPE_PUBLIC_KEY=pk_test_...
VITE_APP_NAME=SmartSpec Pro
VITE_APP_URL=https://smartspecpro.com
```

#### 4. Build Configuration

**`vite.config.ts` updates:**
```typescript
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  build: {
    outDir: 'dist',
    sourcemap: true,
    rollupOptions: {
      output: {
        manualChunks: {
          'react-vendor': ['react', 'react-dom', 'react-router-dom'],
          'ui-vendor': ['@radix-ui/react-dialog', '@radix-ui/react-dropdown-menu'],
          'charts': ['recharts'],
        },
      },
    },
  },
})
```

#### 5. Deployment

**Vercel Deployment:**
```bash
# Install Vercel CLI
pnpm add -g vercel

# Deploy
vercel --prod
```

**Vercel Configuration (`vercel.json`):**
```json
{
  "buildCommand": "pnpm build",
  "outputDirectory": "dist",
  "framework": "vite",
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ]
}
```

**Deliverables:**
- ✅ Test suite
- ✅ Documentation
- ✅ Environment configuration
- ✅ Build optimization
- ✅ Deployment setup
- ✅ CI/CD pipeline

**Git Commit:**
```bash
git add .
git commit -m "Phase 10: Testing, documentation, and deployment"
git push origin main
```

---

## Summary

**Total Duration:** 20-30 days

**Phases:**
1. ✅ Project Setup (1 day) - COMPLETE
2. 🔄 Authentication (2-3 days) - NEXT
3. ⏳ Public Website (3-4 days)
4. ⏳ Dashboard Layout (2-3 days)
5. ⏳ Credits Management (2-3 days)
6. ⏳ LLM Gateway UI (3-4 days)
7. ⏳ Payment Integration (2-3 days)
8. ⏳ Analytics Dashboard (2-3 days)
9. ⏳ Admin Dashboard (3-4 days)
10. ⏳ Testing & Deployment (2-3 days)

**Git Workflow:**
- Each phase = 1 commit
- Commit message format: "Phase X: Description"
- Push after each phase completion

**Next Steps:**
1. Start Phase 2: Authentication System
2. Install dependencies (react-hook-form, zod)
3. Create login/register pages
4. Implement form validation
5. Test authentication flow
6. Commit and push

---

## Notes

**Backend APIs Available:**
- ✅ `/api/auth/*` - Authentication
- ✅ `/api/credits/*` - Credits Management
- ✅ `/api/llm/*` - LLM Gateway
- ✅ `/api/payments/*` - Payment Processing
- ✅ `/api/analytics/*` - Usage Analytics
- ✅ `/api/admin/*` - Admin Functions

**Design System:**
- shadcn/ui components
- Tailwind CSS utilities
- Consistent spacing (4px grid)
- Color scheme: neutral + primary
- Typography: Inter font family

**Best Practices:**
- TypeScript strict mode
- ESLint + Prettier
- Component composition
- Custom hooks for logic
- API service layer
- Error boundaries
- Loading states
- Optimistic updates
