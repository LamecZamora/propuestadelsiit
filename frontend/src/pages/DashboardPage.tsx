import { useQuery } from "@tanstack/react-query";
import { ArrowUpRight, CalendarDays, ClipboardList, GraduationCap, AlertTriangle, CheckCircle2, Info, Mail } from "lucide-react";
import { Link } from "react-router-dom";

import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { apiFetch } from "@/lib/api-client";
import { settings } from "@/lib/settings";

type CalificacionRow = { materia_nombre: string; parciales: (number | null)[] };
type DashboardData = { promedio_general: number | null; materias_en_curso: number; proxima_clase: { materia: string; dia_semana: string; hora_inicio: string; aula: string | null } | null };

const avisos = [
  { tipo: "atencion" as const, titulo: "Reinscripción", texto: "El horario de reinscripción será publicado después de las 11pm (hora en la que el banco proporciona la información de los pagos registrados)." },
  { tipo: "atencion" as const, titulo: "Tutorías obligatorias", texto: "A todos los alumnos que vayan a cursar segundo semestre, favor de cargar Tutorías (son créditos complementarios). Es de carácter obligatorio." },
  { tipo: "info" as const, titulo: "Buzón de quejas y sugerencias", texto: "¿Quieres compartir cómo te brindamos el servicio educativo? Escríbenos a sgc.buzondequejasysugerencias@itdurango.edu.mx" },
];

export default function DashboardPage() {
  const { data: dashboard } = useQuery({ queryKey: ["dashboard"], queryFn: () => apiFetch<DashboardData>("/dashboard") });
  const { data: calificaciones } = useQuery({ queryKey: ["calificaciones"], queryFn: () => apiFetch<CalificacionRow[]>("/calificaciones") });

  const nombreCorto = "Alumno";

  return (
    <div className="mx-auto max-w-7xl space-y-6">
      <div className="relative overflow-hidden rounded-3xl bg-gradient-guinda p-6 text-primary-foreground shadow-elegant md:p-8">
        <div className="pointer-events-none absolute inset-0 opacity-30 [background-image:radial-gradient(circle_at_20%_20%,white_0,transparent_40%),radial-gradient(circle_at_80%_60%,white_0,transparent_40%)]" />
        <div className="relative flex flex-col gap-6 md:flex-row md:items-end md:justify-between">
          <div>
            <div className="text-xs uppercase tracking-[0.18em] opacity-80">Buen día</div>
            <h1 className="mt-2 font-display text-3xl font-semibold md:text-4xl">{nombreCorto}, este es tu resumen académico.</h1>
            <p className="mt-2 max-w-xl text-sm opacity-90">
              {settings.CURRENT_PERIODO} · estado:{" "}
              <span className="inline-flex items-center gap-1 rounded-full bg-white/15 px-2 py-0.5 text-xs font-medium">
                <CheckCircle2 className="h-3 w-3" /> Inscrito
              </span>
            </p>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <Metric label="Promedio" value={dashboard?.promedio_general?.toFixed(1) ?? "—"} />
            <Metric label="Materias" value={String(dashboard?.materias_en_curso ?? 0)} />
          </div>
        </div>
      </div>

      <div className="grid gap-3 md:grid-cols-3">
        {avisos.map((a) => {
          const Icon = a.tipo === "atencion" ? AlertTriangle : Info;
          const color = a.tipo === "atencion" ? "border-warning/40 bg-warning/10 text-warning-foreground" : "border-primary/30 bg-primary-soft text-foreground";
          return (
            <div key={a.titulo} className={`rounded-2xl border p-4 ${color}`}>
              <div className="flex items-center gap-2">
                <Icon className={`h-4 w-4 ${a.tipo === "atencion" ? "text-warning" : "text-primary"}`} />
                <span className={`text-[10px] font-semibold uppercase tracking-[0.16em] ${a.tipo === "atencion" ? "text-warning" : "text-primary"}`}>
                  {a.tipo === "atencion" ? "Atención" : "Aviso"}
                </span>
              </div>
              <div className="mt-2 text-sm font-semibold leading-tight">{a.titulo}</div>
              <p className="mt-1 text-xs leading-relaxed text-foreground/80">{a.texto}</p>
            </div>
          );
        })}
      </div>

      <div className="grid gap-4 md:grid-cols-3">
        <QuickAction to="/calificaciones" icon={ClipboardList} title="Calificaciones" hint="Parciales del periodo" />
        <QuickAction to="/horario" icon={CalendarDays} title="Mi horario" hint={`${dashboard?.materias_en_curso ?? 0} materias inscritas`} />
        <QuickAction to="/kardex" icon={GraduationCap} title="Kardex" hint="Historial académico" />
      </div>

      <Card>
        <CardHeader className="flex flex-row items-center justify-between pb-3">
          <CardTitle className="text-sm font-medium text-muted-foreground">Materias en curso</CardTitle>
          <Link to="/calificaciones" className="text-xs font-medium text-primary">Ver todas</Link>
        </CardHeader>
        <CardContent>
          <ul className="divide-y">
            {(calificaciones ?? []).map((m) => {
              const [p1, p2, p3] = m.parciales;
              return (
                <li key={m.materia_nombre} className="flex items-center justify-between gap-3 py-3">
                  <div className="flex items-center gap-3">
                    <GraduationCap className="h-4 w-4 text-primary" />
                    <span className="text-sm font-medium">{m.materia_nombre}</span>
                  </div>
                  <div className="flex items-center gap-2 text-xs">
                    <Badge variant="secondary" className="font-mono">P1 {p1 ?? "—"}</Badge>
                    <Badge variant="secondary" className="font-mono">P2 {p2 ?? "—"}</Badge>
                    <Badge variant="secondary" className="font-mono">P3 {p3 ?? "—"}</Badge>
                  </div>
                </li>
              );
            })}
          </ul>
        </CardContent>
      </Card>

      {dashboard?.proxima_clase && (
        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="text-sm font-medium text-muted-foreground">Próxima clase</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-center justify-between rounded-xl border bg-card px-3 py-2.5">
              <div>
                <div className="text-sm font-medium">{dashboard.proxima_clase.materia}</div>
                <div className="text-[11px] text-muted-foreground">{dashboard.proxima_clase.dia_semana} · {dashboard.proxima_clase.aula ?? "—"}</div>
              </div>
              <Badge variant="secondary" className="font-mono">{dashboard.proxima_clase.hora_inicio}</Badge>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}

function Metric({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-2xl bg-white/10 px-4 py-3 backdrop-blur ring-1 ring-white/20">
      <div className="text-[10px] uppercase tracking-[0.18em] opacity-80">{label}</div>
      <div className="mt-1 font-display text-xl font-semibold">{value}</div>
    </div>
  );
}

function QuickAction({ to, icon: Icon, title, hint }: { to: string; icon: any; title: string; hint: string }) {
  return (
    <Link to={to} className="group flex items-center gap-3 rounded-2xl border bg-card p-4 shadow-card transition hover:-translate-y-0.5 hover:border-primary/30 hover:shadow-elegant">
      <div className="grid h-11 w-11 place-items-center rounded-xl bg-primary-soft text-primary">
        <Icon className="h-5 w-5" />
      </div>
      <div className="min-w-0 flex-1">
        <div className="text-sm font-medium">{title}</div>
        <div className="text-[11px] text-muted-foreground">{hint}</div>
      </div>
      <ArrowUpRight className="h-4 w-4 text-muted-foreground transition group-hover:text-primary" />
    </Link>
  );
}
