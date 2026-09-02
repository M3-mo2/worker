const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10MB
const ALLOWED_PHP_EXTENSIONS = [/\.php$/i];

export interface ValidationResult {
  valid: boolean;
  message: string;
}

export function validateWorkerUrl(url: string): ValidationResult {
  if (!url.trim()) {
    return { valid: false, message: "URL is required" };
  }

  try {
    const parsed = new URL(url);
    if (parsed.protocol !== "http:" && parsed.protocol !== "https:") {
      return { valid: false, message: "URL must use http or https protocol" };
    }
    if (!parsed.hostname) {
      return { valid: false, message: "URL must have a valid hostname" };
    }
    return { valid: true, message: "" };
  } catch {
    return { valid: false, message: "Please enter a valid URL (e.g. https://worker.up.railway.app)" };
  }
}

export function validateWorkerName(name: string): ValidationResult {
  if (!name || !name.trim()) {
    return { valid: false, message: "Worker name is required" };
  }
  if (name.length > 64) {
    return { valid: false, message: "Worker name must be 64 characters or fewer" };
  }
  return { valid: true, message: "" };
}

export function validateSecret(secret: string): ValidationResult {
  if (!secret || !secret.trim()) {
    return { valid: false, message: "Internal secret is required" };
  }
  return { valid: true, message: "" };
}

export function validateUserId(userId: string): ValidationResult {
  if (!userId.trim()) {
    return { valid: false, message: "User ID is required" };
  }
  if (!/^\d+$/.test(userId.trim())) {
    return { valid: false, message: "User ID must be a numeric Telegram user ID" };
  }
  return { valid: true, message: "" };
}

export function validateBotToken(token: string): ValidationResult {
  if (!token.trim()) {
    return { valid: false, message: "Bot token is required" };
  }
  const tokenRegex = /^\d{8,12}:[a-zA-Z0-9_-]{35}$/;
  if (!tokenRegex.test(token.trim())) {
    return { valid: false, message: "Invalid bot token format (expected 12345678:ABCdef...)" };
  }
  return { valid: true, message: "" };
}

export function validatePhpFile(file: File | null): ValidationResult {
  if (!file) {
    return { valid: false, message: "Please select a PHP file to upload" };
  }

  if (!ALLOWED_PHP_EXTENSIONS.some((ext) => ext.test(file.name))) {
    return { valid: false, message: "Only .php files are allowed" };
  }

  if (file.size > MAX_FILE_SIZE) {
    const sizeMB = (file.size / (1024 * 1024)).toFixed(2);
    return { valid: false, message: `File size ${sizeMB}MB exceeds the 10MB limit` };
  }

  return { valid: true, message: "" };
}

export function validateLogLines(lines: number): ValidationResult {
  if (!Number.isInteger(lines)) {
    return { valid: false, message: "Lines must be an integer" };
  }
  if (lines < 1) {
    return { valid: false, message: "Lines must be at least 1" };
  }
  if (lines > 5000) {
    return { valid: false, message: "Lines cannot exceed 5000" };
  }
  return { valid: true, message: "" };
}
