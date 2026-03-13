const API_URL = (process.env.NEXT_PUBLIC_API_URL || "http://localhost:5000").replace(/\/$/, "");

type ApiErrorShape = {
  error?: {
    code?: string;
    message?: string | string[];
  };
};

export type AnalysisRequestPayload = {
  communication_text: string;
  channel_type: "sms" | "email" | "url";
  metadata?: {
    domain?: string;
    entity_name?: string;
  };
};

export type FraudSignal = {
  type: string;
  description: string;
  matches?: string[];
};

export type AnalysisResult = {
  analysis_id: string;
  authenticity_score: number;
  raw_score: number;
  breakdown: {
    domain_contribution: number;
    similarity_contribution: number;
    fraud_contribution: number;
  };
  confidence: number;
  explainable_flags: string[];
  fraud_signals: FraudSignal[];
  redacted_text: string;
  registry_match?: Record<string, unknown> | null;
  semantic_similarity: number;
  translation_allowed: boolean;
  processing_time_ms: number;
  channel_type: string;
  created_at: number;
};

export type TranslationPayload = {
  analysis_id: string;
  original_text: string;
  target_lang: string;
};

export type TranslationResult = {
  translation_id: string;
  translated_text: string;
  target_language: string;
  translation_integrity_score: number;
  integrity_status: "HIGH" | "WARNING";
  processing_time_ms: number;
};

export type AppealPayload = {
  analysis_id: string;
  reason: string;
  contact_email: string;
};

export type AppealResponse = {
  message: string;
  appeal_id: string;
  status: string;
  queue_status: string;
};

export type RegistrySearchParams = {
  entity_name?: string;
  domain?: string;
  entity_type?: string;
};

export type RegistryEntry = {
  entity_name?: string;
  domain?: string;
  entity_type?: string;
  confidence?: number;
  [key: string]: unknown;
};

export type RegistrySearchResponse = {
  results: RegistryEntry[];
  count: number;
};

export type MethodologyResponse = {
  scoring_weights: {
    domain_verification: number;
    semantic_similarity: number;
    fraud_detection_penalty: number;
  };
  score_mapping: Record<string, string>;
  translation_threshold: {
    similarity_required_for_integrity: number;
  };
  principles: string[];
  registry_data_source: {
    table_name: string;
    table_status: string;
    item_count: number | null;
    global_secondary_indexes: string[];
  };
};

export type HealthResponse = {
  status: "online" | "degraded";
  mock_mode: boolean;
  services: Record<string, "ok" | "error">;
};

class ApiError extends Error {
  code?: string;

  constructor(message: string, code?: string) {
    super(message);
    this.code = code;
  }
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, {
    cache: "no-store",
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...(init?.headers || {}),
    },
  });

  const raw = await response.text();
  const data = raw ? (JSON.parse(raw) as T & ApiErrorShape) : ({} as T & ApiErrorShape);

  if (!response.ok) {
    const message = Array.isArray(data.error?.message)
      ? data.error?.message.join(", ")
      : data.error?.message || "API request failed";
    throw new ApiError(message, data.error?.code);
  }

  return data;
}

export async function analyzeCommunication(payload: AnalysisRequestPayload) {
  return request<AnalysisResult>("/analyze", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function getAnalysisResult(analysisId: string) {
  return request<AnalysisResult>(`/analyze/${analysisId}`);
}

export async function translateMessage(payload: TranslationPayload) {
  return request<TranslationResult>("/translate", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function submitAppeal(payload: AppealPayload) {
  return request<AppealResponse>("/appeals", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export async function searchRegistry(params: RegistrySearchParams) {
  const query = new URLSearchParams();
  Object.entries(params).forEach(([key, value]) => {
    if (value) {
      query.set(key, value);
    }
  });
  return request<RegistrySearchResponse>(`/registry/search?${query.toString()}`);
}

export async function getMethodology() {
  return request<MethodologyResponse>("/methodology");
}

export async function getHealth() {
  return request<HealthResponse>("/health");
}
