export class ApiError extends Error {
  public readonly status: number;
  public readonly detail: string;

  constructor(status: number, detail: string) {
    super(detail);
    this.name = "ApiError";
    this.status = status;
    this.detail = detail;
  }

  get isNetworkError(): boolean {
    return this.status === 0 || this.status === 408;
  }

  get isNotFound(): boolean {
    return this.status === 404;
  }

  get isAuthError(): boolean {
    return this.status === 403;
  }
}
