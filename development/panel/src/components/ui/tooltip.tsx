import * as React from "react";
import * as TooltipPrimitive from "@radix-ui/react-tooltip";
import { cn } from "@/lib/utils/cn";

export const TooltipProvider = TooltipPrimitive.Provider;
export const Tooltip = TooltipPrimitive.Root;
export const TooltipTrigger = TooltipPrimitive.Trigger;

export const TooltipContent = React.forwardRef<
  React.ElementRef<typeof TooltipPrimitive.Content>,
  React.ComponentPropsWithoutRef<typeof TooltipPrimitive.Content>
>(({ className, ...props }, ref) => (
  <TooltipPrimitive.Content
    ref={ref}
    sideOffset={4}
    className={cn(
      "z-50 overflow-hidden rounded-md bg-popover px-3 py-1.5 text-xs text-popover-foreground shadow-md",
      "data-[state=delayed-open]:data-[side=bottom]:slide-in-from-top-1",
      "data-[state=delayed-open]:data-[side=top]:slide-in-from-bottom-1",
      "data-[state=delayed-open]:data-[side=left]:slide-in-from-right-1",
      "data-[state=delayed-open]:data-[side=right]:slide-in-from-left-1",
      className
    )}
    {...props}
  />
));
TooltipContent.displayName = TooltipPrimitive.Content.displayName;
