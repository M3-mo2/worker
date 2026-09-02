"use client";

import { useState, useRef } from "react";
import { useWorkersStore } from "@/lib/store/workers";
import { createBotApi } from "@/lib/api/bots";
import { validatePhpFile, validateUserId, validateBotToken } from "@/lib/utils/validation";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent } from "@/components/ui/card";
import { toast } from "@/hooks/use-toast";
import { Upload, FileText, AlertCircle } from "lucide-react";
import { cn } from "@/lib/utils/cn";

interface DeployFormProps {
  workerId: string;
}

export function DeployForm({ workerId }: DeployFormProps) {
  const worker = useWorkersStore((s) => s.workers.find((w) => w.id === workerId));
  const [userId, setUserId] = useState("");
  const [botToken, setBotToken] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const [isDeploying, setIsDeploying] = useState(false);
  const [errors, setErrors] = useState<Record<string, string>>({});
  const fileInputRef = useRef<HTMLInputElement>(null);

  if (!worker) {
    return (
      <Card>
        <CardContent className="py-8 text-center">
          <AlertCircle className="mx-auto h-6 w-6 text-destructive mb-2" />
          <p className="text-muted-foreground">Worker not found. Please select a valid worker.</p>
        </CardContent>
      </Card>
    );
  }

  const validate = () => {
    const newErrors: Record<string, string> = {};
    const userIdErr = validateUserId(userId);
    if (!userIdErr.valid) newErrors.userId = userIdErr.message;

    const tokenErr = validateBotToken(botToken);
    if (!tokenErr.valid) newErrors.botToken = tokenErr.message;

    const fileErr = validatePhpFile(file);
    if (!fileErr.valid) newErrors.file = fileErr.message;

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selected = e.target.files?.[0] ?? null;
    setFile(selected);
    setErrors((prev) => ({ ...prev, file: "" }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (isDeploying) return;
    if (!validate()) return;

    setIsDeploying(true);
    try {
      const botApi = createBotApi({ baseUrl: worker.url, secret: worker.secret });
      await botApi.deploy(userId.trim(), botToken.trim(), file!);

      toast.success("Bot deployed successfully!", {
        description: `Bot for user ${userId} has been deployed and webhook registered.`,
      });
      setUserId("");
      setBotToken("");
      setFile(null);
      if (fileInputRef.current) fileInputRef.current.value = "";
    } catch (err) {
      const error = err as Error & { status?: number };
      toast.error("Deploy failed", {
        description: error.message || "An unexpected error occurred.",
      });
    } finally {
      setIsDeploying(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
        <div className="space-y-2">
          <Label htmlFor="deploy-user-id">User ID</Label>
          <Input
            id="deploy-user-id"
            type="number"
            placeholder="123456789"
            value={userId}
            onChange={(e) => {
              setUserId(e.target.value);
              if (errors.userId) setErrors((p) => ({ ...p, userId: "" }));
            }}
            aria-invalid={!!errors.userId}
            disabled={isDeploying}
          />
          {errors.userId && <p className="text-xs text-destructive">{errors.userId}</p>}
        </div>

        <div className="space-y-2">
          <Label htmlFor="deploy-bot-token">Bot Token</Label>
          <Input
            id="deploy-bot-token"
            type="password"
            placeholder="12345678:ABCdefGHIjkl..."
            value={botToken}
            onChange={(e) => {
              setBotToken(e.target.value);
              if (errors.botToken) setErrors((p) => ({ ...p, botToken: "" }));
            }}
            aria-invalid={!!errors.botToken}
            disabled={isDeploying}
          />
          {errors.botToken && <p className="text-xs text-destructive">{errors.botToken}</p>}
        </div>
      </div>

      <div className="space-y-2">
        <Label htmlFor="deploy-file">PHP File</Label>
        <div className="flex items-center gap-3">
          <label
            htmlFor="deploy-file"
            className={cn(
              "flex flex-1 cursor-pointer items-center gap-2 rounded-md border border-input bg-background px-3 py-2 text-sm transition-colors hover:bg-accent",
              "file:mr-4 file:cursor-pointer file:rounded-md file:border-0 file:bg-primary file:py-2 file:px-4 file:text-sm file:font-medium file:text-primary-foreground hover:file:bg-primary/90"
            )}
          >
            <Upload className="h-4 w-4 text-muted-foreground" />
            <span className="truncate">
              {file ? file.name : "Click to select a .php file"}
            </span>
            <input
              id="deploy-file"
              type="file"
              accept=".php"
              ref={fileInputRef}
              onChange={handleFileChange}
              className="hidden"
              disabled={isDeploying}
            />
          </label>
        </div>
        {file && (
          <div className="flex items-center gap-2 text-xs text-muted-foreground">
            <FileText className="h-3 w-3" />
            <span>
              {(file.size / 1024).toFixed(1)} KB — must be .php, max 10MB
            </span>
          </div>
        )}
        {errors.file && <p className="text-xs text-destructive">{errors.file}</p>}
      </div>

      <div className="flex justify-end">
        <Button type="submit" disabled={isDeploying} className="min-w-[120px]">
          {isDeploying ? "Deploying…" : "Deploy Bot"}
        </Button>
      </div>
    </form>
  );
}
