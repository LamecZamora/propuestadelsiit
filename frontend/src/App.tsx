import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import { Toaster } from "sonner";

import { AuthProvider } from "@/auth/AuthContext";
import { RequireAuth } from "@/auth/RequireAuth";
import { ThemeProvider } from "@/components/ThemeProvider";
import { AppLayout } from "@/layouts/AppLayout";
import AvancePage from "@/pages/AvancePage";
import BecaPage from "@/pages/BecaPage";
import CalificacionesPage from "@/pages/CalificacionesPage";
import ComingSoonPage from "@/pages/ComingSoonPage";
import DashboardPage from "@/pages/DashboardPage";
import DatosEscolaresPage from "@/pages/DatosEscolaresPage";
import ExtraescolarPage from "@/pages/ExtraescolarPage";
import FichaPagoPage from "@/pages/FichaPagoPage";
import HorarioPage from "@/pages/HorarioPage";
import KardexPage from "@/pages/KardexPage";
import LoginPage from "@/pages/LoginPage";
import ReinscripcionPage from "@/pages/ReinscripcionPage";
import ResidenciasPage from "@/pages/ResidenciasPage";
import { NAV_ITEMS } from "@/lib/nav";

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
});

// Rutas de NAV_ITEMS que ya tienen página real construida — todo lo demás
// del sidebar/buscador cae automáticamente en ComingSoonPage.
const RUTAS_CONSTRUIDAS = new Set([
  "/dashboard", "/horario", "/calificaciones", "/kardex", "/avance",
  "/curp", "/inscripcion", "/residencias", "/ficha-pago", "/extraescolar", "/datos",
]);
const MODULOS_FUTUROS = NAV_ITEMS.map((item) => item.url).filter((url) => !RUTAS_CONSTRUIDAS.has(url));

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
                  <Route path="/avance" element={<AvancePage />} />
                  <Route path="/curp" element={<BecaPage />} />
                  <Route path="/inscripcion" element={<ReinscripcionPage />} />
                  <Route path="/residencias" element={<ResidenciasPage />} />
                  <Route path="/ficha-pago" element={<FichaPagoPage />} />
                  <Route path="/extraescolar" element={<ExtraescolarPage />} />
                  <Route path="/datos" element={<DatosEscolaresPage />} />
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
