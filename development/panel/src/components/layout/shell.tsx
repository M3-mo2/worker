import { cn } from "@/lib/utils/cn";
import { PropsWithChildren } from "react";

interface ShellProps {
  className?: string;
  fixed?: boolean;
}

export function Shell({ children, className, fixed = false }: PropsWithChildren<ShellProps>) {
  return (
    <div
      className={cn(
        "flex w-full flex-1 flex-col gap-4 overflow-hidden",
        fixed && "fixed inset-0 top-(--header-height) z-10",
        className
      )}
    >
      {children}
    </div>
  );
}
