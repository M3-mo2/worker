import { ApiError } from "./types";
import type { CreateApiClientOptions } from "@/lib/types";

export const DEFAULT_TIMEOUT = 10000;

export interface FetchRequestInit extends RequestInit {
  skipAuth?: boolean;
}

function mergeSignals(...signals: (AbortSignal | undefined)[]) {
  const active = signals.filter((s): s is AbortSignal => s != null);
  if (active.length === 0) return undefined;
  if (active.length === 1) return active[0];
  const controller = new AbortController();
  for (const signal of active) {
    if (signal.aborted) {
      controller.abort();
      break;
    }
    signal.addEventListener("abort", () => controller.abort(), { once: true });
  }
  return controller.signal;
}

export class ApiClient {
  private baseUrl: string;
  private secret: string;
  private timeout: number;

  constructor(options: CreateApiClientOptions) {
    this.baseUrl = options.baseUrl.endsWith("/") ? options.baseUrl.slice(0, -1) : options.baseUrl;
    this.secret = options.secret;
    this.timeout = options.timeout ?? DEFAULT_TIMEOUT;
  }

  async request<T>(path: string, init: FetchRequestInit = {}): Promise<T> {
    const { skipAuth, headers: initHeaders, signal: initSignal, ...restInit } = init;

    const url = this.baseUrl + path;
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), this.timeout);

    const combinedHeaders: Record<string, string> = {
      ...(skipAuth ? {} : { "X-Internal-Secret": this.secret }),
    };

    if (initHeaders) {
      if (initHeaders instanceof Headers) {
        initHeaders.forEach((value, key) => {
          combinedHeaders[key] = value;
        });
      } else if (Array.isArray(initHeaders)) {
        for (const [key, value] of initHeaders) {
          combinedHeaders[key] = value;
        }
      } else {
        Object.assign(combinedHeaders, initHeaders);
      }
    }

    const signal = mergeSignals(controller.signal, initSignal ?? undefined);

    let response: Response;
    try {
      response = await fetch(url, {
        ...restInit,
        headers: combinedHeaders,
        signal,
      });
    } catch (err) {
      if (err instanceof Error && err.name === "AbortError") {
        throw new ApiError(408, "Request timed out — the worker may be down or unresponsive");
      }
      throw new ApiError(0, `Network error: ${(err as Error).message || "Failed to connect to worker"}`);
    } finally {
      clearTimeout(timeoutId);
    }

    const contentType = response.headers.get("content-type");

    if (!response.ok) {
      let detail = `HTTP ${response.status}`;
      if (contentType?.includes("application/json")) {
        try {
          const errorBody = (await response.json()) as { detail?: string };
          if (errorBody.detail) detail = errorBody.detail;
        } catch {
          // not JSON, use default detail
        }
      }
      throw new ApiError(response.status, detail);
    }

    if (contentType?.includes("text/plain")) {
      return (await response.text()) as unknown as T;
    }

    if (contentType?.includes("application/json")) {
      return (await response.json()) as T;
    }

    const text = await response.text();
    try {
      return JSON.parse(text) as T;
    } catch {
      return text as unknown as T;
    }
  }
}

export function createApiClient(options: CreateApiClientOptions): ApiClient {
  return new ApiClient(options);
}
