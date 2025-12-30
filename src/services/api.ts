import axios, { type AxiosInstance, AxiosError } from 'axios';
import type {
  User,
  LoginRequest,
  RegisterRequest,
  AuthResponse,
  CreditTransaction,
  CreditBalance,
  PaymentTransaction,
  CreateCheckoutRequest,
  CheckoutResponse,
  UsageStats,
  PaginatedResponse,
  APIError,
} from '@/types';

// API Base URL - will be configured based on environment
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

class APIService {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Request interceptor to add auth token
    this.client.interceptors.request.use(
      (config) => {
        const token = localStorage.getItem('access_token');
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    // Response interceptor to handle errors
    this.client.interceptors.response.use(
      (response) => response,
      (error: AxiosError<APIError>) => {
        if (error.response?.status === 401) {
          // Token expired or invalid
          localStorage.removeItem('access_token');
          window.location.href = '/login';
        }
        return Promise.reject(error);
      }
    );
  }

  // Auth endpoints
  async login(data: LoginRequest): Promise<AuthResponse> {
    const formData = new FormData();
    formData.append('username', data.email);
    formData.append('password', data.password);
    
    const response = await this.client.post<AuthResponse>('/api/auth/login', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
  }

  async register(data: RegisterRequest): Promise<AuthResponse> {
    const response = await this.client.post<AuthResponse>('/api/auth/register', data);
    return response.data;
  }

  async getCurrentUser(): Promise<User> {
    const response = await this.client.get<User>('/api/auth/me');
    return response.data;
  }

  async logout(): Promise<void> {
    await this.client.post('/api/auth/logout');
    localStorage.removeItem('access_token');
  }

  // Credits endpoints
  async getCreditBalance(): Promise<CreditBalance> {
    const response = await this.client.get<CreditBalance>('/api/credits/balance');
    return response.data;
  }

  async getCreditHistory(page: number = 1, pageSize: number = 20): Promise<PaginatedResponse<CreditTransaction>> {
    const response = await this.client.get<PaginatedResponse<CreditTransaction>>('/api/credits/history', {
      params: { page, page_size: pageSize },
    });
    return response.data;
  }

  // Payment endpoints
  async createCheckout(data: CreateCheckoutRequest): Promise<CheckoutResponse> {
    const response = await this.client.post<CheckoutResponse>('/payments/create-checkout', data);
    return response.data;
  }

  async getPaymentHistory(page: number = 1, pageSize: number = 20): Promise<PaginatedResponse<PaymentTransaction>> {
    const response = await this.client.get<PaginatedResponse<PaymentTransaction>>('/payments/history', {
      params: { page, page_size: pageSize },
    });
    return response.data;
  }

  async getPaymentStatus(sessionId: string): Promise<PaymentTransaction> {
    const response = await this.client.get<PaymentTransaction>(`/payments/status/${sessionId}`);
    return response.data;
  }

  // Analytics endpoints
  async getUsageStats(days: number = 30): Promise<UsageStats> {
    const response = await this.client.get<UsageStats>('/api/analytics/usage', {
      params: { days },
    });
    return response.data;
  }

  // Dashboard endpoints
  async getDashboardData(): Promise<{
    user: User;
    credits: CreditBalance;
    recent_usage: UsageStats;
  }> {
    const response = await this.client.get('/api/dashboard');
    return response.data;
  }

  // OAuth endpoints
  async getGoogleAuthUrl(): Promise<{ authorization_url: string }> {
    const response = await this.client.get('/api/oauth/google/authorize');
    return response.data;
  }

  async getGithubAuthUrl(): Promise<{ authorization_url: string }> {
    const response = await this.client.get('/api/oauth/github/authorize');
    return response.data;
  }

  async handleGoogleCallback(code: string): Promise<AuthResponse> {
    const response = await this.client.post('/api/oauth/google/callback', { code });
    return response.data;
  }

  async handleGithubCallback(code: string): Promise<AuthResponse> {
    const response = await this.client.post('/api/oauth/github/callback', { code });
    return response.data;
  }

  async getOAuthConnections(): Promise<{ connections: Array<{ provider: string; connected_at: string; email_verified: boolean }> }> {
    const response = await this.client.get('/api/oauth/connections');
    return response.data;
  }

  async linkOAuthAccount(provider: string, code: string): Promise<{ message: string }> {
    const response = await this.client.post('/api/oauth/link', { provider, code });
    return response.data;
  }

  async unlinkOAuthAccount(provider: string): Promise<{ message: string }> {
    const response = await this.client.delete(`/api/oauth/unlink/${provider}`);
    return response.data;
  }

  // Password reset endpoints
  async forgotPassword(email: string): Promise<{ message: string }> {
    const response = await this.client.post('/api/auth/forgot-password', { email });
    return response.data;
  }

  async resetPassword(token: string, newPassword: string): Promise<{ message: string }> {
    const response = await this.client.post('/api/auth/reset-password', { 
      token, 
      new_password: newPassword 
    });
    return response.data;
  }
}

export const apiService = new APIService();
export default apiService;
