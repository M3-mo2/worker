import * as React from "react";
import { cn } from "@/lib/utils/cn";

export type SeparatorProps = React.HTMLAttributes<HTMLElement> & {
  orientation?: "horizontal" | "vertical";
};

export const Separator = React.forwardRef<HTMLHRElement, SeparatorProps>(
  ({ className, orientation = "horizontal", ...props }, ref) => (
    <hr
      ref={ref}
      className={cn(
        "shrink-0 border-0 bg-border",
        orientation === "horizontal" ? "h-px w-full" : "h-full w-px",
        className
      )}
      {...props}
    />
  )
);
Separator.displayName = "Separator";
