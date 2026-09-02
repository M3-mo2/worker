"use client";

import { useEffect, useState, useCallback } from "react";
import { useWorkersStore } from "@/lib/store/workers";
import { checkHealthRaw } from "@/lib/api/health";
import type { WorkerHealth } from "@/lib/types";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { LoadingSpinner } from "@/components/ui/loading-spinner";
import { RefreshCw, CheckCircle, XCircle, Clock, Server, AlertCircle } from "lucide-react";
import { cn } from "@/lib/utils/cn";
import { formatResponseTime } from "@/lib/utils/format";
import { toast } from "@/hooks/use-toast";

interface HealthResult {
  workerId: string;
  name: string;
  url: string;
  health: WorkerHealth["health"];
  responseTime: number;
  error?: string;
  timestamp: string;
}

export function HealthDashboard() {
  const workers = useWorkersStore((s) => s.workers);
  const [results, setResults] = useState<HealthResult[]>([]);
  const [isChecking, setIsChecking] = useState(false);

  const runChecks = useCallback(async () => {
    if (workers.length === 0) return [];

    const newResults: HealthResult[] = [];

    for (const w of workers) {
      const result = await checkHealthRaw(w.url);
      newResults.push({
        workerId: w.id,
        name: w.name,
        url: w.url,
        health: (result.healthy ? "healthy" : "unhealthy") as WorkerHealth["health"],
        responseTime: result.responseTime,
        error: result.error,
        timestamp: new Date().toISOString(),
      });
    }

    return newResults;
  }, [workers]);

  const handleRefresh = useCallback(async () => {
    setIsChecking(true);
    const newResults = await runChecks();
    setResults(newResults);
    setIsChecking(false);
    toast.success("Health checks complete", {
      description: `${newResults.filter((r) => r.health === "healthy").length} of ${newResults.length} workers healthy.`,
    });
  }, [runChecks]);

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect
    void handleRefresh();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [workers.length]);

  const healthyCount = results.filter((r) => r.health === "healthy").length;
  const unhealthyCount = results.filter((r) => r.health === "unhealthy").length;

  if (workers.length === 0) {
    return (
      <Card>
        <CardContent className="py-8 text-center">
          <Server className="mx-auto h-10 w-10 text-muted-foreground/40 mb-3" />
          <p className="text-muted-foreground">No workers configured yet.</p>
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-lg font-semibold">Health Dashboard</h2>
          <p className="text-sm text-muted-foreground">
            Live health status for all configured workers
          </p>
        </div>
        <Button variant="outline" size="sm" onClick={runChecks} disabled={isChecking}>
          <RefreshCw className={cn("h-4 w-4", isChecking && "animate-spin")} />
        </Button>
      </div>

      <div className="flex gap-4">
        <Card className="flex-1">
          <CardContent className="pt-6">
            <div className="flex items-center gap-2">
              <CheckCircle className="h-5 w-5 text-green-500" />
              <span className="text-2xl font-bold">{healthyCount}</span>
            </div>
            <p className="text-sm text-muted-foreground">Healthy</p>
          </CardContent>
        </Card>
        <Card className="flex-1">
          <CardContent className="pt-6">
            <div className="flex items-center gap-2">
              <XCircle className="h-5 w-5 text-red-500" />
              <span className="text-2xl font-bold">{unhealthyCount}</span>
            </div>
            <p className="text-sm text-muted-foreground">Unhealthy</p>
          </CardContent>
        </Card>
        <Card className="flex-1">
          <CardContent className="pt-6">
            <div className="flex items-center gap-2">
              <Clock className="h-5 w-5 text-muted-foreground" />
              <span className="text-2xl font-bold">
                {results.length > 0
                  ? `${Math.round(results.reduce((a, r) => a + r.responseTime, 0) / results.length)}ms`
                  : "—"}
              </span>
            </div>
            <p className="text-sm text-muted-foreground">Avg Response</p>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Worker Details</CardTitle>
          <CardDescription>
            {workers.length} workers monitored
          </CardDescription>
        </CardHeader>
        <CardContent>
          {isChecking && results.length === 0 ? (
            <div className="py-8 text-center">
              <LoadingSpinner className="mx-auto mb-2" />
              <p className="text-sm text-muted-foreground">Running health checks…</p>
            </div>
          ) : (
            <div className="space-y-3">
              {results.map((r) => (
                <div
                  key={r.workerId}
                  className="flex items-center justify-between rounded-md border border-border/50 p-3"
                >
                  <div className="flex items-center gap-3">
                    <div
                      className={cn(
                        "flex h-8 w-8 shrink-0 items-center justify-center rounded-lg",
                        r.health === "healthy" ? "bg-green-500/10" : "bg-red-500/10"
                      )}
                    >
                      {r.health === "healthy" ? (
                        <CheckCircle className="h-4 w-4 text-green-500" />
                      ) : (
                        <XCircle className="h-4 w-4 text-red-500" />
                      )}
                    </div>
                    <div>
                      <p className="font-medium">{r.name}</p>
                      <p className="text-sm text-muted-foreground break-all">{r.url}</p>
                      {r.error && (
                        <p className="text-xs text-destructive mt-0.5 flex items-start gap-1">
                          <AlertCircle className="h-3 w-3 shrink-0 mt-0.5" />
                          {r.error}
                        </p>
                      )}
                    </div>
                  </div>
                  <div className="flex items-center gap-3">
                    <div className="text-right">
                      <Badge
                        variant={r.health === "healthy" ? "success" : "destructive"}
                        size="sm"
                      >
                        {r.health === "healthy" ? "Healthy" : "Unhealthy"}
                      </Badge>
                      <p className="text-xs text-muted-foreground mt-1">
                        {formatResponseTime(r.responseTime)}
                      </p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
