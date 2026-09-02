"use client";

import { Plus } from "lucide-react";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
} from "@/components/ui/dialog";
import { AddWorkerForm } from "@/components/workers/add-worker-form";

export function AddWorkerShortcut({ className }: { className?: string }) {
  const [open, setOpen] = useState(false);

  return (
    <>
      <Button onClick={() => setOpen(true)} className={className}>
        <Plus className="h-4 w-4 mr-2" />
        Add Worker
      </Button>

      <Dialog open={open} onOpenChange={setOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Add Worker</DialogTitle>
            <DialogDescription>
              Add a new Telegram Bot Hosting Worker to manage bots on.
            </DialogDescription>
          </DialogHeader>
          <AddWorkerForm onSuccess={() => setOpen(false)} onCancel={() => setOpen(false)} />
        </DialogContent>
      </Dialog>
    </>
  );
}
