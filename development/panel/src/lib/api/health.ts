import { ApiClient, DEFAULT_TIMEOUT } from "./client";
import type { HealthCheck, WorkerHealth } from "@/lib/types";

export async function checkHealth(
  baseUrl: string,
  secret?: string,
  timeout?: number
): Promise<WorkerHealth & { status: HealthCheck }> {
  const client = new ApiClient({
    baseUrl,
    secret: secret ?? "",
    timeout,
  });

  const start = Date.now();
  const result = await client.request<HealthCheck>("/health", {
    skipAuth: true,
    method: "GET",
  });
  const responseTime = Date.now() - start;

  return {
    status: result,
    health: "healthy",
    responseTime,
    timestamp: result.timestamp,
  } as WorkerHealth & { status: HealthCheck };
}

export interface HealthCheckOptions {
  secret?: string;
  timeout?: number;
  signal?: AbortSignal;
}

export async function checkHealthRaw(
  baseUrl: string,
  options?: HealthCheckOptions
): Promise<{ healthy: boolean; responseTime: number; status?: HealthCheck; error?: string }> {
  const start = Date.now();
  const client = new ApiClient({
    baseUrl,
    secret: options?.secret ?? "",
    timeout: options?.timeout ?? DEFAULT_TIMEOUT,
  });

  try {
    const status = await client.request<HealthCheck>("/health", {
      skipAuth: true,
      method: "GET",
      signal: options?.signal,
    });
    const responseTime = Date.now() - start;
    return { healthy: status.status === "ok", responseTime, status };
  } catch (err) {
    const responseTime = Date.now() - start;
    return { healthy: false, responseTime, error: (err as Error).message };
  }
}

export function createHealthApi(worker: { url: string; secret: string }): { check(): Promise<HealthCheck> } {
  const client = new ApiClient({ baseUrl: worker.url, secret: worker.secret });
  return {
    check: () => client.request<HealthCheck>("/health", { skipAuth: true }),
  };
}
