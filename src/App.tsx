import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { HelmetProvider } from 'react-helmet-async';
import { AuthProvider } from '@/contexts/AuthContext';
import { ThemeProvider } from '@/components/ThemeProvider';
import { ProtectedRoute } from '@/components/ProtectedRoute';

// Layouts
import { DashboardLayout } from '@/layouts/DashboardLayout';

// Public Pages
import LandingPage from '@/pages/public/LandingPage';
import FeaturesPage from '@/pages/public/FeaturesPage';
import PricingPage from '@/pages/public/PricingPage';

// Auth Pages
import LoginPage from '@/pages/auth/LoginPage';
import RegisterPage from '@/pages/auth/RegisterPage';
import ResetPasswordPage from '@/pages/auth/ResetPasswordPage';
import OAuthCallbackPage from '@/pages/auth/OAuthCallbackPage';

// Dashboard Pages
import DashboardPage from '@/pages/dashboard/DashboardPage';
import { PlaceholderPage } from '@/pages/dashboard/PlaceholderPage';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
});

function App() {
  return (
    <HelmetProvider>
      <QueryClientProvider client={queryClient}>
        <ThemeProvider defaultTheme="system" storageKey="smartspec-ui-theme">
          <BrowserRouter>
            <AuthProvider>
            <Routes>
              {/* Public Routes */}
              <Route path="/" element={<LandingPage />} />
              <Route path="/features" element={<FeaturesPage />} />
              <Route path="/pricing" element={<PricingPage />} />

              {/* Auth Routes */}
              <Route path="/login" element={<LoginPage />} />
              <Route path="/register" element={<RegisterPage />} />
              <Route path="/reset-password" element={<ResetPasswordPage />} />
              <Route path="/auth/callback/:provider" element={<OAuthCallbackPage />} />

              {/* Dashboard Routes (Protected) */}
              <Route
                path="/dashboard"
                element={
                  <ProtectedRoute>
                    <DashboardLayout />
                  </ProtectedRoute>
                }
              >
                <Route index element={<DashboardPage />} />
                <Route path="llm-gateway" element={<PlaceholderPage title="LLM Gateway" phase="Phase 6" />} />
                <Route path="analytics" element={<PlaceholderPage title="Analytics" phase="Phase 8" />} />
                <Route path="credits" element={<PlaceholderPage title="Credits" phase="Phase 5" />} />
                <Route path="payments" element={<PlaceholderPage title="Payments" phase="Phase 7" />} />
                <Route path="api-keys" element={<PlaceholderPage title="API Keys" phase="Future" />} />
                <Route path="monitoring" element={<PlaceholderPage title="Monitoring" phase="Future" />} />
                <Route path="logs" element={<PlaceholderPage title="Logs" phase="Future" />} />
                <Route path="settings" element={<PlaceholderPage title="Settings" phase="Future" />} />
                <Route path="admin" element={<PlaceholderPage title="Admin Panel" phase="Phase 9" />} />
              </Route>

              {/* Catch all */}
              <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
            </AuthProvider>
          </BrowserRouter>
        </ThemeProvider>
      </QueryClientProvider>
    </HelmetProvider>
  );
}

export default App;
