import { useMemo, useState } from "react";
import { useQuery } from "@tanstack/react-query";

import { PageHeader } from "@/components/PageHeader";
import { Card, CardContent } from "@/components/ui/card";
import { apiFetch } from "@/lib/api-client";
import { cn } from "@/lib/utils";

type SesionGrupo = { dia: string; hora_inicio: string; hora_fin: string; aula: string | null };
type GrupoCargadoRow = {
  semestre: number;
  clave_grupo: string;
  materia_clave: string;
  materia_nombre: string;
  docente: string;
  sesiones: SesionGrupo[];
};
type GruposCargadosResponse = { periodo: string; rows: GrupoCargadoRow[] };

const DIAS = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"];

export default function GruposCargadosPage() {
  const { data, isLoading, error } = useQuery({
    queryKey: ["grupos-cargados"],
    queryFn: () => apiFetch<GruposCargadosResponse>("/grupos-cargados"),
  });

  const [semestre, setSemestre] = useState<number | "todos">("todos");

  const rows = data?.rows ?? [];
  const periodo = data?.periodo ?? "—";
  const semestres = useMemo(() => Array.from(new Set(rows.map((r) => r.semestre))).sort((a, b) => a - b), [rows]);
  const filas = semestre === "todos" ? rows : rows.filter((r) => r.semestre === semestre);

  return (
    <div className="mx-auto max-w-[1300px] space-y-6">
      <PageHeader title="Grupos Cargados" subtitle={`Al periodo ${periodo}`} />

      {!isLoading && !error && rows.length > 0 && (
        <div className="flex flex-wrap gap-2">
          <button
            onClick={() => setSemestre("todos")}
            className={cn(
              "rounded-full border px-3 py-1 text-xs font-medium transition-colors",
              semestre === "todos" ? "border-primary bg-primary-soft text-primary" : "border-border text-muted-foreground hover:bg-secondary/60"
            )}
          >
            Todos
          </button>
          {semestres.map((s) => (
            <button
              key={s}
              onClick={() => setSemestre(s)}
              className={cn(
                "rounded-full border px-3 py-1 text-xs font-medium transition-colors",
                semestre === s ? "border-primary bg-primary-soft text-primary" : "border-border text-muted-foreground hover:bg-secondary/60"
              )}
            >
              Semestre {s}
            </button>
          ))}
        </div>
      )}

      <Card>
        <CardContent className="overflow-x-auto p-0">
          {isLoading ? (
            <div className="p-10 text-center text-sm text-muted-foreground">Cargando…</div>
          ) : error ? (
            <div className="p-10 text-center text-sm text-destructive">Error al cargar grupos cargados</div>
          ) : filas.length === 0 ? (
            <div className="p-10 text-center text-sm text-muted-foreground">No hay grupos cargados para este filtro.</div>
          ) : (
            <table className="w-full min-w-[1150px] text-sm">
              <thead>
                <tr className="bg-secondary/60 text-left text-[10px] uppercase tracking-[0.16em] text-muted-foreground">
                  <th className="px-3 py-3 w-16 text-center">Grupo</th>
                  <th className="px-4 py-3">Materia / Docente</th>
                  <th className="px-3 py-3 w-16 text-center">Sem.</th>
                  {DIAS.map((d) => (
                    <th key={d} className="px-2 py-3 w-[105px] text-center">{d}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {filas.map((g, i) => (
                  <tr key={`${g.clave_grupo}-${g.materia_clave}-${i}`} className="border-t align-top">
                    <td className="px-3 py-3 text-center">
                      <span className="rounded-md bg-primary-soft px-2 py-0.5 font-mono text-xs font-medium text-primary">{g.clave_grupo}</span>
                    </td>
                    <td className="px-4 py-3">
                      <div className="font-mono text-[10px] text-muted-foreground">{g.materia_clave}</div>
                      <div className="text-sm font-medium leading-tight">{g.materia_nombre}</div>
                      <div className="mt-1 text-[11px] text-muted-foreground">{g.docente}</div>
                    </td>
                    <td className="px-3 py-3 text-center font-mono">{g.semestre}</td>
                    {DIAS.map((d) => {
                      const sesion = g.sesiones.find((s) => s.dia === d);
                      return (
                        <td key={d} className="px-2 py-3 text-center">
                          {sesion ? (
                            <div className="rounded-md bg-primary-soft px-2 py-1 text-[11px] font-medium text-primary">
                              {sesion.hora_inicio}–{sesion.hora_fin}
                              {sesion.aula && <div className="text-[10px] opacity-70">{sesion.aula}</div>}
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
            </table>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
