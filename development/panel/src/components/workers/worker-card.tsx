"use client";

import { WorkerConfig, WorkerHealth } from "@/lib/types";
import { Bot, Clock, ExternalLink, Globe, Server } from "lucide-react";
import { cn } from "@/lib/utils/cn";
import { formatRelativeDate } from "@/lib/utils/format";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Tooltip, TooltipTrigger, TooltipContent, TooltipProvider } from "@/components/ui/tooltip";
import Link from "next/link";

interface WorkerCardProps {
  worker: WorkerConfig;
  health?: WorkerHealth;
  onSelect?: (worker: WorkerConfig) => void;
  isSelected?: boolean;
}

export function WorkerCard({ worker, health, onSelect, isSelected }: WorkerCardProps) {
  const healthStatus = health?.health ?? "unknown";

  const statusIndicator = {
    healthy: { color: "bg-green-500", label: "Healthy", variant: "success" as const },
    unhealthy: { color: "bg-red-500", label: "Unhealthy", variant: "destructive" as const },
    unknown: { color: "bg-yellow-500", label: "Checking…", variant: "warning" as const },
  }[healthStatus];

  return (
    <Card
      className={cn(
        "group relative transition-shadow hover:shadow-md",
        isSelected && "ring-2 ring-primary ring-offset-2"
      )}
    >
      <CardHeader className="pb-3">
        <div className="flex items-start justify-between">
          <div className="flex items-center gap-2.5">
            <div
              className={cn(
                "flex h-9 w-9 shrink-0 items-center justify-center rounded-lg",
                "bg-primary/10 text-primary"
              )}
            >
              <Server className="h-5 w-5" />
            </div>
            <div>
              <CardTitle className="text-lg">{worker.name}</CardTitle>
              <p className="text-sm text-muted-foreground break-all">{worker.url}</p>
              <p className="text-xs text-muted-foreground">
                Created {formatRelativeDate(worker.createdAt)}
              </p>
            </div>
          </div>

          <TooltipProvider>
            <Tooltip>
              <TooltipTrigger asChild>
                <span className="flex items-center gap-1.5">
                  <span className={cn("h-2.5 w-2.5 rounded-full", statusIndicator.color)} />
                  <Badge variant={statusIndicator.variant} size="sm">
                    {statusIndicator.label}
                  </Badge>
                </span>
              </TooltipTrigger>
              <TooltipContent>
                {health?.responseTime !== undefined && (
                  <p>Response time: {health.responseTime}ms</p>
                )}
                {health && <p>Last checked: {formatRelativeDate(health.timestamp)}</p>}
              </TooltipContent>
            </Tooltip>
          </TooltipProvider>
        </div>
      </CardHeader>

      <CardContent className="pb-3">
        <div className="flex items-center gap-4 text-xs text-muted-foreground">
          <span className="flex items-center gap-1">
            <Bot className="h-3 w-3" />
            Bot hosting
          </span>
          <span className="flex items-center gap-1">
            <Globe className="h-3 w-3" />
            {new URL(worker.url).hostname}
          </span>
          {health?.responseTime !== undefined && (
            <span className="flex items-center gap-1">
              <Clock className="h-3 w-3" />
              {health.responseTime}ms
            </span>
          )}
        </div>
      </CardContent>

      <div className="flex items-center justify-end gap-2 border-t border-border/50 px-4 py-2 opacity-0 transition-opacity group-hover:opacity-100">
        {onSelect && (
          <Button
            variant="outline"
            size="sm"
            onClick={() => onSelect(worker)}
          >
            {isSelected ? "Managing" : "Manage"}
          </Button>
        )}
        <TooltipProvider>
          <Tooltip>
            <TooltipTrigger asChild>
              <Button variant="ghost" size="sm" asChild>
                <Link href={`/workers/${worker.id}`}>
                  <ExternalLink className="h-4 w-4" />
                </Link>
              </Button>
            </TooltipTrigger>
            <TooltipContent>
              <p>Open bot management</p>
            </TooltipContent>
          </Tooltip>
        </TooltipProvider>
      </div>
    </Card>
  );
}
