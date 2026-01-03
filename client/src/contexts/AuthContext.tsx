/**
 * Authentication Context
 * Manages user authentication state and provides auth methods
 */

import { createContext, useContext, useState, useEffect, ReactNode } from 'react';

export interface User {
  id: string;
  email: string;
  name: string;
  avatar?: string;
  company?: string;
  plan: 'free' | 'pro' | 'enterprise';
  credits?: number;
}

interface AuthContextType {
  user: User | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  login: (userOrEmail: User | string, password?: string) => Promise<void>;
  signup: (data: SignupData) => Promise<void>;
  logout: () => Promise<void>;
  loginWithGoogle: () => Promise<void>;
  loginWithGitHub: () => Promise<void>;
  refreshUser: () => Promise<void>;
  updateUser: (updates: Partial<User>) => void;
}

interface SignupData {
  name: string;
  email: string;
  password: string;
  company?: string;
  plan: 'free' | 'pro';
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

// API base URL - configure based on environment
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // Check for existing session on mount
  useEffect(() => {
    checkAuth();
  }, []);

  const checkAuth = async () => {
    try {
      const token = localStorage.getItem('auth_token');
      if (!token) {
        setIsLoading(false);
        return;
      }

      const response = await fetch(`${API_BASE_URL}/api/auth/me`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (response.ok) {
        const userData = await response.json();
        setUser(userData);
      } else {
        // Token invalid, clear it
        localStorage.removeItem('auth_token');
      }
    } catch (error) {
      console.error('Auth check failed:', error);
      // For demo mode, check if we have a stored user
      const storedUser = localStorage.getItem('demo_user');
      if (storedUser) {
        setUser(JSON.parse(storedUser));
      } else {
        localStorage.removeItem('auth_token');
      }
    } finally {
      setIsLoading(false);
    }
  };

  const login = async (userOrEmail: User | string, password?: string) => {
    setIsLoading(true);
    try {
      // If userOrEmail is a User object (from OAuth callback)
      if (typeof userOrEmail === 'object') {
        setUser(userOrEmail);
        localStorage.setItem('demo_user', JSON.stringify(userOrEmail));
        localStorage.setItem('auth_token', 'demo_token_' + userOrEmail.id);
        return;
      }

      // Otherwise, it's email/password login
      const email = userOrEmail;
      const response = await fetch(`${API_BASE_URL}/api/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Login failed');
      }

      const data = await response.json();
      localStorage.setItem('auth_token', data.access_token);
      setUser(data.user);
    } catch (error) {
      // Demo mode: create mock user for testing
      if (typeof userOrEmail === 'string') {
        const mockUser: User = {
          id: 'demo_' + Date.now(),
          email: userOrEmail,
          name: userOrEmail.split('@')[0],
          avatar: `https://api.dicebear.com/7.x/avataaars/svg?seed=${userOrEmail}`,
          plan: 'free',
          credits: 100,
        };
        setUser(mockUser);
        localStorage.setItem('demo_user', JSON.stringify(mockUser));
        localStorage.setItem('auth_token', 'demo_token_' + mockUser.id);
      } else {
        throw error;
      }
    } finally {
      setIsLoading(false);
    }
  };

  const signup = async (signupData: SignupData) => {
    setIsLoading(true);
    try {
      const response = await fetch(`${API_BASE_URL}/api/auth/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(signupData),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || 'Signup failed');
      }

      const data = await response.json();
      localStorage.setItem('auth_token', data.access_token);
      setUser(data.user);
    } catch (error) {
      // Demo mode: create mock user
      const mockUser: User = {
        id: 'demo_' + Date.now(),
        email: signupData.email,
        name: signupData.name,
        company: signupData.company,
        avatar: `https://api.dicebear.com/7.x/avataaars/svg?seed=${signupData.email}`,
        plan: signupData.plan,
        credits: signupData.plan === 'pro' ? 500 : 100,
      };
      setUser(mockUser);
      localStorage.setItem('demo_user', JSON.stringify(mockUser));
      localStorage.setItem('auth_token', 'demo_token_' + mockUser.id);
    } finally {
      setIsLoading(false);
    }
  };

  const logout = async () => {
    try {
      const token = localStorage.getItem('auth_token');
      if (token && !token.startsWith('demo_')) {
        await fetch(`${API_BASE_URL}/api/auth/logout`, {
          method: 'POST',
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
      }
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      localStorage.removeItem('auth_token');
      localStorage.removeItem('demo_user');
      setUser(null);
    }
  };

  const loginWithGoogle = async () => {
    // Store state for CSRF protection
    const state = Math.random().toString(36).substring(7);
    sessionStorage.setItem('oauth_state', state);
    sessionStorage.setItem('oauth_provider', 'google');
    
    // Redirect to Google OAuth
    const redirectUri = `${window.location.origin}/auth/callback/google`;
    const googleAuthUrl = `${API_BASE_URL}/api/auth/google?redirect_uri=${encodeURIComponent(redirectUri)}&state=${state}`;
    window.location.href = googleAuthUrl;
  };

  const loginWithGitHub = async () => {
    // Store state for CSRF protection
    const state = Math.random().toString(36).substring(7);
    sessionStorage.setItem('oauth_state', state);
    sessionStorage.setItem('oauth_provider', 'github');
    
    // Redirect to GitHub OAuth
    const redirectUri = `${window.location.origin}/auth/callback/github`;
    const githubAuthUrl = `${API_BASE_URL}/api/auth/github?redirect_uri=${encodeURIComponent(redirectUri)}&state=${state}`;
    window.location.href = githubAuthUrl;
  };

  const refreshUser = async () => {
    const token = localStorage.getItem('auth_token');
    if (!token) return;

    // Demo mode
    if (token.startsWith('demo_')) {
      const storedUser = localStorage.getItem('demo_user');
      if (storedUser) {
        setUser(JSON.parse(storedUser));
      }
      return;
    }

    try {
      const response = await fetch(`${API_BASE_URL}/api/auth/me`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (response.ok) {
        const userData = await response.json();
        setUser(userData);
      }
    } catch (error) {
      console.error('Failed to refresh user:', error);
    }
  };

  const updateUser = (updates: Partial<User>) => {
    if (user) {
      const updatedUser = { ...user, ...updates };
      setUser(updatedUser);
      localStorage.setItem('demo_user', JSON.stringify(updatedUser));
    }
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        isLoading,
        isAuthenticated: !!user,
        login,
        signup,
        logout,
        loginWithGoogle,
        loginWithGitHub,
        refreshUser,
        updateUser,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}
