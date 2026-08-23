import {
  Award,
  Banknote,
  Building2,
  CalendarDays,
  ClipboardCheck,
  ClipboardList,
  FileSearch,
  FileSignature,
  GraduationCap,
  IdCard,
  LayoutDashboard,
  type LucideIcon,
  ScrollText,
  TrendingUp,
  Users,
  Wifi,
} from "lucide-react";
import { BookOpen } from "lucide-react";

export type NavItem = { title: string; url: string; icon: LucideIcon; group: string };

// Única fuente de verdad para la navegación (sidebar + buscador de comandos).
// Antes estaba duplicada en AppSidebar.tsx y CommandPalette.tsx por separado.
export const NAV_ITEMS: NavItem[] = [
  { title: "Inicio", url: "/dashboard", icon: LayoutDashboard, group: "Resumen" },

  { title: "Datos escolares", url: "/datos", icon: GraduationCap, group: "Información Escolar" },
  { title: "CURP y Beca", url: "/curp", icon: IdCard, group: "Información Escolar" },
  { title: "Horario", url: "/horario", icon: CalendarDays, group: "Información Escolar" },
  { title: "Calificaciones", url: "/calificaciones", icon: ClipboardList, group: "Información Escolar" },
  { title: "Exámenes esp./globales", url: "/examenes", icon: FileSearch, group: "Información Escolar" },
  { title: "Kardex", url: "/kardex", icon: BookOpen, group: "Información Escolar" },
  { title: "Avance reticular", url: "/avance", icon: TrendingUp, group: "Información Escolar" },
  { title: "Tutorías", url: "/tutorias", icon: Users, group: "Información Escolar" },
  { title: "Residencias", url: "/residencias", icon: Building2, group: "Información Escolar" },

  { title: "Reinscripción", url: "/inscripcion", icon: FileSignature, group: "Inscripciones" },
  { title: "Grupos cargados", url: "/grupos", icon: Users, group: "Inscripciones" },
  { title: "Ficha de depósito", url: "/ficha-pago", icon: Banknote, group: "Inscripciones" },
  { title: "Extraescolar", url: "/extraescolar", icon: Award, group: "Inscripciones" },

  { title: "Evaluación docente", url: "/evaluacion", icon: ClipboardCheck, group: "Evaluaciones" },
  { title: "Auditoría de servicios", url: "/auditoria", icon: ScrollText, group: "Evaluaciones" },

  { title: "Contrato", url: "/contrato", icon: FileSignature, group: "Cuenta" },
  { title: "Cuenta internet", url: "/cuenta", icon: Wifi, group: "Cuenta" },
];

export function agruparNavItems(items: NavItem[]): Array<{ label: string; items: NavItem[] }> {
  const orden: string[] = [];
  const porGrupo = new Map<string, NavItem[]>();
  for (const item of items) {
    if (!porGrupo.has(item.group)) {
      porGrupo.set(item.group, []);
      orden.push(item.group);
    }
    porGrupo.get(item.group)!.push(item);
  }
  return orden.map((label) => ({ label, items: porGrupo.get(label)! }));
}
