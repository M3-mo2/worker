"use client";

import { ReactNode } from "react";
import { Sidebar } from "@/components/layout/sidebar";
import { Header } from "@/components/layout/header";

interface DashboardLayoutProps {
  children: ReactNode;
  title?: string;
  subtitle?: string;
  showBack?: boolean;
  onRefresh?: () => void;
  refreshing?: boolean;
}

export function DashboardLayout({
  children,
  title = "",
  subtitle,
  showBack = false,
  onRefresh,
  refreshing = false,
}: DashboardLayoutProps) {
  return (
    <div className="flex h-screen w-full overflow-hidden bg-background">
      <Sidebar />
      <div className="flex flex-1 flex-col overflow-hidden">
        <Header
          title={title}
          subtitle={subtitle}
          showBack={showBack}
          onRefresh={onRefresh}
          refreshing={refreshing}
        />
        <main className="flex-1 overflow-y-auto overflow-x-hidden p-4 sm:p-6">
          <div className="mx-auto w-full max-w-6xl">{children}</div>
        </main>
      </div>
    </div>
  );
}
