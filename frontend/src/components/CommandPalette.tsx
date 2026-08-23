import {
  BookOpen,
  CalendarDays,
  ClipboardCheck,
  ClipboardList,
  FileSearch,
  FileSignature,
  GraduationCap,
  IdCard,
  LayoutDashboard,
  LogOut,
  Moon,
  ScrollText,
  Sun,
  TrendingUp,
  Users,
  Wifi,
} from "lucide-react";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import { useAuth } from "@/auth/AuthContext";
import { useTheme } from "./ThemeProvider";
import {
  CommandDialog,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
  CommandSeparator,
} from "@/components/ui/command";

const routes = [
  { url: "/dashboard", label: "Inicio", icon: LayoutDashboard, group: "Navegación" },
  { url: "/datos", label: "Datos escolares", icon: GraduationCap, group: "Navegación" },
  { url: "/curp", label: "CURP y Beca", icon: IdCard, group: "Navegación" },
  { url: "/horario", label: "Horario", icon: CalendarDays, group: "Navegación" },
  { url: "/calificaciones", label: "Calificaciones", icon: ClipboardList, group: "Navegación" },
  { url: "/examenes", label: "Exámenes esp./globales", icon: FileSearch, group: "Navegación" },
  { url: "/kardex", label: "Kardex", icon: BookOpen, group: "Navegación" },
  { url: "/avance", label: "Avance reticular", icon: TrendingUp, group: "Navegación" },
  { url: "/tutorias", label: "Tutorías", icon: Users, group: "Navegación" },
  { url: "/inscripcion", label: "Reinscripción", icon: FileSignature, group: "Inscripciones" },
  { url: "/grupos", label: "Grupos cargados", icon: Users, group: "Inscripciones" },
  { url: "/evaluacion", label: "Evaluación docente", icon: ClipboardCheck, group: "Evaluaciones" },
  { url: "/auditoria", label: "Auditoría de servicios", icon: ScrollText, group: "Evaluaciones" },
  { url: "/contrato", label: "Contrato", icon: FileSignature, group: "Cuenta" },
  { url: "/cuenta", label: "Cuenta internet", icon: Wifi, group: "Cuenta" },
];

export function CommandPalette({ open, onOpenChange }: { open: boolean; onOpenChange: (v: boolean) => void }) {
  const navigate = useNavigate();
  const { theme, toggle } = useTheme();
  const { logout } = useAuth();

  const go = (url: string) => {
    onOpenChange(false);
    navigate(url);
  };

  const grouped = routes.reduce<Record<string, typeof routes>>((acc, r) => {
    (acc[r.group] ||= []).push(r);
    return acc;
  }, {});

  return (
    <CommandDialog open={open} onOpenChange={onOpenChange}>
      <CommandInput placeholder="Buscar página o acción…" />
      <CommandList>
        <CommandEmpty>Sin resultados.</CommandEmpty>
        {Object.entries(grouped).map(([group, items]) => (
          <CommandGroup key={group} heading={group}>
            {items.map((r) => (
              <CommandItem key={r.url} value={`${group} ${r.label}`} onSelect={() => go(r.url)}>
                <r.icon className="mr-2 h-4 w-4" />
                {r.label}
              </CommandItem>
            ))}
          </CommandGroup>
        ))}
        <CommandSeparator />
        <CommandGroup heading="Acciones">
          <CommandItem value="cambiar tema modo oscuro claro" onSelect={() => { toggle(); onOpenChange(false); }}>
            {theme === "dark" ? <Sun className="mr-2 h-4 w-4" /> : <Moon className="mr-2 h-4 w-4" />}
            Cambiar a modo {theme === "dark" ? "claro" : "oscuro"}
          </CommandItem>
          <CommandItem
            value="cerrar sesion logout salir"
            onSelect={() => {
              onOpenChange(false);
              logout();
              navigate("/");
            }}
          >
            <LogOut className="mr-2 h-4 w-4" />
            Cerrar sesión
          </CommandItem>
        </CommandGroup>
      </CommandList>
    </CommandDialog>
  );
}

export function useCommandPalette() {
  const [open, setOpen] = useState(false);
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") {
        e.preventDefault();
        setOpen((v) => !v);
      }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, []);
  return { open, setOpen };
}
