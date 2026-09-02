# Telegram Bot Host Control Panel

A Next.js 15+ developer control panel for managing [Telegram Bot Hosting Workers](https://). The panel provides a web UI to add/edit/remove workers, deploy bots, check bot status, stop/delete bots, view redacted logs, and run health checks.

## Quick Start

### Prerequisites

- Node.js 20+ (tested with v24)
- npm 10+

### Development

```bash
cd development/panel
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

### Build

```bash
npm run build
```

### Lint & Typecheck

```bash
npm run lint          # ESLint — zero warnings enforced
npx tsc --noEmit     # TypeScript type checking
```

---

## How It Works

The panel communicates with Telegram Bot Hosting Workers via their HTTP API. Each worker requires:

- **URL** — e.g. `https://worker.up.railway.app`
- **Internal Secret** (`X-Internal-Secret` header value) — authenticates API requests

Worker configs are saved in your browser&apos;s `localStorage` (key: `telegram_workers`) using Zustand&apos;s persist middleware. No backend or database is required.

### Worker API Endpoints

| Method | Endpoint | Auth | Purpose |
|--------|----------|------|---------|
| GET    | `/health` | None | Health check - `{"status":"ok","timestamp":"..."}` |
| POST   | `/deploy` | Internal Secret | Upload `bot.php` + register webhook |
| POST   | `/stop`   | Internal Secret | Stop bot (delete webhook, set status="stopped") |
| POST   | `/delete` | Internal Secret | Full delete (webhook, directory, registry) |
| POST   | `/files/delete` | Internal Secret | Delete a single file in user dir |
| GET    | `/status/{user_id}` | Internal Secret | Bot status (running/stopped/not_found) |
| GET    | `/logs/{user_id}?lines=N` | Internal Secret | Redacted error log (text/plain) |
| POST   | `/webhook/{user_id}` | Telegram secret | Internal - not used by the panel |

All endpoints except `/health` require the `X-Internal-Secret` header. The panel attaches it automatically to every request.

---

## Usage Guide

### 1. Add a Worker

1. Click the **+** button in the sidebar, or use the "Add Worker" shortcut on the empty-state dashboard.
2. Fill in:
   - **Worker Name** - a display label
   - **Worker URL** - the full base URL of your hosting worker
   - **Internal Secret** - the `X-Internal-Secret` value configured on the worker
3. Click **Add Worker**.

Workers are auto-saved to localStorage. The sidebar shows a live health dot (green = healthy, red = unhealthy, yellow = checking).

### 2. Deploy a Bot

1. Select a worker from the sidebar, or click **Manage** on a worker card.
2. In the **Deploy Bot** section, enter:
   - **User ID** - your Telegram user ID (numeric)
   - **Bot Token** - the token from @BotFather
   - **PHP File** - upload a `.php` file (max 10 MB)
3. Click **Deploy Bot**. The worker will upload, register the webhook, and start the bot.

### 3. Check Bot Status

1. In the **Bot Status Lookup** section, enter a **User ID**.
2. Click **Check Status**.
3. The bot status is displayed with a color-coded badge:
   - **Running** (green) - the bot is active
   - **Stopped** (yellow) - the bot was stopped
   - **Not Found** (red) - no bot is registered for this user ID

### 4. Manage a Bot (Stop / Delete / Delete File)

After checking a bot&apos;s status, action buttons appear:

- **Stop Bot** - removes the webhook and sets status to "stopped". Confirmation required.
- **Delete Bot** - permanently removes the bot (webhook, directory, registry entry). Requires typing the user ID to confirm.
- **Delete File** - removes a single file from the bot directory. Defaults to `bot.php`.

### 5. View Logs

Below the status lookup, the **Logs** section automatically loads error logs for the checked user ID:

- Tokens are **already redacted** by the worker before being returned.
- Adjust the number of lines via the **Log Controls** (presets: 100, 500, 1000, 2000; max 5000).
- Error lines are highlighted in red.
- Use **Copy** to copy logs to clipboard or **Download** to save as a `.txt` file.

### 6. Health Dashboard

The main dashboard displays:

- **Summary cards** - count of healthy/unhealthy workers and average response time.
- **Worker Details** - per-worker health, response time, and any error messages.
- Health checks auto-refresh every 15 seconds, or click the **Refresh** button for an immediate check.

### 7. Dark / Light Mode

Use the theme toggle (sun/moon icon) in the header to cycle between **Light**, **Dark**, and **System** (follows your OS preference).

---

## Project Structure

```
src/
  app/
    layout.tsx                  Root layout (ThemeProvider, Toaster)
    page.tsx                    Dashboard (health + worker list)
    workers/[id]/page.tsx       Bot management for a selected worker
  lib/
    api/
      client.ts                 Base fetch wrapper (ApiClient class)
      types.ts                  ApiError class
      health.ts                 GET /health
      bots.ts                   deploy, stop, delete, files/delete, status
      logs.ts                   GET /logs/{user_id}
      workers.ts                createWorkerApi() aggregator
    store/
      workers.ts                Zustand store (localStorage-persisted)
    types.ts                    Shared TypeScript interfaces
    utils/
      cn.ts                     clsx + tailwind-merge helper
      validation.ts             URL, user_id, bot_token, file validation
      format.ts                 Date/time, response time, token truncation
  components/
    ui/                         Shadcn-style primitives (Button, Card, Dialog, etc.)
    layout/                     Sidebar, Header, DashboardLayout, Shell
    workers/                    WorkerCard, AddWorkerForm, EditWorkerForm, etc.
    bots/                       DeployForm, BotStatusDisplay, BotActionButtons
    logs/                       LogViewer, LogControls
    health/                     HealthDashboard
  hooks/
    use-toast.tsx               Sonner toast wrapper
```

### API Client Design

The API client (`lib/api/client.ts`) provides a typed `ApiClient` class:

```ts
import { createApiClient } from "@/lib/api/client";

const client = createApiClient({
  baseUrl: "https://worker.up.railway.app",
  secret: "your-internal-secret",
  timeout: 10000, // 10s default
});

// Typed request with automatic error parsing
const status = await client.request<WorkerBotStatus>("/status/123456789");
```

Each module (`bots.ts`, `logs.ts`, `health.ts`) exports a factory function that creates a typed API for a given worker config. Errors are thrown as `ApiError` instances with `status`, `detail`, `isNetworkError`, `isNotFound`, and `isAuthError` helpers.

---

## Key Libraries

| Library | Purpose |
|---------|---------|
| Next.js 16 (App Router) | Framework |
| TypeScript | Type safety |
| Tailwind CSS v4 | Styling |
| Zustand | State management (worker configs) |
| Radix UI | Headless UI primitives |
| Lucide React | Icons |
| Sonner | Toast notifications |
| date-fns | Date formatting |
