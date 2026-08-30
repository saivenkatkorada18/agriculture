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

const API_BASE = '/api';

export class ApiError extends Error {
  status: number;
  constructor(message: string, status: number) {
    super(message);
    this.status = status;
    this.name = 'ApiError';
  }
}

async function handleResponse<T>(res: Response): Promise<T> {
  if (!res.ok) {
    let errorDetail = 'Network response was not ok';
    try {
      const errJson = await res.json();
      errorDetail = errJson.detail || errJson.message || errorDetail;
    } catch {
      // ignore
    }
    throw new ApiError(errorDetail, res.status);
  }
  return res.json() as Promise<T>;
}

export const api = {
  // Health & Stats
  async getHealth(): Promise<SystemHealth> {
    const res = await fetch(`${API_BASE}/health`);
    return handleResponse<SystemHealth>(res);
  },

  async getStats(): Promise<DashboardStats> {
    const res = await fetch(`${API_BASE}/analyses/stats/summary`);
    return handleResponse<DashboardStats>(res);
  },

  // Image Analysis
  async analyzePlant(file: File | Blob): Promise<PlantAnalysisResult> {
    const formData = new FormData();
    formData.append('file', file, 'leaf.jpg');

    const res = await fetch(`${API_BASE}/analyze/plant`, {
      method: 'POST',
      body: formData,
    });
    return handleResponse<PlantAnalysisResult>(res);
  },

  async analyzeSoil(file: File | Blob): Promise<SoilAnalysisResult> {
    const formData = new FormData();
    formData.append('file', file, 'soil.jpg');

    const res = await fetch(`${API_BASE}/analyze/soil`, {
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

    const res = await fetch(`${API_BASE}/analyses?${query.toString()}`);
    return handleResponse<AnalysisSummary[]>(res);
  },

  async getAnalysisById(id: string): Promise<PlantAnalysisResult | SoilAnalysisResult> {
    const res = await fetch(`${API_BASE}/analyses/${id}`);
    return handleResponse<PlantAnalysisResult | SoilAnalysisResult>(res);
  },

  async deleteAnalysis(id: string): Promise<{ status: string }> {
    const res = await fetch(`${API_BASE}/analyses/${id}`, {
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
    const res = await fetch(`${API_BASE}/chat`, {
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
    const res = await fetch(`${API_BASE}/crops`);
    return handleResponse(res);
  },
};
