import { createApiClient } from "./client";

export interface LogsApiDeps {
  baseUrl: string;
  secret: string;
  timeout?: number;
}

export interface FetchLogsParams {
  userId: string;
  lines?: number;
}

export interface LogsApi {
  fetchLogs(params: FetchLogsParams): Promise<string>;
}

export function createLogsApi(worker: LogsApiDeps): LogsApi {
  const client = createApiClient({
    baseUrl: worker.baseUrl,
    secret: worker.secret,
    timeout: worker.timeout,
  });

  return {
    fetchLogs: async (params: FetchLogsParams): Promise<string> => {
      const searchParams = new URLSearchParams();
      if (params.lines !== undefined) {
        searchParams.set("lines", String(params.lines));
      }
      const query = searchParams.toString();
      const path = `/logs/${encodeURIComponent(params.userId)}${query ? `?${query}` : ""}`;
      return client.request<string>(path, { method: "GET" });
    },
  };
}
