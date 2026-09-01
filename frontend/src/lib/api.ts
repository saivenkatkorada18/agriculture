/**
 * API Client for Soil & Crop Health Analyzer
 */
import {
  PlantAnalysisResult,
  SoilAnalysisResult,
  AnalysisSummary,
  DashboardStats,
  ChatMessage,
  SystemHealth,
} from '../types';

const API_BASE = (import.meta.env.VITE_API_URL as string) || '/api';

export class ApiError extends Error {
  status: number;
  constructor(message: string, status: number) {
    super(message);
    this.status = status;
    this.name = 'ApiError';
  }
}

async function safeFetch(url: string, init?: RequestInit): Promise<Response> {
  try {
    return await fetch(url, init);
  } catch (err: any) {
    throw new ApiError(
      'Cannot connect to backend server. Please ensure the backend is running on http://127.0.0.1:8000 (e.g., using run_app.bat).',
      0
    );
  }
}

async function handleResponse<T>(res: Response): Promise<T> {
  if (!res.ok) {
    let errorDetail = `Server Error (${res.status})`;
    try {
      const text = await res.text();
      try {
        const errJson = JSON.parse(text);
        errorDetail = errJson.detail || errJson.message || errorDetail;
      } catch {
        if (text && text.length < 200) {
          errorDetail = text;
        }
      }
    } catch {
      // ignore
    }
    if (res.status === 502 || res.status === 504) {
      errorDetail = 'Backend server (port 8000) is unreachable. Please run "run_app.bat" or start Uvicorn.';
    }
    throw new ApiError(errorDetail, res.status);
  }
  return res.json() as Promise<T>;
}

export const api = {
  // Health & Stats
  async getHealth(): Promise<SystemHealth> {
    const res = await safeFetch(`${API_BASE}/health`);
    return handleResponse<SystemHealth>(res);
  },

  async getStats(): Promise<DashboardStats> {
    const res = await safeFetch(`${API_BASE}/analyses/stats/summary`);
    return handleResponse<DashboardStats>(res);
  },

  // Image Analysis
  async analyzePlant(file: File | Blob): Promise<PlantAnalysisResult> {
    const formData = new FormData();
    formData.append('file', file, 'leaf.jpg');

    const res = await safeFetch(`${API_BASE}/analyze/plant`, {
      method: 'POST',
      body: formData,
    });
    return handleResponse<PlantAnalysisResult>(res);
  },

  async analyzeSoil(file: File | Blob): Promise<SoilAnalysisResult> {
    const formData = new FormData();
    formData.append('file', file, 'soil.jpg');

    const res = await safeFetch(`${API_BASE}/analyze/soil`, {
      method: 'POST',
      body: formData,
    });
    return handleResponse<SoilAnalysisResult>(res);
  },

  // History & Details
  async getAnalyses(params?: {
    type?: string;
    status?: string;
    query?: string;
    limit?: number;
    offset?: number;
  }): Promise<AnalysisSummary[]> {
    const query = new URLSearchParams();
    if (params?.type && params.type !== 'all') query.append('analysis_type', params.type);
    if (params?.status && params.status !== 'all') query.append('status', params.status);
    if (params?.query) query.append('q', params.query);
    if (params?.limit) query.append('limit', params.limit.toString());
    if (params?.offset) query.append('offset', params.offset.toString());

    const res = await safeFetch(`${API_BASE}/analyses?${query.toString()}`);
    return handleResponse<AnalysisSummary[]>(res);
  },

  async getAnalysisById(id: string): Promise<PlantAnalysisResult | SoilAnalysisResult> {
    const res = await safeFetch(`${API_BASE}/analyses/${id}`);
    return handleResponse<PlantAnalysisResult | SoilAnalysisResult>(res);
  },

  async deleteAnalysis(id: string): Promise<{ status: string }> {
    const res = await safeFetch(`${API_BASE}/analyses/${id}`, {
      method: 'DELETE',
    });
    return handleResponse<{ status: string }>(res);
  },

  // AI Farming Assistant Chat
  async sendChatMessage(payload: {
    message: string;
    session_id?: string;
    context_crop?: string;
    context_disease?: string;
  }): Promise<{
    session_id: string;
    message: string;
    role: string;
    suggested_actions: string[];
    related_topics: string[];
    disclaimer: string;
    created_at: string;
  }> {
    const res = await safeFetch(`${API_BASE}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    });
    return handleResponse(res);
  },

  // Crop Encyclopedia
  async getCropEncyclopedia(): Promise<Record<string, any>> {
    const res = await safeFetch(`${API_BASE}/crops`);
    return handleResponse(res);
  },
};

