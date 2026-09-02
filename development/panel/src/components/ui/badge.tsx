import * as React from "react";
import { cn } from "@/lib/utils/cn";

export type BadgeVariant = "default" | "secondary" | "destructive" | "outline" | "success" | "warning";
export type BadgeSize = "sm" | "default";

export interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  variant?: BadgeVariant;
  size?: BadgeSize;
}

const badgeVariants = {
  base: "inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2",
  variant: {
    default: "border-transparent bg-primary text-primary-foreground hover:bg-primary/80",
    secondary: "border-transparent bg-secondary text-secondary-foreground hover:bg-secondary/80",
    destructive: "border-transparent bg-destructive text-destructive-foreground hover:bg-destructive/80",
    outline: "text-foreground",
    success: "border-transparent bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400",
    warning: "border-transparent bg-amber-100 text-amber-800 dark:bg-amber-900/30 dark:text-amber-400",
  },
  size: {
    sm: "px-2 py-0.5 text-xs",
    default: "px-2.5 py-0.5 text-xs",
  },
};

export const Badge = React.forwardRef<HTMLSpanElement, BadgeProps>(
  ({ className, variant = "default", size = "default", ...props }, ref) => (
    <span
      className={cn(badgeVariants.base, badgeVariants.variant[variant], badgeVariants.size[size], className)}
      ref={ref}
      {...props}
    />
  )
);
Badge.displayName = "Badge";
