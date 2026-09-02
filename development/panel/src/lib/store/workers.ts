import { create } from "zustand";
import { persist } from "zustand/middleware";
import { v4 as uuidv4 } from "uuid";
import type { WorkerConfig } from "@/lib/types";

const STORAGE_KEY = "telegram_workers";

export interface WorkersState {
  workers: WorkerConfig[];
  selectedWorkerId: string | null;
  addWorker: (name: string, url: string, secret: string) => string;
  updateWorker: (id: string, updates: Partial<Omit<WorkerConfig, "id" | "createdAt">>) => void;
  removeWorker: (id: string) => void;
  setSelectedWorker: (id: string | null) => void;
  clearWorkers: () => void;
}

export const useWorkersStore = create<WorkersState>()(
  persist(
    (set, get) => ({
      workers: [],
      selectedWorkerId: null,
      addWorker: (name, url, secret) => {
        const id = uuidv4();
        const newWorker: WorkerConfig = {
          id,
          name,
          url,
          secret,
          createdAt: new Date().toISOString(),
        };
        set((state) => ({
          workers: [...state.workers, newWorker],
          selectedWorkerId: state.workers.length === 0 ? id : state.selectedWorkerId,
        }));
        return id;
      },
      updateWorker: (id, updates) => {
        set((state) => ({
          workers: state.workers.map((w) => (w.id === id ? { ...w, ...updates } : w)),
        }));
      },
      removeWorker: (id) => {
        const { workers, selectedWorkerId } = get();
        const newSelectedId = selectedWorkerId === id
          ? (workers.find((w) => w.id !== id)?.id ?? null)
          : selectedWorkerId;
        set((state) => ({
          workers: state.workers.filter((w) => w.id !== id),
          selectedWorkerId: newSelectedId,
        }));
      },
      setSelectedWorker: (id) => {
        set({ selectedWorkerId: id });
      },
      clearWorkers: () => {
        set({ workers: [], selectedWorkerId: null });
      },
    }),
    {
      name: STORAGE_KEY,
      partialize: (state) => ({
        workers: state.workers,
        selectedWorkerId: state.selectedWorkerId,
      }),
    }
  )
);

export const useWorkers = () => {
  const workers = useWorkersStore((state) => state.workers);
  const selectedWorkerId = useWorkersStore((state) => state.selectedWorkerId);
  const selectedWorker = workers.find((w) => w.id === selectedWorkerId) ?? null;
  const addWorker = useWorkersStore((state) => state.addWorker);
  const updateWorker = useWorkersStore((state) => state.updateWorker);
  const removeWorker = useWorkersStore((state) => state.removeWorker);
  const setSelectedWorker = useWorkersStore((state) => state.setSelectedWorker);
  const clearWorkers = useWorkersStore((state) => state.clearWorkers);

  return {
    workers,
    selectedWorkerId,
    selectedWorker,
    addWorker,
    updateWorker,
    removeWorker,
    setSelectedWorker,
    clearWorkers,
  };
};

export const getWorkers = (): WorkerConfig[] => {
  if (typeof window === "undefined") return [];
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return [];
    const parsed = JSON.parse(raw) as { state?: { workers?: WorkerConfig[] } };
    return parsed.state?.workers ?? [];
  } catch {
    return [];
  }
};
