import { NextRequest, NextResponse } from "next/server";

const BACKEND_API_URL = (process.env.BACKEND_API_URL || "http://127.0.0.1:5000").replace(/\/$/, "");
const CORS_ALLOWED_ORIGINS = (process.env.CORS_ALLOWED_ORIGINS || "*")
  .split(",")
  .map((origin) => origin.trim())
  .filter(Boolean);
const FALLBACK_METHODOLOGY = {
  scoring_weights: {
    domain_verification: 0.4,
    semantic_similarity: 0.35,
    fraud_detection_penalty: 0.25,
  },
  score_mapping: {
    "5": ">= 0.80",
    "4": "0.60 - 0.79",
    "3": "0.40 - 0.59",
    "2": "0.20 - 0.39",
    "1": "< 0.20",
  },
  translation_threshold: {
    similarity_required_for_integrity: 0.75,
  },
  principles: [
    "Citizen empowerment",
    "Political neutrality",
    "Explainable scoring",
    "No enforcement of content",
    "Human oversight via appeals",
    "Privacy protection with PII redaction",
  ],
  registry_data_source: {
    table_name: "InstitutionalRegistry",
    table_status: "unavailable",
    item_count: null,
    global_secondary_indexes: [],
  },
};

const FALLBACK_HEALTH = {
  status: "degraded",
  mock_mode: true,
  services: {
    dynamodb: "error",
    s3: "error",
    bedrock: "error",
    comprehend: "error",
    sqs: "error",
  },
};

function buildTargetUrl(pathSegments: string[], request: NextRequest) {
  const path = pathSegments.join("/");
  const search = request.nextUrl.search || "";
  return `${BACKEND_API_URL}/${path}${search}`;
}

function resolveAllowedOrigin(request: NextRequest) {
  const requestOrigin = request.headers.get("origin");
  if (CORS_ALLOWED_ORIGINS.includes("*")) {
    return "*";
  }
  if (requestOrigin && CORS_ALLOWED_ORIGINS.includes(requestOrigin)) {
    return requestOrigin;
  }
  return CORS_ALLOWED_ORIGINS[0] || "*";
}

function corsHeaders(request: NextRequest, contentType = "application/json") {
  return {
    "content-type": contentType,
    "Access-Control-Allow-Origin": resolveAllowedOrigin(request),
    Vary: "Origin",
    "Access-Control-Allow-Headers": "Content-Type, Authorization, X-Request-Id",
    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
  };
}

function fallbackResponse(request: NextRequest, path: string[]) {
  const joined = path.join("/");
  if (joined === "health") {
    return NextResponse.json(FALLBACK_HEALTH, {
      status: 200,
      headers: corsHeaders(request),
    });
  }
  if (joined === "methodology") {
    return NextResponse.json(FALLBACK_METHODOLOGY, {
      status: 200,
      headers: corsHeaders(request),
    });
  }
  return null;
}

async function proxy(request: NextRequest, context: { params: Promise<{ path: string[] }> }) {
  const { path } = await context.params;
  const targetUrl = buildTargetUrl(path, request);

  const upstreamHeaders = new Headers();
  request.headers.forEach((value, key) => {
    if (!["host", "connection", "content-length", "origin", "referer", "cookie"].includes(key.toLowerCase())) {
      upstreamHeaders.set(key, value);
    }
  });

  const hasBody = !["GET", "HEAD"].includes(request.method);
  try {
    const upstreamResponse = await fetch(targetUrl, {
      method: request.method,
      headers: upstreamHeaders,
      body: hasBody ? await request.text() : undefined,
      cache: "no-store",
    });

    if (!upstreamResponse.ok && request.method === "GET") {
      const fallback = fallbackResponse(request, path);
      if (fallback && [403, 404, 500, 502, 503, 504].includes(upstreamResponse.status)) {
        fallback.headers.set("x-ccai-proxy-fallback", `upstream-${upstreamResponse.status}`);
        return fallback;
      }
    }

    const responseHeaders = new Headers();
    const contentType = upstreamResponse.headers.get("content-type");
    if (contentType) {
      responseHeaders.set("content-type", contentType);
    }
    responseHeaders.set("Access-Control-Allow-Origin", resolveAllowedOrigin(request));
    responseHeaders.set("Vary", "Origin");
    responseHeaders.set("Access-Control-Allow-Headers", "Content-Type, Authorization, X-Request-Id");
    responseHeaders.set("Access-Control-Allow-Methods", "GET, POST, OPTIONS");

    return new NextResponse(await upstreamResponse.text(), {
      status: upstreamResponse.status,
      headers: responseHeaders,
    });
  } catch {
    const fallback = request.method === "GET" ? fallbackResponse(request, path) : null;
    if (fallback) {
      fallback.headers.set("x-ccai-proxy-fallback", "network-error");
      return fallback;
    }
    return NextResponse.json(
      {
        error: {
          code: "UPSTREAM_UNAVAILABLE",
          message: "Backend service is unavailable.",
        },
      },
      {
        status: 503,
        headers: corsHeaders(request),
      }
    );
  }
}

export async function GET(request: NextRequest, context: { params: Promise<{ path: string[] }> }) {
  return proxy(request, context);
}

export async function POST(request: NextRequest, context: { params: Promise<{ path: string[] }> }) {
  return proxy(request, context);
}

export async function OPTIONS(request: NextRequest) {
  return new NextResponse(null, {
    status: 200,
    headers: corsHeaders(request, "text/plain"),
  });
}
