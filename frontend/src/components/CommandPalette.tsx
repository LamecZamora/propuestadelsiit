import { LogOut, Moon, Sun } from "lucide-react";
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
import { NAV_ITEMS } from "@/lib/nav";

const routes = NAV_ITEMS.map((item) => ({ url: item.url, label: item.title, icon: item.icon, group: item.group }));

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
