import { useQuery } from "@tanstack/react-query";

import { PageHeader } from "@/components/PageHeader";
import { Card, CardContent } from "@/components/ui/card";
import { apiFetch } from "@/lib/api-client";

type CalificacionRow = {
  materia_clave: string;
  materia_nombre: string;
  grupo: string;
  docente: string;
  periodo: string;
  unidades: (number | null)[];
};

const unidadHeaders = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"];

function promedio(nums: (number | null)[]): number | null {
  const v = nums.filter((n): n is number => typeof n === "number");
  if (!v.length) return null;
  return v.reduce((a, b) => a + b, 0) / v.length;
}

export default function CalificacionesPage() {
  const { data, isLoading, error } = useQuery({
    queryKey: ["calificaciones"],
    queryFn: () => apiFetch<CalificacionRow[]>("/calificaciones"),
  });

  const rows = data ?? [];
  const periodo = rows[0]?.periodo ?? "—";
  const promedios = rows.map((r) => promedio(r.unidades)).filter((p): p is number => p !== null);
  const promedioGeneral = promedios.length ? promedios.reduce((a, b) => a + b, 0) / promedios.length : 0;
  const unidadesEval = rows.reduce((a, r) => a + r.unidades.filter((u) => u !== null).length, 0);

  return (
    <div className="mx-auto max-w-[1300px] space-y-6">
      <PageHeader title="Calificaciones parciales" subtitle={`Periodo: ${periodo}`} />

      <div className="grid gap-4 md:grid-cols-3">
        <Stat label="Promedio del periodo" value={promedios.length ? promedioGeneral.toFixed(1) : "—"} highlight />
        <Stat label="Materias inscritas" value={String(rows.length)} />
        <Stat label="Unidades evaluadas" value={String(unidadesEval)} />
      </div>

      <Card>
        <CardContent className="overflow-x-auto p-0">
          <div className="bg-gradient-guinda px-5 py-2.5 text-primary-foreground">
            <div className="text-xs font-semibold uppercase tracking-[0.16em]">Calificaciones parciales</div>
          </div>
          {isLoading ? (
            <div className="p-10 text-center text-sm text-muted-foreground">Cargando…</div>
          ) : error ? (
            <div className="p-10 text-center text-sm text-destructive">Error al cargar calificaciones</div>
          ) : rows.length === 0 ? (
            <div className="p-10 text-center text-sm text-muted-foreground">Sin calificaciones registradas todavía.</div>
          ) : (
            <table className="w-full min-w-[1400px] text-sm">
              <thead>
                <tr className="bg-secondary/60 text-left text-[10px] uppercase tracking-[0.16em] text-muted-foreground">
                  <th className="px-4 py-3">Materia / Docente</th>
                  <th className="px-3 py-3 w-16 text-center">Grupo</th>
                  {unidadHeaders.map((h) => (
                    <th key={h} className="w-16 px-1 py-3 text-center font-mono">{h}</th>
                  ))}
                  <th className="px-3 py-3 w-20 text-center">Prom.</th>
                </tr>
              </thead>
              <tbody>
                {rows.map((m) => {
                  const prom = promedio(m.unidades);
                  return (
                    <tr key={m.materia_clave} className="border-t align-top hover:bg-secondary/30">
                      <td className="px-4 py-3">
                        <div className="font-mono text-[10px] text-muted-foreground">{m.materia_clave}</div>
                        <div className="text-sm font-medium leading-tight">{m.materia_nombre}</div>
                        <div className="mt-1 text-[11px] text-muted-foreground">{m.docente}</div>
                      </td>
                      <td className="px-3 py-3 text-center">
                        <span className="rounded-md bg-primary-soft px-2 py-0.5 font-mono text-xs font-medium text-primary">{m.grupo}</span>
                      </td>
                      {m.unidades.map((u, i) => (
                        <td key={i} className="px-1 py-3 text-center">
                          {u !== null ? (
                            <span
                              className={`inline-flex h-7 w-10 items-center justify-center rounded-md font-mono text-[12px] font-medium ${
                                u < 70 ? "bg-destructive/10 text-destructive" : u >= 90 ? "bg-success/10 text-success" : "bg-secondary text-foreground"
                              }`}
                            >
                              {u}
                            </span>
                          ) : (
                            <span className="text-muted-foreground/40">—</span>
                          )}
                        </td>
                      ))}
                      <td className="px-3 py-3 text-center">
                        <span className="inline-flex min-w-12 justify-center rounded-md bg-primary-soft px-2 py-1 font-mono text-sm font-semibold text-primary">
                          {prom !== null ? prom.toFixed(1) : "—"}
                        </span>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          )}
        </CardContent>
      </Card>
    </div>
  );
}

function Stat({ label, value, highlight }: { label: string; value: string; highlight?: boolean }) {
  return (
    <Card>
      <CardContent className={`p-5 ${highlight ? "bg-gradient-guinda text-primary-foreground rounded-lg" : ""}`}>
        <div className={`text-xs uppercase tracking-[0.16em] ${highlight ? "opacity-80" : "text-muted-foreground"}`}>{label}</div>
        <div className="mt-2 font-display text-3xl font-semibold">{value}</div>
      </CardContent>
    </Card>
  );
}
