const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";
const TOKEN_KEY = "siit_token";

export function getToken(): string | null {
  return localStorage.getItem(TOKEN_KEY);
}

export function hasToken(): boolean {
  return getToken() !== null;
}

export function setToken(token: string | null) {
  if (token) {
    localStorage.setItem(TOKEN_KEY, token);
  } else {
    localStorage.removeItem(TOKEN_KEY);
  }
}

export class ApiError extends Error {
  status: number;

  constructor(status: number, message: string) {
    super(message);
    this.status = status;
  }
}

export async function apiFetch<T>(path: string, options: RequestInit = {}): Promise<T> {
  const headers = new Headers(options.headers);
  headers.set("Content-Type", "application/json");
  const token = getToken();
  if (token) headers.set("Authorization", `Bearer ${token}`);

  const response = await fetch(`${API_URL}${path}`, { ...options, headers });

  if (!response.ok) {
    const body = await response.json().catch(() => ({ detail: "Error desconocido" }));
    throw new ApiError(response.status, body.detail ?? "Error desconocido");
  }

  return response.json() as Promise<T>;
}
