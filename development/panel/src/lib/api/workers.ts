import { createApiClient } from "./client";
import { createBotApi, type BotApi } from "./bots";
import { createLogsApi, type LogsApi } from "./logs";
import type { WorkerConfig } from "@/lib/types";

export interface WorkerApi {
  health: {
    check(): Promise<{ status: "ok"; timestamp: string }>;
  };
  bots: BotApi;
  logs: LogsApi;
}

export function createWorkerApi(worker: WorkerConfig): WorkerApi {
  const client = createApiClient({
    baseUrl: worker.url,
    secret: worker.secret,
  });

  return {
    health: {
      check: () => client.request<{ status: "ok"; timestamp: string }>("/health", { skipAuth: true }),
    },
    bots: createBotApi({
      baseUrl: worker.url,
      secret: worker.secret,
    }),
    logs: createLogsApi({
      baseUrl: worker.url,
      secret: worker.secret,
    }),
  };
}
