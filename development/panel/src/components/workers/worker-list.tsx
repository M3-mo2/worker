"use client";

import { useEffect, useState, useCallback } from "react";
import { useWorkersStore } from "@/lib/store/workers";
import { checkHealthRaw } from "@/lib/api/health";
import type { WorkerHealth } from "@/lib/types";
import { WorkerCard } from "@/components/workers/worker-card";
import { Button } from "@/components/ui/button";
import { RefreshCw, Server } from "lucide-react";
import { toast } from "@/hooks/use-toast";

export function WorkerList() {
  const workers = useWorkersStore((s) => s.workers);
  const selectedWorkerId = useWorkersStore((s) => s.selectedWorkerId);
  const setSelectedWorker = useWorkersStore((s) => s.setSelectedWorker);
  const [healthMap, setHealthMap] = useState<Map<string, WorkerHealth>>(new Map());
  const [isRefreshing, setIsRefreshing] = useState(false);

  const checkAllHealth = useCallback(async (): Promise<Map<string, WorkerHealth>> => {
    if (workers.length === 0) return new Map();

    const newMap = new Map<string, WorkerHealth>();
    const promises = workers.map(async (w) => {
      const result = await checkHealthRaw(w.url);
      return {
        id: w.id,
        workerId: w.id,
        health: (result.healthy ? "healthy" : "unhealthy") as WorkerHealth["health"],
        responseTime: result.responseTime,
        timestamp: new Date().toISOString(),
      };
    });

    const results = await Promise.allSettled(promises);
    results.forEach((res) => {
      if (res.status === "fulfilled") {
        newMap.set(res.value.id, res.value);
      }
    });
    return newMap;
  }, [workers]);

  useEffect(() => {
    let cancelled = false;
    const run = async () => {
      const result = await checkAllHealth();
      if (!cancelled) setHealthMap(result);
    };
    run();
    const interval = setInterval(run, 15000);
    return () => {
      cancelled = true;
      clearInterval(interval);
    };
  }, [checkAllHealth]);

  const handleRefresh = async () => {
    setIsRefreshing(true);
    const result = await checkAllHealth();
    setHealthMap(result);
    setIsRefreshing(false);
    toast.success("Health check complete", { description: "All worker statuses have been refreshed." });
  };

  if (workers.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center gap-4 py-12">
        <Server className="h-12 w-12 text-muted-foreground/40" />
        <div className="text-center">
          <h3 className="text-lg font-semibold">No workers configured</h3>
          <p className="text-sm text-muted-foreground max-w-sm">
            Add your first Telegram Bot Hosting Worker to get started. Click the
            &quot;+&quot; button in the sidebar.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="text-lg font-semibold">Workers ({workers.length})</h2>
        <Button
          variant="outline"
          size="sm"
          onClick={handleRefresh}
          disabled={isRefreshing}
        >
          <RefreshCw className={`h-4 w-4 ${isRefreshing ? "animate-spin" : ""}`} />
        </Button>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {workers.map((worker) => (
          <WorkerCard
            key={worker.id}
            worker={worker}
            health={healthMap.get(worker.id)}
            isSelected={worker.id === selectedWorkerId}
            onSelect={(w) => setSelectedWorker(w.id)}
          />
        ))}
      </div>
    </div>
  );
}
