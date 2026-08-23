import { useQuery } from "@tanstack/react-query";
import { AlertCircle } from "lucide-react";

import { PageHeader } from "@/components/PageHeader";
import { Card, CardContent } from "@/components/ui/card";
import { apiFetch } from "@/lib/api-client";

type SesionHorario = { dia: string; hora_inicio: string; hora_fin: string };
type HorarioRow = {
  materia_clave: string;
  materia_nombre: string;
  grupo: string;
  docente: string;
  creditos: number;
  aula: string;
  sesiones: SesionHorario[];
};
type HorarioResponse = { periodo: string; rows: HorarioRow[] };

const dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"];

export default function HorarioPage() {
  const { data, isLoading, error } = useQuery({
    queryKey: ["horario"],
    queryFn: () => apiFetch<HorarioResponse>("/horario"),
  });

  const rows = data?.rows ?? [];
  const periodo = data?.periodo ?? "—";
  const totalCreditos = rows.reduce((a, m) => a + m.creditos, 0);

  return (
    <div className="mx-auto max-w-[1200px] space-y-6">
      <PageHeader title="Horario del alumno" subtitle={`Periodo en curso: ${periodo}`} />

      <Card>
        <CardContent className="overflow-x-auto p-0">
          {isLoading ? (
            <div className="p-10 text-center text-sm text-muted-foreground">Cargando…</div>
          ) : error ? (
            <div className="p-10 text-center text-sm text-destructive">Error al cargar horario</div>
          ) : rows.length === 0 ? (
            <div className="p-10 text-center text-sm text-muted-foreground">No tienes materias inscritas en este periodo.</div>
          ) : (
            <table className="w-full min-w-[1030px] text-sm">
              <thead>
                <tr className="bg-secondary/60 text-left text-[10px] uppercase tracking-[0.16em] text-muted-foreground">
                  <th className="px-4 py-3">Materia / Docente</th>
                  <th className="px-3 py-3 w-16 text-center">Grupo</th>
                  <th className="px-3 py-3 w-14 text-center">Cr.</th>
                  {dias.map((d) => (
                    <th key={d} className="px-2 py-3 w-[110px] text-center">{d}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {rows.map((m) => (
                  <tr key={m.materia_clave} className="border-t align-top">
                    <td className="px-4 py-3">
                      <div className="font-mono text-[10px] text-muted-foreground">{m.materia_clave}</div>
                      <div className="text-sm font-medium leading-tight">{m.materia_nombre}</div>
                      <div className="mt-1 text-[11px] text-muted-foreground">{m.docente}</div>
                    </td>
                    <td className="px-3 py-3 text-center">
                      <span className="rounded-md bg-primary-soft px-2 py-0.5 font-mono text-xs font-medium text-primary">{m.grupo}</span>
                    </td>
                    <td className="px-3 py-3 text-center font-mono">{m.creditos}</td>
                    {dias.map((d) => {
                      const sesion = m.sesiones.find((s) => s.dia === d);
                      return (
                        <td key={d} className="px-2 py-3 text-center">
                          {sesion ? (
                            <div className="rounded-md bg-primary-soft px-2 py-1 text-[11px] font-medium text-primary">
                              {sesion.hora_inicio}–{sesion.hora_fin}
                              {m.aula !== "—" && <div className="text-[10px] opacity-70">{m.aula}</div>}
                            </div>
                          ) : (
                            <span className="text-muted-foreground/40">—</span>
                          )}
                        </td>
                      );
                    })}
                  </tr>
                ))}
              </tbody>
              <tfoot>
                <tr className="border-t bg-gradient-guinda text-primary-foreground">
                  <td colSpan={2} className="px-4 py-2.5 text-right text-xs font-semibold uppercase tracking-[0.14em]">Total créditos</td>
                  <td className="px-3 py-2.5 text-center font-mono text-sm font-semibold">{totalCreditos}</td>
                  <td colSpan={6} />
                </tr>
              </tfoot>
            </table>
          )}
        </CardContent>
      </Card>

      <div className="flex items-start gap-3 rounded-xl border border-warning/30 bg-warning/10 p-4 text-sm">
        <AlertCircle className="mt-0.5 h-4 w-4 shrink-0 text-warning" />
        <div>
          <div className="font-medium">Periodo {periodo}</div>
          <p className="text-xs text-muted-foreground">
            Las altas y bajas de las materias deben solicitarse dentro de las fechas oficiales del calendario escolar.
          </p>
        </div>
      </div>
    </div>
  );
}
