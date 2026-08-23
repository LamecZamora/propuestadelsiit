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
  ScrollText,
  TrendingUp,
  Users,
  Wifi,
} from "lucide-react";
import { Link, useLocation } from "react-router-dom";

import { useAuth } from "@/auth/AuthContext";
import { SiitLogo } from "@/components/SiitLogo";
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  useSidebar,
} from "@/components/ui/sidebar";

const groups: Array<{ label: string; items: Array<{ title: string; url: string; icon: any }> }> = [
  { label: "Resumen", items: [{ title: "Inicio", url: "/dashboard", icon: LayoutDashboard }] },
  {
    label: "Información Escolar",
    items: [
      { title: "Datos escolares", url: "/datos", icon: GraduationCap },
      { title: "CURP y Beca", url: "/curp", icon: IdCard },
      { title: "Horario", url: "/horario", icon: CalendarDays },
      { title: "Calificaciones", url: "/calificaciones", icon: ClipboardList },
      { title: "Exámenes esp./globales", url: "/examenes", icon: FileSearch },
      { title: "Kardex", url: "/kardex", icon: BookOpen },
      { title: "Avance reticular", url: "/avance", icon: TrendingUp },
      { title: "Tutorías", url: "/tutorias", icon: Users },
    ],
  },
  {
    label: "Inscripciones",
    items: [
      { title: "Reinscripción", url: "/inscripcion", icon: FileSignature },
      { title: "Grupos cargados", url: "/grupos", icon: Users },
    ],
  },
  {
    label: "Evaluaciones",
    items: [
      { title: "Evaluación docente", url: "/evaluacion", icon: ClipboardCheck },
      { title: "Auditoría de servicios", url: "/auditoria", icon: ScrollText },
    ],
  },
  {
    label: "Cuenta",
    items: [
      { title: "Contrato", url: "/contrato", icon: FileSignature },
      { title: "Cuenta internet", url: "/cuenta", icon: Wifi },
    ],
  },
];

function iniciales(nombre: string): string {
  const partes = nombre.trim().split(/\s+/);
  return ((partes[0]?.[0] ?? "") + (partes[1]?.[0] ?? "")).toUpperCase();
}

export function AppSidebar({ perfil }: { perfil: { nombre: string; matricula: string } }) {
  const { state } = useSidebar();
  const collapsed = state === "collapsed";
  const path = useLocation().pathname;

  return (
    <Sidebar collapsible="icon" className="border-r">
      <SidebarHeader className="border-b px-3 py-3">
        {!collapsed ? <SiitLogo /> : <SiitLogo className="justify-center [&>div:last-child]:hidden" />}
      </SidebarHeader>
      <SidebarContent>
        {groups.map((g) => (
          <SidebarGroup key={g.label}>
            {!collapsed && (
              <SidebarGroupLabel className="text-[10px] uppercase tracking-[0.18em] text-muted-foreground/70">
                {g.label}
              </SidebarGroupLabel>
            )}
            <SidebarGroupContent>
              <SidebarMenu>
                {g.items.map((item) => {
                  const active = path === item.url;
                  return (
                    <SidebarMenuItem key={item.url}>
                      <SidebarMenuButton
                        asChild
                        isActive={active}
                        tooltip={item.title}
                        className="data-[active=true]:bg-primary-soft data-[active=true]:text-primary data-[active=true]:font-medium"
                      >
                        <Link to={item.url} className="flex items-center gap-2.5">
                          <item.icon className="h-4 w-4 shrink-0" />
                          <span>{item.title}</span>
                        </Link>
                      </SidebarMenuButton>
                    </SidebarMenuItem>
                  );
                })}
              </SidebarMenu>
            </SidebarGroupContent>
          </SidebarGroup>
        ))}
      </SidebarContent>
      <SidebarFooter className="border-t p-3">
        {!collapsed ? (
          <div className="flex items-center gap-3">
            <div className="grid h-9 w-9 place-items-center rounded-full bg-gradient-guinda text-xs font-semibold text-primary-foreground">
              {iniciales(perfil.nombre)}
            </div>
            <div className="min-w-0 leading-tight">
              <div className="truncate text-sm font-medium">{perfil.nombre}</div>
              <div className="truncate text-[11px] text-muted-foreground">No. {perfil.matricula}</div>
            </div>
          </div>
        ) : (
          <div className="mx-auto grid h-9 w-9 place-items-center rounded-full bg-gradient-guinda text-xs font-semibold text-primary-foreground">
            {iniciales(perfil.nombre)}
          </div>
        )}
      </SidebarFooter>
    </Sidebar>
  );
}

export { iniciales };
