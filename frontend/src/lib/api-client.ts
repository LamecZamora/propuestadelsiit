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

// Se registra desde AuthContext para reaccionar a un 401 en CUALQUIER
// llamada autenticada (no solo en AppLayout) cerrando sesión de forma
// uniforme; RequireAuth se encarga de redirigir una vez que isAuthenticated
// pasa a false, sin necesidad de navegar manualmente desde aquí.
type UnauthorizedHandler = () => void;
let unauthorizedHandler: UnauthorizedHandler | null = null;

export function setUnauthorizedHandler(handler: UnauthorizedHandler | null) {
  unauthorizedHandler = handler;
}

export async function apiFetch<T>(path: string, options: RequestInit = {}): Promise<T> {
  const headers = new Headers(options.headers);
  headers.set("Content-Type", "application/json");
  const token = getToken();
  if (token) headers.set("Authorization", `Bearer ${token}`);

  const response = await fetch(`${API_URL}${path}`, { ...options, headers });

  if (!response.ok) {
    const body = await response.json().catch(() => ({ detail: "Error desconocido" }));
    // Solo tratamos el 401 como "sesión expirada" si la petición SÍ llevaba
    // token — un 401 de /auth/login (sin token) es simplemente credenciales
    // incorrectas, no una sesión que haya que cerrar.
    if (response.status === 401 && token) {
      unauthorizedHandler?.();
    }
    throw new ApiError(response.status, body.detail ?? "Error desconocido");
  }

  return response.json() as Promise<T>;
}
