/**
 * API Hooks
 * Custom hooks for API communication with backend
 */

import { useState, useCallback } from 'react';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

interface ApiResponse<T> {
  data: T | null;
  error: string | null;
  isLoading: boolean;
}

interface ApiOptions {
  method?: 'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH';
  body?: unknown;
  headers?: Record<string, string>;
  requireAuth?: boolean;
}

export function useApi<T>() {
  const [state, setState] = useState<ApiResponse<T>>({
    data: null,
    error: null,
    isLoading: false,
  });

  const request = useCallback(async (endpoint: string, options: ApiOptions = {}) => {
    const { method = 'GET', body, headers = {}, requireAuth = true } = options;

    setState((prev) => ({ ...prev, isLoading: true, error: null }));

    try {
      const token = localStorage.getItem('auth_token');
      
      const requestHeaders: Record<string, string> = {
        'Content-Type': 'application/json',
        ...headers,
      };

      if (requireAuth && token) {
        requestHeaders['Authorization'] = `Bearer ${token}`;
      }

      const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        method,
        headers: requestHeaders,
        body: body ? JSON.stringify(body) : undefined,
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `Request failed with status ${response.status}`);
      }

      const data = await response.json();
      setState({ data, error: null, isLoading: false });
      return data;
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'An error occurred';
      setState({ data: null, error: errorMessage, isLoading: false });
      throw error;
    }
  }, []);

  return { ...state, request };
}

// Specific API hooks

export function useCredits() {
  const { data, error, isLoading, request } = useApi<{
    balance: number;
    used: number;
    reserved: number;
    plan: string;
  }>();

  const fetchCredits = useCallback(() => {
    return request('/api/credits/balance');
  }, [request]);

  const purchaseCredits = useCallback((amount: number) => {
    return request('/api/payments/checkout/credits', {
      method: 'POST',
      body: { amount },
    });
  }, [request]);

  return { credits: data, error, isLoading, fetchCredits, purchaseCredits };
}

export function useGeneration() {
  const { data, error, isLoading, request } = useApi<{
    task_id: string;
    status: string;
    result_url?: string;
  }>();

  const generateImage = useCallback((prompt: string, model: string, options: Record<string, unknown> = {}) => {
    return request('/api/v2/generation/generate', {
      method: 'POST',
      body: {
        type: 'image',
        prompt,
        model,
        ...options,
      },
    });
  }, [request]);

  const generateVideo = useCallback((prompt: string, model: string, options: Record<string, unknown> = {}) => {
    return request('/api/v2/generation/generate', {
      method: 'POST',
      body: {
        type: 'video',
        prompt,
        model,
        ...options,
      },
    });
  }, [request]);

  const generateAudio = useCallback((text: string, voice: string, options: Record<string, unknown> = {}) => {
    return request('/api/v2/generation/generate', {
      method: 'POST',
      body: {
        type: 'audio',
        prompt: text,
        model: 'elevenlabs-tts',
        voice,
        ...options,
      },
    });
  }, [request]);

  const getTaskStatus = useCallback((taskId: string) => {
    return request(`/api/v2/generation/tasks/${taskId}`);
  }, [request]);

  return {
    generation: data,
    error,
    isLoading,
    generateImage,
    generateVideo,
    generateAudio,
    getTaskStatus,
  };
}

export function useGallery() {
  const { data, error, isLoading, request } = useApi<{
    items: Array<{
      id: string;
      title: string;
      thumbnail_url: string;
      media_type: string;
      likes_count: number;
      views_count: number;
    }>;
    total: number;
    page: number;
    per_page: number;
  }>();

  const fetchGallery = useCallback((page = 1, category?: string, sort = 'latest') => {
    const params = new URLSearchParams({
      page: page.toString(),
      per_page: '20',
      sort,
    });
    if (category) params.append('category', category);
    
    return request(`/api/gallery/public?${params}`, { requireAuth: false });
  }, [request]);

  const likeItem = useCallback((itemId: string) => {
    return request(`/api/gallery/${itemId}/like`, { method: 'POST' });
  }, [request]);

  return { gallery: data, error, isLoading, fetchGallery, likeItem };
}

export function useContact() {
  const { error, isLoading, request } = useApi<{ success: boolean }>();

  const submitContact = useCallback((data: {
    name: string;
    email: string;
    subject: string;
    message: string;
    type: string;
  }) => {
    return request('/api/contact', {
      method: 'POST',
      body: data,
      requireAuth: false,
    });
  }, [request]);

  return { error, isLoading, submitContact };
}
