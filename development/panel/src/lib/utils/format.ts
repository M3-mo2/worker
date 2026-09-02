import { formatDistanceToNow, format } from "date-fns";

export function formatDate(date: string | Date): string {
  try {
    const d = typeof date === "string" ? new Date(date) : date;
    return format(d, "PPpp");
  } catch {
    return "Invalid date";
  }
}

export function formatRelativeDate(date: string | Date): string {
  try {
    const d = typeof date === "string" ? new Date(date) : date;
    return formatDistanceToNow(d, { addSuffix: true });
  } catch {
    return "Invalid date";
  }
}

export function formatTimestamp(date: string | Date): string {
  try {
    const d = typeof date === "string" ? new Date(date) : date;
    return format(d, "PPp");
  } catch {
    return "—";
  }
}

export function formatResponseTime(ms: number): string {
  if (ms < 1000) {
    return `${ms}ms`;
  }
  return `${(ms / 1000).toFixed(2)}s`;
}

export function truncateMiddle(str: string, maxLength: number): string {
  if (str.length <= maxLength) {
    return str;
  }
  const half = Math.floor(maxLength / 2);
  return `${str.slice(0, half)}…${str.slice(str.length - half)}`;
}

export function truncateToken(token: string, visibleChars = 4): string {
  if (!token) return "";
  if (token.length <= visibleChars) return "*".repeat(token.length);
  return "*".repeat(token.length - visibleChars) + token.slice(-visibleChars);
}

export const REDACTED_NOTE = "Tokens in logs are already redacted by the worker before being returned.";
