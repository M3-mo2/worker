export interface WorkerConfig {
  id: string;
  name: string;
  url: string;
  secret: string;
  createdAt: string;
}

export type BotStatus = "running" | "stopped" | "not_found";

export interface WorkerBotStatus {
  user_id: string;
  status: BotStatus;
  created_at: string;
}

export interface HealthCheck {
  status: "ok";
  timestamp: string;
}

export interface ErrorResponse {
  detail: string;
}

export type HealthStatus = "healthy" | "unhealthy" | "unknown";

export interface WorkerHealth {
  workerId: string;
  health: HealthStatus;
  timestamp: string;
  responseTime?: number;
}

export interface CreateApiClientOptions {
  baseUrl: string;
  secret: string;
  timeout?: number;
}
