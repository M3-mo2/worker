"use client";

import { Toaster as SonnerToaster } from "sonner";
import { useTheme } from "next-themes";

export function Toaster() {
  const { theme } = useTheme();
  const themeMap: Record<string, "light" | "dark" | "system"> = {
    light: "light",
    dark: "dark",
    system: "system",
  };
  return <SonnerToaster theme={themeMap[theme ?? "system"]} closeButton richColors />;
}
