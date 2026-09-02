"use client";

import { useEffect, useState, useMemo, useCallback } from "react";
import { useWorkersStore } from "@/lib/store/workers";
import { createWorkerApi } from "@/lib/api/workers";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { LoadingSpinner } from "@/components/ui/loading-spinner";
import { toast } from "@/hooks/use-toast";
import { Download, Copy, RefreshCw, AlertCircle, FileText } from "lucide-react";
import { cn } from "@/lib/utils/cn";
import { LogControls } from "@/components/logs/log-controls";
import { REDACTED_NOTE } from "@/lib/utils/format";

interface LogViewerProps {
  workerId: string;
  userId: string;
}

function HighlightedLog({ logText }: { logText: string }) {
  const lines = useMemo(() => logText.split("\n"), [logText]);

  return (
    <div className="space-y-0.5">
      {lines.map((line, i) => {
        const isError = /(\b(error|fatal|exception|warning|critical)\b)/gi.test(line);
        return (
          <pre
            key={i}
            className={cn(
              "text-xs leading-tight",
              isError
                ? "bg-red-950/30 text-red-300 font-mono"
                : "text-muted-foreground font-mono"
            )}
          >
            {line || "\u00a0"}
          </pre>
        );
      })}
    </div>
  );
}

export function LogViewer({ workerId, userId }: LogViewerProps) {
  const worker = useWorkersStore((s) => s.workers.find((w) => w.id === workerId));
  const [logText, setLogText] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [lines, setLines] = useState(500);
  const [error, setError] = useState<string | null>(null);

  const fetchLogs = useCallback(async () => {
    if (!worker) return;
    setError(null);
    try {
      const api = createWorkerApi(worker);
      const text = await api.logs.fetchLogs({ userId, lines });
      setLogText(text || "(no logs available)");
    } catch (err) {
      const error = err as Error;
      setError(error.message);
      setLogText("");
      toast.error("Failed to load logs", { description: error.message });
    }
  }, [worker, userId, lines]);

  const handleRefresh = useCallback(async () => {
    setIsLoading(true);
    await fetchLogs();
    setIsLoading(false);
  }, [fetchLogs]);

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect
    void fetchLogs();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [workerId, userId, lines]);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(logText);
      toast.success("Logs copied to clipboard");
    } catch {
      toast.error("Failed to copy logs");
    }
  };

  const handleDownload = () => {
    const blob = new Blob([logText], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `bot-${userId}-logs.txt`;
    URL.revokeObjectURL(url);
    a.click();
  };

  if (!worker) {
    return (
      <Card>
        <CardContent className="py-8 text-center">
          <AlertCircle className="mx-auto h-6 w-6 text-destructive mb-2" />
          <p className="text-muted-foreground">Worker not found.</p>
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-semibold">Error Logs</h3>
          <p className="text-sm text-muted-foreground">
            {REDACTED_NOTE}
          </p>
        </div>

        <div className="flex items-center gap-2">
          <Button variant="outline" size="sm" onClick={handleRefresh} disabled={isLoading}>
            <RefreshCw className={cn("h-4 w-4", isLoading && "animate-spin")} />
          </Button>
          <Button variant="outline" size="sm" onClick={handleCopy} disabled={!logText || isLoading}>
            <Copy className="h-4 w-4" />
          </Button>
          <Button variant="outline" size="sm" onClick={handleDownload} disabled={!logText || isLoading}>
            <Download className="h-4 w-4" />
          </Button>
        </div>
      </div>

      <LogControls lines={lines} onChange={setLines} />

      <Card>
        <CardContent className="pt-4">
          <div className="relative max-h-96 w-full overflow-auto rounded-md border bg-black/90 p-3 font-mono text-xs">
            {isLoading ? (
              <div className="py-8 text-center">
                <LoadingSpinner className="mx-auto mb-2" />
                <p className="text-muted-foreground">Loading logs…</p>
              </div>
            ) : error ? (
              <div className="flex items-center gap-2 text-destructive">
                <AlertCircle className="h-4 w-4" />
                {error}
              </div>
            ) : logText ? (
              <HighlightedLog logText={logText} />
            ) : (
              <div className="flex items-center gap-2 text-muted-foreground">
                <FileText className="h-4 w-4" />
                No logs available yet.
              </div>
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
