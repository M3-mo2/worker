import { createApiClient } from "./client";
import type { WorkerBotStatus } from "@/lib/types";

export interface BotApiDeps {
  baseUrl: string;
  secret: string;
  timeout?: number;
}

export function createBotApi(worker: BotApiDeps) {
  const client = createApiClient({
    baseUrl: worker.baseUrl,
    secret: worker.secret,
    timeout: worker.timeout,
  });

  return {
    deploy(userId: string, botToken: string, file: File): Promise<void> {
      const formData = new FormData();
      formData.append("user_id", userId);
      formData.append("bot_token", botToken);
      formData.append("file", file);
      return client.request<void>("/deploy", {
        method: "POST",
        body: formData,
      });
    },

    stop(userId: string): Promise<void> {
      return client.request<void>("/stop", {
        method: "POST",
        body: JSON.stringify({ user_id: userId }),
        headers: { "Content-Type": "application/json" },
      });
    },

    deleteBot(userId: string): Promise<void> {
      return client.request<void>("/delete", {
        method: "POST",
        body: JSON.stringify({ user_id: userId }),
        headers: { "Content-Type": "application/json" },
      });
    },

    deleteFile(userId: string, filename: string): Promise<void> {
      return client.request<void>("/files/delete", {
        method: "POST",
        body: JSON.stringify({ user_id: userId, filename }),
        headers: { "Content-Type": "application/json" },
      });
    },

    getStatus(userId: string): Promise<WorkerBotStatus> {
      return client.request<WorkerBotStatus>(`/status/${encodeURIComponent(userId)}`, {
        method: "GET",
      });
    },
  };
}

export type BotApi = ReturnType<typeof createBotApi>;
