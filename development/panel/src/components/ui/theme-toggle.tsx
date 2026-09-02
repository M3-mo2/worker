"use client";

import { useTheme } from "next-themes";
import { Sun, Moon, Monitor } from "lucide-react";
import { cn } from "@/lib/utils/cn";
import { Button } from "@/components/ui/button";

export function ThemeToggle({ className }: { className?: string }) {
  const { theme, setTheme } = useTheme();

  const cycleTheme = () => {
    if (theme === "light") {
      setTheme("dark");
    } else if (theme === "dark") {
      setTheme("system");
    } else {
      setTheme("light");
    }
  };

  return (
    <Button
      variant="ghost"
      size="icon"
      onClick={cycleTheme}
      className={cn("relative h-9 w-9", className)}
      aria-label="Toggle theme"
    >
      <Sun className="h-4 w-4 rotate-0 scale-100 transition-all dark:rotate-90 dark:scale-0" />
      <Moon className="absolute h-4 w-4 rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />
      <Monitor className="absolute h-4 w-4 rotate-0 scale-0 transition-all dark:rotate-90 dark:scale-100" />
    </Button>
  );
}

export function ThemeToggleDropdown({ className }: { className?: string }) {
  const { theme, setTheme } = useTheme();

  const options = [
    { value: "light" as const, label: "Light", icon: Sun },
    { value: "dark" as const, label: "Dark", icon: Moon },
    { value: "system" as const, label: "System", icon: Monitor },
  ];

  return (
    <div className={cn("flex items-center gap-1 rounded-md bg-muted p-1", className)}>
      {options.map((opt) => {
        const Icon = opt.icon;
        const isActive = theme === opt.value || (theme === "system" && opt.value === "system");
        return (
          <button
            key={opt.value}
            onClick={() => setTheme(opt.value)}
            className={cn(
              "flex items-center gap-1.5 rounded px-2.5 py-1.5 text-xs font-medium transition-colors",
              isActive
                ? "bg-background shadow-sm text-foreground"
                : "text-muted-foreground hover:text-foreground"
            )}
            aria-pressed={isActive}
          >
            <Icon className="h-3 w-3" />
            {opt.label}
          </button>
        );
      })}
    </div>
  );
}
