import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import { Toaster } from "sonner";

import { AuthProvider } from "@/auth/AuthContext";
import { RequireAuth } from "@/auth/RequireAuth";
import { ThemeProvider } from "@/components/ThemeProvider";
import { AppLayout } from "@/layouts/AppLayout";
import CalificacionesPage from "@/pages/CalificacionesPage";
import ComingSoonPage from "@/pages/ComingSoonPage";
import DashboardPage from "@/pages/DashboardPage";
import HorarioPage from "@/pages/HorarioPage";
import KardexPage from "@/pages/KardexPage";
import LoginPage from "@/pages/LoginPage";

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
});

const MODULOS_FUTUROS = [
  "/datos", "/curp", "/examenes", "/avance", "/tutorias",
  "/inscripcion", "/grupos", "/evaluacion", "/auditoria", "/contrato", "/cuenta",
];

export default function App() {
  return (
    <ThemeProvider>
      <QueryClientProvider client={queryClient}>
        <AuthProvider>
          <BrowserRouter>
            <Routes>
              <Route path="/" element={<LoginPage />} />
              <Route element={<RequireAuth />}>
                <Route element={<AppLayout />}>
                  <Route path="/dashboard" element={<DashboardPage />} />
                  <Route path="/horario" element={<HorarioPage />} />
                  <Route path="/calificaciones" element={<CalificacionesPage />} />
                  <Route path="/kardex" element={<KardexPage />} />
                  {MODULOS_FUTUROS.map((path) => (
                    <Route key={path} path={path} element={<ComingSoonPage />} />
                  ))}
                </Route>
              </Route>
              <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
          </BrowserRouter>
        </AuthProvider>
      </QueryClientProvider>
      <Toaster richColors position="top-right" />
    </ThemeProvider>
  );
}
