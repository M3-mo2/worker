"use client";

import { useWorkers } from "@/lib/store/workers";
import { DashboardLayout } from "@/components/layout/dashboard-layout";
import { WorkerList } from "@/components/workers/worker-list";
import { HealthDashboard } from "@/components/health/health-dashboard";
import { AddWorkerShortcut } from "@/components/workers/add-worker-shortcut";
import { Server } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";

export default function DashboardPage() {
  const { workers } = useWorkers();

  return (
    <DashboardLayout
      title="Telegram Bot Host"
      subtitle={`${workers.length} worker${workers.length !== 1 ? "s" : ""} configured`}
    >
      <div className="space-y-8">
        {workers.length === 0 ? (
          <Card>
            <CardContent className="py-12 text-center">
              <Server className="mx-auto h-12 w-12 text-muted-foreground/30 mb-4" />
              <h3 className="text-lg font-semibold mb-2">No workers configured yet</h3>
              <p className="text-sm text-muted-foreground max-w-md mx-auto mb-4">
                Welcome to the Telegram Bot Hosting control panel. Add your first worker
                to start managing bots.
              </p>
              <AddWorkerShortcut />
            </CardContent>
          </Card>
        ) : (
          <>
            <HealthDashboard />

            <div>
              <h2 className="text-lg font-semibold mb-4">Your Workers</h2>
              <WorkerList />
            </div>
          </>
        )}
      </div>
    </DashboardLayout>
  );
}
