"use client";

import { useState } from "react";
import { useWorkersStore } from "@/lib/store/workers";
import { createWorkerApi } from "@/lib/api/workers";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { toast } from "@/hooks/use-toast";
import { Pause, Power, Trash2, AlertTriangle } from "lucide-react";
import { LoadingSpinner } from "@/components/ui/loading-spinner";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
  DialogFooter,
} from "@/components/ui/dialog";

interface BotActionButtonsProps {
  workerId: string;
  userId: string;
  onStatusChanged?: () => void;
}

type DialogType = "stop" | "delete" | "deleteFile" | null;

export function BotActionButtons({ workerId, userId, onStatusChanged }: BotActionButtonsProps) {
  const worker = useWorkersStore((s) => s.workers.find((w) => w.id === workerId));
  const [isStopping, setIsStopping] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);
  const [activeDialog, setActiveDialog] = useState<DialogType>(null);
  const [confirmText, setConfirmText] = useState("");
  const [fileFilename, setFileFilename] = useState("bot.php");

  if (!worker) return null;

  const closeDialog = () => {
    setActiveDialog(null);
    setConfirmText("");
    setFileFilename("bot.php");
  };

  const handleStop = async () => {
    closeDialog();
    setIsStopping(true);
    try {
      const api = createWorkerApi(worker);
      await api.bots.stop(userId);
      toast.success("Bot stopped", {
        description: `Bot for user ${userId} has been stopped (webhook removed).`,
      });
      onStatusChanged?.();
    } catch (err) {
      const error = err as Error;
      toast.error("Failed to stop bot", { description: error.message });
    } finally {
      setIsStopping(false);
    }
  };

  const handleDelete = async () => {
    closeDialog();
    setIsDeleting(true);
    try {
      const api = createWorkerApi(worker);
      await api.bots.deleteBot(userId);
      toast.success("Bot fully deleted", {
        description: `Bot for user ${userId} has been completely removed.`,
      });
      onStatusChanged?.();
    } catch (err) {
      const error = err as Error;
      toast.error("Failed to delete bot", { description: error.message });
    } finally {
      setIsDeleting(false);
    }
  };

  const handleDeleteFile = async () => {
    const filename = fileFilename.trim() || "bot.php";
    closeDialog();
    setIsDeleting(true);
    try {
      const api = createWorkerApi(worker);
      await api.bots.deleteFile(userId, filename);
      toast.success("File deleted", {
        description: `${filename} deleted for user ${userId}.`,
      });
      onStatusChanged?.();
    } catch (err) {
      const error = err as Error;
      toast.error("Failed to delete file", { description: error.message });
    } finally {
      setIsDeleting(false);
    }
  };

  const confirmDeleteReady = confirmText === userId;

  return (
    <>
      <div className="flex gap-2">
        <Button
          variant="outline"
          size="sm"
          onClick={() => setActiveDialog("stop")}
          disabled={isStopping || isDeleting}
          className="border-yellow-500/30 text-yellow-700 hover:bg-yellow-500/10 dark:text-yellow-400"
        >
          {isStopping ? (
            <LoadingSpinner size="sm" className="mr-2" />
          ) : (
            <Pause className="h-4 w-4 mr-1" />
          )}
          Stop Bot
        </Button>

        <Button
          variant="destructive"
          size="sm"
          onClick={() => setActiveDialog("delete")}
          disabled={isStopping || isDeleting}
        >
          {isDeleting ? (
            <LoadingSpinner size="sm" className="mr-2" />
          ) : (
            <Power className="h-4 w-4 mr-1" />
          )}
          Delete Bot
        </Button>

        <Button
          variant="outline"
          size="sm"
          onClick={() => setActiveDialog("deleteFile")}
          disabled={isStopping || isDeleting}
        >
          <Trash2 className="h-4 w-4 mr-1" />
          Delete File
        </Button>
      </div>

      {/* Stop Confirmation */}
      <Dialog open={activeDialog === "stop"} onOpenChange={(open) => !open && closeDialog()}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle className="flex items-center gap-2">
              <AlertTriangle className="h-5 w-5 text-amber-500" />
              Stop Bot
            </DialogTitle>
            <DialogDescription>
              This will remove the webhook for user <strong>{userId}</strong> and set the bot
              status to &quot;stopped&quot;. The bot files will not be removed.
            </DialogDescription>
          </DialogHeader>
          <DialogFooter>
            <Button variant="outline" size="sm" onClick={closeDialog}>
              Cancel
            </Button>
            <Button variant="outline" size="sm" onClick={handleStop} disabled={isStopping}>
              {isStopping ? "Stopping…" : "Stop Bot"}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Delete Bot Confirmation */}
      <Dialog open={activeDialog === "delete"} onOpenChange={(open) => !open && closeDialog()}>
        <DialogContent className="border-destructive/30">
          <DialogHeader>
            <DialogTitle className="flex items-center gap-2 text-destructive">
              <AlertTriangle className="h-5 w-5" />
              Delete Bot (Destructive)
            </DialogTitle>
            <DialogDescription>
              This will <strong>permanently delete</strong> the bot for user{" "}
              <strong>{userId}</strong>. This action removes the webhook, deletes the bot
              directory on the worker, and removes it from the registry.
              <br />
              <br />
              This cannot be undone. The bot token and files will be lost.
            </DialogDescription>
          </DialogHeader>
          <div className="space-y-2">
            <Label htmlFor="confirm-delete">
              Type <strong>{userId}</strong> to confirm:
            </Label>
            <Input
              id="confirm-delete"
              placeholder={userId}
              value={confirmText}
              onChange={(e) => setConfirmText(e.target.value)}
            />
          </div>
          <DialogFooter>
            <Button variant="outline" size="sm" onClick={closeDialog}>
              Cancel
            </Button>
            <Button
              variant="destructive"
              size="sm"
              onClick={handleDelete}
              disabled={isDeleting || !confirmDeleteReady}
            >
              {isDeleting ? "Deleting…" : "Delete Bot"}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Delete File Confirmation */}
      <Dialog open={activeDialog === "deleteFile"} onOpenChange={(open) => !open && closeDialog()}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle className="flex items-center gap-2">
              <AlertTriangle className="h-5 w-5 text-amber-500" />
              Delete File
            </DialogTitle>
            <DialogDescription>
              Delete a single file from the bot directory for user <strong>{userId}</strong>.
              The default is <code>bot.php</code>. Only the specified file will be removed.
            </DialogDescription>
          </DialogHeader>
          <div className="space-y-2">
            <Label htmlFor="filename-input">Filename</Label>
            <Input
              id="filename-input"
              placeholder="bot.php"
              value={fileFilename}
              onChange={(e) => setFileFilename(e.target.value)}
            />
          </div>
          <DialogFooter>
            <Button variant="outline" size="sm" onClick={closeDialog}>
              Cancel
            </Button>
            <Button
              variant="outline"
              size="sm"
              onClick={handleDeleteFile}
              disabled={isDeleting || !fileFilename.trim()}
            >
              {isDeleting ? "Deleting…" : "Delete File"}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </>
  );
}
