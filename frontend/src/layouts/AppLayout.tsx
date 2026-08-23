import { Bell, Command as CommandIcon, LogOut, Search } from "lucide-react";
import { useQuery } from "@tanstack/react-query";
import { Outlet, useNavigate } from "react-router-dom";

import { useAuth } from "@/auth/AuthContext";
import { AppSidebar, iniciales } from "@/components/AppSidebar";
import { CommandPalette, useCommandPalette } from "@/components/CommandPalette";
import { ThemeToggle } from "@/components/ThemeToggle";
import { SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar";
import { apiFetch } from "@/lib/api-client";
import { settings } from "@/lib/settings";

type Perfil = { matricula: string; nombre: string; correo: string; carrera: string; semestre: number };

export function AppLayout() {
  const { open, setOpen } = useCommandPalette();
  const { logout } = useAuth();
  const navigate = useNavigate();
  const { data: perfil } = useQuery({ queryKey: ["perfil"], queryFn: () => apiFetch<Perfil>("/auth/me") });

  function handleLogout() {
    logout();
    navigate("/");
  }

  if (!perfil) {
    return <div className="grid min-h-screen place-items-center bg-background text-sm text-muted-foreground">Cargando…</div>;
  }

  return (
    <SidebarProvider>
      <div className="flex min-h-screen w-full bg-gradient-soft">
        <AppSidebar perfil={perfil} />
        <div className="flex min-w-0 flex-1 flex-col">
          <header className="sticky top-0 z-30 flex h-14 items-center gap-3 border-b bg-background/80 px-4 backdrop-blur">
            <SidebarTrigger className="-ml-1" />
            <div className="hidden h-6 w-px bg-border md:block" />
            <div className="hidden flex-col leading-tight md:flex">
              <span className="text-[11px] uppercase tracking-[0.16em] text-muted-foreground">Periodo</span>
              <span className="text-xs font-medium">{settings.CURRENT_PERIODO}</span>
            </div>
            <button
              onClick={() => setOpen(true)}
              className="ml-auto hidden h-9 w-72 items-center gap-2 rounded-md border bg-secondary/60 px-3 text-left text-xs text-muted-foreground transition hover:bg-secondary md:flex"
            >
              <Search className="h-3.5 w-3.5" />
              <span className="flex-1">Buscar página, acción…</span>
              <kbd className="pointer-events-none inline-flex h-5 select-none items-center gap-1 rounded border bg-background px-1.5 font-mono text-[10px] font-medium">
                <CommandIcon className="h-3 w-3" />K
              </kbd>
            </button>
            <ThemeToggle />
            <button className="relative grid h-9 w-9 place-items-center rounded-full text-muted-foreground hover:bg-secondary hover:text-foreground transition">
              <Bell className="h-4 w-4" />
              <span className="absolute right-2 top-2 h-1.5 w-1.5 rounded-full bg-primary" />
            </button>
            <button
              onClick={handleLogout}
              className="grid h-9 w-9 place-items-center rounded-full text-muted-foreground hover:bg-secondary hover:text-foreground transition"
              aria-label="Cerrar sesión"
            >
              <LogOut className="h-4 w-4" />
            </button>
            <div className="ml-1 hidden items-center gap-2 md:flex">
              <div className="grid h-8 w-8 place-items-center rounded-full bg-gradient-guinda text-[11px] font-semibold text-primary-foreground">
                {iniciales(perfil.nombre)}
              </div>
            </div>
          </header>
          <main className="flex-1 p-4 md:p-8">
            <Outlet />
          </main>
        </div>
        <CommandPalette open={open} onOpenChange={setOpen} />
      </div>
    </SidebarProvider>
  );
}
