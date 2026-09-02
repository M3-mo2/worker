"use client";

import { toast as sonnerToast, type ExternalToast } from "sonner";

type ToastFn = (message: string, data?: ExternalToast) => string | number;

export interface UseToastResult {
  (message: string, options?: ExternalToast): string | number;
  success: ToastFn;
  error: ToastFn;
  warning: ToastFn;
  info: ToastFn;
  promise: typeof sonnerToast.promise;
  dismiss: typeof sonnerToast.dismiss;
  loading: ToastFn;
}

export const useToast = (): UseToastResult => {
  const toast: UseToastResult = ((message: string, options?: ExternalToast) => {
    return sonnerToast(message, options);
  }) as UseToastResult;

  toast.success = sonnerToast.success;
  toast.error = sonnerToast.error;
  toast.warning = sonnerToast.warning;
  toast.info = sonnerToast.info;
  toast.promise = sonnerToast.promise;
  toast.dismiss = sonnerToast.dismiss;
  toast.loading = sonnerToast.loading;

  return toast;
};

export const toast = {
  success: (message: string, options?: ExternalToast) => sonnerToast.success(message, options),
  error: (message: string, options?: ExternalToast) => sonnerToast.error(message, options),
  warning: (message: string, options?: ExternalToast) => sonnerToast.warning(message, options),
  info: (message: string, options?: ExternalToast) => sonnerToast.info(message, options),
  promise: sonnerToast.promise,
  dismiss: sonnerToast.dismiss,
  loading: (message: string, options?: ExternalToast) => sonnerToast.loading(message, options),
};
