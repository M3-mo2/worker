"use client";

import { Plus, Server, Trash2, Edit3 } from "lucide-react";
import { useEffect, useState } from "react";
import { useWorkers } from "@/lib/store/workers";
import { checkHealthRaw } from "@/lib/api/health";
import { WorkerConfig, WorkerHealth } from "@/lib/types";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils/cn";
import { AddWorkerForm } from "@/components/workers/add-worker-form";
import { EditWorkerForm } from "@/components/workers/edit-worker-form";
import { Tooltip, TooltipTrigger, TooltipContent, TooltipProvider } from "@/components/ui/tooltip";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
  DialogDescription,
} from "@/components/ui/dialog";

interface SidebarProps {
  className?: string;
}

export function Sidebar({ className }: SidebarProps) {
  const { workers, selectedWorkerId, setSelectedWorker, removeWorker } = useWorkers();
  const [healthMap, setHealthMap] = useState<Map<string, WorkerHealth>>(new Map());
  const [isAddOpen, setIsAddOpen] = useState(false);
  const [editingWorker, setEditingWorker] = useState<WorkerConfig | null>(null);
  const [deletingWorker, setDeletingWorker] = useState<WorkerConfig | null>(null);

  useEffect(() => {
    const controller = new AbortController();
    let cancelled = false;
    const checkAll = async () => {
      const results = await Promise.all(
        workers.map(async (w) => {
          const result = await checkHealthRaw(w.url, { signal: controller.signal });
          return { id: w.id, ...result };
        })
      );
      if (!cancelled) {
        setHealthMap(
          new Map(
            results.map((r) => [
              r.id,
              {
                workerId: r.id,
                health: (r.healthy ? "healthy" : "unhealthy") as WorkerHealth["health"],
                responseTime: r.responseTime,
                timestamp: new Date().toISOString(),
              },
            ])
          )
        );
      }
    };
    checkAll();
    const interval = setInterval(checkAll, 15000);
    return () => {
      controller.abort();
      cancelled = true;
      clearInterval(interval);
    };
  }, [workers]);

  const handleRemove = (worker: WorkerConfig) => {
    removeWorker(worker.id);
    setDeletingWorker(null);
    setSelectedWorker(workers.find((w) => w.id !== worker.id)?.id ?? null);
  };

  const handleSelect = (worker: WorkerConfig) => {
    setSelectedWorker(worker.id);
  };

  return (
    <TooltipProvider delayDuration={300}>
      <aside
        className={cn(
          "flex h-screen w-72 flex-col gap-4 overflow-y-auto overflow-x-hidden border-r bg-card p-4 text-sm",
          className
        )}
      >
        <div className="flex items-center justify-between">
          <h2 className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
            Workers
          </h2>
          <Tooltip>
            <TooltipTrigger asChild>
              <Button
                variant="ghost"
                size="sm"
                className="h-6 w-6"
                onClick={() => setIsAddOpen(true)}
              >
                <Plus className="h-4 w-4" />
              </Button>
            </TooltipTrigger>
            <TooltipContent side="right">
              <p>Add worker</p>
            </TooltipContent>
          </Tooltip>
        </div>

        {workers.length === 0 ? (
          <div className="flex flex-col items-center justify-center gap-3 py-8 text-center">
            <Server className="h-10 w-10 text-muted-foreground/50" />
            <p className="text-sm text-muted-foreground">No workers configured</p>
            <Button size="sm" onClick={() => setIsAddOpen(true)}>
              Add your first worker
            </Button>
          </div>
        ) : (
          <nav className="flex flex-col gap-2 overflow-y-auto">
            {workers.map((worker) => {
              const health = healthMap.get(worker.id);
              const isSelected = worker.id === selectedWorkerId;
              const isUnhealthy = health?.health === "unhealthy";

              return (
                <div key={worker.id} className="group relative">
                  <button
                    type="button"
                    onClick={() => handleSelect(worker)}
                    className={cn(
                      "flex w-full items-center gap-2.5 rounded-md border p-2.5 text-left transition-all",
                      isSelected
                        ? "border-primary bg-primary/5 shadow-sm"
                        : "border-transparent hover:bg-accent",
                      isUnhealthy && !isSelected && "border-destructive/30",
                    )}
                  >
                    <span
                      className={cn(
                        "flex h-2.5 w-2.5 shrink-0 rounded-full",
                        health?.health === "healthy"
                          ? "bg-green-500"
                          : health?.health === "unhealthy"
                            ? "bg-red-500"
                            : "bg-yellow-500 animate-pulse"
                      )}
                    />
                    <span className="flex-1 truncate">{worker.name}</span>
                    {health && (
                      <span
                        className={cn(
                          "text-[10px] font-medium",
                          health.health === "healthy"
                            ? "text-green-600 dark:text-green-400"
                            : "text-red-600 dark:text-red-400"
                        )}
                      >
                        {health.responseTime !== undefined
                          ? `${health.responseTime}ms`
                          : health.health === "healthy"
                            ? "ok"
                            : "down"}
                      </span>
                    )}
                    {isSelected && (
                      <span className="h-2 w-2 shrink-0 rounded-full bg-primary" />
                    )}
                  </button>

                  <div
                    className={cn(
                      "absolute right-1 top-1/2 -translate-y-1/2 flex flex-col gap-0.5 opacity-0 transition-opacity group-hover:opacity-100",
                      isSelected && "opacity-100"
                    )}
                  >
                    <Tooltip>
                      <TooltipTrigger asChild>
                        <Button
                          variant="ghost"
                          size="sm"
                          className="h-5 w-5"
                          onClick={() => setEditingWorker(worker)}
                        >
                          <Edit3 className="h-3 w-3" />
                        </Button>
                      </TooltipTrigger>
                      <TooltipContent side="left">
                        <p>Edit worker</p>
                      </TooltipContent>
                    </Tooltip>
                    <Tooltip>
                      <TooltipTrigger asChild>
                        <Button
                          variant="ghost"
                          size="sm"
                          className="h-5 w-5 text-destructive hover:text-destructive"
                          onClick={() => setDeletingWorker(worker)}
                        >
                          <Trash2 className="h-3 w-3" />
                        </Button>
                      </TooltipTrigger>
                      <TooltipContent side="left">
                        <p>Remove worker</p>
                      </TooltipContent>
                    </Tooltip>
                  </div>
                </div>
              );
            })}
          </nav>
        )}
      </aside>

      {/* Add Worker Dialog */}
      <Dialog open={isAddOpen} onOpenChange={setIsAddOpen}>
        <DialogTrigger asChild>
          <div />
        </DialogTrigger>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Add Worker</DialogTitle>
            <DialogDescription>
              Add a new Telegram Bot Hosting Worker to manage bots on.
            </DialogDescription>
          </DialogHeader>
          <AddWorkerForm
            onSuccess={() => setIsAddOpen(false)}
            onCancel={() => setIsAddOpen(false)}
          />
        </DialogContent>
      </Dialog>

      {/* Edit Worker Dialog */}
      <Dialog
        open={!!editingWorker}
        onOpenChange={(open) => {
          if (!open) setEditingWorker(null);
        }}
      >
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Edit Worker</DialogTitle>
            <DialogDescription>
              Update the worker configuration.
            </DialogDescription>
          </DialogHeader>
          {editingWorker && (
            <EditWorkerForm
              worker={editingWorker}
              onSuccess={() => setEditingWorker(null)}
              onCancel={() => setEditingWorker(null)}
            />
          )}
        </DialogContent>
      </Dialog>

      {/* Remove Worker Confirmation */}
      <Dialog
        open={!!deletingWorker}
        onOpenChange={(open) => {
          if (!open) setDeletingWorker(null);
        }}
      >
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Remove Worker</DialogTitle>
            <DialogDescription>
              Are you sure you want to remove &quot;{deletingWorker?.name}&quot;? This will
              remove the worker from your list but will not affect any bots
              running on the worker itself.
            </DialogDescription>
          </DialogHeader>
          <div className="flex justify-end gap-2">
            <Button variant="outline" size="sm" onClick={() => setDeletingWorker(null)}>
              Cancel
            </Button>
            <Button
              variant="destructive"
              size="sm"
              onClick={() => deletingWorker && handleRemove(deletingWorker)}
            >
              Remove Worker
            </Button>
          </div>
        </DialogContent>
      </Dialog>
    </TooltipProvider>
  );
}
