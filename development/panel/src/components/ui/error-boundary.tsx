"use client";

import { Component } from "react";
import { AlertTriangle, RefreshCw } from "lucide-react";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils/cn";

interface ErrorBoundaryProps {
  children: React.ReactNode;
  fallback?: React.ReactNode;
  className?: string;
}

interface ErrorBoundaryState {
  hasError: boolean;
  error: Error | null;
}

export class ErrorBoundary extends Component<ErrorBoundaryProps, ErrorBoundaryState> {
  constructor(props: ErrorBoundaryProps) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    console.error("ErrorBoundary caught an error:", error, errorInfo);
  }

  reset = () => {
    this.setState({ hasError: false, error: null });
  };

  render() {
    if (this.state.hasError) {
      if (this.props.fallback) {
        return <>{this.props.fallback}</>;
      }
      return (
        <div
          className={cn(
            "flex flex-col items-center justify-center gap-4 rounded-lg border border-destructive/30 bg-destructive/5 p-6 text-center",
            this.props.className
          )}
        >
          <AlertTriangle className="h-10 w-10 text-destructive" />
          <div>
            <h3 className="font-semibold text-destructive">Something went wrong</h3>
            <p className="text-sm text-muted-foreground mt-1">
              {this.state.error?.message ?? "An unexpected error occurred"}
            </p>
          </div>
          <Button variant="outline" size="sm" onClick={this.reset}>
            <RefreshCw className="h-4 w-4 mr-2" />
            Retry
          </Button>
        </div>
      );
    }
    return this.props.children;
  }
}
