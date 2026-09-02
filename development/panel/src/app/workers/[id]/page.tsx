"use client";

import { use, useState, useEffect } from "react";
import { notFound } from "next/navigation";
import { useWorkers } from "@/lib/store/workers";
import { DashboardLayout } from "@/components/layout/dashboard-layout";
import { DeployForm } from "@/components/bots/deploy-form";
import { BotStatusDisplay } from "@/components/bots/bot-status";
import { BotActionButtons } from "@/components/bots/bot-actions";
import { LogViewer } from "@/components/logs/log-viewer";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { validateUserId } from "@/lib/utils/validation";
import { toast } from "@/hooks/use-toast";
import { Bot } from "lucide-react";

interface WorkerBotsPageProps {
  params: Promise<{ id: string }>;
}

export default function WorkerBotsPage({ params }: WorkerBotsPageProps) {
  const { id } = use(params);
  const { workers, setSelectedWorker } = useWorkers();
  const worker = workers.find((w) => w.id === id);

  const [checkUserId, setCheckUserId] = useState("");
  const [checkedUserId, setCheckedUserId] = useState<string | null>(null);

  useEffect(() => {
    setSelectedWorker(id);
  }, [id, setSelectedWorker]);

  useEffect(() => {
    if (!worker) {
      notFound();
    }
  }, [worker]);

  if (!worker) {
    return null;
  }

  const handleCheckStatus = () => {
    const validation = validateUserId(checkUserId);
    if (!validation.valid) {
      toast.error(validation.message);
      return;
    }
    setCheckedUserId(checkUserId.trim());
  };

  return (
    <DashboardLayout
      title={worker.name}
      subtitle={`Bot management · ${new URL(worker.url).hostname}`}
      showBack
    >
      <div className="space-y-6">
        {/* Deploy Bot */}
        <Card>
          <CardHeader>
            <CardTitle>Deploy Bot</CardTitle>
            <CardDescription>
              Upload a bot.php file, provide the user ID and bot token to register
              and start the bot on this worker.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <DeployForm workerId={worker.id} />
          </CardContent>
        </Card>

        {/* Bot Status Lookup */}
        <Card>
          <CardHeader>
            <CardTitle>Bot Status Lookup</CardTitle>
            <CardDescription>
              Enter a Telegram user ID to check the bot&apos;s status and perform actions
              (stop, delete, delete file, view logs).
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="flex gap-2 items-end">
              <div className="flex-1 space-y-1">
                <Label htmlFor="lookup-user-id">User ID</Label>
                <Input
                  id="lookup-user-id"
                  type="number"
                  placeholder="123456789"
                  value={checkUserId}
                  onChange={(e) => setCheckUserId(e.target.value)}
                  onKeyDown={(e) => e.key === "Enter" && handleCheckStatus()}
                />
              </div>
              <Button onClick={handleCheckStatus} disabled={!checkUserId.trim()}>
                <Bot className="h-4 w-4 mr-1" />
                Check Status
              </Button>
            </div>

            {checkedUserId && (
              <div className="mt-4 space-y-4">
                <BotStatusDisplay
                  workerId={worker.id}
                  userId={checkedUserId}
                  onStatusChanged={() => {}}
                />

                <BotActionButtons
                  workerId={worker.id}
                  userId={checkedUserId}
                  onStatusChanged={() => {}}
                />
              </div>
            )}
          </CardContent>
        </Card>

        {/* Logs */}
        {checkedUserId && (
          <Card>
            <CardHeader>
              <CardTitle>Logs for user {checkedUserId}</CardTitle>
              <CardDescription>
                View error logs for this bot (tokens are already redacted by the worker).
              </CardDescription>
            </CardHeader>
            <CardContent>
              <LogViewer workerId={worker.id} userId={checkedUserId} />
            </CardContent>
          </Card>
        )}
      </div>
    </DashboardLayout>
  );
}
