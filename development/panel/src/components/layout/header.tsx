"use client";

import { ThemeToggle } from "@/components/ui/theme-toggle";
import { Button } from "@/components/ui/button";
import { ArrowLeft, RefreshCw } from "lucide-react";
import Link from "next/link";
import { cn } from "@/lib/utils/cn";
import { useWorkers } from "@/lib/store/workers";

interface HeaderProps {
  title: string;
  subtitle?: string;
  showBack?: boolean;
  onRefresh?: () => void;
  refreshing?: boolean;
}

export function Header({ title, subtitle, showBack = false, onRefresh, refreshing = false }: HeaderProps) {
  const { selectedWorker } = useWorkers();

  return (
    <header className="flex items-center justify-between border-b border-border bg-card px-4 py-3 sm:px-6">
      <div className="flex items-center gap-4">
        {showBack && (
          <Button variant="ghost" size="sm" asChild>
            <Link href="/">
              <ArrowLeft className="h-4 w-4" />
            </Link>
          </Button>
        )}
        <div>
          <h1 className="text-xl font-semibold text-foreground">{title}</h1>
          {subtitle && (
            <p className="text-sm text-muted-foreground">{subtitle}</p>
          )}
        </div>
      </div>

      <div className="flex items-center gap-3">
        {selectedWorker && (
          <span className="hidden text-sm text-muted-foreground sm:inline">
            on{" "}
            <span className="font-medium text-foreground">
              {selectedWorker.name}
            </span>
          </span>
        )}
        {onRefresh && (
          <Button
            variant="outline"
            size="sm"
            onClick={onRefresh}
            disabled={refreshing}
          >
            <RefreshCw className={cn("h-4 w-4", refreshing && "animate-spin")} />
          </Button>
        )}
        <ThemeToggle />
      </div>
    </header>
  );
}
