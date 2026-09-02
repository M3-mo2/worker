"use client";

import { useState, useEffect, useCallback } from "react";
import { useWorkersStore } from "@/lib/store/workers";
import { createWorkerApi } from "@/lib/api/workers";
import type { WorkerBotStatus } from "@/lib/types";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { LoadingSpinner } from "@/components/ui/loading-spinner";
import { Play, Pause, XCircle, AlertCircle, RefreshCw } from "lucide-react";
import { formatTimestamp } from "@/lib/utils/format";
import { cn } from "@/lib/utils/cn";

interface BotStatusDisplayProps {
  workerId: string;
  userId: string;
  onStatusChanged?: () => void;
}

function StatusIcon({ status }: { status: WorkerBotStatus["status"] }) {
  switch (status) {
    case "running":
      return <Play className="h-4 w-4 text-green-500" />;
    case "stopped":
      return <Pause className="h-4 w-4 text-yellow-500" />;
    case "not_found":
      return <XCircle className="h-4 w-4 text-red-500" />;
    default:
      return <AlertCircle className="h-4 w-4 text-muted-foreground" />;
  }
}

function StatusBadge({ status }: { status: WorkerBotStatus["status"] }) {
  const config = {
    running: { variant: "success" as const, label: "Running", icon: <Play className="h-3 w-3" /> },
    stopped: { variant: "warning" as const, label: "Stopped", icon: <Pause className="h-3 w-3" /> },
    not_found: { variant: "destructive" as const, label: "Not Found", icon: <XCircle className="h-3 w-3" /> },
  }[status];

  return (
    <Badge variant={config.variant} size="sm" className="gap-1">
      {config.icon}
      {config.label}
    </Badge>
  );
}

export function BotStatusDisplay({ workerId, userId, onStatusChanged }: BotStatusDisplayProps) {
  const worker = useWorkersStore((s) => s.workers.find((w) => w.id === workerId));
  const [status, setStatus] = useState<WorkerBotStatus | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isRefreshing, setIsRefreshing] = useState(false);

  const fetchStatus = useCallback(async () => {
    if (!worker || !userId) return;
    setError(null);
    try {
      const api = createWorkerApi(worker);
      const result = await api.bots.getStatus(userId);
      setStatus(result);
    } catch (err) {
      const error = err as Error & { status?: number };
      if (error.status === 404) {
        setStatus({ user_id: userId, status: "not_found", created_at: "" });
      } else {
        setError(error.message);
      }
    }
  }, [worker, userId]);

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect
    void fetchStatus();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [workerId, userId]);

  const handleRefresh = async () => {
    setIsRefreshing(true);
    await fetchStatus();
    setIsRefreshing(false);
    onStatusChanged?.();
  };

  if (!worker) return null;

  const showLoading = status === null && !error && !isRefreshing;

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <div>
            <CardTitle>Bot Status</CardTitle>
            <CardDescription>Real-time status for user ID {userId}</CardDescription>
          </div>
          <Button
            variant="ghost"
            size="sm"
            className="h-7 w-7"
            onClick={handleRefresh}
            disabled={isRefreshing}
            aria-label="Refresh status"
          >
            <RefreshCw className={cn("h-4 w-4", isRefreshing && "animate-spin")} />
          </Button>
        </div>
      </CardHeader>
      <CardContent>
        {isRefreshing ? (
          <div className="py-8 text-center">
            <LoadingSpinner className="mx-auto mb-2" />
            <p className="text-sm text-muted-foreground">Refreshing…</p>
          </div>
        ) : showLoading ? (
          <div className="py-8 text-center">
            <LoadingSpinner className="mx-auto mb-2" />
            <p className="text-sm text-muted-foreground">Loading status…</p>
          </div>
        ) : status ? (
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <StatusIcon status={status.status} />
              <div>
                <p className="font-medium capitalize">{status.status.replace("_", " ")}</p>
                {status.created_at && (
                  <p className="text-sm text-muted-foreground">
                    Created: {formatTimestamp(status.created_at)}
                  </p>
                )}
              </div>
            </div>
            <StatusBadge status={status.status} />
          </div>
        ) : error ? (
          <div className="flex items-center gap-2 text-destructive">
            <AlertCircle className="h-4 w-4" />
            {error}
          </div>
        ) : (
          <p className="text-sm text-muted-foreground">Status not available.</p>
        )}
      </CardContent>
    </Card>
  );
}
