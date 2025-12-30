# SmartSpec Pro - Web Dashboard

> Modern, beautiful, and feature-rich web dashboard for SmartSpec Pro LLM Gateway platform.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![React](https://img.shields.io/badge/React-18.3.1-blue.svg)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.6.2-blue.svg)](https://www.typescriptlang.org/)
[![Vite](https://img.shields.io/badge/Vite-7.3.0-purple.svg)](https://vitejs.dev/)

## 🌟 Features

### Public Website
- **Landing Page** - Beautiful hero section with glassmorphism design
- **Features Page** - Showcase platform capabilities
- **Pricing Page** - Clear pricing tiers and packages
- **SEO Optimized** - Meta tags, Open Graph, Schema.org
- **Responsive Design** - Mobile-first approach

### Authentication
- **Email/Password Login** - Secure authentication
- **User Registration** - With password strength validation
- **OAuth Integration** - Google and GitHub login
- **Password Reset** - Forgot password flow
- **Protected Routes** - Secure dashboard access

### Dashboard
- **Modern Layout** - Collapsible sidebar, responsive header
- **Credits Management** - View balance, transaction history, buy credits
- **LLM Gateway Configuration** - Multi-tier strategy, load balancing, failover
- **Payment Integration** - Stripe checkout, billing history
- **Analytics Dashboard** - Charts, metrics, usage statistics
- **Admin Panel** - User management, system health, audit logs

### Design
- **Modern UI** - shadcn/ui components
- **Dark/Light Theme** - Theme toggle with system preference
- **Glassmorphism** - Backdrop blur effects
- **Smooth Animations** - Framer Motion transitions
- **Responsive** - Works on all devices

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ 
- pnpm 8+
- Backend API running (see [python-backend](../python-backend/))

### Installation

```bash
# Clone the repository
git clone https://github.com/naibarn/SmartSpec.git
cd SmartSpec/web-dashboard

# Install dependencies
pnpm install

# Copy environment variables
cp .env.example .env

# Edit .env with your configuration
nano .env
```

### Environment Variables

Create a `.env` file in the root directory:

```env
# API Configuration
VITE_API_BASE_URL=http://localhost:8000
VITE_API_TIMEOUT=30000

# OAuth Configuration
VITE_GOOGLE_CLIENT_ID=your_google_client_id
VITE_GITHUB_CLIENT_ID=your_github_client_id

# Stripe Configuration
VITE_STRIPE_PUBLISHABLE_KEY=your_stripe_publishable_key

# App Configuration
VITE_APP_NAME=SmartSpec Pro
VITE_APP_URL=https://smartspecpro.com
```

### Development

```bash
# Start development server
pnpm dev

# Open browser at http://localhost:5173
```

### Build

```bash
# Build for production
pnpm build

# Preview production build
pnpm preview
```

## 📁 Project Structure

```
web-dashboard/
├── src/
│   ├── components/          # Reusable components
│   │   ├── ui/             # shadcn/ui components
│   │   ├── dashboard/      # Dashboard-specific components
│   │   ├── SEO.tsx         # SEO component
│   │   ├── ThemeProvider.tsx
│   │   ├── ThemeToggle.tsx
│   │   ├── Motion.tsx      # Animation wrappers
│   │   └── ProtectedRoute.tsx
│   ├── pages/              # Page components
│   │   ├── public/         # Public pages
│   │   │   ├── LandingPage.tsx
│   │   │   ├── FeaturesPage.tsx
│   │   │   └── PricingPage.tsx
│   │   ├── auth/           # Authentication pages
│   │   │   ├── LoginPage.tsx
│   │   │   ├── RegisterPage.tsx
│   │   │   ├── ResetPasswordPage.tsx
│   │   │   └── OAuthCallbackPage.tsx
│   │   └── dashboard/      # Dashboard pages
│   │       ├── DashboardPage.tsx
│   │       ├── CreditsPage.tsx
│   │       ├── BuyCreditsPage.tsx
│   │       ├── LLMGatewayPage.tsx
│   │       ├── PaymentsPage.tsx
│   │       ├── AnalyticsPage.tsx
│   │       └── AdminPage.tsx
│   ├── layouts/            # Layout components
│   │   └── DashboardLayout.tsx
│   ├── contexts/           # React contexts
│   │   └── AuthContext.tsx
│   ├── services/           # API services
│   │   └── api.ts
│   ├── lib/                # Utilities
│   │   ├── utils.ts
│   │   └── validations.ts
│   ├── types/              # TypeScript types
│   │   └── index.ts
│   ├── assets/             # Static assets
│   ├── App.tsx             # Main app component
│   ├── main.tsx            # Entry point
│   └── index.css           # Global styles
├── public/                 # Public assets
├── docs/                   # Documentation
│   ├── API_INTEGRATION.md
│   ├── DEPLOYMENT.md
│   ├── DEVELOPER_GUIDE.md
│   ├── USER_GUIDE.md
│   ├── ARCHITECTURE.md
│   └── CONFIGURATION.md
├── components.json         # shadcn/ui config
├── tailwind.config.js      # Tailwind CSS config
├── vite.config.ts          # Vite config
├── tsconfig.json           # TypeScript config
├── package.json            # Dependencies
└── README.md               # This file
```

## 🛠️ Tech Stack

### Core
- **React 18.3.1** - UI library
- **TypeScript 5.6.2** - Type safety
- **Vite 7.3.0** - Build tool
- **React Router 7.1.1** - Routing

### UI & Styling
- **Tailwind CSS 3.4.17** - Utility-first CSS
- **shadcn/ui** - Component library
- **Radix UI** - Headless UI components
- **Framer Motion 12.0.0** - Animations
- **Lucide React** - Icons

### State & Data
- **TanStack Query 5.62.11** - Data fetching
- **Axios 1.7.9** - HTTP client
- **React Hook Form 7.54.2** - Form management
- **Zod 3.24.1** - Schema validation

### Charts & Visualization
- **Recharts 2.15.0** - Charts library

### Payment
- **Stripe React 2.10.0** - Payment integration
- **Stripe.js 4.11.0** - Stripe SDK

### SEO
- **React Helmet Async 2.0.5** - Meta tags management

## 📚 Documentation

- [API Integration Guide](./docs/API_INTEGRATION.md) - How to connect to backend APIs
- [Deployment Guide](./docs/DEPLOYMENT.md) - Deploy to production
- [Developer Guide](./docs/DEVELOPER_GUIDE.md) - Development workflow
- [User Guide](./docs/USER_GUIDE.md) - User manual
- [Architecture](./docs/ARCHITECTURE.md) - System architecture
- [Configuration](./docs/CONFIGURATION.md) - Environment setup

## 🎨 Design System

### Colors
- **Primary**: Blue (#3b82f6)
- **Success**: Green (#10b981)
- **Warning**: Orange (#f59e0b)
- **Error**: Red (#ef4444)
- **Info**: Purple (#8b5cf6)

### Typography
- **Font Family**: Inter, system-ui, sans-serif

### Border Radius
- **lg**: 0.5rem (8px)
- **xl**: 0.75rem (12px)
- **2xl**: 1rem (16px)
- **3xl**: 1.5rem (24px)
- **full**: 9999px

## 🔐 Security

- **Authentication**: JWT tokens
- **OAuth**: Secure OAuth 2.0 flow
- **HTTPS**: Required in production
- **Input Validation**: Zod schemas

## 📦 Building for Production

```bash
# Build optimized production bundle
pnpm build

# Preview production build locally
pnpm preview
```

## 🚀 Deployment

See [DEPLOYMENT.md](./docs/DEPLOYMENT.md) for detailed instructions.

## 📝 License

This project is licensed under the MIT License.

## 📞 Support

- **Email**: support@smartspecpro.com
- **GitHub Issues**: https://github.com/naibarn/SmartSpec/issues

---

**Built with ❤️ by SmartSpec Team**
