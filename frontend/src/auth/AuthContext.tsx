import { createContext, useContext, useEffect, useState, type ReactNode } from "react";

import { apiFetch, hasToken, setToken, setUnauthorizedHandler } from "@/lib/api-client";

interface AuthContextValue {
  isAuthenticated: boolean;
  login: (matricula: string, password: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextValue | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [isAuthenticated, setIsAuthenticated] = useState(() => hasToken());

  async function login(matricula: string, password: string) {
    const { access_token } = await apiFetch<{ access_token: string; token_type: string }>("/auth/login", {
      method: "POST",
      body: JSON.stringify({ matricula, password }),
    });
    setToken(access_token);
    setIsAuthenticated(true);
  }

  function logout() {
    setToken(null);
    setIsAuthenticated(false);
  }

  // Cualquier apiFetch autenticado que reciba un 401 (token vencido/inválido)
  // cierra sesión aquí; RequireAuth redirige solo al ver isAuthenticated=false.
  useEffect(() => {
    setUnauthorizedHandler(logout);
    return () => setUnauthorizedHandler(null);
  }, []);

  return <AuthContext.Provider value={{ isAuthenticated, login, logout }}>{children}</AuthContext.Provider>;
}

export function useAuth(): AuthContextValue {
  const context = useContext(AuthContext);
  if (!context) throw new Error("useAuth debe usarse dentro de AuthProvider");
  return context;
}
