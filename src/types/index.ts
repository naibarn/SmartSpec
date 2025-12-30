// User Types
export interface User {
  id: string;
  email: string;
  username: string;
  full_name?: string;
  credits_balance: number;
  role: 'user' | 'admin';
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

// Auth Types
export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  password: string;
  full_name: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}

// Credits Types
export interface CreditTransaction {
  id: number;
  user_id: string;
  amount: number;
  transaction_type: 'purchase' | 'usage' | 'refund' | 'bonus';
  description: string;
  balance_after: number;
  created_at: string;
}

export interface CreditBalance {
  balance: number;
  total_purchased: number;
  total_used: number;
}

// Payment Types
export interface PaymentTransaction {
  id: number;
  user_id: string;
  amount_usd: number;
  credits_amount: number;
  status: 'pending' | 'completed' | 'failed' | 'refunded';
  payment_method: string;
  payment_intent_id?: string;
  created_at: string;
  completed_at?: string;
}

export interface CreateCheckoutRequest {
  amount_usd: number;
  success_url: string;
  cancel_url: string;
}

export interface CheckoutResponse {
  session_id: string;
  url: string;
  credits_to_receive: number;
  amount_usd: number;
  payment_transaction_id: number;
}

// Usage Analytics Types
export interface UsageStats {
  total_requests: number;
  total_credits_used: number;
  requests_by_day: Array<{
    date: string;
    count: number;
    credits_used: number;
  }>;
  requests_by_feature: Array<{
    feature: string;
    count: number;
    credits_used: number;
  }>;
}

// API Response Types
export interface APIResponse<T> {
  data: T;
  message?: string;
  success: boolean;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

// Error Types
export interface APIError {
  detail: string;
  status_code: number;
}
