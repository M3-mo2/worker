"use client";

import { useState } from "react";
import { useWorkersStore } from "@/lib/store/workers";
import { validateSecret, validateWorkerName, validateWorkerUrl } from "@/lib/utils/validation";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { toast } from "@/hooks/use-toast";
import { Eye, EyeOff } from "lucide-react";

interface AddWorkerFormProps {
  onSuccess: () => void;
  onCancel: () => void;
}

export function AddWorkerForm({ onSuccess, onCancel }: AddWorkerFormProps) {
  const addWorker = useWorkersStore((s) => s.addWorker);
  const workers = useWorkersStore((s) => s.workers);

  const [name, setName] = useState("");
  const [url, setUrl] = useState("");
  const [secret, setSecret] = useState("");
  const [showSecret, setShowSecret] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const [errors, setErrors] = useState<Record<string, string>>({});

  const validate = () => {
    const newErrors: Record<string, string> = {};
    const nameErr = validateWorkerName(name);
    if (!nameErr.valid) newErrors.name = nameErr.message;
    const urlErr = validateWorkerUrl(url);
    if (!urlErr.valid) newErrors.url = urlErr.message;
    const secretErr = validateSecret(secret);
    if (!secretErr.valid) newErrors.secret = secretErr.message;

    const duplicate = workers.find(
      (w) => w.url === url.trim() && w.secret === secret.trim()
    );
    if (duplicate) {
      newErrors.url = `A worker with this URL and secret already exists ("${duplicate.name}")`;
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (isSubmitting) return;
    if (!validate()) return;

    setIsSubmitting(true);
    try {
      addWorker(name.trim(), url.trim(), secret.trim());
      onSuccess();
      toast.success("Worker added", {
        description: `"${name}" has been added successfully.`,
      });
    } catch {
      toast.error("Failed to add worker", {
        description: "An unexpected error occurred.",
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="space-y-2">
        <Label htmlFor="name">Worker Name</Label>
        <Input
          id="name"
          placeholder="My Production Worker"
          value={name}
          onChange={(e) => setName(e.target.value)}
          aria-invalid={!!errors.name}
          aria-describedby={errors.name ? "name-error" : undefined}
        />
        {errors.name && <p id="name-error" className="text-xs text-destructive">{errors.name}</p>}
      </div>

      <div className="space-y-2">
        <Label htmlFor="url">Worker URL</Label>
        <Input
          id="url"
          type="url"
          placeholder="https://worker.up.railway.app"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          aria-invalid={!!errors.url}
          aria-describedby={errors.url ? "url-error" : undefined}
        />
        {errors.url && <p id="url-error" className="text-xs text-destructive">{errors.url}</p>}
      </div>

      <div className="space-y-2">
        <Label htmlFor="secret">Internal Secret</Label>
        <div className="relative">
          <Input
            id="secret"
            type={showSecret ? "text" : "password"}
            placeholder="X-Internal-Secret value"
            value={secret}
            onChange={(e) => setSecret(e.target.value)}
            aria-invalid={!!errors.secret}
            aria-describedby={errors.secret ? "secret-error" : undefined}
          />
          <button
            type="button"
            tabIndex={-1}
            className="absolute right-2 top-1/2 -translate-y-1/2 rounded p-1 text-muted-foreground hover:text-foreground"
            onClick={() => setShowSecret(!showSecret)}
            aria-label={showSecret ? "Hide secret" : "Show secret"}
          >
            {showSecret ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
          </button>
        </div>
        {errors.secret && <p id="secret-error" className="text-xs text-destructive">{errors.secret}</p>}
      </div>

      <div className="flex justify-end gap-2 pt-2">
        <Button type="button" variant="outline" size="sm" onClick={onCancel} disabled={isSubmitting}>
          Cancel
        </Button>
        <Button type="submit" size="sm" disabled={isSubmitting}>
          {isSubmitting ? "Adding…" : "Add Worker"}
        </Button>
      </div>
    </form>
  );
}
